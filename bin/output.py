import json
import sqlite3
import threading

from src.util import remove_destaques_uniqueness


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


def count_category(cursor, day, month, category):
    res = cursor.execute('''
            WITH stats AS (
                SELECT snippet IS NOT NULL AS has_snippet, COALESCE(img_urls.status = 200, FALSE) AS has_image FROM articles
                LEFT OUTER JOIN urls AS img_urls on articles.img_url = img_urls.url
                WHERE day = ? AND month = ? AND category = ?
            )
            SELECT
                (SELECT COUNT(*) FROM stats) AS total,
                (SELECT COUNT(*) FROM stats WHERE has_snippet OR has_image) AS large,
                (SELECT COUNT(*) FROM stats WHERE NOT has_snippet AND NOT has_image) AS small
        ''', (day, month, category)).fetchall()[0]

    return {
        'total': res[0],
        'large': res[1],
        'small': res[2]
    }


def get_day_stats(cursor, day, month):
    total_articles = cursor.execute('SELECT COUNT(*) FROM articles WHERE day = ? AND month = ?', (day, month)).fetchall()[0][0]
    with_snippet = cursor.execute('SELECT COUNT(*) FROM articles WHERE day = ? AND month = ? AND snippet IS NOT NULL', (day, month)).fetchall()[0][0]
    with_img = cursor.execute('SELECT COUNT(*) FROM articles WHERE day = ? AND month = ? AND img_url IS NOT NULL AND (SELECT status NOT IN (404,400,500,0) FROM urls WHERE url = img_url)', (day, month)).fetchall()[0][0]

    categories = {
        'Genérico': count_category(cursor, day, month, 'Genérico'),
        'Desporto': count_category(cursor, day, month, 'Desporto'),
        'Portugal': count_category(cursor, day, month, 'Portugal'),
        'Mundo': count_category(cursor, day, month, 'Mundo'),
        'Economia': count_category(cursor, day, month, 'Economia'),
        'Entretenimento': count_category(cursor, day, month, 'Entretenimento'),
        'Ciência': count_category(cursor, day, month, 'Ciência'),
        'Saúde': count_category(cursor, day, month, 'Saúde'),
        'Política': count_category(cursor, day, month, 'Política'),
        'Cultura': count_category(cursor, day, month, 'Cultura'),
        'Educação': count_category(cursor, day, month, 'Educação'),
        'Tecnologia': count_category(cursor, day, month, 'Tecnologia'),
        'Sociedade': count_category(cursor, day, month, 'Sociedade'),
        'Local': count_category(cursor, day, month, 'Local'),
        'Ambiente': count_category(cursor, day, month, 'Ambiente'),
        'Opinião': count_category(cursor, day, month, 'Opinião')
    }

    # only show categories with articles
    categories = {k: v for (k, v) in categories.items() if v['total'] > 0}

    years = cursor.execute('SELECT DISTINCT year FROM articles WHERE day = ? AND month = ?', (day, month)).fetchall()
    years = sorted([year[0] for year in years])

    return {
        'total': total_articles,
        'snippets': with_snippet,
        'imgs': with_img,
        'categories': categories,
        'years': years
    }


def produce_output(cursor, global_stats, days):
    # threads only
    if not cursor:
        cursor = sqlite3.connect('parsed_articles.db').cursor()

    for day, month in days:
        print('{:02}/{:02}'.format(day, month))
        stats = get_day_stats(cursor, day, month)

        if global_stats:
            global_stats['totals'].append(stats['total'])
            global_stats['snippet'].append(stats['snippets'])
            global_stats['img'].append(stats['imgs'])
            global_stats['large_cats'].append(len([c for c in stats['categories'] if stats['categories'][c]['large'] >= 2 and stats['categories'][c]['total'] >= 6]))
            global_stats['medium_cats'].append(len([c for c in stats['categories'] if stats['categories'][c]['large'] >= 1 and stats['categories'][c]['total'] >= 3]))
            global_stats['small_cats'].append(len([c for c in stats['categories'] if stats['categories'][c]['total'] >= 4]))

        # write file
        res = cursor.execute('''SELECT
                                    --COALESCE(article_urls.redirect_url, articles.article_url) AS article_url, -- this leads to noFrame articles unfortunately
                                    articles.article_url,
                                    arquivo_source_url,
                                    title,
                                    source,
                                    year,
                                    category,
                                    importance,
                                    headline,
                                    snippet,
                                    COALESCE(img_urls.redirect_url, articles.img_url) AS img_url,
                                    article_urls.status = 200 AS has_article_url,
                                    img_urls.status = 200 AS has_img_url
                                FROM (SELECT * FROM articles WHERE day = ? AND month = ? ORDER BY year ASC)  AS articles
                                LEFT OUTER JOIN urls AS article_urls ON articles.article_url = article_urls.url
                                LEFT OUTER JOIN urls AS img_urls on articles.img_url = img_urls.url
                                ''', (day, month)).fetchall()

        daily_news = []
        for row in res:
            # some publico images seem like they're there but they're an empty placeholder
            has_img_url = row[11] and not row[9].endswith('pxTransparente.gif')

            daily_news.append({
                'article_url': remove_destaques_uniqueness(row[0]),
                'arquivo_source_url': row[1],
                'title': row[2],
                'source': row[3],
                'year': row[4],
                'category': row[5],
                'importance': row[6],
                'pretitle': row[7],
                'snippet': row[8],
                'img_url': row[9] if has_img_url else None,
                'has_article_url': row[10]
            })

        # write to file
        with open('out/{:02}{:02}.json'.format(month, day), 'w', newline='') as file:
            file.write(json.dumps({
                'metadata': stats,
                'articles': daily_news
            }))


def main(thread_count=1):
    conn = sqlite3.connect('parsed_articles.db')
    cursor = conn.cursor()
    days = cursor.execute('SELECT DISTINCT day,month FROM articles ORDER BY month,day').fetchall()

    global_stats = {
        'totals': [],
        'snippet': [],
        'img': [],
        'large_cats': [],
        'medium_cats': [],
        'small_cats': []
    }

    if thread_count > 1:
        parts = list(split(days, thread_count))

        thread_objs = []
        for i in range(thread_count):
            thread = threading.Thread(target=produce_output, args=(None, None, parts[i]))
            thread.start()
            thread_objs.append((thread, conn))

        for t, conn in thread_objs:
            t.join()
            conn.close()
    else:
        produce_output(cursor, global_stats, days)
        print('{} {} {} / {} {} {}'.format(min(global_stats['totals']), min(global_stats['snippet']),  min(global_stats['img']), min(global_stats['large_cats']), min(global_stats['medium_cats']), min(global_stats['small_cats'])))

    # close main connection
    conn.close()


main(8)
