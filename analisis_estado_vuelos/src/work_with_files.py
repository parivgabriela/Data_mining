import glob
import pandas as pd
import os

YEAR = 2025

def read_csv_file(filename):
    return pd.read_csv(filename)


def load_data(file_path, **kwargs):
    """
    Load a CSV file or Parquet and return a DataFrame of Pandas.
    :param file_path: str, path to file.
    :param kwargs: Adicional pd.read_csv o pd.read_parquet.
    :return: pd.DataFrame
    """
    _, extension_file = os.path.splitext(file_path)
    extension_file = extension_file.lower()

    try:
        if extension_file == '.csv':
            return pd.read_csv(file_path, **kwargs)
        elif extension_file == '.parquet':
            return pd.read_parquet(file_path, **kwargs)
        else:
            raise ValueError(f"unsupported format: {extension_file}. Use CSV or Parquet.")

    except Exception as e:
        print(f"Error loading file: {e}")
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



