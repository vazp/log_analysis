# Log analysis
Full Stack Web Developer Nanodegree

This script makes use of the news PostgreSQL database provided by Udacity as
part of the Full Stack Web Developer Nanodegree

To make the script work correctly, two views must be added to the database
using the following commands

CREATE VIEW condensed_log AS
	SELECT ar.title as article, au.name as author, l.path, l.status
	FROM articles ar, log l, authors au
	WHERE l.path LIKE '%' || ar.slug || '%' and au.id = ar.author;

CREATE VIEW requests_per_day AS
  SELECT t1.date, t1.total, t2.ok, t3.error, round((cast (t3.error as decimal) / t1.total * 100), 3) as error_percent
	FROM (
    SELECT date(time) as date, count(status) as total
    FROM log
	  WHERE path LIKE '/article%'
    GROUP BY date) t1
	LEFT JOIN (
    SELECT date(time) as date, count(status) as ok
    FROM log
    WHERE path LIKE '/article%' AND status = '200 OK'
    GROUP BY date) t2 ON t1.date = t2.date
	LEFT JOIN (
    SELECT date(time) as date, count(status) as error
    FROM log
    WHERE path LIKE '/article%' AND status = '404 NOT FOUND'
    GROUP BY date) t3 ON t1.date = t3.date;

The script connects to the database using the psycopg2 library and then
performs three queries that answer the following questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?
