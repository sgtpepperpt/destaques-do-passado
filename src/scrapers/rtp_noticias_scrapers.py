import re
from urllib.parse import unquote_to_bytes

from bs4 import BeautifulSoup

from src.scrapers.rtp_scrapers import red_scraper, modern_scraper
from src.util import generate_dummy_url, get_direct_strings, is_after, get_direct_strings_between, find_comments, \
    find_comments_regex, is_between
from src.text_util import clean_special_chars, remove_clutter

from src.scrapers.news_scraper import NewsScraper, Importance


class ScraperRtpNoticias01(NewsScraper):
    source = 'noticias.rtp.pt'
    cutoff = 20040415030613

    def scrape_page(self, soup):
        return red_scraper(soup)


class ScraperRtpNoticias02(NewsScraper):
    source = 'noticias.rtp.pt'
    cutoff = 20071011234507

    def scrape_page(self, soup):
        return modern_scraper(soup)


class ScraperRtpNoticias03(NewsScraper):
    source = 'noticias.rtp.pt'
    cutoff = 20081021143915

    def scrape_page(self, soup):
        all_news = []

        feature = soup.find('div', id='dstk_principal')
        # category = feature.find('span', class_='seccoes').get_text()
        img_elem = feature.find('div', id='MancheteMoldura').find('img')

        title_elem = feature.find('span', id='MancheteTitle').find_parent('a')
        snippet_elem = feature.find('div', id='MancheteLead')

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title_elem.get_text(),
            'snippet': snippet_elem.get_text(),
            'img_url': img_elem.get('src'),
            'category': 'Destaques',
            'importance': Importance.FEATURE
        })

        larger_articles = soup.find_all('div', class_='subdstk')
        for article_elem in larger_articles:
            category = article_elem.find('p', class_='seccoes').get_text()
            img_elem = article_elem.find('div', id=re.compile(r'^Moldura1Substk(_Old)?$')).find('img')

            pretitle = None

            if category == 'Presidência UE':
                pretitle = category
                category = 'Política'

            title_elem = article_elem.find('a', class_='titulos_subdstks')
            snippet_elem = article_elem.find('p', class_='Lead_subdstks')

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'headline': pretitle,
                'snippet': snippet_elem.get_text(),
                'img_url': img_elem.get('src'),
                'category': category,
                'importance': Importance.LARGE
            })

        category_boxes = soup.find_all('div', class_='mais_noticias')
        for category_box in category_boxes:
            category = get_direct_strings(category_box.find('p', class_='maisnoticias_seccoes'))

            for title_elem in category_box.find_all('a', class_='informacao_small'):
                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title_elem.get_text(),
                    'category': category,
                    'importance': Importance.SMALL
                })

        # big latest strip at top
        latest_strip = soup.find('div', class_='UltimaHora')
        if latest_strip:
            all_news.append({
                'article_url': latest_strip.find('a').get('href'),
                'title': latest_strip.find('a').get_text(),
                'category': 'Destaques',
                'importance': Importance.LATEST
            })

        return all_news


