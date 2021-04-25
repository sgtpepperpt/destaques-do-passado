import re
from urllib.parse import unquote_to_bytes

from bs4 import BeautifulSoup

from src.util import generate_dummy_url, get_direct_strings, is_after, get_direct_strings_between, find_comments, \
    find_comments_regex, is_between
from src.text_util import clean_special_chars, remove_clutter

from src.scrapers.news_scraper import NewsScraper, Importance


def red_extract_feature(all_news, main_article):
    title_elem = main_article.find('a', class_='titulo') or main_article.find('font', class_='titulo').find_parent('a') or main_article.find('font', class_='titulo').find('a')

    snippet_elem = main_article.find(re.compile(r'^(td|font)$'), class_='abertura')
    snippet = snippet_elem.get_text() if snippet_elem else None

    img_elems = [e for e in main_article.find_all('img') if not e.get('src').lower().endswith('.gif') and e.get('alt')]
    img_url = img_elems[0].get('src') if len(img_elems) > 0 else None

    all_news.append({
        'article_url': title_elem.get('href'),
        'title': title_elem.get_text(),
        'snippet': snippet,
        'img_url': img_url,
        'category': 'Destaques',
        'importance': Importance.FEATURE
    })


def red_extract_latest(all_news, soup):
    latest_news = soup.find_all('span', class_='noticia_breve')
    for title_elem in [e.find('a') for e in latest_news if e.find('a')]:
        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title_elem.get_text(),
            'category': 'Destaques',
            'importance': Importance.LATEST
        })


def red_extract_large(all_news, soup):
    # extract large features
    # visually a small one appears to be part of this section, but it has no img
    # and is hence a part of a later group of elements caught later
    large_markers = find_comments_regex(soup, r' DESTAQUE SECUNDÁRIO [0-9] ')

    if len(large_markers) == 0:
        raise Exception

    for article_elem in [e.next_sibling.next_sibling for e in large_markers if e.next_sibling.next_sibling.name == 'table']:
        title_elem = article_elem.find('a', class_='titulo_pequeno_info')

        snippet_elem = article_elem.find('span', class_='texto_info')
        snippet = snippet_elem.get_text() if snippet_elem else None

        # find img in left td
        img_elems = [e for e in article_elem.find('td').find_all('img') if not e.get('src').lower().endswith('.gif')]
        img_url = img_elems[0].get('src')

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title_elem.get_text(),
            'snippet': snippet,
            'img_url': img_url,
            'category': 'Destaques',
            'importance': Importance.LARGE
        })


def red_extract_smaller(all_news, soup):
    smaller_articles = soup.find_all('span', class_='titulo_pequeno_info')
    for i in range(len(smaller_articles)):
        title_elem = smaller_articles[i].find('a')
        next_elem = smaller_articles[i + 1] if i + 1 < len(smaller_articles) else None

        # snippet must be between us and the next
        snippet_elem = [e.find('font', attrs={'color': '#000000'}) for e in title_elem.find_all_next('a') if  e.find('font', attrs={'color': '#000000'}) and (is_between(title_elem, next_elem, e) if next_elem else True)]
        snippet = snippet_elem[0].get_text()

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title_elem.get_text(),
            'snippet': snippet,
            'category': 'Destaques',
            'importance': Importance.LARGE
        })


def red_scraper(soup):
    all_news = []

    # test for small red version and large one
    large_version = False
    main_article = find_comments(soup, ' DESTAQUE PRINCIPAL HP')
    if len(main_article) > 0:
        main_article = main_article[0].find_next_sibling('table')
    else:
        main_article = find_comments_regex(soup, r' DESTAQUE PRINCIPAL \* [A-Z]* ')[0].find_next_sibling('table')
        large_version = True

    red_extract_feature(all_news, main_article)

    # important to keep extraction order in case of repeated smaller version of article (only first is kept),
    # so don't put this at the if above
    if large_version:
        red_extract_large(all_news, soup)
        red_extract_smaller(all_news, soup)

    red_extract_latest(all_news, soup)
    return all_news


