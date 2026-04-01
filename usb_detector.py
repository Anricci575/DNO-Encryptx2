"""
Módulo de detección de USB - DNO Encryptx
Detecta unidades USB y las gestiona
"""

import os
import sys
import time
import platform
from colors import Colors

class USBDetector:
    """Detector y gestor de unidades USB"""
    
    def __init__(self):
        self.system = platform.system()
        self.usb_devices = []
        
    def get_usb_drives(self):
        """Detectar todas las unidades USB conectadas"""
        self.usb_devices = []
        
        if self.system == "Windows":
            self._detect_windows()
        elif self.system == "Linux":
            self._detect_linux()
        elif self.system == "Darwin":  # macOS
            self._detect_mac()
        
        return self.usb_devices
    
    def _detect_windows(self):
        """Detectar USB en Windows (con fallback seguro)"""
        try:
            # Intentar usar win32api (más preciso)
            import win32api
            import win32file
            
            drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
            for drive in drives:
                drive_type = win32file.GetDriveType(drive)
                if drive_type == 2:  # DRIVE_REMOVABLE
                    try:
                        volume_info = win32api.GetVolumeInformation(drive)
                        self.usb_devices.append({
                            'drive': drive,
                            'label': volume_info[0] if volume_info[0] else f"USB {drive[0]}",
                            'serial': volume_info[1],
                            'free_space': self._get_free_space(drive)
                        })
                    except:
                        # Si falla obtener información, agregar con datos básicos
                        self.usb_devices.append({
                            'drive': drive,
                            'label': f"USB {drive[0]}",
                            'free_space': self._get_free_space(drive)
                        })
        except ImportError:
            # Fallback: si no hay win32api, usar método alternativo
            self._detect_windows_fallback()
    
    def _detect_windows_fallback(self):
        """Método alternativo para detectar USB sin win32api"""
        # Unidades USB comunes (letras D a Z)
        for letter in ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                # Intentar determinar si es USB por su tamaño o simplemente asumir
                # que las unidades extraíbles suelen ser USB
                try:
                    # En fallback, asumimos que cualquier unidad que no sea C: es potencial USB
                    if letter != 'C':  # Evitar disco duro principal
                        self.usb_devices.append({
                            'drive': drive,
                            'label': f"Unidad {letter}",
                            'free_space': self._get_free_space(drive)
                        })
                except:
                    pass
    
    def _detect_linux(self):
        """Detectar USB en Linux"""
        media_path = "/media"
        if os.path.exists(media_path):
            for item in os.listdir(media_path):
                mount_path = os.path.join(media_path, item)
                if os.path.ismount(mount_path):
                    self.usb_devices.append({
                        'drive': mount_path,
                        'label': item,
                        'mount': mount_path,
                        'free_space': self._get_free_space(mount_path)
                    })
        
        # También revisar /mnt
        mnt_path = "/mnt"
        if os.path.exists(mnt_path):
            for item in os.listdir(mnt_path):
                mount_path = os.path.join(mnt_path, item)
                if os.path.ismount(mount_path):
                    self.usb_devices.append({
                        'drive': mount_path,
                        'label': item,
                        'mount': mount_path,
                        'free_space': self._get_free_space(mount_path)
                    })
    
    def _detect_mac(self):
        """Detectar USB en macOS"""
        volumes_path = "/Volumes"
        if os.path.exists(volumes_path):
            for item in os.listdir(volumes_path):
                if item not in ['Macintosh HD', 'Recovery HD']:
                    mount_path = os.path.join(volumes_path, item)
                    if os.path.ismount(mount_path):
                        self.usb_devices.append({
                            'drive': mount_path,
                            'label': item,
                            'mount': mount_path,
                            'free_space': self._get_free_space(mount_path)
                        })
    
    def _get_free_space(self, path):
        """Obtener espacio libre en bytes"""
        try:
            if self.system == "Windows":
                # Intentar con ctypes para Windows
                try:
                    import ctypes
                    free_bytes = ctypes.c_ulonglong(0)
                    ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                        ctypes.c_wchar_p(path), None, None, ctypes.pointer(free_bytes))
                    return free_bytes.value
                except:
                    # Fallback: usar os.statvfs no funciona en Windows, devolver 0
                    return 0
            else:
                # Linux/Mac
                stat = os.statvfs(path)
                return stat.f_frsize * stat.f_bavail
        except:
            return 0
    
    def format_size(self, bytes):
        """Formatear tamaño de bytes a formato legible"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.1f} PB"
    
    def select_usb(self):
        """Mostrar USBs disponibles y permitir seleccionar uno"""
        self.get_usb_drives()
        
        if not self.usb_devices:
            print(f"\n{Colors.RED}[!] No se encontraron unidades USB{Colors.RESET}")
            print(f"{Colors.YELLOW}[!] Asegúrate de tener un USB conectado{Colors.RESET}")
            return None
        
        print(f"\n{Colors.CYAN}┌{'─' * 65}┐{Colors.RESET}")
        print(f"{Colors.CYAN}│{Colors.BOLD}{Colors.GREEN}   UNIDADES USB DETECTADAS{' ' * 44}{Colors.CYAN}│{Colors.RESET}")
        print(f"{Colors.CYAN}├{'─' * 65}┤{Colors.RESET}")
        
        for i, usb in enumerate(self.usb_devices, 1):
            free_space = self.format_size(usb['free_space'])
            label = usb.get('label', f"USB {usb['drive'][0]}")
            print(f"{Colors.CYAN}│{Colors.RESET} {Colors.YELLOW}{i:2}.{Colors.RESET} {Colors.GREEN}{usb['drive']:<12}{Colors.RESET} "
                  f"[{label:<15}] - Libre: {free_space:<10} {Colors.CYAN}│{Colors.RESET}")
        
        print(f"{Colors.CYAN}└{'─' * 65}┘{Colors.RESET}")
        
        try:
            choice = input(f"\n{Colors.CYAN}[?] Selecciona USB (1-{len(self.usb_devices)}): {Colors.RESET}")
            idx = int(choice) - 1
            if 0 <= idx < len(self.usb_devices):
                return self.usb_devices[idx]
        except:
            pass
        
        return None
    
    def is_installed_on_usb(self):
        """Verificar si el programa está instalado en un USB"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return self.is_usb_path(current_dir)
    
    def is_usb_path(self, path):
        """Verificar si una ruta está en una unidad USB"""
        if self.system == "Windows":
            try:
                drive = os.path.splitdrive(path)[0] + "\\"
                # Intentar con win32file si está disponible
                try:
                    import win32file
                    return win32file.GetDriveType(drive) == 2
                except ImportError:
                    # Fallback: asumir que unidades que no son C: son USB
                    return drive.upper() != "C:\\"
            except:
                return False
        elif self.system == "Linux":
            return '/media/' in path or '/mnt/' in path
        elif self.system == "Darwin":
            return '/Volumes/' in path
        return False
    
    def get_usb_info(self):
        """Obtener información detallada de los USBs detectados"""
        self.get_usb_drives()
        info = []
        for usb in self.usb_devices:
            info.append({
                'drive': usb['drive'],
                'label': usb.get('label', 'Desconocido'),
                'free_space_gb': usb['free_space'] / (1024**3) if usb['free_space'] else 0,
                'free_space_str': self.format_size(usb['free_space']),
                'is_usb': True
            })
        return info