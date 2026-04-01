"""
Módulo de notificaciones - DNO Encryptx
Sistema de alertas y recordatorios con detalles de servicios
"""

from datetime import datetime, timedelta
import os
import json

class NotificationManager:
    """Gestor de notificaciones y alertas"""
    
    def __init__(self, password_manager):
        self.pm = password_manager
        self.notifications_file = "notifications.json"
        self.notifications = self._load_notifications()
    
    def _load_notifications(self):
        """Cargar notificaciones guardadas"""
        if os.path.exists(self.notifications_file):
            try:
                with open(self.notifications_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {'seen': [], 'dismissed': []}
    
    def _save_notifications(self):
        """Guardar notificaciones"""
        try:
            with open(self.notifications_file, 'w', encoding='utf-8') as f:
                json.dump(self.notifications, f, indent=2)
            return True
        except:
            return False
    
    def check_old_passwords(self, days_threshold=90):
        """Verificar contraseñas que no se han actualizado en X días"""
        alerts = []
        now = datetime.now()
        
        for service, info in self.pm.data.items():
            updated_str = info.get('updated', info.get('created'))
            if updated_str:
                try:
                    updated = datetime.strptime(updated_str, "%Y-%m-%d %H:%M:%S")
                    days_old = (now - updated).days
                    
                    if days_old >= days_threshold:
                        alerts.append({
                            'type': 'old_password',
                            'service': service,
                            'days': days_old,
                            'username': info.get('username', 'N/A'),
                            'message': f"📅 '{service}' - {days_old} días sin actualizar",
                            'priority': 'high' if days_old >= 180 else 'medium'
                        })
                except:
                    pass
        return alerts
    
    def check_weak_passwords(self):
        """Verificar contraseñas débiles con detalles de fortaleza"""
        from password_generator import PasswordGenerator
        
        alerts = []
        for service, info in self.pm.data.items():
            password = info.get('password', '')
            if password:
                strength = PasswordGenerator.check_strength(password)
                if strength['score'] <= 2:  # Débil o muy débil
                    # Icono según fortaleza
                    if strength['score'] <= 1:
                        icon = "🔴"
                        level = "MUY DÉBIL"
                    else:
                        icon = "🟡"
                        level = "DÉBIL"
                    
                    alerts.append({
                        'type': 'weak_password',
                        'service': service,
                        'username': info.get('username', 'N/A'),
                        'score': strength['score'],
                        'strength': strength['strength'],
                        'level': level,
                        'icon': icon,
                        'message': f"{icon} '{service}' - Contraseña {level} (puntuación: {strength['score']}/5)",
                        'priority': 'high' if strength['score'] <= 1 else 'medium'
                    })
        return alerts
    
    def check_duplicate_passwords(self):
        """Verificar contraseñas repetidas con lista de servicios"""
        password_map = {}
        alerts = []
        
        for service, info in self.pm.data.items():
            password = info.get('password', '')
            if password:
                if password not in password_map:
                    password_map[password] = []
                password_map[password].append({
                    'service': service,
                    'username': info.get('username', 'N/A')
                })
        
        for password, services in password_map.items():
            if len(services) > 1:
                # Lista de servicios afectados
                service_list = []
                for s in services:
                    service_list.append(f"{s['service']} ({s['username']})")
                
                alerts.append({
                    'type': 'duplicate_password',
                    'services': services,
                    'service_names': [s['service'] for s in services],
                    'password': password[:4] + '***',
                    'count': len(services),
                    'message': f"🔄 Contraseña repetida en {len(services)} servicios: {', '.join(service_list[:3])}" + ("..." if len(services) > 3 else ""),
                    'priority': 'high'
                })
        return alerts
    
    def check_backup_needed(self, days_threshold=30):
        """Verificar si se necesita hacer backup"""
        backup_files = [f for f in os.listdir('.') if f.startswith('backup_') and f.endswith('.enc')]
        
        if backup_files:
            latest_backup = max(backup_files, key=os.path.getctime)
            backup_time = datetime.fromtimestamp(os.path.getctime(latest_backup))
            days_since_backup = (datetime.now() - backup_time).days
            
            if days_since_backup >= days_threshold:
                return [{
                    'type': 'backup_needed',
                    'days': days_since_backup,
                    'message': f"💾 Último backup hace {days_since_backup} días. ¡Haz un backup nuevo!",
                    'priority': 'medium'
                }]
        else:
            return [{
                'type': 'backup_needed',
                'message': "💾 Nunca has hecho un backup. ¡Es importante hacer backups regulares!",
                'priority': 'high'
            }]
        return []
    
    def get_all_alerts(self):
        """Obtener todas las alertas con detalles"""
        all_alerts = []
        all_alerts.extend(self.check_old_passwords())
        all_alerts.extend(self.check_weak_passwords())
        all_alerts.extend(self.check_duplicate_passwords())
        all_alerts.extend(self.check_backup_needed())
        
        # Filtrar notificaciones ya vistas/descartadas
        seen_ids = self.notifications.get('seen', [])
        dismissed_ids = self.notifications.get('dismissed', [])
        
        new_alerts = []
        for alert in all_alerts:
            alert_id = f"{alert['type']}_{alert.get('service', 'global')}"
            if alert_id not in seen_ids and alert_id not in dismissed_ids:
                new_alerts.append(alert)
        
        return new_alerts
    
    def mark_seen(self, alert_id):
        """Marcar notificación como vista"""
        if 'seen' not in self.notifications:
            self.notifications['seen'] = []
        if alert_id not in self.notifications['seen']:
            self.notifications['seen'].append(alert_id)
            self._save_notifications()
    
    def dismiss(self, alert_id):
        """Descartar notificación permanentemente"""
        if 'dismissed' not in self.notifications:
            self.notifications['dismissed'] = []
        if alert_id not in self.notifications['dismissed']:
            self.notifications['dismissed'].append(alert_id)
            self._save_notifications()
    
    def show_notifications(self, ui, colors):
        """Mostrar notificaciones en pantalla con detalles"""
        alerts = self.get_all_alerts()
        
        if not alerts:
            print(f"\n{colors.GREEN}{'═' * 70}{colors.RESET}")
            print(f"{colors.BOLD}{colors.CYAN}   ✅ TODO EN ORDEN{colors.RESET}")
            print(f"{colors.GREEN}{'═' * 70}{colors.RESET}")
            print(f"\n{colors.GREEN}🎉 ¡No hay notificaciones pendientes! Todas tus contraseñas están seguras.{colors.RESET}")
            return False
        
        print(f"\n{colors.YELLOW}{'═' * 70}{colors.RESET}")
        print(f"{colors.BOLD}{colors.CYAN}   🔔 NOTIFICACIONES DE SEGURIDAD ({len(alerts)} alertas){colors.RESET}")
        print(f"{colors.YELLOW}{'═' * 70}{colors.RESET}")
        
        for i, alert in enumerate(alerts, 1):
            # Color según prioridad
            if alert['priority'] == 'high':
                color = colors.RED
                border = colors.RED
            elif alert['priority'] == 'medium':
                color = colors.YELLOW
                border = colors.YELLOW
            else:
                color = colors.CYAN
                border = colors.CYAN
            
            alert_id = f"{alert['type']}_{alert.get('service', 'global')}"
            
            # Mostrar notificación con formato mejorado
            print(f"\n{border}{'─' * 70}{colors.RESET}")
            print(f"{color}{alert['message']}{colors.RESET}")
            
            # Mostrar detalles adicionales según tipo
            if alert['type'] == 'weak_password':
                print(f"   {colors.DIM}👤 Usuario: {alert.get('username', 'N/A')}{colors.RESET}")
                print(f"   {colors.DIM}📊 Nivel: {alert.get('level', 'Desconocido')} (puntuación: {alert.get('score', 0)}/5){colors.RESET}")
                print(f"   {colors.YELLOW}💡 Recomendación: Usa mayúsculas, números y símbolos{colors.RESET}")
            
            elif alert['type'] == 'old_password':
                print(f"   {colors.DIM}👤 Usuario: {alert.get('username', 'N/A')}{colors.RESET}")
                print(f"   {colors.DIM}📅 Días sin actualizar: {alert.get('days', 0)}{colors.RESET}")
                print(f"   {colors.YELLOW}💡 Recomendación: Cambia la contraseña regularmente{colors.RESET}")
            
            elif alert['type'] == 'duplicate_password':
                print(f"   {colors.DIM}🔄 Servicios afectados:{colors.RESET}")
                for s in alert.get('services', []):
                    print(f"      {colors.YELLOW}•{colors.RESET} {s['service']} ({s['username']})")
                print(f"   {colors.YELLOW}💡 Recomendación: Usa contraseñas únicas para cada servicio{colors.RESET}")
            
            elif alert['type'] == 'backup_needed':
                if 'days' in alert:
                    print(f"   {colors.DIM}📅 Días sin backup: {alert.get('days', 0)}{colors.RESET}")
                print(f"   {colors.YELLOW}💡 Recomendación: Ejecuta la opción 5 del menú principal{colors.RESET}")
            
            # Opciones para la notificación
            print(f"\n   {colors.GREEN}[V]{colors.RESET} Marcar como vista  {colors.RED}[D]{colors.RESET} Descartar  {colors.CYAN}[S]{colors.RESET} Saltar")
            action = input(f"   {colors.CYAN}Acción (V/D/S): {colors.RESET}").strip().lower()
            
            if action == 'v':
                self.mark_seen(alert_id)
                print(f"   {colors.GREEN}✓ Notificación marcada como vista{colors.RESET}")
            elif action == 'd':
                self.dismiss(alert_id)
                print(f"   {colors.GREEN}✓ Notificación descartada{colors.RESET}")
            elif action == 's':
                print(f"   {colors.CYAN}→ Notificación saltada{colors.RESET}")
        
        print(f"\n{colors.YELLOW}{'═' * 70}{colors.RESET}")
        return True
    
    def get_stats(self):
        """Obtener estadísticas de seguridad con detalles"""
        total = len(self.pm.data)
        weak_passwords = self.check_weak_passwords()
        old_passwords = self.check_old_passwords()
        duplicate_passwords = self.check_duplicate_passwords()
        
        # Detalles de contraseñas débiles
        weak_details = []
        for w in weak_passwords:
            weak_details.append({
                'service': w['service'],
                'username': w.get('username', 'N/A'),
                'level': w.get('level', 'Débil'),
                'score': w.get('score', 0)
            })
        
        # Detalles de contraseñas antiguas
        old_details = []
        for o in old_passwords:
            old_details.append({
                'service': o['service'],
                'username': o.get('username', 'N/A'),
                'days': o.get('days', 0)
            })
        
        return {
            'total': total,
            'weak': len(weak_passwords),
            'old': len(old_passwords),
            'duplicate': len(duplicate_passwords),
            'weak_details': weak_details,
            'old_details': old_details,
            'security_score': self._calculate_security_score(total, len(weak_passwords), len(old_passwords), len(duplicate_passwords))
        }
    
    def _calculate_security_score(self, total, weak, old, duplicate):
        """Calcular puntuación de seguridad (0-100)"""
        if total == 0:
            return 100
        
        score = 100
        score -= (weak / total) * 30 if weak > 0 else 0
        score -= (old / total) * 20 if old > 0 else 0
        score -= (duplicate / total) * 25 if duplicate > 0 else 0
        
        return max(0, min(100, int(score)))