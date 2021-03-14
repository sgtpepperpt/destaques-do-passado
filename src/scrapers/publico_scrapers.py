import re

from src.util import prettify_text, clean_special_chars, ignore_title, remove_clutter, generate_dummy_url

from src.scrapers.news_scraper import NewsScraper, Importance


# Extracts a title from an element containing it. Removes markup such as <b> and <i> tags,
# as well as the hour at the beginning.
def extract_title(elem):
    text = elem.get_text().strip()

    match_hour = re.findall(r'[012][0-9]:[0-9][0-9]\s*-(.*)', text)
    if len(match_hour) > 0:
        text = match_hour[0].strip()

    # remove a special kind of ellipsis which has a blank space before
    if text.endswith(' ...'):
        text = re.sub(r' \.\.\.', '', text)

    return remove_clutter(re.sub(r' +', ' ', text))


def process_snippet(snippet):
    if 'Life&Style' in snippet:
        return None

    return prettify_text(snippet.strip())


class ScraperPublico01(NewsScraper):
    source = 'publico.pt'
    cutoff = 19981212032121
    used = False

    # dummy scraper, returns a set of very old news only once
    def scrape_page(self, soup):
        if self.used:
            return None

        all_news = []

        timestamp = 19961013180332
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/19961013180332/http://www.publico.pt/publico/hoje/Y01X01.html',
            'img_url': 'https://arquivo.pt/wayback/19961013180354im_/http://www.publico.pt/publico/hoje/27/0/76.jpg',
            'headline': 'Cimeira de Roma pressiona líderes balcânicos',
            'title': 'Retomar a paz, unificar Sarajevo',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Autarquias vão receber o dobro do dinheiro',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Benfica-Sporting: o nulo total',
            'category': 'Desporto',
            'importance': Importance.SMALL
        })

        timestamp = 19981212032121
        all_news.append({
            'timestamp': timestamp,
            'headline': 'Os combates regressaram ao Planalto Central',
            'title': 'Começou a Terceira Guerra Civil Angolana',
            'snippet': 'O Governo angolano reclamou a conquista do Bailundo e do Andulo, os dois quartéis-generais da UNITA no Planalto Central. A UNITA desmente e fala da "surpresa dos generais de Luanda" perante a resistência do Galo Negro. Mas nenhum dos beligerantes esconde o facto essencial: "É o regresso à guerra". A terceira, com epicentro no Bié. As baixas ainda não têm número, mas já começaram.',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'headline': 'Reino Unido',
            'title': 'Luz Verde para a Clonagem Terapêutica',
            'snippet': 'Um grupo de especialistas em bioética a quem o Governo britânico pediu um parecer sobre a clonagem aconselhou ontem o Executivo de Tony Blair a autorizar a investigação de técnicas de clonagem com fins terapêuticos, para tratar doenças como o cancro e Alzheimer. Quanto à clonagem de seres humanos completos, o comité continua a recomendar a sua proibição.',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'headline': 'Narcotráfico',
            'title': 'Detido Chefe de Clã Galego Procurado Há Seis Anos',
            'snippet': 'A detenção de um conhecido narcotraficante galego e de outros três indivíduos, num hotel em Cascais, todos implicados no sequestro, em Seixas (Caminha), de um jovem de Cambados (Galiza), é o resultado mais espectacular de uma operação concertada entre as autoridades espanholas e a PJ portuguesa. Todos os envolvidos neste enredo têm antecedentes por narcotráfico.',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'headline': 'Nobel',
            'title': 'Elite de Estocolmo Rendida a Saramago',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'headline': 'NATO',
            'title': 'Futuro da Aliança Discutido em Bruxelas',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'headline': 'Clinton',
            'title': 'Defesa Não Convence Comité',
            'snippet': 'O primeiro dos dois dias dedicados à defesa de Bill Clinton não parece ter contribuído para alterar a posição dos membros do Comité Judiciário, que já tomaram a sua decisão: votar a favor da destituição do Presidente norte-americano. Durante mais de sete horas, os advogados de Clinton expuseram argumentos para tentar alterar esta decisão. Mas o Comité manteve-se impermeável.',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'headline': 'Técnica ainda mais eficiente revelada na "Science"',
            'title': 'Oito Vitelos Clonados no Japão',
            'category': 'Ciência',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'headline': 'Concurso EuroPrix MultiMediaArt 98 premeia sete trabalhos em CD-ROM e "online"',
            'title': 'O "Top" do Multimédia Europeu',
            'snippet': 'Sete trabalhos multimédia de fabrico europeu acabam de ser premiados pelo júri da primeira edição do concurso Europrix MultimediaArt . Contos para crianças, histórias policial-filosóficas, uma colecção de cartas de amor, o mundo da política suíça e outras coisas ainda. Um verdadeiro "pot-pourri" de produtos interactivos, "online" ou em CD-ROM.',
            'category': 'Tecnologia',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'headline': 'O lado negro das grandes fusões',
            'title': 'Despedimentos Globais e em Massa',
            'snippet': 'Raramente a contabilidade da concentração empresarial se faz em termos de custos sociais. Normalmente não são divulgados "rankings" de despedimentos, ao contrário do que se passa com as habituais listas com os montantes envolvidos nos maiores negócios. Em poucas semanas, soube-se de cerca de cem mil despedimentos. Em tempo de recessão semiglobal, parece que algo começa a mexer.',
            'category': 'Economia',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'headline': 'Ana Vieira, ao público',
            'title': 'A Desmontagem da Ilusão',
            'snippet': 'Inaugurou ontem na Fundação de Serralves, no Porto, uma exposição antológica de Ana Vieira. Nome significativo dos anos 60, é um exemplo da internacionalização das linguagens da arte portuguesa de então, uma época em que, por toda a parte, assistimos a várias rupturas artísticas globais A realidade dos anos 90 trazem à luz do dia uma nova dinâmica ao seu trabalho.',
            'category': 'Cultura',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'headline': 'Bruce Springsteen',
            'title': 'Regresso ao Passado em New Jersey',
            'snippet': '"Tracks", a caixa de quatro CD com refugo de 25 anos de gravação de Bruce Springsteen, não é mais que um velho sonho dos fãs do "Boss", que durante anos coleccionaram discos piratas atrás uns dos outros para poder ter acesso a tudo o que ele gravava e não lançava em disco. Springsteen contemplou-os agora com 56 temas inéditos.',
            'category': 'Música',
            'importance': Importance.LARGE
        })

        # add deterministic no url flag (deterministic because it's used as key)
        for news in all_news:
            if 'article_url' not in news:
                news['article_url'] = generate_dummy_url(self.source, news['timestamp'], news['category'], news['title'])

        self.used = True
        return all_news


