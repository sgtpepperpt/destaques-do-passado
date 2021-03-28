# Conjunto de Scrapers para extracção de notícias portuguesas do arquivo.pt

Divide-se em três aplicações:
* `crawl`: recolhe a lista de páginas arquivadas pelo arquivo.pt, e guarda as mesmas localmente
* `scrape`: faz o scraping das páginas recolhidas e coloca-as numa base de dados SQLite3
* `output`: produz uma lista de 366 ficheiros JSON com recurso à base de dados produzida anteriormente