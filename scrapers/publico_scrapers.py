import re

from util import prettify_text, clean_special

from scrapers.news_scraper import NewsScraper


def ignore_title(title):
    starts = ['Revista de imprensa', 'Destaques d', 'Sorteio', 'Chave do', 'Jackpot', 'Dossier:', 'Fotogaleria',
              'Vídeo:', 'Público lança', 'Consulte as previsões', 'Previsão do tempo', 'Veja o tempo']
    for forbidden in starts:
        if title.startswith(forbidden):
            return True
    return False

# TODO some titles with italic don't show those because it's text inside <i> tags

# TODO adicionar alguns snippets dos anos 90 a mao
class ScraperPublico01(NewsScraper):
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
        head = clean_special(destaque.find_previous(class_='destaqueseccao').get_text())
        snippet = destaque.find_next(class_='destaquecorpo').get_text()

        img_src_relative = destaque.find_next('img')['src']
        img_src = re.search(r'(.*/).*', url.replace('ultimahora.publico', 'www.publico')).group(1) + img_src_relative

        all_news.append({
            'article_url': url,
            'img_url': img_src,
            'headline': head,
            'title': clean_special(destaque.get_text()),
            'snippet': prettify_text(snippet),
            'category': 'Destaque'
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
                'title': clean_special(title.get_text()),
                'category': category
            })

        return all_news


class ScraperPublico02(NewsScraper):
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
        snippet = destaque.find_next(class_=v['destaque_snippet'])

        img_src = self.find_image(destaque['href'], destaque)

        all_news.append({
            'article_url': destaque['href'],
            'img_url': img_src,
            'headline': clean_special(head),
            'title': clean_special(destaque.get_text()),
            'snippet': prettify_text(snippet.get_text()),
            'category': 'Destaque'
        })

        if not destaque['href'].startswith('http'):
            pass

        # segundo destaque
        destaque_2 = snippet.find_next(class_=v['destaque_2_title'])

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

        all_news.append({
            'article_url': destaque_2_title['href'],
            'img_url': img_src,
            'title': clean_special(destaque_2_title.get_text()),
            'snippet': prettify_text(destaque_2_snippet),
            'category': 'Destaque'
        })

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
                'title': clean_special(title.get_text()),
                'category': 'Desporto' if 'desporto.publico.pt' in title['href'] else 'Última hora'
            })

        return all_news

    def find_image(self, example_link, elem):
        while True:
            elem = elem.find_next('img')
            if not elem['src'].endswith('.gif'):
                return re.search(r'(.*/).*', example_link.replace('ultimahora.publico', 'www.publico')).group(1) + elem['src']


