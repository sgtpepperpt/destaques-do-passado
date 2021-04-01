import re

from bs4 import NavigableString, Comment

from src.util import prettify_text, ignore_title, remove_clutter, is_between, generate_dummy_url, clean_spacing, \
    clean_special_chars, find_comments

from src.scrapers.news_scraper import NewsScraper, Importance


class ScraperExpresso01(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20000302151731

    def scrape_page(self, soup):
        all_news = []

        last_snippet_elem = soup.contents[0]

        titles = soup.find_all('font', attrs={'size': 5})
        for title_elem in [title.find('b') for title in titles if title.find('b')]:
            title = title_elem.get_text(separator=' ')

            snippet_elem = title_elem.find_next('font', attrs={'size': 3})
            snippet = snippet_elem.get_text()

            url_elem = [e for e in snippet_elem.find_all('a') if e.find('img')][-1]
            url = url_elem.get('href')

            img_elem = [e.find('img') for e in soup.find_all('a') if is_between(title_elem, url_elem, e) and e.find('img') and e.find('img').get('src').endswith('.jpg')]
            img = img_elem[0].get('src') if img_elem else None

            headline_elems = title_elem.find_previous('font', attrs={'size': 4, 'color': re.compile(r'(#CF2D16|#8E0000)')})
            headline = None
            if headline_elems:
                headlines = [e for e in headline_elems if is_between(last_snippet_elem, title_elem, e)]
                if headlines:
                    headline = remove_clutter(headlines[0].get_text())

            last_snippet_elem = snippet_elem  # to find next headline

            all_news.append({
                'article_url': url,
                'title': remove_clutter(title),
                'snippet': prettify_text(snippet),
                'img_url': img,
                'headline': headline,
                'category': 'Destaque',
                'importance': Importance.LARGE
            })

        # colourful boxes
        titles = soup.find_all('font', attrs={'size': 3})
        titles = [t for t in titles if t.find_parent('td', attrs={'bgcolor': re.compile(r'(#CF2D16|#8E0000)')}) and not t.get('face')]  # find the face attr to avoid repetitions
        for title_elem in titles:  # avoid a repetition
            snippet_elem = title_elem.find_next('td', attrs={'bgcolor': '#A2BECB'}).find('font', attrs={'size': 3})
            snippet = snippet_elem.get_text()

            url_elem = snippet_elem.find_all('a')
            url = None
            if len(url_elem) > 0:
                url_elem = url_elem[-1] # always last link
                url = url_elem.get('href')

            img_elem = [e.find('img') for e in soup.find_all('a') if is_between(title_elem, url_elem or snippet_elem, e) and e.find('img') and e.find('img').get('src').endswith('.jpg')]
            img = img_elem[0].get('src') if img_elem else None

            # if url wasn't founnd before try in image
            if img_elem:
                url = img_elem[0].find_parent('a').get('href')

            headline_elem = title_elem.find_parent('td', attrs={'bgcolor': re.compile(r'(#CF2D16|#8E0000)')}).find('font', attrs={'size': 2})
            headline = None
            if headline_elem:
                headline = headline_elem.get_text()

            all_news.append({
                'article_url': url,
                'title': remove_clutter(title_elem.get_text()),
                'snippet': prettify_text(snippet),
                'img_url': img,
                'headline': remove_clutter(headline),
                'category': 'Destaque',
                'importance': Importance.LARGE
            })

        # latest and short news
        latest_banner1 = soup.find('img', attrs={'src': re.compile(r'.*24_horas.gif')})
        latest_news = latest_banner1.find_next('blockquote').find_all('font', attrs={'size': 3})

        latest_banner2 = soup.find('img', attrs={'src': re.compile(r'.*ultimas.gif')})
        if latest_banner2:
            latest_news += latest_banner2.find_next('blockquote').find_all('font', attrs={'size': 3})

        for article_elem in [article.find('b') for article in latest_news]:
            all_news.append({
                'article_url': article_elem.find_next('a').get('href'),
                'title': remove_clutter(article_elem.get_text()),
                'category': 'Outras',
                'importance': Importance.LATEST
            })

        return all_news


class ScraperExpresso02(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20000510015940

    def scrape_page(self, soup):
        all_news = []

        last_snippet_elem = soup.contents[0]

        categories = [c for c in soup.find_all('a') if c.get('name')]  # find the closest category, starting from below (otherwise all news would be the first category)
        categories.reverse()

        titles = soup.find_all('span', class_='ad-pu-titulo')
        for title_elem in titles:
            title = title_elem.get_text(separator=' ')

            snippet_elem = title_elem.find_next('span', class_='ad-pu-corpo')
            snippet = snippet_elem.get_text()

            url_elem = title_elem.find_parent('a', class_='titulo')
            url = url_elem.get('href')

            img_elem = [e for e in soup.find_all('img') if is_between(title_elem, snippet_elem, e)]
            img = img_elem[0].get('src') if img_elem else None

            headline_elems = title_elem.find_previous('span', class_='ad-pu-antetitulo')
            headline = None
            if headline_elems:
                headlines = [e for e in headline_elems if is_between(last_snippet_elem, title_elem, e)]
                if headlines:
                    headline = remove_clutter(headlines[0])

            last_snippet_elem = snippet_elem  # to find next headline

            # find category
            category = self.find_category(categories, soup.contents[0], title_elem)

            all_news.append({
                'article_url': url,
                'title': remove_clutter(title),
                'snippet': prettify_text(snippet),
                'img_url': img,
                'headline': headline,
                'category': category,
                'importance': Importance.LARGE
            })

        related_elems = soup.find_all('td', class_='ad-artigo-titulo-relacionado')
        for elem in [e.find('a') for e in related_elems]:
            all_news.append({
                'article_url': elem.get('href'),
                'title': remove_clutter(elem.get_text()),
                'category': self.find_category(categories, soup.contents[0], elem),
                'importance': Importance.RELATED
            })

        return all_news

    def find_category(self, categories, document_start, title_elem):
        elligible_categories = [c for c in categories if is_between(document_start, title_elem, c)]
        if len(elligible_categories) > 0:
            return elligible_categories[0].get('name')
        else:
            return 'Destaque'


class ScraperExpresso03(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20000520032636

    def scrape_page(self, soup):
        # design goes back in time
        return ScraperExpresso01().scrape_page(soup)


class ScraperExpresso04(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20001018012510

    last_snippet_elem = None

    def extract_articles(self, soup, title_elem, headline_class, category, importance):
        title = title_elem.get_text()

        snippet_elem = title_elem.find_next('span', class_='primeira-corpo')
        snippet = snippet_elem.get_text()

        url_elem = title_elem.find_parent('a', class_='link-k')
        url = url_elem.get('href')

        img_elem = [e for e in soup.find_all('img') if is_between(title_elem, snippet_elem, e)]
        img = img_elem[0].get('src') if img_elem else None

        headline_elems = title_elem.find_previous('span', class_=headline_class)
        headline = None
        if headline_elems:
            headlines = [e for e in headline_elems if is_between(self.last_snippet_elem, title_elem, e)]
            if headlines:
                headline = remove_clutter(headlines[0])

        self.last_snippet_elem = snippet_elem  # to find next headline

        return {
            'article_url': url,
            'title': remove_clutter(title),
            'snippet': prettify_text(snippet),
            'img_url': img,
            'headline': headline,
            'category': category,
            'importance': importance
        }

    def scrape_page(self, soup):
        all_news = []

        self.last_snippet_elem = soup.contents[0]

        titles = soup.find_all('span', class_='manchete1-titulo')
        for title_elem in titles:
            all_news.append(self.extract_articles(soup, title_elem, 'manchete-antetitulo', 'Destaque', Importance.FEATURE))

        titles = soup.find_all('span', class_='primeira-titulo')
        for title_elem in titles:
            all_news.append(self.extract_articles(soup, title_elem, 'primeira-antetitulo', 'Destaque', Importance.LARGE))

        titles = soup.find_all('span', class_='agenda-primeira-titulo')
        for title_elem in titles:
            all_news.append(self.extract_articles(soup, title_elem, 'agenda-primeira-antetitulo', 'Sociedade', Importance.LARGE))

        return all_news


class ScraperExpresso05(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20010628221949

    last_snippet_elem = None

    def extract_articles(self, title_elem, headline_class, category, importance):
        title = remove_clutter(title_elem.get_text())

        if title in ['Praia da Arrifana', 'Costa Vicentina']:
            snippet_elem = title_elem.find_next('span', class_='texto-caixa')
        else:
            snippet_elem = title_elem.find_next('td', class_='texto').find('p') or title_elem.find_next('span', class_='texto').find('p')

        snippet = snippet_elem.get_text()

        url_elem = title_elem.find_parent('a', class_='link-k')
        url = url_elem.get('href') if url_elem else generate_dummy_url('expresso.pt', 'scraper05', category, title)  # exceptionally a url was forgotten

        img_elem = [e for e in snippet_elem.find_all('img') if e.get('src').endswith('jpg')]
        img = img_elem[0].get('src') if img_elem else None

        headline_elems = title_elem.find_previous('span', class_=headline_class)
        headline = None
        if headline_elems:
            headlines = [e for e in headline_elems if is_between(self.last_snippet_elem, title_elem, e)]
            if headlines:
                headline = remove_clutter(headlines[0])

        if headline == 'Leia no Expresso':
            headline = None

        self.last_snippet_elem = snippet_elem  # to find next headline

        return {
            'article_url': url,
            'title': title,
            'snippet': prettify_text(snippet),
            'img_url': img,
            'headline': headline,
            'category': category,
            'importance': importance
        }

    def extract_box_article(self, title_elem):
        title = remove_clutter(title_elem.find('a').get_text())

        for ignore in ['últimas', '24 horas', 'para a semana', 'o cartoon', 'eles dizem', 'tempo']:
            if ignore in title.lower():
                return

        url = title_elem.find('a').get('href')

        snippet_elem = title_elem.find_next('span', class_='texto-caixa')
        snippet = snippet_elem.get_text()

        img_elem = [e for e in snippet_elem.find_parent('table').find_all('img') if e.get('src').endswith('jpg')]
        img = img_elem[0].get('src') if img_elem else None

        return {
            'article_url': url,
            'title': remove_clutter(title),
            'snippet': prettify_text(snippet),
            'img_url': img,
            'category': 'Destaque',
            'importance': Importance.LARGE
        }

    def scrape_page(self, soup):
        all_news = []

        self.last_snippet_elem = soup.contents[0]

        titles = soup.find_all('span', class_='titulo-ablack')
        for title_elem in titles:
            all_news.append(self.extract_articles(title_elem, 'antetitulo', 'Destaque', Importance.LARGE))

        titles = soup.find_all('span', class_='titulo-gr')
        for title_elem in titles:
            all_news.append(self.extract_articles(title_elem, 'antetitulo', 'Destaque', Importance.FEATURE))

        related_elems = soup.find_all('span', class_='art-rel-on')
        for elem in [e.find_parent('a') for e in related_elems]:
            all_news.append({
                'article_url': elem.get('href'),
                'title': remove_clutter(elem.get_text()),
                'category': 'Outras',
                'importance': Importance.RELATED
            })

        # boxes
        box_titles = soup.find_all('td', class_='tit-caixa')
        box_titles = [e for e in box_titles if e.find('a') ]
        for title_elem in box_titles:
            article = self.extract_box_article(title_elem)
            if article:
                all_news.append(article)

        # shorts
        short_articles = soup.find_all('span', class_='breves')
        for elem in [a.find('a') for a in short_articles]:
            all_news.append({
                'article_url': elem.get('href'),
                'title': remove_clutter(elem.get_text()),
                'category': 'Outras',
                'importance': Importance.LATEST
            })

        return all_news


# Two versions alternate at this point and for a while
def scrape_online_version(soup):
    all_news = []

    titles = soup.find_all('a', class_='titulo20')
    for article_elem in [a.find_parent('td') for a in titles]:
        title_elem = article_elem.find('a', class_='titulo20')
        snippet_elem = article_elem.find('span', class_='texto')

        img_elem = [img for img in article_elem.find_all('img') if img.get('src').endswith('.jpg')]
        img_url = img_elem[0].get('src') if len(img_elem) else None

        headline_elem = article_elem.find('span', class_='antetitulo')
        headline = remove_clutter(headline_elem.get_text()) if headline_elem else None

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': remove_clutter(title_elem.get_text()),
            'snippet': prettify_text(snippet_elem.get_text()),
            'img_url': img_url,
            'headline': headline,
            'category': 'Destaque',
            'importance': Importance.LARGE
        })

        # get related
        related_elem = article_elem.find('td', class_='relacionados')
        if related_elem:
            related_articles = related_elem.find_parent('table').find_all('a', class_='titulo11')
            for article in related_articles:
                all_news.append({
                    'article_url': article.get('href'),
                    'title': remove_clutter(article.get_text()),
                    'category': 'Outras',
                    'importance': Importance.RELATED
                })

    # get latest
    latest_sections = [e for e in soup.find_all('td', class_='tituloslotwhite') if remove_clutter(e.get_text()) in ['Os dez mais comentados', 'Últimas', '24 Horas']]

    for section in latest_sections:
        # the actual table is directly below the title one
        latest_articles = section.find_parent('table').find_next_sibling('table', attrs={'bgcolor': '#CCCCCC'}).find_all('a', class_='titulo11')

        for article in latest_articles:
            all_news.append({
                'article_url': article.get('href'),
                'title': remove_clutter(article.get_text()),
                'category': 'Outras',
                'importance': Importance.LATEST
            })

    # get short ones at bottom
    short_elems = soup.find_all('a', class_='titulo13')
    for title_elem in short_elems:
        headline = title_elem.find_previous('span', class_='antetituloazul')
        all_news.append({
            'article_url': title_elem.get('href'),
            'title': remove_clutter(title_elem.get_text()),
            'headline': remove_clutter(headline.get_text()),
            'category': 'Outras',
            'importance': Importance.LATEST
        })

    return all_news


def scrape_semanal_version(soup):
    all_news = []

    # track last snippet for when we need categories / headlines
    last_seen_elem = soup.contents[0]

    feature_titles = soup.find_all('a', class_='news_titulomanchete')
    for title_elem in feature_titles:
        title = title_elem.get_text()

        snippet_elem = title_elem.find_next('span', class_='news_txt')
        snippet = prettify_text(snippet_elem.get_text())
        if snippet.endswith('»'):
            snippet = prettify_text(snippet[:-1])

        headline_elem = [e for e in title_elem.find_next('span', class_='news_postitulo') if is_between(title_elem, snippet_elem, e) and isinstance(e, NavigableString)]
        headline = headline_elem[0] if len(headline_elem) else None

        img_elem = [e for e in snippet_elem.find_all('img') if e.get('src') and e.get('src').endswith('.jpg')]
        img_url = img_elem[0].get('src') if img_elem else None

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': remove_clutter(title),
            'snippet': snippet,
            'img_url': img_url,
            'headline': remove_clutter(headline),
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })

        last_seen_elem = snippet_elem

    article_titles = soup.find_all('a', class_='news_titulo')
    for title_elem in article_titles:
        title = title_elem.get_text()
        if ignore_title(title):
            continue

        snippet_elem = title_elem.find_next('span', class_='news_txt')
        snippet = prettify_text(snippet_elem.get_text())

        if snippet.endswith('»'):
            snippet = prettify_text(snippet[:-1])  # wrongly captured link symbol

        previous_header = title_elem.find_previous('span', class_='news_seccao')
        if previous_header and is_between(last_seen_elem, title_elem, previous_header):
            category = previous_header.get_text()
            last_seen_elem = previous_header  # don't catch headlines from previous news when there's a category
        else:
            category = 'Destaque'

        previous_headline = title_elem.find_previous('span', class_='news_antetitulo')
        if previous_headline and is_between(last_seen_elem, title_elem, previous_headline):
            headline = previous_headline.get_text()
            last_seen_elem = previous_headline
        else:
            headline = None

        img_elem = [e for e in snippet_elem.find_all('img') if e.get('src') and e.get('src').endswith('.jpg')]
        img_url = img_elem[0].get('src') if img_elem else None

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': remove_clutter(title),
            'snippet': snippet,
            'img_url': img_url,
            'headline': remove_clutter(headline),
            'category': category,
            'importance': Importance.FEATURE
        })

        last_seen_elem = snippet_elem

    return all_news


