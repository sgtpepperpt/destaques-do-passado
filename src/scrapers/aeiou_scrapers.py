import re

from bs4 import NavigableString, Comment, Tag

from src.util import is_link_pt, find_comments, is_between, find_comments_regex, get_direct_strings
from src.text_util import remove_clutter, clean_special_chars, prettify_text, ignore_title

from src.scrapers.news_scraper import NewsScraper, Importance


def process_source(source):
    if source == 'Publico':
        return 'Público', 'Genérico'
    if source == 'Canal_Negocios':
        return 'Canal de Negócios', 'Economia'
    if source == 'Recortes':
        return 'Recortes', 'Tecnologia'
    if source == 'Musicnet':
        return 'Musicnet', 'Entretenimento'
    if source in ['Jornal_Noticias', 'J.Notícias']:
        return 'Jornal de Notícias', 'Genérico'
    if source == 'Infordesporto':
        return 'Infordesporto', 'Desporto'
    if source == 'Record':
        return 'Record', 'Desporto'
    if source == 'FocusOnline':
        return 'Focus', 'Genérico'
    if source in ['Euronoticias', 'Euronotícias']:
        return 'EuroNotícias', 'Genérico'
    if source == 'Valor':
        return 'Valor', 'Economia'
    if source == 'ZDNet':
        return 'ZDNet', 'Economia'
    if source == 'vida':
        return 'Vida', 'Entretenimento'
    if source == 'Ideias_Negocios':
        return 'Ideias e Negócios', 'Economia'
    if source in ['relvado', 'Relvado']:
        return 'Relvado', 'Desporto'

    # follwing only appear on the red version
    if source in ['Expresso', 'BolsaPT', 'Tecmania', 'TSF', 'Diário de Notícias', 'O Jogo', 'Agência Financeira',
                  '123 Som', 'Estreia Online', 'A Bola', 'Infodesktop', 'Público']:
        return source, None

    if source == 'Ciberia':
        return 'Cibéria', None
    if source == 'Negocios.pt':
        return 'Jornal de Negócios', None

    raise Exception


class ScraperAeiou01(NewsScraper):
    source = 'aeiou.pt'
    cutoff = 19991117010356

    def scrape_page(self, soup):
        all_news = []

        start_marker = find_comments(soup, 'Inicio Quiosque')[0]
        end_marker = find_comments(soup, ' Fim Quiosque')[0]  # space intended
        quisoque = [e for e in soup.find_all('table', attrs={'bgcolor': '#ffffff'}) if is_between(start_marker, end_marker, e)][0]

        source = 'AEIOU'
        category = 'Genérico'
        for elem in quisoque.find_all('tr'):
            # process img elems
            img_elem = elem.find('img')
            if img_elem:
                if img_elem.get('src').endswith('branco.gif'):
                    continue

                # get article's source
                source = img_elem.get('alt')
                source, category = process_source(source)
                continue

            title_elem = elem.find('font', attrs={'face': 'Arial,Helvetica', 'size': -2})
            if not title_elem:
                continue

            title_elem = title_elem.find('a')
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': remove_clutter(title_elem.get_text()),
                'source': source,
                'category': category,
                'importance': Importance.SMALL
            })

        return all_news


def scrape_first_version(soup):
    all_news = []

    start_marker = find_comments_regex(soup, 'Inicio Quiosque')[0]
    end_marker = (find_comments(soup, ' Fim Quiosque') or find_comments(soup, 'Fim Quiosque'))[0]  # space intended
    quisoque = [e for e in soup.find_all('font', attrs={'face': 'Arial,Helvetica', 'size': -2}) if
                is_between(start_marker, end_marker, e)][0]

    source = 'AEIOU'
    category = 'Genérico'
    for elem in quisoque.find_all(re.compile(r'a|img')):
        if elem.name == 'img':
            if elem.get('src').endswith('branco.gif'):
                continue

            # get article's source
            source = elem.get('alt')
            source, category = process_source(source)
            continue

        # if not an image then it's a title
        title = remove_clutter(elem.get_text())
        if title == 'mais notícias':
            continue

        all_news.append({
            'article_url': elem.get('href'),
            'title': title,
            'source': source,
            'category': category,
            'importance': Importance.SMALL
        })

    return all_news


