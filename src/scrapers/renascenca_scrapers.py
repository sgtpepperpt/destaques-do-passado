import re
from urllib.parse import unquote_to_bytes

from bs4 import BeautifulSoup

from src.scrapers.rtp_scrapers import red_scraper, modern_scraper
from src.util import generate_dummy_url, get_direct_strings, is_after, get_direct_strings_between, find_comments, \
    find_comments_regex, is_between
from src.text_util import clean_special_chars, remove_clutter

from src.scrapers.news_scraper import NewsScraper, Importance


class ScraperRenascenca01(NewsScraper):
    source = 'rr.pt'
    cutoff = 20061009131912

    def constrain_category(self, category):
        if category in ['Atenas 2004']:
            return 'Desporto', category

        return category, None

    def scrape_page(self, soup):
        all_news = []

        feature_title = soup.find('a', class_='font_tit')
        inner_elem = feature_title.find_parent('table').find_next_sibling('p') or feature_title.find_parent('tr').find_parent('tr').find_next_sibling('tr').find('p')  # 20050122093848

        img_elem = inner_elem.find('a', recursive=False)
        img_elem = img_elem.find('img') if img_elem else inner_elem.find('img')  # 20050617033556

        snippet_elem = inner_elem.find('font', class_='fonts_outros_titulos').find('b')

        all_news.append({
            'article_url': feature_title.get('href') or generate_dummy_url(self.source, 'rr01', 'manchete', feature_title),
            'title': feature_title.get_text(),
            'snippet': snippet_elem.get_text(),
            'img_url': img_elem.get('src'),
            'category': 'Destaques',
            'importance': Importance.FEATURE
        })

        category_headers = [e for e in soup.find_all('tr', attrs={'bgcolor': '#CCCCCC'}) if e.find('font', attrs={'color': '#000000'})]
        for i in range(len(category_headers)):
            category_header = category_headers[i]
            next = category_headers[i+1] if i+1 < len(category_headers) else None

            category, pretitle = self.constrain_category(clean_special_chars(category_header.get_text()))

            text_elems = category_header.find_parent('table').find_all('span', class_='FontsHomepage')
            if len(text_elems) > 0:
                # large elem with snippet
                title_elem = text_elems[0].find('b').find('a') or text_elems[0].find('b')
                snippet_elem = text_elems[1].find('p') or text_elems[1].find('font')

                all_news.append({
                    'article_url': title_elem.get('href') or generate_dummy_url(self.source, 'rr01maincat', category, title_elem),
                    'title': title_elem.get_text(),
                    'headline': pretitle,
                    'snippet': snippet_elem.get_text(),
                    'category': category,
                    'importance': Importance.LARGE
                })
            else:
                # small titles (some are repeated but url uniqueness deals with that)
                titles = category_header.find_parent('table').find_all('td', class_='fonts_outros_tit')
                titles = [e.find('a') or e.find('font') for e in titles if e.find('font', attrs={'color': '#000000'}, recursive=False) or e.find('a', recursive=False) and (is_between(category_header, next, e) if next else True)]
                for title_elem in titles:
                    all_news.append({
                        'article_url': title_elem.get('href') or generate_dummy_url(self.source, 'rr01', 'smallcats', title_elem),
                        'title': title_elem.get_text(),
                        'category': category,
                        'importance': Importance.SMALL
                    })

        latest_articles = soup.find_all('td', class_='ultimahora')
        for title_elem in [e.find('font', attrs={'size': 1}) for e in latest_articles]:
            all_news.append({
                'article_url': generate_dummy_url(self.source, 'rr01', 'ultimas', title_elem),
                'title': title_elem.find('b').get_text(),
                'category': 'Destaques',
                'importance': Importance.LATEST
            })

        return all_news


