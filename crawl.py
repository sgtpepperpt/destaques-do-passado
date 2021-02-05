import random

import requests

sources = [
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
    {'site': 'exameinformatica.pt'},
    {'site': 'pcguia.pt'},

    {'site': '24.sapo.pt'},  # starts 2015
    {'site': 'observador.pt'},  # starts 2013
]


all_days = dict()

min = 2020
max = 0
total_snapshots = 0
for source in sources:
    print('Crawl ' + source['site'])

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
        continue

    snapshots = 0
    reqs = 1
    first = 2020
    last = 0
    days = set()
    squashed_days = set()
    while 'response_items' in data and len(data['response_items']) > 0:
        for item in data['response_items']:
            snapshots += 1

            # if random.randint(0, 10000) > 9988:
            #     print(item['linkToArchive'])

            y = int(item['tstamp'][:4])
            if y < min:
                min = y
            if y > max:
                max = y
            if y < first:
                first = y
            if y > last:
                last = y

            # if this day in history was already crawled continue (1 snapshot per day only)
            if item['tstamp'][:8] in days:
                continue
            days.add(item['tstamp'][:8])

            # the date which we care about
            squashed_days.add(item['tstamp'][4:8])

        data = requests.get(data['next_page']).json()
        reqs += 1

    for day in days:
        if day[4:] not in all_days:
            all_days[day[4:]] = 1
        else:
            all_days[day[4:]] += 1

    total_snapshots += snapshots
    print('\tTotal snapshots {} (w/o same-day crawls {})'.format(snapshots, len(days)))
    # print('\tTotal reqs ' + str(reqs))
    print('\tRange {}-{}'.format(first, last))
    print('\tCoverage {:.2%} ({})'.format(len(squashed_days)/366.0, len(squashed_days)))


print(sorted(((v, k) for k, v in all_days.items()), reverse=True))
print(len(all_days))
print('Total range {}-{}'.format(min, max))
print('Total snapshots {}'.format(total_snapshots))
