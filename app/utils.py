import base64
import json
import hashlib

from settings import ISP, PREFIX, DOMAIN, PATH


def get_vmess_ws_link(name: str, address: str, domain: str, path: str, uuid: str) -> str:
    j = json.dumps({
        "v": "2", "ps": name, "add": address, "port": "443", "id": uuid,
        "aid": "0", "net": "ws", "type": "none", "sni": domain,
        "host": domain, "path": path, "tls": "tls"
    })
    return "vmess://" + base64.b64encode(j.encode('ascii')).decode('ascii')


def generate_all_links(uuid):
    yield get_vmess_ws_link(PREFIX, DOMAIN, DOMAIN, PATH, uuid)
    for isp in ISP:
        name = PREFIX + ' - ' + isp[0]
        address = isp[1]
        yield get_vmess_ws_link(name, address, DOMAIN, PATH, uuid)


def hash_uuid(uuid: str) -> str:
    return hashlib.md5(uuid.encode('utf-8')).hexdigest()