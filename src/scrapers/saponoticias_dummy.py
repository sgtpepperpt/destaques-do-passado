from src.scrapers.news_scraper import NewsScraper, Importance
from src.util import generate_dummy_url


class DummySapoNoticias01(NewsScraper):
    source = 'noticias.sapo.pt'
    cutoff = 19981212020017
    used = False

    # dummy scraper, returns a set of very old news only once
    def scrape_page(self, soup):
        if self.used:
            return None

        self.used = True

        all_news = []

        timestamp = 19981212020017
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/19981212020017mp_/http://noticias.sapo.pt:80/cgi/ngetid?id=http://www.musicnet.forum.pt/noticias.asp%3Fx%3D976',
            'title': 'JIMI HENDRIX ao vivo',
            'source': 'Music.Net',
            'category': 'Entretenimento',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/19981212020017mp_/http://noticias.sapo.pt:80/cgi/ngetid?id=http://www.digito.pt/tecnologia/noticias/tec582.html',
            'title': 'Site de postais processa Microsoft',
            'snippet': 'Um site de postais virtuais processou a Microsoft alegando que o Internet Explorer bloqueia os seus postais.',
            'source': 'Dígito',
            'category': 'Destaque',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/19981212020017mp_/http://noticias.sapo.pt:80/cgi/ngetid?id=http://www.digito.pt/tecnologia/noticias/tec581.html',
            'title': 'Uma carteira no servidor',
            'snippet': 'Uma empresa norte-americana anunciou um serviço que facilita as compras on-line.',
            'source': 'Dígito',
            'category': 'Destaque',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/19981212020017mp_/http://noticias.sapo.pt:80/cgi/ngetid?id=http://www.digito.pt/jogos/noticias/jog121.html',
            'title': 'Demo de Nascar Revolution disponível',
            'snippet': 'A empresa responsável pela série Need for Speed, a Electronic Arts, utilizou a sua experiência em jogos de corrida para criar Nascar Revolution.',
            'source': 'Dígito',
            'category': 'Jogos',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/19981212020017mp_/http://noticias.sapo.pt:80/cgi/ngetid?id=http://www.digito.pt/jogos/noticias/jog120.html',
            'title': 'Luta com tanques em Star Trek!',
            'snippet': 'A Interplay prepara lançamento de Star Trek: New Worlds; um jogo com um certo ambiente de Star Trek, mas onde o jogador não encontra pontes de comando de espaçonaves.',
            'source': 'Dígito',
            'category': 'Jogos',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/19981212020017mp_/http://noticias.sapo.pt:80/cgi/ngetid?id=http://www.musicnet.forum.pt/noticias.asp%3Fx%3D977',
            'title': 'ADN no Porto',
            'snippet': 'Os portuenses ADN apresentam pela primeira vez ao vivo o seu álbum de estreia...',
            'source': 'Music.Net',
            'category': 'Entretenimento',
            'importance': Importance.LARGE
        })
        all_news.append({
            'arquivo_source_url': 'https://arquivo.pt/wayback/19981212020017/http://noticias.sapo.pt:80/',
            'timestamp': 19981205000000,
            'article_url': 'https://arquivo.pt/wayback/19981212020017mp_/http://noticias.sapo.pt:80/cgi/ngetid?id=http://ip.pt/recortes/92/9211.htm',
            'title': 'Revelados planos dum Windows todo feito em Java',
            'snippet': 'Segundo documentos agora revelados, a Microsoft considerou reescrever o Windows por completo em Java.',
            'source': 'Recortes',
            'category': 'Tecnologia',
            'importance': Importance.LARGE
        })
        all_news.append({
            'arquivo_source_url': 'https://arquivo.pt/wayback/19981212020017/http://noticias.sapo.pt:80/',
            'timestamp': 19981205000000,
            'article_url': 'https://arquivo.pt/wayback/19981212020017mp_/http://noticias.sapo.pt:80/cgi/ngetid?id=http://ip.pt/recortes/92/9210.htm',
            'title': '3Com apresenta nova versão do PalmPilot',
            'snippet': 'A 3Com anunciou as características do sucessor do popular PalmPilot.',
            'source': 'Recortes',
            'category': 'Tecnologia',
            'importance': Importance.LARGE
        })
        all_news.append({
            'arquivo_source_url': 'https://arquivo.pt/wayback/19981212020017/http://noticias.sapo.pt:80/',
            'timestamp': 19981205000000,
            'article_url': 'https://arquivo.pt/wayback/19981212020017mp_/http://noticias.sapo.pt:80/cgi/ngetid?id=http://ip.pt/recortes/92/929.htm',
            'title': 'Representantes da Netscape e da Microsoft apupados',
            'snippet': 'Numa sala recheada de webmasters e designers, os representantes da Microsoft e Netscape foram apupados e tiveram que responder a uma série de acusações.',
            'source': 'Recortes',
            'category': 'Tecnologia',
            'importance': Importance.LARGE
        })
        all_news.append({
            'arquivo_source_url': 'https://arquivo.pt/wayback/19981212020017/http://noticias.sapo.pt:80/',
            'timestamp': 19981205000000,
            'article_url': 'https://arquivo.pt/wayback/19981212020017mp_/http://noticias.sapo.pt:80/cgi/ngetid?id=http://ip.pt/recortes/92/924.htm',
            'title': 'Intel copia extra-terrestres?',
            'snippet': 'Segundo afirma um novo livro, uma série de documentos secretos dos Estados Unidos provam que os circuitos impressos e as fibras ópticas são o resultado da investigação da nave alienígena que caíu em Roswell em 1947.',
            'source': 'Recortes',
            'category': 'Destaques',
            'importance': Importance.LARGE
        })

        # add deterministic no url flag (deterministic because it's used as key)
        for news in all_news:
            if 'article_url' not in news:
                news['article_url'] = generate_dummy_url(self.source, news['timestamp'], news['category'], news['title'])

        return all_news
