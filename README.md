# 🔐 DNO-Encryptx v2.0 - Hacker Edition

![Python Version](https://img.shields.io/badge/Python-3.6%2B-blue?style=for-the-badge&logo=python)
![Encryption](https://img.shields.io/badge/Encryption-AES%20%7C%20Fernet-red?style=for-the-badge&logo=shield)
![UI](https://img.shields.io/badge/Interface-CLI%20%7C%20GUI-brightgreen?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Stable%20Release-success?style=for-the-badge)

> **DNO-Encryptx** es una suite de ciberseguridad y gestor de contraseñas de grado militar, 100% portable y diseñada con una estética híbrida (Terminal Hacker / Interfaz Gráfica Tkinter). 

Este proyecto no es solo un gestor de credenciales; es una herramienta completa de privacidad que incluye encriptación de archivos físicos, esteganografía y ejecución en memoria volátil (RAM) anti-rastreo.

---

## 🚀 Características Principales

### 🛡️ Core de Seguridad
* **Cifrado Local Absoluto:** Todo se encripta en tu máquina. Cero servidores, cero telemetría.
* **Algoritmo Robusto:** Utiliza `cryptography.fernet` (AES en modo CBC con firma de 128-bit) derivando la clave maestra mediante **PBKDF2HMAC** y salt aleatorio.
* **Auto-destrucción en RAM:** Las rutinas de visualización procesan los datos directamente en la memoria volátil. Al cerrar la ventana, los bytes son destruidos sin tocar el disco duro.

### 🧰 Arsenal de Herramientas
* **📦 File Vault:** Encripta y desencripta archivos de cualquier tipo (.pdf, .docx, imágenes, código). Soporta clave maestra o claves personalizadas para compartir archivos de forma segura.
* **👁️ Visor Seguro RAM:** Abre archivos desencriptados (texto, código, PNG, JPG, GIF) directamente en una ventana temporal usando `io.BytesIO`. Sin rastros en la caché del sistema.
* **🖼️ Esteganografía LSB:** ¿Ocultar a simple vista? Inyecta tu base de datos completa dentro de los píxeles (Least Significant Bit) de una imagen inofensiva.
* **📝 Notas Seguras & Generador:** Almacena notas de texto libre encriptadas y genera contraseñas complejas y memorables.

### 🔌 Portabilidad USB Avanzada
* **👑 Modo Maestro:** Instala el programa "virgen" en un pendrive para regalarlo o desplegarlo en otro equipo.
* **🔗 Modo Esclavo:** Clona tu suite entera (programa + tus contraseñas + FileVault) para llevar tu vida digital en el bolsillo.
* **👻 Stealth Mode:** Crea un ejecutable que corre **100% en la memoria RAM** de la computadora anfitriona. Al retirar el USB, es como si nunca hubieras estado ahí.

---

## 🖥️ Interfaz Dual

DNO-Encryptx se adapta a tu estilo de trabajo:
1. **Modo CLI (Command Line Interface):** Menús rápidos, interactivos y con estética *Matrix/Hacker* para operar a máxima velocidad desde la consola.
2. **Modo GUI (Graphical User Interface):** Entorno visual completo construido con `Tkinter` (Dark Theme) para gestionar archivos y contraseñas de forma más cómoda e intuitiva (Tecla `[U]` desde la terminal).

---

## ⚙️ Instalación y Uso

### Requisitos previos
* Python 3.6 o superior.
* Clonar este repositorio.

### Dependencias
Instala las librerías necesarias ejecutando:
```bash
pip install cryptography pyperclip Pillow
```
⚠️ Disclaimer
Esta herramienta fue desarrollada con fines educativos y de portafolio profesional en el ámbito de la ingeniería de software y la ciberseguridad. El autor no se hace responsable por la pérdida de datos derivada del olvido de la Contraseña Maestra (no hay forma de recuperar los datos sin ella).
