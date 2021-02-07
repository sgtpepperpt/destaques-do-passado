import os
import pathlib
from collections import Counter
from enum import Enum

from scrapers.google_news_scrapers import *
from scrapers.news_scraper import ScraperCentral


class Category(Enum):
    GENERIC = 'Genérico'
    SPORTS = 'Desporto'
    NATIONAL = 'Portugal'
    WORLD = 'Mundo'
    BUSINESS = 'Negócios'
    ENTERTAINMENT = 'Entretenimento'
    SCIENCE = 'Ciência'
    HEALTH = 'Saúde'


category_bindings = {
    ('Notícias do dia', 'Mais notícias principais', 'Notícias principais', 'Principais notícias', 'Últimas notícias'): Category.GENERIC,
    ('Portugal', ): Category.NATIONAL,
    ('Mundo', 'Internacional'): Category.WORLD,
    ('Desporto', 'Esportes'): Category.SPORTS,
    ('Negócios',): Category.BUSINESS,
    ('Entretenimento',): Category.ENTERTAINMENT,
    ('Ciência',): Category.SCIENCE,
    ('Saúde',): Category.HEALTH
}


def bind_category(category_text):
    cat_dict = {}
    for k, v in category_bindings.items():
        for key in k:
            cat_dict[key] = v

    if category_text not in cat_dict:
        raise Exception('Unknown category: ' + category_text)

    return cat_dict[category_text]


def bind_source(source_text):
    if source_text == 'Público.pt (Assinatura':
        return 'Público.pt'
    return source_text


def scrape(source):
    scraper = ScraperCentral()
    scraper.register_scraper(source, ScraperGoogleNews01)
    scraper.register_scraper(source, ScraperGoogleNews02)
    scraper.register_scraper(source, ScraperGoogleNews03)

    all_news = []
    all_cat = Counter()
    all_source = Counter()

    for file in sorted([p for p in pathlib.Path(os.path.join('crawled', source, 'pages')).iterdir() if p.is_file()]):
        print(file.name)
        filename = file.name.split('.')[0]
        date = filename.split('-')[0]
        is_https = filename.split('-')[1] == 's'

        with open(file) as f:
            content = f.read()

        news = scraper.scrape_page(source, date, content)
        if len(news) < 5:
            raise Exception('So few news here!')

        for n in news:
            n['category'] = bind_category(n['category']).value
            n['source'] = bind_source(n['source'])

            # add metadata to news object
            n['year'] = date[:4]
            n['arquivo_source'] = 'https://arquivo.pt/wayback/{}/http{}://{}/'.format(date, 's' if is_https else '', source)

            # for internal processing purposes, shouldn't be on final output file
            n['ts'] = date
            n['original_article_url'] = get_original_news_link(n['article_url'])

            all_cat[n['category']] += 1
            all_source[n['source']] += 1

        all_news += news

    # if a news article is repeated keep only the first version
    # TODO

    # print stats
    print(all_cat)
    print(all_source)
    print(len(all_news))


scrape('news.google.pt')
#scrape('publico.pt')