def get_snippet_elems(elems):
    snippet_elems = [e for e in elems if isinstance(e, NavigableString) and not isinstance(e, Comment) or isinstance(e, Tag) and e.name in ['b', 'i']]

    source = None
    elems = []
    for elem in snippet_elems:
        if isinstance(elem, NavigableString) and (elem.strip().startswith(',') or elem.strip().startswith('(')):
            source = clean_special_chars(elem.replace('(', ''))
            continue

        if isinstance(elem, Tag):
            elems.append(remove_clutter(elem.get_text()))
        else:
            elems.append(remove_clutter(elem))

    elems = [e for e in elems if len(e) > 0]
    return ''.join(elems), source


def scrape_red_version(soup):
    all_news = []

    start_marker = find_comments_regex(soup, ' inicio noticia destaque quiosque ')[0]
    end_marker = find_comments(soup, ' fim noticia destaque quiosque ')[0]
    feature_elem = [e for e in soup.find_all('table') if is_between(start_marker, end_marker, e)][0]

    img_elem = feature_elem.find_all('tr')[1].find_all('td')[-1].find('img', attrs={'alt': '[Foto]'})
    main_elem = feature_elem.find('td', recursive=False)
    title_elem = main_elem.find('a', class_='qiosktit')

    # source in later versions is a link
    direct_source = main_elem.find('a', class_='qiosklnk', recursive=False)
    if direct_source:
        source = direct_source.get_text().replace('(', '').replace(')', '')

        # get snippet freely, knowing that source isn't there
        snippet_elems = [remove_clutter(e) for e in main_elem.contents if isinstance(e, NavigableString) and not isinstance(e, Comment)]
        snippet_elems = [e for e in snippet_elems if len(e) > 1]  # this ignores ()
        snippet = ' '.join(snippet_elems)
    else:
        # gets snippet and source
        snippet, source = get_snippet_elems(main_elem.contents)

    all_news.append({
        'article_url': title_elem.get('href'),
        'title': title_elem.get_text(),
        'snippet': snippet,
        'img_url': img_elem.get('src'),
        'source': process_source(source)[0] if source else 'AEIOU.pt',  # starting 20031222093143 it can be a source in itself
        'category': 'Genérico',
        'importance': Importance.FEATURE
    })

    start_marker = find_comments_regex(soup, ' inicio headlines quiosque ')[0]
    end_marker = find_comments(soup, ' fim headlines quiosque ')[0]
    quiosque_elem = [e for e in soup.find_all('table') if is_between(start_marker, end_marker, e)][0]

    for title_elem in quiosque_elem.find_all('a', class_='qiosklnk'):
        category_elem = title_elem.find_previous('td', class_='trezea')
        category = clean_special_chars(category_elem.get_text()) if category_elem else 'Genérico'

        source = process_source(clean_special_chars(title_elem.next_sibling))[0]

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title_elem.get_text(),
            'source': source,
            'category': category,
            'importance': Importance.SMALL
        })

    return all_news


class ScraperAeiou02(NewsScraper):
    source = 'aeiou.pt'
    cutoff = 20070306023751

    def scrape_page(self, soup):
        # detect version, since they alternate heavily here
        first_version_marker = len(find_comments_regex(soup, 'Inicio Quiosque')) > 0
        if first_version_marker:
            return scrape_first_version(soup)
        else:
            return scrape_red_version(soup)


