import re

from bs4 import NavigableString, Comment

from src.categories import bind_category
from src.util import generate_dummy_url, get_direct_strings, find_comments, find_comments_regex, is_between, \
    is_between_nonrecursive, is_after, generate_destaques_uniqueness
from src.text_util import remove_clutter, clean_special_chars, prettify_text, ignore_title, clean_spacing

from src.scrapers.news_scraper import NewsScraper, Importance


def previous_string(elem):
    while elem:
        if isinstance(elem, NavigableString):
            return elem
        else:
            elem = elem.previous


def sanitise_url(url, timestamp, category, title):
    if url.startswith('javascript:ShowNews'):
        return generate_dummy_url('sapo', timestamp, category, title)
    return url


class ScraperSapoNoticias02(NewsScraper):
    source = 'noticias.sapo.pt'
    cutoff = 19990429132749

    def scrape_page(self, soup):
        all_news = []

        img_articles = soup.find('tr', attrs={'bgcolor': '#dddddd'}).find_all('td')
        for article_elem in img_articles:
            url_elem = article_elem.find('a')

            img_elem = url_elem.find('img')
            img_url = img_elem.get('src') if img_elem else None

            all_news.append({
                'article_url': url_elem.get('href'),
                'title': article_elem.find('strong').get_text(),
                'img_url': img_url,
                'category': 'Destaques',
                'importance': Importance.FEATURE
            })

        side_articles_elem = soup.find('td', attrs={'bgcolor': '#FFF4D2', 'valign': 'TOP', 'width': 125}).find('font', attrs={'size': 2, 'face': 'Arial, Helvetica'})
        for url_elem in side_articles_elem.find_all('a'):
            title = previous_string(url_elem)
            category = url_elem.find_previous('font', attrs={'color': '#FF0000'}).get_text()

            all_news.append({
                'article_url': sanitise_url(url_elem.get('href'), 'sapo02', category, title),
                'title': title,
                'category': category,
                'importance': Importance.SMALL
            })

        return all_news


class ScraperSapoNoticias03(NewsScraper):
    source = 'noticias.sapo.pt'
    cutoff = 19991114103617

    def scrape_page(self, soup):
        all_news = []

        article_elems = soup.find_all('table', attrs={'bgcolor': '#FFF4D2', 'width': 106})
        for article_elem in article_elems:
            category = article_elem.find('font', attrs={'color': 'FFFFFF'}).find('b').get_text()

            inner_article = article_elem.find('center')
            url_elem = inner_article.find('a')
            title_elem = inner_article.find('font', attrs={'size': 1, 'face': 'helvetica'})

            img_url = url_elem.find('img').get('src')
            if not img_url.endswith('.JPG'):
                img_url = None  # ignore when it's a category image

            all_news.append({
                'article_url': url_elem.get('href'),
                'title': title_elem.get_text(),
                'img_url': img_url,
                'category': category,
                'importance': Importance.FEATURE
            })

        return all_news


