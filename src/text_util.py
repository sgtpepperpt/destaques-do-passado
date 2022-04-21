import re


def clean_spacing(text):
    return ' '.join(text.split()).strip()


def remove_clutter(text):
    if not text:
        return

    to_remove = ['(em actualização)', '(em atualização)', '(actualização)', '(atualização)', '(actualizações)',
                 '(atualizações)', '(com vídeo)', '[com vídeo]', '[vídeo]', '(VÍDEO)', 'PORTUGAL:', '(COM TRAILER)',
                 'EXCLUSIVO:', '(galeria de fotos)', '(com fotogaleria)', '(ouve-o aqui)', '(fotogaleria)', '(FOTOS)',
                 '(vídeo)', '[em actualização]', '(com VÍDEO)', '(vídeos)', '(ACTUALIZADA)', '-- oficial',
                 'CORREÇÃO: ', ' - jornal', '(actual)', '- ACTUALIZADA', '. Veja as fotos', '(act.)', '(em imagens)',
                 '(Fotos)', '(act)', '(em imagens)']

    for elem in to_remove:
        text = text.replace(elem, '')

    if text.startswith('•') or text.startswith(',') or text.startswith(':'):
        text = text[1:]

    # remove (actual.) (actual.I) (actual.II) etc
    match_actual = re.match(r'(.*)\(actual\.I*\)$', text)
    if match_actual:
        text = match_actual.group(1)

    return clean_spacing(text)


def clean_special_chars(text):
    # removes clutter and also special chars from the text
    return re.sub(r'[\W|»|”|"|’]+$', '', remove_clutter(text))


def prettify_title(title):
    if not title:
        return

    # remove spaces with ellipsis
    if title.endswith('...'):
        title = title[:-3].strip() + '...'

    title = remove_clutter(title)

    return clean_spacing(title)


def prettify_text(text):
    if not text:
        return text

    had_ellipsis = False
    had_period = False

    # remove text clutter and spaces
    text = remove_clutter(clean_spacing(text))

    if not text or len(text) < 3:
        return text

    # remove ...
    if text[-4:] == '....':
        had_ellipsis = True
        text = text[:-4].strip()
    elif text[-3:] == '...':
        had_ellipsis = True
        text = text[:-3].strip()
    elif text[-5:] == '(...)':
        had_ellipsis = True
        text = text[:-5].strip()

    # remove period
    if text[-1] == '.':
        had_period = True
        text = text[:-1].strip()

    # remove terminating comma
    if text[-1] == ',':
        text = text[:-1].strip()

    # remove Odivelas, 11 jun (Lusa) --
    groups = re.search(r'^[A-Za-zÀ-ÿ\s]+, [0-9]+ [A-Za-z]+ \(Lusa\) --? (.*)', text)
    if groups:
        text = groups.group(1)

    if text.startswith('PDiário:'):
        text = text.replace('PDiário:', '')

    # remove more clutter
    to_remove = ['IMPRIMIR(0). ENVIAR. TAGS.', '(Em actualização) - ', '( ler artigo',
                 'PUB. Global Imagens. Lusa. Facebook · Twitter; Imprimir. Partilhar; Comentar.', 'IMPRIMIR(0).',
                 'Filipe Casaca. 0. Tópicos · Justiça · Supremo Tribunal de Justiça · Polícia Judiciária · Ministério Público · Crianças · Portimão.']
    for elem in to_remove:
        text = text.replace(elem, '')

    # remove doubled spaces
    text = clean_spacing(text)

    # restore stuff
    if had_period:
        text += '.'
    elif had_ellipsis:
        text += '...'

    return text


def ignore_title(title):
    ignore_starts = ['Revista de imprensa', 'Destaques d', 'Sorteio', 'Chave do', 'Jackpot', 'Dossier:', 'Fotogaleria',
                     'Vídeo:', 'Público lança', 'Público vence', 'Consulte as previsões', 'Previsão do tempo',
                     'Veja o tempo', 'Comentário:', 'Reportagem:', 'Exclusivo assinantes', 'Entrevista:', 'Perfil:',
                     'Blog ', 'Home ', 'CR7 exclusivo em', 'http', 'Mudança na publicação de comentários online',
                     'Quiosque:', 'Comente ', 'Euromilhões', 'Vote', 'Opinião:', 'Nota editorial', 'Faça aqui',
                     'Expresso nos', 'Já pensou onde ir', 'Top 10', 'Conheça as novidades do site',
                     'Justiça seja feita', 'Revista \'Lui\' tira a roupa', 'Veja', 'Editorial', 'Sudoku (',
                     'As melhores fotografias', 'Esta é a fotografia', 'Conheça', 'Fórum:', 'GALERIA DE FOTOS',
                     'Infografista do PÚBLICO', 'Vídeos d', 'Quiz:', 'Gráfico animado', 'Guia para', 'SAPO dá',
                     'SAPO renova', 'Mitrologia: ', 'Passatempo: ', 'Diário Digital muda', 'A sua opinião:',
                     'Renascença nomeada', 'Opinião de', 'Acha que sabe', 'Em directo:', 'Nota da Renascença',
                     'Tem dúvidas sobre', 'Fim-de-semana de portas', 'Análise:', 'Os negócios da comida', 'Guia de',
                     'Boa Cama: Termine o Verão', 'Cruzadas (', 'Hoje é Notícia']

    ignore_contains = ['(exclusivo assinantes)', 'Veja o vídeo', 'e o novo Expresso', 'com o Expresso',
                       'para a casa ir abaixo', 'Expresso Diário', 'dicas para', 'A 1ª página do Expresso',
                       'A primeira página do', 'a Revista E', 'A grande revista sobre o Benfica campeão',
                       'notícias + lidas', 'Portal AEIOU', 'mulheres da vida de', 'adivinhe', 'sugestão do PÚBLICO',
                       'sugestões do PÚBLICO', 'do Cinemax', 'entrevistado quinta', 'novo site e nova web TV',
                       'ganhe um', 'Renascença responde', 'Faça contas com o simulador', ' em fotos', 'saiba qua',
                       'saiba como', 'emissão especial', 'Participe', 'Nuovo video di Bin Laden']

    allows = ['Sorteio da Liga', 'Sorteio dos quartos', 'Sorteio da Superliga']

    exact = ['Estreia']

    for forbidden in ignore_starts:
        if title.lower().startswith(forbidden.lower()):
            return True

    for forbidden in ignore_contains:
        if forbidden.lower() in title.lower() and forbidden.lower() not in allows:
            return True

    for forbidden in exact:
        if title.lower().startswith(forbidden.lower()):
            return True

    # ignore if the title starts with a date/time
    if re.match(r'[0-3][0-9]\.[0-1][0-9]\.[1-2][0-9][0-9][0-9]\s*-\s*.*', title):
        return True

    # ignore if it's a job offer
    if re.match(r'.* procura .* \((?:m/f|m|f)\)\s*$', title):
        return True

    return False


def ignore_pretitle(pretitle):
    return pretitle in ['Grátis', 'Passatempo', 'Passatempos', 'Editorial', 'Projecto DN', 'Artigo de opinião']


def ignore_snippet(snippet):
    # if no snippet, don't ignore article because of it
    if not snippet:
        return False

    ignore_contains = ['Ideias para este', 'o EXPRESSO oferece-lhe']

    for forbidden in ignore_contains:
        if forbidden.lower() in snippet.lower():
            return True

    return False