def modern_scraper(soup):
    all_news = []

    feature = soup.find('span', class_='textodestaquesLead')
    if feature:  # because of noticias.rtp parser, whose pages don't always have this
        feature = feature.find_parent('td')
        title_elem = feature.find('span', class_='textodestaquesLead').find('a')
        snippet_elem = feature.find('font', class_='textogeral12')

        img_elem = [e for e in feature.find('img') if e.find_parent('a')]
        img_url = img_elem[0].get('src') if len(img_elem) > 0 else None

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title_elem.get_text(),
            'snippet': snippet_elem.get_text(),
            'img_url': img_url,
            'category': 'Destaques',
            'importance': Importance.FEATURE
        })

        # get desporto (appears later)
        desporto_article = soup.find('div', class_='DestkHPRTPDesporto')
        if desporto_article:
            title_elem = desporto_article.find('a', class_='Title')
            snippet_elem = desporto_article.find('span', class_='Lead')
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet_elem.get_text(),
                'category': 'Desporto',
                'importance': Importance.LARGE
            })

    # get latest
    latest_articles = soup.find_all('p', class_='textoultimas')
    for title_elem in [e.find('a') for e in latest_articles if e.find('a')]:
        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title_elem.get_text(),
            'category': 'Destaques',
            'importance': Importance.LATEST
        })

    return all_news


class ScraperRtp01(NewsScraper):
    source = 'rtp.pt'
    cutoff = 20040328075115

    # red site

    def scrape_page(self, soup):
        return red_scraper(soup)


class ScraperRtp02(NewsScraper):
    source = 'rtp.pt'
    cutoff = 20080401044447

    # more modern, "not a lot of news" site

    def scrape_page(self, soup):
        return modern_scraper(soup)


class ScraperRtp03(NewsScraper):
    source = 'rtp.pt'
    cutoff = 20091218141946
    minimum_news = 2

    # focused on tv channel, just two article boxes

    def extract_article_new(self, all_news, box, category):
        feature = box.find('div', class_='DestkManchete')
        img_elem = feature.find('a', class_='Imagem').find('img')
        title_elem = feature.find('div', class_='AbsoluteTitle').find('a')
        pretitle_elem = feature.find('div', class_='AbsoluteAnteTitle')

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title_elem.get_text(),
            'pretitle': pretitle_elem.get_text(),
            'img_url': img_elem.get('src'),
            'category': category,
            'importance': Importance.FEATURE
        })

    def extract_article(self, all_news, box, category):
        feature = box.find('div', class_='DestkManchete')
        img_elem = feature.find('a', class_='Img').find('img')
        title_elem = feature.find('span', recursive=False).find('a')

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title_elem.get_text(),
            'img_url': img_elem.get('src'),
            'category': category,
            'importance': Importance.FEATURE
        })

    def scrape_page(self, soup):
        all_news = []

        feature = soup.find('div', id='NoticiasArea')
        if feature.find('div', class_='AbsoluteTitle'):
            self.extract_article_new(all_news, feature, 'Destaques')  # 20090520151017
        else:
            self.extract_article(all_news, feature, 'Destaques')

        feature = soup.find('div', id='DesportoArea')
        if feature.find('div', class_='AbsoluteTitle'):
            self.extract_article_new(all_news, feature, 'Desporto')  # 20090925092650
        else:
            self.extract_article(all_news, feature, 'Desporto')

        return all_news


def get_pretitle_category(category):
    if category in ['Benfica', 'Motores', 'Outras Modalidades', 'FC Porto', 'Seleção Nacional', 'Sporting',
                    'Volta a Portugal 2011', 'Mundial 2014', '1.ª Liga']:
        return category, 'Desporto'

    if category in ['Presidenciais']:
        return category, 'Política'

    if category in ['Guimarães 2012']:
        return category, 'Cultura'

    if category in ['Eleições na Grécia', 'Grécia - Dias decisivos']:
        return category, 'Mundo'

    if category in ['Greve TAP']:
        return category, 'Portugal'

    if category == 'Fórmula1':
        return 'Fórmula 1', 'Desporto'

    # not 1n ignore, but rather to force the default category to be chosen
    if category in ['LUSA-INBOX']:
        return None, None

    return None, category


