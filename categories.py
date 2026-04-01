"""
Módulo de categorías y etiquetas - DNO Encryptx
Organización de contraseñas por categorías y tags
"""

import json
import os
from datetime import datetime

class CategoryManager:
    """Gestor de categorías y etiquetas"""
    
    # Categorías predefinidas
    DEFAULT_CATEGORIES = [
        "📧 Email",
        "🔐 Redes Sociales",
        "🏦 Bancos y Finanzas",
        "🛒 Compras Online",
        "💼 Trabajo",
        "🎮 Gaming",
        "📱 Apps y Servicios",
        "🌐 Sitios Web",
        "🔧 Desarrollo",
        "📁 Otros"
    ]
    
    def __init__(self, data_manager=None):
        self.data_manager = data_manager
        self.categories_file = "categories.json"
        self.categories = self._load_categories()
    
    def _load_categories(self):
        """Cargar categorías desde archivo"""
        if os.path.exists(self.categories_file):
            try:
                with open(self.categories_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return self.DEFAULT_CATEGORIES.copy()
    
    def _save_categories(self):
        """Guardar categorías en archivo"""
        try:
            with open(self.categories_file, 'w', encoding='utf-8') as f:
                json.dump(self.categories, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def add_category(self, category_name):
        """Agregar nueva categoría"""
        if category_name not in self.categories:
            self.categories.append(category_name)
            self._save_categories()
            return True
        return False
    
    def remove_category(self, category_name):
        """Eliminar categoría"""
        if category_name in self.categories and category_name not in self.DEFAULT_CATEGORIES:
            self.categories.remove(category_name)
            self._save_categories()
            return True
        return False
    
    def get_categories(self):
        """Obtener lista de categorías"""
        return self.categories
    
    def get_category_icon(self, category_name):
        """Obtener icono de categoría"""
        icons = {
            "📧 Email": "📧",
            "🔐 Redes Sociales": "🔐",
            "🏦 Bancos y Finanzas": "🏦",
            "🛒 Compras Online": "🛒",
            "💼 Trabajo": "💼",
            "🎮 Gaming": "🎮",
            "📱 Apps y Servicios": "📱",
            "🌐 Sitios Web": "🌐",
            "🔧 Desarrollo": "🔧",
            "📁 Otros": "📁"
        }
        return icons.get(category_name, "📁")


class TagManager:
    """Gestor de etiquetas/tags"""
    
    def __init__(self, data_manager=None):
        self.data_manager = data_manager
        self.tags_file = "tags.json"
        self.tags = self._load_tags()
    
    def _load_tags(self):
        """Cargar etiquetas desde archivo"""
        if os.path.exists(self.tags_file):
            try:
                with open(self.tags_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_tags(self):
        """Guardar etiquetas en archivo"""
        try:
            with open(self.tags_file, 'w', encoding='utf-8') as f:
                json.dump(self.tags, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def add_tag_to_service(self, service, tag):
        """Agregar etiqueta a un servicio"""
        if service not in self.tags:
            self.tags[service] = []
        if tag not in self.tags[service]:
            self.tags[service].append(tag)
            self._save_tags()
            return True
        return False
    
    def remove_tag_from_service(self, service, tag):
        """Eliminar etiqueta de un servicio"""
        if service in self.tags and tag in self.tags[service]:
            self.tags[service].remove(tag)
            if not self.tags[service]:
                del self.tags[service]
            self._save_tags()
            return True
        return False
    
    def get_service_tags(self, service):
        """Obtener etiquetas de un servicio"""
        return self.tags.get(service, [])
    
    def get_services_by_tag(self, tag):
        """Obtener servicios por etiqueta"""
        return [s for s, tags in self.tags.items() if tag in tags]
    
    def get_all_tags(self):
        """Obtener todas las etiquetas únicas"""
        all_tags = set()
        for tags in self.tags.values():
            all_tags.update(tags)
        return sorted(all_tags)