import os
import random
from generateFolder import GenerateFolder
from helpers.create_random_number import generate_random_number
from helpers.generate_hash import generate_hash
from status import mission, device_type, device_status
from datetime import datetime
from typing import Any, TextIO, Optional, List





class GenerateFile:
    """Clase para la generación de archivos con información específica."""

    def __init__(self) -> None:
        """Inicializa una instancia de GenerateFile."""
        pass

    def generate_files(self, config_file_path: str)-> None:
        """Genera archivos basados en información aleatoria y los almacena en un directorio específico.

        Args:
            config_file_path (str): La ruta del archivo de configuración.

        Returns:
            None
        """
        devices_directory = GenerateFolder.generate_folder()

        if devices_directory:
            random_number = generate_random_number(config_file_path)

            for i in range(random_number):
                self._generate_file(devices_directory, i)

    def _generate_file(self, devices_directory: str, index: int)-> None:
        """Genera un archivo con información específica.

        Args:
            devices_directory (str): El directorio donde se creará el archivo.
            index (int): El índice utilizado para formatear el nombre del archivo.

        Returns:
            None
        """
        mission_random = random.choice(mission)
        device_type_random = random.choice(device_type)
        device_status_random = random.choice(device_status)

        formatted_number = str(index).zfill(3)

        file_path = os.path.join(devices_directory, f"APL[{mission_random}]-[{formatted_number}].log")

        with open(file_path, "w") as file:
            if mission_random == 'UNKN':
                self._write_unknown_data(file)
            else:
                self._write_formatted_data(file, mission_random, device_type_random, device_status_random)
                
        
        
    def _write_unknown_data(self, file)-> None:
        """Escribe datos desconocidos en el archivo.

        Args:
            file: El objeto de archivo para escribir los datos.

        Returns:
            None
        """
        date_info = datetime.now()
        mission_info = 'unknown'
        device_type_info = 'unknown'
        device_status_info = 'unknown'
        hashed_info = 'unknown'
        date_info_str = date_info.strftime("%d%m%y/%H%M%S")

        self._write_data_to_file(file, date_info_str, mission_info, device_type_info, device_status_info, hashed_info)

    def _write_formatted_data(self, file, mission_info: str, device_type_info: str, device_status_info: str)-> None:
        """Escribe datos formateados en el archivo.

        Args:
            file: El objeto de archivo para escribir los datos.
            mission_info (str): Información sobre la misión.
            device_type_info (str): Información sobre el tipo de dispositivo.
            device_status_info (str): Información sobre el estado del dispositivo.

        Returns:
            None
        """
        date_info = datetime.now()
        date_info_str = date_info.strftime("%d%m%y/%H%M%S")
        hashed_info = generate_hash(date_info, mission_info, device_type_info, device_status_info)

        self._write_data_to_file(file, date_info_str, mission_info, device_type_info, device_status_info, hashed_info)

    def _write_data_to_file(self, file, date_info_str: str, mission_info: str, device_type_info: str, device_status_info: str, hashed_info: str) -> None:
        """Escribe datos en el archivo.

        Args:
            file: El objeto de archivo para escribir los datos.
            date_info_str (str): Información de fecha formateada.
            mission_info (str): Información sobre la misión.
            device_type_info (str): Información sobre el tipo de dispositivo.
            device_status_info (str): Información sobre el estado del dispositivo.
            hashed_info (str): Información obtenida al generar un hash.

        Returns:
            None
        """
        file.write(f"date: {date_info_str}, mission: {mission_info}, device_type: {device_type_info}, "
                   f"device_status: {device_status_info}, hash: {hashed_info}\n")
