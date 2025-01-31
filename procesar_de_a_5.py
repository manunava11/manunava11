import os
import re
import shutil

def rename_files(directory):
    # Obtener lista de archivos que sigan el patrón "_frame_nro"
    files = [f for f in os.listdir(directory) if re.search(r'_frame_(\d+)', f)]
    
    # Ordenar archivos por el número al final del nombre
    files.sort(key=lambda x: int(re.search(r'_frame_(\d+)', x).group(1)))
    
    cow_count = 1  # Contador para los diferentes grupos 'cow'
    sequence_count = 1  # Contador para la secuencia dentro de un grupo
    
    # Iterar sobre los archivos
    for i in range(len(files) - 1):
        current_file = files[i]
        next_file = files[i + 1]
        
        # Obtener los números de frame del archivo actual y el siguiente
        current_frame = int(re.search(r'_frame_(\d+)', current_file).group(1))
        next_frame = int(re.search(r'_frame_(\d+)', next_file).group(1))
        
        # Renombrar el archivo actual
        new_name = f"cow{cow_count}_{sequence_count}.jpg"  # Ajusta la extensión según el tipo de archivo
        os.rename(os.path.join(directory, current_file), os.path.join(directory, new_name))
        
        # Si la diferencia es de 5, continuar la secuencia
        if next_frame - current_frame == 5:
            sequence_count += 1
        else:
            # Si la diferencia no es de 5, empezar un nuevo grupo de 'cow'
            cow_count += 1
            sequence_count = 1  # Reiniciar la secuencia para el nuevo grupo
    
    # Renombrar el último archivo
    last_file = files[-1]
    new_name = f"cow{cow_count}_{sequence_count}.jpg"
    os.rename(os.path.join(directory, last_file), os.path.join(directory, new_name))

# Ejemplo de uso:



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
directory = r'C:\Users\Manuel\Desktop\Carpeta Visual\DatasetBarracas6\V3_3_frame'  # Cambia a tu ruta
rename_files(directory)
move_images_to_folders(directory)

# Revisar que no coincidan al final dos vacas!