class ScraperSapoNoticias04(NewsScraper):
    source = 'noticias.sapo.pt'
    cutoff = 20010202144300

    def get_category(self, filename):
        cat_id = filename.split('/')[-1].replace('.GIF', '')

        # unknown categories, don't seem to fit the repository
        if cat_id in ['32', '77', '117']:
            return None

        categories = {
            '80': 'Política',
            '79': 'Internacional',
            '110': 'Internacional',
            '96': 'Sociedade',
            '78': 'Local e Regional',
            '81': 'Cultura',
            '71': 'Comunidades Lusófonas',
            '74': 'Economia',
            '72': 'Economia',
            '114': 'Economia',
            '73': 'Educação',
            '109': 'Portugal',
        }

        return categories[cat_id]

    def scrape_page(self, soup):
        all_news = []

        article_boxes = soup.find('td', attrs={'width': 319}).find_all('p')
        feature_article = article_boxes[0]
        url_img_elem = feature_article.find('a', recursive=False)
        title_elem = feature_article.find('font', attrs={'size': 4}).find('b').find('a')

        snippet = get_direct_strings(feature_article)
        img_url = url_img_elem.find('img').get('src')
        if not img_url.endswith('.JPG'):
            img_url = None  # ignore when it's a category image (eg 20000310150241)

        all_news.append({
            'article_url': url_img_elem.get('href'),
            'title': title_elem.get_text(),
            'snippet': snippet,
            'img_url': img_url,
            'category': 'Destaques',
            'importance': Importance.FEATURE
        })

        other_articles = article_boxes[1].find_all('table', recursive=False)[-1].find_all('tr')
        for article_elem in other_articles:
            category_elem = article_elem.find('td').find('a').find('img')
            category = self.get_category(category_elem.get('src'))

            if not category:
                continue

            inner_article = article_elem.find_all('td')[1]
            title_elem = inner_article.find('a')
            snippet = inner_article.find('font', attrs={'size': 1}).get_text()

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet,
                'category': category,
                'importance': Importance.LARGE
            })

        return all_news


class ScraperSapoNoticias05(NewsScraper):
    source = 'noticias.sapo.pt'
    cutoff = 20010516023359

    def scrape_page(self, soup):
        all_news = []

        top_box = soup.find('table', attrs={'width': 455, 'cellspacing': 5})
        for article_elem in [e.find_parent('div', attrs={'align': 'center'}) for e in top_box.find_all('span', class_='titdestaque')]:
            title_elem = article_elem.find('span', class_='titdestaque')
            img_url = article_elem.find('img').get('src')

            all_news.append({
                'article_url': title_elem.find_parent('a').get('href'),
                'title': title_elem.get_text(),
                'img_url': img_url,
                'category': 'Destaques',
                'importance': Importance.LARGE
            })

        feature_elems = [e.find_parent('td') for e in soup.find_all('span', class_='titdestaque') if not e.find_parent('table', attrs={'cellspacing': 5})]
        for article_elem in feature_elems:
            category_elem = article_elem.find('span', class_='destaque')
            title_elem = article_elem.find('span', class_='titdestaque')
            snippet_elem = article_elem.find('span', class_='textopreto')

            all_news.append({
                'article_url': title_elem.find_parent('a').get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet_elem.get_text(),
                'category': category_elem.get_text(),
                'importance': Importance.FEATURE
            })

        latest_elem = soup.find('img', attrs={'src': re.compile(r'ultimas_lateral\.gif$')}).find_next('td')
        for title_elem in latest_elem.find_all('a', recursive=False):
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'category': 'Destaques',
                'importance': Importance.LATEST
            })

        return all_news


def extract_snippet_after(elem, after, ignore=[]):
    # useful when snippet and title are in the same element, this gets everything after the title
    # getting only direct navigable strings would ignore parts of the text in bold or italics
    snippet = ''

    for el in elem.contents:
        if not is_after(after, el) or isinstance(el, Comment):
            continue
        if el.name in ignore:
            continue
        snippet += el if isinstance(el, NavigableString) else el.get_text()

    return snippet


def get_source(source):
    if source in ['Lusa', 'Sol', 'TSF', 'TeK', 'SIC', 'GameOver', 'RTN', 'RTP', 'Time Out', 'Volante', 'Expresso',
                  'Visão', 'Naturlink', 'Pplware', 'Superstars', 'Blitz', 'Autosport', 'Tek', 'Green Savers',
                  'Relvado', 'MAG', 'TVNet', 'TvNet', 'TV Net', 'TVNET']:
        return source

    if source.startswith('SAPO') or source in ['Vídeos', 'Desporto', 'Cinema', 'Música', 'TV', 'Família', 'Lifestyle']:
        return 'SAPO'

    return {
        'DN': 'Diário de Notícias',
        'DN MAD': 'Diário de Notícias',
        'DN/Lusa': 'Diário de Notícias',

        'JN': 'Jornal de Notícias',

        'AO': 'Açoriano Oriental',

        'DD': 'Diário Digital',
        'DD/Lusa': 'Diário Digital',

        'DE': 'Diário Económico',
        'DE/LUSA': 'Diário Económico',
        'Económico': 'Diário Económico',

        'SIC/Lusa': 'SIC',

        'Sol/Lusa': 'Sol',
        'SOL': 'Sol',

        'RR-L': 'Rock In Rio',

        'DA': 'Diário de Aveiro',

        'RR': 'Rádio Renascença',
        'Renascença': 'Rádio Renascença',
        'Renascenca': 'Rádio Renascença',

        'Exame Expresso': 'Expresso',

        'CMTV': 'Correio da Manhã',
    }[source]