class ScraperRtp04(NewsScraper):
    source = 'rtp.pt'
    cutoff = 20110906051254
    minimum_news = 20

    def extract_elemento(self, all_news, elemento, is_small=False):
        img_elem = elemento.find('div', class_='Img')
        img_url = img_elem.find('img').get('src') if img_elem else None

        inner_elem = elemento.find('div', class_='Text')
        title_elem = inner_elem.find('h2').find('a')

        # small elements have an h6 or b for category
        elem = title_elem.find(re.compile(r'^(h6|b)$'))
        if elem:
            pretitle, category = get_pretitle_category(clean_special_chars(elem.get_text()))
            title = get_direct_strings(title_elem)
        else:
            category = 'Destaques'
            title = title_elem.get_text()
            pretitle = inner_elem.find('h5').get_text()

        if pretitle and re.match(r'^20[0-9]+-', pretitle):
            raise Exception

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title,
            'headline': pretitle,
            'img_url': img_url,
            'category': category,
            'importance': Importance.SMALL if is_small else Importance.FEATURE
        })

    def extract_tabs(self, all_news, box):
        feature = box.find('div', class_='DestkPrincipal')
        if feature:
            self.extract_elemento(all_news, feature.find('div', class_='Elemento'))

        # two types of small: no image or Elemento
        short_articles = box.find(re.compile(r'^(ul|div)$'), class_='LastNews')
        for title_elem in [e.find('a') for e in short_articles.find_all('li')]:
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'category': 'Destaques',
                'importance': Importance.SMALL
            })

        for elem in short_articles.find_all('div', class_='Elemento'):
            self.extract_elemento(all_news, elem, True)

    def scrape_page(self, soup):
        all_news = []

        # get the "Notícias", "Vídeos" and "Aúdios" tabs since they contains news-worthy titles
        news_boxes = soup.find('div', id='NewsContent').find_all('div', id=re.compile(r'^News_Item_[0-9]$'))[:3]
        for box in news_boxes:
            self.extract_tabs(all_news, box)

        sports_box = soup.find('div', id='SportContent').find_all('div', id=re.compile(r'^Sport_Item_[0-9]$'))[:2]
        for box in sports_box:
            self.extract_tabs(all_news, box)

        return all_news


