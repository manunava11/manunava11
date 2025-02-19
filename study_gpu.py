import torch
import subprocess
import re

def get_gpu_info():
    if torch.cuda.is_available():
        device = torch.device("cuda")
        props = torch.cuda.get_device_properties(device)

        gpu_name = props.name
        vram_total = props.total_memory / 1e9  # Convertir a GB (más preciso)
        vram_allocated = torch.cuda.memory_allocated(device) / 1e9  # Memoria en uso por PyTorch
        vram_reserved = torch.cuda.memory_reserved(device) / 1e9  # Memoria reservada por PyTorch

        # Obtener memoria libre real desde nvidia-smi
        try:
            result = subprocess.run(["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
                                    capture_output=True, text=True)
            vram_free = float(result.stdout.strip()) / 1024  # Convertir MB a GB
        except Exception:
            vram_free = "No disponible"

        sm_count = props.multi_processor_count  # Número de multiprocesadores

        # CUDA Cores por SM para diferentes arquitecturas
        cuda_cores_per_sm = {
            "Turing": 64,  # RTX 20XX
            "Ampere": 128,  # RTX 30XX
            "Ada": 128  # RTX 40XX
        }

        architecture = "Ampere"  # RTX 3090 usa Ampere
        cuda_cores = sm_count * cuda_cores_per_sm.get(architecture, 128)

        # Obtener la frecuencia de la GPU con nvidia-smi
        try:
            result = subprocess.run(["nvidia-smi", "--query-gpu=clocks.sm", "--format=csv,noheader,nounits"],
                                    capture_output=True, text=True)
            clock_speed = int(result.stdout.strip())  # Convertir a MHz
        except Exception:
            clock_speed = "No disponible"

        print(f"GPU: {gpu_name}")
        print(f"Memoria VRAM Total: {vram_total:.2f} GB")
        print(f"Memoria VRAM Libre (real): {vram_free} GB")
        print(f"Memoria VRAM Reservada por PyTorch: {vram_reserved:.2f} GB")
        print(f"Memoria VRAM en Uso por PyTorch: {vram_allocated:.2f} GB")
        print(f"Núcleos CUDA: {cuda_cores}")
        print(f"Frecuencia de la GPU: {clock_speed} MHz")
    else:
        print("No se detectó una GPU con soporte CUDA.")

get_gpu_info()