class ScraperSapoNoticias06(NewsScraper):
    source = 'noticias.sapo.pt'
    cutoff = 20050820060144

    def infer_category(self, url):
        return url.split('=')[-1] if 'tsfnoticias.com' in url else 'Destaques'

    def get_category_pretitle(self, header_text):
        # conform header text to category, or use it as pretitle and define its category accordingly
        try:
            try_cat = bind_category(header_text)
            return try_cat.value, None
        except Exception:
            if header_text in ['Ataque aos EUA', 'Afeganistão', 'Alemanha', 'Guerra ao Terrorismo', 'Timor-Leste',
                               'Itália', 'Crise Indo-Paquistanesa', 'Tensão na Ásia do Sul', 'Crise no Golfo',
                               'Médio Oriente', 'Espanha', 'França', 'Venezuela', 'Iraque', 'Israel', 'Washington',
                               'Roma', 'Terrorismo']:
                return 'Mundo', header_text

            if header_text in ['Madeira', 'Açores', 'Ponta Delgada', 'Faro', 'Amadora', 'Torres Vedras']:
                return 'Local', header_text

            if header_text in ['Mundial 2002', 'Ciclismo', 'I Liga', 'Meia-Maratona de Lisboa', 'Selecção',
                               'União de Leiria-FC Porto', 'Europeu', 'Sporting', 'José António Camacho', 'Superliga',
                               'Portugal 1 - Itália 2']:
                return 'Desporto', header_text

            if header_text in ['Cancro da mama']:
                return 'Saúde', header_text

            if header_text in ['Orçamento', 'Assembleia', 'Autárquicas', 'PP/Açores', 'OE 2001', 'Autárquicas/Coimbra',
                               'Orçamento de Estado', 'A caminho do Governo', 'Parlamento', 'Barómetro', 'PS',
                               'Lei dos Partidos', 'Constituição']:
                return 'Política', header_text

            if header_text in ['Património', 'Entre-os-Rios', 'Aborto', 'Justiça', 'Impostos', 'Guimarães',  # Guimarães is an article referring to the country
                               '5 de Outubro']:
                return 'Portugal', header_text

            if header_text in ['Universidade dos Açores', 'Ensino básico', 'Escolaridade obrigatória', 'Superior']:
                return 'Educação', header_text

            if header_text in ['Paulo Portas', 'Manuel Monteiro', 'Rúben Capela', 'Felícia Cabrita']:
                return 'Opinião', header_text

            if header_text in ['Sistema solar']:
                return 'Ciência', header_text

            if header_text in ['Fura dels Bau', 'Casa da Música', 'Concerto', 'Exposição']:
                return 'Cultura', header_text

            if header_text in ['Verão']:
                return 'Sociedade', header_text

            if header_text in ['Dossier', 'ETC']:
                return None, None

            return 'Destaques', header_text

    def extract_feature_articles(self, all_news, feature_elem, category, source):
        # get main feature
        main_feature_elems = feature_elem[0].find('tr').find_all('td')

        img_elem = main_feature_elems[1].find('img')
        url_elem = main_feature_elems[0].find('a', class_='a2')

        inner_elem = url_elem.find('font')
        title_elem = inner_elem.find('b')
        snippet = extract_snippet_after(inner_elem, title_elem)

        url = url_elem.get('href')
        if url.endswith('infordesporto.sapo.pt'):
            # 20031208224331, got only site url
            url += '/' + generate_destaques_uniqueness(category, inner_elem.get_text(), snippet)

        all_news.append({
            'article_url': url,
            'title': inner_elem.find('b').get_text(),
            'snippet': snippet,
            'img_url': img_elem.get('src'),
            'source': source,
            'category': category or self.infer_category(url_elem.get('href')),
            'importance': Importance.FEATURE
        })

        # get other features
        other_feature_rows = feature_elem[1].find_all('tr', attrs={'valign': 'top'})
        other_feature_elems = []
        for row in other_feature_rows:
            other_feature_elems += row.find_all('td', attrs={'colspan': 2})

        for article_elem in [e.find('a') for e in other_feature_elems]:
            pretitle_elem = article_elem.find('b')
            title = extract_snippet_after(article_elem, pretitle_elem)

            if not title:
                continue  # 20040925022458

            all_news.append({
                'article_url': article_elem.get('href'),
                'title': title,
                'headline': pretitle_elem.get_text(),
                'source': source,
                'category': category or self.infer_category(article_elem.get('href')),
                'importance': Importance.FEATURE
            })

    def process_tsf_elem(self, all_news, tsf_elem):
        start_feature = find_comments(tsf_elem, ' modulo de noticias ')[0]
        end_feature = find_comments(tsf_elem, ' FIM modulo de noticias ')[0]
        feature_elem = [e for e in tsf_elem.find_all('table') if is_between_nonrecursive(start_feature, end_feature, e)]
        self.extract_feature_articles(all_news, feature_elem, None, 'TSF')

        start_latest = find_comments(tsf_elem, ' ultimas noticias ')[0]
        latest_elem = start_latest.find_next_sibling('table')

        for title_elem in latest_elem.find_all('a', class_='a2'):
            title = title_elem.get_text()
            if not title:
                continue  # 20040616005651

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title,
                'source': 'TSF',
                'category': self.infer_category(title_elem.get('href')),
                'importance': Importance.LATEST
            })

    def process_infordesporto_elem(self, all_news, infordesporto_elem):
        start_feature = find_comments(infordesporto_elem, ' modulo de noticias ')[0]
        end_feature = find_comments(infordesporto_elem, ' FIM modulo de noticias ')[0]
        feature_elem = [e for e in infordesporto_elem.find_all('table') if is_between_nonrecursive(start_feature, end_feature, e)]
        self.extract_feature_articles(all_news, feature_elem, 'Desporto', 'Infordesporto')

        start_diarioeconomico = find_comments_regex(infordesporto_elem, r'^\s*DIARIO ECONOMICO.*$')
        if start_diarioeconomico:
            start_diarioeconomico = start_diarioeconomico[0]
            diarioeconomico_articles = start_diarioeconomico.find_next_sibling('table').find_next_sibling('table').find_all('tr', attrs={'valign': 'top'})

            for article_elem in [e.find('a', class_='a2') for e in diarioeconomico_articles]:
                pretitle_elem = article_elem.find('b')
                title = extract_snippet_after(article_elem, pretitle_elem)

                all_news.append({
                    'article_url': article_elem.get('href'),
                    'title': title,
                    'headline': pretitle_elem.get_text(),
                    'source': 'Diário Económico',
                    'category': 'Destaques',
                    'importance': Importance.SMALL
                })
        else:
            # we got agencia financeira instead (20020529010101)
            start_agencia = find_comments(infordesporto_elem, ' modulo de noticias ')

            if len(start_agencia) > 1:
                start_agencia = start_agencia[1]
                article_elems = start_agencia.find_next_sibling('table').find_all('font', attrs={'size': -2})

                for title_elem in [e.find('a', class_='a2') for e in article_elems]:
                    all_news.append({
                        'article_url': title_elem.get('href'),
                        'title': title_elem.get_text(),
                        'source': 'Agência Financeira',
                        'category': 'Economia',
                        'importance': Importance.SMALL
                    })
            else:
                # got nothing there then...
                pass

    def process_hoje_elem(self, all_news, hoje_elem):
        start_feature = find_comments(hoje_elem, ' modulo de noticias ')[0]
        end_feature = find_comments(hoje_elem, ' FIM modulo de noticias ')[0]

        hoje_table = [e for e in hoje_elem.find_all('table') if is_between_nonrecursive(start_feature, end_feature, e)][0]

        article_elems = hoje_table.find_all('font', attrs={'size': -2})
        for article_elem in article_elems:
            inner_elem = article_elem.find('b')
            header_elem = article_elem.find('a', class_='a2')

            category, pretitle = self.get_category_pretitle(header_elem.get_text())
            if not category:
                continue

            source = get_direct_strings(inner_elem)
            matcher = re.match(r'^\((.*)\) -', source)
            source = get_source(matcher.group(1))

            all_news.append({
                'article_url': header_elem.get('href'),
                'title': get_direct_strings(article_elem),
                'headline': pretitle,
                'category': category,
                'source': source,
                'importance': Importance.SMALL
            })

    def scrape_page(self, soup):
        all_news = []

        # TSF main section
        start_tsf = find_comments_regex(soup, r'^\s*TSF cor.*$')[0]
        end_tsf = find_comments(soup, ' FIM TSF ')[0]
        tsf_elem = [e for e in soup.find_all('table') if is_between_nonrecursive(start_tsf, end_tsf, e)][1]
        self.process_tsf_elem(all_news, tsf_elem)

        # infordesporto and diario economico section
        start_infordesporto = find_comments_regex(soup, r'^\s*INFORDESPORTO cor.*$')[0]
        end_infordesporto = find_comments(soup, ' FIM Infordesporto/diario economico ')[0]
        infordesporto_elem = [e for e in soup.find_all('table') if is_between_nonrecursive(start_infordesporto, end_infordesporto, e)][0].find('tr')
        self.process_infordesporto_elem(all_news, infordesporto_elem)

        # "hoje nos jornais"
        start_hoje = find_comments_regex(soup, r'^\s*HOJE NA IMPRENSA cor.*$')[0]
        hoje_elem = start_hoje.find_next_sibling('table').find_next_sibling('table')
        self.process_hoje_elem(all_news, hoje_elem)

        return all_news


