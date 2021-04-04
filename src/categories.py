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


category_bindings = {
    ('Notícias do dia', 'Mais notícias principais', 'Notícias principais', 'Principais notícias', 'Últimas notícias', 'Destaque', 'Última hora', 'Outras', '1ª Página', 'Em foco', 'Foco', 'Última', 'Útimas notícias', 'Últimas',
     'Actualidade', 'Destaques'): Category.GENERIC,
    ('Portugal', 'País', 'Nacional'): Category.NATIONAL,
    ('Mundo', 'Internacional', 'Europa', 'Enviados', 'África', 'Globo', 'Eleições em Espanha'): Category.WORLD,
    ('Desporto', 'Esportes', 'Euro 2004', 'Euro2016'): Category.SPORTS,
    ('Negócios', 'Economia', 'Economia & Internacional', 'Dinheiro', 'Dinheiro Vivo', 'Salário Mínimo', 'Caso Banif'): Category.BUSINESS,
    ('Entretenimento', 'Música', 'Cinema', 'Palco', 'Televisão', 'Arte e média', 'Star Wars'): Category.ENTERTAINMENT,
    ('Ciência', 'Ciências', 'Ciencia'): Category.SCIENCE,
    ('Saúde', 'Morte no Hospital de S. José'): Category.HEALTH,
    ('Política', 'Politica'): Category.POLITICS,
    ('Cultura', 'Leituras', 'Cartaz', 'Artes'): Category.CULTURE,
    ('Educação', 'Ranking das escolas'): Category.EDUCATION,
    ('Tecnologia', 'Ciência/tecnologia', 'Ciência e tecnologia'): Category.TECHNOLOGY,
    ('Sociedade', 'Grande Plano', 'Tema da semana', 'Polícia', 'Gente', 'Vidas', 'Vida', 'Fotogalerias', 'Dossiês', 'Dossiê', 'Alertas Expresso', 'Dossies Actualidade', 'Pessoas'): Category.SOCIETY,
    ('Local', 'Local Lisboa', 'Grande Porto', 'Grande Lisboa', 'Grande Lsiboa', 'Porto 2001', 'Regional'): Category.LOCAL,
    ('Ambiente', 'Ecosfera', 'DN + EDP na Cimeira do Clima', 'Cimeira do Clima'): Category.ENVIRONMENT,
    ('Opinião', 'Análise'): Category.OPINION,
    ('Acredite se quiser', 'Esta é boca', 'Mundo Insólito', 'Pausa para Café'): Category.UNUSUAL
}


def bind_category(category_text):
    cat_dict = {}
    for k, v in category_bindings.items():
        for key in k:
            cat_dict[key.lower()] = v

    if category_text.lower() not in cat_dict:
        raise Exception('Unknown category: ' + category_text)

    return cat_dict[category_text.lower()]
