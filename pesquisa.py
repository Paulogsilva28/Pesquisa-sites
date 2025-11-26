import requests
from bs4 import BeautifulSoup
import os 


URL_G1 = "https://g1.globo.com/busca/?q=vagas+estagio+ti+goiania+orgao+publico"

arquivo_links = 'Links_Vagas.txt'
def carregar_já_vistos():
    if os.pach.existes(arquivo_links):
        with open(arquivo_links,'r') as f:
            return set (line.strip() for line in f)
        return set()
    
    
    