class ScraperExpresso06(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20030421210350

    def scrape_page(self, soup):
        return scrape_online_version(soup)


class ScraperExpresso07(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20030524114736

    def scrape_page(self, soup):
        return scrape_semanal_version(soup)


class ScraperExpresso08(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20030929125402

    def scrape_page(self, soup):
        return scrape_online_version(soup)


class ScraperExpresso09(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20031006043212

    def scrape_page(self, soup):
        return scrape_semanal_version(soup)


class ScraperExpresso10(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20031218003414

    def scrape_page(self, soup):
        return scrape_online_version(soup)


def scrape_modern_online_version(soup):
    all_news = []

    def extract_article(article_elem, title_class, importance):
        title_elem = article_elem.find('a', class_=title_class)
        title = remove_clutter(title_elem.get_text())

        headline_elem = article_elem.find('span', class_='news_antetituloorange')
        headline = remove_clutter(headline_elem.get_text()) if headline_elem else None

        snippet_elem = article_elem.find('span', class_='news_txt')
        snippet = prettify_text(snippet_elem.get_text())

        if snippet.endswith('»'):
            snippet = prettify_text(snippet[:-1])

        img_elem = [e for e in article_elem.find_all('img') if e.get('src').endswith('jpg')]
        img_url = img_elem[0].get('src') if img_elem else None

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title,
            'snippet': snippet,
            'img_url': img_url,
            'headline': headline,
            'category': 'Destaque',
            'importance': importance
        })

    feature_titles = soup.find_all('a', class_='news_tituloonline')
    for article_elem in [e.find_parent('td') for e in feature_titles]:
        extract_article(article_elem, 'news_tituloonline', Importance.FEATURE)

    large_titles = soup.find_all('a', class_='news_titulomanchetemini')
    for article_elem in [e.find_parent('td') for e in large_titles]:
        extract_article(article_elem, 'news_titulomanchetemini', Importance.LARGE)

    short_titles = [t for t in soup.find_all('a', class_='news_titulopeq') if t.find_parent('table', attrs={'bgcolor': '#FFFEF9'})]
    for article_elem in short_titles:
        all_news.append({
            'article_url': article_elem.get('href'),
            'title': remove_clutter(article_elem.get_text()),
            'category': 'Outras',
            'importance': Importance.SMALL
        })

    return all_news


class ScraperExpresso11(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20040519132236

    def scrape_page(self, soup):
        return scrape_modern_online_version(soup)


class ScraperExpresso12(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20040605190044

    def scrape_page(self, soup):
        return scrape_semanal_version(soup)


class ScraperExpresso13(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20040618224202

    def scrape_page(self, soup):
        return scrape_modern_online_version(soup)


class ScraperExpresso14(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20040619141206

    def scrape_page(self, soup):
        return scrape_semanal_version(soup)


class ScraperExpresso15(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20040705013715

    def scrape_page(self, soup):
        return scrape_modern_online_version(soup)


class ScraperExpresso16(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20040710044711

    def scrape_page(self, soup):
        return scrape_semanal_version(soup)


class ScraperExpresso17(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20040716051944

    def scrape_page(self, soup):
        return scrape_modern_online_version(soup)


class ScraperExpresso18(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20040717074159

    def scrape_page(self, soup):
        return scrape_semanal_version(soup)


class ScraperExpresso19(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20040722052704

    def scrape_page(self, soup):
        return scrape_modern_online_version(soup)


class ScraperExpresso20(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20040723072605

    def scrape_page(self, soup):
        return scrape_semanal_version(soup)


class ScraperExpresso21(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20050211122132

    def scrape_page(self, soup):
        return scrape_modern_online_version(soup)


class ScraperExpresso22(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20051107212943

    def scrape_page(self, soup):
        return scrape_semanal_version(soup)


class ScraperExpresso23(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20060222115122

    def scrape_page(self, soup):
        return scrape_modern_online_version(soup)


class ScraperExpresso24(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20070316010313

    def scrape_page(self, soup):
        all_news = []

        titles = soup.find_all('span', class_='news_tit')
        for title_elem in titles:
            title = title_elem.get_text()

            url_elem = title_elem.find_parent('a')

            snippet_elems = [e for e in url_elem.contents if isinstance(e, NavigableString)]
            snippet = prettify_text(' '.join(snippet_elems).replace('Exclusivo EXPRESSO', ''))

            category_elem = url_elem.find_parent('div').find_previous_sibling('div')
            category = category_elem.get_text()

            all_news.append({
                'article_url': url_elem.get('href'),
                'title': remove_clutter(title),
                'snippet': snippet,
                'category': category,
                'importance': Importance.LARGE
            })

        sic_titles = soup.find_all('span', class_='sictitulo')
        for title_elem in sic_titles:
            title = title_elem.get_text()

            snippet = title_elem.find_next('span', class_='siclead').get_text()
            category = clean_special_chars(title_elem.find_previous('span', class_='sicseccao').get_text().replace('|', '')) or 'Destaque'

            if title == 'Integração de imigrantes nas escolas':  # 20061107104938, lead and category swapped
                snippet = category
                category = 'Educação'

            all_news.append({
                'article_url': generate_dummy_url(self.source, 'scraper24', category, title),
                'title': remove_clutter(title),
                'snippet': prettify_text(snippet),
                'category': category,
                'importance': Importance.SMALL,
                'source': 'SIC'
            })

        return all_news


class ScraperExpresso25(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20070611144049

    def scrape_page(self, soup):
        all_news = []

        feature_elems = [e for e in soup.find_all('div', class_='HP07') if len(e.attrs.get('class')) == 1 and e.find(class_='Big Text') and e.find(class_='XBig Highlight')]

        for article_elem in [e.find('a') for e in feature_elems]:
            title = article_elem.find('span', class_='XBig Highlight').get_text()

            snippet_elems = [e for e in article_elem.find('span', class_='Big Text').contents if isinstance(e, NavigableString)]
            snippet = prettify_text(' '.join(snippet_elems))

            headline = article_elem.find('span', class_='Big Gray00').get_text()

            img_elem = [e for e in article_elem.find_all('img') if e.get('src').endswith('jpg')]
            img_url = img_elem[0].get('src') if img_elem else None

            all_news.append({
                'article_url': article_elem.get('href'),
                'title': remove_clutter(title),
                'snippet': snippet,
                'headline': remove_clutter(headline),
                'img_url': img_url,
                'category': 'Destaque',
                'importance': Importance.FEATURE
            })

        article_elems = soup.find_all('div', class_='HP07 NoticiarioContent', id=lambda x: not x)
        for article_elem in [e.find('a') for e in article_elems]:
            title = article_elem.find('span', class_='Big Highlight').get_text()
            headline = article_elem.find('b', class_='Red').get_text()
            category = article_elem.find('b', class_='Gray3').get_text()

            img_elem = [e for e in article_elem.find_all('img', id=re.compile(r'oPhotoNoticiario[0-9]*')) if e.get('src').endswith('jpg')]
            img_url = img_elem[0].get('src') if img_elem else None

            all_news.append({
                'article_url': article_elem.get('href'),
                'title': remove_clutter(title),
                'headline': remove_clutter(headline),
                'img_url': img_url,
                'category': category,
                'importance': Importance.SMALL
            })

        # latest news
        latest_elems = [e for e in soup.find_all('b', class_='Big Blue2 Text') if e.get_text() == 'Última Hora'][0]  # first we find the table's header
        latest_elems = [e.find_parent('a') for e in latest_elems.find_parent('div', class_='HP07').find_all(re.compile(r'(b|span)'), class_='Big Text')]  # then find all titles, and project they 'a' parent, which contains everything

        for article_elem in latest_elems:
            title = article_elem.find('span', class_='Gray1 Text Highlight').get_text()

            snippet_elem = [e for e in article_elem.find_all('span', class_='Text') if len(e.attrs.get('class')) == 1]
            snippet = prettify_text(snippet_elem[0].get_text(separator=' ')) if len(snippet_elem) > 0 else None

            all_news.append({
                'article_url': article_elem.get('href'),
                'title': remove_clutter(title),
                'snippet': snippet,
                'category': 'Outras',
                'importance': Importance.LATEST
            })

        return all_news


class ScraperExpresso26(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20081022051424

    def extract_main_feature(self, all_news, feature_main):
        feature_left = feature_main.find('td', class_='esq01')

        title_elem = feature_left.find('td', class_='esq01Titulo').find('a')
        title = remove_clutter(title_elem.get_text())

        category_elem = feature_left.find('span', class_='esq01SeccaoB')
        category = category_elem.get_text()

        if title == '"Senti alguma tristeza com acusações políticas"':
            category = 'Actualidade'

        snippet = (feature_left.find('a', class_='esq01txt') or feature_left.find('span', class_='esq01txt')).get_text()

        headline_elem = feature_left.find('td', class_='cent01Subtitulo')
        headline = remove_clutter(headline_elem.get_text())
        if not headline:
            headline_elem = feature_left.find('span', class_='esq01Seccao')
            headline = remove_clutter(headline_elem.get_text())

        img_elems = [e for e in feature_left.find_all('img') if is_between(category_elem, title_elem, e)]
        img_url = img_elems[0].get('src') if len(img_elems) > 0 else None

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title,
            'snippet': prettify_text(snippet),
            'headline': headline,
            'img_url': img_url,
            'category': category,
            'importance': Importance.FEATURE
        })

    def extract_feature_right(self, all_news, feature_right, start_elem, end_elem):
        category_elem = feature_right.find_all('span', class_='esq01SeccaoB')
        category_elem = [e for e in category_elem if is_between(start_elem, end_elem, e)][0].find('a')
        category = clean_special_chars(category_elem.get_text())

        title_elem = feature_right.find_all('div', class_='cent02Tit')
        title_elem = [e for e in title_elem if is_between(start_elem, end_elem, e)][0].find('a')

        headline_elem = feature_right.find_all('div', class_='cent01Subtitulo')
        headline_elem = [e for e in headline_elem if is_between(start_elem, end_elem, e)][0]

        snippet_elem = feature_right.find_all('div', class_='cent01TxtBody')

        if not snippet_elem:
            snippet_elem = feature_right.find_all('span', class_=r'esq01txt')

        snippet = None
        img_url = None
        if snippet_elem:
            snippet_elem = [e for e in snippet_elem if is_between(start_elem, end_elem, e)]

            if snippet_elem:
                snippet_elem = snippet_elem[0].find('a')

                snippet = ' '.join([e for e in snippet_elem.contents if isinstance(e, NavigableString) and not isinstance(e, Comment)])

                img_elem = snippet_elem.find('img')
                img_url = img_elem.get('src') if img_elem else None

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': remove_clutter(title_elem.get_text()),
            'snippet': prettify_text(snippet),
            'headline': remove_clutter(headline_elem.get_text()),
            'img_url': img_url,
            'category': category,
            'importance': Importance.FEATURE
        })

    def scrape_page(self, soup):
        all_news = []

        feature_main = soup.find('div', id='firstCellC1_line1')

        ## LEFT FEATURE
        self.extract_main_feature(all_news, feature_main)

        ## RIGHT FEATURES
        feature_right = feature_main.find('td', class_='cent01').find('table')

        start = find_comments(feature_right, ' begin bd_manchete_titulos_fechado ')
        end = find_comments(feature_right, ' end bd_manchete_titulos_fechado ')

        for i in range(len(start)):
            start_elem = start[i]
            end_elem = end[i]

            self.extract_feature_right(all_news, feature_right, start_elem, end_elem)

        start = find_comments(feature_right, ' begin bd_manchete_titulos_aberto ')
        end = find_comments(feature_right, ' end bd_manchete_titulos_aberto ')

        for i in range(len(start)):
            start_elem = start[i]
            end_elem = end[i]

            self.extract_feature_right(all_news, feature_right, start_elem, end_elem)

        ## SECOND LINE
        articles_elem = soup.find('div', id='firstCellC1_line2')

        all_articles = articles_elem.find_all('div', id=re.compile(r'noticiario_o_[0-9]*'))  # noticiario_c_* is a condensed version
        for article_elem in all_articles:
            title_elem = article_elem.find(re.compile(r'(span|div)'), class_='esq02Tit').find_all('a')
            title_elem = title_elem[0] if len(title_elem) == 1 else title_elem[1]
            headline = remove_clutter(article_elem.find('span', class_='esq02Subt').find('a').get_text())
            category = clean_special_chars(article_elem.find('span', class_='esq02Seccao').get_text())

            if category == 'Rede Expresso':
                category = 'Local'
            elif category != 'Actualidade':
                headline = '{}: {}'.format(category, headline)
                category = 'Destaque'

            img_elem = article_elem.find('img', class_='picNotL')
            img_url = None
            if img_elem:
                img_url = img_elem.get('src')

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': remove_clutter(title_elem.get_text()),
                'headline': headline,
                'img_url': img_url,
                'category': category,
                'importance': Importance.SMALL
            })

        # short news at bottom
        categories = soup.find_all('div', class_='lastNewsActualidade')
        for elem in categories:
            category = clean_special_chars(elem.find('td', class_='sepactualidade').find('a').get_text())

            if category in ['Dossiês', 'Postais', 'Iniciativas e Produtos', 'Blogues']:
                continue

            article_elems = elem.find_all('td', class_='lastNTit')
            for article_elem in article_elems:
                title_elem = article_elem.find_all('a')[-1]

                actual_cat = category
                if category == 'Última Hora Lusa':
                    new_cat = article_elem.find('span', class_='lastNSubTit')
                    actual_cat = clean_special_chars(new_cat.find('a').get_text())

                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': remove_clutter(title_elem.get_text()),
                    'category': actual_cat,
                    'importance': Importance.SMALL
                })

        return all_news


class ScraperExpresso27(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20110129160454

    def scrape_page(self, soup):
        all_news = []

        # SPECIAL BIG FEATURE
        big_features = soup.find_all('div', class_='mancheteTodaLargura')
        for article_elem in big_features:
            img_elem = article_elem.find('div', class_='imgTodaLargura').find('img')
            img_url = img_elem.get('src') if img_elem else None

            headline_elem = article_elem.find('div', class_='preTitle')
            title_elem = article_elem.find('h1', class_='bigTitle').find('a')
            snippet = article_elem.find('div', class_='mancheteBody').find('h3', class_='textoMancheteSmall').get_text()

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': remove_clutter(title_elem.get_text()),
                'snippet': prettify_text(snippet),
                'headline': remove_clutter(headline_elem.get_text()),
                'img_url': img_url,
                'category': 'Destaque',
                'importance': Importance.FEATURE
            })

            # RELATED ARTICLES
            related_articles = article_elem.find_all('td', class_='related')
            for title_elem in [e.find('a') for e in related_articles]:
                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': remove_clutter(title_elem.get_text()),
                    'category': 'Outras',
                    'importance': Importance.RELATED
                })

        # MAIN FEATURES
        features = soup.find_all('div', class_='mancheteImg')
        for article_elem in features:
            title_elem = article_elem.find(re.compile(r'div|h2'), class_='smallTitle')
            importance = Importance.LARGE
            if not title_elem:
                title_elem = article_elem.find(re.compile(r'div|h2'), class_='bigTitle')
                importance = Importance.FEATURE

            title_elem = title_elem.find('a')

            snippet_elem = article_elem.find('div', class_='mancheteBody').find('div', class_='texto')
            snippet = ' '.join([e for e in snippet_elem.contents if isinstance(e, NavigableString) and not isinstance(e, Comment)]) if snippet_elem else None

            headline_elem = article_elem.find('div', class_='preTitle')
            headline = remove_clutter(headline_elem.get_text()) if headline_elem else None

            img_elem = article_elem.find('div', class_='imgManchete')
            img_elem = img_elem.find('img') if img_elem else None
            img_url = img_elem.get('src') if img_elem else None

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': remove_clutter(title_elem.get_text()),
                'snippet': prettify_text(snippet),
                'headline': headline,
                'img_url': img_url,
                'category': 'Destaque',
                'importance': importance
            })

        # SMALL LATEST-LIKE ARTICLES
        small_features = soup.find('div', class_='destaquesHP')
        if small_features:
            for elem in small_features.find_all('div', class_='destaquesArtigo'):
                title_elem = elem.find(re.compile(r'div|h5'), class_='titles').find('a')
                headline_elem = elem.find_previous_sibling('div', class_='preTitle')

                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': remove_clutter(title_elem.get_text()),
                    'headline': remove_clutter(headline_elem.get_text()),
                    'category': 'Destaque',
                    'importance': Importance.LATEST
                })

        # LUSA AS A SOURCE
        lusa_features = soup.find('div', id='lusaHP').find_all(re.compile(r'div|h5'), class_='lusaArtigo')
        for title_elem in [e.find('span', class_='texto').find('a') for e in lusa_features]:
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': remove_clutter(title_elem.get_text()),
                'category': 'Destaque',
                'importance': Importance.LATEST,
                'source': 'Lusa'
            })

        # MISC SECTIONS
        section_elems = soup.find_all('div', class_='secDestaque')
        for section_elem in section_elems:
            category_elem = section_elem.find('span', class_='secDestaqueSection')
            category = clean_special_chars(category_elem.get_text())

            if category not in ['Dossies Actualidade', 'Desporto', 'Actualidade']:
                continue

            # each article in is a div
            articles = category_elem.find_parent('div').find_next_siblings('div')
            for article_elem in [e for e in articles if not re.match(r'destaqueMenu[A-Za-z]*', e.get('id') or '')]:
                title_elem = article_elem.find(re.compile(r'div|h6'), class_='secDestaqueTitle') or article_elem.find(re.compile(r'div|h6'), class_='secDestaqueTitleSmall')
                title_elem = title_elem.find('a')

                snippet_elem = article_elem.find('div', class_='texto')
                snippet = snippet_elem.get_text() if snippet_elem else None

                img_elem = article_elem.find('img', class_='picNotLM')
                img_url = img_elem.get('src') if img_elem else None

                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': remove_clutter(title_elem.get_text()),
                    'snippet': prettify_text(snippet),
                    'img_url': img_url,
                    'category': category,
                    'importance': Importance.SMALL
                })

        # ARTICLES FROM OTHER SOURCES
        other_sources_section = soup.find('div', id='feedJornaisHP').find_all('div', class_='mainTitle')
        for title_elem in [e.find('a') for e in other_sources_section]:
            source_elem = title_elem.find_next('div', class_='comentario').find('a')
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': remove_clutter(title_elem.get_text()),
                'category': 'Outras',
                'importance': Importance.SMALL,
                'source': clean_special_chars(source_elem.get_text())
            })

        return all_news


