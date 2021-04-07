import re

from bs4 import Tag, Comment, NavigableString

from src.util import generate_dummy_url, generate_destaques_uniqueness, is_between, find_comments, find_comments_regex
from src.text_util import remove_clutter, clean_special_chars, prettify_text, ignore_title

from src.scrapers.news_scraper import NewsScraper, Importance


class ScraperJornalDeNoticias01(NewsScraper):
    source = 'jn.pt'
    cutoff = 20000706210529
    used = False

    # dummy scraper, returns a set of very old news only once
    def scrape_page(self, soup):
        if self.used:
            return None

        all_news = []

        timestamp = 19981212030154
        all_news.append({
            'timestamp': timestamp,
            'title': 'Oliveira de ramo verde aos 90 anos',
            'category': 'Destaque',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Condes de Penha Garcia mortos em incêndio no Fundão ',
            'snippet': 'No solar funcionava um lar para idosos',
            'category': 'Destaque',
            'importance': Importance.LARGE
        })

        timestamp = 19990125090420
        all_news.append({
            'timestamp': timestamp,
            'title': 'Obras no Centro de Saúde de Sever aguardam aprovação',
            'snippet': 'Falta de condições do posto de Rocas em foco na Assembleia Municipal',
            'category': 'Destaque',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Povo convidado a consultar impacte ambiental do IC14 ',
            'snippet': 'Habitações da freguesia barcelense de Carvalhal vão ser demolidas. Terrenos agrícolas os mais afectados. Consequências do progresso',
            'category': 'Destaque',
            'importance': Importance.LARGE
        })

        timestamp = 20000301021608
        all_news.append({
            'timestamp': timestamp,
            'title': 'Uma dança dos sentidos com bandoneón',
            'snippet': '"Forever Tango", de Luis Bravo, a partir de hoje e até 12 de Março, no CCB, reúne bailarinos e orquestra ao vivo. "Um sentimento que se dança", em toda a sua pujança e criatividade, agora em Portugal, dez anos depois da estreia em San Diego, num espectáculo várias vezes premiado',
            'category': 'Cultura',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': 20000229103034,
            'article_url': 'https://arquivo.pt/wayback/20000229103034/http://jn.pt:80/textos/textho2.htm',  # found this one by doing the "hidden pages" one below
            'title': 'Subida no preço do papel marca evolução do sector',
            'snippet': 'No horizonte de três a quatro anos é previsível que a Papéis Inapa reforce a capacidade de produção com novos equipamentos',
            'category': 'Economia',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Órgão de tubos continua fora de tom',
            'snippet': 'Conserto de valioso instrumento do séc. XIX, da igreja de Santo Ildefonso, custa 20 mil contos. A falta de apoios financeiros tem adiado o restauro desta obra prima com 1308 tubos. O cónego Alfredo Soares resolveu restituir a dignidade do orgão colocado no coro alto do templo religioso',
            'category': 'Cultura',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Cidadão deficiente não pára de crescer',
            'snippet': 'Associação Portuguesa de Pais e Amigos do Cidadão com Deficiência Mental contabiliza dezenas de milhares no Alto Minho, dos quais 3504 com problemas mentais',
            'category': 'Sociedade',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Surf do Porto na onda do sucesso',
            'snippet': 'Grémio nortenho, fundado em 1990 por um grupo de surfistas, é tricampeão, mas está contra o actual figurino do campeonato nacional de clubes',
            'category': 'Desporto',
            'importance': Importance.LARGE
        })

        timestamp = 20000302190807
        all_news.append({
            'timestamp': timestamp,
            'title': 'Reforçar o lado urbano do turismo português',
            'snippet': 'Lisboa e Funchal são os únicos pólos. Quanto ao Porto, pode-se falar num turismo compósito e itinerante num espaço que vai para lá da Área Metropolitana do Porto, abrangendo praticamente todo o Norte e com polaridades diferentes entre si',
            'category': 'Sociedade',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Salão do Livro já mexe em Paris',
            'snippet': 'Antecipando o Salão do Livro de Paris, realiza-se hoje na Sorbonne um colóquio subordinado ao tema «Portugal, Sonho e Descobertas»',
            'category': 'Cultura',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Barco para a arte da xávega reforça a frota da Torreira',
            'snippet': 'Lançamento à água, na Ribeira de Pardilhó, teve honras de grande evento, com foguetes e espumante derramado no casco',
            'category': 'Sociedade',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Escórias da Metalimex ainda dão dor de cabeça',
            'snippet': 'O presidente da Junta de Freguesia do Sado, Eusébio Candeias, continua à espera que o Ministério do Ambiente avalie a eventual contaminação dos terrenos do Vale da Rosa',
            'category': 'Ambiente',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': '«Saí pela porta pequena do futebol português»',
            'snippet': 'Miguel Simão é um jovem deste tempo, um imigrante contemporâneo, sem receios do inesperado. De trato afável e amigável, a sua imagem transparece uma grande segurança. De olhos grandes e atentos, curiosos, dispostos a aceitar as diferenças culturais do mundo, Miguel, é o descobridor moderno em busca de novos lugares e oportunidades',
            'category': 'Desporto',
            'importance': Importance.LARGE
        })

        timestamp = 20000407102519
        all_news.append({
            'timestamp': timestamp,
            'title': 'Europa chumba subsídios à RTP e dá razão à SIC',
            'snippet': 'Tribunal de 1.ª Instância contraria decisão da Comissão Europeia. Governo desvaloriza acórdão de Luxemburgo',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Roma acena a Mário Jardel',
            'snippet': 'Clube italiano disposto a pagar 3,5 milhões de contos',
            'category': 'Desporto',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Lusomundo aprova oferta de aquisição lançada pela PT Multimédia',
            'snippet': 'Operação é considerada oportuna do ponto de vista estratégico e atractiva quanto ao preço',
            'category': 'Economia',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Porto perde históricos Armazéns do Anjo',
            'snippet': 'Loja de referência da cidade foi uma das mais pujantes e durante anos esteve na esquina das ruas de Alexandre Braga e Formosa',
            'category': 'Local',
            'importance': Importance.LARGE
        })

        timestamp = 20000619173457
        all_news.append({
            'timestamp': timestamp,
            'title': 'Chave ouro no final da presidência portuguesa da UE',
            'snippet': 'Harmonização fiscal dos "Quinze" coroou meio ano de trabalhos',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Selecção em pleno na primeira fase do Euro\'2000',
            'snippet': 'Goleada (3-0) à Alemanha, campeã em título, teve como herói Sérgio Conceição',
            'category': 'Desporto',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Combate ao consumo de drogas agita Parlamento',
            'snippet': 'Quatro projectos hoje em debate. Penalista Faria Costa contra o referendo. Deputados da Oposição justificam-se no JN. Ordem dos Advogados critica despenalização',
            'category': 'Política',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Belmiro de crítico a candidato à obra das molhes do Douro',
            'snippet': 'Grupo do empresário apresenta proposta de construção mais cara',
            'category': 'Economia',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Luciano Pavarotti faça chuva ou sol',
            'snippet': 'Tenor italiano actua hoje no estádio S. Luís, em Faro, num concerto em que foi anulada a participação de Nuno Guerreiro',
            'category': 'Cultura',
            'importance': Importance.LARGE
        })

        # the following news were not crawled by the script, they're not main page news, and arquivo.pt doesn't have the
        # corresponding main page for them; I found them by clicking on main page news and being shown that page but
        # from other date (the same page url was reused for different news)
        all_news.append({
            'timestamp': 20000119161401,
            'arquivo_source_url': 'https://arquivo.pt/wayback/20000119161401/http://www.jn.pt:80/textos/textho1.htm',
            'title': 'Londres na iminência de libertar Pinochet',
            'snippet': 'O Ministério da Defesa britânico informou ontem estar prevista para hoje a chegada a uma base militar de Londres do avião militar que deverá transportar o ex-ditador Augusto Pinochet de volta ao Chile.',
            'category': 'Internacional',
            'importance': Importance.UNKNOWN
        })
        all_news.append({
            'timestamp': 20000305233005,
            'arquivo_source_url': 'https://arquivo.pt/wayback/20000305233005/http://www.jn.pt:80/textos/textho1.htm',
            'title': 'Primeira piscina por meio milhão',
            'snippet': 'A Câmara Municipal de Mira vai investir cerca de meio milhão de contos na construção da que será a primeira piscina pública do município.',
            'category': 'Local',
            'importance': Importance.UNKNOWN
        })
        all_news.append({
            'timestamp': 20000606115230,
            'arquivo_source_url': 'https://arquivo.pt/wayback/20000606115230/http://www.jn.pt:80/textos/textho1.htm',
            'title': 'Droga cercada em três frentes',
            'snippet': 'A Directoria de Faro da Polícia Judiciária (PJ) anunciou, ontem, a apreensão, durante o fim-de-semana, em Tavira, de cerca de 3600 quilogramas de haxixe, o equivalente a 18 milhões de doses individuais daquele estupefaciente.',
            'category': 'Portugal',
            'importance': Importance.UNKNOWN
        })
        all_news.append({
            'timestamp': 20000615035758,
            'arquivo_source_url': 'https://arquivo.pt/wayback/20000615035758/http://jn.pt:80/textos/textho1.htm',
            'title': 'Doenças da pele afectam 10% das crianças',
            'snippet': 'Mais de 10% das crianças sofrem de eczemas atópicos, uma doença de pele que causa muito desconforto e que pode aparecer logo aos três meses de idade.',
            'category': 'Sociedade',
            'importance': Importance.UNKNOWN
        })
        all_news.append({
            'timestamp': 20000622040528,
            'arquivo_source_url': 'https://arquivo.pt/wayback/20000622040528/http://jn.pt:80/textos/textho1.htm',
            'title': 'Doadores generosos com Timor',
            'snippet': 'A reunião de ontem, em Lisboa, entre o Banco Mundial e o Banco de Desenvolvimento Asiático (ADP) com os países doadores foi recheada de críticas e promessas.',
            'category': 'Política',
            'importance': Importance.UNKNOWN
        })
        all_news.append({
            'timestamp': 20001001130645,
            'arquivo_source_url': 'https://arquivo.pt/wayback/20001001130645/http://jn.pt:80/textos/textho1.htm',
            'title': 'Câmaras desperdiçam a Internet',
            'snippet': 'Paras as autarquias locais, os tempos são de mudança: o cidadão tem mais consciência e capacidade reivindicativa dos seus direitos; vulgariza-se a utilização da Internet na sociedade...',
            'category': 'Sociedade',
            'importance': Importance.UNKNOWN
        })

        all_news.append({
            'timestamp': 19991013014029,
            'arquivo_source_url': 'https://arquivo.pt/wayback/19991013014029/http://www.jn.pt:80/textos/textho2.htm',
            'title': 'Idosos da Maia visitaram belezas dos Açores',
            'snippet': 'Durante cinco dias, cinquenta idosos do concelho da Maia visitaram algumas das belezas naturais da ilha de S.Miguel, nos Açores.',
            'category': 'Sociedade',
            'importance': Importance.UNKNOWN
        })
        all_news.append({
            'timestamp': 19991108231317,
            'arquivo_source_url': 'https://arquivo.pt/wayback/19991108231317/http://www.jn.pt:80/textos/textho2.htm',
            'title': 'Série sobre Macau vai estrear na RTP',
            'snippet': 'Antecipando a entrega da administração de Macau à República Popular Chinesa, que tem lugar no próximo dia 20 de Dezembro, a RTP estreia na sexta-feira a série documental "Macau entre Dois Mundos".',
            'category': 'Entretenimento',
            'importance': Importance.UNKNOWN
        })
        all_news.append({
            'timestamp': 20000306015406,
            'arquivo_source_url': 'https://arquivo.pt/wayback/20000306015406/http://www.jn.pt:80/textos/textho2.htm',
            'title': 'Presidentes da República inauguram casa de Cabral',
            'snippet': 'Pedro Álvares Cabral - ou "Pedrão", como lhe chamam os brasileiros -, terá, dentro de alguns dias, o seu nome e os seus "feitos" perpetuados numa casa onde, tudo indicia, terá vivido.',
            'category': 'Local',
            'importance': Importance.UNKNOWN
        })
        all_news.append({
            'timestamp': 20000606150440,
            'arquivo_source_url': 'https://arquivo.pt/wayback/20000606150440/http://www.jn.pt:80/textos/textho2.htm',
            'title': 'Benfica em sobressalto',
            'snippet': 'Em estado de choque. Esta foi a imagem deixada por cerca de meio milhar de adeptos que ontem cercaram as imediações do complexo do Benfica procurando explicações para a saída de João Pinto.',
            'category': 'Desporto',
            'importance': Importance.UNKNOWN
        })
        all_news.append({
            'timestamp': 20001011020914,
            'arquivo_source_url': 'https://arquivo.pt/wayback/20001011020914/http://www.jn.pt:80/textos/textho2.htm',
            'title': 'Serenata no gelo',
            'snippet': 'Aonde quer que se desloquem garantem casa cheia; a linguagem que utilizam é tão universal que derruba quaisquer barreiras, culturais, ideológicas, linguísticas melhor ainda: são vistos, e apreciados, tanto por crianças como por adultos. Milagre de consenso? Numa linha: Holiday on Ice.',
            'category': 'Cultura',
            'importance': Importance.UNKNOWN
        })
        all_news.append({
            'timestamp': 20010113010200,
            'arquivo_source_url': 'https://arquivo.pt/wayback/20010113010200/http://www.jn.pt:80/textos/textho2.htm',
            'title': 'Olhos postos na abstenção',
            'snippet': '"Abstenção" foi talvez a palavra mais ouvida nesta campanha presidencial. Como um verdadeiro adversário político, veio mobilizar os esforços dos cinco candidatos presidenciais para levar os portugueses às urnas.',
            'category': 'Política',
            'importance': Importance.UNKNOWN
        })
        all_news.append({
            'timestamp': 20010308145751,
            'arquivo_source_url': 'https://arquivo.pt/wayback/20010308145751/http://jn.pt:80/textos/textho2.htm',
            'title': 'Molhes do Douro arrancam este ano',
            'snippet': 'O consórcio liderado pelas empresas "Irmãos Cavaco" e "Somague Engenharia" arrecadou o primeiro lugar na classificação provisória do concurso internacional para a concepção e construção dos molhes do Douro, apurou o JN.',
            'category': 'Local',
            'importance': Importance.UNKNOWN
        })

        all_news.append({
            'timestamp': 20010308145259,
            'arquivo_source_url': 'https://arquivo.pt/wayback/20010308145259/http://jn.pt:80/textos/textho4.htm',
            'title': 'Emoção forte nas Antas',
            'snippet': 'A maioria dos adeptos do Liverpool chega esta manhã ao Aeroporto Francisco Sá Carneiro. Ao todo, serão cerca de 1000, contrariando, assim, as expectativas de uma maior invasão. Segundo informações colhidas junto do clube inglês, a derrota em Leicester terá abalado a confiança dos adeptos.',
            'category': 'Desporto',
            'importance': Importance.UNKNOWN
        })

        all_news.append({
            'timestamp': 20010308144849,
            'arquivo_source_url': 'https://arquivo.pt/wayback/20010308144849/http://jn.pt:80/textos/textho5.htm',
            'title': 'Barricado do Carrefour passou o dia na PJ',
            'snippet': 'José Luís Silva, o homem que se barricou, com uma refém, na terça-feira, na dependência do Banco Internacional de Crédito (BIC) do Carrefour de Telheiras, após ter alvejado a mulher, foi ontem presente pela primeira vez ao Tribunal de Instrução Criminal de Lisboa, mas só hoje será ouvido por um magistrado.',
            'category': 'Portugal',
            'importance': Importance.UNKNOWN
        })

        # add deterministic no url flag (deterministic because it's used as key)
        for news in all_news:
            if 'article_url' not in news:
                news['article_url'] = generate_dummy_url(self.source, news['timestamp'], news['category'], news['title'])

        self.used = True
        return all_news