class ScraperPublico03(NewsScraper):
    source = 'publico.pt'
    cutoff = 20071118104048

    def scrape_page(self, soup):
        all_news = []

        # destaque
        destaques = soup.find_all(id='caixasNoticias')
        for destaque in destaques:
            head = destaque.find(text=True)
            title = destaque.find(class_='manchete').find('a')
            snippet = destaque.find(class_='textoNews').find(text=True)

            all_news.append({
                'article_url': title['href'],
                'headline': clean_special(head),
                'title': clean_special(title.find('strong').get_text()),
                'snippet': prettify_text(snippet),
                'category': 'Destaque'
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
                title = title_elem.find(text=True)

                # sometimes the news title is "hidden", having no title
                # (aka article probably removed and left an element as ghost)
                if not title:
                    continue

                title = clean_special(title)

                if ignore_title(title):
                    continue

                # news articles can be repeated between destaques and the other sections
                # ignore the second occurence (since destaques has more info)
                if self.has_title(all_news, title):
                    continue

                all_news.append({
                    'article_url': title_elem['href'],
                    'title': title,
                    'category': category
                })

        return all_news

    def has_title(self, news, title):
        for article in news:
            if article['title'] == title:
                return True
        return False

    def ignore_category(self, category_text):
        return category_text in ['Media', 'Media e Tecnologia']


class ScraperPublico04(NewsScraper):
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

            snippet = title.find_next(class_='verdana_11_gray')
            all_news.append({
                'article_url': title['href'],
                'title': title.find(text=True),
                'snippet': snippet.find(text=True),
                'category': 'Destaque'
            })

        # get small news
        seccoes = news_table.find_all(class_='verdana_10_blue')
        for seccao in seccoes:
            title_elem = seccao.find('a')
            title = title_elem.find(text=True)

            if ignore_title(title):
                continue

            category = 'Destaque'
            if title.startswith('Opinião:'):
                category = 'Opinião'

            all_news.append({
                'article_url': title_elem['href'],
                'title': title,
                'category': category
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
                title = article.find(text=True)

                if ignore_title(title):
                    continue

                all_news.append({
                    'article_url': article['href'],
                    'title': title,
                    'category': category
                })

        return all_news

    def ignore_category(self, category_text):
        return category_text in ['Media', 'Media e Tecnologia']


class ScraperPublico05(NewsScraper):
    source = 'publico.pt'
    cutoff = 20121116161647

    def scrape_page(self, soup):
        all_news = []

        # find big feature
        feature = soup.find(class_='feature-big')
        if feature:
            feature_box = feature.find(class_='feature-big-text')
            title = feature_box.find('a')
            snippet = feature_box.find_all('p')[1]

            # check for image
            img_elem = feature.find('img')
            img_src = None
            if img_elem:
                img_src = img_elem['src']

            all_news.append({
                'article_url': self.cleanup_url(title['href']),
                'title': title.find(text=True),
                'snippet': snippet.find(text=True),
                'img_url': img_src,
                'category': 'Destaque'
            })

        # find all articles in the left or middle column ("desporto box" handled separately)
        main_articles = [article for article in soup.find_all('div', class_='entry') if (article.find_parent(id="sec-content") or article.find_parent(id="main-content"))
                         and not article.find_parent(class_="desporto box")
                         and not article.find_parent(id='feature-verao2011')
                         and not article.find_parent(id='feature-911')
                         and not article.find_parent(id='feature-publico-mais')]

        for article in main_articles:
            title_elem = article.find('a')
            snippet = article.find(class_='entry-body').find_all('p')
            if len(snippet) > 1:
                snippet = snippet[1]
            else:
                snippet = snippet[0]

            title = title_elem.find(text=True)
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
                'snippet': snippet.find(text=True),
                'img_url': img_src,
                'category': category
            })

            # some news link to related articles
            related_news = article.find(class_='entry-links')
            if related_news:
                for news in related_news.find_all('a'):
                    # ignore "news" that lead to other sites, found out by having an absolute link instead of relative
                    if news['href'].startswith('https://arquivo.pt') and 'publico.pt/' not in news['href']:
                        continue

                    title = news.find(text=True)
                    if not title or ignore_title(title):
                        continue

                    # check for category
                    category = 'Outras'
                    if 'mundial2010' in article.attrs['class']:
                        category = 'Desporto'

                    all_news.append({
                        'article_url': self.cleanup_url(news['href']),
                        'title': title,
                        'category': category
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
                'title': feature.find(text=True),
                'img_url': img_src,
                'category': category
            })

            # add the others
            others = box.find(class_='newslist').find_all('li')
            for article in others:
                title = article.find('a')
                all_news.append({
                    'article_url': self.cleanup_url(title['href']),
                    'title': title.get_text(),
                    'category': category
                })

        # latest news box needs an additional ajax request if wanted
        # eg. https://arquivo.pt/noFrame/replay/20100401120844/http://www.publico.clix.pt/Tops/
        # anyway after a while it's there and no ajax anymore
        latest_news = soup.find(class_='maisnoticias box')
        if latest_news:
            for article in latest_news.find_all('li'):
                title_elem = article.find('a')

                title = title_elem.find(text=True, recursive=False)
                if ignore_title(title):
                    continue

                all_news.append({
                    'article_url': self.cleanup_url(title_elem['href']),
                    'title': title,
                    'category': 'Outras'
                })

        return self.clean_repeated(all_news)

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

    def clean_repeated(self, news):
        # between two repeats, choose the one with the biggest snippet
        return news


class ScraperPublico06(NewsScraper):
    source = 'publico.pt'
    cutoff = 20131112190529  # could work past this, not tested

    def scrape_page(self, soup):
        all_news = []

        articles = soup.find_all('article')
        for article in articles:
            if article.find_parent(class_='entries-collection'):
                continue

            header = article.find('header')
            snippet = article.find(class_='entry-summary')
            if snippet:
                snippet = snippet.find('p').find(text=True)

            img = article.find('figure')
            if img:
                img = img.find('img')['src']

            all_news.append({
                'article_url': header.find('a')['href'],
                'title': clean_special(str(header.find('h2').get_text())),
                'snippet': prettify_text(snippet or ''),
                'img_url': img,
                'category': 'Destaque'
            })

            related = article.find(class_='related-entries')
            if related:
                for news in related.find_all('li'):
                    all_news.append({
                        'article_url': news.find('a')['href'],
                        'title': clean_special(news.find('a').find(text=True)),
                        'category': 'Outras'
                    })


        # category sections
        sections = soup.find(class_='content-sections').find('section', class_='primary').find_all(class_='overview-section')
        for section in sections:
            category = clean_special(section.find(class_='module-title').find('a').get_text())

            # feature
            feature_box = section.find(class_='section-featured')
            title = feature_box.find('a')
            if title:
                img = feature_box.find('img')
                if img:
                    img = feature_box.find('img')['src']

                all_news.append({
                    'article_url': self.cleanup_url(title['href']),
                    'title': feature_box.find(class_='entry-title').get_text(),
                    'img_url': img,
                    'category': category
                })

            # others
            others = section.find(class_='section-headlines').find_all('li')
            for other in others:
                all_news.append({
                    'article_url': self.cleanup_url(other.find('a')['href']),
                    'title': str(other.find('a').get_text()),
                    'category': category
                })

        return self.clean_repeated(all_news)

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

    def clean_repeated(self, news):
        # between two repeats, choose the one with the biggest snippet
        return news
