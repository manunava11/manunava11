import subprocess
import os

# Ruta completa a ffprobe.exe (modifica según tu instalación)
FFPROBE_PATH = "C:/ffmpeg/ffprobe.exe"
FFMPEG_PATH = "C:/ffmpeg/ffmpeg.exe"

def get_video_resolution(video_path):
    # Comando para obtener la resolución del video usando ffprobe
    cmd = [
        FFPROBE_PATH, '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=s=x:p=0',
        video_path
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        width, height = map(int, result.stdout.strip().split('x'))
        return width, height
    except subprocess.CalledProcessError:
        print("Error al obtener la resolución del video.")
        return None, None
    except FileNotFoundError:
        print("No se encontró ffprobe. Verifica la ruta en FFPROBE_PATH.")
        return None, None

def optimize_video(video_path):
    width, height = get_video_resolution(video_path)
    
    if width == 3840 and height == 2160:
        print("Video 4K detectado. Iniciando optimización...")
        
        # Definir el nombre del video de salida
        output_path = os.path.splitext(video_path)[0] + "_4k_optimized.mp4"
        
        # Comando FFmpeg para ajustar el bitrate a 20 Mbps
        cmd = [
            FFMPEG_PATH, '-i', video_path,
            '-c:v', 'libx264', '-preset', 'slow',
            '-profile:v', 'high', '-level', '5.2',
            '-b:v', '20000k', '-maxrate', '25000k',
            '-bufsize', '50000k',
            '-c:a', 'aac', '-b:a', '192k',
            '-movflags', '+faststart',
            output_path
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"Video optimizado exitosamente: {output_path}")
        except subprocess.CalledProcessError:
            print("Error al optimizar el video.")
        except FileNotFoundError:
            print("No se encontró ffmpeg. Verifica la ruta en FFMPEG_PATH.")
    else:
        print(f"El video no es 4K (resolución detectada: {width}x{height}). No se aplicaron cambios.")

# Verificar si ffprobe está funcionando antes de iniciar el procesamiento
try:
    subprocess.run([FFPROBE_PATH, '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("ffprobe está funcionando correctamente.")
except FileNotFoundError:
    print("Error: ffprobe no está disponible. Verifica la ruta en FFPROBE_PATH.")
    exit(1)

# Ruta del video (modifica esto según la ubicación de tu archivo)
video_path = "C:/Users/Manuel/Downloads/Conteo y Pesaje Novillos Chicos Pasada 3 9.8mts_20250210_142441.MP4"
optimize_video(video_path)
