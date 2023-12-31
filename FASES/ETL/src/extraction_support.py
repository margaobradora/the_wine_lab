#%% 
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import csv
import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
#%% 

def obtener_urls_vinissimus():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)  
    driver.maximize_window()
    driver.get("https://www.vinissimus.com/es/")

    try:
        cookie_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/button[2]")
        cookie_button.click()
        print("Cookies aceptadas")
    except NoSuchElementException:
        print("No se encontró el botón de cookies")

    driver.find_element(By.XPATH, "/html/body/nav/ul/li[1]/a").click()
    print("Accediendo a Vinos")

    driver.find_element(By.XPATH, "/html/body/div/main/div/section/div[1]/button[2]").click()
    print("Accediendo a vinos españoles")

    dict_urls = {"urls": {}}
    num_paginas = 25
    buttons_to_iterate = 4

    for page in range(2, num_paginas + 2):
        try:
            close_button = driver.find_element(By.XPATH, '/html/body/div[3]/div/h4/span')
            close_button.click()
            print("Popup cerrado")
            driver.implicitly_wait(5)  
        except NoSuchElementException:
            pass

        if page <= buttons_to_iterate:
            xpath = f'//*[@id="__next"]/main/div[2]/section/nav/button[{page}]'
        else:
            xpath = '//*[@id="__next"]/main/div[2]/section/nav/button[5]'

        try:
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            button.click()

            enlaces_vinos = driver.find_elements(By.XPATH, '//div[contains(@class, "details")]/a')

            for index, enlace in enumerate(enlaces_vinos, start=1):
                try:
                    wine_url = enlace.get_attribute('href')
                    dict_urls['urls'][f"Page_{page}_Wine_{index}"] = wine_url
                    print(f"URL del vino en la página {page} - Wine_{index}: {wine_url}")
                except NoSuchElementException:
                    print(f"No se pudo obtener la URL para el enlace {index} en la página {page}")

        except Exception as e:
            print(f"No se pudo acceder a la página {page}: {str(e)}")

    driver.quit()
    return dict_urls


#%%
def guardar_urls_csv(dict_urls, ruta_salida):
    # Extraer solo los valores del diccionario y guardarlos en una lista
    urls_list = list(dict_urls.get('urls', {}).values())

    # Guardar la lista de URLs en un archivo CSV
    with open(ruta_salida, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['URL'])  # Encabezado de la columna

        for url in urls_list:
            writer.writerow([url])

    print(f"Las URLs se han guardado correctamente en '{ruta_salida}'")

#%%

