import os
from typing import Optional
import logging

class GenerateFolder:
    """Clase para manejar la generación de carpetas."""

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    @staticmethod
    def generate_folder()-> Optional[str]:
        """Genera una carpeta y devuelve su ruta.

        Returns:
            str: La ruta de la carpeta generada.
        """
        number_folder = 0

        current_directory = os.path.dirname(os.path.abspath(__file__))
        path_folder = os.path.join(current_directory, "devices")

        if not os.path.exists(path_folder):
            devices_directory = GenerateFolder._create_folder(path_folder, number_folder)
            return devices_directory
        else:
            devices_directory = GenerateFolder._create_next_folder(path_folder)
            return devices_directory

    @staticmethod
    def _create_folder(path_folder: str, number_folder: int)-> str:
        """Crea una carpeta con un número especificado y devuelve su ruta.

        Args:
            path_folder (str): La ruta de la carpeta padre.
            number_folder (int): El número que se incluirá en el nombre de la nueva carpeta.

        Returns:
            str: La ruta de la carpeta creada.
        """
        devices_directory = os.path.join(path_folder, f"folder_{number_folder}")
        os.makedirs(devices_directory)
        GenerateFolder.logger.info(f"The folder was created: folder_{number_folder}")
        return devices_directory

    @staticmethod
    def _create_next_folder(path_folder: str)-> str:
        """Crea la siguiente carpeta en una secuencia y devuelve su ruta.

        Args:
            path_folder (str): La ruta de la carpeta padre.

        Returns:
            str: La ruta de la carpeta creada.
        """
        files = os.listdir(path_folder)

        if len(files) == 0:
            return GenerateFolder._create_folder(path_folder, 0)
        else:
            latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(path_folder, x)))
            number_folder = int(latest_file.split("_")[-1]) + 1
            devices_directory = GenerateFolder._create_folder(path_folder, number_folder)
            return devices_directory
