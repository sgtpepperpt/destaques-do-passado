import json
import sqlite3


def count_category(cursor, day, month, category):
    return cursor.execute('SELECT COUNT(*) FROM articles WHERE day = ? AND month = ? AND category = ?', (day, month, category)).fetchall()[0][0]


def get_day_stats(cursor, day, month):
    total_articles =  cursor.execute('SELECT COUNT(*) FROM articles WHERE day = ? AND month = ?', (day, month)).fetchall()[0][0]
    with_snippet = cursor.execute('SELECT COUNT(*) FROM articles WHERE day = ? AND month = ? AND snippet IS NOT NULL', (day, month)).fetchall()[0][0]
    with_img = cursor.execute('SELECT COUNT(*) FROM articles WHERE day = ? AND month = ? AND img_url IS NOT NULL', (day, month)).fetchall()[0][0]

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

    return {
        'total': total_articles,
        'snippets': with_snippet,
        'imgs': with_img,
        'categories': categories
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
        res = cursor.execute('''SELECT article_url,arquivo_source_url,title,source,year,category,importance,headline,snippet,img_url,
                                    (SELECT status != 404 FROM urls WHERE url = article_url) AS has_article_url,(SELECT status != 404 FROM urls WHERE url = img_url) AS has_img_url
                                    FROM articles WHERE day = ? AND month = ?''', (day, month)).fetchall()

        daily_news = []
        for row in res:
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
                'img_url': row[9],
                'has_article_url': row[10],
                'has_img_url': row[11]
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
