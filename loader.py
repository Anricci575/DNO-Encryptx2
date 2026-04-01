"""
DNO-Encryptx v2.0 - Loader (Sin Rastro)
Ejecuta el programa completamente en memoria RAM
No deja rastros en la computadora anfitriona
"""

import os
import sys
import base64
import tempfile
import subprocess
import platform
import ctypes
import shutil
from cryptography.fernet import Fernet
import hashlib

class StealthLoader:
    """Cargador sigiloso que ejecuta todo en RAM"""
    
    def __init__(self):
        self.system = platform.system()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        
    def hide_console(self):
        """Ocultar la ventana de consola (Windows)"""
        if self.system == "Windows":
            try:
                # Ocultar ventana de consola
                wh = ctypes.windll.kernel32.GetConsoleWindow()
                if wh:
                    ctypes.windll.user32.ShowWindow(wh, 0)  # 0 = SW_HIDE
            except:
                pass
    
    def show_console(self):
        """Mostrar la ventana de consola"""
        if self.system == "Windows":
            try:
                wh = ctypes.windll.kernel32.GetConsoleWindow()
                if wh:
                    ctypes.windll.user32.ShowWindow(wh, 5)  # 5 = SW_SHOW
            except:
                pass
    
    def execute_in_memory(self, python_code, filename="<memory>"):
        """Ejecutar código Python directamente en memoria"""
        try:
            # Compilar y ejecutar en memoria
            compiled = compile(python_code, filename, 'exec')
            exec(compiled, globals(), locals())
            return True
        except Exception as e:
            print(f"Error ejecutando código en memoria: {e}")
            return False
    
    def decrypt_payload(self, encrypted_payload, password):
        """Desencriptar el payload en memoria"""
        try:
            # Derivar clave
            key = hashlib.sha256(password.encode()).digest()
            key = base64.urlsafe_b64encode(key)
            cipher = Fernet(key)
            
            # Desencriptar
            decrypted = cipher.decrypt(encrypted_payload)
            return decrypted.decode('utf-8')
        except Exception as e:
            print(f"Error desencriptando payload: {e}")
            return None
    
    def read_encrypted_payload(self):
        """Leer el payload encriptado desde el USB"""
        payload_path = os.path.join(self.current_dir, "encrypted_payload.bin")
        if not os.path.exists(payload_path):
            print("[!] Payload encriptado no encontrado")
            return None
        
        with open(payload_path, 'rb') as f:
            return f.read()
    
    def run_without_trace(self):
        """Ejecutar el programa sin dejar rastro"""
        self.hide_console()
        
        print("=" * 60)
        print("   DNO-Encryptx - Stealth Mode")
        print("   Ejecutando desde RAM - Sin dejar rastro")
        print("=" * 60)
        
        # Solicitar contraseña de desencriptación del payload
        import getpass
        password = getpass.getpass("\n[?] Contraseña del payload: ")
        
        # Leer y desencriptar payload
        encrypted = self.read_encrypted_payload()
        if not encrypted:
            return
        
        code = self.decrypt_payload(encrypted, password)
        if not code:
            print("[!] Contraseña incorrecta o payload corrupto")
            input("\nPresiona Enter para salir...")
            return
        
        # Ejecutar en memoria
        print("[✓] Payload desencriptado en RAM")
        print("[✓] Ejecutando programa desde memoria...")
        print("-" * 60)
        
        self.show_console()
        
        # Ejecutar el código en memoria
        self.execute_in_memory(code)
        
        # Al terminar, limpiar
        self.hide_console()
        print("\n[✓] Programa finalizado - No se dejaron rastros")
        time.sleep(2)


def create_encrypted_payload():
    """Crear el payload encriptado (ejecutar solo durante la instalación)"""
    import zipfile
    import json
    
    # Lista de archivos a empaquetar
    files_to_pack = [
        'config.py', 'colors.py', 'banner.py', 'crypto_manager.py',
        'password_manager.py', 'ui_effects.py', 'menus.py',
        'language_manager.py', 'usb_detector.py', 'installer.py',
        'locales/es.json', 'locales/en.json'
    ]
    
    # Crear un archivo ZIP en memoria
    import io
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file in files_to_pack:
            if os.path.exists(file):
                zip_file.write(file)
                print(f"   ✓ {file}")
    
    # Convertir a string base64 para empaquetar
    zip_data = zip_buffer.getvalue()
    
    # Crear el código del launcher que descomprime y ejecuta
    launcher_code = f'''
import sys
import os
import zipfile
import io
import base64
import tempfile
import shutil

# Datos del payload encriptado (ZIP en base64)
PAYLOAD_DATA = {repr(base64.b64encode(zip_data).decode())}

def execute_from_memory():
    """Descomprimir y ejecutar desde memoria"""
    # Decodificar base64
    zip_data = base64.b64decode(PAYLOAD_DATA)
    
    # Crear un archivo ZIP en memoria
    zip_buffer = io.BytesIO(zip_data)
    
    # Descomprimir en memoria
    with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
        # Extraer archivos a memoria (no a disco)
        files = {{}}
        for file_info in zip_file.infolist():
            files[file_info.filename] = zip_file.read(file_info.filename)
    
    # Importar el módulo principal desde memoria
    import importlib.util
    
    # Crear un módulo temporal en memoria
    spec = importlib.util.spec_from_loader('main', loader=None)
    main_module = importlib.util.module_from_spec(spec)
    
    # Ejecutar el código en el módulo
    if 'main.py' in files:
        exec(files['main.py'].decode('utf-8'), main_module.__dict__)
    
    return True

if __name__ == "__main__":
    execute_from_memory()
'''
    
    return launcher_code


if __name__ == "__main__":
    # Si se ejecuta directamente, crear el payload encriptado
    if len(sys.argv) > 1 and sys.argv[1] == "--create-payload":
        print("[*] Creando payload encriptado...")
        code = create_encrypted_payload()
        with open("encrypted_payload.bin", "w") as f:
            f.write(code)
        print("[✓] Payload creado: encrypted_payload.bin")
    else:
        # Ejecutar el cargador
        loader = StealthLoader()
        loader.run_without_trace()