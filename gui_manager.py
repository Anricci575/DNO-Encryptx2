"""
Módulo de Interfaz Gráfica - DNO Encryptx
GUI con Tkinter para gestión de contraseñas, File Vault y Esteganografía
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog, simpledialog
import threading
import time
import os
import json
import base64
from datetime import datetime

class PasswordManagerGUI:
    """Interfaz gráfica para el gestor de contraseñas"""
    
    def __init__(self, pm, crypto, lang, notification_manager):
        self.pm = pm
        self.crypto = crypto
        self.lang = lang
        self.notification_manager = notification_manager
        
        # Inicializar FileVault
        from file_vault import FileVault
        self.file_vault = FileVault(self.crypto)
        
        # Inicializar Esteganografía
        from steganography import Steganography
        self.stego_manager = Steganography()
        
        self.root = tk.Tk()
        self.root.title("DNO-Encryptx - Gestor de Contraseñas")
        self.root.geometry("1000x650")
        self.root.configure(bg='#1a1a2e')
        
        # Configurar estilo
        self.setup_styles()
        
        # Variable para controlar la pestaña actual
        self.current_tab = tk.StringVar(value="passwords")
        
        self.setup_ui()
        
    def setup_styles(self):
        """Configurar estilos de la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores personalizados
        style.configure('Dark.TFrame', background='#1a1a2e')
        style.configure('Dark.TLabel', background='#1a1a2e', foreground='#00ff00')
        style.configure('Dark.TButton', background='#16213e', foreground='#00ff00', borderwidth=0)
        style.map('Dark.TButton', background=[('active', '#0f3460')])
        
        style.configure('Treeview', background='#16213e', foreground='#00ff00', fieldbackground='#16213e')
        style.configure('Treeview.Heading', background='#0f3460', foreground='#00ff00')
        
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_label = ttk.Label(main_frame, text="🔐 DNO-ENCRYPTX v2.0", 
                                font=('Courier', 18, 'bold'), 
                                style='Dark.TLabel')
        title_label.pack(pady=10)
        
        self.status_bar = ttk.Label(main_frame, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestañas
        self.passwords_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.passwords_tab, text="📁 Contraseñas")
        self.setup_passwords_tab()
        
        self.notes_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.notes_tab, text="📝 Notas Seguras")
        self.setup_notes_tab()
        
        self.vault_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.vault_tab, text="📦 File Vault")
        self.setup_vault_tab()
        
        self.stats_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.stats_tab, text="📊 Estadísticas")
        self.setup_stats_tab()
        
        self.config_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.config_tab, text="⚙️ Configuración")
        self.setup_config_tab()

    # =========================================================================
    # PESTAÑA: CONTRASEÑAS
    # =========================================================================
    def setup_passwords_tab(self):
        list_frame = ttk.Frame(self.passwords_tab, style='Dark.TFrame')
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ('Servicio', 'Usuario', 'Categoría', 'Actualizado')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        details_frame = ttk.Frame(self.passwords_tab, style='Dark.TFrame')
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        btn_frame = ttk.Frame(details_frame, style='Dark.TFrame')
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="➕ Agregar", command=self.add_password_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="👁️ Ver", command=self.view_password).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="✏️ Editar", command=self.edit_password).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="🗑️ Eliminar", command=self.delete_password).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="🔄 Actualizar", command=self.refresh_passwords).pack(side=tk.LEFT, padx=2)
        
        info_frame = ttk.LabelFrame(details_frame, text="Detalles", style='Dark.TFrame')
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.service_label = ttk.Label(info_frame, text="Servicio: -", style='Dark.TLabel')
        self.service_label.pack(anchor=tk.W, padx=5, pady=2)
        self.username_label = ttk.Label(info_frame, text="Usuario: -", style='Dark.TLabel')
        self.username_label.pack(anchor=tk.W, padx=5, pady=2)
        self.password_label = ttk.Label(info_frame, text="Contraseña: ***", style='Dark.TLabel')
        self.password_label.pack(anchor=tk.W, padx=5, pady=2)
        self.category_label = ttk.Label(info_frame, text="Categoría: -", style='Dark.TLabel')
        self.category_label.pack(anchor=tk.W, padx=5, pady=2)
        self.created_label = ttk.Label(info_frame, text="Creado: -", style='Dark.TLabel')
        self.created_label.pack(anchor=tk.W, padx=5, pady=2)
        
        ttk.Button(details_frame, text="📋 Copiar Contraseña", command=self.copy_password).pack(pady=10)
        self.refresh_passwords()

    def refresh_passwords(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.pm.load()
        for service, info in self.pm.data.items():
            self.tree.insert('', tk.END, values=(
                service,
                info.get('username', 'N/A'),
                info.get('category', '📁 Otros'),
                info.get('updated', info.get('created', 'N/A'))
            ))
        self.status_bar.config(text=f"Total: {len(self.pm.data)} contraseñas")
        
    def add_password_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Contraseña")
        dialog.geometry("400x350")
        dialog.configure(bg='#1a1a2e')
        
        ttk.Label(dialog, text="Servicio:", style='Dark.TLabel').pack(pady=5)
        service_entry = ttk.Entry(dialog, width=40)
        service_entry.pack(pady=5)
        ttk.Label(dialog, text="Usuario/Email:", style='Dark.TLabel').pack(pady=5)
        username_entry = ttk.Entry(dialog, width=40)
        username_entry.pack(pady=5)
        ttk.Label(dialog, text="Contraseña:", style='Dark.TLabel').pack(pady=5)
        password_entry = ttk.Entry(dialog, width=40, show="*")
        password_entry.pack(pady=5)
        show_var = tk.BooleanVar()
        ttk.Checkbutton(dialog, text="Mostrar contraseña", variable=show_var, command=lambda: password_entry.config(show="" if show_var.get() else "*")).pack()
        ttk.Label(dialog, text="Categoría:", style='Dark.TLabel').pack(pady=5)
        category_entry = ttk.Entry(dialog, width=40)
        category_entry.pack(pady=5)
        
        def save():
            service = service_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get()
            category = category_entry.get().strip() or "📁 Otros"
            if not service or not username or not password:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            self.pm.add(service, username, password, category)
            self.refresh_passwords()
            dialog.destroy()
            self.status_bar.config(text=f"✓ Contraseña '{service}' agregada")
            
        ttk.Button(dialog, text="Guardar", command=save).pack(pady=20)
        
    def view_password(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Selección", "Selecciona una contraseña primero")
            return
        item = self.tree.item(selection[0])
        service = item['values'][0]
        info = self.pm.get(service)
        if info:
            self.service_label.config(text=f"Servicio: {service}")
            self.username_label.config(text=f"Usuario: {info.get('username', 'N/A')}")
            self.password_label.config(text=f"Contraseña: {info.get('password', 'N/A')}")
            self.category_label.config(text=f"Categoría: {info.get('category', '📁 Otros')}")
            self.created_label.config(text=f"Creado: {info.get('created', 'N/A')}")
            
    def edit_password(self):
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0])
        service = item['values'][0]
        info = self.pm.get(service)
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Editar - {service}")
        dialog.geometry("400x350")
        dialog.configure(bg='#1a1a2e')
        
        ttk.Label(dialog, text="Servicio:", style='Dark.TLabel').pack(pady=5)
        service_entry = ttk.Entry(dialog, width=40)
        service_entry.insert(0, service)
        service_entry.pack(pady=5)
        service_entry.config(state='readonly')
        ttk.Label(dialog, text="Usuario/Email:", style='Dark.TLabel').pack(pady=5)
        username_entry = ttk.Entry(dialog, width=40)
        username_entry.insert(0, info.get('username', ''))
        username_entry.pack(pady=5)
        ttk.Label(dialog, text="Nueva Contraseña:", style='Dark.TLabel').pack(pady=5)
        password_entry = ttk.Entry(dialog, width=40, show="*")
        password_entry.insert(0, info.get('password', ''))
        password_entry.pack(pady=5)
        
        def save():
            self.pm.add(service, username_entry.get().strip(), password_entry.get())
            self.refresh_passwords()
            dialog.destroy()
            self.status_bar.config(text=f"✓ Contraseña '{service}' actualizada")
            
        ttk.Button(dialog, text="Actualizar", command=save).pack(pady=20)
        
    def delete_password(self):
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0])
        service = item['values'][0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{service}' permanentemente?"):
            self.pm.delete(service)
            self.refresh_passwords()
            self.status_bar.config(text=f"✓ Contraseña '{service}' eliminada")
            
    def copy_password(self):
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0])
        service = item['values'][0]
        info = self.pm.get(service)
        if info:
            self.root.clipboard_clear()
            self.root.clipboard_append(info.get('password', ''))
            self.status_bar.config(text="✓ Contraseña copiada al portapapeles")

    # =========================================================================
    # PESTAÑA: FILE VAULT (VISOR SEGURO)
    # =========================================================================
    def setup_vault_tab(self):
        list_frame = ttk.Frame(self.vault_tab, style='Dark.TFrame')
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ('Archivo Físico', 'Nombre Original', 'Tamaño', 'Protección', 'Fecha')
        self.vault_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        self.vault_tree.heading('Archivo Físico', text='Archivo (.dno)')
        self.vault_tree.heading('Nombre Original', text='Nombre Original')
        self.vault_tree.heading('Tamaño', text='Tamaño (MB)')
        self.vault_tree.heading('Protección', text='Protección')
        self.vault_tree.heading('Fecha', text='Fecha Cifrado')
        
        self.vault_tree.column('Archivo Físico', width=120)
        self.vault_tree.column('Nombre Original', width=150)
        self.vault_tree.column('Tamaño', width=80)
        self.vault_tree.column('Protección', width=100)
        self.vault_tree.column('Fecha', width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.vault_tree.yview)
        self.vault_tree.configure(yscrollcommand=scrollbar.set)
        self.vault_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        action_frame = ttk.Frame(self.vault_tab, style='Dark.TFrame')
        action_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=15, pady=20)
        ttk.Label(action_frame, text="🛡️ Acciones de Bóveda", font=('Courier', 12, 'bold'), style='Dark.TLabel').pack(pady=15)
        ttk.Button(action_frame, text="➕ Encriptar Archivo", command=self.vault_encrypt).pack(fill=tk.X, pady=5)
        ttk.Button(action_frame, text="👁️ VER EN RAM (Seguro)", command=self.vault_view_ram).pack(fill=tk.X, pady=5)
        ttk.Button(action_frame, text="🔓 Extraer a Disco", command=self.vault_extract).pack(fill=tk.X, pady=5)
        ttk.Button(action_frame, text="🗑️ Eliminar Archivo", command=self.vault_delete).pack(fill=tk.X, pady=5)
        ttk.Button(action_frame, text="🔄 Actualizar Lista", command=self.refresh_vault).pack(fill=tk.X, pady=25)
        
        self.refresh_vault()

    def refresh_vault(self):
        for item in self.vault_tree.get_children():
            self.vault_tree.delete(item)
        files = self.file_vault.list_vault_files()
        for f in files:
            protection = "🔐 Maestra" if f['use_master_key'] else "🔑 Personalizada"
            self.vault_tree.insert('', tk.END, values=(
                f['filename'],
                f"{f['icon']} {f['original_name']}",
                f"{f['size_mb']:.2f}",
                protection,
                f['created']
            ))
            
    def vault_encrypt(self):
        file_path = filedialog.askopenfilename(title="Seleccionar archivo a proteger")
        if not file_path:
            return
        use_custom = messagebox.askyesno("Protección", "¿Deseas protegerlo con una contraseña personalizada?\n(Si eliges 'No', usará la clave maestra del programa)")
        custom_password = None
        if use_custom:
            custom_password = simpledialog.askstring("Contraseña", "Ingresa la contraseña personalizada:", show='*')
            if not custom_password:
                return
        success, msg, path = self.file_vault.encrypt_file(file_path, use_master_key=not use_custom, custom_password=custom_password)
        if success:
            self.status_bar.config(text=f"✓ {msg}")
            self.refresh_vault()
        else:
            messagebox.showerror("Error", msg)

    def vault_extract(self):
        selection = self.vault_tree.selection()
        if not selection:
            messagebox.showwarning("Selección", "Selecciona un archivo de la bóveda primero")
            return
        item = self.vault_tree.item(selection[0])
        filename = item['values'][0]
        file_info = self.file_vault.get_file_info(filename)
        
        custom_password = None
        if not file_info['use_master_key']:
            custom_password = simpledialog.askstring("Contraseña", "Este archivo usa contraseña personalizada.\nIngresa la clave:", show='*')
            if not custom_password:
                return
        out_dir = filedialog.askdirectory(title="Seleccionar carpeta de extracción")
        if not out_dir:
            return
        file_path = os.path.join(self.file_vault.vault_path, filename)
        success, msg, path = self.file_vault.decrypt_file(file_path, output_dir=out_dir, custom_password=custom_password)
        if success:
            self.status_bar.config(text=f"✓ Archivo extraído a: {path}")
            messagebox.showinfo("Éxito", f"Archivo extraído en:\n{path}")
        else:
            messagebox.showerror("Error", msg)

    def vault_delete(self):
        selection = self.vault_tree.selection()
        if not selection:
            return
        item = self.vault_tree.item(selection[0])
        filename = item['values'][0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar {filename} permanentemente?"):
            success, msg = self.file_vault.delete_file(filename)
            self.refresh_vault()
            self.status_bar.config(text=f"✓ {msg}")

    def vault_view_ram(self):
        selection = self.vault_tree.selection()
        if not selection:
            messagebox.showwarning("Selección", "Selecciona un archivo primero")
            return
        item = self.vault_tree.item(selection[0])
        filename = item['values'][0]
        file_info = self.file_vault.get_file_info(filename)
        
        if not file_info:
            return
        custom_password = None
        if not file_info['use_master_key']:
            custom_password = simpledialog.askstring("Contraseña", "Este archivo usa contraseña personalizada.\nIngresa la clave:", show='*')
            if not custom_password:
                return
        try:
            from cryptography.fernet import Fernet
            with open(file_info['path'], 'rb') as f:
                metadata_len = int.from_bytes(f.read(4), 'big')
                metadata_json = f.read(metadata_len)
                metadata = json.loads(metadata_json.decode())
                encrypted_data = f.read()
            if metadata.get('use_master_key', True):
                cipher = self.crypto.cipher
            else:
                salt = base64.b64decode(metadata.get('salt', ''))
                key, _ = self.file_vault._generate_key_from_password(custom_password, salt)
                cipher = Fernet(key)
                
            decrypted_data = cipher.decrypt(encrypted_data)
            self._show_secure_viewer(metadata['original_name'], decrypted_data, metadata['file_type'])
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al desencriptar.\n¿Contraseña incorrecta?\nDetalle: {e}")

    def _show_secure_viewer(self, name, data, ftype):
        viewer = tk.Toplevel(self.root)
        viewer.title(f"👁️ Visor Seguro RAM - {name}")
        viewer.geometry("800x600")
        viewer.configure(bg='#000000')
        
        lbl = tk.Label(viewer, text="[!] MODO SEGURO: Los datos están solo en la memoria RAM y desaparecerán al cerrar.", 
                       bg='red', fg='white', font=('Courier', 10, 'bold'))
        lbl.pack(fill=tk.X)
        
        if ftype in ['document', 'code', 'other']:
            try:
                text_data = data.decode('utf-8')
                txt = scrolledtext.ScrolledText(viewer, bg='#0d0d0d', fg='#00ff00', font=('Courier', 11))
                txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                txt.insert(tk.END, text_data)
                txt.config(state=tk.DISABLED)
            except UnicodeDecodeError:
                tk.Label(viewer, text="[!] Archivo binario. No se puede visualizar como texto.", 
                         bg='#000000', fg='yellow', font=('Courier', 12)).pack(pady=100)
        elif ftype == 'image':
            try:
                # 🚀 MEJORA: Usar Pillow para soportar JPG, JPEG, WEBP, etc.
                import io
                from PIL import Image, ImageTk
                
                # Leer la imagen desde la memoria RAM (BytesIO)
                img = Image.open(io.BytesIO(data))
                
                # Redimensionar la imagen si es muy grande para la ventana
                max_size = (750, 500)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                photo = ImageTk.PhotoImage(img)
                img_lbl = tk.Label(viewer, image=photo, bg='#000000')
                img_lbl.image = photo # Evitar que el recolector de basura la elimine
                img_lbl.pack(expand=True, pady=10)
                
            except ImportError:
                # Si no tiene Pillow, intentar con el método nativo (solo PNG/GIF)
                try:
                    photo = tk.PhotoImage(data=data)
                    img_lbl = tk.Label(viewer, image=photo, bg='#000000')
                    img_lbl.image = photo
                    img_lbl.pack(expand=True)
                    tk.Label(viewer, text="[!] Solo formato PNG/GIF. Para ver JPG, instala Pillow (pip install Pillow)", 
                             bg='#000000', fg='orange', font=('Courier', 9)).pack(side=tk.BOTTOM)
                except Exception:
                    tk.Label(viewer, text="[!] Formato no soportado o falta librería Pillow.\nAbre la terminal y escribe:\npip install Pillow", 
                             bg='#000000', fg='yellow', font=('Courier', 12)).pack(pady=100)
            except Exception as e:
                tk.Label(viewer, text=f"[!] Error procesando imagen: {e}", 
                         bg='#000000', fg='red', font=('Courier', 12)).pack(pady=100)
        else:
            tk.Label(viewer, text="[!] Archivo comprimido o formato no soportado para vista previa en RAM.\nUsa la opción 'Extraer a Disco'.", 
                     bg='#000000', fg='yellow', font=('Courier', 12)).pack(pady=100)
                     
        def on_close():
            nonlocal data
            data = b"" # Destruir los bytes de la imagen de la memoria RAM
            viewer.destroy()
        viewer.protocol("WM_DELETE_WINDOW", on_close)

    # =========================================================================
    # PESTAÑA: NOTAS
    # =========================================================================
    def setup_notes_tab(self):
        notes_frame = ttk.Frame(self.notes_tab, style='Dark.TFrame')
        notes_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.notes_listbox = tk.Listbox(notes_frame, bg='#16213e', fg='#00ff00', font=('Courier', 10))
        self.notes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(notes_frame, orient=tk.VERTICAL, command=self.notes_listbox.yview)
        self.notes_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        content_frame = ttk.Frame(self.notes_tab, style='Dark.TFrame')
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        btn_frame = ttk.Frame(content_frame, style='Dark.TFrame')
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="➕ Nueva Nota", command=self.add_note_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="👁️ Ver Nota", command=self.view_note).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="🗑️ Eliminar", command=self.delete_note).pack(side=tk.LEFT, padx=2)
        
        self.note_content = scrolledtext.ScrolledText(content_frame, bg='#16213e', fg='#00ff00', font=('Courier', 10), height=20)
        self.note_content.pack(fill=tk.BOTH, expand=True, pady=10)
        self.note_content.config(state=tk.DISABLED)
        self.refresh_notes()

    def refresh_notes(self):
        self.notes_listbox.delete(0, tk.END)
        try:
            from secure_notes import SecureNotesManager
            notes_manager = SecureNotesManager(self.crypto)
            notes = notes_manager.list_notes()
            for note in notes:
                self.notes_listbox.insert(tk.END, f"{note['icon']} {note['title']} ({note['type']})")
        except:
            pass

    def add_note_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Nota Segura")
        dialog.geometry("500x400")
        dialog.configure(bg='#1a1a2e')
        
        ttk.Label(dialog, text="Título:", style='Dark.TLabel').pack(pady=5)
        title_entry = ttk.Entry(dialog, width=50)
        title_entry.pack(pady=5)
        ttk.Label(dialog, text="Contenido:", style='Dark.TLabel').pack(pady=5)
        content_text = scrolledtext.ScrolledText(dialog, bg='#16213e', fg='#00ff00', height=15)
        content_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        def save():
            title = title_entry.get().strip()
            content = content_text.get("1.0", tk.END).strip()
            if not title:
                messagebox.showerror("Error", "El título es obligatorio")
                return
            try:
                from secure_notes import SecureNotesManager
                notes_manager = SecureNotesManager(self.crypto)
                success, msg = notes_manager.add_note(title, content, "text")
                if success:
                    self.refresh_notes()
                    dialog.destroy()
                    self.status_bar.config(text=f"✓ Nota '{title}' agregada")
                else:
                    messagebox.showerror("Error", msg)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Guardar", command=save).pack(pady=10)

    def view_note(self):
        selection = self.notes_listbox.curselection()
        if not selection:
            return
        note_text = self.notes_listbox.get(selection[0])
        title = note_text.split(' ', 1)[1].split(' (')[0]
        try:
            from secure_notes import SecureNotesManager
            notes_manager = SecureNotesManager(self.crypto)
            note = notes_manager.get_note(title)
            if note:
                self.note_content.config(state=tk.NORMAL)
                self.note_content.delete("1.0", tk.END)
                self.note_content.insert("1.0", note.content)
                self.note_content.config(state=tk.DISABLED)
        except:
            pass

    def delete_note(self):
        selection = self.notes_listbox.curselection()
        if not selection:
            return
        note_text = self.notes_listbox.get(selection[0])
        title = note_text.split(' ', 1)[1].split(' (')[0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar nota '{title}'?"):
            try:
                from secure_notes import SecureNotesManager
                notes_manager = SecureNotesManager(self.crypto)
                success, msg = notes_manager.delete_note(title)
                if success:
                    self.refresh_notes()
                    self.note_content.config(state=tk.NORMAL)
                    self.note_content.delete("1.0", tk.END)
                    self.note_content.config(state=tk.DISABLED)
                    self.status_bar.config(text=f"✓ Nota '{title}' eliminada")
            except:
                pass

    # =========================================================================
    # PESTAÑAS: ESTADÍSTICAS Y CONFIGURACIÓN (CON ESTEGANOGRAFÍA)
    # =========================================================================
    def setup_stats_tab(self):
        stats_frame = ttk.Frame(self.stats_tab, style='Dark.TFrame')
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.stats_text = scrolledtext.ScrolledText(stats_frame, bg='#16213e', fg='#00ff00', font=('Courier', 10), height=25)
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        self.stats_text.config(state=tk.DISABLED)
        ttk.Button(stats_frame, text="🔄 Actualizar Estadísticas", command=self.refresh_stats).pack(pady=10)
        self.refresh_stats()

    def refresh_stats(self):
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete("1.0", tk.END)
        stats = self.pm.get_stats()
        cat_stats = self.pm.get_category_stats()
        stats_str = f"\n{'═' * 60}\n   📊 ESTADÍSTICAS GENERALES\n{'═' * 60}\n\n[+] Total de contraseñas: {stats['total']}\n[+] Última actualización: {stats['last_update'] or 'N/A'}\n\n{'═' * 60}\n   📁 DISTRIBUCIÓN POR CATEGORÍA\n{'═' * 60}\n"
        for cat, count in sorted(cat_stats.items(), key=lambda x: -x[1]):
            stats_str += f"   {cat}: {count}\n"
        if hasattr(self, 'notification_manager') and self.notification_manager:
            sec_stats = self.notification_manager.get_stats()
            stats_str += f"\n{'═' * 60}\n   🛡️ ESTADÍSTICAS DE SEGURIDAD\n{'═' * 60}\n\n[+] Contraseñas débiles: {sec_stats['weak']}\n[+] Contraseñas antiguas: {sec_stats['old']}\n[+] Contraseñas repetidas: {sec_stats['duplicate']}\n[+] Puntuación seguridad: {sec_stats['security_score']}/100\n"
        self.stats_text.insert("1.0", stats_str)
        self.stats_text.config(state=tk.DISABLED)

    def setup_config_tab(self):
        config_frame = ttk.Frame(self.config_tab, style='Dark.TFrame')
        config_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ⚙️ Sección de Configuración General
        ttk.Label(config_frame, text="⚙️ Configuración del Sistema", font=('Courier', 12, 'bold'), style='Dark.TLabel').pack(pady=(10, 5))
        
        btn_frame_1 = ttk.Frame(config_frame, style='Dark.TFrame')
        btn_frame_1.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame_1, text="💾 Crear Backup", command=self.create_backup).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame_1, text="📤 Exportar CSV", command=self.export_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame_1, text="🔔 Ver Notificaciones", command=self.show_notifications).pack(side=tk.LEFT, padx=5)
        
        # 🖼️ Sección de Esteganografía
        ttk.Label(config_frame, text="🖼️ Esteganografía (Imagen Bóveda)", font=('Courier', 12, 'bold'), style='Dark.TLabel').pack(pady=(20, 5))
        ttk.Label(config_frame, text="Oculta tu base de datos de contraseñas dentro de una imagen inofensiva.", style='Dark.TLabel').pack(pady=2)
        
        btn_frame_2 = ttk.Frame(config_frame, style='Dark.TFrame')
        btn_frame_2.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame_2, text="🔒 Ocultar Base de Datos en Imagen", command=self.gui_hide_vault).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame_2, text="🔓 Restaurar Datos desde Imagen", command=self.gui_restore_vault).pack(side=tk.LEFT, padx=5)
        
        # Volver al terminal
        ttk.Button(config_frame, text="🖥️ Volver al Modo Terminal", command=self.switch_to_terminal).pack(pady=30)

    def gui_hide_vault(self):
        """Ocultar la base de datos desde la GUI"""
        from config import Config
        if not os.path.exists(Config.DATA_FILE):
            messagebox.showerror("Error", "No hay una base de datos activa para ocultar.")
            return
            
        cover_path = filedialog.askopenfilename(title="Seleccionar imagen portadora", 
                                                filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
        if not cover_path:
            return
            
        name_without_ext = os.path.splitext(os.path.basename(cover_path))[0]
        output_name = f"{name_without_ext}_vault.png"
        output_path = os.path.join(os.path.dirname(cover_path), output_name)
        
        try:
            with open(Config.DATA_FILE, 'rb') as f:
                vault_data = f.read()
                
            self.status_bar.config(text="Procesando esteganografía... Por favor, espera.")
            self.root.update()
            
            success, msg = self.stego_manager.hide_data(cover_path, vault_data, output_path)
            
            if success:
                messagebox.showinfo("Éxito", f"Datos ocultos con éxito.\nImagen guardada en:\n{output_path}")
                self.status_bar.config(text="✓ Imagen Bóveda creada exitosamente.")
            else:
                messagebox.showerror("Error", msg)
                self.status_bar.config(text="✗ Error en esteganografía.")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def gui_restore_vault(self):
        """Restaurar la base de datos desde la GUI"""
        from config import Config
        stego_path = filedialog.askopenfilename(title="Seleccionar Imagen Bóveda", 
                                                filetypes=[("Imágenes PNG", "*.png")])
        if not stego_path:
            return
            
        self.status_bar.config(text="Extrayendo datos de la imagen... Por favor, espera.")
        self.root.update()
        
        success, result = self.stego_manager.extract_data(stego_path)
        
        if success:
            if os.path.exists(Config.DATA_FILE):
                if not messagebox.askyesno("Advertencia", "¿Sobrescribir tu base de datos actual con la restaurada?"):
                    self.status_bar.config(text="Operación cancelada.")
                    return
            
            try:
                with open(Config.DATA_FILE, 'wb') as f:
                    f.write(result)
                
                # Recargar los datos en la interfaz
                self.pm.load()
                self.refresh_passwords()
                
                messagebox.showinfo("Éxito", "Base de datos restaurada con éxito.\nLas contraseñas han sido actualizadas.")
                self.status_bar.config(text="✓ Base de datos restaurada.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar la base de datos: {e}")
        else:
            messagebox.showerror("Error", result)
            self.status_bar.config(text="✗ Error al extraer datos.")

    def create_backup(self):
        import shutil
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.enc"
        try:
            shutil.copy2("passwords.enc", backup_name)
            self.status_bar.config(text=f"✓ Backup creado: {backup_name}")
            messagebox.showinfo("Backup", f"Backup creado: {backup_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear backup: {e}")

    def export_csv(self):
        filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            self.pm.export_csv(filename)
            self.status_bar.config(text=f"✓ Exportado a: {filename}")
            messagebox.showinfo("Exportación", f"Datos exportados a: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {e}")

    def show_notifications(self):
        if self.notification_manager:
            alerts = self.notification_manager.get_all_alerts()
            if alerts:
                msg = "\n".join([f"• {a['message']}" for a in alerts])
                messagebox.showwarning("Notificaciones", msg)
            else:
                messagebox.showinfo("Notificaciones", "✅ No hay notificaciones pendientes")
        else:
            messagebox.showinfo("Notificaciones", "Sistema de notificaciones no disponible")

    def switch_to_terminal(self):
        if messagebox.askyesno("Confirmar", "¿Volver al modo terminal? Se cerrará la interfaz gráfica."):
            self.root.quit()
            self.root.destroy()

    def run(self):
        self.root.mainloop()