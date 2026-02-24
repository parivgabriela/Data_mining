import glob
import pandas as pd
import os

YEAR = 2025

def read_csv_file(filename):
    return pd.read_csv(filename)

def load_data(ruta_archivo, **kwargs):
    """
    Carga un archivo CSV o Parquet y devuelve un DataFrame de Pandas.
    :param ruta_archivo: str, camino al archivo.
    :param kwargs: Argumentos adicionales para pd.read_csv o pd.read_parquet.
    :return: pd.DataFrame
    """
    # Extraemos la extensión del archivo
    _, extension = os.path.splitext(ruta_archivo)
    extension = extension.lower()

    try:
        if extension == '.csv':
            return pd.read_csv(ruta_archivo, **kwargs)
        elif extension == '.parquet':
            return pd.read_parquet(ruta_archivo, **kwargs)
        else:
            raise ValueError(f"Formato no soportado: {extension}. Solo CSV o Parquet.")

    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return None

def export_and_unify_files(folder_path, company, format="parquet", prefijo=None):
    # 1. Buscar todos los archivos mensuales'
    patron = "*.csv"
    
    if prefijo:
        patron = f"{prefijo}*.csv"

    archivos = glob.glob(os.path.join(folder_path, patron))
    archivos.sort() # Para mantener el orden cronológico

    lista_dfs = []
    for archivo in archivos:
        print(f"Leyendo: {archivo}")
        df = pd.read_csv(archivo)
        lista_dfs.append(df)

    # 2. Unir todos (pandas ignora los headers repetidos y crea un solo esquema)
    df_final = pd.concat(lista_dfs, ignore_index=True)

    nombre_archivo = f"vuelos_anual_{company}_consolidado_{YEAR}"
    # 3. Exportar según formato
    if format == "csv":
        df_final.to_csv(nombre_archivo + ".csv", index=False)
    elif format == "parquet":
        # Requiere: pip install pyarrow fastparquet
        df_final.to_parquet(nombre_archivo + ".parquet", index=False)
    elif format == "excel":
        df_final.to_excel(nombre_archivo + ".xlsx", index=False)

    print(f"Consolidación exitosa. Filas totales: {len(df_final)}")
    return df_final

def unify_datasets_list(datsets_list, filename):
    df_final = pd.concat(datsets_list, ignore_index=True)
    f_name = f"{filename}.parquet"
    df_final.to_parquet(f_name)
    print("¡Todo unificado y guardado!")



