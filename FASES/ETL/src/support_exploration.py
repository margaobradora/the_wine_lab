#%%
import pandas as pd
import os
import sys

pd.set_option('display.max_columns', None) # para poder visualizar todas las columnas de los DataFrames

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
