import json
import os
from collections import Counter

import chardet
import requests
import pathlib

from bs4 import BeautifulSoup

from src.util import is_https_link, get_actual_source

# pages can be ignored via timestamp or range of timestamps, eg if page didn't change in consecutive days or there was a page error
# encoding can be defined like timestamps
news_sources = [
    {'site': 'news.google.pt', 'from': '20051124000000'},
    {'site': 'publico.pt', 'special': {'20100910150634': '?fl=1', '20110703150815': '?mobile=no'}, 'ignore': ['19961013180344', '19990421171920-20001203173200']},
    {'site': 'ultimahora.publico.pt'},
    {'site': 'sabado.pt'},
    {'site': 'diariodigital.pt'},
    {'site': 'iol.pt'},
    {'site': 'aeiou.pt'},
    {'site': 'portugaldiario.iol.pt', 'ignore': ['20001119134000', '20001202055200', '20010202072300', '20050325075505', '20050828053247'], 'to': '20100626141610'},  # becomes a redirect to tvi24 after
    {'site': 'sicnoticias.sapo.pt'},
    {'site': 'rtp.pt'},
    {'site': 'dn.pt'},
    {'site': 'tsf.pt'},
    {
        'site': 'jn.pt',
        'encoding': {
            '20040605042739-20080314182313': 'utf-8'
        },
        'ignore': [
            '20011014000211', '20011103001652', '20011107005932', '20011107010100', '20011108003840', '20011108010152', '20011116002347', '20011116002419', '20011117011734', '20011128004742',
            '20021125205745', '20030218052808', '20030407162709', '20030624151104', '20031030000220', '20031214025515', '20031225105031', '20040612021612', '20040616183544', '20081022054919',
            '20090926013934', '20091218091852', '20060826115813', '20060826202309', '20080215063034', '20081022054919', '20081022055157', '20081022063817', '20090522005146',  '20090623195309',
            '20100606104209', '20110621150208', '20131115102830', '20100706140103'
        ]
    },
    {'site': 'visao.sapo.pt'},
    {'site': 'expresso.pt'},
    {'site': 'sol.sapo.pt'},
    {'site': 'tvi24.iol.pt'},

    {'site': 'destak.pt'},
    {'site': 'sapo.pt'},
    # {'site': 'cmjornal.pt'},
    # {'site': 'cmjornal.xl.pt'},
    {'site': 'ionline.pt'},
    {'site': 'lux.iol.pt'},
    {'site': 'meiosepublicidade.pt'},
    {'site': 'oprimeirodejaneiro.pt', 'to': '20071231235959'},

    # regional
    {'site': 'dnoticias.pt'},

    # musica
    {'site': 'blitz.pt'},

    # economia
    {'site': 'dinheirovivo.pt'},
    {'site': 'jornaldenegocios.pt'},
    {'site': 'economico.sapo.pt'},

    # desporto
    {'site': 'abola.pt'},
    {'site': 'ojogo.pt'},
    {'site': 'maisfutebol.iol.pt'},
    {'site': 'record.pt'},

    # informatica
    {'site': 'exameinformatica.clix.pt'},
    {'site': 'pcguia.pt'},

    # {'site': '24.sapo.pt'},  # starts 2015
    {'site': 'observador.pt'},  # starts 2013
]


# def get_snapshot_list_api(source):
#     params = {
#         'versionHistory': source['site'],
#         'to': source.get('to') or '20131231235959',
#         'maxItems': 200
#     }
#
#     if 'from' in source:
#         params['from'] = source['from']
#
#     r = requests.get('https://arquivo.pt/textsearch', params)
#     data = r.json()
#
#     if 'response_items' not in data or len(data['response_items']) == 0:
#         print('\tNo results')
#         return
#
#     dates = set()
#     snapshots = []
#     while 'response_items' in data and len(data['response_items']) > 0:
#         for item in data['response_items']:
#             # if this day in history was already crawled continue (1 snapshot per day only)
#             if item['tstamp'][:8] in dates:
#                 continue
#             dates.add(item['tstamp'][:8])
#
#             snapshots.append({
#                 'tstamp': item['tstamp'],
#                 'linkToArchive': item['linkToArchive'],
#                 'linkToNoFrame': item['linkToNoFrame'],
#                 'linkToScreenshot': item['linkToScreenshot']
#             })
#
#         data = requests.get(data['next_page']).json()
#
#     return snapshots

def is_ignored(source, timestamp):
    if 'ignore' not in source:
        return False

    if timestamp in source['ignore']:
        return True

    ignore_intervals = [ignore for ignore in source['ignore'] if '-' in ignore]
    for min, max in [interval.split('-') for interval in ignore_intervals]:
        if min <= timestamp <= max:
            return True

    return False


def get_encoding(source, timestamp):
    if 'encoding' not in source:
        return None

    if timestamp in source['encoding']:
        return source['encoding'][timestamp]

    intervals = [ignore for ignore in source['encoding'].keys() if '-' in ignore]
    for key in intervals:
        min, max = key.split('-')
        if min <= timestamp <= max:
            return source['encoding'][key]

    return None