class ScraperRenascenca02(NewsScraper):
    source = 'rr.pt'
    cutoff = 20090520150926

    def extract_feature(self, all_news, feature, img_id):
        category_elem = feature.find('p', class_='categoria').find('span')
        title_elem = feature.find('span', class_='titulo')
        snippet_elem = feature.find('span', class_='lead')
        img_elem = feature.find_previous('div', id=img_id).find('img')
        url_elem = img_elem.find_parent('a')

        all_news.append({
            'article_url': url_elem.get('href'),
            'title': title_elem.get_text(),
            'snippet': snippet_elem.get_text(),
            'img_url': img_elem.get('src'),
            'category': 'Destaques',
            'importance': Importance.FEATURE
        })

        related_elems = feature.find('ul').find_all('a')
        for title_elem in related_elems:
            all_news.append({
                'article_url': url_elem.get('href'),
                'title': title_elem.get_text(),
                'category': clean_special_chars(category_elem.get_text()),
                'importance': Importance.RELATED
            })

    def scrape_page(self, soup):
        all_news = []

        self.extract_feature(all_news, soup.find('div', id='INFORMACAO'), 'IMG_INFORMACAO')
        self.extract_feature(all_news, soup.find('div', id='BOLABRANCA'), 'IMG_BOLABRANCA')

        return all_news


class ScraperRenascenca03(NewsScraper):
    source = 'rr.pt'
    cutoff = 20110925164826

    def extract_section(self, all_news, section_box, category='Destaques'):
        img_elem = section_box.find('img', class_='img')
        title_elem = section_box.find('a', class_='usual_lnk')

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title_elem.get_text(),
            'img_url': img_elem.get('src'),
            'category': category,
            'importance': Importance.FEATURE
        })

        small_news = section_box.find('div', id='outros_destaques').find_all('li')
        for article_elem in [e.find('div') for e in small_news]:
            title_elem = article_elem.find('a', class_='small_lnk')
            img_elem = article_elem.find('a', recursive=False).find('img')

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'img_url': img_elem.get('src'),
                'category': category,
                'importance': Importance.SMALL
            })

    def scrape_page(self, soup):
        all_news = []

        feature = soup.find('div', id='informacao').find('div', class_='main_tab_body')
        self.extract_section(all_news, feature)

        feature = soup.find('div', id='bola_branca').find('div', class_='main_tab_body')
        self.extract_section(all_news, feature, 'Desporto')

        return all_news


class ScraperRenascenca04(NewsScraper):
    source = 'rr.pt'
    cutoff = 20150911170225

    def extract_article(self, all_news, feature_elem, importance):
        # get image but not if there's a media player there
        img_elem = feature_elem.find('div', class_='imgNews') or feature_elem.find('div', id='imgNews')
        img_url = img_elem.find('img').get('src') if img_elem and not img_elem.find('div', id=re.compile(r'^mediaplayer')) else None

        pretitle_elem = feature_elem.find('div', class_='topTitleNews') or feature_elem.find('div', id='topTitleNews')
        pretitle = pretitle_elem.find('h4').get_text() if pretitle_elem else None

        title_elem = (feature_elem.find('div', class_='mainNewsTitle') or feature_elem.find('div', id='mainNewsTitle') or feature_elem.find('div', id='titleWithImg') or feature_elem.find('h2')).find('a')  # 20120729011312 no id or class, just h2
        title = title_elem.get_text() if title_elem else feature_elem.find('div', id='titleWithImg').find('span').get_text()  # 20111006161635

        url = title_elem.get('href') if title_elem else generate_dummy_url(self.source, 'rr04', pretitle_elem, title_elem)  # 20111006161635

        snippet_elem = feature_elem.find('div', class_=re.compile(r'^(mainLead|leadNews|leadNewsCenter)$')) or feature_elem.find('div', id=re.compile(r'^(mainLead|leadNews|leadNewsCenter)$'))
        snippet = snippet_elem.get_text() if snippet_elem else None

        category = 'Desporto' if (feature_elem.find('div', class_='topTitleNewsBolaBranca') or feature_elem.find('div', id='topTitleNewsBolaBranca')) else 'Destaques'

        all_news.append({
            'article_url': url,
            'title': title,
            'headline': pretitle,
            'snippet': snippet,
            'img_url': img_url,
            'category': category,
            'importance': importance
        })

        related_elems = feature_elem.find('div', id='relatedNews')
        if related_elems:
            for title_elem in [e.find('a') for e in related_elems.find_all('li')]:
                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title_elem.get_text(),
                    'category': category,
                    'importance': Importance.RELATED
                })

    def scrape_page(self, soup):
        all_news = []

        feature_elem = soup.find('div', id='mainNews')
        self.extract_article(all_news, feature_elem, Importance.FEATURE)

        other_article_sections = soup.find_all('div', class_='otherNews') + soup.find_all('div', id='otherNews')
        for section in other_article_sections:
            for article_elem in section.find('ul').find_all('li', recursive=False):
                self.extract_article(all_news, article_elem, Importance.LARGE)

        return all_news


