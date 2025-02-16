import base64
from cryptography.fernet import Fernet
from keyrings.alt.file import PlaintextKeyring
import logging

class KeyManager:
    def __init__(self):
        self.SERVICE_NAME = "SecureClipboard"
        self.KEY_NAME = "encryption_key"
        self.keyring = PlaintextKeyring()
        logging.info("Initialized KeyManager with PlaintextKeyring backend")

    def generate_new_key(self):
        """Generate and store a new encryption key"""
        try:
            key = Fernet.generate_key()
            self.keyring.set_password(self.SERVICE_NAME, self.KEY_NAME, key.decode())
            logging.info("Successfully generated and stored new encryption key")
            return key
        except Exception as e:
            logging.error(f"Error generating new key: {e}")
            return None

    def get_encryption_key(self):
        """Retrieve the stored encryption key"""
        try:
            key = self.keyring.get_password(self.SERVICE_NAME, self.KEY_NAME)
            if key:
                logging.info("Successfully retrieved encryption key")
                return key.encode()
            logging.warning("No encryption key found")
            return None
        except Exception as e:
            logging.error(f"Error retrieving key: {e}")
            return None

    def delete_key(self):
        """Delete the stored encryption key"""
        try:
            self.keyring.delete_password(self.SERVICE_NAME, self.KEY_NAME)
            logging.info("Successfully deleted encryption key")
            return True
        except Exception as e:
            logging.error(f"Error deleting key: {e}")
            return False