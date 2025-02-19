import os
import cv2
import random
import numpy as np
from ultralytics import YOLO
from albumentations import Compose, RandomBrightnessContrast, RandomGamma, Rotate, OneOf, GaussNoise, ShiftScaleRotate, HorizontalFlip, VerticalFlip, Affine, BboxParams, ToGray, RandomScale

# Configuración
VIDEO_DIR = r"C:\Users\Manuel\Desktop\Carpeta Visual\Ovinos\Videos"  # Cambia por la ruta de los videos
OUTPUT_DIR = r"C:\Users\Manuel\Desktop\Carpeta Visual\Ovinos\Resultados"  # Cambia por la ruta donde guardar resultados
FRAME_INTERVAL = 1  # Intervalo de extracción en segundos
MODEL_PATH = r"C:\Users\Manuel\Desktop\Carpeta Visual\Sistema-De-Conteo-De-Ganado\EntrenarYolov8\v11x_ovejas.pt"  # Ruta al modelo YOLOv8
CONFIDENCE_THRESHOLD = 0.5  # Umbral de confianza configurable
IOU_THRESHOLD = 0.4  # Umbral de IoU
BRIGHTNESS_LIMIT = 0.3  # Rango de brillo (-0.2 a 0.2)
CONTRAST_LIMIT = 0.3  # Rango de contraste (-0.2 a 0.2)

def create_folders():
    os.makedirs(os.path.join(OUTPUT_DIR, "images"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "labels"), exist_ok=True)

def extract_frames(video_path, frame_interval, model):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_step = frame_interval * fps
    frame_count = 0
    
    while cap.isOpened():
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_filename = f"{os.path.basename(video_path).split('.')[0]}_frame{frame_count}.jpg"
        frame_path = os.path.join(OUTPUT_DIR, "images", frame_filename)
        cv2.imwrite(frame_path, frame)
        
        # Detectar y etiquetar
        label_path = os.path.join(OUTPUT_DIR, "labels", frame_filename.replace('.jpg', '.txt'))
        detect_and_label(frame, model, label_path)
        
        frame_count += frame_step
    
    cap.release()

def detect_and_label(image, model, label_path):
    results = model(image, conf=CONFIDENCE_THRESHOLD, iou=IOU_THRESHOLD)
    height, width, _ = image.shape
    with open(label_path, 'w') as f:
        for result in results:
            for box in result.boxes.xywh:
                x, y, w, h = box.tolist()
                # Normalizar bounding boxes a formato YOLO
                x /= width
                y /= height
                w /= width
                h /= height
                f.write(f"0 {x} {y} {w} {h}\n")

def load_labels(label_path):
    bboxes = []
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            for line in f.readlines():
                values = line.strip().split()
                class_id = int(values[0])  # Asegurar que la clase sea un entero
                x, y, w, h = map(float, values[1:])
                bboxes.append([x, y, w, h, class_id])
    return bboxes

def apply_augmentation():
    aug1 = Compose([
        RandomBrightnessContrast(brightness_limit=BRIGHTNESS_LIMIT, contrast_limit=CONTRAST_LIMIT, p=0.7),
        RandomGamma(gamma_limit=(80, 120), p=0.7),
        OneOf([
            HorizontalFlip(p=1.0),
            VerticalFlip(p=1.0)
        ], p=1.0)
    ], bbox_params=BboxParams(format='yolo', label_fields=['class_labels']))
    
    aug2 = Compose([
        GaussNoise(var_limit=(10, 50), p=0.8),
        Affine(translate_percent=(0.10, 0.10), p=1.0),
        RandomScale(scale_limit=0.2, p=0.7),
        ToGray(p=0.8)
    ], bbox_params=BboxParams(format='yolo', label_fields=['class_labels']))
    
    image_dir = os.path.join(OUTPUT_DIR, "images")
    label_dir = os.path.join(OUTPUT_DIR, "labels")
    
    for img_file in os.listdir(image_dir):
        img_path = os.path.join(image_dir, img_file)
        label_path = os.path.join(label_dir, img_file.replace('.jpg', '.txt'))
        
        bboxes = load_labels(label_path)
        if bboxes:
            image = cv2.imread(img_path)
            height, width, _ = image.shape
            class_labels = [int(box[4]) for box in bboxes]  # Asegurar que las clases sean enteros
            
            transformed1 = aug1(image=image, bboxes=[box[:4] for box in bboxes], class_labels=class_labels)
            transformed2 = aug2(image=image, bboxes=[box[:4] for box in bboxes], class_labels=class_labels)
            
            new_img_path1 = img_path.replace('.jpg', '_aug1.jpg')
            new_label_path1 = label_path.replace('.txt', '_aug1.txt')
            new_img_path2 = img_path.replace('.jpg', '_aug2.jpg')
            new_label_path2 = label_path.replace('.txt', '_aug2.txt')
            
            cv2.imwrite(new_img_path1, transformed1['image'])
            cv2.imwrite(new_img_path2, transformed2['image'])
            
            with open(new_label_path1, 'w') as f:
                for bbox, cls in zip(transformed1['bboxes'], transformed1['class_labels']):
                    f.write(f"{int(cls)} {' '.join(map(str, bbox[:4]))}\n")
            
            with open(new_label_path2, 'w') as f:
                for bbox, cls in zip(transformed2['bboxes'], transformed2['class_labels']):
                    f.write(f"{int(cls)} {' '.join(map(str, bbox[:4]))}\n")

if __name__ == "__main__":
    create_folders()
    model = YOLO(MODEL_PATH)
    
    for video in os.listdir(VIDEO_DIR):
        if video.endswith(('.mp4', '.avi', '.mov','.MP4')):
            video_path = os.path.join(VIDEO_DIR, video)
            extract_frames(video_path, FRAME_INTERVAL, model)
    
    apply_augmentation()
    print("Proceso completado.")
