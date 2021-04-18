import re

from bs4 import NavigableString, Comment

from src.categories import bind_category
from src.util import generate_dummy_url, get_direct_strings, find_comments, find_comments_regex, is_between, \
    is_between_nonrecursive, is_after, generate_destaques_uniqueness
from src.text_util import remove_clutter, clean_special_chars, prettify_text, ignore_title, clean_spacing

from src.scrapers.news_scraper import NewsScraper, Importance


def time_cleaner(text):
    return re.match(r'^(.*)\s*\(\s*[0-9]+:[0-9]+\s*/\s*[0-9]+\s*[A-Za-z]{3}\s*\)$', text.strip()).group(1)


class ScraperTSF02(NewsScraper):
    source = 'tsf.pt'
    cutoff = 20010702162106

    def scrape_page(self, soup):
        all_news = []

        news_boxes = soup.find('td', attrs={'width': 465}).find_all('table', attrs={'width': 465})

        last_marker = soup
        for article_elem in [e.find_parent('tr') for e in news_boxes[1].find_all('span', class_='resume')]:
            cells = article_elem.find_all('td')
            img_elem = cells[0].find('img')

            inner_elem = cells[2]

            pretitle_elem = inner_elem.find('span', class_='container')
            title_elem = inner_elem.find('span', class_='hl1').find_parent('a')

            snippet_elem = inner_elem.find('span', class_='resume')

            # will be used later
            last_marker = snippet_elem

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'headline': pretitle_elem.get_text(),
                'snippet': time_cleaner(snippet_elem.get_text()),
                'img_url': img_elem.get('src'),
                'category': 'Destaques',
                'importance': Importance.FEATURE
            })

        # latest articles
        end_marker = find_comments(soup, 'Agora no mundo')[0]
        latest_articles = [e for e in soup.find_all('span', class_='resume') if is_between(last_marker.next, end_marker, e)]
        for article_elem in [e.find_parent('td') for e in latest_articles]:
            pretitle_elem = article_elem.find('span', class_='container')
            title_elem = article_elem.find('span', class_='resume')

            url = title_elem.find_parent('a').get('href')
            category = url.split('=')[-1]

            all_news.append({
                'article_url': url,
                'title': time_cleaner(title_elem.get_text()),
                'headline': pretitle_elem.get_text(),
                'category': category,
                'importance': Importance.LATEST
            })

        return all_news


class ScraperTSF03(NewsScraper):
    source = 'tsf.pt'
    cutoff = 20011228150549
    # ATTENTION: arquivo_source_url makes it so that it only works with a single snapshot

    def ts_from_elems(self, date_elem, time_elem):
        date_match = re.match(r'([0-9]+)/([0-9]+)/([1-2]0[0-9][0-9])', date_elem)
        time_match = re.match(r'([0-9]+):([0-9]+)', time_elem)

        return date_match.group(3) + date_match.group(2) + date_match.group(1) + time_match.group(1) +time_match.group(2) + '00'

    def scrape_page(self, soup):
        all_news = []

        larger_titles = soup.find_all('a', class_='titulos')
        for title_elem in larger_titles:
            category = title_elem.get('href').split('=')[-1]
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'category': category,
                'importance': Importance.SMALL
            })

        # get all latest news by identifying 'resume' spans, then getting the tr parents
        # get every other one since there are two resume spans per title
        latest_table = soup.find_all('table', attrs={'width': 458})[0].find('table').find_all('span', class_='resume')
        latest_rows = []
        for i in range(0, len(latest_table), 2):
            latest_rows.append(latest_table[i].find_parent('tr'))

        for article_elem in latest_rows:
            time_elem = article_elem.find('span', class_='resume')
            date_elem = article_elem.find_next_sibling('tr').find('span', class_='resume')
            timestamp = self.ts_from_elems(date_elem.get_text(), time_elem.get_text())

            title_elem = article_elem.find('a')
            all_news.append({
                'arquivo_source_url': 'https://arquivo.pt/wayback/20011228150549/http://www.tsf.pt:80/especial_portugal_aut.asp',
                'timestamp': timestamp,
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'category': 'Destaques',
                'importance': Importance.LATEST
            })

        return all_news