class ScraperAeiou03(NewsScraper):
    source = 'aeiou.pt'
    cutoff = 20090520103730

    def scrape_page(self, soup):
        all_news = []

        category_elems = soup.find_all('div', id=re.compile(r'^cx_if_[A-Za-z]*$'))
        for category_elem in category_elems:
            category = re.match(r'^cx_if_([A-Za-z]*)$', category_elem.get('id')).group(1)
            if category == 'tags':
                continue  # 20070406030156, avoid tags

            # get elements which have a snippet
            article_elems = category_elem.find_all(re.compile(r'^(td|div)$'), class_='caixa_info_texto')
            for article_elem in article_elems:
                if article_elem.find('div', class_='caixa_td_tag_txt'):
                    continue  # 20070414135441, avoid tag elems

                img_elem = article_elem.find('img', class_='caixa_info_imagem')
                img_url = img_elem.get('src') if img_elem else None

                title_elem = article_elem.find('a', class_='caixa_info_titulo')

                snippet = get_direct_strings(article_elem)

                newer_bottom_elem = article_elem.find('span', class_='caixa_info_data')
                if newer_bottom_elem and newer_bottom_elem.find('a', class_='caixa_info_plussign'):
                    source = newer_bottom_elem.find('a', class_='caixa_info_plussign').get_text()
                else:
                    source = 'AEIOU.pt'

                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title_elem.get_text(),
                    'snippet': snippet,
                    'img_url': img_url,
                    'source': source,
                    'category': category,
                    'importance': Importance.FEATURE if img_url else Importance.LARGE
                })

            # get small elements
            article_elems = category_elem.find_all('ul', class_='caixa_info_ul')
            for article_elem in article_elems:
                if article_elem.find('li', class_=re.compile(r'caixa_info_titulo_li_(gra|sm)')):
                    continue  # ignore sports results

                title_elem = article_elem.find('li', class_='caixa_info_titulo_li').find('a')

                inner_category = category  # avoids hiding parent category below

                # get source (+ category if present)
                main_bottom_elem = article_elem.find('li', class_='caixa_info_data_li')
                # check if newer version
                newer_version = main_bottom_elem.find('a', class_='caixa_info_plussign')
                if newer_version:
                    source = newer_version.get_text()
                else:
                    # trim [] and get comma-separated elems
                    bottom_elems = main_bottom_elem.get_text()[1:-1].split(',')

                    # in the main tab (em foco) a category may be contained too
                    if len(bottom_elems) > 2:
                        # bug starting 20070407084004, only replace category if not one of these
                        if bottom_elems[0] not in ['aeiou', 'Segunda 17', 'Segunda 7'] \
                                and not bottom_elems[0].startswith('Terça') \
                                and not bottom_elems[0].startswith('Quarta') \
                                and not bottom_elems[0].startswith('Quinta') \
                                and not bottom_elems[0].startswith('Sexta') \
                                and not bottom_elems[0].startswith('Sábado') \
                                and not bottom_elems[0].startswith('Domingo'):
                            inner_category = bottom_elems[0]

                    source = clean_special_chars(bottom_elems[-1])

                # ignore some categories
                if inner_category in ['Fórum']:
                    continue  # appears first at 20070930171308

                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title_elem.get_text(),
                    'source': source,
                    'category': inner_category,
                    'importance': Importance.SMALL
                })

        return all_news


class ScraperAeiou04(NewsScraper):
    source = 'aeiou.pt'
    cutoff = 20100520160530

    def scrape_page(self, soup):
        all_news = []

        # in this version only the "em foco" box is archived
        articles = soup.find('div', id='bx_info-1').find('div', class_='efLinks').find_all('li', class_=re.compile(r'^mbot0[0-9]$'))
        for article_elem in articles:
            title_elem = article_elem.find('a', class_='lst_ttl') \
                         or article_elem.find('a', class_='f13') \
                         or article_elem.find('a', recursive=False) \
                         or article_elem.find('span', class_='dgray')

            if title_elem.name != 'a':
                title_elem = title_elem.find('a')

            snippet_elem = article_elem.find('span', class_='descr_txt_12')
            snippet = get_direct_strings(snippet_elem) if snippet_elem else None

            source_elem = article_elem.find('a', class_='descr_lnk_11 tc b')
            source = source_elem.get_text()

            img_elem = article_elem.find('img', class_=re.compile(r'^im(?:left|right)$'))
            img_url = img_elem.get('src') if img_elem else None

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet,
                'img_url': img_url,
                'source': source,
                'category': 'Em foco',
                'importance': Importance.LARGE
            })

        return all_news


