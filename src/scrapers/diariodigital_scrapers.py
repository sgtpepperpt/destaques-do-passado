import re

from bs4 import NavigableString

from src.util import generate_dummy_url, get_direct_strings, find_comments, generate_destaques_uniqueness

from src.scrapers.news_scraper import NewsScraper, Importance


def find_with_children(root, elem_name, children_name):
    # gets all elements of a root which have a children of a given type
    return [e for e in root.find_all(elem_name) if e.find(children_name)]


def extract_large_feature(all_news, article_elem):
    img_elem = [e for e in find_with_children(article_elem, 'a', 'img') if e.find('img') and not e.find('img').get('src').endswith('azul.gif')]

    if len(img_elem) > 0:
        img_elem = img_elem[0].find('img')
        title_elem = find_with_children(article_elem, 'a', 'font')[0]

        title = title_elem.get_text(separator=' ')
        url = title_elem.get('href')
    else:
        # version without urls (20010510205351)
        img_elem = article_elem.find('img')
        title_elem = article_elem.find('font', attrs={'size': -1})

        title = title_elem.get_text(separator=' ')
        url = generate_dummy_url('diariodigital.pt', 'diariodigital01', 'Destaques', title)

    snippet_elem = article_elem.find('font', attrs={'size': -2}, recursive=False)

    if url.endswith('diariodigital.sapo.pt/dinheiro_digital/'):
        url += generate_destaques_uniqueness('DestaquesDD', title, snippet_elem)  # generic non-id url at 20031213054017

    all_news.append({
        'article_url': url,
        'title': title,
        'snippet': snippet_elem.get_text(),
        'img_url': img_elem.get('src'),
        'category': 'Destaques',
        'importance': Importance.LARGE
    })


class ScraperDiarioDigital01(NewsScraper):
    source = 'diariodigital.pt'
    cutoff = 20031027120557

    def extract_small_category(self, all_news, bullet_list, category):
        for title_elem in [e.find_next('a') for e in bullet_list]:
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'category': category,
                'importance': Importance.SMALL
            })

    def extract_main_feature(self, all_news, main_feature):
        img_elem = find_with_children(main_feature, 'a', 'img')

        if len(img_elem) > 0:
            img_elem = img_elem[0].find('img')
            title_elem = find_with_children(main_feature, 'a', 'font')[0]

            title = title_elem.get_text(separator=' ')
            url = title_elem.get('href')
        else:
            # version without urls (20010509105317)
            img_elem = main_feature.find('img', recursive=False)
            title_elem = main_feature.find('font', attrs={'size': 6}, recursive=False)

            title = title_elem.get_text(separator=' ')
            url = generate_dummy_url(self.source, 'diariodigital01', 'Destaques', title)

        snippet_elems = [e.get_text(separator=' ') for e in main_feature.find_all('p', recursive=False)]
        snippet = ' '.join(snippet_elems)

        all_news.append({
            'article_url': url,
            'title': title,
            'snippet': snippet,
            'img_url': img_elem.get('src'),
            'category': 'Destaques',
            'importance': Importance.FEATURE
        })

    def scrape_page(self, soup):
        all_news = []

        # LEFT SHORTS
        left_bar = soup.find('table', class_='leftMenu').find_parent('td')
        self.extract_small_category(all_news, left_bar.find_all('img', attrs={'src': re.compile(r'images_site/bullet_desporto\.gif$')}), 'Desporto')
        self.extract_small_category(all_news, left_bar.find_all('img', attrs={'src': re.compile(r'images_site/bullet_dinheiro\.gif$')}), 'Economia')

        # MAIN FEATURED
        comment_marker = find_comments(soup, ' HighLigh HeadLine ')[0]
        main_feature = comment_marker.find_next('td').find('td')

        self.extract_main_feature(all_news, main_feature)

        # RIGHT OF FEATURED SHORTS
        comment_marker = find_comments(soup, 'Main HighLights ')[0]
        small_highlights = comment_marker.find_next('td').find_all('table', recursive=False)
        for article_elem in [e.find('tr').find_all('td')[1] for e in small_highlights]:
            url_elem = article_elem.find('a')

            # sometimes acts like a snippet, sometimes as continuation from the title... seems to fit well being concatenated to title
            text_elem = article_elem.find('font', recursive=False).get_text(separator=' ')
            text = text_elem[0].lower() + text_elem[1:]

            all_news.append({
                'article_url': url_elem.get('href'),
                'title': url_elem.get_text(separator=' ') + ' ' + text,
                'category': 'Destaques',
                'importance': Importance.SMALL
            })

        # REST OF NEWS
        news_boxes = soup.find('td', class_='news').find('p').find_all('table', recursive=False)

        large_features = news_boxes[0].find_all('td', attrs={'background': 'images_site/high2_back.gif'})
        for article_elem in [e.find('table').find('td') for e in large_features]:
            extract_large_feature(all_news, article_elem)

        section_elems = news_boxes[2].find('font', attrs={'size': -1}).find_all('a', recursive=False)
        category = 'Destaques'
        for elem in section_elems:
            if elem.find('img'):
                category = elem.find('img').get('src').split('/')[-1].split('_')[0]
                continue

            all_news.append({
                'article_url': elem.get('href'),
                'title': elem.get_text(separator=' '),
                'category': category,
                'importance': Importance.SMALL
            })

        return all_news