def orange_2003_scraper(soup):
    all_news = []

    news_boxes = soup.find('td', attrs={'width': 477}).find_all('table', attrs={'width': 465, 'xmlns:msxsl': lambda a: a is not None})

    latest_marker = [e for e in soup.find_all('span', class_='titlegrupo') if e.get_text() == 'ÚLTIMAS'][0]

    main_features = [e for e in news_boxes if not is_after(latest_marker, e)]
    for article_elem in [e.find_all('tr', recursive=False)[1] for e in main_features]:
        cells = article_elem.find_all('td')
        img_elem = cells[0].find('img')

        inner_elem = cells[2]

        pretitle_elem = inner_elem.find('a', class_='container')
        title_elem = inner_elem.find('a', class_='hl1')
        snippet_elem = inner_elem.find('span', class_='resume')

        if not title_elem:
            continue  # 20040212113622

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title_elem.get_text(),
            'headline': pretitle_elem.get_text(),
            'snippet': time_cleaner(snippet_elem.get_text()),
            'img_url': img_elem.get('src'),
            'category': 'Destaques',
            'importance': Importance.FEATURE
        })

    latest_box = [e for e in news_boxes if is_after(latest_marker, e)][0]
    latest_articles = latest_box.find_all('a', class_='container')
    for article_elem in [e.find_parent('td') for e in latest_articles]:
        pretitle_elem = article_elem.find('a', class_='container')
        title_elem = article_elem.find('a', class_='resume')

        url = title_elem.get('href')
        category = category_from_url(url)

        all_news.append({
            'article_url': url,
            'title': time_cleaner(title_elem.get_text()),
            'headline': pretitle_elem.get_text(),
            'category': category,
            'importance': Importance.LATEST
        })

    return all_news

class ScraperTSF04(NewsScraper):
    source = 'tsf.pt'
    cutoff = 20021201090724

    # slight changes from scraper 02, still warrants new scraper for clarity

    def scrape_page(self, soup):
        return orange_2003_scraper(soup)


def category_from_url(url):
    category = re.match(r'.*http://(?:www\.)?tsf\.(?:sapo\.)?pt(?::80)?/online/([a-zA-Z0-9]*)/interior\.asp\?id_artigo=[A-Za-z0-9]*$', url).group(1)

    if category == 'ocios':
        return 'Lazer'

    return category


def category_from_url_new(url):
    # newer version 20081021143609
    match = re.match(r'.*http://tsf\.sapo\.pt/PaginaInicial/([A-Za-z0-9]*)/Interior\.aspx\?content_id=[A-Za-z0-9]*$', url)
    return match.group(1) if match else None


class ScraperTSF05(NewsScraper):
    source = 'tsf.pt'
    cutoff = 20030405000422

    def extract_small_article(self, all_news, article_elem, importance):
        pretitle = get_direct_strings(article_elem)
        title_elem = article_elem.find('a', class_='hl1')

        category = category_from_url(title_elem.get('href'))

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title_elem.get_text(),
            'headline': pretitle,
            'category': category,
            'importance': importance
        })

    def scrape_page(self, soup):
        all_news = []

        news_boxes = soup.find('td', attrs={'valign': 'TOP'}).find('table', attrs={'width': 756}).find('table', attrs={'width': 756}).find_all('tr', recursive=False)

        main_features = news_boxes[0].find('td').find_all('table', recursive=False)
        for article_elem in main_features:
            img_elem = article_elem.find_all('td')[0].find('img')

            inner_elem = article_elem.find_all('td')[1]
            pretitle_elem = inner_elem.find('a', class_='container')
            title_elem = inner_elem.find('a', class_='hl1')

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'headline': pretitle_elem.get_text(),
                'img_url': img_elem.get('src'),
                'category': 'Destaques',
                'importance': Importance.FEATURE
            })

        latest_articles = news_boxes[0].find('td', attrs={'align': 'right'}).find('table', attrs={'width': 446}).find('table', attrs={'xmlns:msxsl': lambda a: a is not None}).find_all('td', class_='container')
        for article_elem in latest_articles:
            self.extract_small_article(all_news, article_elem, Importance.LATEST)

        other_articles = news_boxes[2].find_all('td', class_='container')
        for article_elem in other_articles:
            self.extract_small_article(all_news, article_elem, Importance.SMALL)

        return all_news


class ScraperTSF06(NewsScraper):
    source = 'tsf.pt'
    cutoff = 20040402142348

    def scrape_page(self, soup):
        return orange_2003_scraper(soup)