class ScraperPublico02(NewsScraper):
    source = 'publico.pt'
    cutoff = 20001203173200

    def scrape_page(self, soup):
        all_news = []

        articles = soup.find('applet').find_all('param', attrs={'name': re.compile('desc[0-9]-0')})
        for article in articles:
            id = article.get('name').split('-')[0][-1]

            headline = article.find_next('param', attrs={'name': 'desc{}-1'.format(id)})
            title = article.find_next('param', attrs={'name': 'desc{}-2'.format(id)})
            url = article.find_next('param', attrs={'name': 'desturl{}-1'.format(id)}) or article.find_next('param', attrs={'name': 'desturl{}-2'.format(id)})

            has_own_title = not not title
            coalesced_headline = headline.get('value').strip() if has_own_title else None
            coalesced_title = title.get('value') if has_own_title else headline.get('value')

            if coalesced_title == 'Artigo':
                continue

            all_news.append({
                'article_url': url.get('value'),
                'headline': coalesced_headline,
                'title': coalesced_title.strip(),
                'category': article.get('value'),
                'importance': Importance.SMALL
            })

        return all_news


class ScraperPublico03(NewsScraper):
    source = 'publico.pt'
    cutoff = 20010709145903

    def scrape_page(self, soup):
        all_news = []

        # destaque
        destaque = soup.find_all(class_='destaque')
        if len(destaque) > 1:
            raise Exception('Invalid!!!')
        destaque = destaque[0]
        url = destaque['href']
        head = destaque.find_previous(class_='destaqueseccao').get_text()
        snippet = destaque.find_next(class_='destaquecorpo').get_text()

        img_src_relative = destaque.find_next('img')['src']
        img_src = re.search(r'(.*/).*', url.replace('ultimahora.publico', 'www.publico')).group(1) + img_src_relative

        snippet = process_snippet(snippet)
        if snippet:
            all_news.append({
                'article_url': url,
                'img_url': img_src,
                'headline': remove_clutter(head),
                'title': extract_title(destaque),
                'snippet': snippet,
                'category': 'Destaque',
                'importance': Importance.FEATURE
            })

        # seccoes principais
        ultima_hora = destaque.find_parent('table').find_parent('table').find_parent('table').find('tr').find_all('td', recursive=False)[1].find('table')
        desporto = ultima_hora.find(class_='titseccoes')

        category = 'Última hora'
        articles = ultima_hora.find_all(class_='noticiasseccao')
        for article in articles:
            # change category when we pass the delimiter
            if article.sourceline*1000 + article.sourcepos > desporto.sourceline*1000 + desporto.sourcepos:
                category = 'Desporto'

            title = article.find_next(class_='noticiastitulo')

            all_news.append({
                'article_url': title['href'],
                'headline': article.get_text(),
                'title': extract_title(title),
                'category': category,
                'importance': Importance.SMALL
            })

        return all_news