class ScraperJornalDeNoticias02(NewsScraper):
    source = 'jn.pt'
    cutoff = 20010630035911

    # This page has the particular problem of re-using the same urls for different news, so urls are basically unusable.
    # The page is also wildly confusing and disorganised, so some articles are hard-coded. This parser is not intended
    # as an example of automation, it's mostly handwork with a help.

    def scrape_page(self, soup):
        all_news = []

        titles = soup.find_all('a', attrs={'href': re.compile(r'.*/textos/textho[0-9]\.asp')})
        self.process_titles(all_news, titles)

        titles = soup.find_all('a', attrs={'href': re.compile(r'.*/textos/texult[0-9]\.asp')})
        self.process_titles(all_news, titles)

        return all_news

    def process_titles(self, all_news, titles):
        for title_elem in [title for title in titles if not title.find('i') and clean_special_chars(title.get_text())]:
            title = remove_clutter(title_elem.get_text())
            if title.endswith('.'):
                title = title[:-1]

            # 20010118211400: marketing
            if title == 'JN líder destacado nas audiências dos jornais portugueses':
                continue

            category_elem, category = self.extract_category(title_elem)

            # sometimes the category is empty, but there's another one up
            if category is not None and len(category) == 0:
                category_elem, category = self.extract_category(category_elem)

            snippet_elem = title_elem.find_next('font', attrs={'size': 1, 'face': 'Arial'})  # even if there's no snippet this should work as there's an empty element
            snippet = self.extract_snippet(snippet_elem)
            if snippet and snippet.startswith('Foto:'):  # eg 20010302013920
                snippet = None
            if snippet and snippet == 'Jamal Aruri/EPA':  # 20010418144651
                snippet = None

            headline = None

            # 20010301083602: captured both title and headline as different news, this makes it capture the later only
            if title == 'Neto Valente':
                continue
            elif title == 'Raptado em Macau':
                headline = 'Neto Valente'

            # 20010331005408
            if title == 'Censura Pires de Lima ataca Guterres':
                headline = 'Censura'
                title = 'Pires de Lima ataca Guterres'
                snippet = 'Primeiro-ministro, acusado de interferir na Justiça, não responde ao bastonário da Ordem dos Advogados'
            elif title == 'IP5':
                title = 'IP5 será convertido em auto-estrada'
            elif title == 'Eduarda Dionísio Arte e Cultura fora de regras do mercado responsabilidades':
                headline = 'Eduarda Dionísio'
                title = 'Arte e Cultura fora de regras do mercado responsabilidades'
                snippet = None
            elif title == 'Perigos viajam em autocarros camarários':
                category = 'País'
            elif title == 'ETA tenta intimidar os turistas':
                category = 'Mundo'
            elif title == 'Comboio abalroa carrinha e mata duas pessoas':
                category = 'Grande Lisboa'

            # 20010405092529
            if title == 'De Celorico a Cabeceiras de Basto entre buracos':
                continue

            # 20010503192835
            if title == 'Adeptos do Benfica e do Sporting recusam partilha do estádio':
                snippet = None
            elif title == 'Bush avança com guerra das estrelas':
                snippet = 'Decisão viola tratado com os russos'
                category = 'Mundo'
            elif title == 'Há autarcas que vestem a pele de Astérix':
                snippet = 'Comunistas em Penedono e um popular em Tomar'
                category = 'Política'
            elif title == 'Loja e feira do emprego abrem no Estoril':
                category = 'Grande Lisboa'

            # 20010515210519
            if title == 'Portugal garante estreia mundial da tv interactiva':
                snippet = 'Primeiras emissões disponíveis já a 7 de Junho'
            elif title == 'Boavista abdica de eventuais direitos sobre Rafael':
                category = 'Desporto'

            # 20010630035911
            if title == 'Mão-Cheia de ministros':
                continue
            elif title == 'Unidades de saúde têm de registar casos de cancro':
                category = 'Sociedade'

            all_news.append({
                'article_url': generate_dummy_url(self.source, 'parser02', category, title),
                'title': title,
                'snippet': prettify_text(snippet) if snippet else None,
                'headline': headline,
                'category': category,
                'importance': define_importance(title_elem)
            })

    def extract_snippet(self, snippet_elem):
        if snippet_elem.find_parent('td', attrs={'width': '58%'}) or '©' in snippet_elem.get_text() or snippet_elem.attrs.get('color') == '#0075B6':
            # case when no snippet (20001019024432)
            return None

        snippet = snippet_elem.get_text()

        if snippet == '- ':
            # 20010118211400
            snippet_elem = snippet_elem.find_next('font', attrs={'size': 1, 'face': 'Arial'})
            snippet = snippet_elem.get_text()

        if len(snippet) < 3:
            return None

        return snippet

    def extract_category(self, starting_elem):
        category_elem = starting_elem.find_previous('u')
        if not category_elem.find('font'):
            category_elem = category_elem.find_previous('u')

        if not category_elem:
            return None, None

        normal_elem = category_elem.find('a', id='normal') or category_elem.find('a', id='normal10')
        return category_elem, clean_special_chars(normal_elem.get_text())


def define_importance(title_elem):
    if title_elem.find('font') and 'size' in title_elem.find('font'):
        text_size = int(title_elem.find('font')['size'])
    else:
        text_size = 2

    return Importance.FEATURE if text_size > 3 else Importance.LARGE


def snippet_invalid(snippet_elem):
    if snippet_elem.attrs.get('id') == 'normal' or snippet_elem.find('a', id='normal') or snippet_elem.find_parent('a', id='normal'):
        return True

    # avoid case where last title's snippet would be the poll (see 20010919032932)
    if snippet_elem.find_parent('td', attrs={'bgcolor': '#FFCC99'}):
        return True

    return 'Sondagem JN/TSF/Eurosondagem' in (prettify_text(snippet_elem.get_text()) or '')


