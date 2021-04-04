from glob import glob
import json
import os
from collections import Counter

import chardet
import requests
import pathlib

from bs4 import BeautifulSoup

from src.util import is_https_link, get_actual_source, encode_url

# pages can be ignored via timestamp or range of timestamps, eg if page didn't change in consecutive days or there was a page error
# encoding can be defined like timestamps
news_sources = [
    {
        'site': 'news.google.pt',
        'from': '20051124000000'
    },
    {
        'site': 'publico.pt',
        'special': {'20100910150634': '?fl=1', '20110703150815': '?mobile=no'},
        'ignore': ['19961013180344', '19990421171920-20001203173200']
    },
    {
        'site': 'portugaldiario.iol.pt',
        'ignore': ['20001119134000', '20001202055200', '20010202072300', '20050325075505', '20050828053247'],
        'to': '20100626141610'  # becomes a redirect to tvi24 after
    },
    {
        'site': 'jn.pt',
        'encoding': {
            '20040605042739-20080314182313': 'utf-8'
        },
        'ignore': [
            '20011014000211', '20011103001652', '20011107005932', '20011107010100', '20011108003840', '20011108010152', '20011116002347', '20011116002419', '20011117011734', '20011128004742',
            '20021125205745', '20030218052808', '20030407162709', '20030624151104', '20031030000220', '20031214025515', '20031225105031', '20040612021612', '20040616183544', '20081022054919',
            '20090926013934', '20091218091852', '20060826115813', '20060826202309', '20080215063034', '20081022054919', '20081022055157', '20081022063817', '20090522005146',  '20090623195309',
            '20100606104209', '20110621150208', '20131115102830', '20100706140103', '20150416191052-20150505170210'
        ]
    },
    {
        'site': 'expresso.pt',
        'ignore': [
            '20000303215339', '20000304003451', '20000511112040', '20000614221642-20000815100152', '20001019034724-20010519195029', '20010924001343', '20010930112729', '20011002002004',
            '20011014233012', '20010930234309', '20011021145713', '20011022031247', '20011028041447', '20011029044539', '20011104005540', '20011105005759', '20011111012646', '20011112013327',
            '20011114004021', '20011125030751', '20011126050422', '20011202173222', '20011209175945', '20030327225541', '20030408155413', '20011021154458', '20011022040823', '20011028212409',
            '20011029054219', '20011104014656', '20011105022015', '20011111014527', '20011114010516', '20011125161129', '20011202184517', '20011209191928', '20011023013327', '20011104140315',
            '20011106011738', '20011111140017', '20011115021401', '20011116000618', '20011116080231', '20040606233331-20040612075222', '20040626033600-20040701060606', '20040724050140',
            '20040725065449', '20051223054221', '20070614005353', '20040903045728-20041215022252', '20050401233212-20050621185523', '20051124222130', '20051125040706', '20051225095630-20051231182511',
            '20090925190706-20091218062538', '20060102013519', '20060103082829', '20060108135453', '20060101042421', '20060102045952', '20060101123534', '20060102081843', '20091218182923',
            '20060101153422', '20060102113344', '20060101172409', '20060102153620', '20060101201140', '20060102173036', '20060101233307', '20060102205258', '20060102234035', '20061023050337',
            '20070614005353', '20090628235239'
        ]
    },
    {
        'site': 'dn.pt',
        'ignore': ['19971210080753-20011217081100',  # use the first alternative source
                   '20011001070732-20011216025543',  # period where it redirects to lusomundo, which was only archived in 2005
                   '20020117114627-20040618191302',  # use the second alternative source
                   # redirected to sapo.pt
                   '20041112090609', '20041113094530', '20041124092713', '20041126011101', '20050204095321', '20050206084348', '20050331091414',
                   '20041126085901', '20050204233149', '20050206130903', '20050401090655', '20050419080718', '20050420085351', '20060705062020',
                   '20060820071734', '20060825232258', '20060826050346', '20060826185341',

                   # not found
                   '20110121225541',

                   # use the third alternative source
                   '20110522215801-20151013180422'
                   ]
    },
    {
        # it's best to do as a separate source, because special would force the main page's timestamp
        # onto a different page, and the capture dates for the special page might differ from the main's
        'site': 'dn.pt',
        'path': '/pri/sintpri.htm',
        'from': '19971210080753',
        'to': '20011001001039',  # after this and until 2002 it's the 30/09 edition repeated everytime
        'target': 'dn.pt'  # store as if it was this one
    },
    {
        'site': 'dn.sapo.pt',
        'path': '/homepage/homepage.asp',
        'from': '20020117114627',
        'to': '20040618191302',
        'target': 'dn.pt'  # store as if it was this one
    },
    {
        'site': 'dn.pt',
        'path': '/inicio/default.aspx',
        'from': '20110522215801',
        'to': '20151013180422',
        'target': 'dn.pt',  # store as if it was this one
        'ignore': ['20110621150217']
    },
    {'site': 'tsf.pt'},
    {'site': 'ultimahora.publico.pt'},
    {'site': 'sabado.pt'},

    {'site': 'iol.pt'},
    {'site': 'aeiou.pt'},
    {'site': 'sicnoticias.sapo.pt'},
    {'site': 'diariodigital.pt'},
    {'site': 'rtp.pt'},
    {'site': 'visao.sapo.pt'},
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

    intervals = [ignore for ignore in source['ignore'] if '-' in ignore]
    for min, max in [interval.split('-') for interval in intervals]:
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


def get_special(source, timestamp):
    if 'special' not in source:
        return None

    if timestamp in source['special']:
        return source['special'][timestamp]

    intervals = [ignore for ignore in source['special'].keys() if '-' in ignore]
    for key in intervals:
        min, max = key.split('-')
        if min <= timestamp <= max:
            return source['special'][key]

    return None


def get_snapshot_list_cdx(source):
    params = {
        'output': 'json',
        'fields': 'url,timestamp',
        'filter': '!~status:4|5',
        'url': source['site'] + (source.get('path') or ''),
        'to': source.get('to') or '20151231235959'
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

    return r.content.decode(encoding, errors='replace'), actual_url_redirect


def get_page(url, encoding):
    element = True
    while element and url:
        content, actual_url = get_page_content(url, encoding)
        soup = BeautifulSoup(content, features='html5lib')

        # follows meta refresh tags if existent, useful to get over interstitials
        element = soup.find('meta', attrs={'http-equiv': 'refresh'})
        if element and element.get('content') and '=' in element.get('content'):
            if element.get('content').startswith('0'):
                break

            new_url = element['content'].partition('=')[2]

            if new_url.startswith('/noFrame/replay'):
                # handle relative urls
                new_url = 'https://arquivo.pt' + new_url

            if new_url == url:
                break  # no changes, so stop looking

            url = new_url
        else:
            element = None

    return content, actual_url


def crawl_source(source, download=True):
    print('Crawl ' + source['site'] + (source.get('path') or ''))

    img_dir = os.path.join('crawled', source.get('target') or source['site'], 'screenshots')
    page_dir = os.path.join('crawled', source.get('target') or source['site'], 'pages')

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

            # use this if for some reason need to request a different link for a day
            special_url = get_special(source, snapshot['tstamp'])

            # save screenshot and source code
            img = os.path.join(img_dir, snapshot['tstamp'] + https + '.png')
            if not os.path.exists(img):
                snapshot_link = snapshot['linkToScreenshot']
                if special_url:
                    snapshot_link += special_url

                r = requests.get(snapshot_link)
                with open(img, 'wb') as f:
                    f.write(r.content)

            # only download if no file starting by the current timestamp exists
            page = os.path.join(page_dir, snapshot['tstamp'] + https + '*.html')  # '*' for glob only
            if len(glob(page)) == 0:
                link = snapshot['linkToNoFrame']
                if special_url:
                    link += special_url

                # get page content
                encoding = get_encoding(source, snapshot['tstamp'])
                content, actual_url = get_page(link, encoding)

                # get the actual url
                if actual_url:
                    actual_url = encode_url(actual_url + (source.get('path') or ''))
                    page = os.path.join(page_dir, snapshot['tstamp'] + https + '-' + actual_url + '.html')
                else:
                    page = os.path.join(page_dir, snapshot['tstamp'] + https + '.html')

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
