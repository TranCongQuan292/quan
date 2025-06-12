from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def sign_data(data, private_key_pem):
    private_key = RSA.import_key(private_key_pem)
    hash_val = SHA256.new(data)
    signature = pkcs1_15.new(private_key).sign(hash_val)
    return signature

def verify_signature(data, signature, public_key_pem):
    public_key = RSA.import_key(public_key_pem)
    hash_val = SHA256.new(data)
    try:
        pkcs1_15.new(public_key).verify(hash_val, signature)
        return True
    except (ValueError, TypeError):
        return False
