import os
from pathlib import Path
from ultralytics import YOLO
import cv2
import torch

# Parámetros configurables
input_folder = r'C:\Users\Manuel\Desktop\Carpeta Visual\Gordas\dou'
output_folder = r'C:\Users\Manuel\Desktop\Carpeta Visual\DataGordas'
model_path = r'C:\Users\Manuel\Desktop\Carpeta Visual\Sistema-De-Conteo-De-Ganado\EntrenarYolov8\v11l_ft_detection_model.pt'
PERSISTENCE_THRESHOLD = 7  # Frames mínimos para validar una detección
start_id = 58  # Número inicial para los videos generados

# Configuración del modelo y dispositivo
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = YOLO(model_path).to(device)

# Crear la carpeta de salida si no existe
Path(output_folder).mkdir(parents=True, exist_ok=True)

# Obtener lista de videos en la carpeta de entrada y ordenarlos
video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
video_files = sorted(
    [f for f in os.listdir(input_folder) if any(f.lower().endswith(ext) for ext in video_extensions)],
    key=lambda x: int(x.split("V")[1].split("_")[0])  # Extraer el número después de 'V' y antes de '_'
)

# Variables globales
global_cow_id = start_id  # Contador global para track_ids asignados manualmente
track_id_map = {}  # Mapeo de track_id originales a global_cow_id

# Procesar cada video
for file_name in video_files:
    file_path = os.path.join(input_folder, file_name)

    # Abrir el video
    video_capture = cv2.VideoCapture(file_path)
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Procesando {file_name}: {frame_count} frames, {fps} FPS")

    # Variables locales para seguimiento
    cow_persistence = {}  # Persistencia por track_id
    cow_videos = {}  # VideoWriter por track_id

    frame_idx = 0
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break

        # Redimensionar el frame (opcional)
        resized_frame = cv2.resize(frame, (width, height))

        # Realizar detección con tracking habilitado
        results = model.track(source=resized_frame, persist=True, conf=0.7, iou=0.5)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                track_id = int(box.id[0]) if box.id is not None else None

                if track_id is not None:
                    # Asignar un global_cow_id si el track_id no tiene uno
                    if track_id not in track_id_map:
                        track_id_map[track_id] = global_cow_id
                        global_cow_id += 1

                    assigned_id = track_id_map[track_id]  # Obtener el global_cow_id asignado

                    # Incrementar persistencia
                    cow_persistence[assigned_id] = cow_persistence.get(assigned_id, 0) + 1

                    # Crear video si alcanza el umbral de persistencia
                    if cow_persistence[assigned_id] == PERSISTENCE_THRESHOLD:
                        cow_output_path = os.path.join(output_folder, f"cow{assigned_id}_{file_name}")
                        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                        cow_videos[assigned_id] = cv2.VideoWriter(cow_output_path, fourcc, fps, (width, height))
                        print(f"Creado video para Cow {assigned_id}: {cow_output_path}")

                    # Guardar frame en el video correspondiente
                    if assigned_id in cow_videos:
                        cow_videos[assigned_id].write(resized_frame)

        # Reducir persistencia de vacas no detectadas en este frame
        detected_ids = [int(box.id[0]) for box in result.boxes if box.id is not None]
        for cow_id in list(cow_persistence.keys()):
            if cow_id not in [track_id_map.get(d_id, None) for d_id in detected_ids]:
                cow_persistence[cow_id] -= 1
                if cow_persistence[cow_id] <= 0:
                    # Finalizar video si la vaca desaparece
                    if cow_id in cow_videos:
                        cow_videos[cow_id].release()
                        del cow_videos[cow_id]
                    del cow_persistence[cow_id]

        frame_idx += 1
        if frame_idx % 100 == 0:
            print(f"Procesados {frame_idx}/{frame_count} frames")

    # Liberar recursos
    video_capture.release()
    for writer in cow_videos.values():
        writer.release()

    print(f"Procesado completado para {file_name}. Videos generados en: {output_folder}")

print("Proceso completado.")