class ScraperDiarioDigital02(NewsScraper):
    source = 'diariodigital.pt'
    cutoff = 20060406110112

    def extract_main_feature(self, all_news, main_feature):
        title_elem = main_feature.find('a', recursive=False)

        inner_elem = main_feature.find('p', recursive=False)
        img_elem = inner_elem.find('img')
        snippet_elem = inner_elem.find('font', recursive=False)

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title_elem.get_text(),
            'snippet': snippet_elem.get_text(),
            'img_url': img_elem.get('src'),
            'category': 'Destaques',
            'importance': Importance.FEATURE
        })

    def scrape_page(self, soup):
        all_news = []

        # main feature at top
        news_box = soup.find('td', attrs={'width': 380, 'bgcolor': '#FFFFFF'}).find('table', recursive=False)
        main_feature = news_box.find('tr', recursive=False).find('td')
        self.extract_main_feature(all_news, main_feature)

        # get large features
        other_boxes = news_box.find('table', recursive=False).find_all('table', recursive=False)
        large_features = other_boxes[0].find_all('td', attrs={'valign': 'top'})
        for article_elem in large_features:
            extract_large_feature(all_news, article_elem)

        # get sections at end
        section_articles = other_boxes[1].find_all('font', attrs={'size': -1})[-1].find_all(re.compile(r'^a|u$'), recursive=False)
        category = 'Destaques'
        for elem in section_articles:
            if elem.find('img'):
                category = elem.find('img').get('src').split('/')[-1].split('_')[-1].replace('.gif', '')
                continue

            title_elem = elem.find('a')

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(separator=' '),
                'category': category,
                'importance': Importance.SMALL
            })

        return all_news


