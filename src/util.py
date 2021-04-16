import hashlib
import re

from bs4 import Comment, NavigableString

from src.text_util import remove_clutter


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

    groups = re.search(r'https://arquivo\.pt/(?:noFrame/replay|wayback)/[0-9]*(?:oe_|mp_|im_)?/(.*)', url)
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

    if url.startswith('/') and url.count('/') == 1:
        url = url[1:]  # the regex didn't recognise the slash as being the last one, instead using up the first one;
                       # don't want to change it because it could affect everything else previously, only affects dn.pt 10/2015

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

    if 'www.dn.pt//' in url or 'www.dn.pt//' in final:
        print()

    # if not match[0][8]:
    #     raise Exception('Error in absolute url')  # shouldn't be error if some urls have no path, just domain, like leitor.expresso.pt (we ignore those bus it SHOULD be valid if we didn't)

    if final.startswith('/'):
        raise Exception

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


def is_after(first, element):
    previous = element.previous
    while previous:
        if previous == first and previous.sourceline == first.sourceline:  # if two elements are equal but not the same it would return true
            return True
        else:
            previous = previous.previous
    return False


def is_between(first, last, element):
    next = first
    while next and next != last:
        if next == element:
            return True
        else:
            next = next.next
    return False


def is_between_nonrecursive(first, last, element):
    next = first
    while next and next != last:
        if next == element:
            return True
        else:
            next = next.next_sibling
    return False


def find_comments(parent, content):
    return parent.find_all(string=lambda text: isinstance(text, Comment) and text == content)


def find_comments_regex(parent, content):
    return parent.find_all(string=lambda text: isinstance(text, Comment) and re.match(content, text))


def get_direct_strings(elem):
    return remove_clutter(' '.join([e for e in elem.contents if isinstance(e, NavigableString) and not isinstance(e, Comment)]))


def encode_url(url):
    # encode url to save as filename
    return url.replace(':', '*').replace('/', '|').replace('-', '$')


def decode_url(url):
    return url.replace('*', ':').replace('|', '/').replace('$', '-')