def capturar_info(urls_list):
    dict_results = {
        "name_w": [], "year_w": [], "price": [], "user_score": [], "type_w": [], "region": [], 
        "alcohol_content": [], "wine_grape": [], "pk_score": [], "pn_score": [],
        "sk_score":[]
    }

    for url in urls_list:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')


    #------------ NAME of wine :
                
                name_w = soup.find('h1').get_text()
                dict_results['name_w'].append(name_w)
                print(f"Título de la página ({url}): {name_w}")

    #------------ YEAR of wine :
                
                year_w = soup.find('span', class_='heading fs-2em').text if soup.find('span', class_='heading fs-2em') else "No se encontró el elemento year"
                dict_results['year_w'].append(year_w)

    #------------ PRICE of wine :
                
                price = soup.find('p', class_='price uniq large').text if soup.find('p', class_='price uniq large') else "No se encontró el elemento price"
                dict_results['price'].append(price)

    #------------ USER SCORE:
                
                user_score = soup.find('span', class_='styles_grade__EU5A1').text if soup.find('span', class_='styles_grade__EU5A1') else "No se encontró el elemento user_score"
                dict_results['user_score'].append(user_score) 

    #------------ TYPE of wine:
                
                # Encontrar la tabla con la clase especificada
                tabla = soup.find('table', class_='styles_table__jWPKo info-grid technical-info')

                if tabla:
                    # Encontrar el primer elemento 'td' dentro de la tabla
                    primer_td = tabla.find('td')
                    
                    if primer_td:
                        # Extraer el texto del primer 'td' (puede ser un enlace 'a' o texto plano)
                        type_w = primer_td.get_text(strip=True)
                        print(type_w)
                        dict_results["type_w"].append(type_w)
                    else:
                        print("No se encontró el elemento 'td' dentro de la tabla")
                else:
                    print("No se encontró la tabla con la clase especificada")


    #------------ REGION:
                    
                # Encontrar el div con la clase 'region with link'
                div_region = soup.find('div', class_='region with-link')

                if div_region:
                    # Encontrar el primer elemento 'a' dentro del div
                    region = div_region.find('a')
                    
                    if region:
                        # Imprimir el texto del primer 'a' dentro del div
                        dict_results['region'].append(region.text) 
                        print(region.text)
                    else:
                        print("No se encontró el elemento 'a' dentro del div con clase 'region with link'")
                else:
                    print("No se encontró el div con clase 'region with link'")

    #------------ ALCOHOL content:
                    

                # Encontrar la tabla con la clase especificada
                table_info = soup.find('table', class_='styles_table__jWPKo info-grid technical-info')

                if table_info:
                    # Encontrar todos los elementos 'tr' dentro de la tabla
                    rows = table_info.find_all('tr')
                    
                    # Verificar si hay suficientes filas antes de intentar acceder al sexto tr
                    if len(rows) >= 6:
                        sexto_tr = rows[5]  # El índice 5 corresponde al sexto elemento (el índice inicia en 0)
                        
                        # Encontrar el primer elemento 'td' dentro del sexto 'tr'
                        tds = sexto_tr.find_all('td')
                        
                        if len(tds) > 0:
                            texto_alcohol_content = tds[0].get_text(strip=True)  # Obtener el texto del primer 'td'
                            dict_results['alcohol_content'].append(texto_alcohol_content)
                        else:
                            dict_results['alcohol_content'].append('NA')  # Agregar 'NA' si no se encontraron elementos 'td' dentro del sexto 'tr'
                    else:
                        print("No hay suficientes filas para acceder al sexto tr")
                        dict_results['alcohol_content'].append('NA')
                else:
                    print("No se encontró la tabla con la clase especificada")
                    dict_results['alcohol_content'].append('NA')




    #------------ Wine Grape:
                div_alcohol = soup.find('div', class_='tags with-link')
                
                if div_alcohol:
                    wine_grape = div_alcohol.find('a')

                    if wine_grape:
                        dict_results['wine_grape'].append(wine_grape.text)
                    else: 
                        print("No hay info de uva")
                        dict_results['wine_grape'].append("NA")

                else:
                    print("no hay div de uva")

    #------------ PK score 
                tabla = soup.find('table', class_='styles_table__jWPKo info-grid score-awards')

                if tabla:
                    filas = tabla.find_all('tr')
                    
                    found_score = ""  # Valor por defecto si no se encuentra la puntuación
                    
                    for fila in filas:
                        td_parker = fila.find('td', title='Parker')
                        if td_parker and td_parker.get_text(strip=True) != '':
                            found_score = td_parker.get_text(strip=True)
                            break  # Terminar el bucle después de encontrar el primer valor
                    
                    # Agregar 'NA' si el valor es vacío
                    dict_results['pk_score'].append(found_score if found_score else "NA")
                    print(f"El primer valor de Parker es: {found_score}")
                else:
                    print("No se encontró la tabla con la clase especificada")
                    dict_results['pk_score'].append("NA")

    #------------PN score
                    
                tabla = soup.find('table', class_='styles_table__jWPKo info-grid score-awards')

                if tabla:
                    filas = tabla.find_all('tr')
                    
                    found_score = ""  # Valor por defecto si no se encuentra la puntuación
                    
                    for fila in filas:
                        td_penin = fila.find('td', title='Peñín')
                        if td_penin and td_penin.get_text(strip=True) != '':
                            found_score = td_penin.get_text(strip=True)
                            break  # Terminar el bucle después de encontrar el primer valor
                    
                    # Agregar 'NA' si el valor es vacío
                    dict_results['pn_score'].append(found_score if found_score else "NA")
                    print(f"El primer valor de Peñín es: {found_score}")
                else:
                    print("No se encontró la tabla con la clase especificada")
                    dict_results['pn_score'].append("NA")

                    
    #------------ SK score
                    
                tabla = soup.find('table', class_='styles_table__jWPKo info-grid score-awards')

                if tabla:
                    filas = tabla.find_all('tr')
                    
                    found_score = ""  # Valor por defecto si no se encuentra la puntuación
                    
                    for fila in filas:
                        td_suckling = fila.find('td', title='Suckling')
                        if td_suckling and td_suckling.get_text(strip=True) != '':
                            found_score = td_suckling.get_text(strip=True)
                            break  # Terminar el bucle después de encontrar el primer valor
                    
                    # Agregar 'NA' si el valor es vacío
                    dict_results['sk_score'].append(found_score if found_score else "NA")
                    print(f"El primer valor de Suckling es: {found_score}")
                else:
                    print("No se encontró la tabla con la clase especificada")
                    dict_results['sk_score'].append("NA")
                    
        

                # ... FINAL
            else:
                print(f"No se pudo acceder a la URL: {url}")


        except Exception as e:
            print(f"Ocurrió un error al acceder a la URL ({url}): {str(e)}")
    
    return dict_results

# %%
def mostrar_y_guardar(dict_results, nombre_archivo):
    # Crear un DataFrame a partir del diccionario
    dataframe = pd.DataFrame.from_dict(dict_results, orient='index')
    dataframe = dataframe.transpose()
    # Mostrar el DataFrame
    print("Datos del DataFrame:")
    print(dataframe)

    # Guardar el DataFrame en un archivo CSV
    dataframe.to_csv(nombre_archivo, index_label='Encabezados')

    print(f"\nLos datos se han guardado en el archivo '{nombre_archivo}'.")
    
    # Retornar el DataFrame
    return dataframe




# %%
