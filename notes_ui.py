"""
Módulo de interfaz para Notas Seguras - DNO Encryptx
"""

import getpass
from colors import Colors
from banner import get_banner, get_header
from secure_notes import SecureNotesManager

class NotesUI:
    """Interfaz de usuario para el sistema de notas seguras"""
    
    def __init__(self, ui, lang, crypto):
        self.ui = ui
        self.lang = lang
        self.notes_manager = SecureNotesManager(crypto)
    
    def show_main_menu(self):
        """Mostrar menú principal de notas"""
        while True:
            self.ui.clear_screen()
            print(get_banner())
            print(get_header("📝 NOTAS SEGURAS"))
            
            stats = self.notes_manager.get_stats()
            
            print(f"\n{Colors.CYAN}{'═' * 70}{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.GREEN}   📊 ESTADÍSTICAS{Colors.RESET}")
            print(f"{Colors.CYAN}{'═' * 70}{Colors.RESET}")
            print(f"{Colors.YELLOW}[+] Total de notas:{Colors.RESET} {stats['total']}")
            for note_type, count in stats['by_type'].items():
                icon = SecureNotesManager.NOTE_TYPES.get(note_type, {'icon': '📝'})['icon']
                name = SecureNotesManager.NOTE_TYPES.get(note_type, {'name': note_type})['name']
                print(f"   {icon} {name}: {count}")
            
            print(f"\n{Colors.CYAN}{'═' * 70}{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.GREEN}   📋 OPCIONES{Colors.RESET}")
            print(f"{Colors.CYAN}{'═' * 70}{Colors.RESET}")
            print(f"{Colors.GREEN}[1]{Colors.RESET} 📝 Ver todas las notas")
            print(f"{Colors.GREEN}[2]{Colors.RESET} ➕ Crear nueva nota")
            print(f"{Colors.GREEN}[3]{Colors.RESET} 👁️ Ver nota específica")
            print(f"{Colors.GREEN}[4]{Colors.RESET} ✏️ Editar nota")
            print(f"{Colors.GREEN}[5]{Colors.RESET} 🗑️ Eliminar nota")
            print(f"{Colors.GREEN}[6]{Colors.RESET} 🔍 Buscar notas")
            print(f"{Colors.GREEN}[7]{Colors.RESET} 💳 Crear tarjeta de crédito")
            print(f"{Colors.GREEN}[8]{Colors.RESET} 📄 Crear documento seguro")
            print(f"{Colors.GREEN}[9]{Colors.RESET} 🔑 Crear código/contraseña")
            print(f"{Colors.GREEN}[0]{Colors.RESET} 📤 Exportar nota")
            print(f"{Colors.GREEN}[B]{Colors.RESET} 🔙 Volver al menú principal")
            
            opcion = input(f"\n{Colors.CYAN}[Notas]~# {Colors.RESET}").strip().upper()
            
            if opcion == "1":
                self.list_notes()
            elif opcion == "2":
                self.create_note()
            elif opcion == "3":
                self.view_note()
            elif opcion == "4":
                self.edit_note()
            elif opcion == "5":
                self.delete_note()
            elif opcion == "6":
                self.search_notes()
            elif opcion == "7":
                self.create_credit_card()
            elif opcion == "8":
                self.create_document()
            elif opcion == "9":
                self.create_code()
            elif opcion == "0":
                self.export_note()
            elif opcion == "B":
                break
            else:
                self.ui.typewriter("[!] Opción inválida", 0.02, Colors.RED)
    
    def list_notes(self):
        """Listar todas las notas"""
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("📋 MIS NOTAS"))
        
        notes = self.notes_manager.list_notes()
        if not notes:
            self.ui.typewriter("[!] No hay notas guardadas", 0.02, Colors.YELLOW)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        print(f"\n{Colors.CYAN}{'─' * 70}{Colors.RESET}")
        for i, note in enumerate(notes, 1):
            icon = note['icon']
            title = note['title']
            note_type = note['type']
            updated = note['updated']
            print(f"{Colors.GREEN}{i:2}.{Colors.RESET} {icon} {Colors.CYAN}{title}{Colors.RESET}")
            print(f"     {Colors.DIM}Tipo: {note_type} | Actualizado: {updated}{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}{'─' * 70}{Colors.RESET}")
        input(f"\n{self.lang.get('press_enter')}")
    
    def create_note(self):
        """Crear nueva nota"""
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("➕ CREAR NUEVA NOTA"))
        
        title = input(f"\n{Colors.CYAN}[?] Título: {Colors.RESET}").strip()
        if not title:
            self.ui.typewriter("[!] Título requerido", 0.02, Colors.RED)
            return
        
        print(f"\n{Colors.CYAN}Tipo de nota:{Colors.RESET}")
        for i, (key, info) in enumerate(SecureNotesManager.NOTE_TYPES.items(), 1):
            print(f"   {Colors.GREEN}{i}.{Colors.RESET} {info['icon']} {info['name']}")
        
        type_choice = input(f"\n{Colors.CYAN}[?] Tipo (1-{len(SecureNotesManager.NOTE_TYPES)}): {Colors.RESET}").strip()
        types_list = list(SecureNotesManager.NOTE_TYPES.keys())
        if type_choice.isdigit() and 1 <= int(type_choice) <= len(types_list):
            note_type = types_list[int(type_choice)-1]
        else:
            note_type = "text"
        
        print(f"\n{Colors.CYAN}[?] Contenido (Ctrl+Z o línea vacía para terminar):{Colors.RESET}")
        lines = []
        while True:
            try:
                line = input()
                if line == "":
                    break
                lines.append(line)
            except EOFError:
                break
        content = "\n".join(lines)
        
        tags_input = input(f"\n{Colors.CYAN}[?] Etiquetas (separadas por comas): {Colors.RESET}").strip()
        tags = [t.strip() for t in tags_input.split(",") if t.strip()]
        
        success, msg = self.notes_manager.add_note(title, content, note_type, tags)
        self.ui.typewriter(f"[{'✓' if success else '✗'}] {msg}", 0.02, Colors.GREEN if success else Colors.RED)
        input(f"\n{self.lang.get('press_enter')}")
    
    def view_note(self):
        """Ver nota específica"""
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("👁️ VER NOTA"))
        
        notes = self.notes_manager.list_notes()
        if not notes:
            self.ui.typewriter("[!] No hay notas guardadas", 0.02, Colors.YELLOW)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        print(f"\n{Colors.CYAN}Notas disponibles:{Colors.RESET}")
        for i, note in enumerate(notes, 1):
            print(f"   {Colors.GREEN}{i}.{Colors.RESET} {note['icon']} {note['title']}")
        
        title = input(f"\n{Colors.CYAN}[?] Título de la nota: {Colors.RESET}").strip()
        note = self.notes_manager.get_note(title)
        
        if not note:
            self.ui.typewriter("[!] Nota no encontrada", 0.02, Colors.RED)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        self._display_note(note)
        input(f"\n{self.lang.get('press_enter')}")
    
    def _display_note(self, note):
        """Mostrar nota formateada"""
        icon = SecureNotesManager.NOTE_TYPES.get(note.note_type, {'icon': '📝'})['icon']
        print(f"\n{Colors.GREEN}{'═' * 70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}   {icon} {note.title}{Colors.RESET}")
        print(f"{Colors.GREEN}{'═' * 70}{Colors.RESET}")
        print(f"{Colors.YELLOW}Tipo:{Colors.RESET} {note.note_type}")
        print(f"{Colors.YELLOW}Creado:{Colors.RESET} {note.created}")
        print(f"{Colors.YELLOW}Actualizado:{Colors.RESET} {note.updated}")
        if note.tags:
            tags_str = ", ".join([f"#{t}" for t in note.tags])
            print(f"{Colors.YELLOW}Etiquetas:{Colors.RESET} {tags_str}")
        print(f"{Colors.GREEN}{'─' * 70}{Colors.RESET}")
        print(note.content)
        print(f"{Colors.GREEN}{'─' * 70}{Colors.RESET}")
    
    def edit_note(self):
        """Editar nota existente"""
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("✏️ EDITAR NOTA"))
        
        notes = self.notes_manager.list_notes()
        if not notes:
            self.ui.typewriter("[!] No hay notas guardadas", 0.02, Colors.YELLOW)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        print(f"\n{Colors.CYAN}Notas disponibles:{Colors.RESET}")
        for i, note in enumerate(notes, 1):
            print(f"   {Colors.GREEN}{i}.{Colors.RESET} {note['icon']} {note['title']}")
        
        title = input(f"\n{Colors.CYAN}[?] Título de la nota a editar: {Colors.RESET}").strip()
        note = self.notes_manager.get_note(title)
        
        if not note:
            self.ui.typewriter("[!] Nota no encontrada", 0.02, Colors.RED)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        print(f"\n{Colors.CYAN}Contenido actual:{Colors.RESET}")
        print(f"{Colors.DIM}{note.content}{Colors.RESET}")
        print(f"\n{Colors.CYAN}[?] Nuevo contenido (Ctrl+Z o línea vacía para mantener):{Colors.RESET}")
        lines = []
        while True:
            try:
                line = input()
                if line == "":
                    break
                lines.append(line)
            except EOFError:
                break
        
        new_content = "\n".join(lines) if lines else note.content
        success, msg = self.notes_manager.update_note(title, new_content)
        self.ui.typewriter(f"[{'✓' if success else '✗'}] {msg}", 0.02, Colors.GREEN if success else Colors.RED)
        input(f"\n{self.lang.get('press_enter')}")
    
    def delete_note(self):
        """Eliminar nota"""
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("🗑️ ELIMINAR NOTA"))
        
        notes = self.notes_manager.list_notes()
        if not notes:
            self.ui.typewriter("[!] No hay notas guardadas", 0.02, Colors.YELLOW)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        print(f"\n{Colors.CYAN}Notas disponibles:{Colors.RESET}")
        for i, note in enumerate(notes, 1):
            print(f"   {Colors.GREEN}{i}.{Colors.RESET} {note['icon']} {note['title']}")
        
        title = input(f"\n{Colors.CYAN}[?] Título de la nota a eliminar: {Colors.RESET}").strip()
        confirm = input(f"{Colors.RED}[⚠] ¿Eliminar permanentemente '{title}'? (s/n): {Colors.RESET}").lower()
        
        if confirm == 's':
            success, msg = self.notes_manager.delete_note(title)
            self.ui.typewriter(f"[{'✓' if success else '✗'}] {msg}", 0.02, Colors.GREEN if success else Colors.RED)
        
        input(f"\n{self.lang.get('press_enter')}")
    
    def search_notes(self):
        """Buscar notas"""
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("🔍 BUSCAR NOTAS"))
        
        query = input(f"\n{Colors.CYAN}[?] Buscar (título, contenido o etiqueta): {Colors.RESET}").strip()
        if not query:
            return
        
        results = self.notes_manager.search_notes(query)
        
        if not results:
            self.ui.typewriter("[!] No se encontraron resultados", 0.02, Colors.YELLOW)
        else:
            print(f"\n{Colors.GREEN}✓ Encontradas {len(results)} nota(s):{Colors.RESET}")
            for r in results:
                print(f"\n   {Colors.YELLOW}→{Colors.RESET} {r['icon']} {Colors.CYAN}{r['title']}{Colors.RESET}")
                print(f"     {Colors.DIM}{r['preview']}{Colors.RESET}")
        
        input(f"\n{self.lang.get('press_enter')}")
    
    def create_credit_card(self):
        """Crear tarjeta de crédito segura"""
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("💳 TARJETA DE CRÉDITO"))
        
        title = input(f"\n{Colors.CYAN}[?] Título (ej: Visa Personal): {Colors.RESET}").strip()
        if not title:
            title = "Tarjeta de Crédito"
        
        card_info = []
        card_info.append("=== DATOS DE LA TARJETA ===")
        card_info.append(f"Banco: {input(f'{Colors.CYAN}[?] Banco: {Colors.RESET}').strip()}")
        card_info.append(f"Tipo: {input(f'{Colors.CYAN}[?] Tipo (Visa/Mastercard/Amex): {Colors.RESET}').strip()}")
        card_info.append(f"Número: {input(f'{Colors.CYAN}[?] Número: {Colors.RESET}').strip()}")
        card_info.append(f"Titular: {input(f'{Colors.CYAN}[?] Titular: {Colors.RESET}').strip()}")
        card_info.append(f"Vencimiento: {input(f'{Colors.CYAN}[?] Vencimiento (MM/AA): {Colors.RESET}').strip()}")
        card_info.append(f"CVV: {getpass.getpass(f'{Colors.CYAN}[?] CVV: {Colors.RESET}')}")
        
        content = "\n".join(card_info)
        success, msg = self.notes_manager.add_note(title, content, "credit_card")
        self.ui.typewriter(f"[{'✓' if success else '✗'}] {msg}", 0.02, Colors.GREEN if success else Colors.RED)
        input(f"\n{self.lang.get('press_enter')}")
    
    def create_document(self):
        """Crear documento seguro"""
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("📄 DOCUMENTO SEGURO"))
        
        title = input(f"\n{Colors.CYAN}[?] Título del documento: {Colors.RESET}").strip()
        if not title:
            self.ui.typewriter("[!] Título requerido", 0.02, Colors.RED)
            return
        
        doc_type = input(f"{Colors.CYAN}[?] Tipo de documento (DNI/Pasaporte/Licencia/Otro): {Colors.RESET}").strip()
        number = input(f"{Colors.CYAN}[?] Número: {Colors.RESET}").strip()
        issue_date = input(f"{Colors.CYAN}[?] Fecha de emisión: {Colors.RESET}").strip()
        expiry_date = input(f"{Colors.CYAN}[?] Fecha de vencimiento: {Colors.RESET}").strip()
        
        content = f"""=== {doc_type.upper()} ===
Número: {number}
Emisión: {issue_date}
Vencimiento: {expiry_date}"""
        
        success, msg = self.notes_manager.add_note(title, content, "document")
        self.ui.typewriter(f"[{'✓' if success else '✗'}] {msg}", 0.02, Colors.GREEN if success else Colors.RED)
        input(f"\n{self.lang.get('press_enter')}")
    
    def create_code(self):
        """Crear código o contraseña segura"""
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("🔑 CÓDIGO SEGURO"))
        
        title = input(f"\n{Colors.CYAN}[?] Título (ej: Código WiFi, PIN SIM): {Colors.RESET}").strip()
        if not title:
            self.ui.typewriter("[!] Título requerido", 0.02, Colors.RED)
            return
        
        code_type = input(f"{Colors.CYAN}[?] Tipo (PIN/Clave/Código/Token): {Colors.RESET}").strip()
        code = getpass.getpass(f"{Colors.CYAN}[?] Código/Contraseña: {Colors.RESET}")
        description = input(f"{Colors.CYAN}[?] Descripción: {Colors.RESET}").strip()
        
        content = f"""=== {code_type.upper()} ===
Código: {code}
Descripción: {description}"""
        
        success, msg = self.notes_manager.add_note(title, content, "code")
        self.ui.typewriter(f"[{'✓' if success else '✗'}] {msg}", 0.02, Colors.GREEN if success else Colors.RED)
        input(f"\n{self.lang.get('press_enter')}")
    
    def export_note(self):
        """Exportar nota a archivo"""
        self.ui.clear_screen()
        print(get_banner())
        print(get_header("📤 EXPORTAR NOTA"))
        
        notes = self.notes_manager.list_notes()
        if not notes:
            self.ui.typewriter("[!] No hay notas guardadas", 0.02, Colors.YELLOW)
            input(f"\n{self.lang.get('press_enter')}")
            return
        
        print(f"\n{Colors.CYAN}Notas disponibles:{Colors.RESET}")
        for i, note in enumerate(notes, 1):
            print(f"   {Colors.GREEN}{i}.{Colors.RESET} {note['icon']} {note['title']}")
        
        title = input(f"\n{Colors.CYAN}[?] Título de la nota a exportar: {Colors.RESET}").strip()
        filename = input(f"{Colors.CYAN}[?] Nombre del archivo (dejar vacío para automático): {Colors.RESET}").strip()
        
        success, msg = self.notes_manager.export_note(title, filename if filename else None)
        self.ui.typewriter(f"[{'✓' if success else '✗'}] {msg}", 0.02, Colors.GREEN if success else Colors.RED)
        input(f"\n{self.lang.get('press_enter')}")