class ScraperJornalDeNoticias03(NewsScraper):
    source = 'jn.pt'
    cutoff = 20011007040629

    # Same as the previous parser, split this because it was getting too big.

    def scrape_page(self, soup):
        all_news = []

        titles = soup.find_all('a', attrs={'href': re.compile(r'.*/textos/textho[0-9]\.asp')})
        for title_elem in titles:
            if not title_elem.find('font'):
                continue

            title = remove_clutter(title_elem.find('font').get_text())

            if not title:
                # retry a level above, for colourful titles like 20010921052632
                title = remove_clutter(title_elem.get_text())
                if not title:
                    # found in 20010920045320
                    continue
            ################

            ## CATEGORY ##
            category_elem = title_elem.find_previous('a', id='normal')
            if not category_elem:
                # eg 20010918050431 has the category after
                category_elem = title_elem.find_next('a', id='normal')
            elif len(clean_special_chars(category_elem.get_text())) == 0:
                # if category is empty try to find previous one
                category_elem = category_elem.find_previous('a', id='normal')

            category = category_elem.get_text()
            ################

            ## SNIPPET ##
            snippet_elem = title_elem.find_next('font', attrs={'size': 1, 'face': 'Arial'})
            snippet = None

            if snippet_elem:
                # avoid case where snippet finds a category
                if snippet_invalid(snippet_elem):
                    snippet = None
                else:
                    snippet = prettify_text(snippet_elem.get_text())
                    if not snippet:
                        snippet_elem = title_elem.find_next('font', attrs={'size': 2, 'face': 'Arial'})
                        snippet = prettify_text(snippet_elem.get_text())
            ################

            ## IMG ##
            img_url = None

            ## HEADLINE ##
            headline = None

            # 20010918050431
            if title == 'Bolsa de Nova Iorque reabre em queda acentuda mas consegue evitar colapso':
                img_url = title_elem.find_next('img').get('src')

            # 20010919032932
            if title == 'Talibans fazem chantagem':
                snippet = 'Afeganistão admite entregar Bin Laden se os EUA reconhecerem regime'
                img_url = title_elem.find_next('img').get('src')

            # 20010920045320
            if title == 'Tambores da Guerra':
                snippet = 'Justiça infinita: a operação desencadeada pelos EUA está em marcha com apoio do Paquistão'
                img_url = title_elem.find_next('img').get('src')

            # 20010921052632
            if title == '"Com os EUA':
                continue
            elif title == 'ou com os terroristas':
                title = 'Com os EUA ou com os terroristas'
                snippet = 'Bush lança ultimato ao regime taliban'

            # 20010923122735
            if title == 'E o Papa ali tão perto':
                snippet = 'Cazaquistão: João Paulo II pede diálogo em vez das armas'
                img_url = title_elem.find_next('img').get('src')

            # 20010924001640
            if title == 'À ESPERA da ordem de Bush':
                title = 'À espera da ordem de Bush'
                snippet = 'Paquistão: Divisões internas ameaçam estabilidade da região'

            # 20010925000048
            if title == 'RÚSSIA dá passos ao lado dos EUA':
                title = 'Rússia dá passos ao lado dos EUA'
                img_url = title_elem.find_next('img').get('src')

            # 20010926073319
            if title == 'DIPLOMACIA marca terreno':
                title = 'Diplomacia marca terreno'
                snippet = 'Ocidente tenta seduzir mundo muçulmano'
                img_url = title_elem.find_next('img').get('src')

            # 20010927044546
            if title == 'Quase apurados':
                img_url = title_elem.find_next('img').get('src')

            # 20010928121437
            if title == 'Matança na Suíça':
                img_url = title_elem.find_next('img').get('src')
            elif title == 'Corrida às armas no Paquistão':
                headline = 'Fronteira do Paquistão com o Afeganistão'
                snippet = 'Resistência: Diplomata afegão exilado fala ao JN'
            elif title == 'Polícia volta a travar vidreiros à bastonada':
                snippet = None

            # 20010929110049
            if title == 'Tropas dos EUA no Afeganistão':
                snippet = 'Paquistão: Ruas apinhadas com incitamentos à guerra santa'
                img_url = title_elem.find_next('img').get('src')

            # 20010930113220
            if title == 'Afogou-se com a chuva no centro de Setúbal':
                snippet = None
            elif title == 'A crónica de Margarida Rebelo Pinto':
                continue
            elif title == 'Guerra de nervos':
                snippet = 'Miúdos vivem do lixo nas ruas do Paquistão'
                img_url = title_elem.find_next('img').get('src')
            elif title == 'Governo está contra despedimentos na Função Pública':
                snippet = 'Empresários e académicos elaboraram estudo, no qual defendem a dispensa de 150 mil trabalhadores'
            elif title == 'Boavista pode alargar vantagem':
                headline = 'Beira Mar 2 - F.C. Porto 0'
                snippet = 'A noite negra dos comandados de Octávio Machado cedo se percebeu. Foi o Beira Mar que melhor entrou no jogo, dando indícios de repetir a boa exibição conseguida frente ao Benfica...'

            # 20011001011317
            if title == 'Cenário de guerra':
                snippet = 'Bombardeamentos dentro de poucas horas. Bin Laden prepara rotas de fuga no Afeganistão'
                img_url = title_elem.find_next('img').get('src')
            elif title == 'Benfica ganha e continua invicto':
                category = 'Desporto'

            # 20011002002504
            if title == '"Eles não têm coragem para começar uma guerra"':
                category = 'Em foco'
                headline = 'Talibans desafiam EUA '
                img_url = title_elem.find_next('img').get('src')

            # 20011003172711
            if title == 'OTAN':
                title = 'OTAN mais dura'
                snippet = 'Provas dos EUA levam todos os países membros a apoiar ataque contra o terrorismo'
                img_url = title_elem.find_next('img').get('src')
            elif title == 'Assassinados dois presos na cadeia de Vale de Judeus':
                img_url = title_elem.find_next('img').get('src')

            # 20011004044950
            if title == 'PS em maus lençois em Famalicão':
                # political poll results
                continue
            elif title == 'Mortos':
                title = 'Mortos que ninguém quer enterrar'
                snippet = 'Árabes: Secretário da Defesa Rumsfeld tenta vencer resistências'
                img_url = title_elem.find_next('img').get('src')

            # 20011005193815
            if title == 'Bush mata a fome aos afegãos':
                snippet = 'Paquistão aceita provas contra Bin Laden'
                img_url = title_elem.find_next('img').get('src')

            # 20011006045305
            if title == 'Blair confirma apoio Paquistanês':
                snippet = 'Êxito: Primeiro-ministro inglês marca pontos'
                img_url = title_elem.find_next('img').get('src')

            # 20011007040629
            if title == 'Pão-de-ló Margaride adoça o país':
                category = 'Local'
            elif title == 'Bragança aposta no turismo com construção do Millenium Park' or 'Taliban escolhem prisioneiros como escudos humanos' or 'Rochas da Foz classificadas como património natural do Porto':
                snippet = None
            elif title == 'Apoteose':
                category = 'Desporto'

            all_news.append({
                'article_url': title_elem.get('href') + generate_destaques_uniqueness(category, title, snippet),  # got titles back since at this period they seem to be archived
                'title': title,
                'snippet': snippet,
                'category': clean_special_chars(category),
                'img_url': img_url,
                'headline': headline,
                'importance': Importance.FEATURE if img_url else define_importance(title_elem)
            })

        return all_news


class ScraperJornalDeNoticias04(NewsScraper):
    source = 'jn.pt'
    cutoff = 20011008092650

    # This issue was different

    def scrape_page(self, soup):
        all_news = []

        # main title manually
        all_news.append({
            'article_url': 'https://arquivo.pt/noFrame/replay/20011008092650/http://www.jn.pt:80/atentado/',
            'title': '...começou',
            'snippet': '50 mísseis "tomahawk" e bombas guiadas de alta precisão foram lançadas a partir aviões e barcos contra alvos em Cabul, Kandahar, Mazar-e-Sharif, Farah e Kunduz',
            'category': 'Em foco',
            'img_url': 'https://arquivo.pt/noFrame/replay/20011008075350mp_/http://jn.pt:80/Foto1.jpg',
            'importance': Importance.FEATURE
        })

        # the others
        titles = soup.find_all('a', id='titulos')
        for title_elem in titles:
            headline_elem = title_elem.find('font', attrs={'color': '#FF0000'})
            title = headline_elem.find_next('font', attrs={'color': '#000000'}).get_text()

            all_news.append({
                'article_url': title_elem.get('href') + generate_destaques_uniqueness('parser04/Em foco', title, headline_elem.get_text()),
                'headline': remove_clutter(headline_elem.get_text()),
                'title': remove_clutter(title),
                'category': 'Em foco',
                'importance': Importance.SMALL
            })

        return all_news


