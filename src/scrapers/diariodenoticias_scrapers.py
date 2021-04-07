import re

from bs4 import NavigableString, Comment

from src.util import generate_dummy_url, find_comments
from src.text_util import remove_clutter, clean_special_chars, prettify_text

from src.scrapers.news_scraper import NewsScraper, Importance


def get_direct_strings(elem):
    return remove_clutter(' '.join([e for e in elem.contents if isinstance(e, NavigableString) and not isinstance(e, Comment)]))


class ScraperDiarioDeNoticias02(NewsScraper):
    source = 'dn.pt'
    cutoff = 20010801153425

    def scrape_page(self, soup):
        all_news = []

        title_elems = soup.find_all('font', attrs={'color': '#8c0000'})
        for article_elem in [e.find_parent('table') for e in title_elems]:
            # elements are all inside the previous
            pretitle_elem = article_elem.find('font', attrs={'color': '#000000', 'size': 1})
            pretitle = get_direct_strings(pretitle_elem)

            title_elem = (pretitle_elem or article_elem).find('font', attrs={'color': '#8c0000'})
            title = remove_clutter(title_elem.find_all('b')[0].get_text())

            if not title:
                continue  # missing title at 19991010052929

            snippet_elem = title_elem.find('font', attrs={'size': 3})
            snippet = get_direct_strings(snippet_elem)

            if snippet and ('Reportagem no' in snippet or 'Crónica de' in snippet):
                continue  # stuff that isn't archived then

            url_elem = [e.find_parent('a') for e in snippet_elem.find_all('img') if e.get('src').endswith('.gif')]
            url = url_elem[0].get('href') if len(url_elem) > 0 else generate_dummy_url(self.source, 'parser02', pretitle, title)

            img_elem = [e.get('src') for e in article_elem.find_all('img') if e.get('src').endswith('.jpg')]
            img_url = img_elem[0] if len(img_elem) > 0 else None

            all_news.append({
                'article_url': url,
                'headline': pretitle if len(pretitle) > 0 else None,
                'title': title,
                'snippet': prettify_text(snippet),
                'img_url': img_url,
                'category': 'Destaque',
                'importance': Importance.FEATURE if img_url else Importance.LARGE if snippet else Importance.SMALL
            })

        return all_news


class ScraperDiarioDeNoticias04(NewsScraper):
    source = 'dn.pt'
    cutoff = 20041019082233

    def scrape_page(self, soup):
        all_news = []

        # colourful top headers
        top_features = soup.find('table', attrs={'width': 460})
        if top_features:
            top_features = top_features.find_all('tr')  # 20021201081654, edited top table out because of html error

            title_elems = top_features[1].find_all('a', class_='destaques4')
            category_elems = top_features[0].find_all('a', class_='destaques4')
            for i in range(len(title_elems)):
                title_elem = title_elems[i]

                category = category_elems[i].get_text()
                m = re.match(r'(.*)\s*[0-9][0-9]:[0-9][0-9]', category)  # remove the hour
                if m:
                    category = m.group(1)

                if clean_special_chars(category).lower() in ['dossier', 'verão']:
                    continue

                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': remove_clutter(title_elem.get_text()),
                    'category': clean_special_chars(category),
                    'importance': Importance.LARGE
                })

        # TSF section
        tsf_articles = soup.find('table', attrs={'bgcolor': '#FF9700'}).find_all('tr')
        for article_elem in [e.find('td', attrs={'width': re.compile(r'^16[0-2]$')}) for e in tsf_articles]:
            pretitle_elem = article_elem.find(re.compile(r'a|span'), class_='footer6')
            title_elem = article_elem.find(re.compile(r'a|span'), class_='resume')
            url_elem = title_elem.find_parent('a') if title_elem.name == 'span' else title_elem

            all_news.append({
                'article_url': url_elem.get('href'),
                'headline': pretitle_elem.get_text(),
                'title': title_elem.contents[0],  # first navigable string only
                'category': 'Destaque',
                'importance': Importance.SMALL
            })

        # the rest of the elements have no titles, so don't fit the website model...

        return all_news


