import re


def clean_spacing(text):
    return ' '.join(text.split()).strip()


def remove_clutter(text):
    clutter = ['(em actualização)', '(em atualização)', '(com vídeo)', 'PORTUGAL:']
    for elem in clutter:
        text = text.replace(elem, '')

    return clean_spacing(text)


def clean_special(text):
    return re.sub(r'[\W|»|”|"|’]+$', '', remove_clutter(text))


def prettify_text(text):
    had_ellipsis = False
    had_period = False

    # remove text clutter and spaces
    text = remove_clutter(clean_spacing(text))

    if len(text) < 3:
        return text

    # remove ...
    if text[-3:] == '...':
        had_ellipsis = True
        text = text[:-4].strip()

    # remove period
    if text[-1] == '.':
        had_period = True
        text = text[:-1].strip()

    # remove Odivelas, 11 jun (Lusa) --
    groups = re.search(r'^[A-Za-z\s]+, [0-9]+ [A-Za-z]+ \(Lusa\) --? (.*)', text)
    if groups:
        text = groups.group(1)

    # remove doubled spaces
    text = clean_spacing(text)

    if had_period:
        text += '.'
    elif had_ellipsis:
        text += '...'

    return text


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

    groups = re.search(r'https://arquivo\.pt/noFrame/replay/[0-9]*/(.*)', url)
    return groups.group(1)


def is_https_link(link):
    groups = re.search(r'https://arquivo\.pt/wayback/[0-9]*/(https?).*', link)
    return groups.group(1) == 'https'


def split_date(date):
    return date[:4], date[4:6], date[6:8]


def make_absolute(source, date, is_https, url):
    if str(url).startswith('no-article-url'):
        return url

    if not url or len(url) == 0:
        raise Exception('URL not provided')

    possible = r'(https://arquivo\.pt)?(/)?(noFrame/replay)?(/)?([0-9]*)?(?:im_)?(/)?(https?://[^/]*)?(/)?(.*)?'
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
        final += date

    if not match[0][5]:
        final += '/'

    if not match[0][6]:
        final += 'http{}://{}'.format('s' if is_https else '', source)

    if not match[0][7]:
        final += '/'

    if not match[0][8]:
        raise Exception('Error in absolute url')

    return final + url
