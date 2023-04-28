import base64
import json
import urllib.parse
from abc import ABC, abstractmethod


class Config(ABC):
    @abstractmethod
    def get(self, uuid: str) -> str:
        pass


class URLConfig(Config):
    remark: str
    protocol: str
    server: str
    port: int
    params: dict

    def __init__(self, remark: str, protocol: str, server: str, port: int, **params):
        self.remark = remark
        self.protocol = protocol
        self.server = server
        self.port = port
        self.params = params

    def get(self, uuid: str) -> str:
        url = f'{self.protocol}://{uuid}@{self.server}:{self.port}'
        encoded_params = urllib.parse.urlencode(self.params)
        url = url + "?" + encoded_params
        return f'{url}#{self.remark}'


class JSONConfig(Config):
    protocol: str
    params: dict

    def __init__(self, protocol: str, **params):
        self.protocol = protocol
        self.params = params

    def get(self, uuid: str) -> str:
        j = json.dumps({
            'id': uuid,
            **self.params
        })
        return f"{self.protocol}://{base64.b64encode(j.encode('ascii')).decode('ascii')}"


class VMESSConfig(JSONConfig):

    def __init__(self, remark: str, server: str, port: int, **params):
        super().__init__(protocol='vmess', v=2, ps=remark, add=server, port=port, aid=0, **params)


class VLESSConfig(URLConfig):

    def __init__(self, remark: str, server: str, port: int, **params):
        super().__init__(remark=remark, protocol='vless', server=server, port=port, **params)


class VMESSWebSocketConfig(VMESSConfig):

    def __init__(self, remark: str, server: str, port: int,
                 host: str, path: str, tls: bool, **params):
        super().__init__(
            remark=remark,
            server=server,
            port=port,
            net='ws',
            type='none',
            path=path,
            tls='tls' if tls else 'none',
            host=host,
            **params)


class VLESSRealityConfig(VLESSConfig):

    def __init__(self, remark: str, server: str, port: int,
                 sni: str, public_key: str, short_id: str, **params):
        super().__init__(
            remark=remark,
            server=server,
            port=port,
            flow='xtls-rprx-vision',
            security='reality',
            sni=sni,
            pbk=public_key,
            sid=short_id,
            type='tcp',
            headerType='none',
            **params)
