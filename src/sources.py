def bind_source(source_text):
    if source_text in ['Público.pt (Assinatura', 'Público.pt']:
        return 'Público'

    if source_text.startswith('Diário de Notícias'):
        return 'Diário de Notícias'

    if source_text.startswith('Jornal de Negócios'):
        return 'Jornal de Negócios'

    if source_text.startswith('O Ribatejo | jornal regional'):
        return 'O Ribatejo'

    if source_text.startswith('Revista BIT, Informática'):
        return 'Revista BIT'

    return source_text


def source_name_from_file(source):
    sources = {
        'publico.pt': 'Público',
        'ultimahorapublico.pt': 'Público',
        'portugaldiario.iol.pt': 'Portugal Diário',
        'jn.pt': 'Jornal de Notícias',
        'expresso.pt': 'Expresso'
    }

    return sources[source]
