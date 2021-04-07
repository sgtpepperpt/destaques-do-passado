from src.scrapers.news_scraper import NewsScraper, Importance
from src.util import generate_dummy_url


class DummyPublico01(NewsScraper):
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