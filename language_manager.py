"""
Módulo de gestión de idiomas - DNO Encryptx
Soporte para Español e Inglés
"""

import json
import os
from colors import Colors

class LanguageManager:
    """Gestor de traducciones y lenguaje"""
    
    # Idiomas disponibles
    LANGUAGES = {
        'es': 'Español',
        'en': 'English'
    }
    
    def __init__(self, language='es'):
        self.current_language = language
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Cargar traducciones del archivo JSON"""
        locales_dir = os.path.join(os.path.dirname(__file__), 'locales')
        lang_file = os.path.join(locales_dir, f'{self.current_language}.json')
        
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            # Si no existe, crear archivo por defecto
            self.create_default_locale(lang_file)
            with open(lang_file, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
    
    def create_default_locale(self, filepath):
        """Crear archivo de traducción por defecto si no existe"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        if 'es' in filepath:
            default_translations = self.get_es_translations()
        else:
            default_translations = self.get_en_translations()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(default_translations, f, indent=2, ensure_ascii=False)
    
    def get(self, key, **kwargs):
        """Obtener traducción por clave"""
        text = self.translations.get(key, key)
        if kwargs:
            text = text.format(**kwargs)
        return text
    
    def switch_language(self, language):
        """Cambiar idioma"""
        if language in self.LANGUAGES:
            self.current_language = language
            self.load_translations()
            return True
        return False
    
    def get_current_language(self):
        """Obtener idioma actual"""
        return self.LANGUAGES[self.current_language]
    
    def get_available_languages(self):
        """Obtener idiomas disponibles"""
        return self.LANGUAGES
    
    def get_es_translations(self):
        """Traducciones al español"""
        return {
            # Sistema
            "app_name": "DNO-ENCRYPTX v2.0 - HACKER EDITION",
            "app_desc": "Sistema Gestor de Contraseñas Encriptado",
            "access_granted": "[ACCESO CONCEDIDO] - ALMACENAMIENTO SEGURO",
            
            # Setup inicial
            "first_time_setup": "🔐 CONFIGURACIÓN INICIAL - CONTRASEÑA MAESTRA",
            "create_master_password": "CREAR CONTRASEÑA MAESTRA",
            "confirm_master_password": "CONFIRMAR CONTRASEÑA MAESTRA",
            "password_min_length": "¡LA CONTRASEÑA DEBE TENER AL MENOS {length} CARACTERES!",
            "passwords_do_not_match": "¡LAS CONTRASEÑAS NO COINCIDEN!",
            "generating_key": "GENERANDO CLAVE DE ENCRIPTACIÓN SEGURA",
            "database_created": "✓ BASE DE DATOS CREADA EXITOSAMENTE",
            "warning_password_loss": "⚠ ADVERTENCIA: LA PÉRDIDA DE LA CONTRASEÑA MAESTRA = PÉRDIDA PERMANENTE DE DATOS",
            
            # Login
            "secure_access": "🔑 ACCESO SEGURO - AUTENTICACIÓN",
            "no_profile": "¡NO SE ENCONTRÓ PERFIL DE SEGURIDAD!",
            "master_password": "CONTRASEÑA MAESTRA",
            "attempts_left": "{attempts} INTENTOS RESTANTES",
            "access_denied": "¡ACCESO DENEGADO!",
            "access_granted_welcome": "✓ ACCESO CONCEDIDO - BIENVENIDO",
            "system_locked": "¡ACCESO DENEGADO - SISTEMA BLOQUEADO!",
            "decrypting_db": "DESENCRIPTANDO BASE DE DATOS",
            "corrupted_db": "BASE DE DATOS CORRUMPIDA: {error}",
            
            # Menú principal
            "main_operations": "⚡ MENÚ DE OPERACIONES PRINCIPAL",
            "add_credential": "🔐 AGREGAR NUEVA CREDENCIAL",
            "retrieve_credential": "👁️ RECUPERAR CREDENCIAL",
            "list_services": "📋 LISTAR TODOS LOS SERVICIOS",
            "delete_credential": "🗑️ ELIMINAR CREDENCIAL",
            "create_backup": "💾 CREAR RESPALDO",
            "statistics": "📊 ESTADÍSTICAS",
            "search": "🔍 BUSCAR",
            "exit_system": "🚪 SALIR DEL SISTEMA",
            "matrix_mode": "🎨 MODO MATRIX",
            "language": "🌐 CAMBIAR IDIOMA",
            
            # Operaciones
            "add_new": "🔐 AGREGAR NUEVA CREDENCIAL",
            "service_name": "NOMBRE DEL SERVICIO",
            "username_email": "USUARIO/EMAIL",
            "password": "CONTRASEÑA",
            "invalid_service": "¡NOMBRE DE SERVICIO INVÁLIDO!",
            "service_exists": "¡EL SERVICIO '{service}' YA EXISTE!",
            "overwrite": "¿SOBREESCRIBIR? (s/n)",
            "credentials_stored": "✓ CREDENCIALES GUARDADAS - {service}",
            "encrypting_storing": "ENCRIPTANDO Y ALMACENANDO",
            
            # Recuperar credencial
            "retrieve": "👁️ RECUPERAR CREDENCIAL",
            "no_credentials": "¡NO HAY CREDENCIALES GUARDADAS!",
            "active_credentials": "CREDENCIALES ACTIVAS [{total} ENTRADAS]",
            "service_not_found": "¡SERVICIO '{service}' NO ENCONTRADO!",
            "username_label": "USUARIO",
            "password_label": "CONTRASEÑA",
            "created_label": "CREADO",
            "updated_label": "ACTUALIZADO",
            "copy_to_clipboard": "¿COPIAR AL PORTAPAPELES? (s/n)",
            "copied": "✓ CONTRASEÑA COPIADA AL PORTAPAPELES",
            
            # Listar servicios
            "list": "📋 LISTAR TODOS LOS SERVICIOS",
            
            # Eliminar
            "delete": "🗑️ ELIMINAR CREDENCIAL",
            "service_to_delete": "SERVICIO A ELIMINAR",
            "permanent_delete": "⚠ ELIMINAR PERMANENTEMENTE '{service}'? (s/n)",
            "service_deleted": "✓ SERVICIO '{service}' ELIMINADO",
            
            # Backup
            "backup": "💾 CREAR RESPALDO",
            "backup_created": "✓ RESPALDO CREADO: {filename}",
            "backup_failed": "¡ERROR AL CREAR RESPALDO!",
            
            # Estadísticas
            "stats": "📊 ESTADÍSTICAS",
            "total_credentials": "TOTAL DE CREDENCIALES",
            "last_update": "ÚLTIMA ACTUALIZACIÓN",
            
            # Búsqueda
            "search_services": "🔍 BUSCAR SERVICIOS",
            "search_pattern": "PATRÓN DE BÚSQUEDA",
            "found_matches": "✓ ENCONTRADAS {total} COINCIDENCIA(S):",
            "no_matches": "¡NO SE ENCONTRARON COINCIDENCIAS!",
            
            # Errores y mensajes
            "invalid_command": "¡COMANDO INVÁLIDO!",
            "press_enter": "Presiona ENTER para continuar...",
            "system_shutdown": "✓ APAGANDO SISTEMA - CREDENCIALES ASEGURADAS",
            "goodbye": "👋 HACK THE PLANET! - MANTENTE SEGURO",
            "emergency_shutdown": "⚠ APAGADO DE EMERGENCIA - BASE DE DATOS ASEGURADA",
            "critical_error": "⚠ ERROR CRÍTICO: {error}",
            
            # Modo matrix
            "matrix_activated": "✓ MODO MATRIX ACTIVADO",
            "feature_soon": "¡FUNCIONALIDAD PRÓXIMAMENTE!",
            
            # Cambio de idioma
            "language_switch": "🌐 CAMBIAR IDIOMA",
            "select_language": "SELECCIONA IDIOMA (1: Español, 2: English)",
            "language_changed": "✓ IDIOMA CAMBIADO A {language}",
            "invalid_language": "¡IDIOMA INVÁLIDO!",
            
            # Preguntas
            "question_yes_no": "(s/n)",
            "question_yes": "s",
            "question_no": "n",
            "question_overwrite": "¿SOBREESCRIBIR?",
            "question_copy": "¿COPIAR AL PORTAPAPELES?",
            "question_delete": "¿ELIMINAR PERMANENTEMENTE?",
            "question_continue": "¿CONTINUAR?",
            
            # Prompts
            "prompt_service": "SERVICIO",
            "prompt_username": "USUARIO/EMAIL",
            "prompt_password": "CONTRASEÑA",
            "prompt_search": "PATRÓN DE BÚSQUEDA",
            "prompt_language": "IDIOMA (es/en)",
            
            # Estado
            "status_success": "✓ ÉXITO",
            "status_error": "✗ ERROR",
            "status_warning": "⚠ ADVERTENCIA",
            "status_info": "ℹ INFO"
        }
    
    def get_en_translations(self):
        """English translations"""
        return {
            # System
            "app_name": "DNO-ENCRYPTX v2.0 - HACKER EDITION",
            "app_desc": "Encrypted Password Manager System",
            "access_granted": "[ACCESS GRANTED] - SECURE STORAGE",
            
            # Setup inicial
            "first_time_setup": "🔐 FIRST TIME SETUP - MASTER PASSWORD",
            "create_master_password": "CREATE MASTER PASSWORD",
            "confirm_master_password": "CONFIRM MASTER PASSWORD",
            "password_min_length": "PASSWORD MUST BE AT LEAST {length} CHARACTERS!",
            "passwords_do_not_match": "PASSWORDS DO NOT MATCH!",
            "generating_key": "GENERATING SECURE ENCRYPTION KEY",
            "database_created": "✓ DATABASE CREATED SUCCESSFULLY",
            "warning_password_loss": "⚠ WARNING: LOSS OF MASTER PASSWORD = PERMANENT DATA LOSS",
            
            # Login
            "secure_access": "🔑 SECURE ACCESS - AUTHENTICATION",
            "no_profile": "NO SECURITY PROFILE FOUND!",
            "master_password": "MASTER PASSWORD",
            "attempts_left": "{attempts} ATTEMPTS LEFT",
            "access_denied": "ACCESS DENIED!",
            "access_granted_welcome": "✓ ACCESS GRANTED - WELCOME BACK",
            "system_locked": "ACCESS DENIED - SYSTEM LOCKED!",
            "decrypting_db": "DECRYPTING DATABASE",
            "corrupted_db": "CORRUPTED DATABASE: {error}",
            
            # Menú principal
            "main_operations": "⚡ MAIN OPERATIONS MENU",
            "add_credential": "🔐 ADD NEW CREDENTIAL",
            "retrieve_credential": "👁️ RETRIEVE CREDENTIAL",
            "list_services": "📋 LIST ALL SERVICES",
            "delete_credential": "🗑️ DELETE CREDENTIAL",
            "create_backup": "💾 CREATE BACKUP",
            "statistics": "📊 STATISTICS",
            "search": "🔍 SEARCH",
            "exit_system": "🚪 EXIT SYSTEM",
            "matrix_mode": "🎨 MATRIX MODE",
            "language": "🌐 CHANGE LANGUAGE",
            
            # Operaciones
            "add_new": "🔐 ADD NEW CREDENTIAL",
            "service_name": "SERVICE NAME",
            "username_email": "USERNAME/EMAIL",
            "password": "PASSWORD",
            "invalid_service": "INVALID SERVICE NAME!",
            "service_exists": "SERVICE '{service}' ALREADY EXISTS!",
            "overwrite": "OVERWRITE? (y/n)",
            "credentials_stored": "✓ CREDENTIALS STORED - {service}",
            "encrypting_storing": "ENCRYPTING AND STORING",
            
            # Recuperar credencial
            "retrieve": "👁️ RETRIEVE CREDENTIAL",
            "no_credentials": "NO CREDENTIALS FOUND!",
            "active_credentials": "ACTIVE CREDENTIALS [{total} ENTRIES]",
            "service_not_found": "SERVICE '{service}' NOT FOUND!",
            "username_label": "USERNAME",
            "password_label": "PASSWORD",
            "created_label": "CREATED",
            "updated_label": "UPDATED",
            "copy_to_clipboard": "COPY TO CLIPBOARD? (y/n)",
            "copied": "✓ PASSWORD COPIED TO CLIPBOARD",
            
            # Listar servicios
            "list": "📋 LIST ALL SERVICES",
            
            # Eliminar
            "delete": "🗑️ DELETE CREDENTIAL",
            "service_to_delete": "SERVICE TO DELETE",
            "permanent_delete": "⚠ PERMANENT DELETE '{service}'? (y/n)",
            "service_deleted": "✓ SERVICE '{service}' DELETED",
            
            # Backup
            "backup": "💾 CREATE BACKUP",
            "backup_created": "✓ BACKUP CREATED: {filename}",
            "backup_failed": "BACKUP FAILED!",
            
            # Estadísticas
            "stats": "📊 STATISTICS",
            "total_credentials": "TOTAL CREDENTIALS",
            "last_update": "LAST UPDATE",
            
            # Búsqueda
            "search_services": "🔍 SEARCH SERVICES",
            "search_pattern": "SEARCH PATTERN",
            "found_matches": "✓ FOUND {total} MATCH(ES):",
            "no_matches": "NO MATCHES FOUND!",
            
            # Errores y mensajes
            "invalid_command": "INVALID COMMAND!",
            "press_enter": "Press ENTER to continue...",
            "system_shutdown": "✓ SYSTEM SHUTDOWN - CREDENTIALS SECURED",
            "goodbye": "👋 HACK THE PLANET! - STAY SECURE",
            "emergency_shutdown": "⚠ EMERGENCY SHUTDOWN - DATABASE SECURED",
            "critical_error": "⚠ CRITICAL ERROR: {error}",
            
            # Modo matrix
            "matrix_activated": "✓ MATRIX MODE ACTIVATED",
            "feature_soon": "FEATURE COMING SOON!",
            
            # Cambio de idioma
            "language_switch": "🌐 CHANGE LANGUAGE",
            "select_language": "SELECT LANGUAGE (1: Spanish, 2: English)",
            "language_changed": "✓ LANGUAGE CHANGED TO {language}",
            "invalid_language": "INVALID LANGUAGE!",
            
            # Preguntas
            "question_yes_no": "(y/n)",
            "question_yes": "y",
            "question_no": "n",
            "question_overwrite": "OVERWRITE?",
            "question_copy": "COPY TO CLIPBOARD?",
            "question_delete": "PERMANENT DELETE?",
            "question_continue": "CONTINUE?",
            
            # Prompts
            "prompt_service": "SERVICE",
            "prompt_username": "USERNAME/EMAIL",
            "prompt_password": "PASSWORD",
            "prompt_search": "SEARCH PATTERN",
            "prompt_language": "LANGUAGE (es/en)",
            
            # Estado
            "status_success": "✓ SUCCESS",
            "status_error": "✗ ERROR",
            "status_warning": "⚠ WARNING",
            "status_info": "ℹ INFO"
        }