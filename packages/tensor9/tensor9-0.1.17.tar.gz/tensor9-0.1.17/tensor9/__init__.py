import json
import os
import queue
import socket
import struct
from dataclasses import asdict, is_dataclass, dataclass
from enum import Enum
from typing import List

import errno


@dataclass
class CloudResource:
    class Type(Enum):
        AwsS3Bucket = "AwsS3Bucket"
        AwsSqsQueue = "AwsSqsQueue"

    type: Type
    value: str


@dataclass
class CloudCredential:
    class Type(Enum):
        AwsAccessKeyId = "AwsAccessKeyId"
        AwsSecretAccessKey = "AwsSecretAccessKey"
        AwsSessionToken = "AwsSessionToken"
        AwsRoleArn = "AwsRoleArn"
        AwsTrustedAccountArn = "AwsTrustedAccountArn"

        GcpAutoDetect = "GcpAutoDetect"
        GcpTrustedServiceAccountEmail = "GcpTrustedServiceAccount"
        GcpKeyJson = "GcpKeyJson"
        GcpKeyFile = "GcpKeyFile"

    type: Type
    value: str


@dataclass
class MappedCloudResource:
    resource: CloudResource
    credentials: List[CloudCredential]


@dataclass
class MetricDatum:
    metricName: str
    value: float
    unit: str


class AgentProtocol:
    class msg_type(Enum):
        Ok = "Ok"
        Err = "Err"
        GetProxyCfg = "GetProxyCfg"
        ProxyCfg = "ProxyCfg"
        GetAppliance = "GetAppliance"
        Appliance = "Appliance"
        MapResource = "MapResource"
        MappedResource = "MappedResource"
        GetCredentials = "GetCredentials"
        Credentials = "Credentials"
        PublishMetrics = "PublishMetrics"

    @dataclass
    class MapResource:
        type: CloudResource.Type
        rawResource: str

    @dataclass
    class GetCredentials:
        type: CloudResource.Type

    @dataclass
    class MappedResource:
        type: CloudResource.Type
        rawOriginal: str
        rawMapped: str

    @dataclass
    class Credentials:
        credentials: List[CloudCredential]

    @dataclass
    class PublishMetrics:
        deploymentId: str
        metricData: List[MetricDatum]


class SocketPool:
    def __init__(self, host, port, max_size, timeout):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.pool = queue.Queue(maxsize=max_size)

    def _create_socket(self):
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.settimeout(self.timeout)
        skt.connect((self.host, self.port))
        return skt

    def borrow(self):
        try:
            reused = self.pool.get_nowait()
            return reused
        except queue.Empty:
            created = self._create_socket()
            return created

    def release(self, skt):
        if not self.pool.full():
            try:
                skt.send(b'')
            except socket.error as e:
                if e.errno != errno.EAGAIN:
                    skt.close()
                    return
            skt.settimeout(self.timeout)
            self.pool.put(skt)
        else:
            skt.close()

    def close_all(self):
        while not self.pool.empty():
            skt = self.pool.get_nowait()
            if not skt:
                break
            skt.close()


def _skt_read(sock: socket.socket, size: int):
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            raise ConnectionError("Socket connection broken")
        data += packet
    return data


