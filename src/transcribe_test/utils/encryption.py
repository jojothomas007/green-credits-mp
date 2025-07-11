import os
import logging
import sys
from cryptography.fernet import Fernet
import hashlib
import base64

# Set up logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

class Crypt:
    def __init__(self):
        self.cipher:Fernet = Fernet(self.__generate_encryption_key())

    def encrypt(self, message:str):
        encrypted_message = self.cipher.encrypt(message.encode())
        return encrypted_message

    def decrypt(self, encrypted_message:str):
        decrypted_message = self.cipher.decrypt(encrypted_message).decode()
        return decrypted_message
    
    def __generate_encryption_key(self):
        """
        Generate an encryption key based on the Windows username.
        """
        # Get the Windows username
        username = os.getenv("USERNAME")
        # Combine with a salt (to make the key more secure)
        salt = "4d2f8c3a9b6e1f7c8e9a2b4c3d7f6e1c"
        key_material = (username + salt).encode()
        # Use a hashing algorithm (e.g., SHA256) to generate a 32-byte key
        hashed_key = hashlib.sha256(key_material).digest()
        # Fernet requires a base64-encoded key, so encode it
        encryption_key = base64.urlsafe_b64encode(hashed_key[:32])    
        return encryption_key
