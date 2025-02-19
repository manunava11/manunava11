import os
import re

def rename_folders(directory):
    for folder in os.listdir(directory):
        folder_path = os.path.join(directory, folder)
        
        if os.path.isdir(folder_path):  # Verifica que sea una carpeta
            match = re.match(r"(cow\d+)_.*", folder)
            if match:
                new_name = match.group(1)
                new_path = os.path.join(directory, new_name)
                
                if not os.path.exists(new_path):  # Evita sobrescribir carpetas
                    os.rename(folder_path, new_path)
                    print(f"Renombrado: {folder} -> {new_name}")
                else:
                    print(f"No se pudo renombrar {folder}, {new_name} ya existe.")

# Usar la función
ruta_principal = r"C:\Users\Manuel\Desktop\Carpeta Visual\GordasCutoff"  # Ruta principal
rename_folders(ruta_principal)
