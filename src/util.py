import re


def clean_special(str):
    # TODO nao apagar citacoes
    return re.sub(r"\W+$", "", str.strip().replace('(em actualização)', '').replace('(com vídeo)', ''))


def prettify_text(text):
    return ' '.join(text.split())


def is_link_pt(link):
    groups = re.search(r'https://arquivo\.pt/noFrame/replay/[0-9]*/https?://([^/]*)/.*', link)
    full_url = groups.group(1)
    if full_url in ['www.fabricadeconteudos.com']:
        return True

    groups2 = re.search(r'.*\.([a-zA-Z]*)', full_url)
    return groups2.group(1) == 'pt'


def get_original_news_link(link):
    groups = re.search(r'https://arquivo\.pt/noFrame/replay/[0-9]*/(.*)', link)
    return groups.group(1)


def is_https_link(link):
    groups = re.search(r'https://arquivo\.pt/wayback/[0-9]*/(https?).*', link)
    return groups.group(1) == 'https'


def split_date(date):
    return date[:4], date[4:6], date[6:8]


def make_absolute(source, date, is_https, url):
    if not url or len(url) == 0:
        return ''

    possible = r'(https://arquivo\.pt)?(/)?(noFrame/replay)?(/)?([0-9]*)?(/)?(https?://[^/]*)?(/)?(.*)?'
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
