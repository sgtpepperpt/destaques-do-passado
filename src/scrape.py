import os
import pathlib
import sqlite3

import requests

from src.categories import bind_category
from src.scrapers.google_news_scrapers import *
from src.scrapers.news_scraper import ScraperCentral
from src.scrapers.publico_scrapers import ScraperPublico01, ScraperPublico02, ScraperPublico03, ScraperPublico04, \
    ScraperPublico05, ScraperPublico06, ScraperPublico07
from src.sources import bind_source, source_name_from_file
from src.util import *


def check_urls(cursor):
    urls = cursor.execute('''SELECT url FROM urls WHERE status = 0''').fetchall()

    for url in [url[0] for url in urls if not url[0].startswith('no-article-url')]:
        # noFrame gives us the actual status code
        no_frame_url = url.replace('arquivo.pt/wayback', 'arquivo.pt/noFrame/replay')

        r = requests.head(no_frame_url)
        cursor.execute('UPDATE urls SET status = ? WHERE url = ?', (r.status_code, url))
        cursor.connection.commit()


def check_redirects(cursor):
    urls = cursor.execute('''SELECT url FROM urls WHERE status LIKE \'3%\' AND redirect_status = 0''').fetchall()

    for url in [url[0] for url in urls]:
        # noFrame gives us the actual status code
        no_frame_url = url.replace('arquivo.pt/wayback', 'arquivo.pt/noFrame/replay')

        try:
            r = requests.head(no_frame_url, allow_redirects=True)

            cursor.execute('UPDATE urls SET redirect_url = ?, redirect_status = ? WHERE url = ?', (r.url, r.status_code, url))
            cursor.connection.commit()
        except Exception as e:
            print(e)


def create_database(cursor):
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('''CREATE TABLE IF NOT EXISTS urls (
                    url             TEXT    PRIMARY KEY NOT NULL,
                    status          INT     DEFAULT 0,
                    redirect_url    TEXT,
                    redirect_status INT     DEFAULT 0
                )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS articles (
                    original_article_url    TEXT    NOT NULL PRIMARY KEY,
                    article_url             TEXT    NOT NULL,
                    arquivo_source_url      TEXT    NOT NULL,
                    title                   TEXT    NOT NULL,
                    source                  TEXT    NOT NULL,
                    day                     INT     NOT NULL,
                    month                   INT     NOT NULL,
                    year                    INT     NOT NULL,
                    category                TEXT    NOT NULL,
                    importance              INT,
                    headline                TEXT,
                    snippet                 TEXT,
                    img_url                 TEXT,
                    FOREIGN KEY(article_url) REFERENCES urls(url),
                    FOREIGN KEY(img_url) REFERENCES urls(url)
                )''')

    cursor.connection.commit()


def scrape_source(scraper, source, cursor):
    for file in sorted([p for p in pathlib.Path(os.path.join('crawled', source, 'pages')).iterdir() if p.is_file()]):
        print(file.name)
        filename = file.name.split('.')[0]
        date = filename.split('-')[0]
        is_https = filename.split('-')[1] == 's'

        # TODO dev only
        # if int(date) < 20120305160321:
        #     continue

        with open(file) as f:
            content = f.read()

        news = scraper.scrape_page(source, date, content)
        if news is None:  # ignore dummy scrapers
            continue

        if len(news) < 3:  # useful to detect when a parser stops working
            raise Exception('So few news here!')

        for n in news:
            n['article_url'] = make_absolute(source, date, is_https, n['article_url'])

            # source is only present for news aggregators, so if not present deduce it from filename
            article_source = bind_source(n.get('source') or source_name_from_file(source))

            # bind category to a common set
            category = bind_category(n['category']).value

            # add the link to where we got the article from
            arquivo_source_url = 'https://arquivo.pt/wayback/{}/http{}://{}/'.format(date, 's' if is_https else '', source)

            # the original link to the article should be unique for each one, thus indicating its uniqueness
            # (article_url does not work as two different snapshots would have different links)
            original_article_url = get_original_news_url(n['article_url'])

            # convert noFrame url to wayback (with sidebar) for UI purposes
            n['article_url'] = n['article_url'].replace('noFrame/replay', 'wayback')

            print(n)

            # add article to DB
            cursor.execute('''INSERT OR IGNORE INTO urls(url) VALUES (?)''', (n['article_url'],))

            if 'img_url' in n and n['img_url']:
                n['img_url'] = make_absolute(source, date, is_https, n['img_url'])
                cursor.execute('''INSERT OR IGNORE INTO urls(url) VALUES (?)''', (n.get('img_url'),))

            # ignores already-inserted news (article url is unique for each article)
            # assumes sequencial insertion to preserver only earliest occurence of the article
            cursor.execute('''INSERT OR IGNORE INTO articles(original_article_url, article_url,arquivo_source_url,title,source,day,month,year,category,importance,headline,snippet,img_url) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                           (original_article_url, n['article_url'], arquivo_source_url, n['title'], article_source, date[6:8], date[4:6], date[:4], category, n.get('importance'), n.get('headline'), n.get('snippet'), n.get('img_url')))
            cursor.connection.commit()


def main():
    conn = sqlite3.connect('parsed_articles.db')
    cursor = conn.cursor()
    create_database(cursor)

    # init scraping machine
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
    scraper.register_scraper(ScraperPublico07)

    # get scraping
    scrape_source(scraper, 'news.google.pt', cursor)
    scrape_source(scraper, 'publico.pt', cursor)

    # process urls
    check_urls(cursor)
    check_redirects(cursor)

    conn.commit()
    conn.close()


main()
