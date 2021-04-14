import re

from src.text_util import remove_clutter, ignore_title

from src.scrapers.news_scraper import NewsScraper, Importance


class ScraperPortugalDiario01(NewsScraper):
    source = 'portugaldiario.iol.pt'
    cutoff = 20000917093828

    def scrape_page(self, soup):
        all_news = []

        news = soup.find('td', attrs={'width': 480}).find_all('table', recursive=False)
        feature = news[0].find_all('table')[-1].find('td')
        news = news[1].find_all('p')

        # get feature
        url = feature.find('a').get('href')
        title = feature.find('a').get_text()
        snippet = feature.find_all('a')[-1].get_text()

        all_news.append({
            'article_url': url,
            'title': title,
            'snippet': snippet,
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })

        # get other news
        for article in [article.find('td') for article in news]:
            url = article.find('a', class_='titulo')
            headline = article.find('span', class_='antetitulo').get_text()
            snippet = article.find('span', class_='lead').get_text()

            all_news.append({
                'article_url': url.get('href'),
                'headline': headline,
                'title': url.get_text(),
                'snippet': snippet,
                'category': 'Destaque',
                'importance': Importance.LARGE
            })
        return all_news


class ScraperPortugalDiario02(NewsScraper):
    source = 'portugaldiario.iol.pt'
    cutoff = 20010516032701

    def prettify_source(self, source):
        if not source:
            return source, 'Destaque'

        if source == 'DIARIO ECONOMICO':
            return 'Diário Económico', 'Economia'

        if source == 'MAISFUTEBOL':
            return 'Mais Futebol', 'Desporto'

        if source == 'TVI':
            return 'TVI', 'Destaque'

        if source == 'SEMANARIO ECONOMICO':
            return 'Semanário Económico', 'Economia'

        raise Exception('Unparsed source!')

    def scrape_page(self, soup):
        all_news = []

        sections = soup.find_all('table', attrs={'width': '100%', 'cellspacing': 15})[0].find('tr').find('td').find('center').find_all('table', attrs={'width': '100%'}, recursive=False)
        for section in sections:
            articles = section.find_all('td', attrs={'bgcolor': '#FFFFFF'})
            if len(articles) == 0:  # changed at 20010510205836
                articles = section.find_all('table', attrs={'bgcolor': '#FFFFFF'})
            else:
                articles = [article.find('table') for article in articles]

            for article in articles:
                rows = article.find_all('tr')

                # top row has url, headline (sometimes), and title
                top = rows[0].find('a')
                url = top.get('href')

                top = top.find('b')
                break_elem = top.find('br')
                if break_elem:
                    headline = break_elem.previous_sibling
                    title = top.find('div').get_text()
                else:
                    headline = None
                    title = top.get_text()

                # bottom has snippet and img (sometimes)
                bottom = rows[1].find('td').find('span')
                source = None
                if not bottom:
                    elems = rows[1].find('td').find_all('font')
                    bottom = elems[0]
                    if len(elems) > 2:  # in case there's no snippet don't count '|--Texto--|' as the last one
                        source = elems[1].get_text()

                img_elem = bottom.find('img')
                img_url = None
                if img_elem:
                    img_url = img_elem.get('src')
                snippet = bottom.get_text()

                # get category based on source, if no source then generic category
                source, category = self.prettify_source(source)

                all_news.append({
                    'article_url': url,
                    'headline': headline,
                    'title': title,
                    'snippet': snippet,
                    'img_url': img_url,
                    'source': source,  # in some cases the site also aggregates others' news
                    'category': category,
                    'importance': Importance.LARGE
                })
        return all_news


def check_url(url):
    if url.startswith('/'):
        return url[1:]
    return url


def process_categories(all_news, all_lines):
    category = None
    for line in all_lines:
        category_header = line.find(class_='bb')
        if category_header:
            category = category_header.find('a', class_='onzevb').get_text()
            continue

        elem = line.find('a', class_='dozeab') or line.find('a', class_='onzeab')
        title = remove_clutter(elem.get_text())
        if not title:
            continue  # 20050206061731 has an empty title

        if ignore_title(title):
            continue

        all_news.append({
            'article_url': check_url(elem.get('href')),
            'title': title,
            'category': category,
            'importance': Importance.SMALL
        })


