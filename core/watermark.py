import platform
import hashlib
import uuid

def system_fingerprint() -> str:
    raw = (
        platform.node() +
        platform.system() +
        platform.processor() +
        hex(uuid.getnode())
    )
    return hashlib.sha256(raw.encode()).hexdigest()
