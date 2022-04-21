# Destaques do Passado

Conjunto de scrapers usados para extracção de notícias portuguesas do [Arquivo.pt](https://arquivo.pt), presentes no 
sítio e repositório [Destaques do Passado](https://destaquesdopassado.pt).

Criado por Guilherme Borges em 2021.

## Uso
Divide-se em três scripts:
* `crawl.py`: recolhe a lista de páginas arquivadas pelo Arquivo.pt, e guarda as mesmas localmente
* `scrape.py`: faz o scraping das páginas recolhidas e coloca-as numa base de dados SQLite3
* `output.py`: produz uma lista de 366 ficheiros JSON com recurso à base de dados produzida anteriormente

As configurações para o script `crawl.py`, detalhando as fontes a recolher, encontram-se em `config/sources.py`.

O script `scrape.py` usa a biblioteca BeautifulSoup 4 para extrair o conteúdo das páginas recolhidas. Cada fonte tem um
conjunto de scrapers definido no directório `src/scrapers`. Cada scraper suporta uma versão da página original, podendo
suportar pequenas variações no design da página. Algumas versões, por serem demasiado irregulares, e por terem menos
conteúdo, têm o seu conteúdo pre-processado manualmente, e entregue ao script via um scraper chamado "dummy".

## Extender o scraper
O mecanismo de scraping foi feito para ser facilmente extendido para novas fontes de notícias, bem como para adicionar
facilmente anos mais recentes às fontes já existentes.

Para adicionar uma nova fonte deverá editar o ficheiro `src/config.py`.

Para adicionar um scraper (por exemplo, para versões mais recentes de fontes existentes), deverá
seguir o seguinte formato:
```
class ScraperFonte01(NewsScraper):
    source = 'rtp.pt'        # nome da directoria em crawled/"source"
    cutoff = 20151231180236  # timestamp da última versão suportada pelo scraper (vários scrapers são ordenados por este parâmetro)
    minimum_news = 1         # número mínimo de notícias esperadas (OPCIONAL)

    # este método deverá ser implementado por todos os scrapers
    # recebe um objecto BeautifulSoup
    # retorna uma lista de dicionários com a interface descrita em https://destaquesdopassado.pt/api
    def scrape_page(self, soup):
        all_news = []
        return all_news
```

De seguida bastará registar o scraper em `bin/scrape.py`. A ordem pela qual são registados é irrelevante, já que a
ordenação é dada pelo parâmetro `cutoff`: para cada ficheiro com timestamp *t* o programa irá escolher o scraper com
cutoff menor de todos aqueles que são maiores ou iguais a *t*.

## Obter estatísticas
```
-- gráficos
SELECT year, COUNT(*) AS c FROM articles GROUP BY year;
SELECT source, COUNT(*) AS c FROM articles GROUP BY source ORDER BY c DESC;
SELECT COUNT(*) FROM articles GROUP BY day, month ORDER BY month, day;
SELECT category, COUNT(*) AS c FROM articles GROUP BY category ORDER BY c DESC;

-- números
SELECT COUNT(*) FROM articles;
SELECT COUNT(*) FROM articles INNER JOIN urls AS img_urls on articles.img_url = img_urls.url WHERE status = 200;
SELECT COUNT(*) FROM articles WHERE snippet IS NOT NULL;
SELECT COUNT(*) FROM articles LEFT OUTER JOIN urls AS article_urls ON articles.article_url = article_urls.url WHERE status = 200;
SELECT day,month,year FROM articles ORDER BY year,month,day ASC LIMIT 1;

-- url status
SELECT status, COUNT(*) FROM urls GROUP BY status;
```