class ScraperTSF07(NewsScraper):
    source = 'tsf.pt'
    cutoff = 20080314173841

    def scrape_page(self, soup):
        all_news = []

        feature_box = soup.find('table', attrs={'width': 466})
        feature_elems = feature_box.find_all(re.compile(r'(span|div)'), class_='resume')
        feature_elems = [e.find_parent('tr') for e in feature_elems if not e.find(class_='resume')]  # remove a bug with duplicate elems, also get parent elem

        for article_elem in feature_elems:
            img_elem = [e for e in article_elem.find_all('img') if e.find_parent('a') and not e.get('src').endswith('gif')]
            img_url = img_elem[0].get('src') if len(img_elem) > 0 else None

            title_elem = article_elem.find('a', class_='hl1')
            pretitle_elem = title_elem.find_all('span', class_='container')[1]

            snippet_elem = article_elem.find(re.compile(r'(span|div)'), class_='resume')

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': get_direct_strings(title_elem),
                'headline': pretitle_elem.get_text(),
                'snippet': snippet_elem.get_text(),
                'img_url': img_url,
                'category': 'Destaques',
                'importance': Importance.FEATURE
            })

            # related
            related_articles = article_elem.find_all('td', attrs={'height': 15})
            for title_elem in [e.find('a', class_='hl1') for e in related_articles]:
                if not title_elem:
                    continue  # 20041014021132

                # separate pretitle from title by uppercase
                parts = [e for e in title_elem.get_text().strip().split('  ') if len(e) > 0]
                pretitle = parts[0]
                title = parts[-1]

                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title,
                    'pretitle': pretitle,
                    'category': 'Destaques',
                    'importance': Importance.RELATED
                })

        # LATEST
        latest_marker = [e for e in soup.find_all('td', class_='titlegrupo') if e.get_text() == 'ÚLTIMAS NOTÍCIAS'][0]
        latest_articles = latest_marker.find_next('table', attrs={'width': re.compile(r'^(182|128)$')}).find_all('a', class_='hl1')
        for article_elem in latest_articles:
            pretitle_elem = article_elem.find_all('span', class_='container')[1]

            title = get_direct_strings(article_elem)
            if not title:
                continue  # 20070306020736

            category = category_from_url(article_elem.get('href'))

            all_news.append({
                'article_url': article_elem.get('href'),
                'title': title,
                'headline': pretitle_elem.get_text(),
                'category': category,
                'importance': Importance.LATEST
            })

        # SECTIONS
        groups_marker = [e for e in soup.find_all('a', class_='titlegrupo') if e.get_text().strip() == 'PORTUGAL'][0]
        category_box = groups_marker.find_parent('table').find_parent('table')

        category_articles = category_box.find_all('a', class_='hl1')
        for article_elem in category_articles:
            pretitle_elem = article_elem.find_all('span', class_='container')[1]

            category = article_elem.find_previous('a', class_='titlegrupo').get_text()

            all_news.append({
                'article_url': article_elem.get('href'),
                'title': get_direct_strings(article_elem) or article_elem.find('br').get_text(),  # 20080219110900, enclosed in br
                'headline': pretitle_elem.get_text(),
                'category': clean_special_chars(category),
                'importance': Importance.SMALL
            })

        return all_news


class ScraperTSF08(NewsScraper):
    source = 'tsf.pt'
    cutoff = 20090926171532

    def extract_feature(self, all_news, article_elem, importance):
        img_elem = article_elem.find('img', class_='Photo')

        pretitle_elem = article_elem.find('table', class_='TagArea')
        pretitle = pretitle_elem.find('h2', class_=re.compile(r'^Tag1|0$')).get_text() if pretitle_elem else None

        title_elem = article_elem.find('h1', recursive=False)
        title = title_elem.get_text()

        if not title:
            return  # 20090929032613 autarquicas header

        url_elem = title_elem.find('a')

        related_elem = article_elem.find('div', class_='Related')

        # get snippet, not only direct strings, but accounting for italics or bolds, for example
        snippet = ''
        elligible_elems = [e for e in article_elem.contents if is_between(title_elem.next, related_elem, e)] if related_elem else [e for e in article_elem.contents if is_after(title_elem.next, e)]
        for elem in elligible_elems:
            snippet += elem if isinstance(elem, NavigableString) else elem.get_text()

        all_news.append({
            'article_url': url_elem.get('href'),
            'title': title,
            'headline': pretitle,
            'snippet': snippet,
            'img_url': img_elem.get('src'),
            'category': 'Destaques',
            'importance': importance
        })

        if related_elem:
            for title_elem in [e.find('a') for e in related_elem.find('ul').find_all('li')]:
                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title_elem.get_text(),
                    'category': 'Outras',
                    'importance': Importance.RELATED
                })

    def scrape_page(self, soup):
        all_news = []

        feature_articles = soup.find_all('div', class_='Manchete')
        for article_elem in [e.find('div', class_='Content') for e in feature_articles]:
            self.extract_feature(all_news, article_elem, Importance.FEATURE)

        large_articles = soup.find_all('div', class_='Destaque')
        for article_elem in [e.find('div', class_='Content') for e in large_articles]:
            self.extract_feature(all_news, article_elem, Importance.LARGE)

        latest_articles_elem = soup.find('div', class_='Ultimas')
        extract_latest_modern(all_news, latest_articles_elem)

        short_articles = soup.find('div', class_='UltimasEmDestaque').find('div', class_='content').find_all('h1')
        for title_elem in [e.find('a') for e in short_articles]:
            category_elem = title_elem.find_previous('table', class_='TagArea').find('h2', class_=re.compile(r'^Tag1|0$'))
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'category': category_elem.get_text(),
                'importance': Importance.SMALL
            })

        desporto_articles = soup.find('div', class_='DesportoBoxContent').find('table', class_='Content').find_all('h1')
        extract_desporto_modern(all_news, desporto_articles)

        return all_news


