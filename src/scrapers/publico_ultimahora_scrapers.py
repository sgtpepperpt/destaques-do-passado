import re
from urllib.parse import unquote_to_bytes

from bs4 import BeautifulSoup

from src.util import generate_dummy_url, get_direct_strings, is_after, get_direct_strings_between
from src.text_util import clean_special_chars

from src.scrapers.news_scraper import NewsScraper, Importance


class ScraperPublicoUltimaHora01(NewsScraper):
    source = 'ultimahora.publico.pt'
    cutoff = 20001019030350
    minimum_news = 1

    def process_large_article(self, all_news, soup):
        article_table = soup.find('div').find_all('table', recursive=False)[-1].find_all('tr', recursive=False)

        header_elem = article_table[4].find('font')
        title_elem = article_table[5].find('font')
        snippet_elem = article_table[6]
        snippet = get_direct_strings([e.find('p') for e in article_table[6].find_all('font', attrs={'size': 2}) if not e.find('strong')][0])#.get_text()

        img_elem = [e for e in snippet_elem.find_all('img') if not e.get('src').lower().endswith('.gif')]
        img_url = img_elem[0].get('src') if len(img_elem) > 0 else None

        all_news.append({
            'article_url': generate_dummy_url(self.source, header_elem, snippet_elem, title_elem),
            'title': title_elem.get_text(),
            'headline': header_elem.get_text().split('-')[0],
            'snippet': snippet,
            'img_url': img_url,
            'category': 'Destaques',
            'importance': Importance.FEATURE
        })

    def process_article_list(self, all_news, soup):
        article_elems = soup.find_all('a', attrs={'target': 'centro'})
        for title_elem in article_elems:
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'category': 'Destaques',
                'importance': Importance.SMALL
            })

    def scrape_page(self, soup):
        all_news = []

        # two types of pages at this point (were two different frames), news article or short list of latest news
        if soup.find('body', attrs={'bgcolor': '#FDE1AF'}):
            self.process_large_article(all_news, soup)
        else:
            self.process_article_list(all_news, soup)

        return all_news


class ScraperPublicoUltimaHora02(NewsScraper):
    source = 'ultimahora.publico.pt'
    cutoff = 20030220182006

    def extract_categories(self, all_news, category_titles, header_class, split_title=False):
        for category_elem in category_titles:
            category = category_elem.find('a', class_=header_class).get_text()

            if category in ['CARTAS']:
                continue

            for title_elem in category_elem.find_all('a', class_='ultseccoesnot'):
                title = title_elem.get_text()
                pretitle = None

                if split_title:
                    split = title.split(':')
                    title = split[1]
                    pretitle = split[0]

                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title,
                    'headline': pretitle,
                    'category': category,
                    'importance': Importance.SMALL
                })

    def scrape_page(self, soup):
        all_news = []

        for article_elem in [e.find_parent('table', attrs={'width': 530}) for e in soup.find_all('a', class_='ultnottit')]:
            # category_elem = article_elem.find('a', class_='ultnotseccao')  # let it be destaques, that way it'll show at top in the site
            pretitle_elem = article_elem.find('span', class_='ultnotsubtit')
            title_elem = article_elem.find('a', class_='ultnottit')
            snippet_elem = article_elem.find('span', class_='ultnottxt')

            img_elems = [e for e in article_elem.find_all('img') if not e.get('src').lower().endswith('.gif')]
            img_url = img_elems[0].get('src') if len(img_elems) > 0 else None

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'headline': pretitle_elem.get_text(),
                'snippet': snippet_elem.get_text(),
                'img_url': img_url,
                'category': 'Destaques',
                'importance': Importance.FEATURE
            })

        category_titles = [e.find_parent('table').find_parent('td') for e in soup.find_all('a', class_='ultseccoestit')]
        self.extract_categories(all_news, category_titles, 'ultseccoestit')

        large_category_titles = [e.find_parent('table') for e in soup.find_all('a', class_='ultinqueritotit')]
        self.extract_categories(all_news, large_category_titles, 'ultinqueritotit', True)

        latest_articles = soup.find_all('a', class_='ultimasnoticia')
        for title_elem in latest_articles:
            # the previous sibling check ensures we don't just get a previous element's category, it has to be directly before us
            category = title_elem.find_parent('tr').find_previous_sibling('tr').find('a', class_='ultimasseccao').get_text()

            if category in ['Trânsito']:
                continue

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'category': category,
                'importance': Importance.LATEST
            })

        return all_news