def process_small_features(all_news, small_features):
    for article in small_features:
        title_elem = article.find(class_='dezc')
        title_elem = title_elem.find('a', class_='trezevb') or title_elem.find('a', class_='quinzevb') or title_elem.find('a', class_='dozevb')
        snippet = article.find(class_='pquinzee').find(class_='dozep').get_text()

        all_news.append({
            'article_url': check_url(title_elem.get('href')),
            'title': title_elem.get_text(),
            'snippet': snippet,
            'category': 'Destaque',
            'importance': Importance.LARGE
        })


class ScraperPortugalDiario03(NewsScraper):
    source = 'portugaldiario.iol.pt'
    cutoff = 20031120184016

    def scrape_page(self, soup):
        all_news = []

        # first section
        first_section = soup.find('div', id='navega').next_sibling.next_sibling

        # get features elements
        # get all relevant elements first, the layout is very weird
        large_feature_img_elem = first_section.find('img', class_='bum')
        large_feature_headline_elem = large_feature_img_elem.find_next('span', class_='dezp')
        small_features_elem = large_feature_headline_elem.find_next('td', class_='riscos')
        large_feature_elem = small_features_elem.find_parent('tr').find_next_sibling('tr')

        # get large feature
        large_feature_elem = large_feature_elem.find_all('td')[1]
        large_feature_url_elem = large_feature_elem.find('a')
        large_feature_snippet = large_feature_elem.find(class_='dozep').get_text()

        all_news.append({
            'article_url': large_feature_url_elem.get('href'),
            'headline': large_feature_headline_elem.get_text(),
            'title': large_feature_url_elem.get_text(),
            'snippet': large_feature_snippet,
            'img_url': large_feature_img_elem.get('src'),
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })

        # get small features
        small_features = small_features_elem.find_all(class_='pum')
        process_small_features(all_news, small_features)

        # get categories
        category_section = large_feature_elem.find_next('tr', class_='riscos').find_all('tr')
        process_categories(all_news, category_section)

        return all_news


class ScraperPortugalDiario04(NewsScraper):
    source = 'portugaldiario.iol.pt'
    cutoff = 20050509013322

    def scrape_page(self, soup):
        all_news = []

        # featured
        featured_elem = soup.find('table', id='manchete')
        featured_img_elem = featured_elem.find('img', class_='bum') or featured_elem.find('img', class_='bum1')
        featured_url_elem = featured_elem.find('a', class_='vintevb')
        featured_snippet = featured_elem.find('span', class_='dozep').get_text()

        all_news.append({
            'article_url': check_url(featured_url_elem.get('href')),
            'title': featured_url_elem.get_text(),
            'snippet': featured_snippet,
            'img_url': check_url(featured_img_elem.get('src')),
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })

        # get feature's related
        related = featured_elem.find_all('a', class_='onzeab')
        for article in related:
            all_news.append({
                'article_url': check_url(article.get('href')),
                'title': article.get_text(),
                'category': 'Outras',
                'importance': Importance.RELATED
            })

        # get small features
        small_features = featured_elem.find_next_sibling('table', class_='bc').find_all('div', class_="pum")
        process_small_features(all_news, small_features)

        # get categories
        category_section = featured_elem.find_next_sibling('table', class_='bc').find_next_sibling('table').find_next_sibling('table').find('table', attrs={'cellpadding': 8}).find('tr').find_all('tr')
        process_categories(all_news, category_section)

        return all_news


