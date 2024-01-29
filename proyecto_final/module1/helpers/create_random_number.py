import random
import json

def read_config(config_file_path):
    
    try:
        with open(config_file_path, 'r') as file:
            configuracion = json.load(file)
        return configuracion
    except FileNotFoundError:
        print("El archivo de configuración no se encuentra. Asegúrate de que 'config.json' esté en la misma carpeta.")
        return {}

def generate_random_number(config_file_path):
    # Read the configuration from the file
    configuracion = read_config(config_file_path)

    # Extract min_value and max_value from the config
    rango_numeros = configuracion.get("rango_numeros", {"min_value": 1, "max_value": 10})
    min_value = rango_numeros.get("min_value", 1)
    max_value = rango_numeros.get("max_value", 10)
    
    # Generate a random number within the specified range
    return random.randint(min_value, max_value)





