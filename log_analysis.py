#!/usr/bin/env python

import psycopg2

DBNAME = 'news'

database = psycopg2.connect(database=DBNAME)
cursor = database.cursor()

print '\n1. What are the most popular three articles of all time?'

query = """
SELECT ar.title, cl.count
FROM articles ar, condensed_log cl
WHERE cl.path = '/article/' || ar.slug
ORDER BY cl.count DESC
LIMIT 3;"""

cursor.execute(query)

for row in cursor.fetchall():
    print ' "{:25s}" -- {:6d} views'.format(row[0], row[1])

print '\n2. Who are the most popular article authors of all time?'

query = """
SELECT au.name, SUM(cl.count)
FROM articles ar, authors au, condensed_log cl
WHERE cl.path = '/article/' || ar.slug AND ar.author = au.id
GROUP BY au.name
ORDER BY sum DESC;"""

cursor.execute(query)

for row in cursor.fetchall():
    print ' {:25s} -- {:6f} views'.format(row[0], row[1])

print '\n3. On which days did more than 1% of requests lead to errors?'

query = """
SELECT date, error_percent
FROM requests_per_day
WHERE error_percent > 1
ORDER BY date;"""

cursor.execute(query)

for row in cursor.fetchall():
    print ' {:%B %d, %Y} -- {:f}% errors'.format(row[0], row[1])
print''

database.close()
