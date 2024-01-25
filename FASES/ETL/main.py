#%% 
import pandas as pd
import os
from dotenv import load_dotenv
from word2number import w2n
from dotenv import load_dotenv
from src import extraction_support as exsu
from src import eda_support as eda

## empezamos con la parte de EXTRACTION support 
#%% 
urls_dict = exsu.obtener_urls_vinissimus()
#%%
ruta_salida = 'listado_urls_2.csv'
#%%
guardar_urls = exsu.guardar_urls_csv(urls_dict, ruta_salida)
#%%
listado_urls = pd.read_csv(ruta_salida)
#%%
urls_list = listado_urls['URL'].tolist()
# %%
resultados = exsu.capturar_info(urls_list)
# %%
nombre_archivo = 'resultados_extraccion_total_2.csv'
# %%
dataframe_resultante = exsu.mostrar_y_guardar(resultados, nombre_archivo)


## EMPEZAMOS CON LA PARTE DE EDA SUPPORT 
# %%
# Uso de la función para cargar y mostrar datos
load_dotenv("src/.env")

# %%
#ruta_files = eda.obtener_ruta_files()
# %%
#datos_cargados = eda.cargar_y_mostrar_datos(nombre_archivo)
# %%
explore_csv = eda.exploracion_csv(dataframe_resultante)
# %%