class ScraperPortugalDiario05(NewsScraper):
    source = 'portugaldiario.iol.pt'
    cutoff = 20080314152017

    def scrape_page(self, soup):
        all_news = []

        # featured
        featured_elem = soup.find('div', id='manchete')
        featured_url_elem = featured_elem.find('h1').find('a')
        featured_img_elem = featured_elem.find('div', id='img').find('a', class_='lrec').find('img')

        featured_snippet = featured_elem.find('span', class_='res').get_text()

        all_news.append({
            'article_url': featured_url_elem.get('href'),
            'title': featured_url_elem.get_text(),
            'snippet': featured_snippet,
            'img_url': featured_img_elem.get('src'),
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })

        # get feature's related
        related = featured_elem.find('div', id='rel').find_all('a', class_='lrec')
        for article in related:
            title = remove_clutter(article.get_text())
            if not title:
                continue  # 20050607002151 has an empty title

            all_news.append({
                'article_url': article.get('href'),
                'title': title,
                'category': 'Outras',
                'importance': Importance.RELATED
            })

        # get latest news
        latest_elem = soup.find('div', id='ultimas')
        if latest_elem:  # available before 20060203043703
            for article in [article.find('a') for article in latest_elem.find_all('li')]:
                all_news.append({
                    'article_url': article.get('href'),
                    'title': article.get_text(),
                    'category': 'Última hora',
                    'importance': Importance.LATEST
                })

        # get small features
        small_features = soup.find_all('div', attrs={'id': re.compile('submanchete[0-9]')})
        for article in small_features:
            url_elem = article.find('a', class_='lrec')
            snippet_elem = article.find('span', class_='res')
            snippet = None
            if snippet_elem:
                snippet = snippet_elem.get_text()

            all_news.append({
                'article_url': url_elem.get('href'),
                'title': url_elem.get_text(),
                'snippet': snippet,
                'category': 'Destaque',
                'importance': Importance.LARGE
            })

        # get categories
        category_elems = soup.find('div', id='xultimas')
        if category_elems:  # no categories on 20051222163024
            category_elems = category_elems.find_all('div', recursive=False)
            for category_elem in category_elems:
                category = category_elem.find('a').find('img').get('alt')

                for article in [article.find('a', class_='lrec') for article in category_elem.find_all('li')]:
                    # some cases did not capture the full page (eg 20050714023231)
                    if not article:
                        continue

                    all_news.append({
                        'article_url': article.get('href'),
                        'title': article.get_text(),
                        'category': category,
                        'importance': Importance.SMALL
                    })

        return all_news


class ScraperPortugalDiario06(NewsScraper):
    source = 'portugaldiario.iol.pt'
    cutoff = 20100626141610  # source not used after this date (becomes redirect to tvi24)

    def scrape_page(self, soup):
        all_news = []

        # featured
        featured_elems = soup.find('div', id='submanchetes').find_all('li')
        for article in featured_elems:
            headline = article.find('em').get_text()
            url_elem = article.find('h2').find('a')
            snippet = article.find('div', class_='txt').get_text()

            all_news.append({
                'article_url': url_elem.get('href'),
                'headline': headline,
                'title': url_elem.get_text(),
                'snippet': snippet,
                'category': 'Destaque',
                'importance': Importance.FEATURE
            })

        # get large news
        news = soup.find('div', id='bloco2').find_all('div', id=re.compile('destaque[0-9]'))
        for article in news:
            url_elem = article.find('h3') or article.find('h4')
            url_elem = url_elem.find('a')

            # headline optional
            headline_elem = article.find('em')
            headline = headline_elem.get_text() if headline_elem else None

            # img optional
            img_elem = article.find('img')
            img_url = article.find('img').get('src') if img_elem else None

            snippet = article.find('div', class_='txt').get_text()

            all_news.append({
                'article_url': url_elem.get('href'),
                'headline': headline,
                'title': url_elem.get_text(),
                'snippet': snippet,
                'img_url': img_url,
                'category': 'Destaque',
                'importance': Importance.LARGE
            })

            # get related (also optional)
            related = article.find_all('h5')
            for related_article in [related_article.find('a') for related_article in related]:
                all_news.append({
                    'article_url': related_article.get('href'),
                    'title': related_article.get_text(),
                    'category': 'Outras',
                    'importance': Importance.RELATED
                })

        # get latest news
        latest_elem = soup.find('div', id='listanoticiasX').find('div', class_='body').find_all('li')
        for article in latest_elem:
            category_elem = article.find('em').find('a')
            category = category_elem.get_text()

            if category in ['Celebridades']:
                continue

            url_elem = category_elem.find_next('a')
            all_news.append({
                'article_url': url_elem.get('href'),
                'title': url_elem.get_text(),
                'category': category,
                'importance': Importance.LATEST
            })

        # get categories
        sport_articles = soup.find('div', id='destDesporto').find_all('li')
        for article in sport_articles:
            url_elem = article.find('a')

            title_elem = url_elem.find('strong') or url_elem.find('span', class_='overlay')

            snippet_elem = url_elem.find('span', class_='txt')
            snippet = snippet_elem.get_text() if snippet_elem else None

            img_elem = url_elem.find('img')
            img_url = img_elem.get('src') if img_elem else None

            importance = Importance.LARGE if 'first' in (article.get('class') or []) else Importance.SMALL
            all_news.append({
                'article_url': url_elem.get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet,
                'img_url': img_url,
                'category': 'Desporto',
                'importance': importance
            })

        return all_news