class ScraperDiarioDigital03(NewsScraper):
    source = 'diariodigital.pt'
    cutoff = 20080209065812

    def scrape_page(self, soup):
        all_news = []

        main_features = soup.find_all('td', class_='manchete')
        for article_elem in main_features:
            title_elem = article_elem.find('a', class_='manchete')
            img_elem = article_elem.find('img', class_='imgDestaque')
            snippet = img_elem.contents[0]

            if not snippet:
                raise Exception

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet,
                'img_url': img_elem.get('src'),
                'category': 'Destaques',
                'importance': Importance.FEATURE
            })

            # check for related elems
            if len(img_elem.contents) > 1:
                for title_elem in img_elem.contents[1].find_all('a', recursive=False):
                    all_news.append({
                        'article_url': title_elem.get('href'),
                        'title': title_elem.get_text(),
                        'category': 'Destaques',
                        'importance': Importance.RELATED
                    })

        large_features = soup.find_all('td', class_='subManchetes')
        for article_elem in large_features:
            title_elem = article_elem.find('a', class_='subManchetes')
            img_elem = article_elem.find('img', class_='imgDestaque')

            # get snippet
            snippet = get_direct_strings(img_elem)
            if not snippet:
                # older version
                snippet = ' '.join([e.get_text() for e in img_elem.find_all('br', recursive=False)])

            if not snippet:
                raise Exception

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet,
                'img_url': img_elem.get('src'),
                'category': 'Destaques',
                'importance': Importance.LARGE
            })

        short_articles = soup.find('td', class_='linkDestaques') or soup.find('table', class_='TableDestaques')
        for title_elem in short_articles.find_all('a', class_='linkDestaques'):
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'category': 'Destaques',
                'importance': Importance.SMALL
            })

        sections = soup.find_all('table', class_='linkSeccao') or soup.find_all('td', class_='caixaSeccao')
        for category_section in sections:
            # infer category
            is_left = category_section.find_parent('td').find_next_sibling('td') is not None  # infer left or right cell position
            upper_row = category_section.find_parent('tr').find_previous_sibling('tr')  # go to the row above ours
            category_cell = upper_row.find_all('td', recursive=False)[0 if is_left else 1]  # get the cell which has the category img
            category = category_cell.find('img').get('src').split('_')[-1].replace('.gif', '')

            if category == 'ue1':  # presidencia da ue category (20071023195730)
                category = 'Política'
            elif category == 'eua1':  # us elections (20080209065812)
                category = 'Mundo'

            for title_elem in category_section.find_all('a', class_='linkSeccao'):
                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title_elem.get_text(),
                    'category': category,
                    'importance': Importance.SMALL
                })

        return all_news


