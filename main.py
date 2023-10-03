from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


PATH = 'D:\Descargas\chromedriver-win64\chromedriver.exe'

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

chrome_service = ChromeService(executable_path=PATH)
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

url = "https://ion.inapi.cl/Marca/BuscarMarca.aspx"
driver.get(url)

driver.implicitly_wait(10)  # Espera hasta 10 segundos como máximo

numero_registro = "1234567"  # Reemplaza con el número de registro que desees

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
fechas = []
descripciones = []
observaciones = []

# Itera a través de las filas, omitiendo la fila que contiene encabezados
for fila in filas[1:]:
    #Obtengo los datos de la tabla
    celdas = fila.find_elements(By.TAG_NAME, 'td')
    
    # Extrae los datos de las celdas
    fecha = celdas[0].text
    descripcion = celdas[1].text
    observacion = celdas[2].text
    
    # Agrega los datos a las listas
    fechas.append(fecha)
    descripciones.append(descripcion)
    observaciones.append(observacion)

    #Datos
    print(f"Fecha: {fecha}")
    print(f"Descripción: {descripcion}")
    print(f"Observación: {observacion}")
    print("-" * 50)

driver.quit()
