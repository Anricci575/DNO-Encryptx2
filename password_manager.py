"""
Módulo de gestión de contraseñas - DNO Encryptx
"""

from datetime import datetime
from crypto_manager import CryptoManager
from colors import Colors

class PasswordManager:
    """Gestor de contraseñas"""
    
    def __init__(self, crypto):
        self.crypto = crypto
        self.data = {}
    
    def load(self):
        """Cargar datos desde el almacenamiento"""
        self.data = self.crypto.load_encrypted()
        # 🔧 Migrar datos antiguos al nuevo formato
        self._migrate_old_data()
        return self.data
    
    def _migrate_old_data(self):
        """Migrar datos antiguos al nuevo formato (compatibilidad hacia atrás)"""
        modified = False
        for service, info in self.data.items():
            # Si falta el campo 'updated', agregarlo usando 'created' o fecha actual
            if 'updated' not in info:
                info['updated'] = info.get('created', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                modified = True
            # Si falta el campo 'created', agregarlo con fecha actual
            if 'created' not in info:
                info['created'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                modified = True
            # 🆕 Si falta el campo 'category', agregar categoría por defecto
            if 'category' not in info:
                info['category'] = "📁 Otros"
                modified = True
            # 🆕 Si falta el campo 'tags', agregar lista vacía
            if 'tags' not in info:
                info['tags'] = []
                modified = True
        
        # Si hubo modificaciones, guardar los datos migrados
        if modified:
            self.save()
    
    def save(self):
        """Guardar datos al almacenamiento"""
        self.crypto.save_encrypted(self.data)
    
    def add(self, service, username, password, category=None, tags=None):
        """Agregar o actualizar una contraseña con categoría y etiquetas"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data[service] = {
            'username': username,
            'password': password,
            'category': category or "📁 Otros",
            'tags': tags or [],
            'created': now,
            'updated': now
        }
        self.save()
        return True
    
    def get(self, service):
        """Obtener una contraseña (con compatibilidad)"""
        info = self.data.get(service)
        if info:
            # Asegurar que los campos existan para mostrar
            if 'updated' not in info:
                info['updated'] = info.get('created', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            if 'created' not in info:
                info['created'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if 'category' not in info:
                info['category'] = "📁 Otros"
            if 'tags' not in info:
                info['tags'] = []
        return info
    
    def delete(self, service):
        """Eliminar una contraseña"""
        if service in self.data:
            del self.data[service]
            self.save()
            return True
        return False
    
    def list_all(self):
        """Listar todos los servicios"""
        return list(self.data.keys())
    
    def get_stats(self):
        """Obtener estadísticas (con compatibilidad)"""
        total = len(self.data)
        if total > 0:
            # Obtener la fecha más reciente, priorizando 'updated' si existe
            last_update = None
            for info in self.data.values():
                # Usar 'updated' si existe, si no usar 'created'
                date = info.get('updated', info.get('created'))
                if date and (not last_update or date > last_update):
                    last_update = date
            return {'total': total, 'last_update': last_update}
        return {'total': 0, 'last_update': None}
    
    def search(self, pattern):
        """Buscar servicios por patrón"""
        return [s for s in self.data.keys() if pattern.lower() in s.lower()]
    
    def search_by_tag(self, tag):
        """Buscar servicios por etiqueta"""
        results = []
        for service, info in self.data.items():
            tags = info.get('tags', [])
            if tag.lower() in [t.lower() for t in tags]:
                results.append(service)
        return results
    
    def search_by_category(self, category):
        """Buscar servicios por categoría"""
        return [s for s, info in self.data.items() if info.get('category') == category]
    
    def update_category(self, service, category):
        """Actualizar categoría de un servicio"""
        if service in self.data:
            self.data[service]['category'] = category
            self.data[service]['updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save()
            return True
        return False
    
    def add_tag(self, service, tag):
        """Agregar etiqueta a un servicio"""
        if service in self.data:
            if 'tags' not in self.data[service]:
                self.data[service]['tags'] = []
            if tag not in self.data[service]['tags']:
                self.data[service]['tags'].append(tag)
                self.data[service]['updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save()
                return True
        return False
    
    def remove_tag(self, service, tag):
        """Eliminar etiqueta de un servicio"""
        if service in self.data and 'tags' in self.data[service]:
            if tag in self.data[service]['tags']:
                self.data[service]['tags'].remove(tag)
                self.data[service]['updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save()
                return True
        return False
    
    def get_tags(self, service):
        """Obtener etiquetas de un servicio"""
        if service in self.data:
            return self.data[service].get('tags', [])
        return []
    
    def get_all_tags(self):
        """Obtener todas las etiquetas únicas de todos los servicios"""
        all_tags = set()
        for info in self.data.values():
            tags = info.get('tags', [])
            all_tags.update(tags)
        return sorted(all_tags)
    
    def get_services_by_category(self, category):
        """Obtener servicios por categoría"""
        return [s for s, info in self.data.items() if info.get('category') == category]
    
    def get_category_stats(self):
        """Obtener estadísticas por categoría"""
        stats = {}
        for info in self.data.values():
            cat = info.get('category', '📁 Otros')
            stats[cat] = stats.get(cat, 0) + 1
        return stats
    
    def export_csv(self, filename):
        """Exportar a CSV (sin contraseñas por seguridad)"""
        import csv
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Service', 'Username', 'Category', 'Tags', 'Created', 'Updated'])
            for service, info in self.data.items():
                tags_str = ", ".join(info.get('tags', []))
                writer.writerow([
                    service, 
                    info.get('username', 'N/A'),
                    info.get('category', '📁 Otros'),
                    tags_str,
                    info.get('created', 'N/A'),
                    info.get('updated', info.get('created', 'N/A'))
                ])
        return True