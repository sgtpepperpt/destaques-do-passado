import re

from bs4 import NavigableString, Comment

from src.util import generate_dummy_url, find_comments
from src.text_util import remove_clutter, clean_special_chars, prettify_text

from src.scrapers.news_scraper import NewsScraper, Importance


class ScraperDiarioDeNoticias01(NewsScraper):
    source = 'dn.pt'
    cutoff = 19970613204333

    used = False

    def scrape_page(self, soup):
        if self.used:
            return None

        self.used = True

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


def get_direct_strings(elem):
    return remove_clutter(' '.join([e for e in elem.contents if isinstance(e, NavigableString) and not isinstance(e, Comment)]))


class ScraperDiarioDeNoticias02(NewsScraper):
    source = 'dn.pt'
    cutoff = 20010801153425

    def scrape_page(self, soup):
        all_news = []

        title_elems = soup.find_all('font', attrs={'color': '#8c0000'})
        for article_elem in [e.find_parent('table') for e in title_elems]:
            # elements are all inside the previous
            pretitle_elem = article_elem.find('font', attrs={'color': '#000000', 'size': 1})
            pretitle = get_direct_strings(pretitle_elem)

            title_elem = (pretitle_elem or article_elem).find('font', attrs={'color': '#8c0000'})
            title = remove_clutter(title_elem.find_all('b')[0].get_text())

            if not title:
                continue  # missing title at 19991010052929

            snippet_elem = title_elem.find('font', attrs={'size': 3})
            snippet = get_direct_strings(snippet_elem)

            if snippet and ('Reportagem no' in snippet or 'Crónica de' in snippet):
                continue  # stuff that isn't archived then

            url_elem = [e.find_parent('a') for e in snippet_elem.find_all('img') if e.get('src').endswith('.gif')]
            url = url_elem[0].get('href') if len(url_elem) > 0 else generate_dummy_url(self.source, 'parser02', pretitle, title)

            img_elem = [e.get('src') for e in article_elem.find_all('img') if e.get('src').endswith('.jpg')]
            img_url = img_elem[0] if len(img_elem) > 0 else None

            all_news.append({
                'article_url': url,
                'headline': pretitle if len(pretitle) > 0 else None,
                'title': title,
                'snippet': prettify_text(snippet),
                'img_url': img_url,
                'category': 'Destaque',
                'importance': Importance.FEATURE if img_url else Importance.LARGE if snippet else Importance.SMALL
            })

        return all_news