class ScraperSapoNoticias07(NewsScraper):
    source = 'noticias.sapo.pt'
    cutoff = 20070217132649

    def extract_box(self, all_news, box_elem, category):
        main_elem = box_elem.find('div', class_='manchete').find('a')

        img_elem = main_elem.find('img')

        title_elem = main_elem.find('span', class_='titulo')
        if title_elem:
            # "good" organised box
            title = title_elem.get_text()
            pretitle_elem = main_elem.find('span', class_='antTitulo')
        else:
            pretitle_elem = main_elem.find('b')
            title = extract_snippet_after(main_elem, pretitle_elem, ['a'])

        # try to see if there's a source in the title
        source = 'SAPO Notícias'
        match = re.match(r'(.*)(?:\((.*)\))', title)
        if match:
            title = match.group(1)
            source = match.group(2)

        all_news.append({
            'article_url': main_elem.get('href'),
            'title': title,
            'pretitle': pretitle_elem.get_text(),
            'img_url': img_elem.get('src'),
            'source': source,
            'category': category,
            'importance': Importance.FEATURE
        })

        # other news
        other_features = box_elem.find_all('a', recursive=False)
        for article_elem in other_features:
            title_elem = article_elem.find('span', class_='titulo')
            pretitle_elem = article_elem.find('span', class_='antTitulo')

            all_news.append({
                'article_url': article_elem.get('href'),
                'title': title_elem.get_text(),
                'pretitle': pretitle_elem.get_text(),
                'source': 'SAPO Notícias',
                'category': category,
                'importance': Importance.SMALL
            })

    def scrape_page(self, soup):
        all_news = []

        # features
        feature_boxes = soup.find_all('div', class_='destaques')
        for elem in feature_boxes:
            category_elem = find_comments_regex(elem, r'^\s*INICIO DESTAQUES .*\s*$')
            category = re.match(r'^\s*INICIO DESTAQUES (.*)\s*$', category_elem[0]).group(1).strip()
            self.extract_box(all_news, elem, category)

        # latest
        latest_box = soup.find('div', class_='ultimas')
        for title_elem in latest_box.find_all('a'):
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.find('span', class_='titulo').get_text(),
                'source': 'Diário Digital',
                'category': 'Outras',
                'importance': Importance.LATEST
            })

        return all_news


