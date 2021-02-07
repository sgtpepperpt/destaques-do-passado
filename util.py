import re


def clean_special(str):
    return re.sub(r"\W+$", "", str.strip())


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