class ScraperPublicoUltimaHora03(NewsScraper):
    source = 'ultimahora.publico.pt'
    cutoff = 20050221014617

    # looks the same as before, somewhat different html however

    def extract_categories(self, all_news, category_titles, header_class, articles_class, split_title=False):
        for category_elem in category_titles:
            category = category_elem.find('td', class_=header_class).get_text()

            if category in ['CARTAS']:
                continue

            for title_elem in [e.find('a') for e in category_elem.find_all('td', class_=articles_class)]:
                title = title_elem.get_text().replace('•', '')
                pretitle = None

                if split_title:
                    split = title.split(':')
                    title = split[1]
                    pretitle = split[0]

                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title,
                    'headline': pretitle,
                    'category': category,
                    'importance': Importance.SMALL
                })

    def scrape_page(self, soup):
        all_news = []

        # locate features box
        feature_rows = soup.find('td', class_='cabeca1').find_parent('table', attrs={'width': 530}).find_all('tr', recursive=False)
        for i in range(len(feature_rows)):
            category_elem = feature_rows[i].find('td', class_='cabeca1')
            if not category_elem:
                continue

            upper_elem = feature_rows[i+2].find('p')
            lower_elem = feature_rows[i+4]

            pretitle_elem = upper_elem.find('span', class_='textoAntetitulo')
            title_elem = upper_elem.find('a', class_='textoTitulo')
            snippet_elem = lower_elem.find('td', class_='texto')

            img_elem = lower_elem.find_all('td')[-1].find('img')
            img_url = img_elem.get('src') if img_elem else None

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'headline': pretitle_elem.get_text(),
                'snippet': get_direct_strings(snippet_elem),
                'img_url': img_url,
                'category': 'Destaques',
                'importance': Importance.FEATURE
            })

            i += 5  # +1 added by for

        category_titles = [e.find_parent('table') for e in soup.find_all('td', class_='cabeca2')]
        self.extract_categories(all_news, category_titles, 'cabeca2', 'caixasBaixo')

        large_category_titles = [e.find_parent('table') for e in soup.find_all('td', class_='cabeca1') if is_after(feature_rows[-1], e)]
        self.extract_categories(all_news, large_category_titles, 'cabeca1', 'bkgdDesporto', True)

        latest_articles = soup.find('td', class_='esqCaixaCinza2').find_all('p', recursive=False)
        for article_elem in latest_articles:
            category = get_direct_strings(article_elem) or get_direct_strings(article_elem.find('br'))
            title_elem = article_elem.find('strong').find('a')

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'category': category or 'Destaques',
                'importance': Importance.LATEST
            })

        return all_news


class ScraperPublicoUltimaHora04(NewsScraper):
    source = 'ultimahora.publico.pt'
    cutoff = 20071109125414
    minimum_articles = 20

    def scrape_page(self, soup):
        all_news = []

        features = [e.find_parent('tr') for e in soup.find_all('div', id='caixasNoticias')]
        for article_elem in features:
            cells = article_elem.find_all('td', recursive=False)

            img_elem = cells[0].find('img') if len(cells) > 1 else None
            img_url = img_elem.get('src') if img_elem else None

            inner_elem = article_elem.find('div', id='caixasNoticias')
            title_elem = inner_elem.find('span', class_='manchete').find('a')
            pretitle = get_direct_strings_between(inner_elem, inner_elem, title_elem)

            snippet_elem = inner_elem.find('div', id='texto')
            snippet = snippet_elem.find('p').get_text() if snippet_elem.find('p') else get_direct_strings(snippet_elem)

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'headline': pretitle,
                'snippet': snippet,
                'img_url': img_url,
                'category': 'Destaques',
                'importance': Importance.FEATURE
            })

            related_elems = snippet_elem.find_all('div', id='seccaoTitulo')
            for title_elem in [e.find('a') for e in related_elems]:
                url = title_elem.get('href')
                if url.endswith('www.inag.pt') or url.endswith('www.oscars.com'):
                    continue  # 20060111072239, 20060131182206

                all_news.append({
                    'article_url': url,
                    'title': title_elem.get_text(),
                    'category': 'Destaques',
                    'importance': Importance.RELATED
                })

        category_boxes = soup.find_all('td', id='caixaSeccoes')
        for category_box in category_boxes:
            category_elem = category_box.find('div', id='linhaTitulosHeader')
            if not category_elem:
                continue  # empty elem

            article_elems = category_box.find_all('div', id='seccaoTitulo')
            for title_elem in [e.find('a') for e in article_elems]:
                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title_elem.get_text(),
                    'category': category_elem.get_text(),
                    'importance': Importance.SMALL
                })

        latest_articles = soup.find('div', id='ultimasNoticias')
        if latest_articles:
            for elem in latest_articles.find_all('script', recursive=False):
                # the latest section items were encoded as escaped js scripts, so unescape and parse with bs4...
                text = unquote_to_bytes(elem.string.split('unescape')[-1].replace('(\'', '').replace('\'));', '')).decode('ISO-8859-1')
                title_elem = BeautifulSoup(text, 'html.parser').find('div', id='seccaoTitulo').find('a')

                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': get_direct_strings(title_elem),
                    'category': title_elem.find('b').get_text().replace(':', ''),
                    'importance': Importance.LATEST
                })

        main_table_latest_articles = [e for e in soup.find_all('div', id='cabecaMenu') if e.get_text() == 'ÚLTIMAS NOTÍCIAS DESTA SECÇÃO']
        if len(main_table_latest_articles) > 0:
            # doesn't appear at first
            main_table_latest_articles = main_table_latest_articles[0].find_parent('tr').find_next_sibling('tr').find_all('div', id='seccaoTitulo')
            for title_elem in [e.find('a') for e in main_table_latest_articles]:
                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': get_direct_strings(title_elem).replace('-', ''),
                    'category': 'Destaques',
                    'importance': Importance.LATEST
                })

        return all_news


