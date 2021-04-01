import re

from src.util import prettify_text, is_link_pt, clean_special_chars, ignore_title, remove_clutter, generate_dummy_url

from src.scrapers.news_scraper import NewsScraper, Importance


class ScraperDiarioDeNoticias01(NewsScraper):
    source = 'dn.pt'
    cutoff = 20181021122326

    def scrape_page(self, soup):
        all_news = []

        timestamp = 19960811000000  # this date of the article is in the page, not in the arquivo.pt timestamp
        all_news.append({
            'arquivo_source_url': 'https://arquivo.pt/wayback/19961013220428/http://www.dn.pt:80/tem/tex1tem.htm',  # we sourced this one details by following the link of 19961013220426, turns out it's from previous august instead
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/19961013220428/http://www.dn.pt:80/tem/tex1tem.htm',
            'title': '«Troika» mágica em digressão mundial - Carreras, Placido Domingo E Pavarotti',
            'headline': 'Gargantas de Ouro',
            'snippet': 'Três tenores, uma «tróica mágica» como nunca se vira, uma «joint venture» de gargantas que passa a ser imperioso ver ao vivo numa digressão mundial, que parece desenhar-se como o «caso» do mundo do espectáculo em 1996, mas sem visita ibérica prevista.',
            'img_url': 'https://arquivo.pt/wayback/19961013220502im_/http://www.dn.pt:80/tem/64/4/8.gif',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })

        timestamp = 19961102125336
        all_news.append({
            'timestamp': timestamp,
            'title': 'PSD/Açores sem líder',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/19961102125336mp_/http://www.dn.pt:80/int/tex3int.htm',
            'title': 'Desespero no Zaire',
            'img_url': 'https://arquivo.pt/wayback/19961102130843mp_/http://www.dn.pt:80/home.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })

        timestamp = 19970103153714
        all_news.append({
            'timestamp': timestamp,
            'title': 'Provas globais vão acabar',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Neve isola localidades',
            'img_url': 'https://arquivo.pt/wayback/19970103153855mp_/http://www.dn.pt:80/home.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })

        timestamp = 19970112043908
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/19970112043908mp_/http://www.dn.pt:80/des/tex1des.htm',
            'title': 'Um jogo à moda antiga',
            'category': 'Desporto',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/19970112043908mp_/http://www.dn.pt:80/tem/tex1tem.htm',
            'title': 'Os «jobs» não estão em causa',
            'headline': 'António Reis ao DN',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })

        timestamp = 19970412114053
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/19970412114053mp_/http://www.dn.pt:80/eco/tex9eco.htm',
            'title': 'Governo bloqueia fundos europeus pedidos pela CGTP',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/19970412114053mp_/http://www.dn.pt:80/int/tex1int.htm',
            'title': 'Angolanos anseiam triunfo da paz',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })

        timestamp = 19970613204333
        all_news.append({
            'timestamp': timestamp,
            'title': 'TAP à procura de parceiro para privatização em 1998',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })

        # add deterministic no url flag (deterministic because it's used as key)
        for news in all_news:
            if 'article_url' not in news:
                news['article_url'] = generate_dummy_url(self.source, news['timestamp'], news['category'], news['title'])

        return all_news


class ScraperDiarioDeNoticias02(NewsScraper):
    source = 'dn.pt'
    cutoff = 20181021122326

    def scrape_page(self, soup):
        all_news = []

        links = soup.find_all('a', attrs={'id': re.compile('r-[0-9]-[0-9].*')})
        all_news.append({
            'article_url': url,
            'title': remove_clutter(title),
            'source': source,
            'snippet': prettify_text(snippet),
            'img_url': img_url,
            'category': category,
            'importance': Importance.LARGE
        })
        return all_news
