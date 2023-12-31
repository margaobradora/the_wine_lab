#%% 
import pandas as pd
import os
from dotenv import load_dotenv
from word2number import w2n
from src import extraction_support as exsu

#%% 
urls_dict = exsu.obtener_urls_vinissimus()
#%%
ruta_salida = 'listado_urls.csv'
#%%
guardar_urls = exsu.guardar_urls_csv(urls_dict, ruta_salida)
#%%
listado_urls = pd.read_csv("listado_urls.csv")
#%%
urls_list = listado_urls['URL'].tolist()
# %%
resultados = exsu.capturar_info(urls_list)
# %%
nombre_archivo = 'resultados_extraccion_total.csv'
guardar_resultados = exsu.mostrar_y_guardar(resultados, nombre_archivo)
# %%
