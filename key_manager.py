import keyring
import base64
from cryptography.fernet import Fernet

class KeyManager:
    def __init__(self):
        self.SERVICE_NAME = "SecureClipboard"
        self.KEY_NAME = "encryption_key"

    def generate_new_key(self):
        """Generate and store a new encryption key"""
        try:
            key = Fernet.generate_key()
            keyring.set_password(self.SERVICE_NAME, self.KEY_NAME, key.decode())
            return key
        except Exception as e:
            print(f"Error generating new key: {e}")
            return None

    def get_encryption_key(self):
        """Retrieve the stored encryption key"""
        try:
            key = keyring.get_password(self.SERVICE_NAME, self.KEY_NAME)
            if key:
                return key.encode()
            return None
        except Exception as e:
            print(f"Error retrieving key: {e}")
            return None

    def delete_key(self):
        """Delete the stored encryption key"""
        try:
            keyring.delete_password(self.SERVICE_NAME, self.KEY_NAME)
            return True
        except Exception as e:
            print(f"Error deleting key: {e}")
            return False