class ScraperPublico04(NewsScraper):
    source = 'publico.pt'
    cutoff = 20050221185812

    v1 = {
        'destaque_title': 'titulodestaque1',
        'destaque_head': 'titulosdestaques',
        'destaque_snippet': 'textodestaques',
        'destaque_2_title': 'textodestaques',
        'articles_title': 'titulosdestaques'
    }

    v2 = {
        'destaque_title': 'textoTituloVermelho',
        'destaque_head': 'textoAntetitulo',
        'destaque_snippet': 'textoCaixa',
        'destaque_2_title': 'textoTituloPreto',
        'articles_title': 'textoCaixaLink'
    }

    def scrape_page(self, soup):
        all_news = []

        # destaque
        v = self.v1
        destaque = soup.find_all(class_=v['destaque_title'])
        if len(destaque) == 0:
            v = self.v2
            destaque = soup.find_all(class_=v['destaque_title'])

        if len(destaque) > 1:
            raise Exception('Invalid!!!')

        destaque = destaque[0]
        head = destaque.find_previous(class_=v['destaque_head']).find(text=True) or ''
        snippet_elem = destaque.find_next(class_=v['destaque_snippet'])
        snippet = process_snippet(snippet_elem.get_text())
        if snippet:
            img_src = self.find_image(destaque['href'], destaque)

            all_news.append({
                'article_url': destaque['href'],
                'img_url': img_src,
                'headline': remove_clutter(head),
                'title': extract_title(destaque),
                'snippet': snippet,
                'category': 'Destaque',
                'importance': Importance.FEATURE
            })
        ################################################################################################################
        # segundo destaque
        destaque_2 = snippet_elem.find_next(class_=v['destaque_2_title'])

        if v == self.v1:
            destaque_2_title = destaque_2.find(class_='titulosdestaques')
            if destaque_2_title:
                destaque_2_snippet = str(destaque_2_title.find_next_sibling('p').next)
            else:
                destaque_2_title = destaque_2.find(class_='titulosdestaquesCopy')
                destaque_2_snippet = destaque_2_title.get_text()
        else:
            destaque_2_title = destaque_2
            destaque_2_snippet = destaque_2.find_next(class_='textoCaixa').get_text()

        img_src = self.find_image(destaque_2_title['href'], destaque_2)

        snippet = process_snippet(destaque_2_snippet)
        if snippet:
            all_news.append({
                'article_url': destaque_2_title['href'],
                'img_url': img_src,
                'title': extract_title(destaque_2_title),
                'snippet': snippet,
                'category': 'Destaque',
                'importance': Importance.FEATURE
            })
        ################################################################################################################
        # seccoes principais
        if v == self.v1:
            articles = destaque.find_parent('table').find_parent('table').find_parent('table').find_parent('tr').find_next_sibling('tr').find_all(class_='textodestaques')
        else:
            # go to the second feature and find articles below it (but still inside the "main" news table)
            find_articles = destaque.find_parent('table').find(class_=v['destaque_2_title']).find_parent('tr')
            while True:
                find_articles = find_articles.find_next_sibling('tr')
                articles = find_articles.find(class_=v['articles_title'])
                if articles:
                    break

            articles = articles.find_parent('td').find_all(class_='textoCaixa')

        for article in articles:
            title = article.find_next(class_=v['articles_title'])

            all_news.append({
                'article_url': title['href'],
                'headline': article.find(text=True),
                'title': extract_title(title),
                'category': 'Desporto' if 'desporto.publico.pt' in title['href'] else 'Última hora',
                'importance': Importance.SMALL
            })

        return all_news

    def find_image(self, example_link, elem):
        while True:
            elem = elem.find_next('img')
            if not elem['src'].endswith('.gif'):
                return re.search(r'(.*/).*', example_link.replace('ultimahora.publico', 'www.publico')).group(1) + elem['src']