class ScraperJornalDeNoticias05(NewsScraper):
    source = 'jn.pt'
    cutoff = 20011217220519

    snippets = {
        'Guerra está para durar': 'Bombas: Nova vaga de ataques a Cabul e outras cidades',
        'Taliban perdem o céu': 'Liga Árabe: Cimeira do Qatar tenta evitar que a guerra atinja país irmão',
        'Mundo tem mais medo 30 dias depois da tragédia': 'Países islâmicos: Cimeira do Qatar abstém-se de condenar contra-ataque',  # 20011011060710
        'Salários congelados em 2002': 'Governo também propõe no Orçamento de Estado; alterações na tributação das mais-valias da Bolsa',
        'Vírus põem americanos em alerta': 'Receio: Quarto caso de Antraz agora em Nova Iorque',
        'Portugal Fashion em Paris': None,
        'Santana Lopes': '"Espero que Durão Barroso afirme a sua liderança e ganhe as próximas legislativas" "O meu caminho é este: candidatar-me a Lisboa e ser presidente da Câmara"',
        'Antraz espalha o medo': 'Alarme em Lisboa numa oficina de automóveis quando mexeram numa peça encaixotada coberta de pó branco',
        'Boavista ainda firme': ' Derrota com o Borussia de Dortmund (2-1), na Alemanha, teve sabor amargo, mas não rouba a esperança do campeão português. F.C. Porto, hoje (RTP, 19.45 horas), obrigado a vencer para manter o sonho da passagem à segunda fase da Liga dos Campeões',
        'Forças especiais em solo afegão': 'Kandahar: Contra-ataque poderá ter chegado por terra',
        'Paquistaneses avisam governo': 'Paquistão: Classe média contra apoio dos americanos',
        'Bush ganha aliado chinês': 'Xangai: Jiang Zemin apoia ataques para poder silenciar separatistas de Xinjiang',  # 20011020021003
        'Rangers atacam, destroem e fogem de solo afegão': 'Baixas: Queda de helicóptero no Paquistão vitima dois militares norte-americanos',
        'Helicópteros sobre Cabul': 'Ataques: Cidades afegãs à mercê dos "helis" dos EUA',
        'Mau tempo maus presságios': 'Chuvas torrencias alagaram regiões do Norte e Centro. Indeminizações do último Inverno ainda estão por pagar',
        'F. C. Porto entregue a si mesmo frente ao Rosenborg nas Antas': 'Juventos 3 F.C. Porto 1',
        'Irmãos Portas decidem Lisboa': 'João Soares com escassa vantagem sobre Santana. Líder do CDS/PP poderá assegurar maioria de Direita',  # 20011025024821
        '18 dias de bombardeamentos': 'EUA reconhecem ser quase impossível capturar Bin Laden',
        'PS admite ceder na taxa de álcool': 'Socialistas aceitam discutir a relação entre as bebidas alcoólicas e a sinistralidade',
        'Pausa escolar aflige os pais': 'Uma semana sem aulas deixa os alunos entregues a si mesmos e ao deus-dará',
        'Fragilidade paquistanesa aumenta e assusta Estados Unidos': 'Nuclear: Secretas ocidentais tentam neutralizar arsenal na mira de Bin Laden',
        'Ministério da Justiça devolve milhões de contos a empresas': None,
        'Coimbra: Mulher de Machado faz declaração pública de amor': None,
        'Lar ilegal mata idosos em Cascais': ' Perderam a vida seis pessoas. Candeeiro junto à cama provoca tragédia',  # 20011102001415
        'Americanos temem destruição de pontes': 'Golden Gate: Governador da Calofórnia admite ataque terrorista, até quarta-feira',
        'Moda brilha no Porto': None,
        'Governo mantém aposta no Douro': 'Navegabilidade do rio recebe cinco milhões em 2002. Molhes da Foz e canal junto ao Tua são as prioridades',
        'Ligeira vantagem comunista no Barreiro': 'CDU 38,2%; PS 36,0%; PSD 10,4%; CDS/PP 2,1%; BE 1,9%',
        'Deputados contra ataques ao Parlamento': 'Presidente da Assembleia vai responder às acusações de Marcelo Rebelo de Sousa',
        'CGTP luta na rua por melhores salários': None,
        'Juros baixam 0,5% para relançar a economia na zona euro': None,
        'Orçamento provoca crise nos sociais-democratas': None,  # 20011110013045
        'Um cálice do Porto de Siza Vieira': None,
        'EUA travam a entrada em Cabul': 'Novos avanços da Aliança do Norte dependem de compromissos políticos',
        'Cidade mártir': 'Nova Iorque: Queda de avião agrava sentimento de insegurança',
        'Metro do Porto cresce com mais 50 milhões': 'Banco Europeu de Investimentos financia extensões a Gondomar e aeroporto',
        'NTV inicia hoje, às 19 horas, as suas emissões regulares': None,
        'Tribos afegãs tentam evitar guerra civil': 'Na frente: Reporter JN acompanha tomada de Jalalabade',
        'Descida do preço do petróleo torna gás natural ainda mais barato': None,
        'Taliban Resiste': 'Sobrevivência: Regime liderado por mullah Omar, entrincheirado no Sul do Afeganistão, tenta manter o Poder',
        'Guerra trava ópio e dispara droga sintética': 'Bombardeamentos ao Afeganistão estão a destruir plantações do maior produtor mundial de heroína',
        'Mais 90 milhões na Linha do Norte': 'Presidente da REFER garante conclusão das obras na ligação Porto-Lisboa e Lisboa-Algarve até 2004',
        'Anorexia também atinge os homens': 'Doença não é uma mania social e pode levar à morte. Mais de 70% dos jovens portugueses no grupo de risco',
        'Tensão nas cadeias provoca mudanças nas direcções': None,
        'Expresso do Oriente ligará Lisboa-Porto-Douro-Madrid': None,  # 20011124022311
        'Brinquedos causam oito acidentes por dia em Portugal': None,
        'Suíça já não é um paraíso': 'Mais um acidente junta-se à crise económica e social que abala o país',
        'Desembarque americano no Afeganistão': 'Brigada de marines cerca reduto de Kandahar, a última linha de defesa de Osama bin Laden e do mullah Omar',
        'Optimismo em Cabul': 'Cimeira inter-afegã conclui até ao fim da semana elenco do novo Governo',
        'ONU denuncia uma epidemia incontrolada de SIDA em Portugal': None,
        'Pescas portuguesas desperdiçam meio milhão de contos': None,
        'Portugal vai hoje às sortes': 'Sorterio do Mundial de 2002 realiza-se na Coreia do Sul. Selecção portuguesa é 8ª no ranking das apostas',
        'Barriga a mais e sexo a menos': 'Complexos dos portugueses também chegam ao nariz',
        'Vinte bebés por dia nascem de mães ainda adolescentes': None,
        'Indesejável': 'Israel e EUA querem substituir Arafat por outro líder palestiniano',
        'Sampaio pessimista com 2002': 'Discurso no fim do ano lançará repto ao Governo e à Oposição para que as reformas avancem',
        'Testes da sida pouco fiáveis': 'Comissão Nacional propõe concentração de exames em apenas sete laboratórios',
        'Pedofilia': 'Portugal incapaz de dar combate ao crime na Net',
        'Carros alternativos chegam a Portugal': 'Utilitário a ar comprimido à venda no próximo ano. Autocarros do Porto serão movidos a pilha de hidrogénio. Optimismo europeu admite fim dos poluentes em 2010',
        'Seguros recusam cobrir terrorismo e vandalismo': 'Contratos para acautelar estes riscos só mediante um forte aumento dos prémios',  # 20011211023137
        'Maioria absoluta provável no Porto': 'Fernando Gomes 43,5%; Rui Rio 34,2%; Rui Sá 8,4%; Teixeira Lopes 2,3%',
        'Milhares de fraudes na Vila Verde': 'Portugueses usam cada vez mais esquemas para não pagar portagens',
        'Portugal chumba emigração para Angola': 'Governo cria fundo de ajuda a emigrantes em dificuldades nos países de acolhimento',
        'Obviamente, demite-se.': None
    }

    def scrape_page(self, soup):
        all_news = []

        titles = soup.find_all('a', attrs={'href': re.compile(r'.*/textos/textho[0-9]\.asp')})
        titles = [t for t in titles if remove_clutter(t.get_text())]

        for i in range(len(titles)):
            title_elem = titles[i]

            title = remove_clutter(title_elem.get_text())
            if title.startswith('Entrevistas JN'):
                continue  # 20011029044844

            headline = None
            img_url = None
            url = title_elem.get('href')

            ## CATEGORY ##
            category_elem = title_elem.find_previous('a', id='normal')
            if title in ['NTV inicia hoje, às 19 horas, as suas emissões regulares', 'NTV estreia com demissão do subdirector']:
                # 20011115015809, 20011116044355, element didn't have id
                category = 'Televisão'
            elif title == 'Obviamente, demite-se.':
                category = 'Política'
            else:
                category = clean_special_chars(category_elem.get_text())

            # retry
            if not category:
                category_elem = category_elem.find_previous('a', id='normal')
                category = clean_special_chars(category_elem.get_text())

            ## TREAT FEATURE AND SMALLER DIFFERENTLY ##
            if not url.endswith('textho1.asp'):
                # snippet must be between this title and the next
                snippet = find_snippet(title_elem, titles[i+1] if len(titles) > i+1 else None, title)

                # 20011011060710
                if title == 'Nada perdido':
                    img_url = title_elem.find_previous('img').get('src')

                # 20011012101917
                if title == 'Com medo das armas':
                    snippet = 'Fuga: Paquistaneses apoiantes dos taliban fogem do Afeganistão'
                    img_url = title_elem.find_previous('img').get('src')

                # 20011014115702
                if title == 'Mulheres afegãs oprimidas':
                    snippet = 'Mais Guerra: Estados Unidos voltam a atacar o Sul do Iraque'
                    img_url = title_elem.find_next('img').get('src')

                # 20011015003014
                if title == 'À espera de Powell':
                    snippet = 'Paquistão: Presidente Musharraf apresenta factura à diplomacia dos EUA'
                    img_url = title_elem.find_previous('img').get('src')

                # 20011017003532
                if title == 'Índia ataca território paquistanês':
                    snippet = 'Conflito: Caxemira agrava tensões entre Nova Deli e Islamabade'
                    img_url = title_elem.find_next('img').get('src')

                # 20011018132546
                if title == 'Grande gala':
                    img_url = title_elem.find_next('img').get('src')
                elif title == 'Manuel Martins pode obter terceiro mandato em Vila Real':
                    category = 'Política'

                # 20011021034814
                if title == 'Bastidores Marcianos de Júlia Pinheiro':
                    category = 'Cultura'
                elif title == 'Violações Trolha responde por abuso de 30 menores':
                    headline = 'Violações'
                    title = 'Trolha responde por abuso de 30 menores'
                elif title == 'Azul, mas de Belém':
                    # was graphics-dependent
                    snippet = 'F.C. Porto 1 Belenenses 2; Benfica 2 Gil Vicente 0; Boavista 3 Braga 0'

                # 20011022031502
                if title == 'Está de novo em causa o direito à informação':
                    headline = 'Entrevista Luís Sepúlveda'

                # 20011023013638
                if title == 'EUA erram de novo e atacam posições da Aliança do Norte':
                    category = 'Em foco'
                    snippet = 'Afeganistão: Al-Jazeera mostra imagens de peças de héli abatido'
                    img_url = title_elem.find_next('img').get('src')  # two images today!

                # 20011024021219
                if title == 'Refugiados na fronteira do desespero':
                    snippet = 'Afegãos: Fome e Inverno vão matar mais do que as bombas'
                    img_url = title_elem.find_next('img').get('src')

                # 20011025024821
                if title == 'Iminente ofensiva conjunta contra taliban':
                    snippet = 'Afeganistão: Aliança do Norte e EUA concertam estratégia'
                    img_url = title_elem.find_previous('img').get('src')

                # 20011027034705
                if title == 'Taliban executam general da Aliança Norte':
                    snippet = 'Invasão: Governo inglês disponibiliza mais três mil soldados para o combate'

                # 20011028042503
                if title == 'Cabul está a arder':
                    snippet = 'Tesouros: Afegãos desfazem-se de antiguidades e trocam ouro por burros'
                    img_url = title_elem.find_next('img').get('src')

                # 20011029044844
                if title == 'Cristãos massacrados no Paquistão':
                    snippet = 'Extremismo: Seis homens armados invadiram igreja católica e mataram 18 fiéis'
                    img_url = title_elem.find_next('img').get('src')

                # 20011030023220
                if title == '"Quero mais 1500 agentes da PSP nas ruas da cidade"':
                    headline = 'Paulo Portas, candidato em Lisboa'

                # 20011031120132
                if title == 'Que rico Boavista!':
                    img_url = title_elem.find_next('img').get('src')
                elif title == 'Confiança a descer':
                    # just to add the :
                    snippet = 'Sondagens: Norte-americanos e britânicos mostram cansaço quanto à forma do contra-ataque no Afeganistão Pela Paz Manifestações contra a guerra chegam a Lisboa'

                # 20011101121357
                if title == 'Dragões milionários':
                    img_url = title_elem.find_next('img').get('src')
                elif title == 'FBI teme sabotagem nuclear':
                    # just to add the :
                    snippet = 'Prevenção: EUA procuram seis comandos que poderão atacar central atómica'

                # 20011102001415
                if title == 'Nações Unidas pedem o fim da guerra no Afeganistão':
                    snippet = 'Discordância: Kofi Annan contraria norte-americanos indisponíveis para qualquer trégua'

                # 20011103013410
                if title == 'Portugal Fashion antecipa o Verão':
                    img_url = title_elem.find_next('img').get('src')
                elif title == '"Prefiro fazer as pessoas chorar"':
                    headline = 'Entrevista Lydia Lunch'

                # 20011104022419
                if title == 'Droga de infância':
                    img_url = title_elem.find_next('img').get('src')

                # 20011105004557
                if title == 'Na frente':
                    img_url = title_elem.find_previous('img').get('src')
                elif title == 'Itália junta-se ao esforço de guerra':
                    snippet = 'Bombas: Aviões americanos fazem 350 baixas'

                # 20011106020050
                if title == 'Ofendido':
                    headline = 'Sampaio e a Lei de Programação Militar'
                    snippet = '"Não pratiquei qualquer inconstitucionalidade"'
                elif title == 'Taliban pedem ajuda à ONU':
                    img_url = title_elem.find_previous('img').get('src')
                    snippet = 'Vítimas: Embaixador do Paquistão fala em tragédia humanitária'

                # 20011107013212
                if title == 'Cem feridos em Madrid':
                    img_url = title_elem.find_next('img').get('src')
                elif title == 'Bush teme que Bin Laden consiga armas nucleares':
                    snippet = None

                # 20011108011523
                if title == 'O regresso do Concorde':
                    img_url = title_elem.find_next('img').get('src')
                elif title == 'PS e CDU à beira do empate técnico em Setúbal':
                    snippet = 'PS 30,4%; CDU 28,3%; PSD/CDS/PP 21,3%; Cidadãos por Setúbal 3,1%;BE 2,9%; MPT 0,2%'

                # 20011109023920
                if title == 'Guerra já queimou 225 milhões de contos':
                    img_url = title_elem.find_previous('img').get('src')
                    snippet = 'Ramadão: Presidente do Paquistão não consegue tréguas no mês sagrado'

                # 20011110013045
                if title == 'Taliban perdem cidade estratégica':
                    img_url = title_elem.find_previous('img').get('src')
                    snippet = 'Violência: Vaga de manifestações causa mortos e feridos em várias cidades do Paquistão'

                # 20011111013554
                if title == 'Guerra divide Europa':
                    img_url = title_elem.find_next('img').get('src')
                    snippet = '43,9% dos inquiridos admitem que ofensiva abriu brechas na coesão europeia. 65,3% dos portugueses defendem que a guerra é solução contra terrorismo'
                elif title == 'S. João de Deus envergonha cidade do Porto':
                    snippet = 'Degradação extrema desumaniza o bairro e constitui um estigma para os moradores'
                elif title == 'Novo Rossio desagrada às floristas':
                    snippet = None

                # 20011112023025
                if title == 'Argélia está num caos':
                    img_url = title_elem.find_next('img').get('src')
                    snippet = None
                elif title == '"Maioria da Câmara de Lisboa deve ser de esquerda"':
                    headline = 'Miguel Portas'
                    snippet = None
                elif title == '"Há novelas antigas melhores que as actuais"':
                    headline = 'Nicolau Breyner'
                    snippet = None
                elif title == '"Deixar de cantar em português é uma vergonha"':
                    headline = 'Vitorino'
                    snippet = None

                # 20011114005313
                if title == 'Vida nova em Cabul':
                    img_url = title_elem.find_next('img').get('src')
                elif title == 'Assinatura fantasma de Duarte Lima no Parlamento':
                    snippet = None
                elif title == 'NTV arranca amanhã e Carlos Magno confia no êxito':
                    category = 'Televisão'

                # 20011115015809
                if title == 'As vozes da ira':
                    img_url = title_elem.find_previous('img').get('src')
                elif title == 'ONU marca conferência internacional sobre futuro dos afegãos':
                    snippet = 'Terrorismo: Bush determina que os suspeitos sejam julgados em tribunal militar sem recurso'

                # 20011117192155
                if title == 'Líder dos taliban admite rendição':
                    img_url = title_elem.find_next('img').get('src')
                    snippet = 'Desespero: Mullah Omar negoceia fuga para as montanhas'

                # 20011118042355
                if title == 'Mulheres desprotegidas':
                    img_url = title_elem.find_previous('img').get('src')

                # 20011119193959
                if title == 'Um avanço para o passado':
                    img_url = title_elem.find_next('img').get('src')
                elif title == '"Não há clima para negociar salários na TAP"':
                    headline = 'Fernando Pinto'
                elif title == '"Não sei fazer outra coisa que não seja cantar fado"':
                    headline = 'Camané'
                elif title == '"Panathinaikos não é uma equipa de ataque"':
                    headline = 'Paulo Sousa'

                # 20011121020005
                if title == 'Sem brilho, mas eficaz':
                    img_url = title_elem.find_previous('img').get('src')
                elif title == 'Mulheres afegãs reclamam trabalho':
                    snippet = None

                # 20011122002949
                if title == 'Jogar para os pontos':
                    img_url = title_elem.find_next('img').get('src')
                elif title == 'Socialistas à beira de perder Faro':
                    snippet = 'PS 34,9%; PSD  34,5%; CDU 9,4%; PP/PPM 3,1%; BE 3,1%'
                elif title == 'Crianças agonizam no hospital pediátrico da capital afegã':
                    snippet = 'Dificuldade: George W. Bush avisa que o pior será desmantelar al-Qaeda'

                # 20011123035127
                if title == 'GNR falida':
                    img_url = title_elem.find_next('img').get('src')
                    snippet = 'Falta dinheiro para gasolina, gás, água e luz. Circular do Ministério convida militares a andar a pé. Governo nega e fala em contenção.'  # just to add the periods
                elif title == 'El Corte Inglés abre hoje':
                    snippet = 'Inauguração oficial, ontem à noite, contou com convidados de luxo'

                # 20011124022311
                if title == '6':
                    continue
                elif title == 'portugueses assassinados em Angola':
                    title = '6 portugueses assassinados em Angola'
                elif title == 'Taliban resistem às portas da capital':
                    snippet = 'Sucessão: Mullah Omar indica o próximo chefe'
                elif title == 'Loucura no El Corte Inglés':
                    img_url = title_elem.find_previous('img').get('src')
                elif title == '"Espero mais acção do ministro Júlio Pedrosa"':
                    headline = 'Isabel Alarcão'

                # 20011125173410
                if title == 'Dalai Lama atrai notaveis do Porto':
                    img_url = title_elem.find_next('img').get('src')
                    category = 'Destaque'
                elif title == 'Taliban entregam cidade de Kunduz':
                    snippet = None
                elif title == 'Benfica ganha em Braga cinco anos depois':
                    snippet = 'Golo de Mantorras desequilibra um jogo talhado para o 0-0'

                # 20011126233312
                if title == 'Outro galo cantou':
                    img_url = title_elem.find_next('img').get('src')
                    snippet = None
                elif title == 'Aveiro continua socialista':
                    snippet = 'PS 37,2%; PSD 21,5%; CDS/PP 21,0%; CDU 4,1%'
                    category = 'Política'
                elif title == 'Falta de dinheiro paralisa Marinha':
                    category = 'Política'

                # 20011128005818
                if title in ['Sport TV bate recorde no cabo', 'Canal Disney em português 24 horas por dia a partir de hoje', 'Documentário sobre a Guerra Colonial no Canal História']:
                    category = 'Televisão'
                elif title == 'Duarte Silva vence na Figueira':
                    snippet = 'PSD 40,8%; PS 34,5%; CDS/PP 6,1%; CDU 4,1%'

                # 20011129001728
                if title == 'Taxa de alcoolémia PS desautoriza secretário de Estado':
                    headline = 'Taxa de alcoolémia'
                    title = 'PS desautoriza secretário de Estado'
                elif title == 'O filme que voa':
                    img_url = title_elem.find_next('img').get('src')
                    snippet = '"Harry Potter" estreia amanhã em número recorde de salas de cinema'

                # 20011130085524
                if title == 'Remédios os preços sobem amanhã':
                    title = 'Remédios: os preços sobem amanhã'
                elif title == 'Também se faz cá ski':
                    img_url = title_elem.find_next('img').get('src')
                elif title == 'Carlos Encarnação à frente em Coimbra':
                    snippet = 'PS 33,9%; CDU 8,5%; BE 1,1%; PH 0,3%; PCTP/MRPP 0,2%'

                # 20011201161904
                if title == 'Só restam dois':
                    img_url = title_elem.find_next('img').get('src')

                # 20011202073533
                if title == 'Metro já andou em Matosinhos':
                    img_url = title_elem.find_next('img').get('src')

                # 20011203193058
                if title == 'Guerra aberta ameaça Médio Oriente':
                    img_url = title_elem.find_next('img').get('src')
                    snippet = 'Atentados: Quatro ataques extremistas em 12 horas causam 30 mortos e 200 feridos'
                elif title == 'Fernando Ruas com larga vantagem em Viseu':
                    snippet = 'PSD 53,3%; PS 26,0%; CDS/PP 5,0%; CDU 2,9%; BE 1,4%; PH 0,2%'

                # 20011208084647
                if title == '"Portugal tem de mudar de vida"':
                    headline = 'Sousa Franco'
                    img_url = title_elem.find_next('img').get('src')

                # 20011209105956
                if title == 'Grandes mas pouco':
                    img_url = title_elem.find_next('img').get('src')

                # 20011210053533
                if title == 'Sporting isolado na frente':
                    img_url = title_elem.find_previous('img').get('src')

                # 20011211023137
                if title == 'Alto Douro e Guimarães à espera da classificação da UNESCO':
                    img_url = title_elem.find_next('img').get('src')

                # 20011215051255
                if title == 'Douro Vinhateiro uma jóia da Humanidade':
                    title = 'Douro Vinhateiro: uma jóia da Humanidade'
                    img_url = title_elem.find_next('img').get('src')
                elif title == '"Em Portugal há uma enorme incultura de arte"':
                    headline = 'Lima de Carvalho'

                # 20011216204711
                if title == 'Vitorino marca pontos na Europa':
                    snippet = 'Comissário português integra Convenção presidida por Giscard D\' Estaing'
            else:
                if title == 'Portugal incapaz de dar combate ao crime na Net':
                    continue  # 20011209105956, already processed at this point since 2 titles point to the same article

                img_url = title_elem.find_next('img').get('src')
                snippet = self.snippets[title]

                # at these days the picture didn't belong to the article / no picture
                if title in ['Mundo tem mais medo 30 dias depois da tragédia', 'Salários congelados em 2002',
                             'Portugal Fashion em Paris', 'Santana Lopes', 'Boavista ainda firme', 'Forças especiais em solo afegão',
                             'F. C. Porto entregue a si mesmo frente ao Rosenborg nas Antas', 'Irmãos Portas decidem Lisboa',
                             '18 dias de bombardeamentos', 'Pausa escolar aflige os pais', 'Coimbra: Mulher de Machado faz declaração pública de amor',
                             'Americanos temem destruição de pontes', 'Moda brilha no Porto', 'Governo mantém aposta no Douro',
                             'Ligeira vantagem comunista no Barreiro', 'Deputados contra ataques ao Parlamento', 'CGTP luta na rua por melhores salários',
                             'Juros baixam 0,5% para relançar a economia na zona euro', 'Orçamento provoca crise nos sociais-democratas',
                             'Um cálice do Porto de Siza Vieira', 'EUA travam a entrada em Cabul', 'Metro do Porto cresce com mais 50 milhões',
                             'NTV inicia hoje, às 19 horas, as suas emissões regulares', 'Taliban Resiste', 'Guerra trava ópio e dispara droga sintética',
                             'Mais 90 milhões na Linha do Norte', 'Anorexia também atinge os homens', 'Tensão nas cadeias provoca mudanças nas direcções',
                             'Expresso do Oriente ligará Lisboa-Porto-Douro-Madrid', 'Brinquedos causam oito acidentes por dia em Portugal',
                             'Suíça já não é um paraíso', 'Desembarque americano no Afeganistão', 'Optimismo em Cabul', 'ONU denuncia uma epidemia incontrolada de SIDA em Portugal',
                             'Pescas portuguesas desperdiçam meio milhão de contos', 'Portugal vai hoje às sortes', 'Barriga a mais e sexo a menos',
                             'Vinte bebés por dia nascem de mães ainda adolescentes', 'Indesejável', 'Sampaio pessimista com 2002',
                             'Testes da sida pouco fiáveis', 'Pedofilia', 'Carros alternativos chegam a Portugal', 'Seguros recusam cobrir terrorismo e vandalismo',
                             'Maioria absoluta provável no Porto', 'Milhares de fraudes na Vila Verde', 'Portugal chumba emigração para Angola']:
                    img_url = None

                if title in ['Forças especiais em solo afegão', 'Helicópteros sobre Cabul', 'Cidade mártir']:
                    category = 'Em foco'

                # these had the picture before
                if title in ['18 dias de bombardeamentos']:
                    img_url = title_elem.find_previous('img').get('src')

                # 20011217220519, img was a background
                if title == 'Obviamente, demite-se.':
                    img_url = 'Foto1.jpg'

            all_news.append({
                'article_url': title_elem.get('href') + generate_destaques_uniqueness('parser04/' + category, title, snippet),
                'title': title,
                'snippet': snippet,
                'category': category,
                'img_url': img_url,
                'headline': headline,
                'importance': Importance.FEATURE if url.endswith('textho1.asp') and snippet or img_url else Importance.SMALL
            })

        return all_news


