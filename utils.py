import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_salt():
    """Generate a random salt for key derivation"""
    return os.urandom(16)

def derive_key(password, salt):
    """Derive a key from password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def is_base64(text):
    """Check if text is base64 encoded"""
    try:
        base64.urlsafe_b64decode(text)
        return True
    except:
        return False