class Tensor9:
    agent_host: str

    def __init__(self):
        if self.is_enabled():
            print(f"Tensor9 enabled")

            self.deployment_id = os.environ.get('TENSOR9_DEPLOYMENT_ID', None)
            if not self.deployment_id:
                raise ValueError("Expected TENSOR9_DEPLOYMENT_ID environment variable to be set")

            print(f"  - Deployment id: {self.deployment_id}")

            self.agent_host = os.environ.get('TENSOR9_AGENT_HOST', "t9agent.internal")
            self.agent_port = 7782
            print(f"  - Agent endpoint: {self.agent_host}:{self.agent_port}")

            self.so_timeout = 3.0
            self.socket_pool = SocketPool(self.agent_host, self.agent_port, max_size=5, timeout=self.so_timeout)

    def i_am_running_on_prem(self):
        """Determine if the current software environment is on-premises, in a customer appliance.

        Returns:
            bool: True if running on-premises, False otherwise.
        """
        return self.is_enabled()

    def is_enabled(self):
        """Determine if the current software environment is on-premises, in a customer appliance.

        Returns:
            bool: True if running on-premises, False otherwise.
        """
        if os.environ.get('TENSOR9_ENABLED', None):
            return True
        elif os.environ.get('ON_PREM', None):
            return True
        return False

    def get_appliance(self):
        self._ensure_enabled()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            skt.settimeout(self.so_timeout)
            skt.connect((self.agent_host, self.agent_port))
            self._send_msg(skt, AgentProtocol.msg_type.GetAppliance, {})
            msg_type = self._recv_hdr(skt)

            if msg_type == AgentProtocol.msg_type.Appliance:
                appliance = self._recv_json(skt)
                return appliance
            elif msg_type == AgentProtocol.msg_type.Err:
                err = self._recv_json(skt)
                raise ValueError(f"Received error: {err}")
            else:
                raise ValueError(f"Unexpected message: {msg_type}")

    def get_http_proxy(self) -> str:
        """Fetch the Tensor9 HTTP proxy endpoint that can be used to safely communicate with the outside world.

        Returns:
            str: The Tensor9 HTTP proxy endpoint (protocol://host:port).

        Raises:
            ValueError: If there's an error in the response or an unexpected message type is received.
        """

        self._ensure_enabled()

        configured = os.environ.get('TENSOR9_HTTP_PROXY', None)
        if configured:
            return configured

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            skt.settimeout(self.so_timeout)
            skt.connect((self.agent_host, self.agent_port))
            self._send_msg(skt, AgentProtocol.msg_type.GetProxyCfg, {})
            msg_type = self._recv_hdr(skt)

            if msg_type == AgentProtocol.msg_type.ProxyCfg:
                proxyCfg = self._recv_json(skt)
                return 'http://' + proxyCfg['http']
            elif msg_type == AgentProtocol.msg_type.Err:
                err = self._recv_json(skt)
                raise ValueError(f"Received error: {err}")
            else:
                raise ValueError(f"Unexpected message: {msg_type}")

    def get_https_proxy(self) -> str:
        """Fetch the Tensor9 HTTPS proxy endpoint that can be used to safely communicate with the outside world.

        Returns:
            str: The Tensor9 HTTPS proxy endpoint (protocol://host:port).

        Raises:
            ValueError: If there's an error in the response or an unexpected message type is received.
        """

        self._ensure_enabled()

        configured = os.environ.get('TENSOR9_HTTPS_PROXY', None)
        if configured:
            return configured

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            skt.settimeout(self.so_timeout)
            skt.connect((self.agent_host, self.agent_port))
            self._send_msg(skt, AgentProtocol.msg_type.GetProxyCfg, {})
            msg_type = self._recv_hdr(skt)

            if msg_type == AgentProtocol.msg_type.ProxyCfg:
                proxyCfg = self._recv_json(skt)
                return 'http://' + proxyCfg['https']
            elif msg_type == AgentProtocol.msg_type.Err:
                err = self._recv_json(skt)
                raise ValueError(f"Received error: {err}")
            else:
                raise ValueError(f"Unexpected message: {msg_type}")

    def map_resource(self, resource: CloudResource) -> MappedCloudResource:
        self._ensure_enabled()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            skt.settimeout(self.so_timeout)
            skt.connect((self.agent_host, self.agent_port))
            self._send_msg(skt, AgentProtocol.msg_type.MapResource, self._dictify(AgentProtocol.MapResource(resource.type, resource.value.encode("utf-8").hex())))
            msg_type = self._recv_hdr(skt)

            if msg_type == AgentProtocol.msg_type.MappedResource:
                raw = AgentProtocol.MappedResource(**self._recv_json(skt))
                resource = CloudResource(raw.type, bytes.fromhex(raw.rawMapped).decode("utf-8"))
                credentials = self.get_credentials(resource)
                return MappedCloudResource(resource, credentials)
            elif msg_type == AgentProtocol.msg_type.Err:
                err = self._recv_json(skt)
                raise ValueError(f"Received error: {err}")
            else:
                raise ValueError(f"Unexpected message: {msg_type}")

    def get_credentials(self, resource: CloudResource) -> List[CloudCredential]:
        self._ensure_enabled()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            skt.settimeout(self.so_timeout)
            skt.connect((self.agent_host, self.agent_port))
            self._send_msg(skt, AgentProtocol.msg_type.GetCredentials, self._dictify(AgentProtocol.GetCredentials(resource.type)))
            msg_type = self._recv_hdr(skt)

            if msg_type == AgentProtocol.msg_type.Credentials:
                rawCredentials = AgentProtocol.Credentials(**self._recv_json(skt))
                credentials = []
                for rawCredential in rawCredentials.credentials:
                    credentials.append(CloudCredential(rawCredential['type'], bytes.fromhex(rawCredential['value']).decode("utf-8")))
                return credentials
            elif msg_type == AgentProtocol.msg_type.Err:
                err = self._recv_json(skt)
                raise ValueError(f"Received error: {err}")
            else:
                raise ValueError(f"Unexpected message: {msg_type}")

    def publish_metrics(self, metricData: List[MetricDatum]):
        """Publishes metrics for the current deployment.

        These metrics will be sent back to the corresponding facade (in the vendor's cloud) for publishing to their own metrics infrastructure.
        Published metrics will be added to the appliance's audit log.
        """
        self._ensure_enabled()
        skt = self.socket_pool.borrow()
        success = False
        try:
            self._send_msg(skt, AgentProtocol.msg_type.PublishMetrics, self._dictify(AgentProtocol.PublishMetrics(self.deployment_id, metricData)))
            msg_type = self._recv_hdr(skt)

            if msg_type == AgentProtocol.msg_type.Ok:
                ok = self._recv_json(skt)
                success = True
                return
            elif msg_type == AgentProtocol.msg_type.Err:
                err = self._recv_json(skt)
                raise ValueError(f"Received error: {err}")
            else:
                raise ValueError(f"Unexpected message: {msg_type}")
        finally:
            if success:
                self.socket_pool.release(skt)
            else:
                skt.close()

    def _ensure_enabled(self):
        if not self.is_enabled():
            raise ValueError("The Tensor9 SDK is meant to be used with software running inside a Tensor9 appliance, but it looks like we're not currently inside one.")

    def _mk_hdr(self, msg_type):
        return {"v": "V2023_08_22", "type": msg_type.name}

    def _send_msg(self, skt, msg_type, msgPayload):
        self._send_json(skt, self._mk_hdr(msg_type))
        self._send_json(skt, msgPayload)

    def _send_json(self, skt, obj):
        encoded = json.dumps(obj).encode('utf-8')
        return self._send(skt, encoded)

    def _send(self, skt, data):
        # Calculate the frame size as a big endian int32
        frameSz = struct.pack('>I', len(data))

        skt.sendall(frameSz)
        skt.sendall(data)

    def _recv_hdr(self, skt) -> AgentProtocol.msg_type:
        hdr = self._recv_json(skt)

        if hdr.get('v') != "V2023_08_22":
            raise ValueError(f"Unexpected protocol version: {hdr}")

        # Raise an error if hdr.type doesn't exist
        if 'type' not in hdr:
            raise ValueError(f"Missing 'type' in header: {hdr}")

        # Parse hdr.type as a msg_type string and parse the string into a msg_type
        try:
            msg_type = AgentProtocol.msg_type(hdr['type'])
        except ValueError:
            raise ValueError(f"Invalid msg_type value in header: {hdr['type']}")

        # Return the msg_type to the caller
        return msg_type

    def _recv_json(self, skt):
        data = self._recv(skt)
        try:
            # Parse the received data as JSON and return it
            return json.loads(data.decode('utf-8'))
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode received data as JSON: {e}")

    def _recv(self, skt):
        frameSzBuf = _skt_read(skt, 4)

        frameSz = struct.unpack('>I', frameSzBuf)[0]
        data = _skt_read(skt, frameSz)

        return data

    def _dictify(self, obj):
        if is_dataclass(obj):
            return {k: self._dictify(v) for k, v in asdict(obj).items()}
        elif isinstance(obj, Enum):
            return obj.value
        else:
            return obj
