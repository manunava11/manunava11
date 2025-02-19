import os
import re

def hacer_videos_continuos(ruta, prefix="cow"):
    """
    Renombra videos en una carpeta para que sean continuos.
    Ejemplo: Si cow690_V8_2 es seguido por cow697_V8_2, renombrar cow697_V8_2 a cow691_V8_2.
    """
    # Función para extraer el número después del prefijo 'cow'
    def extract_number(file_name):
        match = re.match(rf"{prefix}(\d+)_", file_name)  # Buscar el número después del prefijo 'cow'
        return int(match.group(1)) if match else None  # Devolver el número como entero

    # Obtener la lista de archivos de video en la carpeta
    video_files = sorted(
        [f for f in os.listdir(ruta) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))],
        key=lambda x: extract_number(x) if extract_number(x) is not None else float("inf")
    )

    # Renombrar archivos para que sean continuos
    expected_number = None
    for file_name in video_files:
        # Extraer el número después de 'cow'
        match = re.match(rf"{prefix}(\d+)_", file_name)
        if not match:
            continue  # Saltar archivos que no coinciden con el formato

        current_number = int(match.group(1))  # Número actual
        if expected_number is None:
            expected_number = current_number  # Configurar el primer número esperado

        # Verificar si el número actual coincide con el esperado
        if current_number != expected_number:
            # Crear el nuevo nombre
            rest_of_name = file_name.split("_", 1)[1]  # Conservar todo después del primer '_'
            new_name = f"{prefix}{expected_number}_{rest_of_name}"

            # Construir las rutas completas
            old_path = os.path.join(ruta, file_name)
            new_path = os.path.join(ruta, new_name)

            # Renombrar el archivo
            os.rename(old_path, new_path)
            print(f"Renombrado: {file_name} -> {new_name}")

        # Incrementar el número esperado para el siguiente archivo
        expected_number += 1

    print("Renombrado completado. Los archivos son ahora continuos.")

# Parámetros
ruta_videos = r'C:\Users\Manuel\Desktop\Carpeta Visual\DataGordas'  # Ruta a la carpeta de videos

# Ejecutar función
hacer_videos_continuos(ruta_videos)
