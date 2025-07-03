import asyncio
import csv
import re
from scrapfly import ScrapeConfig, ScrapflyClient
from urllib.parse import quote_plus, urljoin

BASE_URL = "https://nitter.net"

# Chave do scrapfly
SCRAPFLY = ScrapflyClient(key="")

BASE_CONFIG = {
    "asp": True,
    "render_js": True,
}

# Requisições via instância do scrapfly
async def fetch_page(url: str):
    print(f"Fazendo requisição na URL: {url}")
    result = await SCRAPFLY.async_scrape(ScrapeConfig(url, **BASE_CONFIG))
    if not result.content:
        raise Exception("Nenhum conteúdo retornado da página.")
    return result.content

# Busca de padrão no código fonte, baseado na estrutura do HTML do Nitter.
def parse_tweets_from_html(html):
    tweets = []
    tweet_pattern = re.compile(
        r'<div class="tweet-body">.*?<a class="username" href=".*?">@(.+?)</a>.*?<div class="tweet-content media-body" dir="auto">(.*?)</div>.*?<span class="tweet-date"><a href=".*?" title="(.*?)">.*?</a></span>',
        re.DOTALL
    )
    for match in tweet_pattern.findall(html):
        username, content, date = match
        tweet = {
            "nome_usuario": username.strip(),
            "mensagem": content.strip(),
            "data": date.strip(),
        }
        tweets.append(tweet)
    return tweets

# Busca do botão "Load more" e incrementação de requisição para acessar outras páginas.
def find_show_more_button(html):
    show_more_pattern = re.compile(r'<div class="show-more"><a href="(.*?)">Load more</a></div>', re.DOTALL)
    match = show_more_pattern.search(html)
    if match:
        next_page_url = match.group(1).replace("&amp;", "&")
        if next_page_url.startswith('/'):
            return urljoin(BASE_URL + '/search', next_page_url[1:])
        else:
            return urljoin(BASE_URL + '/search', next_page_url)
    return None

# Salvar tweets formatadamente
def salvar_csv(tweets, filename="tweets.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["nome_usuario", "mensagem", "data"])
        writer.writeheader()
        for tweet in tweets:
            writer.writerow(tweet)

# Salvar dados brutos do twitter em tempo real (Sem remoção de duplicatas)
def salvar_csv_incremental(tweets, filename="tweets_raw.csv"):
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["nome_usuario", "mensagem", "data"])
        for tweet in tweets:
            writer.writerow(tweet)

# Remove duplicatas dos tweets, evitando dados repetidos.
def remover_duplicados(tweets):
    seen = set()
    unique_tweets = []
    for tweet in tweets:
        tweet_tuple = (tweet["nome_usuario"], tweet["mensagem"])
        if tweet_tuple not in seen:
            unique_tweets.append(tweet)
            seen.add(tweet_tuple)
    return unique_tweets

# Verificação de tweets por cada página carregada através do "Load more".
async def scrape_load_more(url: str, all_tweets: list, max_load_more: int = 50):
    if max_load_more <= 0:
        print(f"\n[TOTAL DE TWEETS COLETADOS]: {len(all_tweets)}")
        return
    await asyncio.sleep(10)
    html = await fetch_page(url)
    tweets = parse_tweets_from_html(html)
    all_tweets.extend(tweets)
    print(f"Coletados {len(tweets)} tweets nesta página. Total de {len(all_tweets)} até agora.")

    # Salvar tweets brutos incrementalmente
    salvar_csv_incremental(tweets)

    await asyncio.sleep(5)
    next_page = find_show_more_button(html)
    if next_page:
        print(f"Carregando mais tweets... Requisitando a próxima página.")
        print(f"URL de 'Load more' encontrada: {next_page}")
        await scrape_load_more(next_page, all_tweets, max_load_more - 1)
    else:
        print("Não há mais tweets para carregar.")

# Pesquisa de termo
async def scrape_search(term: str):
    all_tweets = []
    url = f"{BASE_URL}/search?f=tweets&q={quote_plus(term)}"
    await scrape_load_more(url, all_tweets, max_load_more=50)
    return all_tweets

if __name__ == "__main__":
    async def main():
        #termo_de_busca = "INSS Lula since:2025-04-23 until:2025-04-30"
        termo_de_busca = "<query>"
        # Criar arquivo tweets_raw.csv com cabeçalho
        with open("tweets_raw.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["nome_usuario", "mensagem", "data"])
            writer.writeheader()

        resultado = await scrape_search(termo_de_busca)
        resultado_unico = remover_duplicados(resultado)
        salvar_csv(resultado_unico)
        print(f"{len(resultado_unico)} tweets únicos salvos em 'tweets.csv'.")

    asyncio.run(main()
