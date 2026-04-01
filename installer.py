"""
Módulo de instalación en USB - DNO Encryptx
Soporte para modo MAESTRO (virgen) y modo ESCLAVO (con datos)
"""

import os
import sys
import shutil
import platform
import base64
import zipfile
import io
from datetime import datetime

# Colores simples por si no existe colors.py
class _Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# Intentar importar colors reales
try:
    from colors import Colors
except ImportError:
    Colors = _Colors

class USBInstaller:
    """Instalador del programa en USB con copia de datos"""
    
    def __init__(self):
        self.system = platform.system()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
    
    def install_on_usb(self, usb_path, mode="esclavo"):
        """
        Instalar el programa en el USB seleccionado
        
        Args:
            usb_path: Ruta del USB
            mode: "maestro" (virgen) o "esclavo" (con datos)
        """
        print(f"\n{Colors.CYAN}{'═' * 70}{Colors.RESET}")
        
        if mode == "maestro":
            print(f"{Colors.BOLD}{Colors.GREEN}   👑 INSTALANDO MODO MAESTRO (Virgen){Colors.RESET}")
            print(f"{Colors.DIM}   • Programa limpio para otra persona{Colors.RESET}")
            print(f"{Colors.DIM}   • Sin tus datos personales{Colors.RESET}")
            print(f"{Colors.DIM}   • La otra persona creará sus propias contraseñas{Colors.RESET}")
        else:
            print(f"{Colors.BOLD}{Colors.GREEN}   🔗 INSTALANDO MODO ESCLAVO (Con tus datos){Colors.RESET}")
            print(f"{Colors.DIM}   • Llevas TODAS tus contraseñas, notas y archivos{Colors.RESET}")
            print(f"{Colors.DIM}   • Funciona en cualquier PC con Python{Colors.RESET}")
        
        print(f"{Colors.CYAN}{'═' * 70}{Colors.RESET}")
        
        # Directorio de instalación
        install_path = os.path.join(usb_path, "DNO-Encryptx")
        
        # Verificar si ya existe
        if os.path.exists(install_path):
            print(f"{Colors.YELLOW}[!] El programa ya está instalado en este USB{Colors.RESET}")
            overwrite = input(f"{Colors.CYAN}[?] ¿Sobrescribir? (s/n): {Colors.RESET}").lower()
            if overwrite != 's':
                return False
            shutil.rmtree(install_path)
            print(f"{Colors.GREEN}[✓] Directorio anterior eliminado{Colors.RESET}")
        
        # Crear directorio
        os.makedirs(install_path)
        print(f"{Colors.GREEN}[✓] Directorio creado: {install_path}{Colors.RESET}")
        
        # ========== 1. COPIAR ARCHIVOS DEL PROGRAMA ==========
        # LÓGICA DINÁMICA: Obtener todos los archivos .py de la carpeta actual
        all_files = [f for f in os.listdir(self.current_dir) if f.endswith('.py')]
        all_files.extend(['startup.bat', 'startup.sh', 'requirements.txt'])
        
        print(f"\n{Colors.CYAN}[+] Copiando archivos del programa...{Colors.RESET}")
        copied = 0
        missing = 0
        
        for file in all_files:
            src = os.path.join(self.current_dir, file)
            dst = os.path.join(install_path, file)
            if os.path.exists(src):
                shutil.copy2(src, dst)
                print(f"   {Colors.GREEN}✓{Colors.RESET} {file}")
                copied += 1
            else:
                print(f"   {Colors.YELLOW}⚠{Colors.RESET} {file} (no encontrado, omitiendo)")
                missing += 1
        
        # Copiar carpeta locales
        locales_src = os.path.join(self.current_dir, 'locales')
        locales_dst = os.path.join(install_path, 'locales')
        if os.path.exists(locales_src):
            if os.path.exists(locales_dst):
                shutil.rmtree(locales_dst)
            shutil.copytree(locales_src, locales_dst)
            print(f"   {Colors.GREEN}✓{Colors.RESET} locales/ (carpeta completa)")
        
        # ========== 2. COPIAR DATOS GUARDADOS (CONTRASEÑAS, NOTAS Y BÓVEDA) ==========
        data_copied = 0
        
        if mode == "esclavo":
            print(f"\n{Colors.CYAN}[+] Copiando TUS datos guardados...{Colors.RESET}")
            
            data_files = ['passwords.enc', 'salt.key', 'preferences.json', 'secure_notes.enc', 'notifications.json', 'categories.json']
            
            for data_file in data_files:
                src = os.path.join(self.current_dir, data_file)
                dst = os.path.join(install_path, data_file)
                if os.path.exists(src):
                    shutil.copy2(src, dst)
                    print(f"   {Colors.GREEN}✓{Colors.RESET} {data_file} (datos migrados)")
                    data_copied += 1
                else:
                    print(f"   {Colors.YELLOW}⚠{Colors.RESET} {data_file} (no hay datos previos)")
            
            # 📁 COPIAR CARPETA FILE VAULT (ARCHIVOS FÍSICOS)
            vault_src = os.path.join(self.current_dir, 'FileVault')
            vault_dst = os.path.join(install_path, 'FileVault')
            if os.path.exists(vault_src):
                if os.path.exists(vault_dst):
                    shutil.rmtree(vault_dst)
                shutil.copytree(vault_src, vault_dst)
                print(f"   {Colors.GREEN}✓{Colors.RESET} FileVault/ (Bóveda de archivos encriptados)")
                data_copied += 1
            else:
                print(f"   {Colors.YELLOW}⚠{Colors.RESET} FileVault/ (La bóveda de archivos está vacía)")

            if data_copied > 0:
                print(f"\n{Colors.GREEN}[✓] Se copiaron archivos y bóvedas con tus datos{Colors.RESET}")
            else:
                print(f"\n{Colors.YELLOW}[!] No hay datos previos para copiar{Colors.RESET}")
        else:
            print(f"\n{Colors.CYAN}[+] Modo MAESTRO - Instalación limpia (sin datos){Colors.RESET}")
            print(f"   {Colors.DIM}• La persona que use este USB creará sus propias contraseñas{Colors.RESET}")
        
        # ========== 3. CREAR ARCHIVO DE IDENTIFICACIÓN DEL MODO ==========
        self._create_mode_file(install_path, mode)
        
        # ========== 4. CREAR SCRIPT DE INICIO EN LA RAÍZ ==========
        self._create_root_startup(usb_path, install_path, mode)
        
        # ========== 5. CREAR AUTORUN.INF ==========
        self._create_autorun(usb_path, mode)
        
        # ========== 6. CREAR INSTALADOR DE DEPENDENCIAS ==========
        self._create_dependency_installer(install_path)
        
        # ========== 7. CREAR SCRIPT DE SINCRONIZACIÓN ==========
        self._create_sync_script(install_path)
        
        # ========== 8. CREAR VERSIÓN STEALTH (SIN RASTRO) ==========
        self._create_stealth_version(install_path)
        
        # ========== RESUMEN FINAL ==========
        print(f"\n{Colors.CYAN}{'─' * 70}{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}[✓] INSTALACIÓN COMPLETADA EXITOSAMENTE{Colors.RESET}")
        print(f"{Colors.CYAN}[+] Modo: {Colors.BOLD}{'👑 MAESTRO (Virgen)' if mode == 'maestro' else '🔗 ESCLAVO (Con tus datos)'}{Colors.RESET}")
        print(f"{Colors.CYAN}[+] Archivos del programa: {copied}{Colors.RESET}")
        if mode == "esclavo":
            print(f"{Colors.CYAN}[+] Archivos de datos: {data_copied}{Colors.RESET}")
        if missing > 0:
            print(f"{Colors.YELLOW}[!] Archivos omitidos: {missing} (no son críticos){Colors.RESET}")
        print(f"{Colors.CYAN}[+] Ubicación: {install_path}{Colors.RESET}")
        print(f"{Colors.CYAN}[+] Script de inicio: {usb_path}startup.bat{Colors.RESET}")
        print(f"{Colors.GREEN}[+] 🆕 MODO STEALTH: {install_path}\\startup_stealth.bat{Colors.RESET}")
        
        if mode == "maestro":
            print(f"\n{Colors.GREEN}👑 ¡USB LISTO PARA REGALAR!{Colors.RESET}")
            print(f"{Colors.GREEN}   La otra persona creará sus propias contraseñas al iniciar.{Colors.RESET}")
        else:
            print(f"\n{Colors.GREEN}🔗 ¡USB LISTO CON TUS DATOS!{Colors.RESET}")
            print(f"{Colors.GREEN}   Tus contraseñas, notas y archivos físicos están seguros en el USB.{Colors.RESET}")
            
        print(f"\n{Colors.GREEN} 🔐 OPCIONES DE ARRANQUE:{Colors.RESET}")
        print(f"{Colors.GREEN}   • Modo normal: startup.bat (deja rastro mínimo){Colors.RESET}")
        print(f"{Colors.GREEN}   • Modo stealth: startup_stealth.bat (SIN DEJAR RASTRO){Colors.RESET}")
        
        return True

    def _create_mode_file(self, install_path, mode):
        """Crear archivo que identifica el modo de instalación"""
        mode_file = os.path.join(install_path, "INSTALL_MODE.txt")
        with open(mode_file, 'w', encoding='utf-8') as f:
            f.write(f"""╔══════════════════════════════════════════════════════════════╗
║              DNO-ENCRYPTX - MODO DE INSTALACIÓN              ║
╚══════════════════════════════════════════════════════════════╝

Modo: {'👑 MAESTRO (Virgen)' if mode == 'maestro' else '🔗 ESCLAVO (Con datos)'}
Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

{'🔐 Este USB está limpio. La primera persona que lo use creará sus propias contraseñas.' if mode == 'maestro' else '🔐 Este USB contiene tus contraseñas, notas y archivos personales.'}
""")

    def _create_root_startup(self, usb_path, install_path, mode):
        """Crear script de inicio en la raíz del USB con ruta dinámica"""
        startup_path = os.path.join(usb_path, "startup.bat")
        
        if mode == "maestro":
            welcome_msg = "👑 DNO-ENCRYPTX - MODO MAESTRO (Virgen)"
            desc_msg = "     Configuración limpia para nueva instalación"
        else:
            welcome_msg = "🔗 DNO-ENCRYPTX - MODO ESCLAVO (Con tus datos)"
            desc_msg = "     Tus contraseñas seguras en el USB"
            
        with open(startup_path, 'w', encoding='utf-8') as f:
            f.write(f"""@echo off
title DNO-Encryptx - Password Manager (Portable)
color 0A
mode con: cols=80 lines=35

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║     {welcome_msg:<55}║
echo ║     {desc_msg:<55}║
echo ║     [ACCESS GRANTED] - SECURE STORAGE                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] ERROR: Python no encontrado en este sistema
    echo.
    echo [*] Para usar DNO-Encryptx necesitas Python 3.6 o superior
    echo [*] Descarga desde: https://python.org
    echo [*] Instala y marca la opcion "Add Python to PATH"
    echo.
    echo [*] O ejecuta: instalar_dependencias.bat para ayuda
    echo.
    pause
    exit /b 1
)

:: Cambiar al directorio dinámico del programa (Soporta cambio de letra USB)
cd /d "%~dp0DNO-Encryptx"

:: Verificar archivos
if not exist "main.py" (
    echo [!] ERROR: Archivos del programa no encontrados en %~dp0DNO-Encryptx
    pause
    exit /b 1
)

:: Verificar si es primera ejecución en modo maestro
if exist "INSTALL_MODE.txt" (
    findstr /C:"MAESTRO" INSTALL_MODE.txt >nul
    if not errorlevel 1 (
        if not exist "passwords.enc" (
            echo [✓] Primera ejecución en modo MAESTRO
            echo [*] Se creará una nueva base de datos para este usuario
            echo.
        )
    )
)

:: Verificar datos
if exist "passwords.enc" (
    echo [✓] Base de datos de contraseñas encontrada
) else (
    echo [!] No hay datos previos, se creará una nueva base de datos
)

echo.
echo [*] Iniciando DNO-Encryptx...
echo.
python main.py

:: Si hay error, mostrar mensaje
if errorlevel 1 (
    echo.
    echo [!] Error al ejecutar el programa
    echo [*] Verifica las dependencias con: pip install cryptography pyperclip Pillow
    echo.
    pause
)
""")
    
    def _create_autorun(self, usb_path, mode):
        """Crear archivo autorun.inf para auto-ejecución"""
        autorun_path = os.path.join(usb_path, "autorun.inf")
        
        if mode == "maestro":
            label = "DNO-Encryptx MAESTRO"
            action = "Iniciar DNO-Encryptx (Modo Virgen)"
        else:
            label = "DNO-Encryptx ESCLAVO"
            action = "Iniciar DNO-Encryptx (Tus contraseñas)"
            
        with open(autorun_path, 'w', encoding='utf-8') as f:
            f.write(f"""[AutoRun]
open=startup.bat
action={action}
icon=%SystemRoot%\\system32\\SHELL32.dll,13
label={label}
shell\\open\\command=startup.bat
shell\\open={action}
""")
    
    def _create_dependency_installer(self, install_path):
        """Crear script para instalar dependencias"""
        dep_path = os.path.join(install_path, "instalar_dependencias.bat")
        with open(dep_path, 'w', encoding='utf-8') as f:
            f.write("""@echo off
echo ===============================================================
echo    DNO-Encryptx - Instalador de Dependencias
echo ===============================================================
echo.
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python no encontrado
    echo [*] Descarga Python desde: https://python.org
    pause
    exit /b 1
)
echo [✓] Python encontrado
echo.
echo [*] Instalando dependencias necesarias...
pip install cryptography pyperclip Pillow
echo.
echo [✓] Instalacion completada
echo [*] Ahora puedes ejecutar startup.bat
pause
""")
    
    def _create_sync_script(self, install_path):
        """Crear script para sincronizar datos desde el USB a la PC"""
        sync_path = os.path.join(install_path, "sincronizar_a_pc.bat")
        with open(sync_path, 'w', encoding='utf-8') as f:
            f.write(f"""@echo off
echo ===============================================================
echo    DNO-Encryptx - Sincronizar datos a PC
echo ===============================================================
echo.
echo [*] Este script copia tus contraseñas y archivos del USB a tu PC
echo [*] Útil si quieres tener una copia local de seguridad
echo.
set /p dest="[?] Directorio destino (ej: C:\\Users\\TuUsuario\\Documentos): "

if not exist "%dest%" (
    echo [!] Directorio no existe
    pause
    exit /b 1
)

echo.
echo [*] Copiando archivos de datos...
copy /Y "passwords.enc" "%dest%\\" 2>nul && echo    ✓ passwords.enc
copy /Y "salt.key" "%dest%\\" 2>nul && echo    ✓ salt.key
copy /Y "preferences.json" "%dest%\\" 2>nul && echo    ✓ preferences.json
copy /Y "secure_notes.enc" "%dest%\\" 2>nul && echo    ✓ secure_notes.enc

echo.
echo [*] Copiando carpeta FileVault (Archivos encriptados)...
xcopy /E /I /Y "FileVault" "%dest%\\FileVault\\" 2>nul && echo    ✓ Carpeta FileVault sincronizada

echo.
echo [✓] Sincronización completada
echo [*] Tus bóvedas están ahora en: %dest%
pause
""")
    
    def _create_stealth_version(self, install_path):
        """Crear versión stealth que se ejecuta en RAM sin dejar rastro"""
        print(f"\n{Colors.CYAN}[+] Creando versión STEALTH (sin dejar rastro)...{Colors.RESET}")
        
        # Empaquetar dinámicamente TODOS los .py del install_path
        files_to_pack = [f for f in os.listdir(install_path) if f.endswith('.py')]
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file in files_to_pack:
                src = os.path.join(install_path, file)
                if os.path.exists(src):
                    zip_file.write(src, file)
                    print(f"   {Colors.GREEN}✓{Colors.RESET} Empaquetado: {file}")
                else:
                    print(f"   {Colors.YELLOW}⚠{Colors.RESET} {file} (no encontrado)")
            
            locales_path = os.path.join(install_path, 'locales')
            if os.path.exists(locales_path):
                for root, dirs, files in os.walk(locales_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.join('locales', file)
                        zip_file.write(file_path, arcname)
                        print(f"   {Colors.GREEN}✓{Colors.RESET} Empaquetado: {arcname}")
        
        zip_data = zip_buffer.getvalue()
        
        loader_code = f'''#!/usr/bin/env python3
"""
DNO-Encryptx Stealth Loader - Ejecuta desde RAM sin dejar rastro
No crea archivos temporales ni registros en la PC anfitriona
"""
import sys
import os
import zipfile
import io
import base64
import platform

PAYLOAD = {repr(base64.b64encode(zip_data).decode())}

def hide_console():
    """Ocultar consola en Windows"""
    if platform.system() == "Windows":
        try:
            import ctypes
            wh = ctypes.windll.kernel32.GetConsoleWindow()
            if wh:
                ctypes.windll.user32.ShowWindow(wh, 0)
        except:
            pass

def execute_in_memory():
    """Ejecutar todo el programa en memoria RAM"""
    try:
        zip_data = base64.b64decode(PAYLOAD)
        zip_buffer = io.BytesIO(zip_data)
        
        files = {{}}
        with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
            for file_info in zip_file.infolist():
                files[file_info.filename] = zip_file.read(file_info.filename)
        
        print("\\n" + "="*60)
        print("   DNO-Encryptx v2.0 - STEALTH MODE")
        print("   Ejecutando desde RAM - Sin dejar rastro")
        print("="*60 + "\\n")
        
        if 'main.py' in files:
            code = files['main.py'].decode('utf-8')
            
            import types
            
            main_module = types.ModuleType('__main__')
            main_module.__file__ = '<stealth_memory>'
            sys.modules['__main__'] = main_module
            
            for filename, content in files.items():
                if filename.endswith('.py') and filename != 'main.py':
                    module_name = filename.replace('.py', '').replace('/', '.')
                    module = types.ModuleType(module_name)
                    exec(content.decode('utf-8'), module.__dict__)
                    sys.modules[module_name] = module
            
            exec(code, main_module.__dict__)
            return True
        return False
    except Exception as e:
        print(f"Error en modo stealth: {{e}}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    hide_console()
    execute_in_memory()
    input("\\nPresiona Enter para salir...")
'''
        
        stealth_loader = os.path.join(install_path, "run_stealth.py")
        with open(stealth_loader, 'w', encoding='utf-8') as f:
            f.write(loader_code)
        print(f"   {Colors.GREEN}✓{Colors.RESET} Loader stealth: run_stealth.py")
        
        stealth_startup = os.path.join(install_path, "startup_stealth.bat")
        with open(stealth_startup, 'w', encoding='utf-8') as f:
            f.write(f"""@echo off
title DNO-Encryptx - Stealth Mode (Sin Rastro)
color 0A
mode con: cols=80 lines=25

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║     DNO-ENCRYPTX v2.0 - STEALTH MODE                        ║
echo ║     Ejecutando desde RAM - NO DEJA RASTRO                   ║
echo ║     Tus contraseñas seguras en el USB                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] ERROR: Python no encontrado
    echo.
    echo [*] Para modo stealth necesitas Python 3.6+
    echo [*] Descarga: https://python.org
    echo.
    pause
    exit /b 1
)

:: Cambiar al directorio dinámico
cd /d "%~dp0"

:: Verificar archivos stealth
if not exist "run_stealth.py" (
    echo [!] ERROR: Archivos stealth no encontrados
    pause
    exit /b 1
)

echo [✓] Iniciando modo stealth...
echo [*] El programa se ejecutará en memoria RAM
echo [*] Al cerrar, NO quedará rastro en este equipo
echo.
python run_stealth.py

if errorlevel 1 (
    echo.
    echo [!] Error en modo stealth
    pause
)
""")
        
        print(f"   {Colors.GREEN}✓{Colors.RESET} Script stealth: startup_stealth.bat")
        
        info_file = os.path.join(install_path, "STEALTH_INFO.txt")
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write("""╔══════════════════════════════════════════════════════════════╗
║              DNO-ENCRYPTX - MODO STEALTH                     ║
║                  SIN DEJAR RASTRO                            ║
╚══════════════════════════════════════════════════════════════╝

📌 ¿QUÉ ES EL MODO STEALTH?
───────────────────────────────────────────────────────────────
Este modo ejecuta el programa COMPLETAMENTE EN MEMORIA RAM.
Cuando cierras el programa, NO queda ningún rastro en la PC:
   • No se crean archivos temporales
   • No se escriben registros en el sistema
   • No quedan datos en el disco duro

🚀 CÓMO USARLO:
───────────────────────────────────────────────────────────────
1. Conecta el USB a cualquier computadora
2. Ejecuta: startup_stealth.bat
3. Usa el programa normalmente
4. Al cerrar, TODO se borra de la RAM

⚠️ IMPORTANTE:
───────────────────────────────────────────────────────────────
• Necesitas Python instalado en la PC (o usar Python portable)
• Las contraseñas se guardan EN EL USB (passwords.enc)
• La PC no guarda NINGUNA información

🎯 DIFERENCIA ENTRE MODOS:
───────────────────────────────────────────────────────────────
• startup.bat       → Modo normal (deja rastro mínimo)
• startup_stealth.bat → Modo stealth (SIN RASTRO)

🔐 ¡TUS CONTRASEÑAS SIEMPRE SEGURAS Y PORTÁTILES!
""")
        print(f"   {Colors.GREEN}✓{Colors.RESET} Archivo info: STEALTH_INFO.txt")
        
        return True