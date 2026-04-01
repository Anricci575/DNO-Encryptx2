"""
Script de auto-inicio - DNO Encryptx
Se ejecuta automáticamente al conectar el USB
"""

import os
import sys
import platform

def check_and_run():
    """Verificar y ejecutar el programa principal"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_file = os.path.join(current_dir, "main.py")
    
    if os.path.exists(main_file):
        # Ejecutar el programa principal
        import subprocess
        subprocess.run([sys.executable, main_file])
    else:
        print("[!] Error: No se encuentra el programa principal")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    check_and_run()