class ScraperDiarioDeNoticias03(NewsScraper):
    source = 'dn.pt'
    cutoff = 20011001001039

    used = False

    def scrape_page(self, soup):
        if self.used:
            return None
        self.used = True

        all_news = []

        timestamp = 20010912000443  # changed to 12 to match the page's date
        all_news.append({
            'timestamp': timestamp,
            'arquivo_source_url': 'https://arquivo.pt/wayback/20010913000443/http://www.dn.pt:80/pri/sintpri.htm',
            'article_url': 'https://arquivo.pt/wayback/20010913000443mp_/http://www.dn.pt:80/eua/texto1.htm',
            'title': 'Portugueses desaparecidos nos EUA; FBI prende suspeitos em Boston; Investigações sobre atentados avançam rapidamente',
            'snippet': 'O cônsul de Portugal em Nova Iorque disse à SIC que há 60 portugueses com paradeiro incerto, na sequência do atentado ao World Trade Center, embora, até ao momento só haja um desaparecido confirmado: um empregado de um restaurante. Dezenas de pessoas têm procurado o consulado em Nova Iorque e a embaixada em Washington, à procura de informações de familiares ou amigos.',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'arquivo_source_url': 'https://arquivo.pt/wayback/20010913000443/http://www.dn.pt:80/pri/sintpri.htm',
            'article_url': 'https://arquivo.pt/wayback/20010913000443mp_/http://www.dn.pt:80/int/12p4a.htm',
            'title': 'Ataque aos EUA (11-09-2001)',
            'snippet': 'Atentados suicidas destroem as duas torres do World Trade Center em Nova Iorque e atingem o Pentágono em Washington. Terroristas desviaram aviões comerciais e provocaram um número indeterminado de vítimas. Reportagem nos EUA, crónicas das principais capitais mundiais e opiniões de especialistas em estratégia. Perfil dos principais suspeitos, a memória das ficções e a história dos edifícios emblemáticos',
            'img_url': 'https://arquivo.pt/wayback/20010913000505im_/http://www.dn.pt:80/pri/pri1.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })

        timestamp = 20010913051725
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010913051725mp_/http://www.dn.pt:80/int/13p56d.htm',
            'title': 'Contra-ataque global',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'snippet': 'ALIANÇA AVANÇA - A NATO está pronta a reagir. Basta provar que o atentado veio do exterior para a Aliança declarar guerra',
            'img_url': 'https://arquivo.pt/wayback/20010913051907im_/http://www.dn.pt:80/pri/pri1.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010913051725mp_/http://www.dn.pt:80/int/13p4a.htm',
            'title': 'FBI identificou terroristas',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'snippet': 'Pilotos suicidas treinados nos EUA. Presos dois suspeitos',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010913051725mp_/http://www.dn.pt:80/int/13p56a.htm',
            'title': '60 portugueses desaparecidos. Consulado divulgou lista e apela a comunicação',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010913051725mp_/http://www.dn.pt:80/int/13p6a.htm',
            'title': 'Horas de angústia em Nova Iorque e Washington. Milhares de pessoas tentam salvar vidas entre destroços',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })

        timestamp = 20010914195828
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010914195828mp_/http://www.dn.pt:80/int/14p7a.htm',
            'title': 'Caça ao homem',
            'snippet': 'Sete mil agentes passam os EUA a pente fino, procurando os 50 terroristas envolvidos nos atentados de terça-feira',
            'headline': 'Ataque aos EUA',
            'img_url': 'https://arquivo.pt/wayback/20010914195832im_/http://www.dn.pt:80/pri/pri1.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010914195828mp_/http://www.dn.pt:80/int/14p7c.htm',
            'title': 'Árabes sob suspeita em Portugal, Alemanha e Itália',
            'headline': 'Ataque aos EUA',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010914195828mp_/http://www.dn.pt:80/int/14p12c.htm',
            'title': 'Três minutos de silêncio hoje às 11 horas',
            'headline': 'Ataque aos EUA',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })

        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010914195828mp_/http://www.dn.pt:80/ige/14p21a.htm',
            'title': 'Pedrito desafiou a lei com uma estocada na Moita',
            'headline': 'Touro de Morte',
            'img_url': 'https://arquivo.pt/wayback/20010914195836im_/http://www.dn.pt:80/pri/pri2.jpg',
            'category': 'Sociedade',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010914195828mp_/http://www.dn.pt:80/tvr/14p60c.htm',
            'title': 'Informação dificulta acordo entre RTP e ex-director da SIC',
            'headline': 'Emídio Rangel',
            'img_url': 'https://arquivo.pt/wayback/20010914195838im_/http://www.dn.pt:80/pri/pri3.jpg',
            'category': 'Portugal',
            'importance': Importance.FEATURE
        })

        timestamp = 20010915030849
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010915030849mp_/http://www.dn.pt:80/int/15p4a.htm',
            'title': 'Mobilização geral',
            'snippet': 'O Presidente George Bush, que ontem proclamou a existência de uma situação de "emergência nacional", decidiu, com base nos poderes que lhe foram conferidos pelo Senado, convocar 50 mil reservistas das forças armadas. Por outro lado, o Congresso deu pelos poderes ao presidente norte-americano para perseguir os autores do atentado, através da criação de instrumentos jurídicos de combate ao terrorismo',
            'headline': 'EUA reagem ao ataque',
            'img_url': 'https://arquivo.pt/wayback/20010915030931im_/http://www.dn.pt:80/pri/pri1.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010915030849mp_/http://www.dn.pt:80/int/15p7a.htm',
            'title': 'FBI suspeita de "toupeira" na Casa Branca',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010915030849mp_/http://www.dn.pt:80/int/15p9a.htm',
            'title': 'Confirmada a morte de cinco portugueses',
            'headline': 'Vítimas do atentado ao World Trade Center',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010915030849mp_/http://www.dn.pt:80/des/15p34a.htm',
            'title': 'Benfica-F.C.Porto',
            'snippet': 'Esperadas 80 mil pessoas no Estádio da Luz para assistirem ao clássico',
            'img_url': 'https://arquivo.pt/wayback/20010915030946im_/http://www.dn.pt:80/pri/pri2.jpg',
            'category': 'Desporto',
            'importance': Importance.FEATURE
        })

        timestamp = 20010916024629
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010916024629mp_/http://www.dn.pt:80/int/16p6a.htm',
            'title': 'Ordem para atacar',
            'headline': 'Estados Unidos',
            'snippet': '"Estamos em guerra", disse ontem aos americanos o Presidente George W. Bush, avisando-os de que terão que fazer sacrifícios "porque o conflito não vai ser fácil", mas que vai ser dada caça aos terroristas, "fumigando os seus buracos para os tirar de lá" e trazê-los perante a justiça. Ao mesmo tempo, pediu aos americanos que regressem ao trabalho e à normalidade possível já a partir de amanhã',
            'img_url': 'https://arquivo.pt/wayback/20010916024652im_/http://www.dn.pt:80/pri/pri1.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010916024629mp_/http://www.dn.pt:80/int/16p12a.htm',
            'headline': 'New York - New York',
            'title': 'A memória dos escritores',
            'snippet': 'Arte, música, filmes e livros. A boa vida na grande cidade. Entrevista com Nuno Portas',
            'img_url': 'https://arquivo.pt/wayback/20010916024659im_/http://www.dn.pt:80/pri/pri2.jpg',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010916024629mp_/http://www.dn.pt:80/des/16p32a.htm',
            'headline': 'Golfe',
            'title': 'Inglaterra vai assistir ao duelo de vedetas',
            'img_url': 'https://arquivo.pt/wayback/20010916024727im_/http://www.dn.pt:80/pri/pri3.jpg',
            'category': 'Desporto',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010916024629mp_/http://www.dn.pt:80/ige/16p24a.htm',
            'title': 'Portugueses tentam salvar miúdos de rua no México',
            'category': 'Sociedade',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010916024629mp_/http://www.dn.pt:80/des/16p34a.htm',
            'title': ' Benfica e FC Porto na Luz dão espectáculo sem golos',
            'img_url': 'https://arquivo.pt/wayback/20010916024740im_/http://www.dn.pt:80/pri/pri4.jpg',
            'category': 'Desporto',
            'importance': Importance.SMALL
        })

        timestamp = 20010917125139
        all_news.append({
            'timestamp': timestamp,
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Funeral de Massud',
            'snippet': 'Milhares de afegãs assistiram ontem ao funeral do ex-lider da Aliança do Norte, movimento que se opõe ao regime talibã e que está ao lado dos EUA no combate ao regime de Cabul',
            'img_url': 'https://arquivo.pt/wayback/20010917125143im_/http://www.dn.pt:80/pri/pri1.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010917125139mp_/http://www.dn.pt:80/int/17p4a.htm',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Paquistão dá três dias a Cabul para entregar Ben Laden. Enviados dos EUA partem para o Paquistão',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010917125139mp_/http://www.dn.pt:80/int/17p10a.htm',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Israel cria zona-tampão na Cisjordânia',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010917125139mp_/http://www.dn.pt:80/int/17p11a.htm',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Entrevista com líder da Fatah',
            'category': 'Mundo',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010917125139mp_/http://www.dn.pt:80/int/17p12a.htm',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Autoridades de Macau prenderam seis paquistaneses suspeitos de preparar novos atentados',
            'category': 'Mundo',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010917125139mp_/http://www.dn.pt:80/int/17p14a.htm',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Pedaços de corpos nos destroços do World Trade Center',
            'category': 'Mundo',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010917125139mp_/http://www.dn.pt:80/int/17p14b.htm',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Um português morto e 35 desaparecidos',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010917125139mp_/http://www.dn.pt:80/int/17p56a.htm',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Bolsa de Nova Iorque reabre hoje',
            'category': 'Mundo',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010917125139mp_/http://www.dn.pt:80/int/17p5a.htm',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Reportagem dos enviados especiais Oscar Mascarenhas (texto) e Rui Coutinho (fotos)',
            'category': 'Mundo',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010917125139mp_/http://www.dn.pt:80/art/17p40a.htm',
            'headline': 'José Régio',
            'title': 'Autor de "Poemas de Deus e do Diabo" nasceu há cem anos',
            'img_url': 'https://arquivo.pt/wayback/20010917125149im_/http://www.dn.pt:80/pri/pri2.jpg',
            'category': 'Cultura',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010917125139mp_/http://www.dn.pt:80/neg/int/17s4a.htm',
            'title': 'Ataque aos EUA baralha previsões económicas',
            'img_url': 'https://arquivo.pt/wayback/20010917125150im_/http://www.dn.pt:80/pri/pri3.jpg',
            'category': 'Economia',
            'importance': Importance.FEATURE
        })

        timestamp = 20010918045243
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010918045243mp_/http://www.dn.pt:80/int/18p4a.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Morto ou vivo',
            'snippet': 'Bush reafirma que o primeiro objectivo é Ben Laden. Líderes religiosos do Afeganistão decidem hoje destino do suspeito número um',
            'img_url': 'https://arquivo.pt/wayback/20010918045305im_/http://www.dn.pt:80/pri/pri1.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010918045243mp_/http://www.dn.pt:80/int/18p13a.htm',
            'headline': 'Ataque aos EUA',
            'title': '49 suspeitos detidos nos EUA',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010918045243mp_/http://www.dn.pt:80/int/18p18a.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Wall Street reabriu em queda',
            'category': 'Economia',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010918045243mp_/http://www.dn.pt:80/int/18p19b.htm',
            'headline': 'Ataque aos EUA',
            'title': 'EUA e Europa baixaram as taxas de juro',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010918045243mp_/http://www.dn.pt:80/des/18p31a.htm',
            'headline': 'Liga dos Campeões',
            'title': 'FC Porto joga hoje na Noruega com o Rosenborg',
            'img_url': 'https://arquivo.pt/wayback/20010918045307im_/http://www.dn.pt:80/pri/pri2.jpg',
            'category': 'Desporto',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010918045243mp_/http://www.dn.pt:80/eco/18p35a.htm',
            'headline': 'Orçamento',
            'title': 'Governo não garante défice de 1,1% em 2001',
            'img_url': 'https://arquivo.pt/wayback/20010918045309im_/http://www.dn.pt:80/pri/pri3.jpg',
            'category': 'Portugal',
            'importance': Importance.LARGE
        })

        timestamp = 20010919040435
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010919040435mp_/http://www.dn.pt:80/int/19p4a.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Talibãs resistem',
            'snippet': 'Cabul recusa entregar Ben Laden e prepara-se para a guerra',
            'img_url': 'https://arquivo.pt/wayback/20010919040444im_/http://www.dn.pt:80/pri/pri1.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010919040435mp_/http://www.dn.pt:80/int/19p4b.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Afegãos procuram fugir e Paquistão fechou fronteiras',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010919040435mp_/http://www.dn.pt:80/int/19p8b.htm',
            'headline': 'Ataque aos EUA',
            'title': 'NATO aconselha prudência e teme que EUA avancem sozinhos',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010919040435mp_/http://www.dn.pt:80/int/19p8a.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Aumenta a pressão interna para Bush dar ordem de ataque',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010919040435mp_/http://www.dn.pt:80/int/19p10b.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Plano terrorista envolvia mais de quatro aviões',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010919040435mp_/http://www.dn.pt:80/int/19p15b.htm',
            'headline': 'Ataque aos EUA',
            'title': 'A rede de terror e financeira de Ben Laden e os milhões que terá ganho com o ataque. Companhias aéreas e turismo em crise',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010919040435mp_/http://www.dn.pt:80/des/19p30a.htm',
            'headline': 'Liga Milionária',
            'title': 'FC Porto venceu noruegueses do Rosenborg por 2-1',
            'img_url': 'https://arquivo.pt/wayback/20010919015901im_/http://www.dn.pt:80/pri/pri2.jpg',
            'category': 'Desporto',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010919040435mp_/http://www.dn.pt:80/ige/19p22y.htm',
            'headline': 'Financiamento',
            'title': 'Universidades com má nota serão castigadas',
            'category': 'Educação',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010919040435mp_/http://www.dn.pt:80/eco/19p35a.htm',
            'headline': 'Balanço',
            'title': 'Governo admite aumento de 30 mil na função pública',
            'category': 'Portugal',
            'importance': Importance.LARGE
        })

        timestamp = 20010920045715
        all_news.append({
            'timestamp': timestamp,
            'headline': 'Ataque aos EUA',
            'title': 'Revolta no Paquistão',
            'snippet': 'Mulheres activistas de um dos principais partidos religiosos paquistaneses manifestaram-se ontem em Lahore contra os norte-americanos',
            'img_url': 'https://arquivo.pt/wayback/20010920045727im_/http://www.dn.pt:80/pri/pri1.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010920045715mp_/http://www.dn.pt:80/int/20p11a.htm',
            'headline': 'Ataque aos EUA',
            'title': ' Barril de pólvora',
            'snippet': 'EUA iniciaram operação "Justiça Infinita" com o envio de mais de cem aviões de combate para o Golfo Pérsico. Bush faz novo aviso a Cabul',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010920045715mp_/http://www.dn.pt:80/int/20p4a.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Coligação contra o terrorismo ameaça desestabilizar Paquistão. Reportagem de Luís Naves em Islamabad',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010920045715mp_/http://www.dn.pt:80/int/20p4b.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Talibãs preparam-se para a guerra',
            'category': 'Mundo',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010920045715mp_/http://www.dn.pt:80/int/20p8b.htm',
            'headline': 'Ataque aos EUA',
            'title': 'FBI segue pista do dinheiro',
            'category': 'Mundo',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010920045715mp_/http://www.dn.pt:80/int/20p12c.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Pacheco Pereira está envergonhado com Guterres',
            'category': 'Portugal',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010920045715mp_/http://www.dn.pt:80/des/20p31a.htm',
            'headline': 'Liga Milionária',
            'title': 'Boavista vence Dinamo de Kiev no Bessa',
            'img_url': 'https://arquivo.pt/wayback/20010920045752im_/http://www.dn.pt:80/pri/pri2.jpg',
            'category': 'Desporto',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010920045715mp_/http://www.dn.pt:80/int/20p23a.htm',
            'headline': 'Gescartera',
            'title': 'Escândalo provoca demissão na CNMV e prisão de gestora',
            'category': 'Destaque',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010920045715mp_/http://www.dn.pt:80/net/20p51a.htm',
            'headline': 'MBNET',
            'title': 'Multibanco tem novo sistema de pagamento "online"',
            'category': 'Destaque',
            'importance': Importance.LARGE
        })


        timestamp = 20010921041703
        all_news.append({
            'timestamp': timestamp,
            'headline': 'Ataque aos EUA',
            'title': 'Tropas no golfo',
            'snippet': 'Militares ingleses começaram a chegar ontem ao aeroporto militar de Omã para participarem num exercício que coincide com o início da operação "Justiça Infinita" desencadeada pelos EUA',
            'img_url': 'https://arquivo.pt/wayback/20010921042007im_/http://www.dn.pt:80/pri/pri1.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })

        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010921041703mp_/http://www.dn.pt:80/int/21p8a.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Até à vitória',
            'snippet': 'Guerra pode durar cinco anos. "Águia Nobre" é a outra face da luta contra o terror',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010921041703mp_/http://www.dn.pt:80/int/21p9a.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Tropas terrestres avançam para o Golfo Pérsico',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010921041703mp_/http://www.dn.pt:80/int/21p56a.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Presidente Bush pediu no Congresso "prontidão" aos militares e calma aos americanos',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010921041703mp_/http://www.dn.pt:80/int/21p8b.htm',
            'headline': 'Ataque aos EUA',
            'title': 'NATO confirma agressão externa aos EUA',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010921041703mp_/http://www.dn.pt:80/int/21p4b.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Religiosos afegãos convidam Ben Laden a sair do país. EUA rejeitam',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010921041703mp_/http://www.dn.pt:80/int/21p12a.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Mais suspeitos presos nos EUA e no Iémen',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010921041703mp_/http://www.dn.pt:80/int/21p10b.htm',
            'headline': 'Ataque aos EUA',
            'title': 'UE aprova pacote antiterrorista',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010921041703mp_/http://www.dn.pt:80/int/21p10a.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Conselho Europeu reúne hoje em Bruxelas',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010921041703mp_/http://www.dn.pt:80/int/21p11a.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Portugal autoriza uso das Lajes e do espaço aéreo',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010921041703mp_/http://www.dn.pt:80/des/21p30a.htm',
            'headline': 'Taça UEFA',
            'title': 'Sporting vence por 3-0 na Dinamarca',
            'img_url': 'https://arquivo.pt/wayback/20010921042245im_/http://www.dn.pt:80/pri/pri2.jpg',
            'category': 'Desporto',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010921041703mp_/http://www.dn.pt:80/art/21p40a.htm',
            'headline': '"Vou para casa"',
            'title': 'Manoel de Oliveira estreia filme que levou a Cannes',
            'category': 'Cultura',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010921041703mp_/http://www.dn.pt:80/tvr/21p52a.htm',
            'headline': 'RTP',
            'title': 'Emídio Rangel promete uma TV para o público',
            'category': 'Portugal',
            'importance': Importance.LARGE
        })

        timestamp = 20010923090240
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010923090240mp_/http://www.dn.pt:80/int/23p6a.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Decisão crítica',
            'snippet': 'George W. Bush decide o ataque, este fim-de-semana, em videoconferência, com os seus colabortadores e os aliados',
            'img_url': 'https://arquivo.pt/wayback/20010923090941im_/http://www.dn.pt:80/pri/pri1.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010923090240mp_/http://www.dn.pt:80/int/23p11a.htm',
            'headline': 'Ataque aos EUA',
            'title': ' Islão, esse desconhecido',
            'snippet': 'Existem 1,3 mil milhões de muçulmanos no mundo. Têm principios comuns mas diferentes maneiras de os viver. Coexistem connosco mas não os conhecemos realmente. DN levanta um pouco do véu que os encobre. Portuguesas oançam um olhar sobre as mulheres no mundo islâmico. Embaixadora do Paquistão sublinha: O islão é tão machista como qualquer outra religião."',
            'category': 'Sociedade',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010923090240mp_/http://www.dn.pt:80/pna/23p23e.htm',
            'title': 'Soares escreve sobre Gustavo Soromenho',
            'snippet': 'A sua vida atravessou o século XX português e confunde-se com a resistência ao Estado Novo de Salazar e Caetano. Ontem, aos 93 anos, faleceu na sua casa no Bairro Alto o advogado, fundador do MUD e do PS Gustavo Soromenho. "Nunca fui ambicioso. Sou discreto", disse de si mesmo em entrevista ao Expresso em 1997. "Sempre disse que quando chegasse o reviralho não queria ser nem deputado nem ministro. Não gosto da política, da intriga política, dos conluios políticos. Gosto da política como eu a faço, luto por princípios".',
            'category': 'Política',
            'importance': Importance.FEATURE
        })

        timestamp = 20010924123609
        all_news.append({
            'timestamp': timestamp,
            'headline': 'Ataque aos EUA',
            'title': 'Já começou',
            'snippet': 'Forças da Aliança do Norte, opositoras dos talibãs, atacaram posições do regime de Cabul e provocaram cerca de 60 mortos. No terreno já estão também comandos da Grã-Bretanha',
            'img_url': 'https://arquivo.pt/wayback/20010924123657im_/http://www.dn.pt:80/pri/pri1.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010924123609mp_/http://www.dn.pt:80/int/24p6c.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Comandos ao ataque',
            'snippet': 'Um grupo de intervenção das SAS britânicas já entrou ontem em confronto com soldados talibãs perto de Cabul (reportagem dos nossos enviados e correspondentes: Luís Naves, no Paquistão; Oscar Mascarenhas, Manuel Ricardo Ferreira e Rui Coutinho, nos EUA; Paula Caçador, em Atenas; Eduardo Hélder, em Berlim)',
            'img_url': 'https://arquivo.pt/wayback/20010924123657im_/http://www.dn.pt:80/pri/pri1.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010924123609mp_/http://www.dn.pt:80/int/24p6b.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Avião espião americano desapareceu no Afeganistão',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010924123609mp_/http://www.dn.pt:80/int/24p6a.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Cabul afirma que suspeito número um está "desaparecido". Casa Branca não acredita e mantém ordem de guerra',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010924123609mp_/http://www.dn.pt:80/int/24p11b.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Ben Laden treinou 11 mil terroristas nas bases afegãs',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010924123609mp_/http://www.dn.pt:80/int/24p11a.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Serviços secretos americanos temem nova vaga de atentados com armas químicas e biológicas',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010924123609mp_/http://www.dn.pt:80/int/24p12a.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Em Israel, Shimon Peres ameaça demitir-se depois do veto de Sharon ao seu encontro com Arafat',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010924123609mp_/http://www.dn.pt:80/pna/24p96a.htm',
            'headline': 'Moeda única',
            'title': 'Faltam 100 dias para o euro',
            'snippet': 'DN inicia hoje a publicação diária de páginas especiais com informação útil sobre a nova moeda europeia',
            'category': 'Destaque',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010924123609mp_/http://www.dn.pt:80/neg/pna/24s3a.htm',
            'title': 'Segurança Social pode falir em 2011',
            'category': 'Destaque',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010924123609mp_/http://www.dn.pt:80/des/24p41a.htm',
            'headline': 'Futebol - I Liga',
            'title': 'Sporting ganha',
            'category': 'Desporto',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010924123609mp_/http://www.dn.pt:80/des/24p40a.htm',
            'headline': 'Futebol - I Liga',
            'title': 'Benfica empata',
            'category': 'Desporto',
            'importance': Importance.LARGE
        })

        timestamp = 20010925102926
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010925102926mp_/http://www.dn.pt:80/int/25p8a.htm',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Na pista do dinheiro',
            'snippet': 'Bush congela bens nos EUA de 27 organizações suspeitas de ligações ao terrorismo',
            'img_url': 'https://arquivo.pt/wayback/20010925103120im_/http://www.dn.pt:80/pri/pri1.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010925102926mp_/http://www.dn.pt:80/int/25p6a.htm',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Rússia abre corredores aéreos aos americanos. Ásia central ex-soviética pode ser base de ataque',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010925102926mp_/http://www.dn.pt:80/int/25p4a.htm',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Regime de Cabul prepara-se para a guerra. Oposição afegã conquista posições aos talibãs. Ben Laden apela à guerra santa',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010925102926mp_/http://www.dn.pt:80/pna/25p14a.htm',
            'headline': 'Euro',
            'title': 'Comissão Europeia trava bancos',
            'snippet': 'Bruxelas quer fixar valores das taxas',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })

        timestamp = 20010926105159
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010926105159mp_/http://www.dn.pt:80/int/26p4a.htm',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Terroristas em fuga',
            'snippet': 'Combatentes árabes leais à milícia dos talibãs deixaram as suas bases no Leste do Afeganistão prevendo um ataque americano, revelaram, ontem, testemunhas chegadas ao Paquistão (Reportagem de Luís Naves no Paquistão e Manuel Ricardo Ferreira em Nova Iorque)',
            'img_url': 'https://arquivo.pt/wayback/20010926105320im_/http://www.dn.pt:80/pri/pri1.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010926105159mp_/http://www.dn.pt:80/int/26p6a.htm',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Bush apela à sublevação dos afegãos. Mullah Omar justifica atentados ao povo americano',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010926105159mp_/http://www.dn.pt:80/int/26p8a.htm',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Blair faz ultimato aos talibãs',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010926105159mp_/http://www.dn.pt:80/int/26p7b.htm',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Arábia Saudita corta relações com Cabul',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010926105159mp_/http://www.dn.pt:80/int/26p10a.htm',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Investigação policial segue pista de Hamburgo',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010926105159mp_/http://www.dn.pt:80/int/26p11a.htm',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Guterres claramente ao lado de Bush',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010926105159mp_/http://www.dn.pt:80/int/26p56a.htm',
            'headline': 'Ataque aos EUA (11-09-2001)',
            'title': 'Máscaras de gás esgotam em Portugal',
            'category': 'Destaque',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010926105159mp_/http://www.dn.pt:80/pna/26p20a.htm',
            'headline': 'Euro',
            'title': 'Notas grandes sem trocos',
            'category': 'Portugal',
            'importance': Importance.LARGE
        })

        timestamp = 20010928105514
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010928105514mp_/http://www.dn.pt:80/int/28p8a.htm',
            'headline': 'Ataque aos EUA',
            'title': 'Raide nas bolsas',
            'snippet': 'Organismos fiscalizadores dos mercados financeiros europeus passaram a pente fino todos os negócios com acções efectuados nas bolsas entre 1 de Agosto e 15 de Setembro para identificar e congelar as contas de indíviduos e organizações ligados ao terrorismo',
            'img_url': 'https://arquivo.pt/wayback/20010928105614im_/http://www.dn.pt:80/pri/pri1.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010928105514mp_/http://www.dn.pt:80/int/28p10a.htm',
            'headline': 'Entrevista',
            'title': 'Soares admite sacrificar alguma liberdade',
            'snippet': 'Mário Soares admite sacrificar "ponderadamente" alguma liberdade para combater o terrorismo. Numa entrevista de fundo ao DN, o ex-presidente da República expressa as suas preocupações sobre a actual crise internacional. Considera nomeadamente que a ONU criou um precedente novo e deu luz verde à "retaliação" dos EUA',
            'img_url': 'https://arquivo.pt/wayback/20010928105715im_/http://www.dn.pt:80/pri/pri2.jpg',
            'category': 'Destaque',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010928105514mp_/http://www.dn.pt:80/des/28p37a.htm',
            'headline': 'Benfica',
            'title': 'Vale e Azevedo escreve carta aos sócios',
            'img_url': 'https://arquivo.pt/wayback/20010928231102im_/http://www.dn.pt:80/pri/pri3.jpg',
            'category': 'Desporto',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010928105514mp_/http://www.dn.pt:80/ige/28p24a.htm',
            'headline': 'Suiça',
            'title': 'Homem mata a tiro 14 pessoas',
            'img_url': 'https://arquivo.pt/wayback/20010928231213im_/http://www.dn.pt:80/pri/pri4.jpg',
            'category': 'Mundo',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010928105514mp_/http://www.dn.pt:80/pna/28p18a.htm',
            'headline': 'Euro',
            'title': 'Algarve preocupado',
            'category': 'Portugal',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010928105514mp_/http://www.dn.pt:80/pna/28p22a.htm',
            'headline': 'Barómetro',
            'title': 'PSD mantém avanço',
            'category': 'Política',
            'importance': Importance.LARGE
        })

        timestamp = 20010929113720
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010929113851im_/http://www.dn.pt:80/pri/pri1.jpg',
            'headline': '"Liberdade Duradoura"',
            'title': 'Tropas de Bush nos montes afegãos',
            'snippet': 'Forças especiais americanas já estão no Afeganistão na caça a Ben Laden (reportagem de Manuel Ricardo Ferreira em Nova Iorque)',
            'img_url': 'https://arquivo.pt/wayback/20010929113851im_/http://www.dn.pt:80/pri/pri1.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010929113720mp_/http://www.dn.pt:80/pna/29p4a.htm',
            'headline': 'Entrevista a Mário Soares',
            'title': 'Cartão amarelo para governação PS',
            'snippet': 'Mário Soares é particularmente crítico em relação aos "dois anos em que houve uma deriva no Governo". Relativamente ao actual ministro dos Negócios Estrangeiros, o ex-presidente da República lembra a falta de solidariedade quando foi alvo de críticas de Luanda: "Toda a gente percebeu que Jaime Gama não me defendeu"',
            'img_url': 'https://arquivo.pt/wayback/20010929113946im_/http://www.dn.pt:80/pri/pri2.jpg',
            'category': 'Política',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010929113720mp_/http://www.dn.pt:80/eco/29p35a.htm',
            'headline': 'Crédito à habitação',
            'title': 'Taxas de juro dos empréstimos tornam a baixar em Portugal',
            'category': 'Destaque',
            'importance': Importance.LARGE
        })

        timestamp = 20010930000000  # not the date in the snapshot, but the date on the actual page
        all_news.append({
            'arquivo_source_url': 'https://arquivo.pt/wayback/20011001001039/http://www.dn.pt:80/pri/sintpri.htm',
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20011001001039mp_/http://www.dn.pt:80/int/30p6a.htm',
            'headline': 'Resistir à pedrada',
            'title': 'Talibãs prometem resistir até ao último homem',
            'snippet': 'O povo afegão tenciona honrar a tradição conquistada ao longo dos séculos e oferecer uma resistência feroz aos invasores estrangeiros, conforme pôde confirmar Luís Naves. O enviado especial do DN está em Quetta, no Paquistão, junto à fronteira com o Afeganistão',
            'img_url': 'https://arquivo.pt/wayback/20011001001152im_/http://www.dn.pt:80/pri/pri1.jpg',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'arquivo_source_url': 'https://arquivo.pt/wayback/20011001001039/http://www.dn.pt:80/pri/sintpri.htm',
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20010929234812im_/http://www.dn.pt:80/pri/pri2.jpg',
            'headline': 'Entrevista a Mário Soares',
            'title': '"Em Portugal há terroristas cabacos tratados como heróis"',
            'img_url': 'https://arquivo.pt/wayback/20010929234812im_/http://www.dn.pt:80/pri/pri2.jpg',
            'category': 'Sociedade',
            'importance': Importance.LARGE
        })
        all_news.append({
            'arquivo_source_url': 'https://arquivo.pt/wayback/20011001001039/http://www.dn.pt:80/pri/sintpri.htm',
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20011001001039mp_/http://www.dn.pt:80/ige/30p31a.htm',
            'title': 'Governo promete dinheiro para o funcionamento das universidades',
            'category': 'Educação',
            'importance': Importance.LARGE
        })
        all_news.append({
            'arquivo_source_url': 'https://arquivo.pt/wayback/20011001001039/http://www.dn.pt:80/pri/sintpri.htm',
            'timestamp': timestamp,
            'article_url': 'https://arquivo.pt/wayback/20011001001039mp_/http://www.dn.pt:80/des/30p32a.htm',
            'headline': 'Meia Maratona',
            'title': 'Africanos no top das expectativas e Sampaio vai correr com a camisola número 1',
            'category': 'Sociedade',
            'importance': Importance.LARGE
        })

        # add deterministic no url flag (deterministic because it's used as key)
        for news in all_news:
            if 'article_url' not in news:
                news['article_url'] = generate_dummy_url(self.source, news['timestamp'], news['category'], news['title'])

        return all_news


