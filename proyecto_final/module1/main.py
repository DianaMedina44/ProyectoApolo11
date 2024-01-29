import time
import json
import os 
from generateFile import GenerateFile
import logging

# Configurar el sistema de registro
log_file_path = 'repetitive_task.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def cargar_configuracion():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    config_path =os.path.join(script_directory, 'config.json')
    try:
        with open(config_path, 'r') as file:
            configuracion = json.load(file)
        return configuracion
    except FileNotFoundError:
        logging.error("El archivo de configuración no se encuentra. Asegúrate de que 'config.json' esté en la misma carpeta.")
        return {}

def repetitive_task():
    
    script_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_directory, 'config.json')
    """Perform a repetitive task using the GenerateFile class."""
    generator = GenerateFile()
    generator.generate_files(config_file_path)
    

if __name__ == "__main__":
    try:
        while True:
            configuracion = cargar_configuracion()
            intervalo_ejecucion = configuracion.get('intervalo_ejecucion_segundos', 1)
            repetitive_task()
            time.sleep(intervalo_ejecucion)  
    except KeyboardInterrupt:
        logging.info('El programa fue interrumpido por el usuario.')
