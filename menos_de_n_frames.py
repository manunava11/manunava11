import os
import cv2

def verificar_videos_con_pocos_frames(ruta):
    """
    Recorre una carpeta, verifica si los videos tienen menos de 7 frames,
    e imprime el nombre de los videos que cumplen esta condición.
    """
    # Extensiones de archivos de video válidas
    extensiones_validas = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')

    # Recorrer todos los archivos en la carpeta
    for archivo in os.listdir(ruta):
        # Verificar si es un archivo de video
        if archivo.lower().endswith(extensiones_validas):
            video_path = os.path.join(ruta, archivo)

            # Abrir el video con OpenCV
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"No se pudo abrir el archivo: {archivo}")
                continue

            # Obtener el número total de frames
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()

            # Verificar si el video tiene menos de 7 frames
            if total_frames < 10:
                print(f"El video '{archivo}' tiene {total_frames} frames (menos de 7).")

    print("Verificación completada.")

# Parámetros
ruta_videos = r'C:\Users\Manuel\Desktop\Carpeta Visual\DatasetBarracas7m\bien\Las100'

# Ejecutar función
verificar_videos_con_pocos_frames(ruta_videos)
