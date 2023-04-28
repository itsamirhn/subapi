import hashlib

def hash_str(uuid: str) -> str:
    return hashlib.md5(uuid.encode('utf-8')).hexdigest()