class ScraperSapoNoticias08(NewsScraper):
    source = 'noticias.sapo.pt'
    cutoff = 20111025150210

    def clean_title(self, title):
        match = re.match(r'^[0-9][0-9]:[0-9][0-9] - (.*)', title)
        new_title = match.group(1) if match else title

        # remove some stuff that might be mixed up with the source
        remove = ['(vídeo)', '(II)', '(comentário)', '(C/INFOGRAFIA))', '(fotos)', '()', '(c/áudio)',
                  '(C/VÍDEO e C/ÁUDIO)', '(ATUALIZADA)', '(som)', '(SÍNTESE)', '(Continuação)', '(c/ vídeo)',
                  '(REPORTAGEM VÍDEO)', '(actualização)', '(COM VÍDEO)', '(com vídeo)', '(act.)', '(vídeos)',
                  '(fotogaleria)', '(fotogaleria e vídeo)', '(vídeo e fotogaleria)']
        for s in remove:
            new_title = new_title.replace(s, '')

        return new_title

    def extract_large_article(self, all_news, elem, importance):
        img_elem = elem.find('img')
        img_url = img_elem.get('src') if img_elem else None

        pretitle_elem = elem.find('h2')
        pretitle = pretitle_elem.get_text() if pretitle_elem else None

        title_elem = elem.find('h1')
        title = self.clean_title(title_elem.get_text().strip())

        if not title and not pretitle:
            return  # happens at 20110922150214

        if not title:
            # happens at 20100529140109
            title = pretitle
            pretitle = None

        if 'opinião do leitor' in title:
            return  # 20100530140109

        snippet_elem = elem.find('p', recursive=False)

        # try to find source from title
        match = re.match(r'(.*)\((\D*)\)$', title)  # match anything but digits, because of football results (eg 20100626140107)
        if match and match.group(2) not in ['Rock/Blues', 'BE', 'McLaren', 'PSD']:  # 20100626140107
            title = match.group(1)
            source = get_source(match.group(2))
        else:
            # try to find source from span
            source_elem = elem.find('span', class_='source')
            source = clean_spacing(source_elem.get_text())

        url_elem = elem.find('a')
        url = url_elem.get('href') if url_elem.get('href') else generate_dummy_url(self.source, 'sapo08', source+snippet_elem.get_text(), title)  # no href in 20100619140107

        all_news.append({
            'article_url': url,
            'title': title,
            'pretitle': pretitle,
            'snippet': snippet_elem.get_text(),
            'img_url': img_url,
            'source': source,
            'category': 'Destaques',
            'importance': importance
        })

        # related seem to be exactly the same as the main (because they're all probably taken from Lusa),
        # but on different sources, so didn't add them

    def extract_lusa(self, all_news, title_elem):
        all_news.append({
            'article_url': title_elem.get('href'),
            'title': self.clean_title(title_elem.get_text()),
            'source': 'Lusa',
            'category': 'Destaques',
            'importance': Importance.LATEST
        })

    def scrape_page(self, soup):
        all_news = []

        # features
        feature_box = soup.find('ul', id='snDestaques') or soup.find('ul', class_='snDestaques')

        main_features = feature_box.find_all('li', class_='newsbig')
        for elem in main_features:
            self.extract_large_article(all_news, elem, Importance.FEATURE)

        other_features = feature_box.find_all('li', id=re.compile(r'ntp[0-9]+'))
        for elem in other_features:
            self.extract_large_article(all_news, elem, Importance.FEATURE)

        large_articles = (soup.find('ul', id='snUltimas') or soup.find('ul', class_='snUltimas')).find_all('li', id=re.compile(r'ntp[0-9]+'))
        for elem in large_articles:
            self.extract_large_article(all_news, elem, Importance.LARGE)

        lusa_articles = soup.find('div', id='boxLusa').find('div', class_='snBoxContent').find_all('li', class_='newsitem')
        for elem in lusa_articles:
            self.extract_lusa(all_news, elem.find('a'))

        return all_news