def find_snippet(first, last, title):
    if not last:
        # if there's no more titles just find the next element
        snippet_elem = first.find_next('font', attrs={'size': '1', 'face': 'Arial'})
        if not snippet_elem:
            return None

        snippet = prettify_text(snippet_elem.get_text())
        return None if snippet_invalid(snippet_elem) else snippet
    else:
        # keep going until the limit element
        next = first
        while next and next != last:
            if isinstance(next, Tag) and next.name == 'font' and next.attrs.get('face') == 'Arial' and next.attrs.get('size') in ['1', '2'] and next.attrs.get('color') != '#800000':
                snippet = prettify_text(next.get_text())

                # the tag is empty (after cleanup), or it's the title_elem again? continue searching
                if next.get_text() and not snippet or snippet == title:
                    next = next.next
                    continue

                return None if snippet_invalid(next) else snippet
            else:
                next = next.next

        return None


def find_category(start):
    while True:
        # retry because of empty elements
        category_elem = start.find_previous('a', id='normal')
        category = clean_special_chars(category_elem.get_text())
        if category:
            return category

        start = category_elem


def find_headline(title, limit):
    # first elements shouldn't have a default headline
    if not limit:
        return

    # keep going until the limit element
    next = title
    while next and next != limit:
        if isinstance(next, Tag) and next.name == 'font' and next.attrs.get('face') == 'Arial' and next.attrs.get('size') == '1' and next.attrs.get('color') in ['#800000', '#FFAC00']:
            headline = remove_clutter(next.get_text())
            if not headline:
                next = next.previous  # try again
                continue

            return None if not headline else headline  # do this to ensure no '', better null than empty string
        else:
            next = next.previous

    return None


