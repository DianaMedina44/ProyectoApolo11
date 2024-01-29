import os
from create_dataframe import CreateDataFrame
from informes import Informes

def repetitive_task():
    """Perform a repetitive task using the GenerateFile class."""
    # Create an instance of the GenerateFile class
    
    current_directory = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.abspath(os.path.join(current_directory, "../module1/devices"))

    if os.path.exists(file_path):
        # Lista de carpetas en la ruta
        folders = os.listdir(file_path)


        for folder in folders:
            new_file_path = os.path.join(file_path, folder)
            df = CreateDataFrame(new_file_path)
            print(df.read_files_from_path())
            
        ruta_csv = os.path.join(os.path.dirname(__file__), 'dataframes')
        procesador = Informes(ruta_csv)
        
        eventos = procesador.contador_eventos()
        desconexiones = procesador.contador_desconexiones()
        killed = procesador.contador_killed()
        porcentajes = procesador.contador_porcentajes()

        procesador.guardar_json(eventos, 'eventos')
        procesador.guardar_json(desconexiones, 'desconexiones')
        procesador.guardar_json(killed, 'killed')
        procesador.guardar_json(porcentajes, 'porcentajes')
    else:
        print("La ruta no es válida.")
    

if __name__ == "__main__":
    repetitive_task()
