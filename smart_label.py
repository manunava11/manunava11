import cv2
import os
from ultralytics import YOLO
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Cargar el modelo
model = YOLO(r"C:\Users\Manuel\Desktop\Carpeta Visual\Sistema-De-Conteo-De-Ganado\EntrenarYolov8\v11l_ft_detection_model.pt").to(device)

def process_image(image_path, output_folder):
    # Leer la imagen
    image = cv2.imread(image_path)

    # Ejecutar detección
    results = model(image)

    # Crear carpetas "labels" y "images" en la ruta especificada si no existen
    labels_folder = os.path.join(output_folder, "labels")
    images_folder = os.path.join(output_folder, "images")
    os.makedirs(labels_folder, exist_ok=True)
    os.makedirs(images_folder, exist_ok=True)

    # Guardar la imagen en la carpeta "images"
    image_name = os.path.basename(image_path)
    cv2.imwrite(os.path.join(images_folder, image_name), image)

    # Procesar los resultados
    for result in results:
        for box in result.boxes:
            # Verificar si la confianza es mayor a 0.6
            if box.conf > 0.4:
                # Obtener las coordenadas
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordenadas del bounding box
                class_id = 0  # Siempre será 0 (cow) en tu caso

                # Crear o abrir el archivo .txt correspondiente
                txt_filename = os.path.splitext(image_name)[0] + ".txt"
                with open(os.path.join(labels_folder, txt_filename), 'a') as f:
                    # Escribir la información en el formato: class_id x_center y_center width height
                    # Los valores deben estar normalizados (0 a 1) según el tamaño de la imagen
                    image_height, image_width, _ = image.shape
                    x_center = (x1 + x2) / 2 / image_width
                    y_center = (y1 + y2) / 2 / image_height
                    width = (x2 - x1) / image_width
                    height = (y2 - y1) / image_height
                    f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

def process_image_folder(folder_path, output_folder):
    # Recorrer todos los archivos en la carpeta
    for filename in os.listdir(folder_path):
        # Verificar si el archivo es una imagen
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            process_image(image_path, output_folder)

# Ejemplo de uso
input_folder = r'C:\Users\Manuel\Desktop\Carpeta Visual\Bovinos\Imagenes\DJI_0391_frame'  # Carpeta con las imágenes a procesar
output_folder = r'C:\Users\Manuel\Desktop\Carpeta Visual\Bovinos\Imagenes\DJI_0391_frame'  # Carpeta donde se guardarán "labels" e "images"
process_image_folder(input_folder, output_folder)  # Procesar todas las imágenes en la carpeta