class ScraperRtp05(NewsScraper):
    source = 'rtp.pt'
    cutoff = 20150708170233
    minimum_news = 1  # because of 20140929030239

    def extract_article(self, all_news, article_elem, category):
        inner_elem = article_elem.find(re.compile(r'^(div|span)$'), class_='Text')
        title_elem = (inner_elem or article_elem).find(re.compile(r'^(h3|h4)$'))
        snippet_elem = (inner_elem or article_elem).find('p', class_=lambda c: c not in ['time'], recursive=False)

        if inner_elem:
            img_elem = article_elem.find('div', class_='Img')
            img_url = img_elem.find('img').get('src') if img_elem else None
            img_category = img_elem.find('img').get('alt') if img_elem else category

            url = title_elem.find('a').get('href')
        else:
            # since 20120202002023
            img_elem = article_elem.find('img')
            img_url = img_elem.get('src') if img_elem else None
            img_category = img_elem.get('alt') if img_elem else category

            url = title_elem.find_parent('a').get('href')

        title = title_elem.get_text()
        if not title:
            return  # 20110928160657

        snippet = snippet_elem.get_text() if snippet_elem else None

        pretitle, compressed_category = get_pretitle_category(img_category)

        all_news.append({
            'article_url': url,
            'title': title,
            'headline': pretitle,
            'snippet': snippet,
            'img_url': img_url,
            'category': compressed_category or category,
            'importance': Importance.FEATURE
        })

        related_elem = (inner_elem or article_elem).find('ul', class_='Relacionados')
        if related_elem:
            for title_elem in [e.find('a') for e in related_elem.find_all('li')]:
                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title_elem.get_text(),
                    'category': category,
                    'importance': Importance.RELATED
                })

    def extract_shorts(self, all_news, main_shorts, category):
        for title_elem in [e.find('a') for e in main_shorts]:
            title = remove_clutter(get_direct_strings(title_elem))
            if not title:
                continue

            all_news.append({
                'article_url': title_elem.get('href') or generate_dummy_url(self.source, 'rtp05', category, title_elem),  # 20111027154751
                'title': title,
                'category': category,
                'importance': Importance.SMALL
            })

    def extract_lateral_vid(self, all_news, article_elem):
        img_elem = article_elem.find('img')
        img_url = img_elem.get('src')
        category = img_elem.get('alt')

        inner_elem = article_elem.find('div', class_='Area')
        title_elem = inner_elem.find('h3').find('a')
        snippet_elem = inner_elem.find('p', recursive=False)

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title_elem.get_text(),
            'snippet': snippet_elem.get_text(),
            'img_url': img_url,
            'category': category,
            'importance': Importance.LARGE
        })

    def extract_lateral_img(self, all_news, article_elem):
        img_elem = article_elem.find('img')
        url_elem = article_elem.find('a')
        snippet_elem = article_elem.find('p', recursive=False)

        title_elem = url_elem.find('h3')

        all_news.append({
            'article_url': url_elem.get('href'),
            'title': title_elem.get_text(),
            'snippet': snippet_elem.get_text(),
            'img_url': img_elem.get('src'),
            'category': 'Outras',
            'importance': Importance.LARGE
        })

    def scrape_page(self, soup):
        all_news = []

        feature_articles = soup.find('div', id='AreaNoticias')
        for article_elem in feature_articles.find_all('div', class_='Elemento'):
            self.extract_article(all_news, article_elem, 'Destaques')

        # top bar dropdowns
        main_articles = soup.find('li', id='noticias').find_all('div', class_='Elemento')
        for article_elem in main_articles:
            self.extract_article(all_news, article_elem, 'Destaques')

        if len(main_articles) > 0:  # until 20121116191502
            main_short = soup.find('li', id='noticias').find('div', class_='LastNews').find(re.compile(r'^(div|ul)$'))
            self.extract_shorts(all_news, main_short.find_all(re.compile(r'^(span|li)$'), recursive=False), 'Destaques')

        desporto_articles = soup.find('li', id='desporto').find_all('div', class_='Elemento')
        for article_elem in desporto_articles:
            self.extract_article(all_news, article_elem, 'Desporto')

        if len(desporto_articles) > 0:
            desporto_short = soup.find('li', id='desporto').find('div', class_='LastNews').find(re.compile(r'^(div|ul)$'))
            self.extract_shorts(all_news, desporto_short.find_all(re.compile(r'^(span|li)$'), recursive=False), 'Desporto')

        lateral_vid_short = soup.find('div', class_='Content MediaDestk VideoInfoArea')
        if lateral_vid_short:
            for article_elem in lateral_vid_short.find_all('div', class_='Elemento'):
                self.extract_lateral_vid(all_news, article_elem)

        lateral_img_short = soup.find('div', class_='Content ImgNews')
        if lateral_img_short:
            for article_elem in lateral_img_short.find_all('div', class_='Elemento'):
                self.extract_lateral_img(all_news, article_elem)

        return all_news


class ScraperRtp06(NewsScraper):
    source = 'rtp.pt'
    cutoff = 20160117180236
    minimum_news = 1  # because of 20151208180229

    def scrape_page(self, soup):
        all_news = []

        articles = soup.find('div', class_='NoticiasHP').find_all('div', role='article')
        for article_elem in articles:
            url_elem = article_elem.find('a', attrs={'itemprop': 'url'})
            img_elem = article_elem.find('img', attrs={'itemprop': 'image'})
            title_elem = article_elem.find(re.compile('^(h2|p)$'), attrs={'itemprop': re.compile(r'^(name|headline)$')})

            snippet_elem = article_elem.find('p', recursive=False)
            snippet = snippet_elem.get_text() if snippet_elem else None

            all_news.append({
                'article_url': url_elem.get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet,
                'img_url': img_elem.get('src'),
                'category': 'Destaques',
                'importance': Importance.FEATURE
            })

        return all_news
