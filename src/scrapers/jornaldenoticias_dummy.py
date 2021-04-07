from src.scrapers.news_scraper import NewsScraper, Importance
from src.util import generate_dummy_url


class DummyJornalDeNoticias01(NewsScraper):
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


class DummyJornalDeNoticias07(NewsScraper):
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