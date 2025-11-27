import requests
from bs4 import BeautifulSoup

# Fazendo a requisição para a página de notícias
url = 'https://www.r7.com/'
response = requests.get(url)
html = response.text

# Criando o objeto Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

# Buscando todos os elementos que contêm os títulos das notícias
titulos = soup.find_all('h2', class_='post__title')

# Extraindo e imprimindo os títulos
for titulo in titulos:
    print("="*100)
    print(titulo.text.strip())