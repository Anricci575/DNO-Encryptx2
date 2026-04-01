"""
Módulo de generación de contraseñas - DNO Encryptx
Generador de contraseñas seguras y evaluación de fortaleza
"""

import secrets
import string
import re

class PasswordGenerator:
    """Generador de contraseñas seguras"""
    
    @staticmethod
    def generate(length=16, use_uppercase=True, use_lowercase=True, 
                 use_numbers=True, use_symbols=True, exclude_ambiguous=False):
        """
        Generar contraseña aleatoria segura
        
        Args:
            length: Longitud de la contraseña (default: 16)
            use_uppercase: Incluir mayúsculas (default: True)
            use_lowercase: Incluir minúsculas (default: True)
            use_numbers: Incluir números (default: True)
            use_symbols: Incluir símbolos (default: True)
            exclude_ambiguous: Excluir caracteres ambiguos (default: False)
        
        Returns:
            str: Contraseña generada
        """
        # Caracteres disponibles
        chars = ""
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_numbers:
            chars += string.digits
        if use_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Excluir caracteres ambiguos (il1Lo0O)
        if exclude_ambiguous:
            ambiguous = "il1Lo0O"
            chars = ''.join(c for c in chars if c not in ambiguous)
        
        # Asegurar que hay al menos un conjunto de caracteres
        if not chars:
            chars = string.ascii_letters + string.digits
        
        # Generar contraseña usando secrets (criptográficamente seguro)
        password = ''.join(secrets.choice(chars) for _ in range(length))
        
        # Verificar que cumple con los requisitos mínimos
        password = PasswordGenerator._ensure_requirements(
            password, use_uppercase, use_lowercase, use_numbers, use_symbols
        )
        
        return password
    
    @staticmethod
    def _ensure_requirements(password, use_uppercase, use_lowercase, use_numbers, use_symbols):
        """Asegurar que la contraseña cumple con los requisitos"""
        # Lista de caracteres por tipo
        uppercase = string.ascii_uppercase
        lowercase = string.ascii_lowercase
        digits = string.digits
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Verificar cada requisito
        checks = []
        if use_uppercase and not any(c in uppercase for c in password):
            checks.append(secrets.choice(uppercase))
        if use_lowercase and not any(c in lowercase for c in password):
            checks.append(secrets.choice(lowercase))
        if use_numbers and not any(c in digits for c in password):
            checks.append(secrets.choice(digits))
        if use_symbols and not any(c in symbols for c in password):
            checks.append(secrets.choice(symbols))
        
        # Si faltan requisitos, agregarlos y mezclar
        if checks:
            password_list = list(password)
            for i, char in enumerate(checks):
                if i < len(password_list):
                    password_list[i] = char
            password = ''.join(password_list)
            # Mezclar para que no queden al principio
            password_list = list(password)
            for i in range(len(password_list) * 3):
                a = secrets.randbelow(len(password_list))
                b = secrets.randbelow(len(password_list))
                password_list[a], password_list[b] = password_list[b], password_list[a]
            password = ''.join(password_list)
        
        return password
    
    @staticmethod
    def generate_memorable(words=3, separator='-', capitalize=True, add_number=True):
        """
        Generar contraseña memorable (tipo passphrase)
        
        Args:
            words: Número de palabras (default: 3)
            separator: Separador entre palabras (default: '-')
            capitalize: Capitalizar palabras (default: True)
            add_number: Agregar número al final (default: True)
        
        Returns:
            str: Contraseña memorable
        """
        # Lista de palabras comunes (puedes expandirla)
        word_list = [
            'tiger', 'eagle', 'python', 'code', 'hacker', 'secure', 'shadow',
            'phantom', 'crypto', 'enigma', 'matrix', 'neon', 'cyber', 'nova',
            'quantum', 'echo', 'alpha', 'omega', 'storm', 'thunder', 'lightning',
            'forest', 'mountain', 'river', 'ocean', 'star', 'moon', 'sun'
        ]
        
        # Seleccionar palabras aleatorias
        selected = [secrets.choice(word_list) for _ in range(words)]
        
        # Capitalizar si es necesario
        if capitalize:
            selected = [w.capitalize() for w in selected]
        
        # Unir con separador
        password = separator.join(selected)
        
        # Agregar número al final
        if add_number:
            password += str(secrets.randbelow(100))
        
        return password
    
    @staticmethod
    def check_strength(password):
        """
        Evaluar fortaleza de la contraseña
        
        Args:
            password: Contraseña a evaluar
        
        Returns:
            dict: Resultados de la evaluación
        """
        score = 0
        feedback = []
        
        # 1. Evaluar longitud
        if len(password) >= 16:
            score += 2
        elif len(password) >= 12:
            score += 1
        elif len(password) < 8:
            feedback.append("❌ Usa al menos 8 caracteres (12+ recomendado)")
        
        # 2. Evaluar mayúsculas
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("❌ Incluye letras MAYÚSCULAS")
        
        # 3. Evaluar minúsculas
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("❌ Incluye letras minúsculas")
        
        # 4. Evaluar números
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("❌ Incluye números (0-9)")
        
        # 5. Evaluar símbolos
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if any(c in symbols for c in password):
            score += 1
        else:
            feedback.append("❌ Incluye símbolos (!@#$%^&*)")
        
        # 6. Evaluar caracteres repetidos
        if re.search(r'(.)\1{2,}', password):
            feedback.append("⚠️ Evita caracteres repetidos (ej: aaa, 111)")
        
        # 7. Evaluar patrones comunes
        common_patterns = ['123', 'abc', 'qwerty', 'admin', 'password']
        if any(pattern in password.lower() for pattern in common_patterns):
            feedback.append("⚠️ Evita patrones comunes (123, abc, qwerty)")
        
        # Determinar nivel de fortaleza
        if score >= 5:
            strength = "🟢 MUY FUERTE"
            color = "GREEN"
        elif score >= 4:
            strength = "🟢 FUERTE"
            color = "GREEN"
        elif score >= 3:
            strength = "🟡 MEDIA"
            color = "YELLOW"
        elif score >= 2:
            strength = "🟠 DÉBIL"
            color = "ORANGE"
        else:
            strength = "🔴 MUY DÉBIL"
            color = "RED"
        
        return {
            'score': score,
            'strength': strength,
            'color': color,
            'feedback': feedback,
            'length': len(password)
        }
    
    @staticmethod
    def get_strength_color(strength):
        """Obtener color ANSI según fortaleza"""
        colors = {
            'MUY FUERTE': '\033[92m',   # Verde
            'FUERTE': '\033[92m',        # Verde
            'MEDIA': '\033[93m',         # Amarillo
            'DÉBIL': '\033[91m',         # Rojo
            'MUY DÉBIL': '\033[91m'      # Rojo
        }
        return colors.get(strength, '\033[0m')