class ScraperSapoNoticias09(NewsScraper):
    source = 'noticias.sapo.pt'
    cutoff = 20140930170207

    def convert_source(self, source):
        return {
            'noticias.sapo.pt': 'SAPO Notícias',
            'saude.sapo.pt': 'SAPO Notícias',
            'noticias.sapo.tl': 'SAPO Notícias',
            'desporto.sapo.pt': 'SAPO Notícias',
            'musica.sapo.pt': 'SAPO Notícias',
            'livros.sapo.pt': 'SAPO Notícias',
            'cesariaevora.sapo.cv': 'SAPO Notícias',
            'saponoticias.blogs.sapo.pt': 'SAPO Notícias',
            'videos.sapo.pt': 'SAPO Notícias',
            'querosaber.sapo.pt': 'SAPO Notícias',
            'cinema.sapo.pt': 'SAPO Notícias',
            'boasnoticias.sapo.pt': 'SAPO Notícias',
            'noticias.sapo.mz': 'SAPO Notícias',
            'tv.sapo.pt': 'SAPO Notícias',
            'crescer.sapo.pt': 'SAPO Notícias',

            'www.rr.pt': 'Rádio Renascença',
            'rr.sapo.pt': 'Rádio Renascença',

            'www.sol.pt': 'Sol',
            'sol.sapo.pt': 'Sol',

            'www.expresso.pt': 'Expresso',
            'expresso.sapo.pt': 'Expresso',

            'diariodigital.sapo.pt': 'Diário Digital',
            'www.diariodigital.sapo.pt': 'Diário Digital',

            'sicnoticias.sapo.pt': 'SIC Notícias',
            'economico.sapo.pt': 'Diário Económico',
            'visao.sapo.pt': 'Visão',
            'dinheirodigital.sapo.pt': 'Dinheiro Digital',
            'autosport.sapo.pt': 'AutoSport',
            'tek.sapo.pt': 'TeK',
            'portocanal.sapo.pt': 'Porto Canal',
            'cmtv.sapo.pt': 'Correio da Manhã',
            'exameinformatica.sapo.pt': 'Exame Informática',
            'turbo.sapo.pt': 'Turbo',
            'greensavers.sapo.pt': 'Green Savers'
        }[source]

    def extract_main_article(self, all_news, article_elem):
        title_elem = (article_elem.find('h1') or article_elem.find('h2')).find('a')

        source_elem = article_elem.find('span', class_='sourceURL')
        source = self.convert_source(source_elem.get_text()) if source_elem else 'SAPO Notícias'

        inner_elem = article_elem.find('div', class_='headings')
        img_elem = (inner_elem or article_elem).find('img')

        snippet_elem = (inner_elem or article_elem).find('p', class_='lead')
        snippet = snippet_elem.get_text() if snippet_elem else None

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title_elem.get_text(),
            'snippet': snippet,
            'img_url': img_elem.get('src'),
            'source': source,
            'category': 'Destaques',
            'importance': Importance.FEATURE
        })

    def scrape_page(self, soup):
        all_news = []

        # features
        main_box = soup.find('ul', class_='headlines')
        for elem in main_box.find_all('li', class_='main'):
            self.extract_main_article(all_news, elem)

        for elem in main_box.find_all('li', class_='secondary'):
            self.extract_main_article(all_news, elem)

        section_boxes = soup.find_all('div', class_='newsByTopic')  # includes latest
        for section_box in section_boxes:
            category = section_box.find('h3').get_text()

            for article_elem in section_box.find('ul', class_='listing').find_all('li', recursive=False):
                # single elem
                if 'class' in article_elem.attrs and 'single' in article_elem.attrs['class']:
                    article_elem = article_elem.find('a')

                    title_elem = article_elem.find('h4')
                    img_elem = article_elem.find('img')
                    snippet_elem = article_elem.find('p', class_='lead')

                    all_news.append({
                        'article_url': article_elem.get('href'),
                        'title': title_elem.get_text(),
                        'snippet': snippet_elem.get_text(),
                        'img_url': img_elem.get('src'),
                        'category': category,
                        'importance': Importance.LARGE
                    })
                else:
                    title_elem = article_elem.find('h4').find('a')

                    source_elem = article_elem.find('p', class_='source')
                    source = source_elem.get_text().replace('Fonte: ', '') or 'SAPO Notícias'

                    pretitle_elem = article_elem.find('p', class_='preTitle')
                    pretitle = pretitle_elem.get_text() if pretitle_elem else None

                    snippet_elem = article_elem.find('p', class_='lead')
                    snippet = snippet_elem.get_text() if snippet_elem else None

                    all_news.append({
                        'article_url': title_elem.get('href'),
                        'title': title_elem.get_text(),
                        'pretitle': pretitle if pretitle and len(pretitle) > 0 else None,
                        'snippet': snippet,
                        'source': get_source(source),
                        'category': category,
                        'importance': Importance.LATEST if category == 'Últimas' else Importance.SMALL
                    })

        return all_news


