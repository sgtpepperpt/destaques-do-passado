import re

from src.util import is_link_pt
from src.text_util import clean_special_chars, ignore_title

from src.scrapers.news_scraper import NewsScraper, Importance


class ScraperGoogleNews01(NewsScraper):
    source = 'news.google.pt'
    cutoff = 20081021122326

    def scrape_page(self, soup):
        all_news = []

        links = soup.find_all('a', attrs={'id': re.compile('r-[0-9]-[0-9].*')})
        for link in links:
            url = link.get('href')
            if not is_link_pt(url):
                # print('ignored ' + link.get('href'))
                continue

            # ignore if there's no bold text (images would fit otherwise)
            title = link.find('b')
            if not title:
                continue

            title = title.get_text()
            if ignore_title(title):
                continue

            # find news category from parent table
            category = clean_special_chars(str(link.find_previous(class_='ks').next))

            # find source name
            source_elem = link.find_next('font', color='#6f6f6f')
            if source_elem.find('b'):
                source = clean_special_chars(source_elem.find('b').get_text())
            else:
                source = clean_special_chars(source_elem.get_text())

            snippet_elem = link.next_sibling.next_sibling.next_sibling.next_sibling
            if snippet_elem.name == 'font':
                snippet = snippet_elem.get_text()
            else:
                snippet = None

            news = {
                'article_url': url,
                'title': title,
                'source': source,
                'snippet': snippet,
                'category': category,
                'importance': Importance.LARGE
            }

            all_news.append(news)
        return all_news


class ScraperGoogleNews02(NewsScraper):
    source = 'news.google.pt'
    cutoff = 20111102160207

    def scrape_page(self, soup):
        all_news = []

        stories = soup.find_all('div', class_='headline-story')
        for story in stories:
            url = story.find('h2', class_='title').find('a').get('href')
            if not is_link_pt(url):
                # print('ignored ' + link.get('href'))
                continue

            title = story.find('h2', class_='title').find('a').get_text()
            if not title or ignore_title(title):
                continue

            # find news category from parent table, two different versions on same layout
            try_header_v1 = story.find_previous('div', class_='section-title') or story.find_previous('td', id='edition-picker-wrapper')
            try_header_v2 = story.find_previous('div', class_='basic-title').find('h2', class_='text')
            if try_header_v1:
                header = try_header_v1.get_text()
            elif try_header_v2:
                sub_category = try_header_v2.find_all('a')
                if sub_category:
                    header = sub_category[-1].get_text()
                else:
                    header = try_header_v2.find('span', class_='title').get_text()

            category = clean_special_chars(str(header))

            source = story.find_next('span', class_='source').get_text()
            snippet = story.find_next('div', class_='snippet').get_text()

            news = {
                'article_url': url,
                'title': title,
                'source': source,
                'snippet': snippet,
                'category': category,
                'importance': Importance.LARGE
            }

            all_news.append(news)
        return all_news


class ScraperGoogleNews03(NewsScraper):
    source = 'news.google.pt'
    cutoff = 20160801170210  # could work after this, haven't tested

    def scrape_page(self, soup):
        all_news = []

        stories = soup.find_all('table', class_='esc-layout-table')
        for story in stories:
            url = story.find('h2', class_='esc-lead-article-title').find('a').get('href')
            if not is_link_pt(url):
                continue  # avoid brazilian sources

            title = story.find('span', class_='titletext').get_text()
            if not title or ignore_title(title):
                continue

            # find news category from parent table
            header = story.find_previous('span', class_='section-name').get_text()
            category = clean_special_chars(str(header))

            source = (story.find_next('span', class_='esc-lead-article-source') or story.find_next('span', class_='al-attribution-source')).get_text()  # handle two different versions
            snippet = story.find_next('div', class_='esc-lead-snippet-wrapper').get_text()

            img_elem = story.find('img', class_='esc-thumbnail-image')
            img_url = (img_elem.get('src') or img_elem.get('imgsrc')) if img_elem else None

            all_news.append({
                'article_url': url,
                'title': title,
                'source': source,
                'snippet': snippet,
                'img_url': img_url,
                'category': category,
                'importance': Importance.LARGE
            })

            # related is basically the same news rewritten...
            # # RELATED ARTICLES
            # related_articles = story.find_all('div', class_='esc-secondary-article-title-wrapper')
            # for article in related_articles:
            #     url = article.find('a').get('href')
            #     title = article.find('span', class_='titletext').get_text()
            #     source = article.find('label', class_='esc-secondary-article-source').get_text()
            #
            #     all_news.append({
            #         'article_url': url,
            #         'title': title,
            #         'source': source,
            #         'category': category,
            #         'importance': Importance.RELATED
            #     })
            #
            # # MORE RELATED
            # diversity_articles = story.find_all('div', class_='esc-diversity-article-wrapper')
            # for article in diversity_articles:
            #     url = article.find('a').get('href')
            #     title = article.find('span', class_='titletext').get_text()
            #     source = article.find('label', class_='esc-diversity-article-source').get_text()
            #
            #     all_news.append({
            #         'article_url': url,
            #         'title': title,
            #         'source': source,
            #         'category': category,
            #         'importance': Importance.RELATED
            #     })

        # LATEST NEWS
        latest_elem = soup.find('div', id='s_BREAKING_NEWS_BOX')
        if latest_elem:
            self.scrape_side_news(all_news, latest_elem, Importance.LATEST)

        # POPULAR NEWS
        popular_elem = soup.find('div', id='s_POPULAR') or soup.find('div', id='s_MOST_POPULAR')
        if popular_elem:
            self.scrape_side_news(all_news, popular_elem, Importance.SMALL)

        return all_news

    def scrape_side_news(self, all_news, elem, importance):
        for story in elem.find_all('div', class_='story'):
            url = story.find('a').get('href')

            if not is_link_pt(url):
                continue  # avoid brazilian sources

            title = story.find('span', class_='titletext').get_text()
            source = story.find('div', class_='source').find('span', class_='source-pref').get_text()

            all_news.append({
                'article_url': url,
                'title': title,
                'source': source,
                'category': 'Outras',
                'importance': importance
            })
