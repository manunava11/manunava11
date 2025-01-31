import cv2
import os
from ultralytics import YOLO
import torch

# Rutas de los archivos
video_input_path = r'C:\Users\Manuel\Desktop\Carpeta Visual\Bovinos\Videos\Bov_4.MP4'
model_folder = r'C:\Users\Manuel\Desktop\Carpeta Visual\Sistema-De-Conteo-De-Ganado\EntrenarYolov8'
output_folder = r'C:\Users\Manuel\Desktop\Carpeta Visual\Bovinos'

# Verificar si CUDA está disponible
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Cargar el modelo YOLO
model = YOLO(os.path.join(model_folder, r'ovejas.pt')).to(device)

# Abrir el video
cap = cv2.VideoCapture(video_input_path)
assert cap.isOpened(), "Error reading video file"

# Obtener propiedades del video
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Inicializar el escritor de video con resolución 600x600
output_video_path = os.path.join(output_folder, "Conteo_Resultante_" + os.path.basename(video_input_path))
video_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (600, 600))

# Variables de conteo
total_count = 0
object_ids = set()

# Procesar el video
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Redimensionar frame a 600x600
    frame = cv2.resize(frame, (600, 600))

    # Realizar la detección de objetos
    results = model.track(frame, persist=True, show=False, conf=0.5, iou=0.6, tracker="botsort.yaml")

    # Revisar cada detección en los resultados
    for detection in results[0].boxes:  # results[0] para acceder a los elementos individuales en la lista
        cls_id = int(detection.cls[0])  # ID de clase

        # Verificar si detection.id es None
        obj_id = int(detection.id[0]) if detection.id is not None else None  # ID del objeto para tracking
        
        # Continuar solo si detection.id no es None
        if cls_id == 0 and obj_id is not None:  # Cambia '0' por el ID de la clase 'cow' en tu modelo
            bbox = detection.xyxy[0]  # Coordenadas del bounding box (x1, y1, x2, y2)

            # Comprobar si el objeto ha cruzado la línea definida
            _, y_center = int((bbox[0] + bbox[2]) / 2), int((bbox[1] + bbox[3]) / 2)  # Centro de la caja
            if y_center > 0 and obj_id not in object_ids:
                object_ids.add(obj_id)
                total_count += 1

            # Dibujar el bounding box y el id en el frame
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)
            cv2.putText(frame, f'ID: {obj_id}', (int(bbox[0]), int(bbox[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Visualización del conteo total en pantalla
    text = f'Conteo total: {total_count}'
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    text_x, text_y = 50, 50
    cv2.rectangle(frame, (text_x - 5, text_y + 5), (text_x + text_size[0] + 5, text_y - text_size[1] - 5), (255, 255, 255), cv2.FILLED)
    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (44, 110, 47), 2, cv2.LINE_AA)

    # Escribir el frame procesado en el video de salida
    video_writer.write(frame)

# Liberar recursos
cap.release()
video_writer.release()
cv2.destroyAllWindows()

print(f"Proceso completado. Total de vacas: {total_count}. Video de salida generado como '{output_video_path}'.")