def extract_latest_modern(all_news, latest_articles):
    for title_elem in [e.find('a') for e in latest_articles.find_all('div', class_='content')]:
        url = title_elem.get('href')
        if not url:
            # 20100602140130, no url
            url = generate_dummy_url('tsf.pt', 'tsfmodern', 'Últimas', title_elem)
            category = 'Outras'
        else:
            # sometimes it might not be possible to infer category even with url, thus the alternative
            category = category_from_url_new(title_elem.get('href')) or 'Outras'

        all_news.append({
            'article_url': url,
            'title': title_elem.get_text(),
            'category': category,
            'importance': Importance.LATEST
        })


def extract_desporto_modern(all_news, desporto_articles):
    for title_elem in [e.find('a') for e in desporto_articles]:
        pretitle_elem = title_elem.find_previous('table', class_='TagArea').find('h2', class_=re.compile(r'^Tag1|0$'))

        url = title_elem.get('href')
        if not url or url.endswith('http://Lusa'):
            # 20100405144754, no url
            # 20150530170220, weird Lusa url
            url = generate_dummy_url('tsf.pt', 'tsfmodern', 'Desporto', title_elem)

        all_news.append({
            'article_url': url,
            'title': title_elem.get_text(),
            'headline': pretitle_elem.get_text(),
            'category': 'Desporto',
            'importance': Importance.SMALL
        })


class ScraperTSF09(NewsScraper):
    source = 'tsf.pt'
    cutoff = 20150907170222

    def extract_large_article(self, all_news, article_elem):
        img_elem = article_elem.find('div', class_='newsimg')
        if img_elem and img_elem.find('script'):
            return  # ignore flash player articles

        img_url = img_elem.find('img').get('src') if img_elem and img_elem.find('img') else None  # extrac check for img because of 20131102170242

        pretitle_elem = article_elem.find('a', class_='taglnk')
        pretitle = pretitle_elem.find('img').get('alt') if pretitle_elem else None

        title_elem = article_elem.find('a', class_='titlnk')
        title = title_elem.get_text() if title_elem else None  # 20110422150224, almost empty page
        if not title:
            return  # special img only element 20100505170135

        url = title_elem.get('href')
        if not url:
            url = generate_dummy_url(self.source, 'tsf09', 'DestaquesLarge', title_elem)  # no url @ 20100607140128

        snippet_elem = article_elem.find('p')
        snippet = snippet_elem.get_text() if snippet_elem else None  # 20110617150229

        all_news.append({
            'article_url': url,
            'title': title,
            'headline': pretitle,
            'snippet': snippet,
            'img_url': img_url,
            'category': 'Destaques',
            'importance': Importance.LARGE
        })

        related_elem = article_elem.find('div', class_=re.compile(r'^ulist[0-9]*$'))
        if related_elem:
            for title_elem in [e.find('a') for e in related_elem.find_all('li')]:
                title = title_elem.get_text()
                if not title:
                    continue  # 20150902170220

                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title,
                    'category': 'Destaques',
                    'importance': Importance.RELATED
                })

    def scrape_page(self, soup):
        all_news = []

        feature_articles = soup.find_all('div', id=re.compile(r'^tabf_[0-9]{7}$'))
        for article_elem in feature_articles:
            pretitle_elem = article_elem.find('a', class_='txttag')
            pretitle = pretitle_elem.get_text() if pretitle_elem else None  # 20110510150233

            title_elem = article_elem.find('div', class_='hl_header').find('a')
            url = title_elem.get('href') or generate_dummy_url(self.source, 'tsf09', 'FeatureTop', title_elem)  # no url @ 20120701150249

            snippet_elem = article_elem.find('div', class_='hl_txt')
            snippet = snippet_elem.get_text() if snippet_elem else None

            img_elem = article_elem.find('div', class_='hl_img').find('img')
            img_url = img_elem.get('src') if img_elem else None

            all_news.append({
                'article_url': url,
                'title': title_elem.get_text(),
                'headline': pretitle,
                'snippet': snippet,
                'img_url': img_url,
                'category': 'Destaques',
                'importance': Importance.FEATURE
            })

        large_articles = soup.find_all('div', class_='tsfmiddle250_news')
        for article_elem in large_articles:
            self.extract_large_article(all_news, article_elem)

        more_large_articles = soup.find_all('div', class_='tsfmiddle390_news')
        for article_elem in more_large_articles:
            self.extract_large_article(all_news, article_elem)

        economia_articles = soup.find('div', class_='EconoNews')
        if economia_articles:  # 20110422150224, almost empty page
            for title_elem in [e.find('a') for e in economia_articles.find_all('li')]:
                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title_elem.get_text(),
                    'category': 'Economia',
                    'importance': Importance.SMALL
                })

        latest_articles_elem = soup.find('div', id='divMaisRecentes')
        if latest_articles_elem:  # 20110422150224, almost empty page
            extract_latest_modern(all_news, latest_articles_elem)

        desporto_articles = soup.find('table', class_='Desporto')
        if desporto_articles:  # 20110422150224, almost empty page
            extract_desporto_modern(all_news, desporto_articles.find_all('h1'))

        return all_news


