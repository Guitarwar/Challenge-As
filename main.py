import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.scraper import buscar_y_extraer_datos

def main():
    try:
        # Leer configuración desde el archivo 'config.json'
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            chrome_driver_path = config.get('chrome_driver_path', '')
            start_maximized = config.get('start_maximized', False)
            wait_time = config.get('wait_time', 10)
            output_file_path = config.get('output_file_path', '')
            lista_registros = config.get('numeros_registro', [])

        chrome_options = Options()
        if start_maximized:
            chrome_options.add_argument("--start-maximized")

        chrome_service = ChromeService(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        resultados = []

        for numero_registro in lista_registros:
            # Intenta buscar e interactuar con el elemento 'txtRegistro' con un tiempo de espera
            try:
                driver.get("https://ion.inapi.cl/Marca/BuscarMarca.aspx")
                registro_input = WebDriverWait(driver, wait_time).until(
                    EC.presence_of_element_located((By.ID, "txtRegistro")))
                registro_input.send_keys(numero_registro)

                buscar_btn = WebDriverWait(driver, wait_time).until(
                    EC.element_to_be_clickable((By.ID, "btnBuscarMarca")))
                buscar_btn.click()

                # proceso de extracción de datos
                datos = buscar_y_extraer_datos(driver, numero_registro)
                resultados.extend(datos)
            except Exception as e:
                print(f"No se pudo interactuar con 'txtRegistro' para el registro {numero_registro}: {str(e)}")

        # Guardar los resultados en un archivo JSON
        with open(output_file_path, 'w') as json_file:
            json.dump(resultados, json_file, indent=4)

    except FileNotFoundError:
        print("No se encontró el archivo de configuración 'config.json'.")
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
