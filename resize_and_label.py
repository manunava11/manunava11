import os
import cv2

def process_dataset(dataset_path):
    """ Procesa todas las imágenes y etiquetas en el dataset """
    new_width, new_height = 3840, 2160  # Resolución final (4K)

    for split in ["train", "valid", "test"]:
        images_path = os.path.join(dataset_path, split, "images")
        labels_path = os.path.join(dataset_path, split, "labels")

        if not os.path.exists(images_path) or not os.path.exists(labels_path):
            continue

        for img_name in os.listdir(images_path):
            img_path = os.path.join(images_path, img_name)
            label_path = os.path.join(labels_path, img_name.replace(".jpg", ".txt"))

            if not img_path.endswith(".jpg"):
                continue

            # Cargar imagen original
            img = cv2.imread(img_path)
            if img is None:
                print(f"Error al cargar la imagen: {img_path}")
                continue

            # Redimensionar imagen a 4K
            img_resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
            cv2.imwrite(img_path, img_resized)

            # ✅ No se modifican los labels porque en YOLO ya están normalizados (0 a 1)
            print(f"Procesado: {img_name}")


dataset_path = r'C:\Users\Manuel\Desktop\Carpeta Visual\Bovinos\Dataset'  # Cambia esto por la ruta real
process_dataset(dataset_path)
