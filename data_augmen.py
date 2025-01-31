import os
import cv2
import numpy as np
import random

def adjust_brightness_contrast(image):
    """Ajusta el brillo y contraste aleatoriamente."""
    alpha = random.uniform(0.5, 1.5)  # Factor de contraste (0.8 a 1.2)
    beta = random.randint(-50, 50)    # Brillo (-30 a 30)
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def rotate_image_and_labels(image, labels, angle):
    """Rota la imagen en múltiplos de 90° y ajusta los bounding boxes."""
    h, w = image.shape[:2]
    
    # Rotar imagen
    if angle == 90:
        rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        rotated_image = cv2.rotate(image, cv2.ROTATE_180)
    elif angle == 270:
        rotated_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        return image, labels  # Si es 0°, no hay cambios

    # Transformar bounding boxes
    updated_labels = []
    for label in labels:
        cls, x_center, y_center, width, height = map(float, label.split())

        if angle == 90:
            new_x = y_center
            new_y = 1 - x_center
            new_w, new_h = height, width
        elif angle == 180:
            new_x = 1 - x_center
            new_y = 1 - y_center
            new_w, new_h = width, height
        elif angle == 270:
            new_x = 1 - y_center
            new_y = x_center
            new_w, new_h = height, width
        else:
            new_x, new_y, new_w, new_h = x_center, y_center, width, height

        updated_labels.append(f"{int(cls)} {new_x:.6f} {new_y:.6f} {new_w:.6f} {new_h:.6f}")

    return rotated_image, updated_labels

def process_dataset(root_path):
    """Recorre cada dataset y aplica aumentaciones"""
    datasets = [f for f in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, f))]

    for dataset in datasets:
        images_path = os.path.join(root_path, dataset, "images")
        labels_path = os.path.join(root_path, dataset, "labels")

        if not os.path.exists(images_path) or not os.path.exists(labels_path):
            print(f"Saltando {dataset}: faltan carpetas 'images' o 'labels'.")
            continue

        for image_file in os.listdir(images_path):
            if not image_file.endswith(('.jpg', '.png', '.jpeg')):
                continue

            image_path = os.path.join(images_path, image_file)
            label_path = os.path.join(labels_path, image_file.replace(".jpg", ".txt").replace(".png", ".txt"))

            if not os.path.exists(label_path):
                print(f"Saltando {image_file}: no tiene un archivo de etiquetas.")
                continue

            # Leer imagen y etiquetas
            image = cv2.imread(image_path)
            with open(label_path, "r") as f:
                labels = f.readlines()

            # Aplicar transformación de brillo y contraste
            modified_image = adjust_brightness_contrast(image)

            # Seleccionar rotación aleatoria de 0, 90, 180 o 270 grados
            angle = random.choice([0,180])
            rotated_image, updated_labels = rotate_image_and_labels(modified_image, labels, angle)

            # Guardar imagen aumentada
            new_image_path = image_path.replace(".jpg", f"aug{angle}.jpg").replace(".png", f"aug{angle}.png")
            cv2.imwrite(new_image_path, rotated_image)

            # Guardar etiquetas modificadas
            new_label_path = label_path.replace(".txt", f"aug{angle}.txt")
            with open(new_label_path, "w") as f:
                f.writelines("\n".join(updated_labels))

            print(f"Procesado: {new_image_path}")

if __name__ == "__main__":
    ruta = r'C:\Users\Manuel\Desktop\Carpeta Visual\Bovinos\ImagenesNew'
    process_dataset(ruta)