class ScraperRenascenca05(NewsScraper):
    source = 'rr.pt'
    cutoff = 20151231180236  # might work longer, not tested

    def extract_article(self, all_news, title_elem, category, importance, generic_pretitle):
        inner_elem = title_elem.find_parent('div')
        article_elem = inner_elem.find_parent('div')

        title = title_elem.get_text()
        if not title:
            return  # 20150919170221

        img_elem = article_elem.find('figure', class_='ink-image')
        img_url = img_elem.find('img').get('src') if img_elem else None

        snippet_elem = inner_elem.find('span', class_='h1LeadFix')
        snippet = snippet_elem.get_text() if snippet_elem else None

        pretitle_elem = inner_elem.find('span', class_=lambda c: 'uppercase' in c and 'txtOrange' in c)
        pretitle = pretitle_elem.get_text() if pretitle_elem else generic_pretitle  # get a generic pretitle from the category section, if exists

        all_news.append({
            'article_url': title_elem.find_parent('a').get('href'),
            'title': title,
            'headline': pretitle,
            'snippet': snippet,
            'img_url': img_url,
            'category': category,
            'importance': importance
        })

        related = inner_elem.find('ul', class_=re.compile(r'^relatedArticles'))
        if related:
            for title_elem in [e.find('a') for e in related.find_all('li')]:
                all_news.append({
                    'article_url': title_elem.get('href') or generate_dummy_url(self.source, 'rr05', category, title_elem),  # 20151202180210
                    'title': title_elem.get_text(),
                    'category': category,
                    'importance': Importance.RELATED
                })

    def extract_box(self, all_news, main_box, category, generic_pretitle=None):
        feature_elems = main_box.find_all('h1', class_='h1Fix')
        for title_elem in feature_elems:
            self.extract_article(all_news, title_elem, category, Importance.FEATURE, generic_pretitle)

        large_elems = main_box.find_all('h2', class_='h2Fix')
        for title_elem in large_elems:
            self.extract_article(all_news, title_elem, category, Importance.LARGE, generic_pretitle)

        small_elems = main_box.find_all('h3', class_=re.compile(r'(h3Fix|superFix)'))
        for title_elem in small_elems:
            self.extract_article(all_news, title_elem, category, Importance.LARGE, generic_pretitle)

    def scrape_page(self, soup):
        all_news = []

        main_box = soup.find('section', class_='highlight')

        self.extract_box(all_news, main_box, 'Destaques')

        sections = soup.find('section', class_='resto').find_all('div', class_='column-group', recursive=False)
        for section_box in sections:
            header = section_box.find('div', class_=lambda c: 'uppercase' in c and 'extralarge' in c and 'txtOrange' in c, recursive=False)
            header_name = header.get_text().strip() if header else None

            include_header = not header_name or header_name in ['Bola Branca', 'Crise dos refugiados', '70 ANOS DA ONU', '70 ANOS DE ONU', '40 anos da independência de Angola']

            # redundant, but useful for breakpoint testing
            exclude_header = header_name and (
                    'V+' in header_name or 'Renascença' in header_name or 'ispos' in header_name or 'ora da ' in header_name or 'egislativa' or 'ruzadas' in header_name
                    or header_name in ['A não perder', 'Papa em Cuba', 'Papa nos Estados Unidos e Cuba']
                    or header_name.startswith('Debate') or header_name.startswith('Opinião') or header_name.startswith('Legislativas'))
            if header_name and not exclude_header and not include_header:
                print()

            category = 'Desporto' if header_name == 'Bola Branca' else 'Mundo' if header_name == '40 anos da independência de Angola' else 'Destaques'

            if include_header:
                self.extract_box(all_news, section_box, category, header_name if header_name != 'Bola Branca' else None)

        latest_elems = soup.find('ul', id='cxultimas')
        for title_elem in [e.find('a', class_='lnkBlack') for e in latest_elems]:
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'category': 'Destaques',
                'importance': Importance.LATEST
            })

        return all_news