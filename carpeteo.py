import os
import shutil
import re

def move_images_to_folders(directory):
    # Obtener todas las carpetas que terminen en "_Cownro"
    folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f)) and re.search(r'_Cow(\d+)', f)]
    
    # Ordenar carpetas por el número "Cow" al final
    folders.sort(key=lambda x: int(re.search(r'_Cow(\d+)', x).group(1)))
    
    # Obtener todas las imágenes que sigan el patrón "cowX_Y"
    images = [f for f in os.listdir(directory) if re.search(r'cow(\d+)_(\d+)\.jpg', f)]
    
    # Agrupar imágenes por "cowX"
    cow_images = {}
    for img in images:
        match = re.search(r'cow(\d+)', img)
        if match:
            cow_number = int(match.group(1))
            if cow_number not in cow_images:
                cow_images[cow_number] = []
            cow_images[cow_number].append(img)
    
    # Ordenar las imágenes dentro de cada grupo "cowX"
    for cow_number in cow_images:
        cow_images[cow_number].sort(key=lambda x: int(re.search(r'cow\d+_(\d+)', x).group(1)))
    
    # Mover las imágenes a las carpetas correspondientes
    for cow_number, images in cow_images.items():
        if cow_number - 1 < len(folders):  # Asegurarse de que haya una carpeta correspondiente
            target_folder = folders[cow_number - 1]
            for img in images:
                source_path = os.path.join(directory, img)
                target_path = os.path.join(directory, target_folder, img)
                shutil.move(source_path, target_path)
                print(f"Moviendo {img} a {target_folder}")

# Ejemplo de uso:
directory = r'C:\Users\Manuel\Desktop\Carpeta Visual\Dia5Barracas\V2_3-004_frame'  # Cambia a tu ruta
move_images_to_folders(directory)