class ScraperDiarioDeNoticias05(NewsScraper):
    source = 'dn.pt'
    cutoff = 20081022054427

    def scrape_page(self, soup):
        all_news = []

        # main features
        category = 'Destaque'
        for article_elem in soup.find_all('table', attrs={'width': re.compile(r'279|450|569')}):
            category_elem = article_elem.find('span', class_='arial_10_cinza_escuro')
            if category_elem:
                category = clean_special_chars(category_elem.get_text())
                continue

            # avoid promotional stuff
            promo_comment = find_comments(article_elem, ' promocoes_centro ')
            if len(promo_comment) > 0:
                continue

            pretitle_elem = article_elem.find('span', class_='arial_10_cinzaclaro')
            pretitle = pretitle_elem.get_text().title() if pretitle_elem else None

            title_elem = article_elem.find('span', class_='arial_azul_escuro_b')
            snippet_elem = article_elem.find('span', class_='arial_noticias_cinza')

            img_elems = article_elem.find_all('img', attrs={'src': re.compile(r'.jpg$')})
            img_url = img_elems[0].get('src') if len(img_elems) > 0 else None

            all_news.append({
                'article_url': title_elem.find_parent('a').get('href'),
                'title': remove_clutter(title_elem.get_text()),
                'headline': pretitle,
                'snippet': snippet_elem.get_text(),
                'img_url': img_url,
                'category': clean_special_chars(category),
                'importance': Importance.FEATURE
            })

        # get categories
        category_articles = soup.find('table', attrs={'bordercolor': '#F1F1F1'}).find_all('span', class_='arial_10_cinza_escuro')
        for article_elem in [e.find_parent('div') for e in category_articles]:
            title_elem = article_elem.find('span', class_='arial_10_azul_esc')
            category = article_elem.find('span', class_='arial_10_cinza_escuro').get_text()

            all_news.append({
                'article_url': title_elem.find_parent('a').get('href'),
                'title': remove_clutter(title_elem.get_text()),
                'category': clean_special_chars(category),
                'importance': Importance.SMALL
            })

        # get latest
        latest_elems = soup.find('div', id='destdir')
        if latest_elems:
            for article_elem in [e.find_parent('a') for e in latest_elems.find_all('span', class_='arial_10_cinza_escuro')]:
                pretitle_elem = article_elem.find('span', class_='arial_10_cinza_escuro')
                title_elem = article_elem.find('span', class_='arial_10_cinzaclaro')

                all_news.append({
                    'article_url': title_elem.find_parent('a').get('href'),
                    'title': remove_clutter(title_elem.get_text()),
                    'pretitle': pretitle_elem.get_text(),
                    'category': 'Outras',
                    'importance': Importance.LATEST
                })

        return all_news