class ScraperDiarioDeNoticias04(NewsScraper):
    source = 'dn.pt'
    cutoff = 20041019082233

    def scrape_page(self, soup):
        all_news = []

        # colourful top headers
        top_features = soup.find('table', attrs={'width': 460})
        if top_features:
            top_features = top_features.find_all('tr')  # 20021201081654, edited top table out because of html error

            title_elems = top_features[1].find_all('a', class_='destaques4')
            category_elems = top_features[0].find_all('a', class_='destaques4')
            for i in range(len(title_elems)):
                title_elem = title_elems[i]

                category = category_elems[i].get_text()
                m = re.match(r'(.*)\s*[0-9][0-9]:[0-9][0-9]', category)  # remove the hour
                if m:
                    category = m.group(1)

                if clean_special_chars(category).lower() in ['dossier', 'verão']:
                    continue

                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': remove_clutter(title_elem.get_text()),
                    'category': clean_special_chars(category),
                    'importance': Importance.LARGE
                })

        # TSF section
        tsf_articles = soup.find('table', attrs={'bgcolor': '#FF9700'}).find_all('tr')
        for article_elem in [e.find('td', attrs={'width': re.compile(r'^16[0-2]$')}) for e in tsf_articles]:
            pretitle_elem = article_elem.find(re.compile(r'a|span'), class_='footer6')
            title_elem = article_elem.find(re.compile(r'a|span'), class_='resume')
            url_elem = title_elem.find_parent('a') if title_elem.name == 'span' else title_elem

            all_news.append({
                'article_url': url_elem.get('href'),
                'headline': pretitle_elem.get_text(),
                'title': title_elem.contents[0],  # first navigable string only
                'category': 'Destaque',
                'importance': Importance.SMALL
            })

        # the rest of the elements have no titles, so don't fit the website model...

        return all_news


