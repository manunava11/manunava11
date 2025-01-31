import os
import re

def eliminar_ultima_imagen(ruta_principal):
    """
    Recorre las carpetas en la ruta principal y elimina la imagen con el mayor número después de 'frame_'.
    """
    # Recorrer cada carpeta en la ruta principal
    for carpeta in os.listdir(ruta_principal):
        carpeta_path = os.path.join(ruta_principal, carpeta)

        # Verificar si es una carpeta
        if os.path.isdir(carpeta_path):
            print(f"Procesando carpeta: {carpeta}")

            # Filtrar archivos que coincidan con el patrón 'frame_'
            imagenes = [f for f in os.listdir(carpeta_path) if re.search(r'frame_(\d+)\.jpg$', f)]

            # Encontrar la imagen con el mayor número después de 'frame_'
            max_frame = -1
            imagen_maxima = None

            for imagen in imagenes:
                match = re.search(r'frame_(\d+)\.jpg$', imagen)
                if match:
                    frame_num = int(match.group(1))
                    if frame_num > max_frame:
                        max_frame = frame_num
                        imagen_maxima = imagen

            # Eliminar la imagen con el mayor número
            if imagen_maxima:
                imagen_a_eliminar = os.path.join(carpeta_path, imagen_maxima)
                os.remove(imagen_a_eliminar)
                print(f"Eliminada: {imagen_a_eliminar}")
            else:
                print(f"No se encontraron imágenes en la carpeta: {carpeta}")

    print("Proceso completado.")

# Parámetros
ruta_principal = r'C:\Users\Manuel\Desktop\Carpeta Visual\DatasetBarracas7m\bien\Las100'  # Cambia esta ruta a tu directorio

# Ejecutar función
eliminar_ultima_imagen(ruta_principal)
