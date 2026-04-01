"""
Módulo de criptografía - DNO Encryptx
"""

import os
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from config import Config
from colors import Colors

class CryptoManager:
    """Gestor de encriptación y desencriptación"""
    
    def __init__(self):
        self.master_key = None
        self.cipher = None
        self.data_file = Config.DATA_FILE
        self.salt_file = Config.SALT_FILE
    
    def _derive_key(self, password, salt):
        """Derivar clave de encriptación usando PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=Config.PBKDF2_ITERATIONS,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def create_master_key(self, password):
        """Crear nueva clave maestra"""
        salt = os.urandom(Config.SALT_SIZE)
        with open(self.salt_file, 'wb') as f:
            f.write(salt)
        
        self.master_key = self._derive_key(password, salt)
        self.cipher = Fernet(self.master_key)
        return True
    
    def load_master_key(self, password):
        """Cargar clave maestra existente"""
        if not os.path.exists(self.salt_file):
            return False
        
        with open(self.salt_file, 'rb') as f:
            salt = f.read()
        
        self.master_key = self._derive_key(password, salt)
        self.cipher = Fernet(self.master_key)
        return True
    
    def encrypt_data(self, data):
        """Encriptar datos"""
        if not self.cipher:
            raise Exception("Cipher not initialized")
        json_data = json.dumps(data, indent=2)
        encrypted_data = self.cipher.encrypt(json_data.encode())
        return encrypted_data
    
    def decrypt_data(self, encrypted_data):
        """Desencriptar datos"""
        if not self.cipher:
            raise Exception("Cipher not initialized")
        decrypted_data = self.cipher.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())
    
    def save_encrypted(self, data):
        """Guardar datos encriptados en archivo"""
        encrypted = self.encrypt_data(data)
        with open(self.data_file, 'wb') as f:
            f.write(encrypted)
    
    def load_encrypted(self):
        """Cargar datos encriptados desde archivo"""
        if not os.path.exists(self.data_file):
            return {}
        
        with open(self.data_file, 'rb') as f:
            encrypted_data = f.read()
        
        return self.decrypt_data(encrypted_data)