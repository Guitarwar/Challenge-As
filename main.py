from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

PATH = 'D:\Descargas\chromedriver-win64\chromedriver.exe'

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

chrome_service = ChromeService(executable_path=PATH)
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

url = "https://ion.inapi.cl/Marca/BuscarMarca.aspx"
driver.get(url)

driver.implicitly_wait(10)  # Espera hasta 10 segundos como máximo

numero_registro = "1236223"  # Reemplaza con el número de registro que desees

## Primera parte Buscar un registro
try:
    registro_input = driver.find_element(By.ID, "txtRegistro")
    registro_input.send_keys(numero_registro)
except NoSuchElementException as e:
    print(f"Elemento 'txtRegistro' no encontrado: {e}")

try:
    buscar_btn = driver.find_element(By.ID, "btnBuscarMarca")
    buscar_btn.click()
except NoSuchElementException as e:
    print(f"Elemento 'btnBuscarMarca' no encontrado: {e}")

## Segunda parte clickear Tabla
try:
    btn_tabla = driver.find_element(By.ID, "tblMarcasResult")
    btn_tabla.click()
except NoSuchElementException as e:
    print(f"Elemento 'tblMarcasResult' no encontrado: {e}")

## Expande el sector de la informacion de Instancias Administrativas
try:
    extender_instaciasAdmin = driver.find_element(By.ID, "exInstancias")
    extender_instaciasAdmin.click()
except NoSuchElementException as e:
    print(f"Elemento 'exInstancias' no encontrado: {e}")

## Obtener los datos de Instancias Administrativas

#Busca el div que contiene la informacion
wait = WebDriverWait(driver, 10)    #Espera hasta que el elemento 'dvInstancias' aparezca en la página
div_instancias = wait.until(EC.presence_of_element_located((By.ID, 'dvInstancias')))

#Busca la tabla dentro del div
time.sleep(5)
tabla_instancias = div_instancias.find_element(By.ID, 'tblInstancias')

# Obtiene todas las filas de la tabla
filas = tabla_instancias.find_elements(By.TAG_NAME, 'tr')

# Inicializa listas para almacenar los datos
resultados = []


# Itera a través de las filas, omitiendo la fila que contiene encabezados
for fila in filas[1:]:
    observada_de_fondo = False
    fecha_observada_fondo = None
    apelaciones = False
    ipt = False
    #Obtengo los datos de la tabla
    celdas = fila.find_elements(By.TAG_NAME, 'td')
    descripcion = celdas[1].text
    print(descripcion)
    
    if "Resolución de observaciones de fondo de marca" in descripcion:
        observada_de_fondo = True
        fecha_observada_fondo = celdas[0].text

    if "Recurso de apelacion" in descripcion:
        apelaciones = True

    if "IPT" in descripcion or "IPTV" in descripcion:
        ipt = True

    # Agrega los resultados a la lista
    resultados.append({
        'Numero_Registro': numero_registro,
        'Observada_de_Fondo': observada_de_fondo,
        'Fecha_Observada_Fondo': fecha_observada_fondo,
        'Apelaciones': apelaciones,
        'IPT': ipt
    })

# Guarda los resultados en un archivo JSON
with open('data/resultados.json', 'w') as json_file:
    json.dump(resultados, json_file, indent=4)

driver.quit()