class ScraperDiarioDeNoticias06(NewsScraper):
    source = 'dn.pt'
    cutoff = 20151013180422

    def get_related(self, all_news, related_elems, category):
        for title_elem in [e.find('a') for e in related_elems]:
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'category': category,
                'importance': Importance.RELATED
            })

    def extract_article(self, all_news, article_elem, category):
        title_elem = article_elem.find('h3', class_=re.compile(r'^destaque(640)?-tit-not$')) or article_elem.find('h4')
        if not title_elem:
            return  # 20110119160220, article without title

        title_elem = title_elem.find('a')
        title = remove_clutter(title_elem.get_text())

        if not title or title.lower() == 'tudo sobre o combate ao défice':
            return  # 20100514140118, not a news article

        snippet_elem = article_elem.find('p', recursive=False)

        pretitle_elem = article_elem.find('h5', class_='dest-anttit')
        pretitle = pretitle_elem.get_text() if pretitle_elem else None

        # grab image, deal with no a tag, a tag but no img tag, or both and then get the src
        img_elem = article_elem.find('a', recursive=False)
        img_url = None
        if img_elem:
            img_elem = img_elem.find('img')
            img_url = img_elem.get('src') if img_elem else None

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title,
            'headline': pretitle,
            'snippet': snippet_elem.get_text(),
            'img_url': img_url,
            'category': category,
            'importance': Importance.LARGE
        })

        # add related
        related_elems = article_elem.find('div', class_='cx-listas')
        if related_elems:
            self.get_related(all_news, related_elems.find_all('li'), category)

    def scrape_page(self, soup):
        all_news = []

        # main feature
        feature_box = soup.find('div', id='ctl00_ctl00_ctl00_bcr_bcr_middlecontent_bcr_Manchetes_ctl00_contentDiv')
        for article_elem in feature_box.find_all('div', recursive=False):
            header_elem = article_elem.find('div', class_='cx-noticias-cor-topo').find('div', class_=re.compile(r'cx-noticias-cor-titulos(-ccc)?'))
            lower_elem = article_elem.find('div', class_='cx-noticias-cor-txt')

            # find img element
            img_elems = [e for e in article_elem.find_all('img') if not e.find('div', class_='cx-noticias-cor-topo') and not e.find('div', class_='cx-noticias-cor-txt') and not e.get('src').endswith('.gif')]
            img_url = img_elems[0].get('src') if len(img_elems) > 0 else None

            # extract title and pretitle
            pretitle_elem = header_elem.find('h5')
            pretitle = pretitle_elem.get_text() if pretitle_elem else None

            title_elem = header_elem.find('h2').find('a')

            # extract snippet
            snippet_elem = lower_elem.find('p')

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'headline': pretitle,
                'snippet': snippet_elem.get_text(),
                'img_url': img_url,
                'category': 'Destaque',
                'importance': Importance.FEATURE
            })

            # add related
            related_elems = lower_elem.find('div', class_='cx-listas')
            if related_elems:
                self.get_related(all_news, related_elems.find_all('li'), 'Destaque')

        # large articles
        large_box = soup.find('div', id=re.compile(r'ctl00_ctl00_ctl00_bcr_bcr_middlecontent_bcr_DestaquesC1?_ctl00_contentDiv'))
        for article_elem in [e.find('td') for e in large_box.find_all('div', class_='destaque')]:
            self.extract_article(all_news, article_elem, 'Destaque')

        # desporto box
        desporto_box = soup.find('div', class_='cx-desporto-txt-n0')

        # desporto large
        desporto_large_articles = desporto_box.find_all('div', id=re.compile(r'ctl00_ctl00_ctl00_bcr_bcr_middlecontent_bcr_Desporto1_Destaque_ctl[0-9][0-9]_contentDiv'))
        for article_elem in desporto_large_articles:
            img_url = article_elem.find('div', class_='vid-desporto').find('img').get('src')

            text_elem = article_elem.find('div', class_='tab-desporto-impar')
            title_elem = text_elem.find('h5').find('a')
            snippet_elem = text_elem.find('p', recursive=False)

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet_elem.get_text(),
                'img_url': img_url,
                'category': 'Desporto',
                'importance': Importance.LARGE
            })

        # desporto small
        desporto_articles = desporto_box.find_all('div', class_=re.compile(r'^tab-desporto-(im)?par$'))[len(desporto_large_articles):]  # exclude the large divs, captured above
        for title_elem in [e.find('h5').find('a') for e in desporto_articles]:
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'category': 'Desporto',
                'importance': Importance.SMALL
            })

        # sections
        section_boxes = soup.find_all('div', id=re.compile(r'ctl00_ctl00_ctl00_bcr_bcr_middlecontent_ctl[0-9][0-9]_ngContent_ctl00_contentDiv'))
        all_articles = []
        for elem in section_boxes:
            all_articles += elem.find_all('div', class_='destaque')

        for article_elem in [e.find('td') for e in all_articles]:
            category = article_elem.find_previous('div', class_='tit-icn-seccoes').find_parent('div').find('h5').get_text()
            self.extract_article(all_news, article_elem, category)

        # narrow column articles
        narrow_box = soup.find('div', id='cln-mid-n2')

        uncategorised_articles = narrow_box.find('div', id='ctl00_ctl00_ctl00_bcr_bcr_bbcr_bbcr_DestaquesD_ctl00_contentDiv').find_all('div', class_=lambda name: name != 'line6', recursive=False)
        for article_elem in uncategorised_articles:
            self.extract_article(all_news, article_elem, 'Destaque')

        category_articles = narrow_box.find_all('div', id=re.compile(r'^ctl00_ctl00_ctl00_bcr_bcr_bbcr_\w*_ngContent_ctl00_contentDiv$'))
        for article_elem in category_articles:
            title_elem = (article_elem.find('h5', class_='tit-sublinhado') or article_elem.find('h4', class_='tit-pessoas-itl')).find('a')
            snippet_elem = article_elem.find('p', class_='tit-sublinhado')

            img_elem = article_elem.find('img')
            img_url = img_elem.get('src') if img_elem else None

            category = article_elem.find_previous('div', class_='tit-icn-seccoes').find_parent('div').find('h5').get_text()

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet_elem.get_text(),
                'img_url': img_url,
                'category': category,
                'importance': Importance.LARGE
            })

            # add related
            related_elems = article_elem.find('div', class_='cx-listas-espacadas')
            if related_elems:
                self.get_related(all_news, related_elems.find_all('li'), category)

        return all_news


