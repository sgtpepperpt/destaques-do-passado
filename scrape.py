import os
import pathlib
from collections import Counter
from enum import Enum

from scrapers.google_news_scrapers import *
from scrapers.news_scraper import ScraperCentral
from scrapers.publico_scrapers import ScraperPublico01, ScraperPublico02, ScraperPublico03, ScraperPublico04, \
    ScraperPublico05, ScraperPublico06
from util import make_absolute


class Category(Enum):
    GENERIC = 'Genérico'
    SPORTS = 'Desporto'
    NATIONAL = 'Portugal'
    WORLD = 'Mundo'
    BUSINESS = 'Economia'
    ENTERTAINMENT = 'Entretenimento'
    SCIENCE = 'Ciência'
    HEALTH = 'Saúde'
    POLITICS = 'Política'
    CULTURE = 'Cultura'
    EDUCATION = 'Educação'
    TECHNOLOGY = 'Tecnologia'
    SOCIETY = 'Sociedade'
    LOCAL = 'Local'
    ENVIRONMENT = 'Ambiente'
    OPINION = 'Opinião'


category_bindings = {
    ('Notícias do dia', 'Mais notícias principais', 'Notícias principais', 'Principais notícias', 'Últimas notícias', 'Destaque', 'Última hora', 'Outras'): Category.GENERIC,
    ('Portugal', ): Category.NATIONAL,
    ('Mundo', 'Internacional'): Category.WORLD,
    ('Desporto', 'Esportes'): Category.SPORTS,
    ('Negócios', 'Economia'): Category.BUSINESS,
    ('Entretenimento',): Category.ENTERTAINMENT,
    ('Ciência', 'Ciências'): Category.SCIENCE,
    ('Saúde',): Category.HEALTH,
    ('Política',): Category.POLITICS,
    ('Cultura',): Category.CULTURE,
    ('Educação',): Category.EDUCATION,
    ('Tecnologia',): Category.TECHNOLOGY,
    ('Sociedade',): Category.SOCIETY,
    ('Local',): Category.LOCAL,
    ('Ambiente', 'Ecosfera'): Category.ENVIRONMENT,
    ('Opinião',): Category.OPINION
}


def bind_category(category_text):
    cat_dict = {}
    for k, v in category_bindings.items():
        for key in k:
            cat_dict[key.lower()] = v

    if category_text.lower() not in cat_dict:
        raise Exception('Unknown category: ' + category_text)

    return cat_dict[category_text.lower()]


def bind_source(source_text):
    if source_text == 'Público.pt (Assinatura':
        return 'Público.pt'
    return source_text


def source_name(source):
    sources = {
        'publico.pt': 'Público',
        'ultimahorapublico.pt': 'Público',
    }

    return sources[source]


def scrape(source):
    scraper = ScraperCentral()
    scraper.register_scraper(ScraperGoogleNews01)
    scraper.register_scraper(ScraperGoogleNews02)
    scraper.register_scraper(ScraperGoogleNews03)
    scraper.register_scraper(ScraperPublico01)
    scraper.register_scraper(ScraperPublico02)
    scraper.register_scraper(ScraperPublico03)
    scraper.register_scraper(ScraperPublico04)
    scraper.register_scraper(ScraperPublico05)
    scraper.register_scraper(ScraperPublico06)

    all_news = []
    all_cat = Counter()
    all_source = Counter()

    for file in sorted([p for p in pathlib.Path(os.path.join('crawled', source, 'pages')).iterdir() if p.is_file()]):
        print(file.name)
        filename = file.name.split('.')[0]
        date = filename.split('-')[0]
        is_https = filename.split('-')[1] == 's'

        # TODO dev only
        if int(date) < 20060910150634:
            continue

        with open(file) as f:
            content = f.read()

        news = scraper.scrape_page(source, date, content)
        if len(news) < 3:
            raise Exception('So few news here!')

        for n in news:
            n['article_url'] = make_absolute(source, date, is_https, n['article_url'])
            print(n)

            # source is only present for news aggregators
            if 'source' not in n:
                n['source'] = source_name(source)

            # bind to common categorisations
            n['category'] = bind_category(n['category']).value
            n['source'] = bind_source(n['source'])

            # add metadata to news object
            n['year'] = date[:4]
            n['arquivo_source'] = 'https://arquivo.pt/wayback/{}/http{}://{}/'.format(date, 's' if is_https else '', source)

            # for internal processing purposes, shouldn't be on final output file
            n['ts'] = date
            n['original_article_url'] = get_original_news_link(n['article_url']) if n['article_url'] else ''

            all_cat[n['category']] += 1
            all_source[n['source']] += 1

        all_news += news

    # if a news article is repeated keep only the first version
    # TODO

    # print stats
    print(all_cat)
    print(all_source)
    print(len(all_news))


#scrape('news.google.pt')
scrape('publico.pt')