class ScraperExpresso28(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20131108023914

    def scrape_page(self, soup):
        all_news = []

        # BIG FEATURES
        features = soup.find_all('div', class_='mancheteBox')
        for article_elem in [e for e in features if 'boxTops' not in e.get('class') and 'scrollBox' not in e.get('class')]:
            img_elem = article_elem.find('div', class_='imgMancheteWrapper')
            img_url = img_elem.find('img').get('src') if img_elem else None

            title_elem = article_elem.find('h2', class_='smallTitle')
            importance = Importance.LARGE
            if not title_elem:
                title_elem = article_elem.find('h2', class_='bigTitle')
                importance = Importance.FEATURE

            title_elem = title_elem.find('a')

            snippet_elem = article_elem.find('div', class_='mancheteBody')
            snippet_elem = snippet_elem.find('h3', class_='texto') if snippet_elem else None  # 20120701150239 mancheteBody does not exist
            snippet = snippet_elem.get_text() if snippet_elem else None

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': remove_clutter(title_elem.get_text()),
                'snippet': prettify_text(snippet),
                'img_url': img_url,
                'category': 'Destaque',
                'importance': importance
            })

            # RELATED ARTICLES
            related_articles = article_elem.find_all(re.compile(r'td|span'), class_='related')
            for title_elem in [e.find('a') for e in related_articles]:
                match = re.match(r'(.*) (\.\.\.) \[[0-9]*]', title_elem.get_text())
                title = match.group(1) + match.group(2) if match else title_elem.get_text()
                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': remove_clutter(title),
                    'category': 'Outras',
                    'importance': Importance.RELATED
                })

        # LATEST NEWS
        latest_elems = soup.find('div', id='lusaHP').find_all('div', class_='item')
        for title_elem in [e.find('a') for e in latest_elems]:
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': remove_clutter(title_elem.get_text()),
                'category': 'Outras',
                'importance': Importance.LATEST
            })

        # SECTIONS
        # sections = soup.find_all('div', class_='auto-block-middle')
        # can't get these yellow boxes at the end, seems like they're loaded asynchronously

        return all_news


