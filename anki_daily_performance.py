import json
import sqlite3


def main():
    conn = sqlite3.connect('collection.anki2')
    c = conn.cursor()
    # the DB structure is documented here:
    # https://github.com/ankidroid/Anki-Android/wiki/Database-Structure
    # cards younger than 10 days are ignored to reduce the bias from new cards
    query = """
    SELECT
        day,
        AVG(ease),
        COUNT(1)
    FROM
        (
            SELECT
                DATE(rl.id / 1000, 'unixepoch', 'localtime') AS day,
                rl.ease
            FROM
                revlog rl
                    JOIN cards c
                        ON rl.cid = c.id
            WHERE
                rl.id - c.id > 1000 * 60 * 60 * 24 * 10
        ) agg
    GROUP BY
        agg.day
    ORDER BY
        agg.day
    """
    with open('anki_daily_performance.jsonl', 'w') as fw:
        for row in c.execute(query):
            fw.write(json.dumps(dict(
                day=row[0],
                avg_ease=row[1],
            )))
            fw.write('\n')

    conn.close()


if __name__ == '__main__':
    main()