class ScraperRtpNoticias04(NewsScraper):
    source = 'noticias.rtp.pt'
    cutoff = 20120128092034

    def constrain_category(self, category):
        if category == 'Gripe A - H1N1':
            return 'Saúde'

        if category in ['Eleições Europeias 2009', 'Legislativas 2009', 'Europeias 2009', 'Autárquicas 2009',
                        'Eleições 2011']:
            return 'Política'

        return category

    def scrape_page(self, soup):
        all_news = []

        feature = soup.find('div', class_='DestkPrincipal')
        img_elem = (feature.find('a', class_='Imagem') or feature.find('a')).find('img')
        title_elem = (feature.find('div', class_='AbsoluteTitle') or feature.find('h2')).find('a')
        pretitle_elem = feature.find('div', class_='AbsoluteAnteTitle') or feature.find('h5')

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title_elem.get_text(),
            'pretitle': pretitle_elem.get_text(),
            'img_url': img_elem.get('src'),
            'category': 'Destaques',
            'importance': Importance.FEATURE
        })

        large_article_boxes = soup.find_all('div', id='DestkSecundarioBO')
        for large_articles in [e.find_all('div', class_='Elemento') for e in large_article_boxes]:
            for article_elem in large_articles:
                img_elem = article_elem.find('div', class_='Img')
                img_url = img_elem.find('img').get('src') if img_elem else None

                inner_elem = article_elem.find('div', class_='Text')
                title_elem = inner_elem.find('h2').find('a')
                pretitle_elem = inner_elem.find('h5')

                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': get_direct_strings(title_elem),
                    'pretitle': pretitle_elem.get_text(),
                    'img_url': img_url,
                    'category': 'Destaques',
                    'importance': Importance.LARGE
                })

        latest_articles = soup.find('div', id='especias_ult')
        if latest_articles:
            for article_elem in [e.find('div', class_='Text') for e in latest_articles.find_all('div', class_='Elemento')]:
                title_elem = article_elem.find('h2').find('a')
                category = self.constrain_category(article_elem.find('h5').get_text())

                title = get_direct_strings(title_elem)
                if 'Debate' in title or 'Entrevista' in title:
                    continue

                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title,
                    'category': category,
                    'importance': Importance.LATEST
                })

        dropdown_category_sections = soup.find('div', id='MenuNoticiasTop').find('ul', id=re.compile(r'^(MenuNiveis_H|MenuTopInfo)$')).find('ul').find_all('li', recursive=False)
        for category_box in dropdown_category_sections:
            category = category_box.find('a').get_text()

            category = self.constrain_category(category)

            for article_elem in [e.find('a') for e in category_box.find_all('li')]:
                pretitle_elem = article_elem.find('b')
                pretitle = pretitle_elem.get_text().replace(':', '') if pretitle_elem else None
                if pretitle in ['RESULTADOS DAS EUROPEIAS 2009', 'RESULTADOS DAS AUTÁRQUICAS 2009', 'RESULTADOS DAS LEGISLATIVAS 2009']:
                    continue

                all_news.append({
                    'article_url': article_elem.get('href'),
                    'title': get_direct_strings(article_elem),
                    'pretitle': pretitle,
                    'category': category,
                    'importance': Importance.SMALL
                })

        category_boxes = soup.find('div', class_='AbaixoDestk').find('div').find_all('div', recursive=False)
        for category_box in category_boxes:
            category = category_box.find('a', class_='Tema').get_text()

            if category in ['Recomendamos', 'Informação Útil']:
                continue  # not all are newsworthy

            main_article = category_box.find('div', class_='EmentoArtigo')
            img_elem = (main_article.find('div', class_='ImgDestk') or main_article.find('div', class_='Img')).find('img')
            title_elem = (main_article.find('h1') or main_article.find('div', class_='Text')).find('a')  # or for 20110519224238

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'img_url': img_elem.get('src'),
                'category': category,
                'importance': Importance.LARGE
            })

            for article_elem in [(e.find('h2') or e.find('div', class_='Text')).find('a') for e in category_box.find('div', class_='EmentoUltimas').find_all('div', class_='Elemento')]:
                pretitle_elem = article_elem.find('span')
                pretitle = pretitle_elem.get_text() if pretitle_elem else None

                if article_elem.find_previous('div', class_='subject'):
                    pretitle = article_elem.find_previous('div', class_='subject').get_text()

                all_news.append({
                    'article_url': article_elem.get('href'),
                    'title': get_direct_strings(article_elem) or article_elem.find('b').get_text(),
                    'pretitle': pretitle,
                    'category': category,
                    'importance': Importance.SMALL
                })

        return all_news