class ScraperJornalDeNoticias06(NewsScraper):
    source = 'jn.pt'
    cutoff = 20031008094205

    # New parser just to clean things up and try new approaches

    imgs = {
        # True for below, False for above
        'Acordo Rio-Amorim': False,  # 20020328105153
        'Encanto só depois do intervalo': False,
        'Magia africana leva ao tapete campeões do Mundo': True,
        'Hoje, a superpotência somos nós!': True,
        'Benfica e Simão sempre a somar': True,
        'Vítimas acusam Carlos Cruz': True,
        'Apagão deixou a Itália às escuras e lançou o caos': True
    }

    headline_ignores = ['Oliveira e Castro', 'Alfredo Leite', 'A. Oliveira e Castro e Júlio Roldão']

    def scrape_page(self, soup):
        all_news = []

        titles = soup.find_all('a', attrs={'href': re.compile(r'.*/textos/textho[0-9]\.asp')})
        titles = [t for t in titles if remove_clutter(t.get_text())]

        for i in range(len(titles)):
            title_elem = titles[i]

            title = remove_clutter(title_elem.get_text())
            url = title_elem.get('href')

            if title == '.':
                continue  # 20030407021054

            # category
            if title in ['Columbia não voltou', 'Raides aéreos abrem nova frente no Norte do Iraque', 'Americanos encerram Bagdade num anel de aço']:
                category = 'Destaque'  # 20030202030522, 20030325170958, 20030407021054
            elif title in ['Porto a três vitórias da festa do título']:
                category = 'Desporto'  # 20030407021054
            else:
                # category must be before the title
                category = find_category(title_elem)

            # snippet must be between this title and the next
            snippet = find_snippet(title_elem, titles[i+1] if len(titles) > i+1 else None, title)

            # check image
            img_url = None
            if title in self.imgs:
                img_url = title_elem.find_next('img').get('src') if self.imgs[title] else title_elem.find_previous('img').get('src')

            # check headline
            headline = find_headline(title_elem, titles[i-1] if i > 0 else None)
            if headline in self.headline_ignores:
                # don't catch reporter's names
                headline = None

            if title in ['III►', 'II►']:
                continue

            title = title.replace('III►', '').strip()

            # 20020526003603
            if title == 'Função Pública':
                headline = 'Função Pública'
                title = 'Agitação afecta 700 mil portugueses'
                snippet = 'Desemprego: Governo fala em 10 mil contratados a prazo e sindicatos em 50 mil'

            # 20020601081931
            if title == 'Magia africana leva ao tapete campeões do Mundo':
                title = 'Já não há respeito!'
                headline = 'França-Senegal'
                snippet = 'Magia africana leva ao tapete campeões do Mundo'
            elif title == 'Governo escorrega no Benfica':
                snippet = 'PS acusa Ferreira Leite de aceitar três milhões de acções da SAD'

            # 20020605120617
            if title == 'Hoje, a superpotência somos nós!':
                snippet = 'Portugal com tracção à frente: uma linha de cinco avançados contra os EUA, hoje, às 10 horas, com transmissão na RTP. Figo espera não sentir dores'

            # 20020927111734
            if title == 'Promessa de Durão confunde Nordeste':
                snippet = 'Os termos em que foi anunciado Ensino Universitário para Bragança causam perplexidade aos autarcas no Congresso de Trás-os-Montes'

            # 20020929144258
            if title == 'Interioridade':
                headline = 'Interioridade'
                title = 'Apelo de Jorge Sampaio: "É preciso ouvir todas as vozes do país"'

            # 20021124015559
            if title == 'Garrafas para Figo e zero golos':
                headline = 'Barcelona - Real Madrid'
            elif title == 'Portugal sem meios para vigiar petroleiros na costa':
                snippet = 'Dois navios por hora passam na nossa costa. Detectadas novas manchas na Galiza. Crise atinge pesca, hotelaria e comércio'
            elif title == 'Governo põe na gaveta plano de emergência':
                headline = 'Violência doméstica'
            elif title == '“Europeus só sabem adiar os problemas”':
                headline = 'Pacheco Pereira'

            # 20021130152758
            if title == 'Galiza entrou em alerta geral':
                headline = 'Maré negra avança para a costa da morte'

            # 20030202030522
            if title == 'Vítimas acusam Carlos Cruz':
                snippet = 'Após longo interrogatório, juiz decidiu manter preso o apresentador. Eram 6.30 horas quando Carlos Cruz foi levado, nesta viatura, para os calabouços da Polícia Judiciária, em Lisboa'
            elif title == 'Axadrezados acabam com ciclo positivo de Artur Jorge':
                snippet = 'Boavista 4 Académica 1'
            elif title == 'Alemanha e Croácia em final inédita':
                headline = 'Mundial de Andebol'
                snippet = None
            elif title == 'Oliveirense e PT disputam Taça da Liga':
                headline = 'Basquetebol'

            # 20030213181204
            if title == 'Iraque recebe mensagem de paz do Papa':
                snippet = 'Aliança Atlântica não chega a acordo'

            # 20030320114439
            if title == 'Expectativa nas últimas horas de paz':
                headline = 'Iraque'

            # 20030325170958
            if title == 'Raides aéreos abrem nova frente no Norte do Iraque':
                if i == 1:  # it repeated itself
                    continue
                snippet = 'Ataque de helicópteros contra forças de elite de Saddam antecipa confronto nas proximidades de Bagdade. Combates intensos e falta de água e de electricidade ameaçam criar catástrofe humanitária em Bassorá'
            elif title == 'Insegurança nas escolas aumentou em 2002':
                snippet = None
            elif title == 'Estatuetas para Nicole e "Chicago" em ano de guerra':
                headline = 'Oscars'
                category = 'Cultura'
                snippet = None
            elif title == 'Jorge Sampaio veta Rendimento Social de Inserção':
                snippet = None
            elif title == 'Informática vai vigiar fraudes na segurança social':
                snippet = None

            # 20030407021054
            if title == 'Americanos encerram Bagdade num anel de aço':
                snippet = None
            elif title == 'Lombas para obrigar a reduzir a velocidade são ilegais':
                snippet = None
            elif title == 'Imposto Sucessório acaba e baixam a sisa e contribuição autárquica':
                category = 'Economia'
            elif title == 'Músicos podem pôr Estado em tribunal':
                snippet = None
                category = 'Cultura'
            elif title == 'Só 1% dos precários não regressam à cadeia':
                category = 'Polícia'

            # 20030727033252
            if title == 'Pensão mínima igual ao salário mínimo':
                if i == 1:  # first pass has empty snippet
                    continue

            # 20030806223450
            if title == 'Jacarta Bomba faz dezenas de vítimas':
                headline = 'Jacarta'
                snippet = 'Explosão provocou graves ferimentos a um cidadão português'
            elif title == 'Juiz convoca reunião com advogados de defesa':
                headline = 'Casa Pia'

            # 20030928171742
            if title == 'O maior circo do Planeta êm Coimbra':
                snippet = 'Rolling Stones foram êxito absoluto'

            # 20031008094205
            if title == 'Estudantes não dão tréguas':
                if i == 2:
                    continue
            elif title == 'Indústria lucra com compra de submarinos':
                headline = '1300 milhões'
                snippet = None
            elif title == 'Investimento no transporte ferroviário':
                headline = '700 milhões'
            elif title == 'Prejuízos causados pelos incêndios só em edifícios':
                headline = '28 milhões'

            all_news.append({
                'article_url': title_elem.get('href') + generate_destaques_uniqueness('parser04/' + category, title, snippet),
                'headline': headline,
                'title': title,
                'snippet': snippet,
                'category': category,
                'img_url': img_url,
                'importance': Importance.FEATURE if url.endswith('textho1.asp') and snippet or img_url else Importance.SMALL
            })

        return all_news


