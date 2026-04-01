"""
Módulo de Cifrado de Archivos - DNO Encryptx
File Vault - Encripta y desencripta archivos físicos
"""

import os
import sys
import shutil
import hashlib
import base64
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import mimetypes

class FileVault:
    """Sistema de cifrado de archivos físicos"""
    
    # Extensiones soportadas para visualización
    SUPPORTED_EXTENSIONS = {
        'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.webp'],
        'document': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
        'code': ['.py', '.js', '.html', '.css', '.json', '.xml', '.yaml', '.sh', '.bat'],
        'compressed': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'other': []
    }
    
    # Iconos por tipo
    FILE_ICONS = {
        'image': '🖼️',
        'document': '📄',
        'code': '💻',
        'compressed': '📦',
        'other': '📁'
    }
    
    def __init__(self, crypto_manager, vault_dir="FileVault"):
        """
        Inicializar File Vault
        
        Args:
            crypto_manager: Gestor de encriptación principal
            vault_dir: Directorio donde se guardarán los archivos encriptados
        """
        self.crypto = crypto_manager
        self.vault_dir = vault_dir
        self.vault_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), vault_dir)
        self._ensure_vault_dir()
        
    def _ensure_vault_dir(self):
        """Asegurar que existe el directorio de la bóveda"""
        if not os.path.exists(self.vault_path):
            os.makedirs(self.vault_path)
    
    def _get_file_type(self, filename):
        """Determinar el tipo de archivo por extensión"""
        ext = os.path.splitext(filename)[1].lower()
        for file_type, extensions in self.SUPPORTED_EXTENSIONS.items():
            if ext in extensions:
                return file_type
        return 'other'
    
    def _get_file_icon(self, file_type):
        """Obtener icono según tipo de archivo"""
        return self.FILE_ICONS.get(file_type, '📁')
    
    def _generate_key_from_password(self, password, salt=None):
        """Generar clave a partir de contraseña (para archivos compartidos)"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def encrypt_file(self, file_path, output_name=None, use_master_key=True, custom_password=None):
        """
        Encriptar un archivo
        
        Args:
            file_path: Ruta del archivo a encriptar
            output_name: Nombre del archivo encriptado (opcional)
            use_master_key: Usar la clave maestra del programa
            custom_password: Contraseña personalizada (si no se usa master key)
        
        Returns:
            tuple: (success, message, output_path)
        """
        if not os.path.exists(file_path):
            return False, f"Archivo no encontrado: {file_path}", None
        
        try:
            # Leer archivo original
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Generar clave
            if use_master_key:
                cipher = self.crypto.cipher
                if cipher is None:
                    return False, "Clave maestra no disponible", None
            else:
                if not custom_password:
                    return False, "Se requiere contraseña personalizada", None
                key, salt = self._generate_key_from_password(custom_password)
                cipher = Fernet(key)
            
            # Encriptar datos
            encrypted_data = cipher.encrypt(file_data)
            
            # Preparar metadatos
            original_name = os.path.basename(file_path)
            file_type = self._get_file_type(original_name)
            
            # Crear archivo de metadatos
            metadata = {
                'original_name': original_name,
                'original_size': len(file_data),
                'encrypted_size': len(encrypted_data),
                'file_type': file_type,
                'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'use_master_key': use_master_key
            }
            
            # Si se usó contraseña personalizada, guardar salt
            if not use_master_key and custom_password:
                metadata['salt'] = base64.b64encode(salt).decode()
            
            # 🛠️ LÓGICA NINJA: Si pones nombre personalizado, NO se le agrega extensión.
            # Se guardará exactamente como lo escribas (ej: "archivo_secreto" sin .dno)
            if output_name:
                output_filename = output_name
            else:
                name_without_ext = os.path.splitext(original_name)[0]
                output_filename = f"{name_without_ext}.dno"
            
            output_path = os.path.join(self.vault_path, output_filename)
            
            # Guardar archivo encriptado
            with open(output_path, 'wb') as f:
                # Guardar metadatos primero (JSON encriptado)
                import json
                metadata_json = json.dumps(metadata).encode()
                metadata_len = len(metadata_json).to_bytes(4, 'big')
                f.write(metadata_len)
                f.write(metadata_json)
                f.write(encrypted_data)
            
            return True, f"Archivo encriptado: {output_filename}", output_path
            
        except Exception as e:
            return False, f"Error al encriptar: {e}", None
    
    def decrypt_file(self, encrypted_path, output_dir=None, custom_password=None):
        """
        Desencriptar un archivo .dno
        """
        if not os.path.exists(encrypted_path):
            return False, f"Archivo no encontrado: {encrypted_path}", None
        
        try:
            with open(encrypted_path, 'rb') as f:
                # Leer metadatos
                metadata_len = int.from_bytes(f.read(4), 'big')
                metadata_json = f.read(metadata_len)
                import json
                metadata = json.loads(metadata_json.decode())
                
                # Leer datos encriptados
                encrypted_data = f.read()
            
            # Descifrar según método
            if metadata.get('use_master_key', True):
                cipher = self.crypto.cipher
                if cipher is None:
                    return False, "Clave maestra no disponible", None
            else:
                if not custom_password:
                    return False, "Se requiere contraseña personalizada", None
                salt = base64.b64decode(metadata.get('salt', ''))
                key, _ = self._generate_key_from_password(custom_password, salt)
                cipher = Fernet(key)
            
            # Desencriptar
            decrypted_data = cipher.decrypt(encrypted_data)
            
            # Determinar nombre de salida
            original_name = metadata['original_name']
            if output_dir:
                output_path = os.path.join(output_dir, original_name)
            else:
                output_path = os.path.join(self.vault_path, "decrypted", original_name)
            
            # Asegurar directorio de salida
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Guardar archivo desencriptado
            with open(output_path, 'wb') as f:
                f.write(decrypted_data)
            
            return True, f"Archivo desencriptado: {original_name}", output_path
            
        except Exception as e:
            return False, f"Error al desencriptar (Verifica la contraseña): {e}", None
    
    def list_vault_files(self):
        """Listar todos los archivos en la bóveda (Solo los que terminan en .dno)"""
        files = []
        if not os.path.exists(self.vault_path):
            return files
        
        for filename in os.listdir(self.vault_path):
            if filename.endswith('.dno'):
                file_path = os.path.join(self.vault_path, filename)
                try:
                    # Leer metadatos
                    with open(file_path, 'rb') as f:
                        metadata_len = int.from_bytes(f.read(4), 'big')
                        metadata_json = f.read(metadata_len)
                        import json
                        metadata = json.loads(metadata_json.decode())
                    
                    file_type = metadata.get('file_type', 'other')
                    icon = self._get_file_icon(file_type)
                    size_mb = metadata.get('encrypted_size', 0) / (1024 * 1024)
                    
                    files.append({
                        'filename': filename,
                        'original_name': metadata.get('original_name', filename),
                        'file_type': file_type,
                        'icon': icon,
                        'size_mb': size_mb,
                        'created': metadata.get('created', 'N/A'),
                        'use_master_key': metadata.get('use_master_key', True),
                        'path': file_path
                    })
                except:
                    # Archivo corrupto o formato incorrecto
                    files.append({
                        'filename': filename,
                        'original_name': filename.replace('.dno', ''),
                        'file_type': 'other',
                        'icon': '⚠️',
                        'size_mb': 0,
                        'created': 'N/A',
                        'use_master_key': True,
                        'path': file_path,
                        'error': True
                    })
        
        return sorted(files, key=lambda x: x['created'], reverse=True)
    
    def delete_file(self, filename):
        """Eliminar archivo de la bóveda"""
        file_path = os.path.join(self.vault_path, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True, f"Archivo {filename} eliminado"
        return False, "Archivo no encontrado"
    
    def get_vault_info(self):
        """Obtener información de la bóveda"""
        files = self.list_vault_files()
        total_size = sum(f.get('size_mb', 0) for f in files)
        
        by_type = {}
        for f in files:
            file_type = f.get('file_type', 'other')
            by_type[file_type] = by_type.get(file_type, 0) + 1
        
        return {
            'total_files': len(files),
            'total_size_mb': total_size,
            'by_type': by_type,
            'vault_path': self.vault_path
        }
    
    def get_file_info(self, filename):
        """Obtener información detallada de un archivo"""
        files = self.list_vault_files()
        for f in files:
            if f['filename'] == filename:
                return f
        return None