def get_snapshot_list_cdx(source):
    params = {
        'output': 'json',
        'fields': 'url,timestamp',
        'filter': '!~status:4|5',
        'url': source['site'],
        'to': source.get('to') or '20131231235959'
    }

    if 'from' in source:
        params['from'] = source['from']

    r = requests.get('https://arquivo.pt/wayback/cdx', params).text
    data = [json.loads(line) for line in r.split('\n') if line and len(line) > 0]

    dates = set()
    snapshots = []
    for line in data:
        # if this day in history was already crawled continue (1 snapshot per day only)
        if line['timestamp'][:8] in dates:
            continue

        if is_ignored(source, line['timestamp']):
            continue

        dates.add(line['timestamp'][:8])

        snapshots.append({
            'tstamp': line['timestamp'],
            'linkToArchive': 'https://arquivo.pt/wayback/{}/{}'.format(line['timestamp'], line['url']),
            'linkToNoFrame': 'https://arquivo.pt/noFrame/replay/{}/{}'.format(line['timestamp'], line['url']),
            'linkToScreenshot': 'https://arquivo.pt/screenshot?url=https://arquivo.pt/noFrame/replay/{}/{}'.format(line['timestamp'], line['url'])
        })
    return snapshots


def analyse_snapshot_list(snapshots):
    years = Counter()
    months = Counter()
    first = 2020
    last = 0

    for snapshot in snapshots:
        day = snapshot['tstamp'][6:8]
        month = snapshot['tstamp'][4:6]
        year = snapshot['tstamp'][:4]

        years[year] += 1

        # get all historic months represented
        # TODO
        months[year + month] += 1

        # get interval extremes
        if int(year) < first:
            first = int(year)
        if int(year) > last:
            last = int(year)

    print('\tTotal snapshots {}'.format(len(snapshots)))
    print('\tRange {}-{}'.format(first, last))

    return first, last, months, years


def get_page_content(url, encoding):
    r = requests.get(url)
    encoding = encoding or chardet.detect(r.content)['encoding'] or 'utf-8'

    actual_url_redirect = get_actual_source(r.url)  # source isn't always the same as expected, see 'jn.pt' vs 'jn.sapo.pt'

    return r.content.decode(encoding, errors='replace'), actual_url_redirect.replace(':', '*')


def get_page(url, encoding):
    element = True
    while element and url:
        content, actual_url = get_page_content(url, encoding)
        soup = BeautifulSoup(content, features='html5lib')

        # follows meta refresh tags if existent
        element = soup.find('meta', attrs={'http-equiv': 'refresh'})
        if element and 'content' in element and '=' in element['content']:
            url = element['content'].partition('=')[2]
        else:
            element = None

    return content, actual_url


def crawl_source(source, download=True):
    print('Crawl ' + source['site'])

    img_dir = os.path.join('crawled', source['site'], 'screenshots')
    page_dir = os.path.join('crawled', source['site'], 'pages')

    if download:
        pathlib.Path(img_dir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(page_dir).mkdir(parents=True, exist_ok=True)

    snapshots = get_snapshot_list_cdx(source)
    stats = analyse_snapshot_list(snapshots)

    if len(snapshots) == 0:
        print('\tNo results')
        return

    special_requests = source.get('special') or {}

    downloads = 0

    days = Counter()
    for snapshot in snapshots:
        calendar_day = snapshot['tstamp'][4:8]
        days[calendar_day] += 1

        if download:
            downloads += 1
            https = '-s' if is_https_link(snapshot['linkToArchive']) else '-p'

            # save screenshot and source code
            img = os.path.join(img_dir, snapshot['tstamp'] + https + '.png')
            if not os.path.exists(img):
                snapshot_link = snapshot['linkToScreenshot']
                if snapshot['tstamp'] in special_requests:  # use this if for some reason need to request a different link for a day
                    snapshot_link += special_requests[snapshot['tstamp']]

                r = requests.get(snapshot_link)
                with open(img, 'wb') as f:
                    f.write(r.content)

            page = os.path.join(page_dir, snapshot['tstamp'] + https + '.html')
            if not os.path.exists(page):  # by adding the source url to the filename this becomes unnecessary, since we can't predict the filename before making the request
                page_link = snapshot['linkToNoFrame']
                if snapshot['tstamp'] in special_requests:  # use this if for some reason need to request a different link for a day
                    page_link += special_requests[snapshot['tstamp']]

                # get page content
                encoding = get_encoding(source, snapshot['tstamp'])
                content, actual_url = get_page(page_link, encoding)

                # get the actual url
                if actual_url:
                    page = os.path.join(page_dir, snapshot['tstamp'] + https + '-' + actual_url + '.html')

                with open(page, 'w') as f:
                    f.write(content)

    print('\tTotal downloaded {}'.format(downloads))
    # print('\tTotal reqs ' + str(reqs))
    print('\tCoverage {:.2%} ({})'.format(len(days)/366.0, len(days)))
    print(stats[3].most_common())

    return stats, len(snapshots), days


def crawl_all(sources):
    all_years = Counter()
    all_days = Counter()
    first = 2020
    last = 0
    total_snapshots = 0
    all_months = Counter()

    for source in sources:
        res = crawl_source(source)
        if not res:
            continue

        stats, snapshots, days = res

        if stats[0] < first:
            first = stats[0]
        if stats[1] > last:
            last = stats[1]

        total_snapshots += snapshots
        all_years += stats[3]
        all_months += stats[2]

        all_days += days

    print(sorted(((v, k) for k, v in all_days.items()), reverse=True))
    print('Total snapshots {}'.format(total_snapshots))
    print('Total range {}-{}'.format(first, last))
    print('Total coverage {:.2%} ({})'.format(len(all_days)/366.0, len(all_days)))
    print(all_years.most_common())
    print(sorted(all_months))

    # for i in range(2000,2013):
    #    count = 0
    #    for k in all_months.keys():
    #        if k.startswith(str(i)):
    #            count += 1
    #    print('{} coverage {:.2%} ({})'.format(i, count / 12.0, count))


crawl_all(news_sources)
