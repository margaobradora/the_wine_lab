#%% 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import requests as re
import os
import sys


#%% 

def obtener_ruta_files():
    # Obtiene la ruta del directorio donde se ejecuta este script
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_files = os.path.join(ruta_actual, 'Files')
    
    # Verifica si la carpeta 'Files' no existe y la crea si es necesario
    if not os.path.exists(ruta_files):
        os.makedirs(ruta_files)
    
    return ruta_files

#%% 
def cargar_y_mostrar_datos(nombre_archivo):
    try:
        # Obtiene la ruta actual
        ruta_files = obtener_ruta_files()
        
        # Construye la ruta completa del archivo a partir de la ruta actual y el nombre del archivo
        ruta_archivo = os.path.join(ruta_files, nombre_archivo)
        
        # Leer archivo especificado por 'nombre_archivo'
        datos = pd.read_csv(ruta_archivo)
        
        # Mostrar todas las columnas del DataFrame
        pd.set_option('display.max_columns', None)
        
        # Leer archivo usando la variable 'nombre_archivo'
        df = pd.read_csv(nombre_archivo, index_col=0)
        
        # Mostrar datos del archivo 'nombre_archivo'
        print(f"Datos del archivo {nombre_archivo}:")
        print(df.head())  # Puedes cambiar esto a lo que necesites hacer con estos datos
        
        # Retornar los datos leídos por si se necesitan más adelante
        return datos
        
    except FileNotFoundError as e:
        print(f"No se pudo encontrar el archivo: {e}")
        return None


# %%
def exploracion_csv(dataframe):
    print(f"Los duplicados que tenemos en el conjunto de datos son: {dataframe.duplicated().sum()}")
    print("\n ..................... \n")
    # generamos un DataFrame para los valores nulos
    print("Los nulos que tenemos en el conjunto de datos son:")
    df_nulos = pd.DataFrame(dataframe.isnull().sum() / dataframe.shape[0] * 100, columns = ["%_nulos"])
    display(df_nulos[df_nulos["%_nulos"] > 0])
    print("\n ..................... \n")
    print(f"Los tipos de las columnas son:")
    display(pd.DataFrame(dataframe.dtypes, columns = ["tipo_dato"]))
    print("\n ..................... \n")
    print("Los valores que tenemos para las columnas categóricas son: ")
    dataframe_categoricas = dataframe.select_dtypes(include = "O")
    for col in dataframe_categoricas.columns:
        print(f"La columna {col.upper()} tiene las siguientes valores únicos:")
        display(pd.DataFrame(dataframe[col].value_counts()).head())
    print("Los valores que tenemos para las columnas numéricas son: ")
    dataframe_numericas = dataframe.select_dtypes(exclude='O')
    try:
        print("\n ..................... \n")
        print(f"Los principales estadísticos de las columnas categóricas son: ")
        display(dataframe_categoricas.describe(include = "O").T)
    except:
        print('No hay columnas categóricas')
    try:
        print("\n ..................... \n")
        print(f"Los principales estadísticos de las columnas numéricas son: ")
        display(dataframe_numericas.describe().T)
    except:
        print('No hay columnas numéricas')

# %%
