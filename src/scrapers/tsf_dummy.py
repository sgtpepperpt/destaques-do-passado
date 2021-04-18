from src.scrapers.news_scraper import NewsScraper, Importance
from src.util import generate_dummy_url


class DummyTSF01(NewsScraper):
    source = 'tsf.pt'
    cutoff = 20001019012135
    used = False

    # dummy scraper, returns a set of very old news only once
    def scrape_page(self, soup):
        if self.used:
            return None

        self.used = True

        all_news = []
        all_news.append({
            'arquivo_source_url': 'https://arquivo.pt/wayback/19981212033620/http://www.tsf.pt:80/',
            'timestamp': 19990507182000,  # arquivo timestamp seems to be far in the past
            'title': 'Nino Vieira na Embaixada portuguesa',
            'headline': 'Guiné Bissau',
            'snippet': 'O presidente guineense está refugiado na Embaixada de Portugal em Bissau. Acompanham-no a mulher, bem como alguns funcionários e militares franceses. Antes, Nino Vieira esteve no Centro Cultural Francês, até ao ataque da Junta Militar. Tanto este edifício como o Palácio Presidencial ficaram em chamas. Os militares fiéis à presidência renderam-se. A agência France Press informou que João Bernardo "Nino" Vieira teria pedido asilo a Portugal, com resposta positiva. Jaime Gama não afasta a hipótese de que isso venha a acontecer mas desmente que o processo do presidente da Guiné-Bissau esteja a ser tratado. O porta-voz das tropas fiéis ao brigadeiro Ansumane Mané garante que não vai haver derramamento de sangue caso Nino Vieira seja capturado.',
            'category': 'Destaques',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'arquivo_source_url': 'https://arquivo.pt/wayback/19981212033620/http://www.tsf.pt:80/',
            'timestamp': 19990507182000,  # arquivo timestamp seems to be far in the past
            'title': 'Albânia pode receber um milhão de refugiados',
            'headline': 'Crise nos Balcãs',
            'snippet': 'O governo albanês anunciou que pode acolher até um milhão de deslocados do Kosovo. Até agora, foram recebidos na Albânia cerca de 450 mil refugiados. As autoridades da vizinha Macedónia decidiram reabrir as fronteiras para permitir a entrada de mais albaneses do Kosovo. Por engano, a Bulgária voltou a ser um alvo da NATO. Pela quinta vez, caíu um míssil em território búlgaro, sem causar vítimas. A Hungria mantém apenas três fronteiras abertas. Os aviões da Aliança Atlântico utilizam o espaço aéreo húngaro para atingir a Jugoslávia. As populações passam a noite com receio de serem atingidas por uma "bomba perdida".',
            'category': 'Destaques',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'arquivo_source_url': 'https://arquivo.pt/wayback/19981212033620/http://www.tsf.pt:80/',
            'timestamp': 19990507182000,  # arquivo timestamp seems to be far in the past
            'title': 'Vitorino responde a Cavaco',
            'headline': 'Política',
            'snippet': 'O socialista António Vitorino saíu em defesa do Governo PS e respondeu às acusações de Cavaco Silva. O antigo líder do PSD e ex-primeiro-ministro aproveitou a festa dos 25 anos do PSD para fazer pontaria ao executivo de António Guterres. Cavaco disse que reina o "caos" na sociedade portuguesa. O porta-voz do Partido Socialista contrapôs com os resultados do "diálogo rosa". António Vitorino disse que a vitória é o destino do PS, nas legislativas deste ano',
            'category': 'Destaques',
            'importance': Importance.FEATURE
        })
        all_news.append({
            'arquivo_source_url': 'https://arquivo.pt/wayback/19981212033620/http://www.tsf.pt:80/',
            'timestamp': 19990507182000,  # arquivo timestamp seems to be far in the past
            'title': 'João Paulo II faz visita polémica',
            'headline': 'Papa na Roménia',
            'snippet': 'O Papa está pela primeira vez Roménia, a convite do Patriarca ortodoxo Teoctist. Este é o primeiro de três dias de uma visita que está a gerar expectativas e alguma agitação. Num acto inédito, João Paulo II vai assistir a uma missa ortodoxa em Bucareste. O esforço ecuménico do chefe da Igreja Católica reabriu velhas feridas da ruptura entre Roma e Constantinopla, ocorrida há quase mil anos.',
            'category': 'Destaques',
            'importance': Importance.FEATURE
        })

        # add deterministic no url flag (deterministic because it's used as key)
        for news in all_news:
            if 'article_url' not in news:
                news['article_url'] = generate_dummy_url(self.source, news['timestamp'], news['category'], news['title'])

        return all_news
