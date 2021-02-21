def bind_source(source_text):
    if source_text in ['Público.pt (Assinatura', 'Público.pt']:
        return 'Público'

    if source_text.startswith('Diário de Notícias'):
        return 'Diário de Notícias'

    if source_text.startswith('Jornal de Negócios'):
        return 'Jornal de Negócios'

    return source_text


def source_name_from_file(source):
    sources = {
        'publico.pt': 'Público',
        'ultimahorapublico.pt': 'Público',
    }

    return sources[source]
