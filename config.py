"""
Módulo de configuración - DNO Encryptx
"""

import os

class Config:
    """Configuración global del sistema"""
    
    # Archivos de datos
    DATA_FILE = "passwords.enc"
    SALT_FILE = "salt.key"
    
    # Configuración de seguridad
    SALT_SIZE = 16
    PBKDF2_ITERATIONS = 100000
    
    # Configuración de UI
    SCREEN_CLEAR = 'cls' if os.name == 'nt' else 'clear'
    
    # Límites
    MAX_LOGIN_ATTEMPTS = 3
    MIN_PASSWORD_LENGTH = 6
    
    @classmethod
    def get_data_paths(cls):
        """Retorna las rutas de los archivos de datos"""
        return {
            'data': cls.DATA_FILE,
            'salt': cls.SALT_FILE
        }