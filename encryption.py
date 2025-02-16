import base64
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from key_manager import KeyManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Encryption:
    def __init__(self):
        self.key_manager = KeyManager()
        self.fernet = None
        self.initialize_fernet()
        logging.info("Encryption module initialized")

    def initialize_fernet(self):
        """Initialize Fernet with the stored key"""
        key = self.key_manager.get_encryption_key()
        if key:
            self.fernet = Fernet(key)
            logging.info("Fernet initialized with stored key")
        else:
            logging.warning("No encryption key found")

    def encrypt(self, text):
        """Encrypt the given text"""
        try:
            if not self.fernet:
                logging.info("Reinitializing Fernet for encryption")
                self.initialize_fernet()

            if not isinstance(text, bytes):
                text = text.encode()

            encrypted = self.fernet.encrypt(text)
            result = base64.urlsafe_b64encode(encrypted).decode()
            logging.info("Text encrypted successfully")
            return result
        except Exception as e:
            logging.error(f"Encryption error: {e}")
            return None

    def decrypt(self, encrypted_text):
        """Decrypt the given text"""
        try:
            if not self.fernet:
                logging.info("Reinitializing Fernet for decryption")
                self.initialize_fernet()

            encrypted_bytes = base64.urlsafe_b64decode(encrypted_text)
            decrypted = self.fernet.decrypt(encrypted_bytes)
            result = decrypted.decode()
            logging.info("Text decrypted successfully")
            return result
        except Exception as e:
            logging.error(f"Decryption error: {e}")
            return None

    def is_encrypted(self, text):
        """Check if the text is encrypted"""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(text)
            self.fernet.decrypt(encrypted_bytes)
            return True
        except:
            return False