from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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

#Primera parte Buscar un registro
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

#Segunda parte clickear Tabla
try:
    btn_tabla = driver.find_element(By.ID, "tblMarcasResult")
    btn_tabla.click()
except NoSuchElementException as e:
    print(f"Elemento 'tblMarcasResult' no encontrado: {e}")

# Espera unos segundos para que la página cargue
time.sleep(5)
driver.quit()