class ScraperRtpNoticias05(NewsScraper):
    source = 'noticias.rtp.pt'
    cutoff = 20150708170255

    def constrain_category_pretitle(self, category):
        if category in ['Futsal', 'Hóquei', 'Benfica', 'Sporting', 'Seleção Nacional', 'Mundial 2014', 'Ciclismo',
                        'Volta a Portugal', 'FC Porto', 'Rio Ave', 'V. Guimarães', '1.ª Liga', 'V. Setúbal',
                        'Atletismo', 'Fórmula1', 'Motos', 'Andebol', 'Judo', 'Académica']:
            return 'Desporto', category

        if category in ['Eleições Europeias 2014', 'Orçamento do Estado']:
            return 'Política', category

        if category in ['Eleições no Brasil', 'França', 'Eleições na Grécia', 'Alemanha', 'Grécia  Dias decisivos']:
            return 'Mundo', category

        if category in ['LUSAINBOX']:
            return 'Destaques', None

        return category, None

    def scrape_page(self, soup):
        all_news = []

        features = [e for e in soup.find_all('div', class_='Elemento') if (e.find_parent('div', class_='EmDestk') or e.find_parent('div', class_='ColunLeft')) and not e.find_parent('div', class_='Ultimos Especiais')]
        for article_elem in features:
            url_elem = article_elem.find('a', attrs={'itemprop': 'url'})
            title_elem = article_elem.find(re.compile('^(h4|h3)$'), attrs={'itemprop': re.compile(r'^(name|headline)$')})

            snippet_elem = article_elem.find('p', attrs={'itemprop': 'description'})
            snippet = snippet_elem.get_text() if snippet_elem else None

            img_elem = article_elem.find('img', attrs={'itemprop': 'image'}) or article_elem.find('img', class_='pull-left')
            img_url = img_elem.get('src') if img_elem else None

            all_news.append({
                'article_url': url_elem.get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet,
                'img_url': img_url,
                'category': 'Destaques',
                'importance': Importance.FEATURE
            })

            related = article_elem.find('ul', class_='Relacionados')
            if related:
                for title_elem in [e.find('a') for e in related.find_all('li')]:
                    all_news.append({
                        'article_url': title_elem.get('href'),
                        'title': title_elem.get_text(),
                        'category': 'Destaques',
                        'importance': Importance.RELATED
                    })

        latest_elems = [e.find('a') for e in soup.find('div', class_='Ultimos').find_all('li')]
        for article_elem in latest_elems:
            category, pretitle = self.constrain_category_pretitle(article_elem.find('b').get_text().replace('-', '').strip())

            all_news.append({
                'article_url': article_elem.get('href'),
                'title': get_direct_strings(article_elem),
                'headline': pretitle,
                'category': category or 'Destaques',  # 20141031180243
                'importance': Importance.LATEST
            })

        category_boxes = soup.find('div', class_='SectionsHPNews').find_all('div', class_='grid_3')
        for category_box in category_boxes:
            category = category_box.find('h3', class_='head').get_text()

            for article_elem in [e.find('a') for e in category_box.find_all(re.compile(r'^(div|p)$'), class_='Elemento')]:
                img_elem = article_elem.find('img')
                img_url = img_elem.get('src') if img_elem else None

                title_elem = article_elem.find('h4')
                title = title_elem.get_text() if title_elem else get_direct_strings(article_elem)  # large title vs small ones

                all_news.append({
                    'article_url': article_elem.get('href'),
                    'title': title,
                    'img_url': img_url,
                    'category': category,
                    'importance': Importance.LARGE if img_url else Importance.SMALL
                })

        return all_news


class ScraperRtpNoticias06(NewsScraper):
    source = 'noticias.rtp.pt'
    cutoff = 20151231180247  # not tested after this, might keep working

    def parent_name(self, elem):
        return elem.find_parent('section').find('header').get_text()

    def header_admissible(self, text):
        excludes = ['Imagem do', 'Galeria', 'Cinemax']
        for e in excludes:
            if e.lower() in text.lower():
                return False
        return True

    def scrape_page(self, soup):
        all_news = []

        features = [e for e in soup.find_all('div', attrs={'role': 'article'}) if not e.find_parent('div', id=re.compile(r'^(media|emfoco|displaymedia)$')) and self.header_admissible(self.parent_name(e))]
        for article_elem in features:
            url_elem = article_elem.find('a', attrs={'itemprop': 'url'})
            title_elem = article_elem.find(re.compile('^(h2|p|div)$'), attrs={'itemprop': re.compile(r'^(name|headline)$')})

            snippet_elem = article_elem.find('p', class_='small')
            snippet = snippet_elem.get_text() if snippet_elem else None

            img_elem = article_elem.find('img', attrs={'itemprop': 'image'})
            img_url = img_elem.get('src') if img_elem else None

            # determine importance
            parent_name = self.parent_name(article_elem)
            importance = Importance.LATEST if 'Últimas' in parent_name else Importance.FEATURE if 'Principais' in parent_name else Importance.LARGE

            all_news.append({
                'article_url': url_elem.get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet,
                'img_url': img_url,
                'category': 'Desporto' if 'Desporto' in parent_name else 'Destaques',
                'importance': importance
            })

            related = article_elem.find('ul')
            if related:
                for title_elem in [e.find('a') for e in related.find_all('li')]:
                    all_news.append({
                        'article_url': title_elem.get('href'),
                        'title': get_direct_strings(title_elem),
                        'category': 'Destaques',
                        'importance': Importance.RELATED
                    })

        return all_news
