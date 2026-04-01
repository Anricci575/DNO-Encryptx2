"""
Módulo de efectos UI - DNO Encryptx
"""

import sys
import time
from colors import Colors

class UIEffects:
    """Efectos visuales para la terminal"""
    
    @staticmethod
    def typewriter(text, delay=0.02, color=Colors.GREEN):
        """Efecto de escritura tipo máquina"""
        for char in text:
            sys.stdout.write(f"{color}{char}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    @staticmethod
    def loading(text="PROCESSING", duration=1, color=Colors.CYAN):
        """Animación de carga con spinner"""
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        end_time = time.time() + duration
        i = 0
        while time.time() < end_time:
            sys.stdout.write(f"\r{color}[{frames[i % len(frames)]}] {text}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(0.05)
            i += 1
        print()
    
    @staticmethod
    def progress_bar(progress, total, width=50):
        """Barra de progreso"""
        percent = progress / total
        filled = int(width * percent)
        bar = '█' * filled + '░' * (width - filled)
        sys.stdout.write(f'\r{Colors.CYAN}[{bar}]{Colors.RESET} {percent:.1%}')
        sys.stdout.flush()
        if progress == total:
            print()
    
    @staticmethod
    def clear_screen():
        """Limpiar pantalla"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_box(text, color=Colors.CYAN, width=70):
        """Imprimir texto en un recuadro"""
        print(f"{color}{'┌' + '─' * (width-2) + '┐'}{Colors.RESET}")
        lines = text.split('\n')
        for line in lines:
            padding = width - len(line) - 2
            print(f"{color}│{Colors.RESET}{line}{' ' * padding}{color}│{Colors.RESET}")
        print(f"{color}{'└' + '─' * (width-2) + '┘'}{Colors.RESET}")