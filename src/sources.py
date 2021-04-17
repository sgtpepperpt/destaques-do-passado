def bind_source(source_text):
    if source_text in ['Público.pt (Assinatura', 'Público.pt']:
        return 'Público'

    if source_text.startswith('Diário de Notícias') or source_text in ['DN']:  # google news has Diário de Notícias - Lisboa
        return 'Diário de Notícias'

    if source_text.startswith('Jornal de Negócios'):
        return 'Jornal de Negócios'

    if source_text.startswith('O Ribatejo | jornal regional'):
        return 'O Ribatejo'

    if source_text.startswith('Revista BIT, Informática') or source_text in ['Revista Bit', 'http://www.bit.pt/feed/', 'B!T', 'Revista BiT', 'Bit']:
        return 'Revista BIT'

    if source_text.startswith('Diário Economico'):
        return 'Diário Económico'

    if source_text.startswith('TSF'):
        return 'TSF'

    if source_text.startswith('Visão'):
        return 'Visão'

    if source_text.lower().startswith('blitz'):
        return 'BLITZ'

    if 'aeiou' in source_text.lower():
        return 'AEIOU'

    if source_text in ['Ionline']:
        return 'iOnline'

    if source_text in ['OJogo', 'O JOGO', 'o Jogo', 'O Jogo Online']:
        return 'O Jogo'

    if source_text in ['ABola']:
        return 'A Bola'

    if source_text in ['Exame Informatica']:
        return 'Exame Informática'

    if source_text in ['Ciberia']:
        return 'Cibéria'

    if source_text in ['JN']:
        return 'Jornal de Notícias'

    if source_text in ['quiosque']:
        return 'Quiosque'

    if source_text in ['Diário Digital P']:
        return 'Diário Digital'

    if source_text in ['Boas Noticias']:
        return 'Boas Notícias'

    if source_text in ['Meios e Publicidade']:
        return 'Meios & Publicidade'

    if source_text in ['Autosport']:
        return 'AutoSport'

    if 'tek' in source_text.lower():
        return 'TeK'

    if source_text.lower() in ['green savers', 'greensavers']:
        return 'Green Savers'

    if source_text.lower() == 'tvnet' or source_text.lower() == 'tv net':
        return 'TVNet'

    return source_text


def source_name_from_file(source):
    sources = {
        'publico.pt': 'Público',
        'ultimahorapublico.pt': 'Público',
        'portugaldiario.iol.pt': 'Portugal Diário',
        'jn.pt': 'Jornal de Notícias',
        'expresso.pt': 'Expresso',
        'dn.pt': 'Diário de Notícias',
        'aeiou.pt': 'AEIOU',
        'noticias.sapo.pt': 'SAPO Notícias',
        'diariodigital.pt': 'Diário Digital'
    }

    return sources[source]
