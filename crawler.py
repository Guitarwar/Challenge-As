import requests
from bs4 import BeautifulSoup

class WebCrawler:
    def __init__(self):
        self.base_url = "https://ion.inapi.cl/Marca/BuscarMarca.aspx"