class ScraperPublicoUltimaHora05(NewsScraper):
    source = 'ultimahora.publico.pt'
    cutoff = 20090925042626  # no more ultimahora after
    minimum_articles = 80

    def scrape_page(self, soup):
        all_news = []

        main_articles = [e.find_parent('td') for e in soup.find_all('div', id=re.compile(r'^ctl[0-9]+_ContentPlaceHolder[0-9]_DestaqueTitulo$'))]
        for article_elem in main_articles:
            img_elem = article_elem.find('table', id=re.compile(r'^ctl[0-9]+_ContentPlaceHolder[0-9]_TableImagem$'))
            img_url = img_elem.find('img').get('src') if img_elem else None

            pretitle_elem = article_elem.find('div', id=re.compile(r'^ctl[0-9]+_ContentPlaceHolder[0-9]_DestaqueSubtitulo$'))
            title_elem = article_elem.find('div', id=re.compile(r'^ctl[0-9]+_ContentPlaceHolder[0-9]_DestaqueTitulo$')).find('a')
            snippet_elem = article_elem.find('div', id=re.compile(r'^ctl[0-9]+_ContentPlaceHolder[0-9]_DestaqueTexto$'))

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'headline': pretitle_elem.get_text(),
                'snippet': snippet_elem.get_text(),
                'img_url': img_url,
                'category': 'Destaques',
                'importance': Importance.FEATURE
            })

        large_articles = [e.find_all('div', recursive=False) for e in soup.find_all('td', id=re.compile(r'^ctl00_ContentPlaceHolder1_(Left|Right)Cell$'))]
        for article_elem in large_articles[0] + large_articles[1]:
            title_elem = article_elem.find('div', class_='manchete_16').find('a')
            snippet_elem = article_elem.find('div', class_='verdana_11_gray')

            img_elem = article_elem.find('img', class_='borderCinzaFotosUHHP')
            img_url = img_elem.get('src') if img_elem else None

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet_elem.get_text(),
                'img_url': img_url,
                'category': 'Destaques',
                'importance': Importance.LARGE
            })

            related_elems = article_elem.find_all('span', class_='verdana_10_blue')
            for title_elem in [e.find('a') for e in related_elems]:
                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title_elem.get_text(),
                    'category': 'Destaques',
                    'importance': Importance.RELATED
                })

        latest_articles_main = soup.find('table', id='ctl00_ContentPlaceHolder1_Ultimas_TableNews').find_all('a', class_='georgia_11_black')
        for title_elem in latest_articles_main:
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'category': 'Destaques',
                'importance': Importance.LATEST
            })

        category_sections = [e.find_all('table') for e in soup.find_all('td', id=re.compile(r'^ctl00_ContentPlaceHolder1_UltimasPorCanal_(left|Rigth)Cell$'))]
        for category_elem in category_sections[0] + category_sections[1]:
            category = category_elem.find('div', class_='cabecasSeparadores').get_text()

            for title_elem in [e.find('a') for e in category_elem.find_all('span', class_='verdana_10_blue')]:
                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title_elem.get_text(),
                    'category': category,
                    'importance': Importance.SMALL
                })

        latest_right_elems = soup.find('table', id='ctl00_Direita_Tops_TableNoticias').find_all('a', class_='verdana_10_black')
        for article_elem in latest_right_elems:
            category = clean_special_chars(article_elem.find('b').get_text().replace(':', ''))
            pretitle = None

            if category in ['Fc Porto', 'Futebol Nacional', 'Râguebi', 'Futebol Internacional']:
                pretitle = category
                category = 'Desporto'

            all_news.append({
                'article_url': article_elem.get('href'),
                'title': get_direct_strings(article_elem),
                'headline': pretitle,
                'category': category,
                'importance': Importance.LATEST
            })

        return all_news
