import os
import random
from collections import Counter

import chardet
import requests
import pathlib

from util import is_https_link

news_sources = [
    {'site': 'news.google.pt', 'from': '20051124000000'},
    {'site': 'publico.pt'},
    {'site': 'sabado.pt'},
    {'site': 'diariodigital.pt'},
    {'site': 'iol.pt'},
    {'site': 'aeiou.pt'},
    {'site': 'portugaldiario.iol.pt'},
    {'site': 'sicnoticias.sapo.pt'},
    {'site': 'rtp.pt'},
    {'site': 'dn.pt'},
    {'site': 'tsf.pt'},
    {'site': 'jn.pt'},
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


def crawl_source(source, download=True):
    print('Crawl ' + source['site'])

    img_dir = os.path.join('crawled', source['site'], 'screenshots')
    page_dir = os.path.join('crawled', source['site'], 'pages')

    if download:
        pathlib.Path(img_dir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(page_dir).mkdir(parents=True, exist_ok=True)

    params = {
        'versionHistory': source['site'],
        'to': source.get('to') or '20131231235959',
        'maxItems': 200
    }

    if 'from' in source:
        params['from'] = source['from']

    r = requests.get('https://arquivo.pt/textsearch', params)
    data = r.json()

    if 'response_items' not in data or len(data['response_items']) == 0:
        print('\tNo results')
        return

    snapshots = 0
    reqs = 1
    first = 2020
    last = 0
    dates = set()
    days = Counter()
    while 'response_items' in data and len(data['response_items']) > 0:
        for item in data['response_items']:
            # if this day in history was already crawled continue (1 snapshot per day only)
            if item['tstamp'][:8] in dates:
                continue
            dates.add(item['tstamp'][:8])

            snapshots += 1

            # if random.randint(0, 10000) > 9988:
            #     print(item['linkToArchive'])

            year = int(item['tstamp'][:4])
            calendar_day = item['tstamp'][4:8]
            if year < first:
                first = year
            if year > last:
                last = year

            days[calendar_day] += 1

            if download:
                https = '-s' if is_https_link(item['linkToArchive']) else '-p'

                # save screenshot and source code
                img = os.path.join(img_dir, item['tstamp'] + https + '.png')
                r = requests.get(item['linkToScreenshot'])
                with open(img, 'wb') as f:
                    f.write(r.content)

                page = os.path.join(page_dir, item['tstamp'] + https + '.html')
                r = requests.get(item['linkToNoFrame'])
                encoding = item.get('encoding') or chardet.detect(r.content)['encoding']
                with open(page, 'w') as f:
                    f.write(r.content.decode(encoding))

        data = requests.get(data['next_page']).json()
        reqs += 1

    print('\tTotal snapshots {}'.format(snapshots))
    # print('\tTotal reqs ' + str(reqs))
    print('\tRange {}-{}'.format(first, last))
    print('\tCoverage {:.2%} ({})'.format(len(days)/366.0, len(days)))

    return first, last, snapshots, days


def crawl(sources):
    all_days = Counter()
    first = 2020
    last = 0
    total_snapshots = 0

    for source in sources:
        first_year, last_year, snapshots, days = crawl_source(source)

        if first_year < first:
            first = first_year
        if last_year > last:
            last = last_year

        total_snapshots += snapshots

        all_days += days

    print(sorted(((v, k) for k, v in all_days.items()), reverse=True))
    print('Total snapshots {}'.format(total_snapshots))
    print('Total range {}-{}'.format(first, last))
    print('Total coverage {:.2%} ({})'.format(len(all_days)/366.0, len(all_days)))


crawl(news_sources)
