import json
import os
from collections import Counter

import chardet
import requests
import pathlib

from src.util import is_https_link

news_sources = [
    {'site': 'news.google.pt', 'from': '20051124000000'},
    {'site': 'publico.pt', 'special': {'20100910150634': '?fl=1', '20110703150815': '?mobile=no'}},
    {'site': 'ultimahora.publico.pt'},
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


def get_snapshot_list_api(source):
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

    dates = set()
    snapshots = []
    while 'response_items' in data and len(data['response_items']) > 0:
        for item in data['response_items']:
            # if this day in history was already crawled continue (1 snapshot per day only)
            if item['tstamp'][:8] in dates:
                continue
            dates.add(item['tstamp'][:8])

            snapshots.append({
                'tstamp': item['tstamp'],
                'linkToArchive': item['linkToArchive'],
                'linkToNoFrame': item['linkToNoFrame'],
                'linkToScreenshot': item['linkToScreenshot']
            })

        data = requests.get(data['next_page']).json()

    return snapshots


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
            if not os.path.exists(page):
                page_link = snapshot['linkToNoFrame']
                if snapshot['tstamp'] in special_requests:  # use this if for some reason need to request a different link for a day
                    page_link += special_requests[snapshot['tstamp']]

                r = requests.get(page_link)
                encoding = chardet.detect(r.content)['encoding'] or 'utf-8'
                with open(page, 'w') as f:
                    f.write(r.content.decode(encoding, errors='replace'))

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
