import requests
from bs4 import BeautifulSoup # Importação Corrigida!
import os 
from datetime import datetime

# --- Configurações ---
URL_G1 = "https://g1.globo.com/busca/?q=vagas+estagio+ti+goiania+orgao+publico"
ARQUIVO_LINKS = 'links_vistos.txt'

# Termos de filtragem (para garantir que a notícia é relevante)
TERMOS_VAGA = ["estágio", "ti", "informática", "seleção", "edital", "concurso", "governo", "prefeitura", "federal", "universidade"]
TERMOS_PRINCIPAIS = ["estágio", "edital", "seleção", "concurso"]


# --- Funções de Controle ---

def carregar_links_vistos():
    """Carrega os links que já foram notificados para evitar repetição."""
    if os.path.exists(ARQUIVO_LINKS):
        with open(ARQUIVO_LINKS, 'r') as f:
            # Retorna um set (conjunto) para consultas rápidas
            return set(line.strip() for line in f)
    return set()

def adicionar_link_visto(link):
    """Adiciona um novo link ao arquivo."""
    with open(ARQUIVO_LINKS, 'a') as f:
        f.write(link + '\n')

# --- Função Principal de Busca ---

def buscar_vagas_no_g1():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando busca no G1...")
    
    links_vistos = carregar_links_vistos()
    novas_vagas = []

    try:
        # 1. Faz a requisição HTTP para a URL
        # O cabeçalho simula um navegador para evitar bloqueios simples
        headers = {'User-Agent': 'Mozilla/5.0'}
        resposta = requests.get(URL_G1, headers=headers, timeout=15)
        resposta.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"ERRO: Não foi possível acessar a URL. Verifique sua conexão ou a URL. Detalhes: {e}")
        return

    # 2. Analisa o conteúdo HTML da página
    sopa = BeautifulSoup(resposta.text, 'html.parser')

    # 3. EXTRAÇÃO DE DADOS
    # Tenta encontrar os links de títulos de notícias.
    # Esta é a parte mais vulnerável a mudanças no código do G1.
    resultados = sopa.find_all('a', class_=lambda x: x and ('_highlight-title' in x or 'post-titulo' in x))
    
    # Tentativa alternativa caso o seletor principal falhe (foca em links na área de resultados)
    if not resultados:
         resultados = sopa.find_all('a', {'data-tracker-label': 'title'}) 


    for resultado in resultados:
        link = resultado.get('href')
        titulo = resultado.text.strip()
        
        # 4. FILTRAGEM DE RELEVÂNCIA
        if link and link not in links_vistos:
            
            titulo_lower = titulo.lower()
            
            # Condição: Deve conter Pelo menos um termo principal (estágio, edital...)
            # E deve conter Pelo menos um termo de vaga/órgão (ti, governo, prefeitura...)
            if any(termo in titulo_lower for termo in TERMOS_PRINCIPAIS) and \
               any(termo in titulo_lower for termo in TERMOS_VAGA):
                
                novas_vagas.append({
                    'titulo': titulo,
                    'link': link
                })

    # 5. Exibir e Salvar novas vagas
    if novas_vagas:
        print(f"\n✅ NOVAS VAGAS DE ÓRGÃO PÚBLICO ENCONTRADAS ({len(novas_vagas)}):")
        print("----------------------------------------------------------------")
        for vaga in novas_vagas:
            print(f"Título: {vaga['titulo']}\nLink: {vaga['link']}\n")
            adicionar_link_visto(vaga['link'])
        print("Links salvos em 'links_vistos.txt'.")
    else:
        print("\nNenhuma nova vaga relevante encontrada nesta rodada.")
    
    print("-" * 60)


if __name__ == "__main__":
    buscar_vagas_no_g1()