class ScraperDiarioDeNoticias05(NewsScraper):
    source = 'dn.pt'
    cutoff = 20081022054427

    def scrape_page(self, soup):
        all_news = []

        # main features
        category = 'Destaque'
        for article_elem in soup.find_all('table', attrs={'width': re.compile(r'279|450|569')}):
            category_elem = article_elem.find('span', class_='arial_10_cinza_escuro')
            if category_elem:
                category = clean_special_chars(category_elem.get_text())
                continue

            # avoid promotional stuff
            promo_comment = find_comments(article_elem, ' promocoes_centro ')
            if len(promo_comment) > 0:
                continue

            pretitle_elem = article_elem.find('span', class_='arial_10_cinzaclaro')
            pretitle = pretitle_elem.get_text().title() if pretitle_elem else None

            title_elem = article_elem.find('span', class_='arial_azul_escuro_b')
            snippet_elem = article_elem.find('span', class_='arial_noticias_cinza')

            img_elems = article_elem.find_all('img', attrs={'src': re.compile(r'.jpg$')})
            img_url = img_elems[0].get('src') if len(img_elems) > 0 else None

            all_news.append({
                'article_url': title_elem.find_parent('a').get('href'),
                'title': remove_clutter(title_elem.get_text()),
                'headline': pretitle,
                'snippet': snippet_elem.get_text(),
                'img_url': img_url,
                'category': clean_special_chars(category),
                'importance': Importance.FEATURE
            })

        # get categories
        category_articles = soup.find('table', attrs={'bordercolor': '#F1F1F1'}).find_all('span', class_='arial_10_cinza_escuro')
        for article_elem in [e.find_parent('div') for e in category_articles]:
            title_elem = article_elem.find('span', class_='arial_10_azul_esc')
            category = article_elem.find('span', class_='arial_10_cinza_escuro').get_text()

            all_news.append({
                'article_url': title_elem.find_parent('a').get('href'),
                'title': remove_clutter(title_elem.get_text()),
                'category': clean_special_chars(category),
                'importance': Importance.SMALL
            })

        # get latest
        latest_elems = soup.find('div', id='destdir')
        if latest_elems:
            for article_elem in [e.find_parent('a') for e in latest_elems.find_all('span', class_='arial_10_cinza_escuro')]:
                pretitle_elem = article_elem.find('span', class_='arial_10_cinza_escuro')
                title_elem = article_elem.find('span', class_='arial_10_cinzaclaro')

                all_news.append({
                    'article_url': title_elem.find_parent('a').get('href'),
                    'title': remove_clutter(title_elem.get_text()),
                    'pretitle': pretitle_elem.get_text(),
                    'category': 'Outras',
                    'importance': Importance.LATEST
                })

        return all_news


