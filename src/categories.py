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
     'Actualidade'): Category.GENERIC,
    ('Portugal', 'País'): Category.NATIONAL,
    ('Mundo', 'Internacional', 'Europa', 'Enviados', 'África'): Category.WORLD,
    ('Desporto', 'Esportes'): Category.SPORTS,
    ('Negócios', 'Economia', 'Economia & Internacional', 'Dinheiro'): Category.BUSINESS,
    ('Entretenimento', 'Música', 'Cinema', 'Palco', 'Televisão'): Category.ENTERTAINMENT,
    ('Ciência', 'Ciências', 'Ciencia'): Category.SCIENCE,
    ('Saúde',): Category.HEALTH,
    ('Política', 'Politica'): Category.POLITICS,
    ('Cultura', 'Leituras', 'Cartaz'): Category.CULTURE,
    ('Educação',): Category.EDUCATION,
    ('Tecnologia', 'Ciência/tecnologia'): Category.TECHNOLOGY,
    ('Sociedade', 'Grande Plano', 'Tema da semana', 'Polícia', 'Gente', 'Vidas', 'Vida', 'Fotogalerias', 'Dossiês', 'Dossiê', 'Alertas Expresso', 'Dossies Actualidade'): Category.SOCIETY,
    ('Local', 'Local Lisboa', 'Grande Porto', 'Grande Lisboa', 'Grande Lsiboa', 'Porto 2001'): Category.LOCAL,
    ('Ambiente', 'Ecosfera'): Category.ENVIRONMENT,
    ('Opinião',): Category.OPINION,
    ('Acredite se quiser', 'Esta é boca', 'Mundo Insólito'): Category.UNUSUAL
}


def bind_category(category_text):
    cat_dict = {}
    for k, v in category_bindings.items():
        for key in k:
            cat_dict[key.lower()] = v

    if category_text.lower() not in cat_dict:
        raise Exception('Unknown category: ' + category_text)

    return cat_dict[category_text.lower()]