class ScraperDiarioDigital04(NewsScraper):
    source = 'diariodigital.pt'
    cutoff = 20120131160244

    def extract_snippet(self, snippet_elem):
        snippet_parts = [e for e in snippet_elem.contents if isinstance(e, NavigableString) or e.name not in ['p']]

        snippet = ''
        for elem in snippet_parts:
            snippet += elem if isinstance(elem, NavigableString) else elem.get_text()
        return snippet

    def scrape_page(self, soup):
        all_news = []

        box_marker = find_comments(soup, ' Coluna Esquerda ')[0]
        main_box_rows = box_marker.find_next_sibling('td').find('table').find_all('tr', recursive=False)

        # get features
        feature_elems = main_box_rows[0].find_all('td', recursive=False)

        ################################################################################################################
        main_feature = feature_elems[0].find('table')
        header_elems = main_feature.find('td', class_='dd_destaque1').find_all('a')

        img_elem = header_elems[0].find('img')
        img_url = img_elem.get('src') if img_elem else None

        title_elem = header_elems[1] if len(header_elems) > 1 else header_elems[0]  # 20100926150217, no photo

        snippet_elem = main_feature.find('td', class_='dd_destaque_texto')
        snippet = self.extract_snippet(snippet_elem)

        if not snippet_elem:
            raise Exception

        all_news.append({
            'article_url': title_elem.get('href') or generate_dummy_url(self.source, 'dd04', snippet, title_elem),  # no url (20100611140106)
            'title': title_elem.get_text(separator=' '),
            'snippet': snippet,
            'img_url': img_url,
            'category': 'Destaques',
            'importance': Importance.FEATURE
        })

        ################################################################################################################
        large_features = feature_elems[4].find_all('td', class_='dd_destaques_mini')

        # each element will give two of these elements, so get only the odd ones
        for i in range(0, len(large_features), 2):
            img_elem = large_features[i].find('img')
            article_elem = large_features[i+1]

            title_elem = article_elem.find('a')
            snippet = get_direct_strings(article_elem)
            if not snippet:
                # different approach if needed, inside a br
                snippet = ' '.join([e.get_text() for e in article_elem.find_all(re.compile(r'^br|p$'))])

            if not snippet:
                raise Exception

            all_news.append({
                'article_url': title_elem.get('href') or generate_dummy_url(self.source, 'dd04', snippet, title_elem),  # no url (20100613140118)
                'title': title_elem.get_text(),
                'snippet': snippet,
                'img_url': img_elem.get('src'),
                'category': 'Destaques',
                'importance': Importance.LARGE
            })

        ################################################################################################################
        # get short articles
        short_article_box = main_box_rows[4].find('td', class_='dd_not3')
        for title_elem in short_article_box.find_all('a', class_='linkDestaques'):
            all_news.append({
                'article_url': title_elem.get('href') or generate_dummy_url(self.source, 'dd04', 'linkDestaques', title_elem),  # no url (20120113160223)
                'title': title_elem.get_text(),
                'category': 'Destaques',
                'importance': Importance.SMALL
            })

        ################################################################################################################
        # get channel articles
        channel_article_box = main_box_rows[4].find('table', class_='dd_not3')
        for box in [e for e in channel_article_box.find_all('tr', recursive=False) if e.find('td', attrs={'valign': 'top'})]:
            category_str = box.find_all('td', recursive=False)[0].find('img').get('src').split('/')[-1].replace('.gif', '')
            category = {
                'din_canais': 'Economia',
                'dis_canais': 'Música'
            }[category_str]

            articles = box.find_all('td', recursive=False)[1]
            for title_elem in articles.find_all('a', recursive=False):
                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title_elem.get_text(),
                    'category': category,
                    'importance': Importance.SMALL
                })

        ################################################################################################################
        # categories should be (and are in HTML) under the td after the comment; beautifulsoup however doesn't show them there
        # therefore kinda hacky way to find them
        sections_box = [e for e in soup.find_all('a') if e.get_text() == 'Mundo'][0].parent.parent.parent.parent.parent.parent
        sections = sections_box.find_all('td', class_='dd_not3')
        for section_elem in sections:
            # infer category
            is_left = section_elem.find_next_sibling('td') is not None  # infer left or right cell position
            upper_row = section_elem.find_parent('tr').find_previous_sibling('tr')  # go to the row above ours
            category_cell = upper_row.find_all('td', attrs={'valign': 'top'}, recursive=False)[0 if is_left else 1]  # get the cell which has the category img
            category = category_cell.find('td', class_='dd_not_title').get_text()

            if category == 'Auto Digital':
                continue  # 20111123160223

            for title_elem in section_elem.find_all('a', recursive=False):
                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': title_elem.get_text(),
                    'category': category,
                    'importance': Importance.SMALL
                })

        return all_news


