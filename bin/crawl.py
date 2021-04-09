from glob import glob
import json
import os
from collections import Counter

import re
import chardet
import requests
import pathlib

from bs4 import BeautifulSoup

from config.crawl_config import news_sources
from src.util import is_https_link, get_actual_source, encode_url


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
        element = soup.find('meta', attrs={'http-equiv': re.compile(r'R|refresh')})
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


# configurations are in config/sources.py
crawl_all(news_sources)
