import os

def verificar_carpetas_con_pocas_imagenes(ruta_principal):
    """
    Recorre las carpetas dentro de una ruta principal y verifica si tienen menos de 5 imágenes.
    Imprime el nombre de las carpetas que cumplen esta condición.
    """
    # Extensiones válidas para imágenes
    extensiones_validas = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')

    # Recorrer todas las carpetas dentro de la ruta principal
    for carpeta in os.listdir(ruta_principal):
        carpeta_path = os.path.join(ruta_principal, carpeta)

        # Verificar si es una carpeta
        if os.path.isdir(carpeta_path):
            # Listar solo archivos con extensiones de imagen
            imagenes = [f for f in os.listdir(carpeta_path) if f.lower().endswith(extensiones_validas)]

            # Verificar si la cantidad de imágenes es menor a 5
            if len(imagenes) < 9:
                print(f"La carpeta '{carpeta}' tiene {len(imagenes)} imágenes (menos de 5).")

    print("Verificación completada.")

# Parámetros
ruta_principal = r'C:\Users\Manuel\Desktop\Carpeta Visual\DatasetBarracas7m\bien\Las100'

# Ejecutar función
verificar_carpetas_con_pocas_imagenes(ruta_principal)
