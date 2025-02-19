import os
import cv2
from ultralytics import YOLO
from tqdm import tqdm

# Rutas de entrada y salida
VIDEO_DIR = r'C:\Users\Manuel\Desktop\Carpeta Visual\DataGordas'
OUTPUT_DIR = r'C:\Users\Manuel\Desktop\Carpeta Visual\GordasCutoff'
FRAME_INTERVAL_SECONDS = 0.2  # Extraer un frame cada X segundos

# Cargar modelo YOLOv8
model = YOLO(r'C:\Users\Manuel\Desktop\Carpeta Visual\Sistema-De-Conteo-De-Ganado\EntrenarYolov8\v11l_ft_detection_model.pt')

def is_bbox_on_border(bbox, img_width, img_height, border_threshold=15):
    """Verifica si el bounding box toca los bordes de la imagen."""
    x1, y1, x2, y2 = bbox
    return (
        x1 <= border_threshold or 
        y1 <= border_threshold or 
        x2 >= img_width - border_threshold or 
        y2 >= img_height - border_threshold
    )

def get_highest_vaca_bbox(results):
    """Devuelve el bounding box de la vaca más alta en la imagen (menor y1)."""
    highest_vaca = None
    min_y1 = float("inf")  # Inicializamos con un valor alto

    for result in results:
        for box in result.boxes.xyxy:
            x1, y1, x2, y2 = box.tolist()
            if y1 < min_y1:  # Buscamos la vaca más alta
                min_y1 = y1
                highest_vaca = (x1, y1, x2, y2)

    return highest_vaca

def process_video(video_path, output_folder):
    """Procesa un video, extrae frames en intervalos definidos y guarda solo los válidos."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error abriendo video: {video_path}")
        return

    os.makedirs(output_folder, exist_ok=True)  # Crear carpeta si no existe
    frame_count = 0

    fps = cap.get(cv2.CAP_PROP_FPS)  # Obtener FPS del video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total de frames
    frame_interval = int(fps * FRAME_INTERVAL_SECONDS)  # Intervalo en frames

    print(f"Procesando {video_path} ({total_frames} frames, FPS: {fps:.2f})...")

    for frame_idx in tqdm(range(0, total_frames, frame_interval), desc=os.path.basename(video_path)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)  # Ir al frame deseado
        ret, frame = cap.read()
        if not ret:
            break  # Fin del video

        height, width, _ = frame.shape
        results = model(frame)  # Realizar detección

        highest_vaca = get_highest_vaca_bbox(results)

        if highest_vaca and not is_bbox_on_border(highest_vaca, width, height):
            frame_filename = f"frame_{frame_count:04d}.jpg"
            frame_path = os.path.join(output_folder, frame_filename)
            cv2.imwrite(frame_path, frame)
            frame_count += 1

    cap.release()
    print(f"Frames guardados en {output_folder}: {frame_count}")

def process_all_videos(video_dir, output_dir):
    """Procesa todos los videos en la carpeta de entrada."""
    for filename in os.listdir(video_dir):
        if filename.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
            video_path = os.path.join(video_dir, filename)
            video_name = os.path.splitext(filename)[0]  # Nombre sin extensión
            output_folder = os.path.join(output_dir, video_name)
            process_video(video_path, output_folder)

# Ejecutar el procesamiento en todos los videos
process_all_videos(VIDEO_DIR, OUTPUT_DIR)