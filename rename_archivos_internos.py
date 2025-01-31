import os
import re

def renombrar_imagenes_en_carpetas(ruta_principal):
    """
    Renombra las imágenes en las carpetas dentro de una ruta principal.
    El nombre de cada imagen será igual al nombre de la carpeta, seguido de un sufijo que indique el orden.
    """
    # Extensiones válidas para imágenes
    extensiones_validas = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')

    # Recorrer todas las carpetas dentro de la ruta principal
    for carpeta in os.listdir(ruta_principal):
        carpeta_path = os.path.join(ruta_principal, carpeta)

        # Verificar si es una carpeta
        if os.path.isdir(carpeta_path):
            print(f"Procesando carpeta: {carpeta}")

            # Listar todas las imágenes en la carpeta
            imagenes = [f for f in os.listdir(carpeta_path) if f.lower().endswith(extensiones_validas)]

            # Ordenar las imágenes por sufijo numérico
            def extraer_sufijo(nombre):
                # Buscar el sufijo numérico en los nombres como "cow8_5" o "cow377_V4_3_frame_5"
                match = re.search(r'_(\d+)(?:\.|$)', nombre)
                return int(match.group(1)) if match else float("inf")

            imagenes.sort(key=extraer_sufijo)

            # Renombrar las imágenes
            for idx, imagen in enumerate(imagenes, start=1):
                # Crear el nuevo nombre basado en el nombre de la carpeta
                extension = os.path.splitext(imagen)[1]  # Obtener la extensión del archivo
                nuevo_nombre = f"{carpeta}_{idx}{extension}"

                # Rutas completas
                imagen_path = os.path.join(carpeta_path, imagen)
                nuevo_nombre_path = os.path.join(carpeta_path, nuevo_nombre)

                # Renombrar la imagen
                os.rename(imagen_path, nuevo_nombre_path)
                print(f"Renombrado: {imagen} -> {nuevo_nombre}")

    print("Renombrado completado.")

# Parámetros
ruta_principal = r"C:\Users\Manuel\Desktop\Carpeta Visual\DatasetElOmbu"  # Ruta principal donde están las carpetas

# Ejecutar función
renombrar_imagenes_en_carpetas(ruta_principal)
