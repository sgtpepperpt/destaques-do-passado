import os
import pathlib
import sqlite3

import requests

from src.categories import bind_category
from src.scrapers.aeiou_scrapers import ScraperAeiou01, ScraperAeiou02, ScraperAeiou03, ScraperAeiou04, ScraperAeiou05, \
    ScraperAeiou06

from src.scrapers.diariodenoticias_dummy import DummyDiarioDeNoticias01, DummyDiarioDeNoticias03
from src.scrapers.jornaldenoticias_dummy import DummyJornalDeNoticias01, DummyJornalDeNoticias07
from src.scrapers.publico_dummy import DummyPublico01

from src.scrapers.diariodenoticias_scrapers import ScraperDiarioDeNoticias02, ScraperDiarioDeNoticias04, \
    ScraperDiarioDeNoticias05, ScraperDiarioDeNoticias06, ScraperDiarioDeNoticias07
from src.scrapers.expresso_scrapers import ScraperExpresso01, ScraperExpresso02, ScraperExpresso03, ScraperExpresso04, \
    ScraperExpresso05, ScraperExpresso06, ScraperExpresso07, ScraperExpresso08, ScraperExpresso09, ScraperExpresso10, \
    ScraperExpresso11, ScraperExpresso12, ScraperExpresso13, ScraperExpresso14, ScraperExpresso15, ScraperExpresso16, \
    ScraperExpresso17, ScraperExpresso18, ScraperExpresso19, ScraperExpresso21, ScraperExpresso20, ScraperExpresso23, \
    ScraperExpresso22, ScraperExpresso24, ScraperExpresso25, ScraperExpresso26, ScraperExpresso27, ScraperExpresso28, \
    ScraperExpresso29, ScraperExpresso30
from src.scrapers.google_news_scrapers import *
from src.scrapers.jornaldenoticias_scrapers import ScraperJornalDeNoticias02, ScraperJornalDeNoticias03, \
    ScraperJornalDeNoticias04, ScraperJornalDeNoticias05, ScraperJornalDeNoticias06, ScraperJornalDeNoticias08, \
    ScraperJornalDeNoticias09, ScraperJornalDeNoticias10
from src.scrapers.portugaldiario_scrapers import ScraperPortugalDiario01, ScraperPortugalDiario02, \
    ScraperPortugalDiario03, ScraperPortugalDiario04, ScraperPortugalDiario05, ScraperPortugalDiario06
from src.scrapers.publico_scrapers import ScraperPublico02, ScraperPublico03, ScraperPublico04, ScraperPublico05, \
    ScraperPublico06, ScraperPublico07, ScraperPublico08


from src.scrapers.news_scraper import ScraperCentral
from src.sources import bind_source, source_name_from_file
from src.text_util import remove_clutter, prettify_text, ignore_title, ignore_pretitle, prettify_title, ignore_snippet
from src.util import *


def check_urls(cursor):
    urls = cursor.execute('''SELECT url FROM urls WHERE status = 0''').fetchall()

    for url in [url[0] for url in urls if not url[0].startswith('no-article-url')]:
        # noFrame gives us the actual status code
        # also remove the db uniqueness key
        no_frame_url = remove_destaques_uniqueness(url.replace('arquivo.pt/wayback', 'arquivo.pt/noFrame/replay'))

        try:
            r = requests.head(no_frame_url, allow_redirects=True)

            cursor.execute('UPDATE urls SET status = ?, redirect_url = ? WHERE url = ?',
                           (r.status_code, r.url, url))
            cursor.connection.commit()
        except Exception as e:
            print(e)