class ScraperDiarioDigital05(NewsScraper):
    source = 'diariodigital.pt'
    cutoff = 20160703170211

    def extract_channel_news(self, all_news, channel_box, category):
        # large news
        main_article = channel_box.find('h3').find('a')

        img_elem = channel_box.find('div', class_='photo').find('img')
        img_url = img_elem.get('src') if img_elem else None

        all_news.append({
            'article_url': main_article.get('href'),
            'title': main_article.get_text(),
            'img_url': img_url,
            'category': category,
            'importance': Importance.LARGE
        })

        # small news
        article_elems = []
        # get all h4 which aren't headings, didn't manage to ignore it better
        for elem in channel_box.find_all('h4'):
            if not elem.get('class') or 'heading' not in elem.get('class'):
                article_elems.append(elem)

        for title_elem in [e.find('a') for e in article_elems]:
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'category': category,
                'importance': Importance.SMALL
            })

    def scrape_page(self, soup):
        all_news = []

        # nav dropdowns have image articles, very useful
        # curiosity: notced these because of css bork at 20120701150239
        nav_elems = soup.find('div', class_='nav').find('ul').find_all('div', class_='dropdown')
        for article_elem in nav_elems:
            img_elem = article_elem.find('div', class_='photo')
            img_url = img_elem.find('img').get('src') if img_elem else None

            title_elem = article_elem.find('h4').find('a')

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'img_url': img_url,
                'category': 'Destaques',
                'importance': Importance.UNKNOWN
            })

        main_features = soup.find_all('div', class_='manchete')
        for article_elem in main_features:
            img_elem = article_elem.find('div', class_='photo')
            img_url = img_elem.find('img').get('src') if img_elem else None

            inner_elem = article_elem.find('div', class_='info w') or article_elem.find('div', class_='txt')  # the second case seems to be for hidden (20120701150239)
            title_elem = (inner_elem.find('h2') or inner_elem.find('h3') or inner_elem.find('h1')).find('a')
            snippet_elem = inner_elem.find('p')

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet_elem.get_text(),
                'img_url': img_url,
                'category': 'Destaques',
                'importance': Importance.FEATURE
            })

            # get related
            related_elem = article_elem.find('div', class_='noticias_relacionadas')
            if related_elem:
                for title_elem in [e.find('a') for e in related_elem.find_all('li')]:
                    all_news.append({
                        'article_url': title_elem.get('href'),
                        'title': title_elem.get_text(),
                        'category': 'Destaques',
                        'importance': Importance.RELATED
                    })

        large_features = soup.find('div', id='destaques_secundarios').find_all('div', class_='set')
        for article_elem in large_features:
            img_elem = article_elem.find('div', class_='photo')
            img_url = img_elem.find('img').get('src') if img_elem else None

            title_elem = article_elem.find('h3').find('a')

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'img_url': img_url,
                'category': 'Destaques',
                'importance': Importance.LARGE
            })

        latest_news = soup.find('div', class_='popular utl').find('ul').find_all('li')
        for title_elem in [e.find('a') for e in latest_news]:
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'category': 'Destaques',
                'importance': Importance.LATEST
            })

        channel_boxes = soup.find_all('div', id=re.compile(r'^canal_[a-z]*$'))
        if channel_boxes:
            for channel_box in channel_boxes:
                channel = re.match(r'^canal_([a-z]*)$', channel_box.get('id')).group(1)
                if channel in ['auto']:
                    continue

                category = {
                    'dinheiro': 'Economia',
                    'disco': 'Música'
                }[channel]

                self.extract_channel_news(all_news, channel_box, category)
        else:
            channel_boxes = soup.find('div', id='network')
            if channel_boxes:
                channel_boxes = channel_boxes.find_all('div', class_='group')
                for channel_box in channel_boxes:
                    heading = channel_box.find('h4', class_='heading').get_text()

                    if heading in ['Auto Digital']:
                        continue

                    category = {
                        'Dinheiro Digital': 'Economia',
                        'Disco Digital': 'Música'
                    }[heading]

                    self.extract_channel_news(all_news, channel_box, category)
            else:
                # no box, eg 20120701150239
                pass

        category_box = soup.find('div', id='categoria')
        if category_box:  # doesn't exist at 20150810170219
            for category_elem in category_box.find_all('div', class_='politica'):
                category = category_elem.find('h4', class_='heading').get_text()

                # larger element
                main_title = category_elem.find('h4', class_=None).find('a')
                all_news.append({
                    'article_url': main_title.get('href'),
                    'title': main_title.get_text(),
                    'category': category,
                    'importance': Importance.SMALL
                })

                for title_elem in [e.find('a') for e in category_elem.find('ul').find_all('li', class_=None)]:
                    all_news.append({
                        'article_url': title_elem.get('href'),
                        'title': title_elem.get_text(),
                        'category': category,
                        'importance': Importance.SMALL
                    })

        return all_news
