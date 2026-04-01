"""
Módulo de menús - DNO Encryptx
"""

import time
from colors import Colors
from banner import get_banner, get_header
from ui_effects import UIEffects

class MenuSystem:
    """Sistema de menús interactivo"""
    
    def __init__(self, pm, lang):
        self.pm = pm
        self.ui = UIEffects()
        self.lang = lang
    
    def show_main_menu(self):
        """Mostrar menú principal"""
        self.ui.clear_screen()
        print(get_banner())
        
        print(f"\n{Colors.GREEN}{'█' * 70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}   ⚡ {self.lang.get('main_operations')} ⚡{Colors.RESET}")
        print(f"{Colors.GREEN}{'█' * 70}{Colors.RESET}")
        
        # Menú maquetado con espacios fijos y borde derecho abierto para evitar desalineación
        menu = f"""
{Colors.YELLOW}  ┌──────────────────────────────────────────────────────────────────────{Colors.RESET}
{Colors.YELLOW}  │{Colors.RESET}  {Colors.GREEN}[1]{Colors.RESET} 🔐 Agregar contraseña       {Colors.GREEN}[5]{Colors.RESET} 💾 Crear backup             
{Colors.YELLOW}  │{Colors.RESET}  {Colors.GREEN}[2]{Colors.RESET} 👁️  Ver contraseña          {Colors.GREEN}[6]{Colors.RESET} 📊 Estadísticas             
{Colors.YELLOW}  │{Colors.RESET}  {Colors.GREEN}[3]{Colors.RESET} 📋 Listar servicios         {Colors.GREEN}[7]{Colors.RESET} 🔍 Buscar                   
{Colors.YELLOW}  │{Colors.RESET}  {Colors.GREEN}[4]{Colors.RESET} 🗑️  Eliminar                {Colors.GREEN}[8]{Colors.RESET} 🌐 Idioma                   
{Colors.YELLOW}  │{Colors.RESET}  {Colors.GREEN}[C]{Colors.RESET} 📁 Categorías               {Colors.GREEN}[T]{Colors.RESET} 🏷️ Etiquetas                
{Colors.YELLOW}  │{Colors.RESET}  {Colors.GREEN}[G]{Colors.RESET} 🔑 Generar                  {Colors.GREEN}[N]{Colors.RESET} 🔔 Notificaciones           
{Colors.YELLOW}  │{Colors.RESET}  {Colors.GREEN}[I]{Colors.RESET} 📀 Instalar USB             {Colors.GREEN}[S]{Colors.RESET} 🎭 Stealth                  
{Colors.YELLOW}  │{Colors.RESET}  {Colors.GREEN}[M]{Colors.RESET} 📝 Notas Seguras            {Colors.GREEN}[X]{Colors.RESET} 🖼️  Imagen Bóveda (Stego) 
{Colors.YELLOW}  │{Colors.RESET}  {Colors.GREEN}[F]{Colors.RESET} 📁 File Vault (Archivos)    {Colors.GREEN}[U]{Colors.RESET} 🖥️  Interfaz Gráfica (GUI) 
{Colors.YELLOW}  │{Colors.RESET}  {Colors.GREEN}[H]{Colors.RESET} 🆘 Ayuda                    {Colors.GREEN}[0]{Colors.RESET} 🎨 Matrix                   
{Colors.YELLOW}  │{Colors.RESET}  {Colors.GREEN}[9]{Colors.RESET} 🚪 Salir                    {' ' * 31}
{Colors.YELLOW}  └──────────────────────────────────────────────────────────────────────{Colors.RESET}
"""
        print(menu)
        
        return input(f"{Colors.CYAN}[{Colors.BOLD}DNO-Encryptx{Colors.RESET}{Colors.CYAN}]~# {Colors.RESET}").strip()
        
    def show_credentials_list(self):
        """Mostrar lista de credenciales"""
        services = self.pm.list_all()
        
        if not services:
            self.ui.typewriter(self.lang.get("no_credentials"), 0.02, Colors.YELLOW)
            return False
        
        print(f"\n{Colors.CYAN}┌{'─' * 66}┐{Colors.RESET}")
        title = self.lang.get('active_credentials', total=len(services))
        print(f"{Colors.CYAN}│{Colors.BOLD}{Colors.GREEN}   {title}{' ' * (66 - len(title) - 3)}{Colors.CYAN}│{Colors.RESET}")
        print(f"{Colors.CYAN}├{'─' * 66}┤{Colors.RESET}")
        
        for i, service in enumerate(services, 1):
            # Mostrar categoría si existe
            info = self.pm.get(service)
            category = info.get('category', '📁') if info else '📁'
            print(f"{Colors.CYAN}│{Colors.RESET} {Colors.YELLOW}{i:2}.{Colors.RESET} {Colors.GREEN}{service:<40}{Colors.RESET} {Colors.DIM}{category:<12}{Colors.CYAN}│{Colors.RESET}")
        
        print(f"{Colors.CYAN}└{'─' * 66}┘{Colors.RESET}")
        return True
    
    def show_credential_details(self, service):
        """Mostrar detalles de una credencial con categoría y etiquetas"""
        entry = self.pm.get(service)
        if not entry:
            self.ui.typewriter(self.lang.get("service_not_found", service=service), 0.02, Colors.RED)
            return None
        
        # Obtener datos
        username = entry.get('username', 'N/A')
        password = entry.get('password', 'N/A')
        created = entry.get('created', 'N/A')
        updated = entry.get('updated', created)
        category = entry.get('category', '📁 Otros')
        tags = entry.get('tags', [])
        
        print(f"\n{Colors.GREEN}{'─' * 70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}   >>> {service.upper()} <<<{Colors.RESET}")
        print(f"{Colors.GREEN}{'─' * 70}{Colors.RESET}")
        print(f"{Colors.YELLOW}[+] Categoría:{Colors.RESET} {category}")
        print(f"{Colors.YELLOW}[+] Usuario:{Colors.RESET} {username}")
        print(f"{Colors.YELLOW}[+] Contraseña:{Colors.RESET} {password}")
        if tags:
            tags_str = ", ".join([f"#{t}" for t in tags])
            print(f"{Colors.YELLOW}[+] Etiquetas:{Colors.RESET} {tags_str}")
        print(f"{Colors.YELLOW}[+] Creado:{Colors.RESET} {created}")
        print(f"{Colors.YELLOW}[+] Actualizado:{Colors.RESET} {updated}")
        print(f"{Colors.GREEN}{'─' * 70}{Colors.RESET}")
        
        return entry
    
    def show_stats(self):
        """Mostrar estadísticas"""
        stats = self.pm.get_stats()
        cat_stats = self.pm.get_category_stats()
        
        print(f"\n{Colors.CYAN}[+] {self.lang.get('total_credentials')}:{Colors.RESET} {Colors.YELLOW}{stats['total']}{Colors.RESET}")
        if stats.get('last_update'):
            print(f"{Colors.CYAN}[+] {self.lang.get('last_update')}:{Colors.RESET} {Colors.GREEN}{stats['last_update']}{Colors.RESET}")
        
        if cat_stats:
            print(f"\n{Colors.CYAN}[+] Distribución por categoría:{Colors.RESET}")
            for cat, count in sorted(cat_stats.items(), key=lambda x: -x[1]):
                print(f"   {Colors.YELLOW}•{Colors.RESET} {cat}: {count}")