class ScraperTSF10(NewsScraper):
    source = 'tsf.pt'
    cutoff = 20151231204526  # might work past this, not tested

    def scrape_page(self, soup):
        all_news = []

        feature_articles = soup.find_all('article')
        for article_elem in feature_articles:
            if article_elem.find_parent('aside'):
                continue  # promo stuff

            if article_elem.find_parent('div', class_=re.compile(r'^t-sidebar-envelope-[0-9]$')):
                continue  # sidebar not needed

            if article_elem.find('input'):
                continue  # ignore newsletter

            # determine prominence
            parent_section = article_elem.find_parent('section')
            if parent_section:
                if re.match(r't-featured-section-[0-9]', parent_section.get('class')[0]):
                    importance = Importance.FEATURE
                elif re.match(r't-section-list-[0-9]', parent_section.get('class')[0]):
                    importance = Importance.LARGE
                else:
                    raise Exception
            else:
                parent_section = article_elem.find_parent('div', class_='t-drawer-pages')
                if parent_section:
                    importance = Importance.SMALL
                else:
                    raise Exception

            # get elements
            img_elem = article_elem.find('figure')
            img_url = img_elem.find('img').get('src') if img_elem else None

            pretitle_elem = article_elem.find(re.compile(r'^(span|strong)$'), class_=re.compile(r'^t-article-theme'))
            pretitle = pretitle_elem.get_text().title() if pretitle_elem else None

            title_elem = article_elem.find('span', class_='t-article-title') or article_elem.find('h3') or article_elem.find('h4')
            title = title_elem.get_text()

            snippet_elem = article_elem.find(re.compile(r'^(span|div)$'), class_='t-article-lead')
            snippet = snippet_elem.get_text() if snippet_elem else None

            url_elem = img_elem.find_parent('a') if img_elem else article_elem.find('header').find('a')
            url = url_elem.get('href')

            # category from url
            if re.match(r'.*http://eleicoes\.tsf\.pt/.*', url):
                category = 'Política'
            else:
                category = re.match(r'.*http://www\.tsf\.pt/([A-Za-z_-]*)/.*', url).group(1)

            if category.lower() in ['programa', 'programas', 'forum_tsf', 'forum-tsf', 'publireportagem', 'i']:
                continue

            if category == 'eleicoes':
                category = 'Política'
                pretitle = 'Eleições'

            if pretitle and pretitle.lower() == category.lower():
                pretitle = None  # remove redundancy

            all_news.append({
                'title': title,
                'article_url': url,
                'headline': pretitle,
                'snippet': snippet,
                'img_url': img_url,
                'category': category,
                'importance': importance
            })

        return all_news
