"""
Módulo de colores - DNO Encryptx
"""

class Colors:
    """Colores ANSI para terminal"""
    
    # Colores básicos
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    BLACK = '\033[90m'
    WHITE = '\033[97m'
    
    # Estilos
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    
    # Fondos
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_PURPLE = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    RESET = '\033[0m'
    
    @classmethod
    def colorize(cls, text, color=None, style=None):
        """Aplica color y estilo al texto"""
        result = ""
        if style:
            result += style
        if color:
            result += color
        result += text
        result += cls.RESET
        return result
    
    @classmethod
    def success(cls, text):
        """Texto de éxito (verde)"""
        return cls.colorize(text, cls.GREEN)
    
    @classmethod
    def error(cls, text):
        """Texto de error (rojo)"""
        return cls.colorize(text, cls.RED)
    
    @classmethod
    def warning(cls, text):
        """Texto de advertencia (amarillo)"""
        return cls.colorize(text, cls.YELLOW)
    
    @classmethod
    def info(cls, text):
        """Texto de información (cian)"""
        return cls.colorize(text, cls.CYAN)