class ScraperDiarioDeNoticias06(NewsScraper):
    source = 'dn.pt'
    cutoff = 20151013180422

    def get_related(self, all_news, related_elems, category):
        for title_elem in [e.find('a') for e in related_elems]:
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'category': category,
                'importance': Importance.RELATED
            })

    def extract_article(self, all_news, article_elem, category):
        title_elem = article_elem.find('h3', class_=re.compile(r'^destaque(640)?-tit-not$')) or article_elem.find('h4')
        if not title_elem:
            return  # 20110119160220, article without title

        title_elem = title_elem.find('a')
        title = remove_clutter(title_elem.get_text())

        if not title or title.lower() == 'tudo sobre o combate ao défice':
            return  # 20100514140118, not a news article

        snippet_elem = article_elem.find('p', recursive=False)

        pretitle_elem = article_elem.find('h5', class_='dest-anttit')
        pretitle = pretitle_elem.get_text() if pretitle_elem else None

        # grab image, deal with no a tag, a tag but no img tag, or both and then get the src
        img_elem = article_elem.find('a', recursive=False)
        img_url = None
        if img_elem:
            img_elem = img_elem.find('img')
            img_url = img_elem.get('src') if img_elem else None

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': title,
            'headline': pretitle,
            'snippet': snippet_elem.get_text(),
            'img_url': img_url,
            'category': category,
            'importance': Importance.LARGE
        })

        # add related
        related_elems = article_elem.find('div', class_='cx-listas')
        if related_elems:
            self.get_related(all_news, related_elems.find_all('li'), category)

    def scrape_page(self, soup):
        all_news = []

        # main feature
        feature_box = soup.find('div', id='ctl00_ctl00_ctl00_bcr_bcr_middlecontent_bcr_Manchetes_ctl00_contentDiv')
        for article_elem in feature_box.find_all('div', recursive=False):
            header_elem = article_elem.find('div', class_='cx-noticias-cor-topo').find('div', class_=re.compile(r'cx-noticias-cor-titulos(-ccc)?'))
            lower_elem = article_elem.find('div', class_='cx-noticias-cor-txt')

            # find img element
            img_elems = [e for e in article_elem.find_all('img') if not e.find('div', class_='cx-noticias-cor-topo') and not e.find('div', class_='cx-noticias-cor-txt') and not e.get('src').endswith('.gif')]
            img_url = img_elems[0].get('src') if len(img_elems) > 0 else None

            # extract title and pretitle
            pretitle_elem = header_elem.find('h5')
            pretitle = pretitle_elem.get_text() if pretitle_elem else None

            title_elem = header_elem.find('h2').find('a')

            # extract snippet
            snippet_elem = lower_elem.find('p')

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'headline': pretitle,
                'snippet': snippet_elem.get_text(),
                'img_url': img_url,
                'category': 'Destaque',
                'importance': Importance.FEATURE
            })

            # add related
            related_elems = lower_elem.find('div', class_='cx-listas')
            if related_elems:
                self.get_related(all_news, related_elems.find_all('li'), 'Destaque')

        # large articles
        large_box = soup.find('div', id=re.compile(r'ctl00_ctl00_ctl00_bcr_bcr_middlecontent_bcr_DestaquesC1?_ctl00_contentDiv'))
        for article_elem in [e.find('td') for e in large_box.find_all('div', class_='destaque')]:
            self.extract_article(all_news, article_elem, 'Destaque')

        # desporto box
        desporto_box = soup.find('div', class_='cx-desporto-txt-n0')

        # desporto large
        desporto_large_articles = desporto_box.find_all('div', id=re.compile(r'ctl00_ctl00_ctl00_bcr_bcr_middlecontent_bcr_Desporto1_Destaque_ctl[0-9][0-9]_contentDiv'))
        for article_elem in desporto_large_articles:
            img_url = article_elem.find('div', class_='vid-desporto').find('img').get('src')

            text_elem = article_elem.find('div', class_='tab-desporto-impar')
            title_elem = text_elem.find('h5').find('a')
            snippet_elem = text_elem.find('p', recursive=False)

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet_elem.get_text(),
                'img_url': img_url,
                'category': 'Desporto',
                'importance': Importance.LARGE
            })

        # desporto small
        desporto_articles = desporto_box.find_all('div', class_=re.compile(r'^tab-desporto-(im)?par$'))[len(desporto_large_articles):]  # exclude the large divs, captured above
        for title_elem in [e.find('h5').find('a') for e in desporto_articles]:
            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'category': 'Desporto',
                'importance': Importance.SMALL
            })

        # sections
        section_boxes = soup.find_all('div', id=re.compile(r'ctl00_ctl00_ctl00_bcr_bcr_middlecontent_ctl[0-9][0-9]_ngContent_ctl00_contentDiv'))
        all_articles = []
        for elem in section_boxes:
            all_articles += elem.find_all('div', class_='destaque')

        for article_elem in [e.find('td') for e in all_articles]:
            category = article_elem.find_previous('div', class_='tit-icn-seccoes').find_parent('div').find('h5').get_text()
            self.extract_article(all_news, article_elem, category)

        # narrow column articles
        narrow_box = soup.find('div', id='cln-mid-n2')

        uncategorised_articles = narrow_box.find('div', id='ctl00_ctl00_ctl00_bcr_bcr_bbcr_bbcr_DestaquesD_ctl00_contentDiv').find_all('div', class_=lambda name: name != 'line6', recursive=False)
        for article_elem in uncategorised_articles:
            self.extract_article(all_news, article_elem, 'Destaque')

        category_articles = narrow_box.find_all('div', id=re.compile(r'^ctl00_ctl00_ctl00_bcr_bcr_bbcr_\w*_ngContent_ctl00_contentDiv$'))
        for article_elem in category_articles:
            title_elem = (article_elem.find('h5', class_='tit-sublinhado') or article_elem.find('h4', class_='tit-pessoas-itl')).find('a')
            snippet_elem = article_elem.find('p', class_='tit-sublinhado')

            img_elem = article_elem.find('img')
            img_url = img_elem.get('src') if img_elem else None

            category = article_elem.find_previous('div', class_='tit-icn-seccoes').find_parent('div').find('h5').get_text()

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet_elem.get_text(),
                'img_url': img_url,
                'category': category,
                'importance': Importance.LARGE
            })

            # add related
            related_elems = article_elem.find('div', class_='cx-listas-espacadas')
            if related_elems:
                self.get_related(all_news, related_elems.find_all('li'), category)

        return all_news