class ScraperAeiou05(NewsScraper):
    source = 'aeiou.pt'
    cutoff = 20120327150246

    def compress_categories(self, category):
        pretitle = None
        if category in ['Transportes', 'Alimentação', 'Protesto', 'Óbito', 'Investigação', 'Turismo', 'Aviação',
                        'Automóveis', 'Entrevista', 'Estudo', 'Cozinha internacional', 'Funeral este Domingo',
                        'Automóvel', 'Violência', 'Habitação', 'Memória', 'Família', 'Redes Sociais', 'Morte',
                        'Crime', 'Droga', 'Solstício', 'Crime informático', 'Papa em Espanha', 'Solidariedade',
                        'Igreja', 'APAV', 'My Social Project', 'Alergias']:
            pretitle = category
            category = 'Sociedade'

        elif category in ['Automobilismo', 'FC Porto', 'Braga 3-0 Celtic', 'Liga de futebol 2010/11', 'Sp.Braga',
                          'Un.Leiria 0-3 Benfica', 'Benfica 4-2 Nacional', 'Marítimo 0-3 Sporting',
                          'Crise agrava-se em Alvalade', 'Jesus não poupou jogadores', 'Derby eterno já ferve',
                          'Benfica, FC Porto, Sporting e Sp. Braga', 'Pontapé de Saída', 'Dérbi em Alvalade',
                          'Benfica', 'Crónica do Jogo', 'Liga Relvado', 'Sporting', 'A grande final', 'Cartão Roxo',
                          'Transferências', 'Seleção', 'Portugal-Bósnia', 'Zenit-Benfica',
                          'Man. City, 4 - FC Porto, 0', 'Exclusivo Relvado', 'Sorteio da UEFA',
                          'Gil Vicente-Sporting (2-0)']:
            pretitle = category
            category = 'Desporto'

        elif category in ['Ricardo Araújo Pereira', 'Rui Santos', 'Análise de Rui Santos', 'Análise Rui Santos']:
            pretitle = category
            category = 'Opinião'

        elif category in ['Trabalho', 'Presidenciais', 'Greve', 'Nova Lei', 'Estado da Nação', 'Nova lei', 'Eleições',
                          'Função Pública', 'Estado', 'Acordo Ortográfico', 'Presidência da República', 'PSD',
                          'Congresso PSD']:
            pretitle = category
            category = 'Política'

        elif category in ['PT/Vivo', 'Agricultura', 'Saldos', 'Profissões de futuro', 'Crédito à habitação', 'Consumo',
                          'Combustíveis', 'Aumentos', 'Medida "Estímulo 2012"', 'Empreendedorismo', 'Desemprego',
                          'Marcas', 'Mercado Imobiliário', 'Restauração']:
            pretitle = category
            category = 'Economia'

        elif category in ['África do Sul', 'Brasil', 'China', 'Finlândia', 'Irão', 'Espanha', 'Homicídio no Brasil',
                          'Alemanha', 'Ameaça', 'Suíça', 'Grécia', 'Itália', 'Terrorismo', 'Paris', 'Reino Unido',
                          'Líbia', 'Nova Zelândia', 'Japão', 'Venezuela', 'EUA', 'Libia', 'Bélgica', 'União Europeia',
                          'Cimeira UE', 'Wikileaks', 'França']:
            pretitle = category
            category = 'Mundo'

        elif category in ['Impostos', 'Portagens', 'Finanças', 'IRS', 'SCUT', 'Calor', 'SCUTs', 'Justiça', 'Incêndio',
                          'Incêndios', 'Incêndios 2010', 'Marinha', 'Madeira', 'Acidente A25', 'Acidente',
                          'Regresso de férias', 'Julgamento', 'Sentença', 'Crise', 'Corrupção', 'Orçamento de Estado',
                          'Operação Furacão', 'Processo Casa Pia', 'Manifestação', 'Abuso', 'Sequestro',
                          'Emprego', '"Face Oculta"', 'Austeridade', 'Ajuda Externa', 'Sinistralidade', 'Comboios',
                          'Temporal', 'Paralização', 'Estrada', 'Aborto', 'Segurança Social', 'Privatizações', 'Seca',
                          'Troika', 'Caso Santa Maria', 'Feriados', 'Política de Austeridade', 'Dia do Consumidor',
                          'Electricidade', 'Tauromaquia', 'Greve geral']:
            pretitle = category
            category = 'Portugal'

        elif category in ['José Saramago', 'Livro', 'Música: Stereophonics', 'Óscares', 'Dia Mundial do Teatro']:
            pretitle = category
            category = 'Cultura'

        elif category in ['Red Bull', 'Rei da Pop', 'Escape - Cartaz', 'Estreias de cinema', 'Globos de Ouro',
                          'Grammys', 'Optimus Primavera Sound', 'Óscares 2012', '38ª Edição ModaLisboa']:
            pretitle = category
            category = 'Entretenimento'

        elif category in ['Energia', 'Futuro', 'Gadgets', 'PlayStation', 'Telemóveis', 'Global Blackout', 'Megaupload']:
            pretitle = category
            category = 'Tecnologia'

        elif category in ['Acção Social']:
            pretitle = category
            category = 'Educação'

        elif category in ['Metro do Porto', 'EMEL', 'Viana do Castelo']:
            pretitle = category
            category = 'Local'

        elif category in ['Nutrição', 'Astronomia']:
            pretitle = category
            category = 'Ciência'

        elif category in ['Hora do Planeta']:
            pretitle = category
            category = 'Ambiente'

        elif category in ['Tempo', 'Metereologia', 'Viagem', 'Iniciativa', 'Gastronomia', 'Psicanálise', 'Luxo',
                          'Sexo', 'Celebridades', 'Reportagem', 'Salazar: 40 anos', 'Polémica', 'Famosos',
                          'Efeméride', 'Naturismo', 'Revelação', 'Cidade', 'Sabores', 'Casamento real', 'Cronologia',
                          'Escape', 'Prémio', 'Imagem', 'Meteo', 'Prémios', 'Beleza', 'Imobiliário', 'Exclusivo', 'FMI',
                          'Fenómeno', 'Personalidades', 'Agressão sexual', 'Truques', 'Motins', 'Reynaldo Gianecchini',
                          'Alerta', 'Indignação geral', 'Aniversário', 'Meteorologia', 'Internt', 'Biografia',
                          'Infografia', 'UNESCO', 'Bronca', 'Segurança', 'Natal', 'Mensagem de Natal',
                          'Passagem de ano', 'Balanço', 'Calendário', 'Mensagem de ano novo', 'Escape: Boa Mesa',
                          'Diversos', 'Carnaval', 'Agenda', 'Sondagem', 'Media', 'Dia dos Namorados', 'Sugestões',
                          'ACTA', 'Operação Carnaval', 'Arquitectura', 'Curiosidades', '7 Maravilhas', 'Audiências',
                          'Comércio', 'Primavera']:
            pretitle = category
            category = 'Outras'

        return category, pretitle

    def get_box_news(self, all_news, box_elem, category):
        big_feature = box_elem.find('div', class_='cboth hidden mbot12 f12')
        if not big_feature:
            return  # 20111113160404, boxes not archived

        img_elem = big_feature.find('a', recursive=False)
        img_url = img_elem.find('img').get('src') if img_elem else None

        # go a bit deeper, only the image was outside "oauto"
        big_feature = big_feature.find('div', class_='oauto')

        title_elem = big_feature.find('div', class_='f14').find('a')
        title = title_elem.get_text()

        # a big feature is not always present (20100602140130)
        if title:
            snippet = get_direct_strings(big_feature)

            source_elem = big_feature.find('a', class_='hl f11 b')
            source = source_elem.get_text() if source_elem else 'AEIOU'

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title,
                'snippet': snippet,
                'img_url': img_url,
                'source': source,
                'category': category,
                'importance': Importance.FEATURE
            })

        small_features = box_elem.find('ul', class_='f12').find_all('li')
        for elem in small_features:
            title_elem = elem.find('a')

            source_elem = elem.find('a', class_='hl f11 b')
            source = source_elem.get_text() if source_elem else 'AEIOU'

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'source': source,
                'category': category,
                'importance': Importance.SMALL
            })

    def scrape_page(self, soup):
        all_news = []

        # get big photo features
        screens = soup.find('div', class_='screens').find_all('div', class_=re.compile(r'player-[0-9]+'))
        titles = soup.find('div', class_='titles').find_all('div', id=re.compile(r'tplayer-[0-9]+'))

        for i in range(len(screens)):
            screen = screens[i]
            title = titles[i]

            if screen.find('object'):
                continue  # 20120121191726, flash, videos, etc.

            title_elem = screen.find('div', class_='content').find('a', class_='', recursive=False)  # no class is important

            # these are always present
            img_url = screen.find('a').find('img').get('src')
            snippet = screen.find('div', class_='content').find('span', class_='f12').get_text()

            # get source by image (original method) or by text (from 20120121191726)
            source = screen.find('div', class_='content').find('a', class_='brand')
            if source:
                source = source.find('img').get('title')
            else:
                source = screen.find('div', class_='content').find('a', class_='mais').get_text()

            # category from title elem
            # they aren't exactly categories 100% but close enough that they can be compressed into ones
            category_elem = title.find('span', class_='f11 grey nb')
            category = category_elem.get_text() if category_elem else None

            if category:
                # exclusion criteria
                match1 = re.match(r'Vídeo do Dia [0-9]+', category)
                match2 = re.match(r'Receita do dia [0-9]+', category)
                if match1 or match2:
                    continue

                # reject some unfitting categories
                if category in ['Exclusivo Expresso', 'Viajar', 'Verão', 'À borla', 'Roteiro', 'Gravuras', 'Férias',
                                'Boa Mesa', 'Viagens', 'Vídeo', 'Boa Cama', 'Inovação', 'Publicidade', 'Borlas',
                                'Astrologia', 'Fotogaleria', 'Ócio', 'Lingerie', 'Galeria', 'S. Valentim',
                                'A estreia do comentador', 'Escape - Borlas', 'Fantásticas ofertas', 'Video',
                                'Sugestão', 'Marketing', 'Álbum de fotos', 'Passatempo', 'Romance', 'FOTOS',
                                'Escape: Passatempo', 'Escape: Borlas', 'Votação', 'Boas Festas', 'Off-side',
                                'Multimédia', 'Fórum']:  # too time-specific / sponsored content
                    continue
            else:
                category = 'Em foco'  # rare, 20100614140130

            # alter some categories and re-purpose them as pretitles
            category, pretitle = self.compress_categories(category)

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet,
                'headline': pretitle,
                'img_url': img_url,
                'source': source,
                'category': category,
                'importance': Importance.FEATURE
            })

        # informação section below photos
        informacao_box = soup.find('div', id='informacao').find('div', class_='content')
        self.get_box_news(all_news, informacao_box, 'Em foco')

        # sports box
        desporto_box = soup.find('div', id='desporto')
        if desporto_box:  # 20111113160404, box not archived
            self.get_box_news(all_news, desporto_box.find('div', class_='content'), 'Desporto')

        return all_news