class ScraperSapoNoticias10(NewsScraper):
    source = 'noticias.sapo.pt'
    cutoff = 20151112224517  # might work past this, not tested

    def scrape_page(self, soup):
        all_news = []

        # sections
        section_elems = soup.find_all('section', id=re.compile(r'noticias-.*'))
        for section_elem in section_elems:
            category = re.match(r'noticias-(.*)', section_elem.attrs['id']).group(1)

            for article_elem in section_elem.find_all('article'):
                img_elem = article_elem.find('figure')
                img_url = img_elem.find('img').get('src') if img_elem else None

                title_elem = article_elem.find('span', class_='title')

                source_elem = article_elem.find('span', class_='source')
                source = get_source(source_elem.get_text()) if source_elem else 'SAPO Notícias'

                snippet_elem = article_elem.find('p', class_='lead')
                snippet = snippet_elem.get_text() if snippet_elem else None

                all_news.append({
                    'article_url': title_elem.find_parent('a').get('href'),
                    'title': title_elem.get_text(),
                    'snippet': snippet,
                    'img_url': img_url,
                    'source': source,
                    'category': category,
                    'importance': Importance.SMALL if 'class' not in article_elem.attrs else Importance.FEATURE if 'mega' in article_elem.attrs['class'] else Importance.LARGE
                })

                # related
                related_elem = article_elem.find('ul', class_='related')
                if related_elem:
                    for article_elem in [e.find('a') for e in related_elem.find_all('li')]:
                        all_news.append({
                            'article_url': article_elem.get('href'),
                            'title': article_elem.find('span', class_='title').get_text(),
                            'source': get_source(article_elem.find('span', class_='source').get_text()),
                            'category': category,
                            'importance': Importance.RELATED
                        })

        return all_news