class ScraperDiarioDeNoticias07(NewsScraper):
    source = 'dn.pt'
    cutoff = 20151231180223  # not tested after this

    def scrape_page(self, soup):
        all_news = []

        # main feature
        article_elems = soup.find_all('article')
        for article_elem in article_elems:
            # remove football results article
            if article_elem.find('h3', id='jornada_atual'):
                continue

            title_elem = article_elem.find('h2', attrs={'itemprop': 'headline'})

            pretitle_elem = article_elem.find('h3', attrs={'itemprop': 'articleSection'})
            pretitle = pretitle_elem.get_text().title() if pretitle_elem else None

            # pretitle ignores
            if pretitle in ['Perfil']:
                continue

            snippet_elem = article_elem.find('h4', attrs={'itemprop': 'description'})
            snippet = snippet_elem.get_text() if snippet_elem else None

            img_elem = article_elem.find('figure')
            img_url = img_elem.find('img').get('data-src') if img_elem else None

            category = 'Destaque'
            parent_section = article_elem.find_parent('section')
            if parent_section:
                # if we are in a section, we need see if the header has something
                header = parent_section.find('header').find('h2')
                if header:
                    category = clean_special_chars(header.find('span').get_text())

                    # sanitise category
                    if category in ['O país à espera', 'Novo Governo', 'O país de novo à espera', 'Novo governo']:
                        category = 'Política'
                    elif category in ['Em Portugal']:
                        category = 'Portugal'
                    elif category in ['No Mundo']:
                        category = 'Mundo'
                    elif category in ['Mundial de Surf', 'Surf em Peniche']:
                        category = 'Desporto'

            # category ignores
            if category in ['Galerias e Vídeos', 'Evasões', 'Notícias Maganize', 'Notícias Magazine', 'Estreiam hoje', 'DN Ilustrado', 'Estreias', 'Os mais lidos de 2015', 'Edição especial 151º aniversário']:
                continue

            all_news.append({
                'article_url': title_elem.find_parent('a').get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet,
                'headline': pretitle,
                'img_url': img_url,
                'category': category,
                'importance': Importance.FEATURE if img_url and snippet else Importance.LARGE if img_url else Importance.SMALL
            })

            # get related elements
            related_articles = article_elem.find('nav', class_='t-article-related-1')
            if related_articles:
                for related_elem in [e.find('a') for e in related_articles.find_all('li')]:
                    all_news.append({
                        'article_url': related_elem.get('href'),
                        'title': related_elem.find('span').get_text(),
                        'category': category,
                        'importance': Importance.RELATED
                    })

        # get topbar latest news
        latest_elems = soup.find_all('div', class_='t-main-topbar-newslist')
        if len(latest_elems) > 0:
            # ignore "ao vivo"
            latest_elems = [e for e in latest_elems if 'Última Hora' in e.find_parent('div').find('strong').get_text()]
            if len(latest_elems) > 0:
                for title_elem in [e.find('a') for e in latest_elems[0].find_all('li')]:
                    all_news.append({
                        'article_url': title_elem.get('href'),
                        'title': title_elem.get_text(),
                        'category': 'Outras',
                        'importance': Importance.LATEST
                    })

        return all_news
