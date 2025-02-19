import os
import glob
import torch
import ultralytics


def check_cuda():
    print("PyTorch version:", torch.__version__)
    print("CUDA version:", torch.version.cuda)
    print("YOLO version:", ultralytics.__version__)
    print("Is CUDA available?", torch.cuda.is_available())

def check_labels_only_class_0(dataset_path):
    label_dirs = ["train/labels", "val/labels"]
    
    for label_dir in label_dirs:
        full_path = os.path.join(dataset_path, label_dir)
        if not os.path.exists(full_path):
            print(f"Directorio no encontrado: {full_path}")
            continue
        
        print(f"Revisando: {full_path}")
        
        for label_file in glob.glob(os.path.join(full_path, "*.txt")):
            with open(label_file, "r") as f:
                for line in f:
                    values = line.strip().split()
                    if len(values) == 0:
                        continue  # Saltar líneas vacías
                    class_id = values[0]
                    if class_id != "0":
                        print(f"Error en {label_file}: Clase no permitida {class_id}")
    
    print("Verificación completada.")

def verify_labels():
    dataset_path = "C:/Users/Manuel/Desktop/Carpeta Visual/Bovinos/Dataset"
    for label_file in glob.glob(dataset_path + "/val/labels/*.txt"):
        with open(label_file, "r") as f:
            for line in f:
                values = line.strip().split()
                if not values or not values[0].isdigit():
                    print(f"Archivo con datos inválidos: {label_file}")

# Uso
ruta_dataset = r"C:\Users\Manuel\Desktop\Carpeta Visual\Bovinos\Dataset"  # Reemplaza con la ruta correcta
#check_labels_only_class_0(ruta_dataset)
verify_labels()