class ScraperExpresso29(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20150424124458

    def scrape_page(self, soup):
        all_news = []

        articles = soup.find_all('article', class_=re.compile(r'^manchete(SmallBox|Box|Top)$'))
        for article_elem in articles:
            # ignore opinion pieces
            if article_elem.find('div', class_='opiniaoItem'):
                continue

            title_elem = article_elem.find('h2', class_=re.compile(r'bigTitle|smallTitle')).find('a')
            title = remove_clutter(title_elem.get_text())
            if ignore_title(title):
                continue

            headline_elem = article_elem.find('div', class_='preTitle')
            headline = remove_clutter(headline_elem.get_text()) if headline_elem else None

            snippet_elem = article_elem.find('h3', class_=re.compile(r'smallText|textoMancheteSmall'))
            snippet = prettify_text(snippet_elem.get_text()) if snippet_elem else None

            img_elem = article_elem.find('figure')
            img_url = img_elem.find('img').get('src') if img_elem else None

            importance = Importance.FEATURE if 'mancheteSmallBox' in article_elem.get('class') else (Importance.LARGE if 'mancheteBox' in article_elem.get('class') else Importance.SMALL)

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title,
                'snippet': snippet,
                'headline': headline,
                'img_url': img_url,
                'category': 'Destaque',
                'importance': importance
            })

            # find related
            for title_elem in [e.find('a') for e in article_elem.find_all('span', class_='related')]:
                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title,
                    'category': 'Destaque',
                    'importance': Importance.RELATED
                })

        return all_news


