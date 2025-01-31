import os
import re

def reformatear_nombres_carpetas(ruta_principal):
    """
    Reformatea nombres de carpetas en la ruta principal.
    Si el nombre contiene 'cow', conserva todo a partir de 'cow'.
    """
    for carpeta in os.listdir(ruta_principal):
        carpeta_path = os.path.join(ruta_principal, carpeta)

        # Verificar si es una carpeta
        if os.path.isdir(carpeta_path):
            # Buscar la palabra 'cow' en el nombre
            match = re.search(r'(cow.*)', carpeta, re.IGNORECASE)
            if match:
                nuevo_nombre = match.group(1)  # Extraer la parte del nombre a partir de 'cow'
                nuevo_nombre_path = os.path.join(ruta_principal, nuevo_nombre)

                # Renombrar si el nombre es diferente
                if carpeta != nuevo_nombre:
                    os.rename(carpeta_path, nuevo_nombre_path)
                    print(f"Renombrado: '{carpeta}' -> '{nuevo_nombre}'")
    print("Renombrado inicial completado.")

def hacer_numeros_continuos(ruta_principal, prefix="cow"):
    """
    Renombra carpetas con nombres tipo 'Cow121' o 'cow519_V6_1_frame' para que los números sean continuos.
    """
    # Función para extraer el número después del prefijo 'cow'
    def extract_number(nombre):
        match = re.match(rf"{prefix}(\d+)", nombre, re.IGNORECASE)
        return int(match.group(1)) if match else None

    # Obtener y ordenar carpetas por su número
    carpetas = sorted(
        [c for c in os.listdir(ruta_principal) if os.path.isdir(os.path.join(ruta_principal, c))],
        key=lambda x: extract_number(x) if extract_number(x) is not None else float("inf")
    )

    # Renombrar carpetas para hacer números continuos
    expected_number = 1
    for carpeta in carpetas:
        carpeta_path = os.path.join(ruta_principal, carpeta)
        current_number = extract_number(carpeta)

        if current_number is not None and current_number != expected_number:
            # Mantener el resto del nombre después del número
            resto_nombre = carpeta[len(f"{prefix}{current_number}"):]  # Extraer lo que sigue después del número
            nuevo_nombre = f"{prefix}{expected_number}{resto_nombre}"
            nuevo_path = os.path.join(ruta_principal, nuevo_nombre)

            # Renombrar la carpeta
            os.rename(carpeta_path, nuevo_path)
            print(f"Renombrado: '{carpeta}' -> '{nuevo_nombre}'")

        # Incrementar el número esperado
        expected_number += 1

    print("Numeración continua completada.")

# Parámetros
ruta_principal = r"C:\Users\Manuel\Desktop\Carpeta Visual\DatasetElOmbuss\DatasetElOmbu"  # Ruta principal

# Ejecutar funciones
reformatear_nombres_carpetas(ruta_principal)
hacer_numeros_continuos(ruta_principal)
