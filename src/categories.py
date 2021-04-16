from enum import Enum


class Category(Enum):
    GENERIC = 'Genérico'
    SPORTS = 'Desporto'
    NATIONAL = 'Portugal'
    WORLD = 'Mundo'
    BUSINESS = 'Economia'
    ENTERTAINMENT = 'Entretenimento'
    SCIENCE = 'Ciência'
    HEALTH = 'Saúde'
    POLITICS = 'Política'
    CULTURE = 'Cultura'
    EDUCATION = 'Educação'
    TECHNOLOGY = 'Tecnologia'
    SOCIETY = 'Sociedade'
    LOCAL = 'Local'
    ENVIRONMENT = 'Ambiente'
    OPINION = 'Opinião'
    UNUSUAL = 'Insólito'
    MISC = 'Miscelânea'


category_bindings = {
    ('Notícias do dia', 'Mais notícias principais', 'Notícias principais', 'Principais notícias', 'Últimas notícias',
     'Destaque', 'Última hora', 'Outras', '1ª Página', 'Em foco', 'Foco', 'Última', 'Útimas notícias', 'Últimas',
     'Actualidade', 'Destaques', 'Genérico', 'emfoco', 'Atualidade', 'Primeira', 'Geral'): Category.GENERIC,
    ('Portugal', 'País', 'Nacional', 'Nacionais'): Category.NATIONAL,
    ('Mundo', 'Internacional', 'Europa', 'Enviados', 'África', 'Globo', 'Eleições em Espanha', 'Internacionais',
     'Comunidades Lusófonas'): Category.WORLD,
    ('Desporto', 'Esportes', 'Euro 2004', 'Euro2016', 'Resultados', 'Relvado', 'Futebol', 'Mundial2010', 'Mundial',
     'Mundial 2010', 'Ténis', 'Euro 2012', 'Primeira Liga', 'Liga dos Campeões', 'Liga Europa'): Category.SPORTS,
    ('Negócios', 'Economia', 'Economia & Internacional', 'Dinheiro', 'Dinheiro Vivo', 'Salário Mínimo', 'Caso Banif',
     'negocios', 'Banca', 'Economa'): Category.BUSINESS,
    ('Entretenimento', 'Música', 'Cinema', 'Palco', 'Televisão', 'Arte e média', 'Star Wars', 'Lazer', 'Festival',
     'Jogos', 'Concertos', 'Espectáculos'): Category.ENTERTAINMENT,
    ('Ciência', 'Ciências', 'Ciencia', 'Nobel', 'Espaço', 'Biologia', 'Ciência e Saúde'): Category.SCIENCE,
    ('Saúde', 'Morte no Hospital de S. José', 'SNS', 'Vacinas'): Category.HEALTH,
    ('Política', 'Politica', 'Partidos', 'Governo'): Category.POLITICS,
    ('Cultura', 'Leituras', 'Cartaz', 'Artes', 'Arte', 'Literatura', 'Dança', 'Exposições', 'BD', 'Teatro'): Category.CULTURE,
    ('Educação', 'Ranking das escolas', 'Ensino'): Category.EDUCATION,
    ('Tecnologia', 'Ciência/tecnologia', 'Ciência e tecnologia', 'Internet', 'Computadores', 'Informática',
     'Tecnologia e Ciência', 'Tecnolologia', 'Hardware'): Category.TECHNOLOGY,
    ('Sociedade', 'Grande Plano', 'Tema da semana', 'Polícia', 'Gente', 'Vidas', 'Vida', 'Fotogalerias', 'Dossiês',
     'Dossiê', 'Alertas Expresso', 'Dossies Actualidade', 'Pessoas', 'Religião', 'Moda'): Category.SOCIETY,
    ('Local', 'Local Lisboa', 'Grande Porto', 'Grande Lisboa', 'Grande Lsiboa', 'Porto 2001', 'Regional', 'Lisboa',
     'Local e regional', 'Porto'): Category.LOCAL,
    ('Ambiente', 'Ecosfera', 'DN + EDP na Cimeira do Clima', 'Cimeira do Clima', 'Biodiversidade', 'Clima'): Category.ENVIRONMENT,
    ('Opinião', 'Análise', 'Crónica'): Category.OPINION,
    ('Acredite se quiser', 'Esta é boca', 'Mundo Insólito', 'Pausa para Café', 'Insólito'): Category.UNUSUAL,
    ('Outras', 'Mais Lidas'): Category.MISC
}


def bind_category(category_text):
    cat_dict = {}
    for k, v in category_bindings.items():
        for key in k:
            cat_dict[key.lower()] = v

    if category_text.lower() not in cat_dict:
        raise Exception('Unknown category: ' + category_text)

    return cat_dict[category_text.lower()]