def create_database(cursor):
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('''CREATE TABLE IF NOT EXISTS urls (
                    url             TEXT    PRIMARY KEY NOT NULL,
                    status          INT     DEFAULT 0,
                    redirect_url    TEXT
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


def scrape_source(scraper, source, cursor, db_insert=True):
    for file in sorted([p for p in pathlib.Path(os.path.join('crawled', source, 'pages')).iterdir() if p.is_file() and p.name != '.DS_Store']):
        filename = file.name.replace('.html', '')
        print(filename)

        elems = filename.split('-')
        date = elems[0]
        is_https = elems[1] == 's'
        actual_url = decode_url(elems[2]) if len(elems) > 2 else None

        # TODO dev only
        # if int(date) < 20120701150250:
        #     continue

        with open(file) as f:
            content = f.read()

        news = scraper.scrape_page(source, date, content)
        if news is None:  # ignore dummy scrapers
            continue

        if len(news) < 3:  # useful to detect when a parser stops working
            raise Exception('So few news here!')

        source_url = actual_url or source

        for n in news:
            # timestamp can be provided in news if using dummy parser, else get it from filename
            timestamp = str(n.get('timestamp') or date)

            # parse the url to the original article, a lot of times it's relative to the original website's root
            article_url = make_absolute(source_url, timestamp, is_https, n['article_url'])

            # source is only present for news aggregators, so if not present deduce it from filename
            article_source = bind_source(n.get('source') or source_name_from_file(source))

            # bind category to a common set
            category = bind_category(n['category']).value

            # add the link to where we got the article from (our source of knowledge)
            # sometimes the source url might be defined by hand (eg when the article is not in the crawled archives, or not on the newpaper's main page)
            arquivo_source_url = n.get('arquivo_source_url') or 'https://arquivo.pt/wayback/{}/http{}://{}/'.format(timestamp, 's' if is_https else '', source_url)

            # the original link to the article should be unique for each one, thus indicating its uniqueness
            # (article_url does not work, as two different snapshots would have different links pointing to the same)
            original_article_url = get_original_news_url(article_url)

            # convert noFrame url to wayback (with sidebar) for UI purposes
            article_url = article_url.replace('noFrame/replay', 'wayback')

            #  title, pretitle and snippet cleanups
            title = prettify_title(n['title'])
            if ignore_title(title):
                continue

            pretitle = prettify_title(n.get('headline'))
            if ignore_pretitle(pretitle):
                continue

            snippet = prettify_text(n.get('snippet'))
            if ignore_snippet(snippet):
                continue

            print('{}; {}; {} / {}; {} / {}; {}'.format(title, pretitle, snippet, category, article_source, article_url, n.get('img_url')))

            # add article to DB
            if not db_insert:
                continue

            cursor.execute('''INSERT OR IGNORE INTO urls(url) VALUES (?)''', (article_url,))

            img_url = None
            if n.get('img_url'):
                img_url = make_absolute(source_url, timestamp, is_https, n['img_url'])
                cursor.execute('''INSERT OR IGNORE INTO urls(url) VALUES (?)''', (img_url,))

            # ignores already-inserted news (article url is unique for each article)
            # assumes sequencial insertion to preserver only earliest occurence of the article
            cursor.execute('''INSERT OR IGNORE INTO articles(original_article_url, article_url,arquivo_source_url,title,source,day,month,year,category,importance,headline,snippet,img_url) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                           (original_article_url, article_url, arquivo_source_url, title, article_source, timestamp[6:8], timestamp[4:6], timestamp[:4], category, n.get('importance'), pretitle, snippet, img_url))
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
    scraper.register_scraper(DummyPublico01)
    scraper.register_scraper(ScraperPublico02)
    scraper.register_scraper(ScraperPublico03)
    scraper.register_scraper(ScraperPublico04)
    scraper.register_scraper(ScraperPublico05)
    scraper.register_scraper(ScraperPublico06)
    scraper.register_scraper(ScraperPublico07)
    scraper.register_scraper(ScraperPublico08)
    scraper.register_scraper(ScraperPortugalDiario01)
    scraper.register_scraper(ScraperPortugalDiario02)
    scraper.register_scraper(ScraperPortugalDiario03)
    scraper.register_scraper(ScraperPortugalDiario04)
    scraper.register_scraper(ScraperPortugalDiario05)
    scraper.register_scraper(ScraperPortugalDiario06)
    scraper.register_scraper(DummyJornalDeNoticias01)
    scraper.register_scraper(ScraperJornalDeNoticias02)
    scraper.register_scraper(ScraperJornalDeNoticias03)
    scraper.register_scraper(ScraperJornalDeNoticias04)
    scraper.register_scraper(ScraperJornalDeNoticias05)
    scraper.register_scraper(ScraperJornalDeNoticias06)
    scraper.register_scraper(DummyJornalDeNoticias07)
    scraper.register_scraper(ScraperJornalDeNoticias08)
    scraper.register_scraper(ScraperJornalDeNoticias09)
    scraper.register_scraper(ScraperJornalDeNoticias10)
    scraper.register_scraper(ScraperExpresso01)
    scraper.register_scraper(ScraperExpresso02)
    scraper.register_scraper(ScraperExpresso03)
    scraper.register_scraper(ScraperExpresso04)
    scraper.register_scraper(ScraperExpresso05)
    scraper.register_scraper(ScraperExpresso06)
    scraper.register_scraper(ScraperExpresso07)
    scraper.register_scraper(ScraperExpresso08)
    scraper.register_scraper(ScraperExpresso09)
    scraper.register_scraper(ScraperExpresso10)
    scraper.register_scraper(ScraperExpresso11)
    scraper.register_scraper(ScraperExpresso12)
    scraper.register_scraper(ScraperExpresso13)
    scraper.register_scraper(ScraperExpresso14)
    scraper.register_scraper(ScraperExpresso15)
    scraper.register_scraper(ScraperExpresso16)
    scraper.register_scraper(ScraperExpresso17)
    scraper.register_scraper(ScraperExpresso18)
    scraper.register_scraper(ScraperExpresso19)
    scraper.register_scraper(ScraperExpresso20)
    scraper.register_scraper(ScraperExpresso21)
    scraper.register_scraper(ScraperExpresso22)
    scraper.register_scraper(ScraperExpresso23)
    scraper.register_scraper(ScraperExpresso24)
    scraper.register_scraper(ScraperExpresso25)
    scraper.register_scraper(ScraperExpresso26)
    scraper.register_scraper(ScraperExpresso27)
    scraper.register_scraper(ScraperExpresso28)
    scraper.register_scraper(ScraperExpresso29)
    scraper.register_scraper(ScraperExpresso30)
    scraper.register_scraper(DummyDiarioDeNoticias01)
    scraper.register_scraper(ScraperDiarioDeNoticias02)
    scraper.register_scraper(DummyDiarioDeNoticias03)
    scraper.register_scraper(ScraperDiarioDeNoticias04)
    scraper.register_scraper(ScraperDiarioDeNoticias05)
    scraper.register_scraper(ScraperDiarioDeNoticias06)
    scraper.register_scraper(ScraperDiarioDeNoticias07)
    scraper.register_scraper(ScraperAeiou01)
    scraper.register_scraper(ScraperAeiou02)
    scraper.register_scraper(ScraperAeiou03)
    scraper.register_scraper(ScraperAeiou04)
    scraper.register_scraper(ScraperAeiou05)
    scraper.register_scraper(ScraperAeiou06)

    # get scraping
    scrape_source(scraper, 'news.google.pt', cursor)
    scrape_source(scraper, 'publico.pt', cursor)
    scrape_source(scraper, 'portugaldiario.iol.pt', cursor)
    scrape_source(scraper, 'jn.pt', cursor)
    scrape_source(scraper, 'expresso.pt', cursor)
    scrape_source(scraper, 'dn.pt', cursor)
    scrape_source(scraper, 'aeiou.pt', cursor)

    # check urls for their status and final destination (in case they're a redirect)
    check_urls(cursor)

    conn.commit()
    conn.close()


main()