class ScraperJornalDeNoticias07(NewsScraper):
    source = 'jn.pt'
    cutoff = 20040526224636
    used = False

    # Categories vanish at this point

    def scrape_page(self, soup):
        if self.used:
            return None

        all_news = []

        timestamp = 20031224223008
        all_news.append({
            'timestamp': timestamp,
            'headline': 'Embaraço',
            'title': 'Julgamento de Saddam no Iraque e pena de morte dividem opiniões',
            'snippet': 'Especialistas portugueses salientam fragilidades do sistema judicial iraquiano. Resistência muda de estratégia e insiste em atacar esquadras policiais',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Cinema português com futuro comprometido',
            'snippet': 'Produtores e realizadores temem “ano de deserto” em 2004 devido a atraso da nova lei',
            'category': 'Cultura',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Aborto senta 17 no tribunal',
            'snippet': 'Adeptos da descriminalização manifestam-se',
            'category': 'Portugal',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Cruz telefonou aos amigos',
            'snippet': 'Almoço de solidariedade juntou mais de 120',
            'category': 'Portugal',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Zidane é de novo o melhor do Mundo',
            'snippet': 'Jogo contra a fome deu um milhão de euros',
            'category': 'Desporto',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Nove árbitros vetam Vitória de Guimarães',
            'category': 'Desporto',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Genéricos já fizeram Estado poupar 29 milhões',
            'category': 'Saúde',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Ingleses são quem compra mais empresas portuguesas',
            'category': 'Economia',
            'importance': Importance.SMALL
        })

        timestamp = 20031224223008
        all_news.append({
            'timestamp': timestamp,
            'title': 'Natal em português',
            'snippet': 'Saudade: Militares do Iraque, Bósnia e Timor celebram quadra a rigor',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Sequestrados de Belmonte encontram a família um ano depois',
            'snippet': 'Tribunal da Covilhã decreta prisão para um dos suspeitos de rapto',
            'category': 'Portugal',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Roquete contra hotel em Bagdade',
            'snippet': 'Saddam enganado por fiéis sobre posse de armas químicas',
            'category': 'Mundo',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Enfermeira condenada por aborto recebe perdão',
            'snippet': 'Presidente da República reduziu pena de Maria do Céu de sete anos e meio para metade',
            'category': 'Portugal',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Pedro Abrunhosa: “Estamos cheios de falsas pop stars”',
            'snippet': 'Abrunhosa fala ao JN no dia em que é estrela da MTV',
            'category': 'Cultura',
            'importance': Importance.SMALL
        })

        timestamp = 20040304114511
        all_news.append({
            'timestamp': timestamp,
            'title': 'Acabou o segredo no processo Casa Pia',
            'snippet': 'Juiz abriu instrução e as diligências serão concluídas até ao final deste mês. Recusadas audições para memória futura pedidas pela defesa de Silvino',
            'headline': 'Pedofilia',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Maioria recusou alterar a lei do aborto',
            'snippet': 'Forte divisão no PS e disciplina imposta no PSD, que diz aceitar novo referendo em 2006',
            'headline': 'Parlamento',
            'category': 'Portugal',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Kerry será o rival de Bush',
            'snippet': 'Vitória demolidora nas eleições primárias',
            'headline': 'Estados Unidos',
            'category': 'Mundo',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Exames nacionais estão de volta',
            'snippet': 'Garantidos no 9º ano e quase certos nos 6º e 4º',
            'headline': 'Educação',
            'category': 'Educação',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Moreira apura Benfica',
            'snippet': '“Oitavos” da UEFA são sorteados hoje',
            'category': 'Desporto',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Mobiliário com design a preço de saldo na feira ‘Stock off’',
            'category': 'Local',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Portugueses são os europeus que trabalham até mais tarde',
            'category': 'Portugal',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Areeiros investigados por suspeita de corrupção',
            'headline': 'Entre-os-Rios',
            'category': 'Portugal',
            'importance': Importance.SMALL
        })

        timestamp = 20040322011306
        all_news.append({
            'timestamp': timestamp,
            'title': 'Assassínio incendeia o mundo árabe',
            'snippet': 'Mísseis israelitas mataram o líder do Hamas e mais sete pessoas à saída de uma mesquita em Gaza. Seguidores de Yassin prometem levar a morte a todas as cidades de Israel. Al-Qaeda pede mobilização geral',
            'headline': 'Alta tensão',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Mais quatro suspeitos presos em Espanha',
            'category': 'Mundo',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Petróleo a arder contra ingleses no Iraque',
            'headline': '13 feridos em Bassorá',
            'category': 'Mundo',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Mil perdem emprego na Delphi',
            'snippet': 'Fábrica do Linhó (Sintra) vai encerrar até ao final do ano',
            'headline': 'Trabalho',
            'category': 'Economia',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Portas quer atrair jovens para a tropa',
            'snippet': 'Serão aliciados no Rock in Rio, Euro 2004 e Volta a Portugal',
            'headline': 'Defesa',
            'category': 'Portugal',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Mourinho convoca César Peixoto',
            'snippet': '“Empate com o Lyon será bom resultado”',
            'category': 'Desporto',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Governo apoia trabalho parcial para dar mais tempo à família',
            'category': 'Portugal',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'PJ desmantela rede de tráfico de drogas sintéticas',
            'category': 'Portugal',
            'importance': Importance.SMALL
        })

        timestamp = 20040327101840
        all_news.append({
            'timestamp': timestamp,
            'title': 'Crime aumenta em todo o país',
            'snippet': 'Só Coimbra, Setúbal e Madeira registaram menor número de queixas. Assinalados em 2003 mais de 234 mil crimes contra o património. Ministro continua a considerar Portugal um dos países mais seguros. Em 2003, a criminalidade em Portugal aumentou em todas as áreas, fixando-se os crimes participados às forças policiais em mais 6% do que em 2002, o que corresponde a uma subida superior a 23.500 crimes entre os dois anos em causa',
            'headline': 'Insegurança',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Celeste Cardona diz que decisão de Entre-os-Rios "será repensada"',
            'category': 'Portugal',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Grupo armado de assaltantes responde a tiro e foge à GNR',
            'category': 'Portugal',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': ' Baía continua fora da lista de Scolari',
            'snippet': 'Postiga convocado para jogo com a Itália',
            'category': 'Desporto',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'VCI será cortada de madrugada para colocação de viaduto',
            'headline': 'Porto',
            'category': 'Local',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Acidente com camião de gás provocou caos no trânsito',
            'headline': 'Gaia',
            'category': 'Portugal',
            'importance': Importance.SMALL
        })

        timestamp = 20040506181136
        all_news.append({
            'timestamp': timestamp,
            'title': ' Novas fotos de sevícias a prisioneiros chocam o Mundo',
            'headline': 'Iraque',
            'category': 'Destaque',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Americanos lançam ofensiva em Najaf para capturar Moqtada Sadr',
            'category': 'Mundo',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Magistratura abre inquérito a juízes da Liga',
            'headline': 'Apito dourado',
            'category': 'Desporto',
            'importance': Importance.LARGE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Choque petrolífero iminente agrava situação económica',
            'category': 'Economia',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Multas mais pesadas e pagas na hora',
            'headline': 'Código da estrada',
            'category': 'Portugal',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': '"Para mim, nunca foi fácil pintar"',
            'headline': 'Júlio Pomar',
            'category': 'Cultura',
            'importance': Importance.SMALL
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'Governo aprova associativismo na Guarda Republicana',
            'category': 'Portugal',
            'importance': Importance.SMALL
        })

        timestamp = 20040526224636
        all_news.append({
            'timestamp': timestamp,
            'title': 'F.C. Porto volta a ser campeão europeu',
            'snippet': 'Festa espalhou-se por todo o país e estendeu-se às comunidades portuguesas. Até no Mónaco houve adeptos a celebrar a vitória do F.C. Porto',
            'headline': 'Amar Azul',
            'img_url': 'foto1.jpg',
            'category': 'Desporto',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'timestamp': timestamp,
            'title': 'José Mourinho assume pela primeira vez desejo de sair para o Chelsea',
            'snippet': '“Quero muito aceitar o convite do clube de Londres”',
            'category': 'Desporto',
            'importance': Importance.LARGE
        })

        # add deterministic no url flag (deterministic because it's used as key)
        for news in all_news:
            if 'article_url' not in news:
                news['article_url'] = generate_dummy_url(self.source, news['timestamp'], news['category'], news['title'])

        self.used = True
        return all_news


def get_snippet_navigable_strings(element):
    snippet = element.find_all(string=lambda text: isinstance(text, NavigableString), recursive=False)
    snippet = '. '.join([p for p in snippet if not isinstance(p, Comment) and len(p) > 5])

    # cleanup
    m = re.match(r'^\s*\-\s+(.*)$', snippet)
    if m:
        snippet = m.groups(1)[0]

    return snippet.strip()


