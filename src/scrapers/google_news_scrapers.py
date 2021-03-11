import re

from src.util import prettify_text, is_link_pt, clean_special, ignore_title

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
            category = clean_special(str(link.find_previous(class_='ks').next))

            # find source name
            source_elem = link.find_next('font', color='#6f6f6f')
            if source_elem.find('b'):
                source = clean_special(source_elem.find('b').get_text())
            else:
                source = clean_special(source_elem.get_text())

            snippet_elem = link.next_sibling.next_sibling.next_sibling.next_sibling
            if snippet_elem.name == 'font':
                snippet = prettify_text(snippet_elem.get_text())

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

            category = clean_special(str(header))

            source = story.find_next('span', class_='source').get_text()
            snippet = story.find_next('div', class_='snippet').get_text()

            news = {
                'article_url': url,
                'title': title,
                'source': source,
                'snippet': prettify_text(snippet),
                'category': category,
                'importance': Importance.LARGE
            }

            all_news.append(news)
        return all_news


class ScraperGoogleNews03(NewsScraper):
    source = 'news.google.pt'
    cutoff = 20131107170219  # we only tested up to here

    def scrape_page(self, soup):
        all_news = []

        stories = soup.find_all('td', class_='esc-layout-article-cell')
        for story in stories:
            url = story.find('h2', class_='esc-lead-article-title').find('a').get('href')
            if not is_link_pt(url):
                # print('ignored ' + link.get('href'))
                continue

            title = story.find('span', class_='titletext').get_text()
            if not title or ignore_title(title):
                continue

            # find news category from parent table
            header = story.find_previous('span', class_='section-name').get_text()
            category = clean_special(str(header))

            source = (story.find_next('span', class_='esc-lead-article-source') or story.find_next('span', class_='al-attribution-source')).get_text()  # handle two different versions
            snippet = story.find_next('div', class_='esc-lead-snippet-wrapper').get_text()

            news = {
                'article_url': url,
                'title': title,
                'source': source,
                'snippet': prettify_text(snippet),
                'category': category,
                'importance': Importance.LARGE
            }

            all_news.append(news)
        return all_news
