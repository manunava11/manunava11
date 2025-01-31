# Import necessary libraries again due to environment reset
import numpy as np
import matplotlib.pyplot as plt

# Parámetros
FOV = 82.1  # Field of View en grados
h_min = 0  # Altura mínima en metros
h_max = 50  # Altura máxima en metros
n_points = 500  # Número de puntos para la gráfica

# Convertir FOV a radianes
FOV_rad = np.radians(FOV)

# Calcular la superficie cubierta en función de la altura
alturas = np.linspace(h_min, h_max, n_points)
anchura_cubierta = 2 * (alturas * np.tan(FOV_rad / 2))  # Ancho de la imagen a distintas alturas
superficie_cubierta = np.pi * (anchura_cubierta / 2) ** 2  # Superficie en metros cuadrados

# Graficar la superficie cubierta
plt.figure(figsize=(8, 6))
plt.plot(alturas, superficie_cubierta, label='Superficie cubierta')
plt.title('Relación entre la altura del dron y la superficie cubierta')
plt.xlabel('Altura (m)')
plt.ylabel('Superficie cubierta (m²)')
plt.grid(True)
plt.legend()
plt.show()