class ScraperJornalDeNoticias08(NewsScraper):
    source = 'jn.pt'
    cutoff = 20080314182313

    # Design radically changes

    categories = {
        'pais': 'Portugal',
        'desporto': 'Desporto',
        'economia': 'Economia'
    }

    def scrape_page(self, soup):
        all_news = []

        # in the browser the content is in two tables, and they should be between the only ones between comments 'tabela_conteudo' and '/tabela_conteudo'
        # however, in the parser only the first table can be found that way (the browser "fixes" it)
        # we thus find the second table by looking for the parent of comment 'caixa_esquerda_pais'

        features_marker = find_comments(soup, 'tabela_destaque_1_noticia')[0]
        feature_table = features_marker.find_parent('table')

        categories_marker = find_comments(soup, 'caixa_esquerda_pais')[0]
        categories_table = categories_marker.find_parent('table')

        ##### FEATURES #####
        # get more specific td instead of table
        features_marker = find_comments(feature_table, 'tabela_destaque_1_noticia')[0]

        big_features = features_marker.find_parent('td').find_all('a', class_='arial_18_preto')
        for title_elem in big_features:
            img_elem = title_elem.find_parent('td').find_previous('img')
            img = None
            if img_elem and not img_elem.get('src').endswith('.gif'):
                img = img_elem.get('src')

            snippet_elem = title_elem.find_next('span', class_='arial_12_preto')
            snippet = get_snippet_navigable_strings(snippet_elem)

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': remove_clutter(title_elem.get_text()),
                'snippet': prettify_text(snippet),
                'img_url': img,
                'category': 'Destaque',
                'importance': Importance.FEATURE
            })

        # find smaller features
        start_marker = find_comments(soup, 'tabela_central_leads1')[0]
        end_marker = find_comments(soup, '/tabela_central_leads1')[0]

        features = [a for a in feature_table.find_all('td', class_='arial_12_preto') if is_between(start_marker, end_marker, a)]
        for elem in features:
            title_elem = elem.find('a')
            snippet = get_snippet_navigable_strings(elem)

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': remove_clutter(title_elem.get_text()),
                'snippet': prettify_text(snippet),
                'category': 'Destaque',
                'importance': Importance.LARGE
            })

        ##### CATEGORIES #####
        category_markers = find_comments_regex(categories_table, r'^caixa_(?:esquerda|direita|fundo)_.*_(?:leads|conteudo)(?:_estrutura_dentro)?$')
        for marker in category_markers:
            a = re.match( r'^caixa_(?:esquerda|direita|fundo)_(.*)_(?:leads|conteudo)', marker)
            category = self.categories[a.groups(1)[0]]

            end = find_comments(soup, '/' + marker)[0]

            article_elems = categories_table.find_all('a', class_=re.compile(r'(arial_12_azul_bold|arial_11_preto)'))
            article_elems = [a.find_parent('td') for a in article_elems if is_between(marker, end, a)]

            # different structure for some categories
            article_elems2 = categories_table.find_all('td', class_=re.compile(r'(arial_12_preto)'))
            article_elems2 = [a for a in article_elems2 if is_between(marker, end, a)]

            for elem in article_elems:
                headline_elem = elem.find('a', class_='arial_12_vermelho')
                title_elem = elem.find('a', class_=re.compile('arial_12_azul_bold|arial_11_preto'))

                snippet_elem = elem.find('span', class_='arial_12_preto')
                snippet = snippet_elem.get_text() if snippet_elem else get_snippet_navigable_strings(elem)

                headline = None
                if headline_elem:
                    headline = headline_elem.get_text()

                all_news.append({
                    'article_url': title_elem.get('href'),
                    'headline': remove_clutter(headline),
                    'title': remove_clutter(title_elem.get_text()),
                    'snippet': prettify_text(snippet),
                    'category': category,
                    'importance': Importance.SMALL
                })

            for elem in article_elems2:
                headline_elem = elem.find('b', recursive=False)
                headline = None
                if headline_elem:
                    headline = headline_elem.get_text()

                title_elem = elem.find('a')

                snippet = get_snippet_navigable_strings(elem)

                all_news.append({
                    'article_url': title_elem.get('href'),
                    'headline': remove_clutter(headline),
                    'title': remove_clutter(title_elem.get_text()),
                    'snippet': prettify_text(snippet),
                    'category': category,
                    'importance': Importance.SMALL
                })

        ##### LATEST #####
        # not always present
        start = find_comments(soup, 'conteudo ultimas')
        end = find_comments(soup, '/conteudo ultimas')

        if start and end:
            start = start[0]
            end = end[0]

            latest_table = soup.find_all('td', class_='arial_12_preto')
            latest_articles = [td for td in latest_table if is_between(start, end, td)]

            for article_elem in latest_articles:
                title_elem = article_elem.find('a', class_='arial_12_azul_bold')
                snippet = get_snippet_navigable_strings(article_elem)

                title = title_elem.get_text()

                img_url = None
                if title == 'Crise no CDS/PP Ribeiro e Castro deve “tirar consequências” do Conselho Nacional':
                    # only case where a valid image was found
                    img_url = 'https://arquivo.pt/noFrame/replay/20070319194309im_/http://thumbs.sapo.pt/?pic=http://jn.sapo.pt/2007/03/19/ultimas/CDSPPCRISE.jpg&W=200&H=100&errorpic=http://jn.sapo.pt/images/lusomundo/jn/errorpic.gif'

                all_news.append({
                    'article_url': title_elem.get('href'),
                    'title': remove_clutter(title),
                    'snippet': prettify_text(snippet),
                    'img_url': img_url,
                    'category': 'Últimas',
                    'importance': Importance.LATEST
                })

        return all_news


class ScraperJornalDeNoticias09(NewsScraper):
    source = 'jn.pt'
    cutoff = 20141001170209

    def extract_news(self, all_news, elem_list, default_importance):
        for elem in elem_list:
            is_special_box = elem.find_parent('div', class_=re.compile(r'(caixa655|caixa250)')) is not None

            if elem.find('div', class_=re.compile(r'(NoticiaJNLive|VideoEsq)')):
                continue

            img_url = None

            # try div 'Photo'
            img_elem = elem.find('div', class_='Photo')
            if img_elem:
                # sometimes it's a flash plugin without an img
                img_elem = img_elem.find('img')
                if img_elem:
                    img_url = img_elem.get('src')
            else:
                img_elem = elem.find('img', class_='Photo')
                if img_elem:
                    img_url = img_elem.get('src')
                else:
                    img_elem = elem.find('a', recursive=False)
                    if img_elem:
                        img_url = img_elem.find('img').get('src')

            inner_elem = elem.find('div', class_=re.compile(r'(Photo|assinatura)'))
            if not is_special_box and inner_elem and inner_elem.find('h1'):
                elem = inner_elem

            # search for a div with category
            category, default_importance = self.get_category(default_importance, elem, is_special_box)
            if category == 'Vídeo':
                continue

            title_elem = elem.find_all('h1')[-1].find('a')
            same_depth_nav = [e for e in title_elem.find_parent('div').contents if isinstance(e, NavigableString)]
            if same_depth_nav:
                snippet = ' '.join(same_depth_nav)
            else:
                snippet = get_snippet_navigable_strings(elem)
                if not snippet:  # eventually a div appears
                    snippet = elem.find('div', class_='destaque-common-summary').get_text()

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': remove_clutter(title_elem.get_text()),
                'snippet': prettify_text(snippet),
                'img_url': img_url,
                'category': category,
                'importance': default_importance
            })

            related_elems = elem.find('div', class_='Related')
            if related_elems:
                for title_elem in related_elems.find_all('a'):
                    all_news.append({
                        'article_url': title_elem.get('href'),
                        'title': remove_clutter(title_elem.get_text()),
                        'category': 'Outras',
                        'importance': Importance.RELATED
                    })

    def get_category(self, default_importance, elem, is_special_box):
        category = 'Destaque'
        if elem.find('div', class_='BoxHeaderFutebol'):
            category = 'Desporto'

        elif elem.find('div', class_='HeaderGente'):
            category = 'Gente'

        # specifically for Legislativas 2009 articles
        elif is_special_box:
            box_parent = elem.find_parent('div', class_='caixa250') or elem.find_parent('div', class_='caixa655')

            if box_parent and box_parent.find('div', class_='title'):
                category_elem = box_parent.find('div', class_='title').find('a')

                if not category_elem:
                    # must be presidenciais 2011
                    category = 'Política'
                elif category_elem.get_text() == 'Legislativas 2009':
                    category = 'Política'
                    elem = elem.find('div')  # only this box iteration needs this
                elif category_elem.get_text() == 'Mundial 2010':
                    category = 'Desporto'

        # "mais notícias" section
        elif elem.find_parent('div', id='ctl00_ctl00_bcr_bcr_Rodape_ctl03_ctl00_contentDiv'):
            category = 'Outras'
            default_importance = Importance.SMALL

        elif elem.find_parent('table'):
            header_elem = elem.find_parent('table').find('div', class_='PageHeader')
            if header_elem:
                category = header_elem.get_text()

        return category, default_importance

    def scrape_page(self, soup):
        all_news = []

        # big feature
        article_elems = soup.find_all('div', class_='Manchete')
        self.extract_news(all_news, [f.find('div', class_='Content') for f in article_elems], Importance.FEATURE)

        # bold box at top right corner usually
        article_elems = soup.find_all('div', class_='Caixa')
        self.extract_news(all_news, [f.find('div', class_='Content') for f in article_elems], Importance.FEATURE)

        # larger text box at top
        feature_elems = soup.find_all('div', class_='Destaque')
        self.extract_news(all_news, [f.find('div', class_='Content') for f in feature_elems], Importance.FEATURE)

        # more large articles, not features
        article_elems = soup.find_all('div', class_='Noticia')
        self.extract_news(all_news, [f.find('div', class_='Content') for f in article_elems
                                     if not f.find_parent('div', class_='news-content')
                                     and not f.find_parent('div', id='ctl00_ctl00_bcr_bcr_TwitterBox_TwitterScript')
                                     ], Importance.LARGE)  # avoid a twitter box 20100615140117

        # newer versions had this box
        new_articles = soup.find_all('div', class_='news-content')
        self.extract_news(all_news, [(f.find('div', class_='Content') or f) for f in new_articles], Importance.FEATURE)

        # latest news
        latest_elems1 = [e.find_all('td')[-1].find('a') for e in soup.find_all('table', class_='UltimasTable')]

        # alternative table for latest news
        l = soup.find('div', class_='tabJNnews_content')
        if l:
            l = l.find('div', id='tabn_1_data').find_all('li', class_=re.compile(r'RegularItem[2]*'))
        else:
            l = []

        latest_elems2 = [e.find('a') for e in l]

        for title_elem in latest_elems1 + latest_elems2:
            all_news.append({
                'article_url': title_elem.get('href') or generate_dummy_url('jn.pt', 'parser09', 'latest', title_elem.get_text()),  # one case doesn't have url (20100530140119)
                'title': remove_clutter(title_elem.get_text()),
                'category': 'Outras',
                'importance': Importance.LATEST
            })

        # local news
        local_elems = soup.find('div', class_='DestaqueConcelhoHome')
        extract_local_news(all_news, local_elems)

        return all_news


def extract_local_news(all_news, local_elems):
    for i in range(0, len(local_elems.contents), 2):
        headline_elem = local_elems.contents[i].find('a')
        title_elem = local_elems.contents[i + 1].find('a')

        all_news.append({
            'article_url': title_elem.get('href'),
            'title': remove_clutter(title_elem.get_text()),
            'headline': headline_elem.get_text(),
            'category': 'Local',
            'importance': Importance.SMALL
        })


class ScraperJornalDeNoticias10(NewsScraper):
    source = 'jn.pt'
    cutoff = 20151201103233  # could work past this, not tested

    def scrape_page(self, soup):
        all_news = []

        article_elems = soup.find_all('div', class_=re.compile(r'^(Destaque|Caixa|Noticia)$'))
        article_elems = [e for e in article_elems if e.find('div', class_=re.compile(r'^NoticiaGeral'))]

        for article_elem in [e.find('div', class_=re.compile(r'c|Content')) for e in article_elems]:
            # find an h1 with a url
            title_elem = [e.find('a') for e in article_elem.find_all('h1') if e.find('a')][0]
            title = remove_clutter(title_elem.get_text())

            snippet_elem = article_elem.find('div', class_='destaque-common-summary')
            snippet = prettify_text(snippet_elem.get_text()) if snippet_elem else None

            img_elem = article_elem.find('a').find('img', class_='Photo')
            if not img_elem:
                # alternative for NoticiaGeralMN
                img_elem = [e for e in article_elem.find_all('img') if is_between(article_elem, title_elem, e)]
                img_elem = img_elem[0] if len(img_elem) > 0 else None

            # find category from parent
            category = 'Destaque'
            if article_elem.find_parent('div', class_='NoticiasPaisHP'):
                category = 'País'
            elif article_elem.find_parent('div', class_='Desporto250'):
                category = 'Desporto'

            all_news.append({
                'article_url': title_elem.get('href'),
                'title': title,
                'snippet': snippet,
                'img_url': img_elem.get('src') if img_elem else None,
                'category': category,
                'importance': Importance.LARGE
            })

            # RELATED ELEMS
            related_elems = article_elem.find('ul', class_='artigos_related')
            if related_elems:
                for title_elem in [e.find('a') for e in related_elems.find_all('li')]:
                    all_news.append({
                        'article_url': title_elem.get('href'),
                        'title': title_elem.get_text(),
                        'category': category,
                        'importance': Importance.RELATED
                    })

        # LOCAL NEWS
        local_elems = soup.find('div', class_='DestaqueConcelhoHome')
        extract_local_news(all_news, local_elems)

        return all_news
