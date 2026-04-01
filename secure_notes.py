"""
Módulo de Notas Seguras - DNO Encryptx
Sistema para guardar notas, tarjetas y documentos encriptados
"""

import json
import os
from datetime import datetime
from colors import Colors

class SecureNote:
    """Clase para una nota segura individual"""
    
    def __init__(self, title, content, note_type="text", tags=None, color="white"):
        self.title = title
        self.content = content
        self.note_type = note_type  # text, credit_card, document, code, password
        self.tags = tags or []
        self.color = color
        self.created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created
    
    def to_dict(self):
        """Convertir nota a diccionario"""
        return {
            'title': self.title,
            'content': self.content,
            'note_type': self.note_type,
            'tags': self.tags,
            'color': self.color,
            'created': self.created,
            'updated': self.updated
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crear nota desde diccionario"""
        note = cls(
            data['title'],
            data['content'],
            data.get('note_type', 'text'),
            data.get('tags', []),
            data.get('color', 'white')
        )
        note.created = data.get('created', note.created)
        note.updated = data.get('updated', note.updated)
        return note


class SecureNotesManager:
    """Gestor de notas seguras"""
    
    NOTE_TYPES = {
        'text': {'icon': '📝', 'name': 'Texto', 'color': 'white'},
        'credit_card': {'icon': '💳', 'name': 'Tarjeta', 'color': 'cyan'},
        'document': {'icon': '📄', 'name': 'Documento', 'color': 'blue'},
        'code': {'icon': '🔑', 'name': 'Código', 'color': 'yellow'},
        'password': {'icon': '🔐', 'name': 'Contraseña', 'color': 'green'},
        'backup': {'icon': '💾', 'name': 'Backup', 'color': 'magenta'}
    }
    
    def __init__(self, crypto_manager):
        self.crypto = crypto_manager
        self.notes_file = "secure_notes.enc"
        self.notes = {}
        self._load_notes()
    
    def _load_notes(self):
        """Cargar notas desde archivo encriptado"""
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, 'rb') as f:
                    encrypted_data = f.read()
                decrypted = self.crypto.decrypt_data(encrypted_data)
                data = json.loads(decrypted)
                for key, note_data in data.items():
                    self.notes[key] = SecureNote.from_dict(note_data)
            except Exception as e:
                print(f"Error cargando notas: {e}")
    
    def _save_notes(self):
        """Guardar notas en archivo encriptado"""
        try:
            data = {}
            for key, note in self.notes.items():
                data[key] = note.to_dict()
            json_data = json.dumps(data, indent=2, ensure_ascii=False)
            encrypted = self.crypto.encrypt_data(json_data)
            with open(self.notes_file, 'wb') as f:
                f.write(encrypted)
            return True
        except Exception as e:
            print(f"Error guardando notas: {e}")
            return False
    
    def add_note(self, title, content, note_type="text", tags=None):
        """Agregar una nueva nota segura"""
        if not title:
            return False, "El título no puede estar vacío"
        
        if title in self.notes:
            return False, "Ya existe una nota con ese título"
        
        note = SecureNote(title, content, note_type, tags)
        self.notes[title] = note
        self._save_notes()
        return True, "Nota guardada exitosamente"
    
    def get_note(self, title):
        """Obtener una nota por título"""
        return self.notes.get(title)
    
    def update_note(self, title, content, note_type=None, tags=None):
        """Actualizar una nota existente"""
        if title not in self.notes:
            return False, "Nota no encontrada"
        
        note = self.notes[title]
        note.content = content
        if note_type:
            note.note_type = note_type
        if tags is not None:
            note.tags = tags
        note.updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_notes()
        return True, "Nota actualizada"
    
    def delete_note(self, title):
        """Eliminar una nota"""
        if title not in self.notes:
            return False, "Nota no encontrada"
        
        del self.notes[title]
        self._save_notes()
        return True, "Nota eliminada"
    
    def list_notes(self, note_type=None):
        """Listar todas las notas (opcionalmente filtradas por tipo)"""
        notes_list = []
        for title, note in self.notes.items():
            if note_type and note.note_type != note_type:
                continue
            notes_list.append({
                'title': title,
                'type': note.note_type,
                'icon': self.NOTE_TYPES.get(note.note_type, {'icon': '📝'})['icon'],
                'created': note.created,
                'updated': note.updated,
                'tags': note.tags
            })
        return sorted(notes_list, key=lambda x: x['updated'], reverse=True)
    
    def search_notes(self, query):
        """Buscar notas por título o contenido"""
        results = []
        query_lower = query.lower()
        for title, note in self.notes.items():
            if (query_lower in title.lower() or 
                query_lower in note.content.lower() or
                any(query_lower in tag.lower() for tag in note.tags)):
                results.append({
                    'title': title,
                    'type': note.note_type,
                    'icon': self.NOTE_TYPES.get(note.note_type, {'icon': '📝'})['icon'],
                    'preview': note.content[:50] + "..." if len(note.content) > 50 else note.content
                })
        return results
    
    def get_stats(self):
        """Obtener estadísticas de notas"""
        stats = {'total': len(self.notes), 'by_type': {}}
        for note in self.notes.values():
            note_type = note.note_type
            stats['by_type'][note_type] = stats['by_type'].get(note_type, 0) + 1
        return stats
    
    def export_note(self, title, filename=None):
        """Exportar nota a archivo de texto"""
        note = self.notes.get(title)
        if not note:
            return False, "Nota no encontrada"
        
        if not filename:
            filename = f"nota_{title.replace(' ', '_')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Título: {note.title}\n")
            f.write(f"Tipo: {note.note_type}\n")
            f.write(f"Creado: {note.created}\n")
            f.write(f"Actualizado: {note.updated}\n")
            f.write(f"Etiquetas: {', '.join(note.tags) if note.tags else 'Ninguna'}\n")
            f.write(f"{'='*50}\n")
            f.write(note.content)
        
        return True, f"Nota exportada a {filename}"