class ScraperAeiou06(NewsScraper):
    source = 'aeiou.pt'
    cutoff = 20151231180212  # not tested thereafter

    def extract_article(self, all_news, article_elem, category):
        possible_span_title = article_elem.find('span')
        title_elem = possible_span_title if possible_span_title and len(possible_span_title.get_text()) > 0 else article_elem
        img_elem = article_elem.find('img')

        # snippet element and source are hidden from view!
        snippet = article_elem.get('title')
        source = 'AEIOU'

        source_match = re.match(r'(.*) \((.*)\)$', snippet)
        if source_match:
            snippet = source_match.group(1)
            source = source_match.group(2)

            if source in ['foto', 'VÍDEO']:
                source = 'AEIOU'  # accidentally captured something not intended as source

        # ignore if encoding problems
        snippet = None if snippet.count('?') > 2 else snippet

        # special case 20120701150250
        if snippet == 'Chamadas em ':
            snippet = None

        all_news.append({
            'article_url': article_elem.get('href'),
            'title': title_elem.get_text(),
            'img_url': img_elem.get('src') if img_elem else None,
            'snippet': snippet,
            'source': source,
            'category': category,
            'importance': Importance.LARGE
        })

    def scrape_page(self, soup):
        all_news = []

        box_elems = soup.find_all('div', id=re.compile(r'box-section-[0-9]+'))
        for box_elem in box_elems:
            category = box_elem.find('h3').get_text()

            title_elems = [e.find('a') for e in box_elem.find('ul').find_all('li')]
            for article_elem in title_elems:
                self.extract_article(all_news, article_elem, category)

        # image articles
        img_articles = soup.find(re.compile(r'^(ul|div)$'), id='destaques').find_all('li')
        for article_elem in [e.find('a') for e in img_articles]:
            self.extract_article(all_news, article_elem, 'Outras')

        return all_news
