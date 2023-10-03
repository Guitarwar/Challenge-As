from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def buscar_y_extraer_datos(driver, numero_registro):
    resultados = []

    ## Primera parte Buscar un registro
    try:
        registro_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "txtRegistro")))
        registro_input.send_keys(numero_registro)
    except Exception as e:
        print(f"Elemento 'txtRegistro' no encontrado o no interactuable: {e}")
        return resultados

    try:
        buscar_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnBuscarMarca")))
        buscar_btn.click()
    except Exception as e:
        print(f"Elemento 'btnBuscarMarca' no encontrado o no interactuable: {e}")
        return resultados

    ## Segunda parte clickear Tabla
    try:
        btn_tabla = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "tblMarcasResult")))
        btn_tabla.click()
    except Exception as e:
        print(f"Elemento 'tblMarcasResult' no encontrado o no interactuable: {e}")
        return resultados

    ## Expande el sector de la información de Instancias Administrativas
    try:
        extender_instanciasAdmin = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "exInstancias")))
        extender_instanciasAdmin.click()
    except Exception as e:
        print(f"Elemento 'exInstancias' no encontrado o no interactuable: {e}")
        return resultados

    ## Obtener los datos de Instancias Administrativas
    try:
        # Busca el div que contiene la información
        div_instancias = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'dvInstancias')))

        # Busca la tabla dentro del div
        time.sleep(5)
        tabla_instancias = div_instancias.find_element(By.ID, 'tblInstancias')

        # Obtiene todas las filas de la tabla
        filas = tabla_instancias.find_elements(By.TAG_NAME, 'tr')

        # Itera a través de las filas, omitiendo la fila que contiene encabezados
        for fila in filas[1:]:
            observada_de_fondo = False
            fecha_observada_fondo = None
            apelaciones = False
            ipt = False
            # Obtengo los datos de la tabla
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
    except Exception as e:
        print(f"Error al obtener datos de Instancias Administrativas: {e}")

    return resultados
