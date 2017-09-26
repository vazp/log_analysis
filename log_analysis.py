#!/usr/bin/env python

import psycopg2

DBNAME = 'news'

database = psycopg2.connect(database=DBNAME)
cursor = database.cursor()

print '\n1. What are the most popular three articles of all time?'

query = """
SELECT article, count(path)
FROM condensed_log
WHERE status = '200 OK'
GROUP BY article
ORDER BY count DESC
LIMIT 3;"""

cursor.execute(query)

for row in cursor.fetchall():
    print ' "{:s}" -- {:d} views'.format(row[0], row[1])

print '\n2. Who are the most popular article authors of all time?'

query = """
SELECT author, count(path)
FROM condensed_log
WHERE status = '200 OK'
GROUP BY author
ORDER BY count DESC;"""

cursor.execute(query)

for row in cursor.fetchall():
    print ' {:s} -- {:d} views'.format(row[0], row[1])

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
