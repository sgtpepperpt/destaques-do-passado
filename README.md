# Destaques do Passado

Conjunto de scrapers usados para extracção de notícias portuguesas do [Arquivo.pt](https://arquivo.pt), presentes no 
site e repositório [Destaques do Passado](https://destaquesdopassado.pt).

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