class ScraperPublico05(NewsScraper):
    source = 'publico.pt'
    cutoff = 20071118104048

    def scrape_page(self, soup):
        all_news = []

        # destaque
        destaques = soup.find_all(id='caixasNoticias')
        for destaque in destaques:
            head = destaque.find(text=True)
            title = destaque.find(class_='manchete').find('a')
            snippet = process_snippet(destaque.find(class_='textoNews').find(text=True))

            if not snippet:
                continue

            all_news.append({
                'article_url': title['href'],
                'headline': remove_clutter(head),
                'title': extract_title(title.find('strong')),
                'snippet': snippet,
                'category': 'Destaque',
                'importance': Importance.FEATURE
            })

        # get news by category, ignore empty elements
        seccoes = [seccao for seccao in soup.find_all(id='caixaSeccoes') if seccao.find(id='linhaTitulosHeader')]
        for seccao in seccoes:
            category = seccao.find(id='linhaTitulosHeader').find(text=True)

            if self.ignore_category(category):
                continue

            articles = seccao.find_all(id='seccaoTitulo')
            for article in articles:
                title_elem = article.find('a')
                title = extract_title(title_elem)

                # sometimes the news title is "hidden", having no title
                # (aka article probably removed and left an element as ghost)
                if not title:
                    continue

                if ignore_title(title):
                    continue

                # news articles can be repeated between destaques and the other sections
                # ignore the second occurence (since destaques has more info)
                if self.has_title(all_news, title):
                    continue

                all_news.append({
                    'article_url': title_elem['href'],
                    'title': title,
                    'category': category,
                    'importance': Importance.SMALL
                })

        return all_news

    def has_title(self, news, title):
        for article in news:
            if article['title'] == title:
                return True
        return False

    def ignore_category(self, category_text):
        return category_text in ['Media', 'Media e Tecnologia']


class ScraperPublico06(NewsScraper):
    source = 'publico.pt'
    cutoff = 20090926091624

    def scrape_page(self, soup):
        all_news = []

        news_table = soup.find('div', class_=re.compile('manchete_[0-9]*')).find_parent('table')

        # destaque
        destaques = news_table.find_all('div', class_=re.compile('manchete_[0-9]*'))
        for destaque in destaques:
            title = destaque.find('a')

            # sometimes we get a "video" element here
            if not title:
                continue

            snippet = process_snippet(title.find_next(class_='verdana_11_gray').find(text=True))
            if not snippet:
                continue

            all_news.append({
                'article_url': title['href'],
                'title': extract_title(title.find('b')),
                'snippet': snippet,
                'category': 'Destaque',
                'importance': Importance.FEATURE
            })

        # get related news
        seccoes = news_table.find_all(class_='verdana_10_blue')
        for seccao in seccoes:
            title_elem = seccao.find('a')
            title = extract_title(title_elem)

            if ignore_title(title):
                continue

            category = 'Destaque'
            if title.startswith('Opinião:'):
                category = 'Opinião'

            all_news.append({
                'article_url': title_elem['href'],
                'title': title,
                'category': category,
                'importance': Importance.RELATED
            })

        # get categorised news
        seccoes_table = soup.find(id='ctl00_ContentPlaceHolder1_Ultimas_TableUltimas')
        if not seccoes_table:
            return all_news

        seccoes_table = seccoes_table.find_all(class_='cabecasSeparadores')
        for seccao in seccoes_table:
            category = str(seccao.find(text=True))

            if self.ignore_category(category):
                continue

            seccao_table = seccao.find_parent('table').find_all(class_='verdana_10_blue')
            for article in [article.find('a') for article in seccao_table]:
                title = extract_title(article)

                if ignore_title(title):
                    continue

                all_news.append({
                    'article_url': article['href'],
                    'title': title,
                    'category': category,
                    'importance': Importance.SMALL
                })

        return all_news

    def ignore_category(self, category_text):
        return category_text in ['Media', 'Media e Tecnologia']


