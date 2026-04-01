#!/bin/bash
# DNO-Encryptx Startup Script

echo "========================================"
echo "   DNO-Encryptx v2.0 - HACKER EDITION"
echo "   Cargando sistema seguro..."
echo "========================================"
echo

cd "$(dirname "$0")"
python3 main.py

if [ $? -ne 0 ]; then
    echo
    echo "[ERROR] Python no encontrado"
    echo "Instala Python 3 desde tu gestor de paquetes"
    read -p "Presiona Enter para salir..."
fi