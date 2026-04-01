"""
DNO-Encryptx v2.0 - HACKER EDITION
Punto de entrada principal con soporte multilenguaje y USB
"""

import sys
import time
import getpass
import os
import json  # Agregado para guardar preferencias

from steganography import Steganography # 🖼️ Nueva importación
from file_vault import FileVault # 🆕 File Vault
from notes_ui import NotesUI  # Notas seguras
from notifications import NotificationManager
from config import Config
from colors import Colors
from banner import get_banner, get_header
from ui_effects import UIEffects
from crypto_manager import CryptoManager
from password_manager import PasswordManager
from menus import MenuSystem
from language_manager import LanguageManager  # Importar gestor de idiomas
from usb_detector import USBDetector  # Importar detector USB
from stats_manager import StatsManager  # Importar el gestor de estadísticas

# Importación condicional para installer
try:
    from installer import USBInstaller
    INSTALLER_AVAILABLE = True
except ImportError:
    INSTALLER_AVAILABLE = False
    USBInstaller = None

# Importación condicional para la Interfaz Gráfica (GUI)
try:
    from gui_manager import PasswordManagerGUI
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False


class DNOEncryptx:
    """Clase principal de la aplicación"""
    
    def __init__(self):
        self.ui = UIEffects()
        self.crypto = CryptoManager()
        self.pm = None
        self.menu = None
        self.lang = LanguageManager()
        self.config_file = "preferences.json"
        self.detector = USBDetector()
        self.installer = None
        self.notes_ui = None  # Se inicializará después del login
        self.file_vault = None # 🆕 File Vault
        if INSTALLER_AVAILABLE:
            self.installer = USBInstaller()
    
    # ==================== MÉTODOS EXISTENTES ====================
    
    def check_usb_mode(self):
        """Verificar si estamos ejecutando desde USB"""
        if self.detector.is_installed_on_usb():
            self.ui.typewriter("[✓] Modo USB detectado", 0.02, Colors.GREEN)
            self.ui.typewriter("[✓] Datos almacenados en dispositivo portable", 0.02, Colors.CYAN)
            return True
        return False
    
    def install_usb_flow(self):
        """Flujo para instalar en USB (Maestro/Esclavo)"""
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("📀 INSTALAR EN USB"))
        
        if not INSTALLER_AVAILABLE or self.installer is None:
            self.ui.typewriter("[!] Módulo instalador no disponible", 0.02, Colors.RED)
            self.ui.typewriter("[!] Asegúrate de tener installer.py en la carpeta", 0.02, Colors.YELLOW)
            input(f"\n{self.lang.get('press_enter')}")
            return
            
        # Selección de Modo (Maestro vs Esclavo)
        print(f"\n{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}   TIPO DE INSTALACIÓN{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.YELLOW}[1]{Colors.RESET} 👑 Modo MAESTRO (Virgen - Programa limpio sin tus datos)")
        print(f"{Colors.YELLOW}[2]{Colors.RESET} 🔗 Modo ESCLAVO (Copia exacta con TODAS tus contraseñas)")
        
        mode_option = input(f"\n{Colors.CYAN}[?] Selecciona el modo (1-2): {Colors.RESET}").strip()
        
        if mode_option == "1":
            install_mode = "maestro"
        elif mode_option == "2":
            install_mode = "esclavo"
        else:
            self.ui.typewriter("[!] Opción inválida. Cancelando...", 0.02, Colors.RED)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        self.ui.typewriter("\n[!] Selecciona la unidad USB donde instalar el programa", 0.02, Colors.YELLOW)
        usb = self.detector.select_usb()
        if usb:
            try:
                # El instalador ahora maneja sus propios prints de éxito
                success = self.installer.install_on_usb(usb['drive'], mode=install_mode)
                if not success:
                    self.ui.typewriter("\n[!] Instalación cancelada.", 0.02, Colors.YELLOW)
            except Exception as e:
                self.ui.typewriter(f"\n[!] Error crítico durante la instalación: {e}", 0.02, Colors.RED)
        else:
            self.ui.typewriter("\n[!] No se seleccionó ninguna USB", 0.02, Colors.RED)
            
        input(f"\n{self.lang.get('press_enter')}")
    
    def create_stealth_usb(self):
        """Crear versión Stealth en USB"""
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("🎭 CREAR VERSIÓN STEALTH"))
        
        usb = self.detector.select_usb()
        if usb:
            install_path = os.path.join(usb['drive'], "DNO-Encryptx")
            if not os.path.exists(install_path):
                self.ui.typewriter("[!] Primero instala el programa normal en el USB", 0.02, Colors.RED)
            else:
                if self.installer and hasattr(self.installer, '_create_stealth_version'):
                    self.installer._create_stealth_version(install_path)
                    self.ui.typewriter(f"\n[✓] Versión Stealth creada", 0.02, Colors.GREEN)
                else:
                    self.ui.typewriter("[!] Instalador no disponible", 0.02, Colors.RED)
        else:
            self.ui.typewriter("[!] No se seleccionó ninguna USB", 0.02, Colors.RED)
            input(f"\n{self.lang.get('press_enter')}")
    
    def generate_password_flow(self):
        """Flujo para generar contraseña segura"""
        from password_generator import PasswordGenerator
        
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("🔑 GENERADOR DE CONTRASEÑAS"))
        
        print(f"\n{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}   Opciones de generación{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.YELLOW}[1]{Colors.RESET} Contraseña aleatoria")
        print(f"{Colors.YELLOW}[2]{Colors.RESET} Contraseña memorable")
        print(f"{Colors.YELLOW}[3]{Colors.RESET} Evaluar fortaleza")
        
        option = input(f"\n{Colors.CYAN}[?] Opción (1-3): {Colors.RESET}").strip()
        if option == "1":
            self._generate_random_password()
        elif option == "2":
            self._generate_memorable_password()
        elif option == "3":
            self._check_password_strength()
        else:
            self.ui.typewriter("[!] Opción inválida", 0.02, Colors.RED)
        input(f"\n{self.lang.get('press_enter')}")
    
    def _generate_random_password(self):
        from password_generator import PasswordGenerator
        print(f"\n{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}   Configuración{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        
        length_input = input(f"{Colors.CYAN}[?] Longitud (8-32) [16]: {Colors.RESET}").strip()
        length = int(length_input) if length_input.isdigit() and 8 <= int(length_input) <= 32 else 16
        use_uppercase = input(f"{Colors.CYAN}[?] MAYÚSCULAS? (s/n) [s]: {Colors.RESET}").lower() != 'n'
        use_lowercase = input(f"{Colors.CYAN}[?] minúsculas? (s/n) [s]: {Colors.RESET}").lower() != 'n'
        use_numbers = input(f"{Colors.CYAN}[?] números? (s/n) [s]: {Colors.RESET}").lower() != 'n'
        use_symbols = input(f"{Colors.CYAN}[?] símbolos? (s/n) [s]: {Colors.RESET}").lower() != 'n'
        
        password = PasswordGenerator.generate(length, use_uppercase, use_lowercase, use_numbers, use_symbols)
        
        print(f"\n{Colors.GREEN}{'─' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}   🔐 CONTRASEÑA GENERADA{Colors.RESET}")
        print(f"{Colors.GREEN}{'─' * 60}{Colors.RESET}")
        print(f"\n{Colors.BOLD}{Colors.GREEN}{password}{Colors.RESET}\n")
        
        strength = PasswordGenerator.check_strength(password)
        print(f"{Colors.YELLOW}📊 Fortaleza: {strength['strength']}{Colors.RESET}")
        self._password_options(password)
    
    def _generate_memorable_password(self):
        from password_generator import PasswordGenerator
        print(f"\n{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}   Contraseña memorable{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        
        words_input = input(f"{Colors.CYAN}[?] Palabras (3-6) [3]: {Colors.RESET}").strip()
        words = int(words_input) if words_input.isdigit() and 3 <= int(words_input) <= 6 else 3
        separator = input(f"{Colors.CYAN}[?] Separador [-]: {Colors.RESET}").strip() or '-'
        
        password = PasswordGenerator.generate_memorable(words, separator)
        
        print(f"\n{Colors.GREEN}{'─' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}   🔐 CONTRASEÑA MEMORABLE{Colors.RESET}")
        print(f"{Colors.GREEN}{'─' * 60}{Colors.RESET}")
        print(f"\n{Colors.BOLD}{Colors.GREEN}{password}{Colors.RESET}\n")
        self._password_options(password)
    
    def _check_password_strength(self):
        from password_generator import PasswordGenerator
        password = getpass.getpass(f"{Colors.CYAN}[?] Contraseña a evaluar: {Colors.RESET}")
        strength = PasswordGenerator.check_strength(password)
        print(f"\n{Colors.GREEN}{'─' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}   📊 RESULTADO{Colors.RESET}")
        print(f"{Colors.GREEN}{'─' * 60}{Colors.RESET}")
        print(f"{Colors.YELLOW}Longitud:{Colors.RESET} {strength['length']}")
        print(f"{Colors.YELLOW}Puntuación:{Colors.RESET} {strength['score']}/5")
        print(f"{Colors.YELLOW}Fortaleza:{Colors.RESET} {strength['strength']}")
    
    def _password_options(self, password):
        copy = input(f"\n{Colors.CYAN}[?] Copiar al portapapeles? (s/n): {Colors.RESET}").lower()
        if copy == 's':
            try:
                import pyperclip
                pyperclip.copy(password)
                self.ui.typewriter("[✓] Copiada", 0.02, Colors.GREEN)
            except ImportError:
                pass
        
        save = input(f"{Colors.CYAN}[?] Guardar para servicio? (s/n): {Colors.RESET}").lower()
        if save == 's':
            service = input(f"{Colors.CYAN}[?] Servicio: {Colors.RESET}").strip()
            username = input(f"{Colors.CYAN}[?] Usuario: {Colors.RESET}").strip()
            if service and username:
                self.pm.add(service, username, password)
                self.ui.typewriter(f"[✓] Guardada en '{service}'", 0.02, Colors.GREEN)
    
    def manage_categories_flow(self):
        """Flujo para gestionar categorías"""
        from categories import CategoryManager
        
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("📁 GESTIÓN DE CATEGORÍAS"))
        
        cat_manager = CategoryManager()
        
        while True:
            print(f"\n{Colors.CYAN}{'═' * 60}{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.GREEN}   Categorías disponibles{Colors.RESET}")
            print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")
            
            categories = cat_manager.get_categories()
            for i, cat in enumerate(categories, 1):
                print(f"{Colors.YELLOW}{i:2}.{Colors.RESET} {cat}")
            
            print(f"\n{Colors.CYAN}{'─' * 60}{Colors.RESET}")
            print(f"{Colors.YELLOW}[A]{Colors.RESET} Agregar categoría")
            print(f"{Colors.YELLOW}[E]{Colors.RESET} Eliminar categoría")
            print(f"{Colors.YELLOW}[S]{Colors.RESET} Asignar categoría a servicio")
            print(f"{Colors.YELLOW}[V]{Colors.RESET} Ver servicios por categoría")
            print(f"{Colors.YELLOW}[T]{Colors.RESET} Estadísticas por categoría")
            print(f"{Colors.YELLOW}[R]{Colors.RESET} Gestión de etiquetas")
            print(f"{Colors.YELLOW}[0]{Colors.RESET} Volver")
            
            opcion = input(f"\n{Colors.CYAN}[?] Opción: {Colors.RESET}").strip().upper()
            
            if opcion == "A":
                new_cat = input(f"{Colors.CYAN}[?] Nueva categoría: {Colors.RESET}").strip()
                if new_cat and cat_manager.add_category(new_cat):
                    self.ui.typewriter(f"[✓] Categoría '{new_cat}' agregada", 0.02, Colors.GREEN)
            elif opcion == "E":
                cat_name = input(f"{Colors.CYAN}[?] Categoría a eliminar: {Colors.RESET}").strip()
                if cat_manager.remove_category(cat_name):
                    self.ui.typewriter(f"[✓] Categoría '{cat_name}' eliminada", 0.02, Colors.GREEN)
            elif opcion == "S":
                self._assign_category_to_service()
            elif opcion == "V":
                self._view_services_by_category()
            elif opcion == "T":
                stats = self.pm.get_category_stats()
                print(f"\n{Colors.GREEN}Estadísticas por categoría:{Colors.RESET}")
                for cat, count in sorted(stats.items(), key=lambda x: -x[1]):
                    print(f"   {cat}: {count}")
                input(f"\n{self.lang.get('press_enter')}")
            elif opcion == "R":
                self._manage_tags_flow()
            elif opcion == "0":
                break
            else:
                self.ui.typewriter("[!] Opción inválida", 0.02, Colors.RED)
    
    def _assign_category_to_service(self):
        services = self.pm.list_all()
        if not services:
            self.ui.typewriter("[!] No hay servicios", 0.02, Colors.YELLOW)
            return
        
        from categories import CategoryManager
        cat_manager = CategoryManager()
        
        print(f"\n{Colors.CYAN}Servicios disponibles:{Colors.RESET}")
        for i, s in enumerate(services, 1):
            cat = self.pm.get(s).get('category', '📁')
            print(f"   {Colors.YELLOW}{i}.{Colors.RESET} {s} [{cat}]")
        
        service = input(f"\n{Colors.CYAN}[?] Servicio: {Colors.RESET}").strip()
        if service not in services:
            self.ui.typewriter("[!] Servicio no encontrado", 0.02, Colors.RED)
            return
        
        categories = cat_manager.get_categories()
        print(f"\n{Colors.CYAN}Categorías:{Colors.RESET}")
        for i, cat in enumerate(categories, 1):
            print(f"   {Colors.YELLOW}{i}.{Colors.RESET} {cat}")
        
        choice = input(f"{Colors.CYAN}[?] Selecciona categoría: {Colors.RESET}").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            category = categories[idx] if 0 <= idx < len(categories) else choice
        else:
            category = choice
        
        if self.pm.update_category(service, category):
            self.ui.typewriter(f"[✓] Categoría asignada", 0.02, Colors.GREEN)
    
    def _view_services_by_category(self):
        from categories import CategoryManager
        cat_manager = CategoryManager()
        
        categories = cat_manager.get_categories()
        print(f"\n{Colors.CYAN}Categorías:{Colors.RESET}")
        for i, cat in enumerate(categories, 1):
            print(f"   {Colors.YELLOW}{i}.{Colors.RESET} {cat}")
        
        choice = input(f"\n{Colors.CYAN}[?] Categoría: {Colors.RESET}").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            category = categories[idx] if 0 <= idx < len(categories) else choice
        else:
            category = choice
        
        services = self.pm.get_services_by_category(category)
        if services:
            print(f"\n{Colors.GREEN}Servicios en '{category}':{Colors.RESET}")
            for s in services:
                print(f"   {Colors.YELLOW}→{Colors.RESET} {s}")
        else:
            self.ui.typewriter(f"[!] No hay servicios", 0.02, Colors.YELLOW)
        input(f"\n{self.lang.get('press_enter')}")
    
    def _manage_tags_flow(self):
        """Flujo para gestionar etiquetas"""
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("🏷️ GESTIÓN DE ETIQUETAS"))
        
        while True:
            all_tags = self.pm.get_all_tags()
            print(f"\n{Colors.CYAN}{'═' * 60}{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.GREEN}   Etiquetas existentes{Colors.RESET}")
            print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")
            if all_tags:
                for tag in all_tags:
                    print(f"   {Colors.YELLOW}#{tag}{Colors.RESET}")
            else:
                print(f"   {Colors.DIM}No hay etiquetas{Colors.RESET}")
            
            print(f"\n{Colors.CYAN}{'─' * 60}{Colors.RESET}")
            print(f"{Colors.YELLOW}[A]{Colors.RESET} Agregar etiqueta")
            print(f"{Colors.YELLOW}[R]{Colors.RESET} Eliminar etiqueta")
            print(f"{Colors.YELLOW}[V]{Colors.RESET} Ver por etiqueta")
            print(f"{Colors.YELLOW}[0]{Colors.RESET} Volver")
            
            opcion = input(f"\n{Colors.CYAN}[?] Opción: {Colors.RESET}").strip().upper()
            if opcion == "A":
                self._add_tag_to_service()
            elif opcion == "R":
                self._remove_tag_from_service()
            elif opcion == "V":
                self._view_services_by_tag()
            elif opcion == "0":
                break
    
    def _add_tag_to_service(self):
        services = self.pm.list_all()
        if not services:
            self.ui.typewriter("[!] No hay servicios", 0.02, Colors.YELLOW)
            return
        
        print(f"\n{Colors.CYAN}Servicios:{Colors.RESET}")
        for i, s in enumerate(services, 1):
            print(f"   {Colors.YELLOW}{i}.{Colors.RESET} {s}")
        
        service = input(f"\n{Colors.CYAN}[?] Servicio: {Colors.RESET}").strip()
        if service not in services:
            self.ui.typewriter("[!] No encontrado", 0.02, Colors.RED)
            return
        
        tag = input(f"{Colors.CYAN}[?] Etiqueta: {Colors.RESET}").strip()
        if self.pm.add_tag(service, tag):
            self.ui.typewriter(f"[✓] Etiqueta '#{tag}' agregada", 0.02, Colors.GREEN)
    
    def _remove_tag_from_service(self):
        services = self.pm.list_all()
        if not services:
            self.ui.typewriter("[!] No hay servicios", 0.02, Colors.YELLOW)
            return
        
        print(f"\n{Colors.CYAN}Servicios:{Colors.RESET}")
        for i, s in enumerate(services, 1):
            print(f"   {Colors.YELLOW}{i}.{Colors.RESET} {s}")
        
        service = input(f"\n{Colors.CYAN}[?] Servicio: {Colors.RESET}").strip()
        if service not in services:
            self.ui.typewriter("[!] No encontrado", 0.02, Colors.RED)
            return
        
        tags = self.pm.get_tags(service)
        if not tags:
            self.ui.typewriter("[!] No tiene etiquetas", 0.02, Colors.YELLOW)
            return
        
        print(f"\n{Colors.CYAN}Etiquetas de '{service}':{Colors.RESET}")
        for t in tags:
            print(f"   {Colors.YELLOW}#{t}{Colors.RESET}")
        
        tag = input(f"\n{Colors.CYAN}[?] Etiqueta a eliminar: {Colors.RESET}").strip()
        if self.pm.remove_tag(service, tag):
            self.ui.typewriter(f"[✓] Etiqueta '#{tag}' eliminada", 0.02, Colors.GREEN)
    
    def _view_services_by_tag(self):
        all_tags = self.pm.get_all_tags()
        if not all_tags:
            self.ui.typewriter("[!] No hay etiquetas", 0.02, Colors.YELLOW)
            return
        
        print(f"\n{Colors.CYAN}Etiquetas:{Colors.RESET}")
        for i, tag in enumerate(all_tags, 1):
            print(f"   {Colors.YELLOW}{i}.{Colors.RESET} #{tag}")
        
        tag = input(f"\n{Colors.CYAN}[?] Etiqueta: {Colors.RESET}").strip()
        services = self.pm.search_by_tag(tag)
        
        if services:
            print(f"\n{Colors.GREEN}Servicios con '#{tag}':{Colors.RESET}")
            for s in services:
                print(f"   {Colors.YELLOW}→{Colors.RESET} {s}")
        else:
            self.ui.typewriter("[!] No hay servicios", 0.02, Colors.YELLOW)
        input(f"\n{self.lang.get('press_enter')}")
    
    def show_help(self):
        """Mostrar ayuda"""
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("🆘 AYUDA - DNO-Encryptx"))
        
        help_text = f"""
{Colors.CYAN}┌{'─' * 66}┐{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.BOLD}📌 GUÍA RÁPIDA DE USO{Colors.RESET}{' ' * 46}{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}├{'─' * 66}┤{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[1]{Colors.RESET} 🔐 Agregar nueva contraseña{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[2]{Colors.RESET} 👁️  Ver contraseña guardada{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[3]{Colors.RESET} 📋 Listar todos los servicios{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[4]{Colors.RESET} 🗑️  Eliminar contraseña{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[5]{Colors.RESET} 💾 Crear backup de seguridad{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[6]{Colors.RESET} 📊 Ver estadísticas{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[7]{Colors.RESET} 🔍 Buscar servicios{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[8]{Colors.RESET} 🌐 Cambiar idioma{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[X]{Colors.RESET} 🖼️  Crear Imagen Bóveda (Esteganografía){' ' * 25}{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[C]{Colors.RESET} 📁 Gestionar Categorías{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[T]{Colors.RESET} 🏷️ Gestionar Etiquetas{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[G]{Colors.RESET} 🔑 Generar contraseña segura{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[I]{Colors.RESET} 📀 Instalar en USB{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[S]{Colors.RESET} 🎭 Versión STEALTH{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[N]{Colors.RESET} 🔔 Ver Notificaciones{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[M]{Colors.RESET} 📝 Notas Seguras{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[F]{Colors.RESET} 📁 File Vault (Archivos Encriptados){Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[U]{Colors.RESET} 🖥️ Abrir Interfaz Gráfica (GUI){Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[H]{Colors.RESET} 🆘 Ayuda{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[0]{Colors.RESET} 🎨 Modo Matrix{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}│{Colors.RESET} {Colors.GREEN}[9]{Colors.RESET} 🚪 Salir{Colors.CYAN}│{Colors.RESET}
{Colors.CYAN}└{'─' * 66}┘{Colors.RESET}
"""
        print(help_text)
        input(f"\n{self.lang.get('press_enter')}")
    
    def load_preferences(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    prefs = json.load(f)
                    if 'language' in prefs:
                        self.lang.switch_language(prefs['language'])
            except:
                pass
    
    def save_preferences(self):
        prefs = {'language': self.lang.current_language}
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(prefs, f, indent=2)
        except:
            pass
    
    def first_time_setup(self):
        self.ui.clear_screen()
        print(get_banner())
        print(get_header(self.lang.get("first_time_setup")))
        
        while True:
            master_pass = getpass.getpass(f"\n{Colors.CYAN}[?] {self.lang.get('create_master_password')}: {Colors.RESET}")
            confirm_pass = getpass.getpass(f"{Colors.CYAN}[?] {self.lang.get('confirm_master_password')}: {Colors.RESET}")
            if master_pass == confirm_pass:
                if len(master_pass) < Config.MIN_PASSWORD_LENGTH:
                    self.ui.typewriter(self.lang.get("password_min_length", length=Config.MIN_PASSWORD_LENGTH), 0.02, Colors.RED)
                    continue
                break
            else:
                self.ui.typewriter(self.lang.get("passwords_do_not_match"), 0.02, Colors.RED)
        
        self.ui.loading(self.lang.get("generating_key"), 1.5)
        self.crypto.create_master_key(master_pass)
        self.pm = PasswordManager(self.crypto)
        self.pm.save()
        
        self.ui.typewriter(self.lang.get("database_created"), 0.02, Colors.GREEN)
        self.ui.typewriter(self.lang.get("warning_password_loss"), 0.02, Colors.YELLOW)
        time.sleep(2)
        return True
        
    def secure_notes_flow(self):
        """Flujo para notas seguras (Carga Perezosa)"""
        if not self.notes_ui:
            try:
                from notes_ui import NotesUI
                self.notes_ui = NotesUI(self.ui, self.lang, self.crypto)
            except Exception as e:
                self.ui.typewriter(f"[!] Error al cargar notas: {e}", 0.02, Colors.RED)
                
        if hasattr(self, 'notes_ui') and self.notes_ui:
            self.notes_ui.show_main_menu()
        else:
            self.ui.typewriter("[!] Sistema de notas no disponible", 0.02, Colors.RED)
            input(f"\n{self.lang.get('press_enter')}")
    
    def launch_gui_flow(self):
        """Abre la interfaz gráfica si está disponible"""
        if not GUI_AVAILABLE:
            self.ui.typewriter("[!] Interfaz gráfica no disponible. Falta 'gui_manager.py' o 'tkinter'.", 0.02, Colors.RED)
            input(f"\n{self.lang.get('press_enter')}")
            return
            
        self.ui.typewriter("\n[+] Cambiando a Modo Gráfico (GUI)...", 0.02, Colors.GREEN)
        time.sleep(1)
        
        try:
            gui = PasswordManagerGUI(self.pm, self.crypto, self.lang, getattr(self, 'notification_manager', None))
            gui.run()
            
            self.ui.clear_screen()
            print(get_banner())
            self.ui.typewriter("[+] Interfaz gráfica cerrada. Regresando al modo terminal...", 0.02, Colors.CYAN)
            time.sleep(1)
        except Exception as e:
            self.ui.typewriter(f"\n[!] Error en la GUI: {e}", 0.02, Colors.RED)
            input(f"\n{self.lang.get('press_enter')}")
            
    def file_vault_flow(self):
        """Flujo para gestionar archivos encriptados"""
        import shutil
        
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("📁 FILE VAULT - ARCHIVOS ENCRIPTADOS"))
        
        while True:
            vault_info = self.file_vault.get_vault_info()
            files = self.file_vault.list_vault_files()
            
            print(f"\n{Colors.CYAN}{'═' * 70}{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.GREEN}   📊 ESTADO DE LA BÓVEDA{Colors.RESET}")
            print(f"{Colors.CYAN}{'═' * 70}{Colors.RESET}")
            print(f"{Colors.YELLOW}[+] Archivos guardados:{Colors.RESET} {vault_info['total_files']}")
            print(f"{Colors.YELLOW}[+] Espacio usado:{Colors.RESET} {vault_info['total_size_mb']:.2f} MB")
            print(f"{Colors.YELLOW}[+] Ubicación:{Colors.RESET} {vault_info['vault_path']}")
            
            if files:
                print(f"\n{Colors.CYAN}{'═' * 70}{Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.GREEN}   📁 ARCHIVOS EN LA BÓVEDA{Colors.RESET}")
                print(f"{Colors.CYAN}{'═' * 70}{Colors.RESET}")
                
                for i, file in enumerate(files, 1):
                    icon = file['icon']
                    name = file['original_name']
                    size = f"{file['size_mb']:.2f} MB" if file['size_mb'] > 0 else "Desconocido"
                    created = file['created']
                    key_status = "🔐" if file['use_master_key'] else "🔑"
                    
                    print(f"{Colors.GREEN}{i:2}.{Colors.RESET} {icon} {Colors.CYAN}{name}{Colors.RESET}")
                    print(f"     {Colors.DIM}Archivo: {file['filename']}{Colors.RESET}")
                    print(f"     {Colors.DIM}Tamaño: {size} | Creado: {created} | {key_status}{Colors.RESET}")
            
            print(f"\n{Colors.CYAN}{'═' * 70}{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.GREEN}   📋 OPCIONES{Colors.RESET}")
            print(f"{Colors.CYAN}{'═' * 70}{Colors.RESET}")
            print(f"{Colors.GREEN}[1]{Colors.RESET} 🔒 Encriptar archivo")
            print(f"{Colors.GREEN}[2]{Colors.RESET} 🔓 Desencriptar archivo")
            print(f"{Colors.GREEN}[3]{Colors.RESET} 📋 Listar archivos")
            print(f"{Colors.GREEN}[4]{Colors.RESET} 🗑️ Eliminar archivo")
            print(f"{Colors.GREEN}[5]{Colors.RESET} 📂 Abrir carpeta de la bóveda")
            print(f"{Colors.GREEN}[6]{Colors.RESET} 🔑 Encriptar con contraseña personalizada")
            print(f"{Colors.GREEN}[0]{Colors.RESET} 🔙 Volver")
            
            opcion = input(f"\n{Colors.CYAN}[FileVault]~# {Colors.RESET}").strip()
            
            if opcion == "1":
                self._encrypt_file_to_vault()
            elif opcion == "2":
                self._decrypt_file_from_vault()
            elif opcion == "3":
                input(f"\n{self.lang.get('press_enter')}")
            elif opcion == "4":
                self._delete_vault_file()
            elif opcion == "5":
                import subprocess
                import platform
                if platform.system() == "Windows":
                    os.startfile(self.file_vault.vault_path)
                elif platform.system() == "Darwin":
                    subprocess.run(["open", self.file_vault.vault_path])
                else:
                    subprocess.run(["xdg-open", self.file_vault.vault_path])
                self.ui.typewriter("[✓] Carpeta de la bóveda abierta", 0.02, Colors.GREEN)
                input(f"\n{self.lang.get('press_enter')}")
            elif opcion == "6":
                self._encrypt_file_with_password()
            elif opcion == "0":
                break
            else:
                self.ui.typewriter("[!] Opción inválida", 0.02, Colors.RED)

    def _encrypt_file_to_vault(self):
        """Encriptar archivo usando clave maestra"""
        import tkinter as tk
        from tkinter import filedialog
        
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("🔒 ENCRIPTAR ARCHIVO"))
        
        print(f"\n{Colors.CYAN}[?] Selecciona el archivo a encriptar{Colors.RESET}")
        
        try:
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(title="Seleccionar archivo a encriptar")
            root.destroy()
        except:
            file_path = input(f"{Colors.CYAN}[?] Ruta del archivo: {Colors.RESET}").strip()
        
        if not file_path:
            self.ui.typewriter("[!] No se seleccionó ningún archivo", 0.02, Colors.RED)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        if not os.path.exists(file_path):
            self.ui.typewriter("[!] Archivo no encontrado", 0.02, Colors.RED)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        custom_name = input(f"{Colors.CYAN}[?] Nombre para el archivo encriptado (dejar vacío para automático): {Colors.RESET}").strip()
        self.ui.loading("Encriptando archivo...", 1)
        
        success, msg, output_path = self.file_vault.encrypt_file(
            file_path, 
            output_name=custom_name if custom_name else None,
            use_master_key=True
        )
        
        if success:
            self.ui.typewriter(f"[✓] {msg}", 0.02, Colors.GREEN)
            self.ui.typewriter(f"[✓] Guardado en: {output_path}", 0.02, Colors.CYAN)
        else:
            self.ui.typewriter(f"[✗] {msg}", 0.02, Colors.RED)
        
        input(f"\n{self.lang.get('press_enter')}")

    def _decrypt_file_from_vault(self):
        """Desencriptar archivo de la bóveda"""
        files = self.file_vault.list_vault_files()
        
        if not files:
            self.ui.typewriter("[!] No hay archivos en la bóveda", 0.02, Colors.YELLOW)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("🔓 DESENCRIPTAR ARCHIVO"))
        
        print(f"\n{Colors.CYAN}Archivos disponibles:{Colors.RESET}")
        for i, file in enumerate(files, 1):
            icon = file['icon']
            name = file['original_name']
            filename = file['filename']
            # Mostrar si está con Clave Maestra o Clave Personalizada
            key_status = "🔐 (Maestra)" if file['use_master_key'] else "🔑 (Personalizada)"
            print(f"   {Colors.GREEN}{i}.{Colors.RESET} {icon} {Colors.CYAN}{name}{Colors.RESET} {Colors.DIM}[{key_status}]{Colors.RESET}")
        
        choice = input(f"\n{Colors.CYAN}[?] Selecciona archivo (número o nombre): {Colors.RESET}").strip()
        
        # Buscar información completa del archivo seleccionado
        selected_file_info = None
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                selected_file_info = files[idx]
        else:
            for f in files:
                if choice.lower() in f['original_name'].lower() or choice == f['filename']:
                    selected_file_info = f
                    break
        
        if not selected_file_info:
            self.ui.typewriter("[!] Archivo no encontrado", 0.02, Colors.RED)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        custom_password = None
        if not selected_file_info['use_master_key']:
            import getpass
            print(f"\n{Colors.YELLOW}[!] Este archivo está protegido con una contraseña personalizada.{Colors.RESET}")
            custom_password = getpass.getpass(f"{Colors.CYAN}[?] Ingresa la contraseña: {Colors.RESET}")
            print() # Salto de línea estético
        
        # Preguntar directorio de salida
        output_dir = input(f"{Colors.CYAN}[?] Directorio de salida (dejar vacío para carpeta 'decrypted'): {Colors.RESET}").strip()
        
        self.ui.loading("Desencriptando archivo...", 1)
        
        file_path = os.path.join(self.file_vault.vault_path, selected_file_info['filename'])
        
        # Pasamos el parámetro custom_password
        success, msg, output_path = self.file_vault.decrypt_file(
            file_path,
            output_dir=output_dir if output_dir else None,
            custom_password=custom_password
        )
        
        if success:
            self.ui.typewriter(f"[✓] {msg}", 0.02, Colors.GREEN)
            self.ui.typewriter(f"[✓] Guardado en: {output_path}", 0.02, Colors.CYAN)
        else:
            self.ui.typewriter(f"[✗] {msg}", 0.02, Colors.RED)
        
        input(f"\n{self.lang.get('press_enter')}")

    def _delete_vault_file(self):
        """Eliminar archivo de la bóveda"""
        files = self.file_vault.list_vault_files()
        
        if not files:
            self.ui.typewriter("[!] No hay archivos en la bóveda", 0.02, Colors.YELLOW)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        print(f"\n{Colors.CYAN}Archivos disponibles:{Colors.RESET}")
        for i, file in enumerate(files, 1):
            icon = file['icon']
            name = file['original_name']
            filename = file['filename']
            print(f"   {Colors.GREEN}{i}.{Colors.RESET} {icon} {Colors.CYAN}{name}{Colors.RESET} ({filename})")
        
        choice = input(f"\n{Colors.CYAN}[?] Selecciona archivo a eliminar: {Colors.RESET}").strip()
        
        selected_file = None
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                selected_file = files[idx]['filename']
        else:
            for f in files:
                if choice.lower() in f['original_name'].lower() or choice == f['filename']:
                    selected_file = f['filename']
                    break
        
        if not selected_file:
            self.ui.typewriter("[!] Archivo no encontrado", 0.02, Colors.RED)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        confirm = input(f"{Colors.RED}[⚠] ¿Eliminar permanentemente '{selected_file}'? (s/n): {Colors.RESET}").lower()
        if confirm == 's':
            success, msg = self.file_vault.delete_file(selected_file)
            self.ui.typewriter(f"[{'✓' if success else '✗'}] {msg}", 0.02, Colors.GREEN if success else Colors.RED)
        
        input(f"\n{self.lang.get('press_enter')}")

    def _encrypt_file_with_password(self):
        """Encriptar archivo con contraseña personalizada (para compartir)"""
        import tkinter as tk
        from tkinter import filedialog
        
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("🔑 ENCRIPTAR CON CONTRASEÑA PERSONALIZADA"))
        
        self.ui.typewriter("[!] Esta opción permite encriptar archivos con una contraseña propia", 0.02, Colors.YELLOW)
        self.ui.typewriter("[!] Ideal para enviar archivos encriptados a otras personas", 0.02, Colors.CYAN)
        print()
        
        try:
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(title="Seleccionar archivo a encriptar")
            root.destroy()
        except:
            file_path = input(f"{Colors.CYAN}[?] Ruta del archivo: {Colors.RESET}").strip()
        
        if not file_path:
            self.ui.typewriter("[!] No se seleccionó ningún archivo", 0.02, Colors.RED)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        print()
        while True:
            password = getpass.getpass(f"{Colors.CYAN}[?] Contraseña para encriptar: {Colors.RESET}")
            confirm = getpass.getpass(f"{Colors.CYAN}[?] Confirmar contraseña: {Colors.RESET}")
            
            if password == confirm:
                if len(password) < 4:
                    self.ui.typewriter("[!] Mínimo 4 caracteres", 0.02, Colors.RED)
                    continue
                break
            else:
                self.ui.typewriter("[!] Las contraseñas no coinciden", 0.02, Colors.RED)
        
        custom_name = input(f"{Colors.CYAN}[?] Nombre para el archivo encriptado: {Colors.RESET}").strip()
        self.ui.loading("Encriptando archivo con contraseña personalizada...", 1)
        
        success, msg, output_path = self.file_vault.encrypt_file(
            file_path,
            output_name=custom_name if custom_name else None,
            use_master_key=False,
            custom_password=password
        )
        
        if success:
            self.ui.typewriter(f"[✓] {msg}", 0.02, Colors.GREEN)
            self.ui.typewriter(f"[✓] Guardado en: {output_path}", 0.02, Colors.CYAN)
            self.ui.typewriter(f"\n{Colors.YELLOW}[!] Para desencriptar, otra persona necesitará:{Colors.RESET}")
            self.ui.typewriter(f"   • El archivo .dno", 0.02, Colors.CYAN)
            self.ui.typewriter(f"   • La contraseña que acabas de crear", 0.02, Colors.CYAN)
            self.ui.typewriter(f"   • El programa DNO-Encryptx", 0.02, Colors.CYAN)
        else:
            self.ui.typewriter(f"[✗] {msg}", 0.02, Colors.RED)
        
        input(f"\n{self.lang.get('press_enter')}")
            
    def login(self):
        self.ui.clear_screen()
        print(get_banner())
        print(get_header(self.lang.get("secure_access")))
        
        if not os.path.exists(Config.SALT_FILE):
            self.ui.typewriter(self.lang.get("no_profile"), 0.02, Colors.RED)
            return False
        
        attempts = Config.MAX_LOGIN_ATTEMPTS
        while attempts > 0:
            master_pass = getpass.getpass(f"\n{Colors.CYAN}[?] {self.lang.get('master_password')} [{attempts}]: {Colors.RESET}")
            if self.crypto.load_master_key(master_pass):
                try:
                    self.pm = PasswordManager(self.crypto)
                    self.pm.load()
                    self.ui.loading(self.lang.get("decrypting_db"), 1)
                    self.ui.typewriter(self.lang.get("access_granted_welcome"), 0.02, Colors.GREEN)
                    
                    # Carga de File Vault en el login
                    self.file_vault = FileVault(self.crypto)
                    time.sleep(1)
                    
                    self.notification_manager = NotificationManager(self.pm)
                    
                    return True
                except Exception as e:
                    self.ui.typewriter(self.lang.get("corrupted_db", error=str(e)), 0.02, Colors.RED)
                    return False
            else:
                attempts -= 1
                if attempts > 0:
                    self.ui.typewriter(f"{self.lang.get('access_denied')} - {attempts} intentos", 0.02, Colors.RED)
                else:
                    self.ui.typewriter(self.lang.get("system_locked"), 0.02, Colors.RED)
                    time.sleep(2)
        return False
    
    def check_notifications(self):
        """Verificar y mostrar notificaciones después del login"""
        if self.pm and self.pm.data:
            from notifications import NotificationManager
            self.notification_manager = NotificationManager(self.pm)
            if self.notification_manager.show_notifications(self.ui, Colors):
                print(f"\n{Colors.CYAN}[!] Revisa las notificaciones de seguridad arriba{Colors.RESET}")
                time.sleep(2)
            return True
        else:
            self.ui.typewriter("[!] No hay datos para analizar", 0.02, Colors.YELLOW)
            return False
    
    def view_notifications_flow(self):
        """Ver notificaciones manualmente desde el menú"""
        if hasattr(self, 'notification_manager') and self.notification_manager:
            self.ui.clear_screen()
            print(get_banner())
            print(get_header("🔔 NOTIFICACIONES DE SEGURIDAD"))
            self.notification_manager.show_notifications(self.ui, Colors)
        else:
            self.ui.typewriter("[!] No hay notificaciones disponibles", 0.02, Colors.YELLOW)
            self.ui.typewriter("[!] Inicia sesión primero para ver notificaciones", 0.02, Colors.RED)
        input(f"\n{self.lang.get('press_enter')}")
    
    def change_language_flow(self):
        self.ui.clear_screen()
        print(get_banner())
        print(get_header(self.lang.get("language_switch")))
        print(f"\n{Colors.CYAN}1. Español{Colors.RESET}")
        print(f"{Colors.CYAN}2. English{Colors.RESET}")
        choice = input(f"\n{Colors.YELLOW}[?] {self.lang.get('select_language')}: {Colors.RESET}").strip()
        if choice == "1":
            self.lang.switch_language('es')
            self.save_preferences()
            self.ui.typewriter(self.lang.get("language_changed", language="Español"), 0.02, Colors.GREEN)
        elif choice == "2":
            self.lang.switch_language('en')
            self.save_preferences()
            self.ui.typewriter(self.lang.get("language_changed", language="English"), 0.02, Colors.GREEN)
        else:
            self.ui.typewriter(self.lang.get("invalid_language"), 0.02, Colors.RED)
        time.sleep(1.5)
    
    def add_credential_flow(self):
        self.ui.clear_screen()
        print(get_banner())
        print(get_header(self.lang.get("add_new")))
        
        service = input(f"\n{Colors.CYAN}[?] {self.lang.get('service_name')}: {Colors.RESET}").strip()
        if not service:
            self.ui.typewriter(self.lang.get("invalid_service"), 0.02, Colors.RED)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        username = input(f"{Colors.CYAN}[?] {self.lang.get('username_email')}: {Colors.RESET}").strip()
        password = getpass.getpass(f"{Colors.CYAN}[?] {self.lang.get('password')}: {Colors.RESET}")
        
        existing = self.pm.get(service)
        if existing:
            self.ui.typewriter(self.lang.get("service_exists", service=service), 0.02, Colors.YELLOW)
            overwrite = input(f"{Colors.CYAN}[?] {self.lang.get('overwrite')}: {Colors.RESET}").lower()
            if overwrite != 's':
                return
        
        self.pm.add(service, username, password)
        self.ui.loading(self.lang.get("encrypting_storing"), 1)
        self.ui.typewriter(self.lang.get("credentials_stored", service=service), 0.02, Colors.GREEN)
        input(f"\n{self.lang.get('press_enter')}")
    
    def retrieve_credential_flow(self):
        self.pm.load()
        services = self.pm.list_all()
        if not services:
            self.ui.clear_screen()
            print(get_banner())
            print(get_header(self.lang.get("retrieve")))
            self.ui.typewriter(self.lang.get("no_credentials"), 0.02, Colors.YELLOW)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        self.ui.clear_screen()
        print(get_banner())
        print(get_header(self.lang.get("retrieve")))
        self.menu.show_credentials_list()
        
        service = input(f"\n{Colors.CYAN}[?] {self.lang.get('service_name')}: {Colors.RESET}").strip()
        entry = self.menu.show_credential_details(service)
        
        if entry:
            try:
                import pyperclip
                copy = input(f"\n{Colors.CYAN}[?] {self.lang.get('copy_to_clipboard')}: {Colors.RESET}").lower()
                if copy == 's':
                    pyperclip.copy(entry['password'])
                    self.ui.typewriter(self.lang.get("copied"), 0.02, Colors.GREEN)
            except ImportError:
                pass
        input(f"\n{self.lang.get('press_enter')}")
    
    def list_services_flow(self):
        self.pm.load()
        self.ui.clear_screen()
        print(get_banner())
        print(get_header(self.lang.get("list")))
        self.menu.show_credentials_list()
        input(f"\n{self.lang.get('press_enter')}")
    
    def delete_credential_flow(self):
        self.pm.load()
        services = self.pm.list_all()
        if not services:
            self.ui.clear_screen()
            print(get_banner())
            print(get_header(self.lang.get("delete")))
            self.ui.typewriter(self.lang.get("no_credentials"), 0.02, Colors.YELLOW)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        self.ui.clear_screen()
        print(get_banner())
        print(get_header(self.lang.get("delete")))
        self.menu.show_credentials_list()
        
        service = input(f"\n{Colors.CYAN}[?] {self.lang.get('service_to_delete')}: {Colors.RESET}").strip()
        if not self.pm.get(service):
            self.ui.typewriter(self.lang.get("service_not_found", service=service), 0.02, Colors.RED)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        confirm = input(f"{Colors.RED}[⚠] {self.lang.get('permanent_delete', service=service)}: {Colors.RESET}").lower()
        if confirm == 's':
            self.pm.delete(service)
            self.ui.typewriter(self.lang.get("service_deleted", service=service), 0.02, Colors.GREEN)
        input(f"\n{self.lang.get('press_enter')}")
    
    def backup_flow(self):
        """Flujo para crear backup"""
        import shutil
        backup_name = f"backup_{time.strftime('%Y%m%d_%H%M%S')}.enc"
        try:
            shutil.copy2(Config.DATA_FILE, backup_name)
            self.ui.clear_screen()
            print(get_banner())
            print(get_header(self.lang.get("backup")))
            self.ui.typewriter(self.lang.get("backup_created", filename=backup_name), 0.02, Colors.GREEN)
        except Exception as e:
            self.ui.typewriter(self.lang.get("backup_failed"), 0.02, Colors.RED)
        input(f"\n{self.lang.get('press_enter')}")

    def statistics_flow(self):
        """Flujo para mostrar estadísticas"""
        self.pm.load()
        self.ui.clear_screen()
        print(get_banner())
        print(get_header(self.lang.get("stats")))
        
        # 1. Mostrar las estadísticas básicas del menú
        self.menu.show_stats()
        
        # 2. Delegar el análisis avanzado al nuevo StatsManager
        stats_manager = StatsManager(self.pm, getattr(self, 'notification_manager', None))
        stats_manager.show_advanced_stats()
        
        input(f"\n{self.lang.get('press_enter')}")

    def search_flow(self):
        """Flujo para buscar servicios"""
        self.pm.load()
        self.ui.clear_screen()
        print(get_banner())
        print(get_header(self.lang.get("search_services")))
        
        pattern = input(f"\n{Colors.CYAN}[?] {self.lang.get('search_pattern')}: {Colors.RESET}").strip()
        if not pattern:
            return
        
        results = self.pm.search(pattern)
        
        if results:
            print(f"\n{Colors.GREEN}[+] {self.lang.get('found_matches', total=len(results))}{Colors.RESET}")
            for r in results:
                print(f"   {Colors.YELLOW}→{Colors.RESET} {r}")
        else:
            self.ui.typewriter(self.lang.get("no_matches"), 0.02, Colors.YELLOW)
        
        input(f"\n{self.lang.get('press_enter')}")

    def steganography_flow(self):
        """Flujo para ocultar/extraer la base de datos en imágenes"""
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("🖼️  ESTEGANOGRAFÍA - IMAGEN BÓVEDA"))

        stego = Steganography()

        print(f"\n{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}   Opciones Esteganográficas{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.YELLOW}[1]{Colors.RESET} 🖼️  Ocultar Base de Datos en Imagen (Crear Portador)")
        print(f"{Colors.YELLOW}[2]{Colors.RESET} 🔓 Restaurar Base de Datos desde Imagen")
        print(f"{Colors.YELLOW}[0]{Colors.RESET} 🔙 Volver")

        opcion = input(f"\n{Colors.CYAN}[?] Opción (1-2): {Colors.RESET}").strip()

        if opcion == "1":
            self._hide_vault_in_image(stego)
        elif opcion == "2":
            self._restore_vault_from_image(stego)
        elif opcion == "0":
            return
        else:
            self.ui.typewriter("[!] Opción inválida", 0.02, Colors.RED)
            input(f"\n{self.lang.get('press_enter')}")

    def _hide_vault_in_image(self, stego_manager):
        """Ocultar passwords.enc dentro de una imagen"""
        if not os.path.exists(Config.DATA_FILE):
            self.ui.typewriter("[!] No hay base de datos activa para ocultar.", 0.02, Colors.RED)
            input(f"\n{self.lang.get('press_enter')}")
            return

        print(f"\n{Colors.BOLD}{Colors.CYAN}>>> CREAR IMAGEN BÓVEDA <<<{Colors.RESET}")
        self.ui.typewriter("[!] La imagen portadora (ej: JPG/PNG) debe ser grande.", 0.02, Colors.YELLOW)

        cover_path = input(f"\n{Colors.CYAN}[?] Ruta de la imagen portadora: {Colors.RESET}").strip()
        if not cover_path or not os.path.exists(cover_path):
            self.ui.typewriter("[!] Imagen no encontrada.", 0.02, Colors.RED)
            input(f"\n{self.lang.get('press_enter')}")
            return

        name_without_ext = os.path.splitext(os.path.basename(cover_path))[0]
        output_name = f"{name_without_ext}_vault.png"
        output_path = os.path.join(os.path.dirname(cover_path), output_name)

        with open(Config.DATA_FILE, 'rb') as f:
            vault_data = f.read()

        self.ui.loading("Ocultando base de datos en píxeles...", 1.5)
        success, msg = stego_manager.hide_data(cover_path, vault_data, output_path)

        if success:
            self.ui.typewriter(f"\n[✓] {msg}", 0.02, Colors.GREEN)
            self.ui.typewriter(f"[!] Archivo creado: {output_path}", 0.02, Colors.WHITE)
        else:
            self.ui.typewriter(f"\n[✗] {msg}", 0.02, Colors.RED)
        input(f"\n{self.lang.get('press_enter')}")

    def _restore_vault_from_image(self, stego_manager):
        """Restaurar passwords.enc desde una imagen portadora"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}>>> RESTAURAR DESDE IMAGEN <<<{Colors.RESET}")
        stego_path = input(f"\n{Colors.CYAN}[?] Ruta de la imagen bóveda (.png): {Colors.RESET}").strip()
        
        if not stego_path or not os.path.exists(stego_path):
            self.ui.typewriter("[!] Imagen no encontrada.", 0.02, Colors.RED)
            input(f"\n{self.lang.get('press_enter')}")
            return

        self.ui.loading("Buscando datos ocultos...", 1.5)
        success, result = stego_manager.extract_data(stego_path)

        if success:
            if os.path.exists(Config.DATA_FILE):
                confirm = input(f"{Colors.RED}[⚠] ¿Sobrescribir base de datos actual? (s/n): {Colors.RESET}").lower()
                if confirm != 's': return
            
            with open(Config.DATA_FILE, 'wb') as f:
                f.write(result)

            self.ui.typewriter("\n[✓] Base de datos restaurada con éxito.", 0.02, Colors.GREEN)
            self.pm = PasswordManager(self.crypto)
            self.pm.load()
        else:
            self.ui.typewriter(f"\n[✗] {result}", 0.02, Colors.RED)
        input(f"\n{self.lang.get('press_enter')}")

    def run(self):
        """Ejecutar la aplicación principal"""
        self.check_usb_mode()
        self.load_preferences()
        
        if not os.path.exists(Config.SALT_FILE):
            if not self.first_time_setup(): return
        
        if not self.login(): return
        
        self.check_notifications()
        self.menu = MenuSystem(self.pm, self.lang)
        
        while True:
            opcion = self.menu.show_main_menu().lower()
            if opcion == "1": self.add_credential_flow()
            elif opcion == "2": self.retrieve_credential_flow()
            elif opcion == "3": self.list_services_flow()
            elif opcion == "4": self.delete_credential_flow()
            elif opcion == "5": self.backup_flow()
            elif opcion == "6": self.statistics_flow()
            elif opcion == "7": self.search_flow()
            elif opcion == "8": self.change_language_flow()
            elif opcion == "c": self.manage_categories_flow()
            elif opcion == "t": self._manage_tags_flow()
            elif opcion == "g": self.generate_password_flow()
            elif opcion == "n": self.view_notifications_flow()
            elif opcion == "m": self.secure_notes_flow()
            elif opcion == "f": self.file_vault_flow()
            elif opcion == "x": self.steganography_flow()
            elif opcion == "u": self.launch_gui_flow()
            elif opcion == "i": self.install_usb_flow()
            elif opcion == "s": self.create_stealth_usb()
            elif opcion == "h": self.show_help()
            elif opcion == "9":
                self.ui.typewriter(f"\n{self.lang.get('system_shutdown')}", 0.02, Colors.GREEN)
                break
            else:
                self.ui.typewriter(self.lang.get("invalid_command"), 0.02, Colors.RED)

if __name__ == "__main__":
    try:
        app = DNOEncryptx()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}[!] EMERGENCY SHUTDOWN{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}[!] CRITICAL ERROR: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        input("Press ENTER to exit...")