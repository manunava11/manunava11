import cv2
import os
import torch
import numpy as np
from ultralytics import YOLO

# Configurar el dispositivo (GPU si está disponible)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Cargar el modelo YOLO
model = YOLO(r"C:\Users\Manuel\Desktop\Carpeta Visual\Sistema-De-Conteo-De-Ganado\EntrenarYolov8\ovejas.pt").to(device)

def iou(box1, box2):
    """Calcula el IoU (Intersection over Union) entre dos bounding boxes."""
    x1, y1, x2, y2 = box1
    x1g, y1g, x2g, y2g = box2

    # Calcular intersección
    xi1 = max(x1, x1g)
    yi1 = max(y1, y1g)
    xi2 = min(x2, x2g)
    yi2 = min(y2, y2g)

    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)

    # Calcular áreas de los cuadros
    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (x2g - x1g) * (y2g - y1g)

    # Calcular IoU
    union_area = box1_area + box2_area - inter_area
    return inter_area / union_area if union_area > 0 else 0

def apply_nms(boxes, iou_threshold=0.5):
    """Elimina detecciones con alto solapamiento (IoU > umbral)."""
    if not boxes:
        return []

    # Ordenar por confianza (mayor a menor)
    boxes = sorted(boxes, key=lambda x: x[5], reverse=True)
    final_boxes = []

    while boxes:
        chosen_box = boxes.pop(0)
        final_boxes.append(chosen_box)

        boxes = [box for box in boxes if iou(chosen_box[:4], box[:4]) < iou_threshold]

    return final_boxes

def process_image(image_path, output_folder):
    """ Procesa una imagen, detecta vacas y guarda las imágenes y etiquetas. """
    image = cv2.imread(image_path)
    results = model(image)

    labels_folder = os.path.join(output_folder, "labels")
    images_folder = os.path.join(output_folder, "images")
    os.makedirs(labels_folder, exist_ok=True)
    os.makedirs(images_folder, exist_ok=True)

    image_name = os.path.basename(image_path)
    cv2.imwrite(os.path.join(images_folder, image_name), image)

    detected_boxes = []

    for result in results:
        for box in result.boxes:
            if box.conf > 0.4:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf)  # Confianza de la detección
                detected_boxes.append([x1, y1, x2, y2, 0, confidence])  # [x1, y1, x2, y2, class_id, conf]

    # Aplicar NMS con IoU threshold de 0.5
    filtered_boxes = apply_nms(detected_boxes, iou_threshold=0.5)

    # Guardar etiquetas normalizadas
    txt_filename = os.path.splitext(image_name)[0] + ".txt"
    txt_path = os.path.join(labels_folder, txt_filename)

    with open(txt_path, 'w') as f:
        for x1, y1, x2, y2, class_id, conf in filtered_boxes:
            h, w, _ = image.shape
            x_center = (x1 + x2) / 2 / w
            y_center = (y1 + y2) / 2 / h
            width = (x2 - x1) / w
            height = (y2 - y1) / h
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

    print(f"Procesado: {image_name} | Detecciones finales: {len(filtered_boxes)}")

def process_dataset(input_root, output_root):
    """ Recorre cada dataset y procesa las imágenes en su subcarpeta 'images'. """
    datasets = [d for d in os.listdir(input_root) if os.path.isdir(os.path.join(input_root, d))]

    for dataset in datasets:
        images_path = os.path.join(input_root, dataset, "images")
        output_folder = os.path.join(output_root, dataset)

        if not os.path.exists(images_path):
            print(f"Saltando {dataset}: no tiene carpeta 'images'.")
            continue

        print(f"Procesando dataset: {dataset}")
        process_image_folder(images_path, output_folder)

def process_image_folder(folder_path, output_folder):
    """ Procesa todas las imágenes en la carpeta dada. """
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            process_image(image_path, output_folder)

if __name__ == "__main__":
    input_root = r"C:\Users\Manuel\Desktop\Carpeta Visual\Bovinos\Imagenes"  # Carpeta con datasets
    output_root = r"C:\Users\Manuel\Desktop\Carpeta Visual\Bovinos\Resultados"  # Carpeta de salida

    process_dataset(input_root, output_root)  # Procesar todas las carpetas
