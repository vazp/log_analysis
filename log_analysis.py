#!/usr/bin/env python

import psycopg2
import sys

DBNAME = 'news'

def connect(database_name):
    """Connect to the PostgreSQL database. Returns a database connection"""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print "Unable to connect to database"
        sys.exit(1)

def get_query_results(query):
    database, cursor = connect(DBNAME)
    cursor.execute(query)
    results = cursor.fetchall()

    database.close()

    return results

def print_top_articles():
    query = """
    SELECT ar.title, cl.count
    FROM articles ar, condensed_log cl
    WHERE cl.path = '/article/' || ar.slug
    ORDER BY cl.count DESC
    LIMIT 3;"""

    results = get_query_results(query)

    print '\n1. What are the most popular three articles of all time?'
    for row in results:
        print ' "{:25s}" -- {:6d} views'.format(row[0], row[1])

def print_top_authors():
    query = """
    SELECT au.name, SUM(cl.count)
    FROM articles ar, authors au, condensed_log cl
    WHERE cl.path = '/article/' || ar.slug AND ar.author = au.id
    GROUP BY au.name
    ORDER BY sum DESC;"""

    results = get_query_results(query)

    print '\n2. Who are the most popular article authors of all time?'
    for row in results:
        print ' {:25s} -- {:6f} views'.format(row[0], row[1])

def print_top_error_days():
    query = """
    SELECT date, error_percent
    FROM requests_per_day
    WHERE error_percent > 1
    ORDER BY date;"""

    results = get_query_results(query)

    print '\n3. On which days did more than 1% of requests lead to errors?'
    for row in results:
        print ' {:%B %d, %Y} -- {:f}% errors'.format(row[0], row[1])
    print''

if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_top_error_days()
