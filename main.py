from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import time


PATH = 'D:\Descargas\chromedriver-win64\chromedriver.exe'


chrome_options = Options()
chrome_options.add_argument("--start-maximized") 


chrome_service = ChromeService(executable_path = PATH)
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


url = "https://ion.inapi.cl/Marca/BuscarMarca.aspx"


driver.get(url)
time.sleep(5)


driver.quit()

