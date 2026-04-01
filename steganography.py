"""
Módulo de Esteganografía - DNO Encryptx
Oculta y extrae datos encriptados dentro de imágenes PNG
Técnica: LSB (Least Significant Bit)
"""

import os
from PIL import Image
import io

class Steganography:
    """Clase para ocultar y extraer datos en imágenes"""

    def __init__(self):
        # Marcador para identificar que la imagen contiene una bóveda DNO
        self.header_marker = b"DNOVAULT"

    def hide_data(self, cover_image_path, data_to_hide, output_image_path):
        """
        Oculta datos (bytes) dentro de una imagen portadora.
        
        Args:
            cover_image_path: Ruta de la imagen portadora (PNG/JPG).
            data_to_hide: Los datos encriptados (bytes) a ocultar.
            output_image_path: Ruta donde se guardará la imagen resultante (siempre PNG).
            
        Returns:
            tuple: (success, message)
        """
        if not os.path.exists(cover_image_path):
            return False, f"Imagen portadora no encontrada: {cover_image_path}"

        try:
            # 1. Preparar la carga útil (Payload)
            # Formato: [Marcador][Longitud de datos (4 bytes)][Datos Encriptados]
            data_len = len(data_to_hide).to_bytes(4, byteorder='big')
            payload = self.header_marker + data_len + data_to_hide
            
            # Convertir payload a una secuencia de bits (0 y 1)
            bits_to_hide = []
            for byte in payload:
                # Convertir byte a 8 bits y añadirlos a la lista
                bits_to_hide.extend([int(b) for b in f"{byte:08b}"])
            
            num_bits = len(bits_to_hide)
            
            # 2. Preparar la imagen portadora
            img = Image.open(cover_image_path)
            
            # Forzar conversión a RGBA para tener 4 canales (Red, Green, Blue, Alpha)
            # Esto nos da más espacio para ocultar datos.
            img = img.convert('RGBA')
            width, height = img.size
            pixels = img.load()
            
            # 3. Verificar capacidad
            # Cada píxel tiene 4 canales (RGBA), podemos guardar 1 bit en cada canal.
            total_capacity_bits = width * height * 4
            
            if num_bits > total_capacity_bits:
                return False, f"La imagen es demasiado pequeña. Capacidad: {total_capacity_bits} bits, Requerido: {num_bits} bits."

            # 4. Ocultar los bits (Algoritmo LSB)
            bit_index = 0
            for y in range(height):
                for x in range(width):
                    if bit_index >= num_bits:
                        # Ya ocultamos todo, guardar y salir
                        img.save(output_image_path, "PNG")
                        return True, f"Datos ocultos con éxito en {output_image_path}"
                    
                    # Obtener el píxel actual (R, G, B, A)
                    r, g, b, a = pixels[x, y]
                    channels = [r, g, b, a]
                    
                    # Modificar el bit menos significativo de cada canal
                    for i in range(4): # RGBA
                        if bit_index < num_bits:
                            # Tomar el canal actual, poner su último bit a 0 (con & ~1) 
                            # y sumarle el bit que queremos ocultar (0 o 1).
                            channels[i] = (channels[i] & ~1) | bits_to_hide[bit_index]
                            bit_index += 1
                    
                    # Actualizar el píxel en la imagen
                    pixels[x, y] = tuple(channels)
            
            # En caso teórico de que el bucle termine justo al final
            img.save(output_image_path, "PNG")
            return True, f"Datos ocultos con éxito en {output_image_path}"

        except Exception as e:
            return False, f"Error en la esteganografía: {e}"

    def extract_data(self, stego_image_path):
        """
        Extrae datos ocultos de una imagen PNG.
        
        Args:
            stego_image_path: Ruta de la imagen que contiene los datos.
            
        Returns:
            tuple: (success, extracted_data_bytes o message)
        """
        if not os.path.exists(stego_image_path):
            return False, "Imagen no encontrada"

        try:
            img = Image.open(stego_image_path)
            img = img.convert('RGBA')
            width, height = img.size
            pixels = img.load()
            
            # 1. Extraer todos los bits LSB
            extracted_bits = []
            for y in range(height):
                for x in range(width):
                    r, g, b, a = pixels[x, y]
                    for channel in [r, g, b, a]:
                        extracted_bits.append(channel & 1)
            
            # Convertir bits a bytes
            all_bytes = bytearray()
            for i in range(0, len(extracted_bits), 8):
                byte_bits = extracted_bits[i:i+8]
                if len(byte_bits) < 8: break # Fin de bits
                
                # Convertir 8 bits a un entero (byte)
                byte_str = "".join(map(str, byte_bits))
                all_bytes.append(int(byte_str, 2))
            
            # 2. Verificar el marcador DNO
            marker_len = len(self.header_marker)
            if all_bytes[:marker_len] != self.header_marker:
                return False, "La imagen no contiene una bóveda DNO válida."
            
            # 3. Leer la longitud de los datos (4 bytes después del marcador)
            data_len_bytes = all_bytes[marker_len : marker_len + 4]
            data_len = int.from_bytes(data_len_bytes, byteorder='big')
            
            # 4. Extraer los datos reales
            start_data = marker_len + 4
            extracted_data = all_bytes[start_data : start_data + data_len]
            
            # Verificación de integridad básica
            if len(extracted_data) != data_len:
                return False, "Error de integridad: los datos extraídos están incompletos."
                
            return True, bytes(extracted_data)

        except Exception as e:
            return False, f"Error al extraer datos: {e}"