class ScraperPublico07(NewsScraper):
    source = 'publico.pt'
    cutoff = 20121116161647

    def scrape_page(self, soup):
        all_news = []

        # find big feature
        feature = soup.find(class_='feature-big')
        if feature:
            feature_box = feature.find(class_='feature-big-text')
            title = feature_box.find('a')
            snippet = process_snippet(str(feature_box.find_all('p')[-1].find(text=True)))

            if snippet:
                # check for image
                img_elem = feature.find('img')
                img_src = None
                if img_elem:
                    img_src = img_elem['src']

                all_news.append({
                    'article_url': self.cleanup_url(title['href']),
                    'title': extract_title(title),
                    'snippet': snippet,
                    'img_url': img_src,
                    'category': 'Destaque',
                    'importance': Importance.FEATURE
                })

        # find all articles in the left or middle column ("desporto box" handled separately)
        main_articles = [article for article in soup.find_all('div', class_='entry') if (article.find_parent(id="sec-content") or article.find_parent(id="main-content"))
                         and not article.find_parent(class_="desporto box")
                         and not article.find_parent(id='feature-verao2011')
                         and not article.find_parent(id='feature-911')
                         and not article.find_parent(id='feature-publico-mais')]

        for article in main_articles:
            title_elem = article.find('a')
            snippet = article.find(class_='entry-body').find_all('p')[-1]

            if snippet.find('iframe'):
                # ignore "youtube" news
                continue

            snippet = process_snippet(snippet.get_text())
            if not snippet:
                continue

            title = extract_title(title_elem)
            if ignore_title(title):
                continue

            # check for image
            img_elem = article.find(class_='entry-img')
            img_src = None
            if img_elem and img_elem.find('img'):
                img_src = img_elem.find('img')['src']

            # check for category
            category = 'Destaque'
            if 'mundial2010' in article.attrs['class']:
                category = 'Desporto'

            all_news.append({
                'article_url': self.cleanup_url(title_elem['href']),
                'title': title,
                'snippet': snippet,
                'img_url': img_src,
                'category': category,
                'importance': Importance.LARGE
            })

            # some news link to related articles
            related_news = article.find(class_='entry-links')
            if related_news:
                for news in related_news.find_all('a'):
                    # ignore "news" that lead to other sites, found out by having an absolute link instead of relative
                    if news['href'].startswith('https://arquivo.pt') and 'publico.pt/' not in news['href']:
                        continue

                    title = extract_title(news)
                    if not title or ignore_title(title):
                        continue

                    # check for category
                    category = 'Outras'
                    if 'mundial2010' in article.attrs['class']:
                        category = 'Desporto'

                    article_url = self.cleanup_url(news['href'])
                    # handle a special case where the site didn't have a link for the article
                    if len(article_url) == 0:
                        article_url = generate_dummy_url(self.source, 'parser07', category, title)

                    all_news.append({
                        'article_url': article_url,
                        'title': title,
                        'category': category,
                        'importance': Importance.RELATED
                    })

        # "desporto boxes", which do not necessarily contain only sports news
        boxes = soup.find_all('div', class_='desporto box')
        for box in boxes:
            category = str(box.find(class_='titlebar-title').find(text=True))

            # add box's feature
            feature = box.find(class_='entry').find('a')

            # check for image
            img_elem = box.find('img')
            img_src = None
            if img_elem:
                img_src = img_elem['src']

            all_news.append({
                'article_url': self.cleanup_url(feature['href']),
                'title': extract_title(feature),
                'img_url': img_src,
                'category': category,
                'importance': Importance.LARGE
            })

            # add the others
            others = box.find(class_='newslist').find_all('li')
            for article in others:
                title = article.find('a')
                all_news.append({
                    'article_url': self.cleanup_url(title['href']),
                    'title': extract_title(title),
                    'category': category,
                    'importance': Importance.SMALL
                })

        # latest news box needs an additional ajax request if wanted
        # eg. https://arquivo.pt/noFrame/replay/20100401120844/http://www.publico.clix.pt/Tops/
        # anyway after a while it's there and no ajax anymore
        latest_news = soup.find(class_='maisnoticias box')
        if latest_news:
            for article in latest_news.find_all('li'):
                title_elem = article.find('a')

                title = extract_title(title_elem)
                if ignore_title(title):
                    continue

                all_news.append({
                    'article_url': self.cleanup_url(title_elem['href']),
                    'title': title,
                    'category': 'Outras',
                    'importance': Importance.LATEST
                })

        return all_news

    def cleanup_url(self, url):
        if not url:
            return url

        # some very rare news had the newstitle as the href 20110721150803
        count = 0
        for i in url:
            if i == ' ':
                count += 1
        if count > 2:
            return ''

        find_relative = re.search(r'.*[0-9]{14}[/]*(.*)', url)
        return find_relative.group(1)


