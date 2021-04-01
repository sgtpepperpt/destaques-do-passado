import hashlib
import re

from bs4 import Comment


def clean_spacing(text):
    return ' '.join(text.split()).strip()


def remove_clutter(text):
    if not text:
        return

    clutter = ['(em actualização)', '(em atualização)', '(actualização)', '(atualização)', '(actualizações)', '(atualizações)', '(com vídeo)', '[com vídeo]', '[vídeo]', 'PORTUGAL:', '(COM TRAILER)', 'EXCLUSIVO:', '(galeria de fotos)']
    for elem in clutter:
        text = text.replace(elem, '')

    return clean_spacing(text)


def clean_special_chars(text):
    # removes clutter and also special chars from the text
    return re.sub(r'[\W|»|”|"|’]+$', '', remove_clutter(text))


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
    if text[-3:] == '...':
        had_ellipsis = True
        text = text[:-4].strip()

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

    # remove doubled spaces
    text = clean_spacing(text)

    if had_period:
        text += '.'
    elif had_ellipsis:
        text += '...'

    return text


def ignore_title(title):
    allows = ['Sorteio da Liga', 'Sorteio dos quartos', 'Sorteio da Superliga']
    starts = ['Revista de imprensa', 'Destaques d', 'Sorteio', 'Chave do', 'Jackpot', 'Dossier:', 'Fotogaleria',
              'Vídeo:', 'Público lança', 'Público vence', 'Consulte as previsões', 'Previsão do tempo', 'Veja o tempo', 'Comentário:',
              'Reportagem:', 'Exclusivo assinantes', 'Entrevista:', 'Perfil:', 'Blog ', 'Home ', 'CR7 exclusivo em', 'http',
              'Mudança na publicação de comentários online', 'Quiosque:', 'Comente', 'Euromilhões', 'Vote', 'Opinião:',
              'Nota editorial', 'Faça aqui', 'Expresso nos', 'Já pensou onde ir', 'Top 10', 'Conheça as novidades do site',
              'Justiça seja feita', 'Revista \'Lui\' tira a roupa']
    for forbidden in starts:
        if title.lower().startswith(forbidden.lower()):
            return True

    contains = ['(exclusivo assinantes)', 'Veja o vídeo', 'e o novo Expresso', 'com o Expresso', 'para a casa ir abaixo',
                'Expresso Diário', 'dicas para', 'A 1ª página do Expresso', 'A primeira página do', 'a Revista E']
    for forbidden in contains:
        if forbidden.lower() in title.lower() and forbidden.lower() not in allows:
            return True

    # ignore if the title starts with a date/time
    if re.match(r'[0-3][0-9]\.[0-1][0-9]\.[1-2][0-9][0-9][0-9]\s*-\s*.*', title):
        return True

    return False


def is_link_pt(link):
    groups = re.search(r'https://arquivo\.pt/noFrame/replay/[0-9]*/https?://([^/]*)/.*', link)
    full_url = groups.group(1)
    if full_url in ['www.fabricadeconteudos.com']:
        return True

    groups2 = re.search(r'.*\.([a-zA-Z]*)', full_url)
    return groups2.group(1) == 'pt'


def get_original_news_url(url):
    if url.startswith('no-article-url'):
        return url

    groups = re.search(r'https://arquivo\.pt/(?:noFrame/replay|wayback)/[0-9]*(?:oe_)?/(.*)', url)
    return groups.group(1)


def is_https_link(link):
    groups = re.search(r'https://arquivo\.pt/wayback/[0-9]*/(https?).*', link)
    return groups.group(1) == 'https'


def split_date(date):
    return date[:4], date[4:6], date[6:8]


def make_absolute(source, timestamp, is_https, url):
    if str(url).startswith('no-article-url'):
        return url

    if not url or len(url) == 0:
        raise Exception('URL not provided')

    if url.startswith('//'):
        # publico misses http sometimes
        # eg '//arquivo.pt/noFrame/replay/20151231180213///www.publico.pt/economia/noticia/pensoes-ate-6288-euros-aumentam-04-a-partir-de-1-de-janeiro-1718873'
        url = 'https' + url
        url = url.replace('///', '/')

    possible = r'(https://arquivo\.pt)?(/)?(noFrame/replay|wayback)?(/)?([0-9]{14})?(?:im_|oe_|mp_)?(/)?(https?://[^/]*)?(/)?(.*)?'
    match = re.findall(possible, url)

    final = ''
    if not match[0][0]:
        final += 'https://arquivo.pt'

    if not match[0][1]:
        final += '/'

    if not match[0][2]:
        final += 'noFrame/replay'

    if not match[0][3]:
        final += '/'

    if not match[0][4]:
        final += timestamp

    if not match[0][5]:
        final += '/'

    if not match[0][6]:
        final += 'http{}://{}'.format('s' if is_https else '', source)

    if not match[0][7]:
        final += '/'

    if not match[0][8]:
        raise Exception('Error in absolute url')  # shouldn't be error if some urls have no path, just domain, like leitor.expresso.pt (we ignore those bus it SHOULD be valid if we didn't)

    return final + url


def get_actual_source(url):
    possible = r'(https://arquivo\.pt)?(/)?(noFrame/replay|wayback)?(/)?([0-9]{14})?(?:im_|oe_|mp_)?(/)?(https?)://([^/]*)?(/)?(.*)?'
    match = re.findall(possible, url)
    return match[0][7]


def generate_dummy_url(source, timestamp, category, title):
    st = '{}-{}-{}-{}'.format(source, timestamp, category, title)
    return 'no-article-url-' + hashlib.sha224(st.encode()).hexdigest()


def generate_destaques_uniqueness(category, title, snippet):
    # use this when a newspaper reuses the same link for different articles, as the scraper default is to use urls as id
    st = '{}-{}-{}'.format(category, title, snippet)
    return '?destaques_uniqueness=' + hashlib.sha224(st.encode()).hexdigest()


def remove_destaques_uniqueness(url):
    possible = r'(.*)\?destaques_uniqueness=.*'
    match = re.findall(possible, url)
    return match[0] if len(match) > 0 else url


def is_between(first, last, element):
    next = first
    while next and next != last:
        if next == element:
            return True
        else:
            next = next.next
    return False


def find_comments(parent, content):
    return parent.find_all(string=lambda text: isinstance(text, Comment) and text == content)


def find_comments_regex(parent, content):
    return parent.find_all(string=lambda text: isinstance(text, Comment) and re.match(content, text))
