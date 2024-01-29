import pandas as pd
import os
import json
from typing import List, Dict, Union
from dataclasses import dataclass

@dataclass
class Informes:
    def __init__(self, ruta_csv: str,carpeta_informes: str="Informes"):
        """
        Inicia una instancia de la clase Informes.

        Args:
            ruta_csv (str): Ruta del directorio que contiene archivos CSV.
            carpeta_informes (str, optional): Nombre de la carpeta para almacenar informes. Por defecto, "Informes".

        Returns:
            None
        """
        self.ruta_csv: str = ruta_csv
        self.carpeta_informes: str = carpeta_informes
        self.dataframes: List[pd.DataFrame] = self.leer_dataframes()
        
        # Crear la carpeta de informes si no existe
        self.crear_carpeta_informes()

    def leer_dataframes(self)-> List[pd.DataFrame]:
        """
        Lee los archivos CSV de la ruta especificada y devuelve una lista de DataFrames.

        Returns:
            List[pd.DataFrame]: Lista de DataFrames creados a partir de archivos CSV.
        """
        archivos_csv:List[str] = sorted([archivo for archivo in os.listdir(self.ruta_csv) if archivo.endswith('.csv')])
        dataframes:List[pd.DataFrame]  = []

        for archivo in archivos_csv:
            ruta_completa: str = os.path.join(self.ruta_csv, archivo)
            # Utilizar read_csv con el delimitador y otros parámetros apropiados para archivos .log
            df = pd.read_csv(ruta_completa)
            dataframes.append(df)

        return dataframes
    
    def crear_carpeta_informes(self)-> None:
        """
        Crea la carpeta 'informes' en la ruta especificada si no existe.

        Returns:
            None
        """
        ruta_informes: str = os.path.join(self.ruta_csv, 'informes')
        if not os.path.exists(ruta_informes):
            os.makedirs(ruta_informes)
        
        

    def contador_eventos(self)-> List[pd.DataFrame]:
        """
        Calcula y devuelve informes de eventos por misión, tipo de dispositivo y estado de dispositivo.

        Returns:
            List[pd.DataFrame]: Lista de DataFrames con informes de eventos.
        """
        informes: List[pd.DataFrame] = []
        for i, df in enumerate(self.dataframes):
            eventos_por_mision_dispositivo = df.groupby(['mission', 'device_type', 'device_status']).size().reset_index(name='event_count')
            informes.append(eventos_por_mision_dispositivo)
        return informes 

    def contador_desconexiones(self)-> List[pd.DataFrame]:
        """
        Calcula y devuelve informes de desconexiones por misión y tipo de dispositivo.

        Returns:
            List[pd.DataFrame]: Lista de DataFrames con informes de desconexiones.
        """
        informes: List[pd.DataFrame] = []
        for i, df in enumerate(self.dataframes):
            unknown_events = df[df['device_status'].eq('unknown') & (df['device_type'] != 'unknown')]
            device_unknown_counts = unknown_events.groupby(['mission','device_type']).size().reset_index(name='unknown_event_count')
            device_unknown_counts =device_unknown_counts.sort_values(by='unknown_event_count', ascending=False)
            informes.append(device_unknown_counts)
            
        return informes 
            
    def contador_killed(self) -> List[pd.Series]:
        """
        Calcula y devuelve informes de dispositivos inoperables.

        Returns:
            List[pd.Series]: Lista de Series con informes de dispositivos inoperables.
        """
        informes: List[pd.Series] = []
        for i, df in enumerate(self.dataframes):
            inoperable_devices = df[df['device_status'].isin(['killed'])]
            inoperable_device_counts = inoperable_devices.groupby('device_type').size() 
            informes.append(inoperable_device_counts)
            
        return informes 
    
    def contador_porcentajes(self)-> List[List[Dict[str, Union[str, float]]]]:
        """
        Calcula y devuelve informes de porcentajes de misiones y tipos de dispositivo.

        Returns:
            List[List[Dict[str, Union[str, float]]]]: Lista de informes de porcentajes.
        """
        informes: List[List[Dict[str, Union[str, float]]]]  = []
        for i, df in enumerate(self.dataframes):
            porcentaje_mision: Dict[str, float] = (df['mission'].value_counts(normalize=True) * 100).round(1).to_dict()
            porcentaje_dispositivo: Dict[str, float] = (df['device_type'].value_counts(normalize=True) * 100).round(1).to_dict()
            informes.append([porcentaje_dispositivo, porcentaje_mision])
            
        return informes
    
    def guardar_json(self, informes: List[Union[pd.DataFrame, pd.Series, List[Dict[str, Union[str, float]]]]], nombre_archivo: str)-> None:
        """
        Guarda los informes en un archivo JSON en la carpeta de informes.

        Args:
            informes (List[Union[pd.DataFrame, pd.Series, List[Dict[str, Union[str, float]]]]]): Lista de informes.
            nombre_archivo (str): Nombre del archivo JSON.

        Returns:
            None
        """
        ruta_guardado = os.path.join(self.ruta_csv, self.carpeta_informes, f"{nombre_archivo}.json")
    
        # Crear la carpeta 'informes' si no existe
        if not os.path.exists(os.path.join(self.ruta_csv, self.carpeta_informes)):
            os.makedirs(os.path.join(self.ruta_csv, self.carpeta_informes))
    
        # Convertir el DataFrame a un formato serializable (en este caso, a una lista de diccionarios)
        informes_serializables: List[List[Dict[str, Union[str, float]]]] = []
        for informe in informes:
            if isinstance(informe, pd.DataFrame):
                informes_serializables.append(informe.reset_index().to_dict(orient='records'))
            elif isinstance(informe, pd.Series):
                informes_serializables.append(informe.reset_index().to_dict())
            elif isinstance(informe, list):
                informes_serializables.append(informe)
            else:
            # Manejar otros tipos de datos según sea necesario
                pass
    

        with open(ruta_guardado, 'w') as f:
            json.dump(informes_serializables, f, indent=4)

        print(f"Resultados guardados en: {ruta_guardado}")
            
ruta_csv =os.path.join(os.path.dirname(__file__), 'dataframes')
procesador = Informes(ruta_csv)
eventos=procesador.contador_eventos()
desconexiones=procesador.contador_desconexiones()
killed=procesador.contador_killed()
porcentajes=procesador.contador_porcentajes()

procesador.guardar_json(eventos, 'eventos')
procesador.guardar_json(desconexiones, 'desconexiones')
procesador.guardar_json(killed, 'killed')
procesador.guardar_json(porcentajes, 'porcentajes')