class ScraperPublico08(NewsScraper):
    source = 'publico.pt'
    cutoff = 20131112190529  # could work past this, not tested

    all_news = []

    def scrape_page(self, soup):
        articles = soup.find_all('article')
        for article in articles:
            self.get_main_article(article)

        # category sections
        sections = soup.find(class_='content-sections').find('section', class_='primary').find_all(class_='overview-section')
        for section in sections:
            category = clean_special_chars(section.find(class_='module-title').find('a').get_text())

            self.extract_section_feature(section, category)
            self.extract_section_small(section, category)

        all_news = self.all_news
        self.all_news = []
        return all_news

    def get_main_article(self, article):
        if article.find_parent(class_='entries-collection'):
            return

        # ignore articles whose content is a video
        if article.find(attrs={'data-fonte': 'VIDEO_SIMPLES'}):
            return

        header = article.find('header')
        snippet = article.find(class_='entry-summary')
        if snippet:
            snippet = process_snippet(snippet.find('p').find(text=True))
            if snippet is None:
                return

        img = article.find('figure')
        if img:
            img = img.find('img')['src']

        title = extract_title(header.find('h2'))
        if ignore_title(title):
            return

        self.all_news.append({
            'article_url': header.find('a')['href'],
            'title': title,
            'snippet': snippet,
            'img_url': img,
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })

        # find if there are related news articles
        related = article.find(class_='related-entries')
        if related:
            for news in related.find_all('li'):
                self.extracted_related_article(news)

    def extracted_related_article(self, article):
        title = extract_title(article.find('a'))
        if ignore_title(title):
            return

        self.all_news.append({
            'article_url': article.find('a')['href'],
            'title': title,
            'category': 'Outras',
            'importance': Importance.RELATED
        })

    def extract_section_feature(self, section, category):
        feature_box = section.find(class_='section-featured')

        title_elem = feature_box.find('a')
        if not title_elem:
            return

        title = extract_title(feature_box.find(class_='entry-title'))
        if ignore_title(title):
            return

        img = feature_box.find('img')
        if img:
            img = feature_box.find('img')['src']
            if img.endswith('1x1.png'):
                img = None

        article_url = self.cleanup_url(title_elem['href'])

        self.all_news.append({
            'article_url': article_url,
            'title': title,
            'img_url': img,
            'category': category,
            'importance': Importance.LARGE
        })

    def extract_section_small(self, section, category):
        others = section.find(class_='section-headlines').find_all('li')

        for other in others:
            title = extract_title(other.find('a'))
            if ignore_title(title):
                return

            article_url = self.cleanup_url(other.find('a')['href'])

            self.all_news.append({
                'article_url': article_url,
                'title': title,
                'category': category,
                'importance': Importance.SMALL
            })

    def cleanup_url(self, url):
        if not url:
            return url

        # some very rare news had the news title as the href 20110721150803
        count = 0
        for i in url:
            if i == ' ':
                count += 1
        if count > 2:
            return ''

        find_relative = re.search(r'.*[0-9]{14}[/]*(.*)', url)
        return find_relative.group(1)