class ScraperExpresso30(NewsScraper):
    source = 'expresso.pt'
    cutoff = 20151201102835  # could work after this, haven't tested

    def scrape_page(self, soup):
        all_news = []

        articles = soup.find_all('article', class_='AT-noticia')
        articles = [a for a in articles if
                    'MC-iniciativaseprodutos.marketing' not in a.get('class')  # ignore marketing
                    and a.find_parent('div').get('data-type') == 'default'  # ignore quotes, etc.
                    ]

        for article_elem in articles:
            title_elem = article_elem.find('h1', class_='title').find('a')
            title = remove_clutter(title_elem.get_text())
            if ignore_title(title):
                continue

            #headline_elem = article_elem.find('div', class_='preTitle')
            #headline = remove_clutter(headline_elem.get_text()) if headline_elem else None

            snippet_elem = article_elem.find('h2', class_='lead')
            snippet = prettify_text(snippet_elem.get_text()) if snippet_elem else None

            img_elem = article_elem.find('figure')
            img_url = img_elem.find('img').get('src') if img_elem else None

            # find article relevance, start by seeing if we're related
            if article_elem.find_parent('ul', class_='relatedInList'):
                importance = Importance.RELATED
            else:
                importance = Importance.FEATURE if 'headline' in article_elem.get('class') else Importance.LARGE

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title,
                'snippet': snippet,
                'img_url': img_url,
                'category': 'Destaque',
                'importance': importance
            })

        return all_news
