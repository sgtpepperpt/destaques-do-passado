import json
import sqlite3


def count_category(cursor, day, month, category):
    return cursor.execute('SELECT COUNT(*) FROM articles WHERE day = ? AND month = ? AND category = ?', (day, month, category)).fetchall()[0][0]


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
    categories = {k: v for (k, v) in categories.items() if v > 0}

    years = cursor.execute('SELECT DISTINCT year FROM articles WHERE day = ? AND month = ?', (day, month)).fetchall()
    years = [year[0] for year in years]

    return {
        'total': total_articles,
        'snippets': with_snippet,
        'imgs': with_img,
        'categories': categories,
        'years': years
    }


def main():
    conn = sqlite3.connect('parsed_articles.db')
    cursor = conn.cursor()
    days = cursor.execute('SELECT DISTINCT day,month FROM articles ORDER BY month,day').fetchall()

    totals = []
    snippet = []
    img = []
    categories_over_5 = []
    categories_over_2 = []

    for day, month in days:
        print('{:02}/{:02}'.format(day, month))
        stats = get_day_stats(cursor, day, month)

        totals.append(stats['total'])
        snippet.append(stats['snippets'])
        img.append(stats['imgs'])
        categories_over_5.append(len([c for c in stats['categories'] if stats['categories'][c] > 5]))
        categories_over_2.append(len([c for c in stats['categories'] if stats['categories'][c] > 2]))

        # write file
        res = cursor.execute('''SELECT
                                    COALESCE(article_urls.redirect_url, articles.article_url) AS article_url,
                                    arquivo_source_url,
                                    title,
                                    source,
                                    year,
                                    category,
                                    importance,
                                    headline,
                                    snippet,
                                    COALESCE(img_urls.redirect_url, articles.img_url) AS img_url,
                                    COALESCE(NULLIF(article_urls.redirect_status, 0), article_urls.status) = 200 AS has_article_url,
                                    COALESCE(NULLIF(img_urls.redirect_status, 0), img_urls.status) = 200 AS has_img_url
                                FROM (SELECT * FROM articles WHERE day = ? AND month = ?)  AS articles
                                INNER JOIN urls AS article_urls ON articles.article_url = article_urls.url
                                LEFT OUTER JOIN urls AS img_urls on articles.img_url = img_urls.url
                                ''', (day, month)).fetchall()

        daily_news = []
        for row in res:
            # some publico images seem like they're there but they're an empty placeholder
            has_img_url = row[11] and not row[9].endswith('pxTransparente.gif')

            daily_news.append({
                'article_url': row[0],
                'arquivo_source_url': row[1],
                'title': row[2],
                'source': row[3],
                'year': row[4],
                'category': row[5],
                'importance': row[6],
                'headline': row[7],
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
    conn.close()

    print('{} {} {} {} {}'.format(min(totals), min(snippet), min(img), min(categories_over_5), min(categories_over_2)))


main()
