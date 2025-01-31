import os

# Directorio que contiene las etiquetas
labels_dir = r'C:\Users\Manuel\Desktop\UltimoTrain\val'

# Contador de instancias
total_instances = 0

# Iterar sobre los archivos .txt en la carpeta
for label_file in os.listdir(labels_dir):
    if label_file.endswith('.txt'):
        file_path = os.path.join(labels_dir, label_file)
        # Contar las líneas en cada archivo (cada línea es una instancia)
        with open(file_path, 'r') as f:
            instances_in_file = len(f.readlines())
            total_instances += instances_in_file

labels_dir = r'C:\Users\Manuel\Desktop\UltimoTrain\train'


# Iterar sobre los archivos .txt en la carpeta
for label_file in os.listdir(labels_dir):
    if label_file.endswith('.txt'):
        file_path = os.path.join(labels_dir, label_file)
        # Contar las líneas en cada archivo (cada línea es una instancia)
        with open(file_path, 'r') as f:
            instances_in_file = len(f.readlines())
            total_instances += instances_in_file

print(f"Total de instancias en el dataset: {total_instances}")
