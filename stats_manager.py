"""
Módulo de estadísticas y análisis de seguridad - DNO Encryptx
"""

from datetime import datetime
from password_generator import PasswordGenerator
from colors import Colors

class StatsManager:
    """Gestor de estadísticas y análisis de seguridad"""
    
    def __init__(self, password_manager):
        self.pm = password_manager
        self.notification_manager = None  # Se puede asignar después
    
    def set_notification_manager(self, notification_manager):
        """Asignar el gestor de notificaciones"""
        self.notification_manager = notification_manager
    
    def get_basic_stats(self):
        """Obtener estadísticas básicas"""
        total = len(self.pm.data)
        if total == 0:
            return {'total': 0, 'last_update': None}
        
        # Fecha más reciente
        last_update = None
        for info in self.pm.data.values():
            date = info.get('updated', info.get('created'))
            if date and (not last_update or date > last_update):
                last_update = date
        
        return {'total': total, 'last_update': last_update}
    
    def get_security_analysis(self):
        """Analizar seguridad de las contraseñas"""
        total = len(self.pm.data)
        if total == 0:
            return {
                'total': 0,
                'weak': 0,
                'old': 0,
                'duplicate': 0,
                'weak_details': [],
                'old_details': [],
                'duplicate_details': [],
                'security_score': 100
            }
        
        # Analizar contraseñas débiles
        weak_details = []
        for service, info in self.pm.data.items():
            password = info.get('password', '')
            if password:
                strength = PasswordGenerator.check_strength(password)
                if strength['score'] <= 2:  # Débil o muy débil
                    weak_details.append({
                        'service': service,
                        'username': info.get('username', 'N/A'),
                        'score': strength['score'],
                        'strength': strength['strength'],
                        'level': 'MUY DÉBIL' if strength['score'] <= 1 else 'DÉBIL'
                    })
        
        # Analizar contraseñas antiguas (más de 90 días)
        old_details = []
        now = datetime.now()
        for service, info in self.pm.data.items():
            updated_str = info.get('updated', info.get('created'))
            if updated_str:
                try:
                    updated = datetime.strptime(updated_str, "%Y-%m-%d %H:%M:%S")
                    days_old = (now - updated).days
                    if days_old >= 90:
                        old_details.append({
                            'service': service,
                            'username': info.get('username', 'N/A'),
                            'days': days_old
                        })
                except:
                    pass
        
        # Analizar contraseñas repetidas
        password_map = {}
        duplicate_details = []
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
                duplicate_details.append({
                    'services': services,
                    'count': len(services),
                    'service_names': [s['service'] for s in services]
                })
        
        # Calcular puntuación de seguridad
        weak_count = len(weak_details)
        old_count = len(old_details)
        duplicate_count = len(duplicate_details)
        
        score = 100
        if total > 0:
            score -= (weak_count / total) * 30
            score -= (old_count / total) * 20
            score -= (duplicate_count / total) * 25
        score = max(0, min(100, int(score)))
        
        # Determinar estado y color
        if score >= 80:
            status = "EXCELENTE"
            color = Colors.GREEN
            icon = "🟢"
        elif score >= 60:
            status = "BUENA"
            color = Colors.CYAN
            icon = "🔵"
        elif score >= 40:
            status = "MEDIA"
            color = Colors.YELLOW
            icon = "🟡"
        else:
            status = "CRÍTICA"
            color = Colors.RED
            icon = "🔴"
        
        return {
            'total': total,
            'weak': weak_count,
            'old': old_count,
            'duplicate': duplicate_count,
            'weak_details': weak_details,
            'old_details': old_details,
            'duplicate_details': duplicate_details,
            'security_score': score,
            'security_status': status,
            'security_color': color,
            'security_icon': icon
        }
    
    def show_statistics(self, ui, colors):
        """Mostrar estadísticas completas en pantalla"""
        basic = self.get_basic_stats()
        security = self.get_security_analysis()
        
        print(f"\n{colors.CYAN}{'═' * 70}{colors.RESET}")
        print(f"{colors.BOLD}{colors.GREEN}   📊 ESTADÍSTICAS GENERALES{colors.RESET}")
        print(f"{colors.CYAN}{'═' * 70}{colors.RESET}")
        print(f"{colors.YELLOW}[+] Total de contraseñas:{colors.RESET} {basic['total']}")
        if basic['last_update']:
            print(f"{colors.YELLOW}[+] Última actualización:{colors.RESET} {basic['last_update']}")
        
        print(f"\n{colors.CYAN}{'═' * 70}{colors.RESET}")
        print(f"{colors.BOLD}{colors.GREEN}   🛡️ ANÁLISIS DE SEGURIDAD{colors.RESET}")
        print(f"{colors.CYAN}{'═' * 70}{colors.RESET}")
        print(f"{colors.YELLOW}[+] Contraseñas débiles:{colors.RESET} {security['weak']}")
        print(f"{colors.YELLOW}[+] Contraseñas antiguas (+90 días):{colors.RESET} {security['old']}")
        print(f"{colors.YELLOW}[+] Contraseñas repetidas:{colors.RESET} {security['duplicate']}")
        
        # Mostrar detalles de contraseñas débiles
        if security['weak_details']:
            print(f"\n{colors.RED}⚠️ CONTRASEÑAS DÉBILES:{colors.RESET}")
            for w in security['weak_details']:
                print(f"   {colors.YELLOW}•{colors.RESET} {w['service']} ({w['username']}) - {w['level']} (puntuación: {w['score']}/5)")
        
        # Mostrar detalles de contraseñas antiguas
        if security['old_details']:
            print(f"\n{colors.YELLOW}📅 CONTRASEÑAS ANTIGUAS:{colors.RESET}")
            for o in security['old_details']:
                print(f"   {colors.YELLOW}•{colors.RESET} {o['service']} ({o['username']}) - {o['days']} días sin actualizar")
        
        # Mostrar detalles de contraseñas repetidas
        if security['duplicate_details']:
            print(f"\n{colors.RED}🔄 CONTRASEÑAS REPETIDAS:{colors.RESET}")
            for d in security['duplicate_details']:
                service_list = ', '.join([s['service'] for s in d['services'][:3]])
                if d['count'] > 3:
                    service_list += f" y {d['count'] - 3} más"
                print(f"   {colors.YELLOW}•{colors.RESET} {d['count']} servicios: {service_list}")
        
        # Barra de puntuación
        score = security['security_score']
        bar_length = 30
        filled = int(bar_length * score / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        print(f"\n{colors.YELLOW}[+] Puntuación seguridad:{colors.RESET} {security['security_color']}[{bar}] {score}%{colors.RESET} ({security['security_status']})")
        
        # Recomendaciones
        if score < 70:
            print(f"\n{colors.RED}📋 RECOMENDACIONES DE SEGURIDAD:{colors.RESET}")
            if security['weak'] > 0:
                print(f"   • Usa el generador de contraseñas (opción G) para crear contraseñas seguras")
                print(f"   • Las contraseñas seguras deben tener mayúsculas, números y símbolos")
            if security['old'] > 0:
                print(f"   • Actualiza las contraseñas antiguas (opción 2 para ver y cambiar)")
            if security['duplicate'] > 0:
                print(f"   • Evita repetir contraseñas, usa una única por servicio")
            print(f"   • Ejecuta la opción N para ver notificaciones detalladas")
        
        return security