import hashlib

def idempotency_key(provider, external_id):
    return hashlib.sha256(f"{provider}:{external_id}".encode()).hexdigest()
