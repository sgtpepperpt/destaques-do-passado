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


category_bindings = {
    ('Notícias do dia', 'Mais notícias principais', 'Notícias principais', 'Principais notícias', 'Últimas notícias', 'Destaque', 'Última hora', 'Outras'): Category.GENERIC,
    ('Portugal', ): Category.NATIONAL,
    ('Mundo', 'Internacional'): Category.WORLD,
    ('Desporto', 'Esportes'): Category.SPORTS,
    ('Negócios', 'Economia'): Category.BUSINESS,
    ('Entretenimento',): Category.ENTERTAINMENT,
    ('Ciência', 'Ciências'): Category.SCIENCE,
    ('Saúde',): Category.HEALTH,
    ('Política',): Category.POLITICS,
    ('Cultura',): Category.CULTURE,
    ('Educação',): Category.EDUCATION,
    ('Tecnologia', 'Ciência/tecnologia'): Category.TECHNOLOGY,
    ('Sociedade',): Category.SOCIETY,
    ('Local',): Category.LOCAL,
    ('Ambiente', 'Ecosfera'): Category.ENVIRONMENT,
    ('Opinião',): Category.OPINION
}


def bind_category(category_text):
    cat_dict = {}
    for k, v in category_bindings.items():
        for key in k:
            cat_dict[key.lower()] = v

    if category_text.lower() not in cat_dict:
        raise Exception('Unknown category: ' + category_text)

    return cat_dict[category_text.lower()]
