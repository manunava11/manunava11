import os
import cv2
import torch
from ultralytics import YOLO

# Ruta de la carpeta que contiene las carpetas de imágenes
ROOT_DIR = r'C:\Users\Manuel\Desktop\Carpeta Visual\GordasSantaIsa'

# Cargar modelo YOLOv8 (cambiar por el modelo que uses)
model = YOLO(r'C:\Users\Manuel\Desktop\Carpeta Visual\Sistema-De-Conteo-De-Ganado\EntrenarYolov8\v11l_ft_detection_model.pt')


def is_bbox_on_border(bbox, img_width, img_height, border_threshold=5):
    """Verifica si el bounding box toca los bordes de la imagen."""
    x1, y1, x2, y2 = bbox
    return (
        x1 <= border_threshold or 
        y1 <= border_threshold or 
        x2 >= img_width - border_threshold or 
        y2 >= img_height - border_threshold
    )

def process_folder(folder_path):
    """Procesa cada imagen de la carpeta y elimina las que cumplen la condición."""
    for filename in os.listdir(folder_path):
        if not filename.lower().endswith((".jpg", ".png", ".jpeg")):
            continue  # Ignorar archivos no imágenes

        image_path = os.path.join(folder_path, filename)
        image = cv2.imread(image_path)

        if image is None:
            print(f"Error cargando {image_path}, ignorando...")
            continue

        height, width, _ = image.shape
        results = model(image)  # Realizar detección

        for result in results:
            for box in result.boxes.xyxy:  # Obtener bounding boxes
                if is_bbox_on_border(box.tolist(), width, height):
                    print(f"Eliminando {image_path} - Vaca en el borde")
                    os.remove(image_path)
                    break  # No revisar más bounding boxes en esta imagen

def process_all_folders(root_dir):
    """Recorre todas las carpetas dentro del directorio raíz."""
    for folder in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder)
        if os.path.isdir(folder_path):
            print(f"Procesando carpeta: {folder}")
            process_folder(folder_path)

# Ejecutar procesamiento en todas las carpetas
process_all_folders(ROOT_DIR)
