import os
import pandas as pd
import shutil
from datetime import datetime
from typing import Any, TextIO, Optional, List
import logging

# Configurar el sistema de registro
logging.basicConfig(level=logging.INFO)  # Puedes cambiar el nivel según tus necesidades

class CreateDataFrame:

    def __init__(self, file_path: str)-> None:    
        """
        Inicializa una instancia de CreateDataFrame.

        Args:
            file_path (str): Ruta del directorio de archivos.

        Returns:
            None
        """    
        self.file_path = file_path
        self.number_folder = file_path.split('\\')[-1].split('_')[-1]
        self.current_directory = os.path.dirname(os.path.abspath(__file__))

    def create_dataframes_folder(self)-> None:
        """Crea la carpeta 'dataframes' si no existe."""
        dataframes_folder = os.path.join(self.current_directory, 'dataframes')
        if not os.path.exists(dataframes_folder):
            os.makedirs(dataframes_folder)
            logging.info("Carpeta dataframe creada")
            
    def move_files_to_backup(self, source_folder: str, backup_folder: str)-> None:
        """Mueve archivos desde la carpeta de origen a la carpeta de respaldo."""
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)
            logging.info("Backup carpeta creada")

        files: List[str] = os.listdir(source_folder)
        for file_name in files:
            source_file: str = os.path.join(source_folder, file_name)
            backup_file: str = os.path.join(backup_folder, file_name)

            try:
                shutil.move(source_file, backup_file)
                logging.info(f"el archivo {file_name} fue movido a carpeta backup.")
            except FileNotFoundError:
                logging.error(f"Error: The file {file_name} not found in the source folder.")
            except Exception as e:
                logging.error(f"Error: Unable to move the file {file_name}. {e}")

    def read_files_from_path(self):
        """Lee los archivos de una ruta y devuelve un DataFrame."""
        # Crear la carpeta 'dataframes' si no existe
        self.create_dataframes_folder()

        # Crear un DataFrame vacío con nombres de columnas
        df_columns: List[str] = ['date', 'mission', 'device_type', 'device_status', 'hash']
        df = pd.DataFrame(columns=df_columns) 

        # Leer los archivos de una ruta
        files:List[str] = os.listdir(self.file_path)

        # Iterar sobre los archivos
        for file in files:
            # Leer el contenido de cada archivo
            file_path: str = os.path.join(self.file_path, file)

            with open(file_path, 'r') as f:
                file_content: str = f.readline()
                # Dividir la cadena por comas y eliminar los espacios en blanco
                key_value_pairs:List[str] = [pair.strip() for pair in file_content.split(',')]

                # Crear un diccionario con los pares key:value
                data_dict: dict = dict(pair.split(': ') for pair in key_value_pairs)

                df = df._append(data_dict, ignore_index=True)
                
                # Obtener la fecha actual en el formato deseado
        current_date: str = datetime.now().strftime("%d%m%y%H%M%S") 
                

        # Guardar el DataFrame como un archivo CSV dentro de la carpeta 'dataframes'
        output_file_path: str = os.path.join(self.current_directory, 'dataframes', f'APLSTATS-[REPORTE]{self.number_folder}-{current_date}.csv')
        df.to_csv(output_file_path, index=False)
        
        # Mover los archivos a la carpeta de respaldo
        backup_folder: str = os.path.join(self.current_directory, 'backup')
        self.move_files_to_backup(self.file_path, backup_folder)


        # Return the DataFrame
        # return df