class ScraperDiarioDeNoticias07(NewsScraper):
    source = 'dn.pt'
    cutoff = 20151231180223  # not tested after this

    def scrape_page(self, soup):
        all_news = []

        # main feature
        article_elems = soup.find_all('article')
        for article_elem in article_elems:
            # remove football results article
            if article_elem.find('h3', id='jornada_atual'):
                continue

            title_elem = article_elem.find('h2', attrs={'itemprop': 'headline'})

            pretitle_elem = article_elem.find('h3', attrs={'itemprop': 'articleSection'})
            pretitle = pretitle_elem.get_text().title() if pretitle_elem else None

            # pretitle ignores
            if pretitle in ['Perfil']:
                continue

            snippet_elem = article_elem.find('h4', attrs={'itemprop': 'description'})
            snippet = snippet_elem.get_text() if snippet_elem else None

            img_elem = article_elem.find('figure')
            img_url = img_elem.find('img').get('data-src') if img_elem else None

            category = 'Destaque'
            parent_section = article_elem.find_parent('section')
            if parent_section:
                # if we are in a section, we need see if the header has something
                header = parent_section.find('header').find('h2')
                if header:
                    category = clean_special_chars(header.find('span').get_text())

                    # sanitise category
                    if category in ['O país à espera', 'Novo Governo', 'O país de novo à espera', 'Novo governo']:
                        category = 'Política'
                    elif category in ['Em Portugal']:
                        category = 'Portugal'
                    elif category in ['No Mundo']:
                        category = 'Mundo'
                    elif category in ['Mundial de Surf', 'Surf em Peniche']:
                        category = 'Desporto'

            # category ignores
            if category in ['Galerias e Vídeos', 'Evasões', 'Notícias Maganize', 'Notícias Magazine', 'Estreiam hoje', 'DN Ilustrado', 'Estreias', 'Os mais lidos de 2015', 'Edição especial 151º aniversário']:
                continue

            all_news.append({
                'article_url': title_elem.find_parent('a').get('href'),
                'title': title_elem.get_text(),
                'snippet': snippet,
                'headline': pretitle,
                'img_url': img_url,
                'category': category,
                'importance': Importance.FEATURE if img_url and snippet else Importance.LARGE if img_url else Importance.SMALL
            })

            # get related elements
            related_articles = article_elem.find('nav', class_='t-article-related-1')
            if related_articles:
                for related_elem in [e.find('a') for e in related_articles.find_all('li')]:
                    all_news.append({
                        'article_url': related_elem.get('href'),
                        'title': related_elem.find('span').get_text(),
                        'category': category,
                        'importance': Importance.RELATED
                    })

        # get topbar latest news
        latest_elems = soup.find_all('div', class_='t-main-topbar-newslist')
        if len(latest_elems) > 0:
            # ignore "ao vivo"
            latest_elems = [e for e in latest_elems if 'Última Hora' in e.find_parent('div').find('strong').get_text()]
            if len(latest_elems) > 0:
                for title_elem in [e.find('a') for e in latest_elems[0].find_all('li')]:
                    all_news.append({
                        'article_url': title_elem.get('href'),
                        'title': title_elem.get_text(),
                        'category': 'Outras',
                        'importance': Importance.LATEST
                    })

        return all_news
