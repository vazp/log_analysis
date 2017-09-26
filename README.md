# Log analysis
Full Stack Web Developer Nanodegree

This project was made on a Windows environment using Vagrant to run a Linux-based virtual machine with PostgreSQL and Python.
To set up the environment, you can download and install the following software:
 * [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
 * [Vagrant](https://www.vagrantup.com/downloads.html)

The virtual machine configuration file can be found [here](https://github.com/udacity/fullstack-nanodegree-vm)

The script makes use of the news PostgreSQL database provided by Udacity that can be downloaded [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

Once everything is downloaded and installed you can run the command *vagrant up* from the directory where the vagrantfile is located to start the virtual machine, and the command *vagrant ssh* to log in the virtual machine.

To load the database you can use the following command inside the virtual machine
```
psql -d news -f newsdata.sql
```

To make the script work correctly, two views must be added to the database
using the following commands
```
CREATE VIEW condensed_log AS
	SELECT path, COUNT(*) AS count
	FROM log
	WHERE status = '200 OK'
	GROUP BY path;

CREATE VIEW requests_per_day AS
	SELECT t1.date, ROUND((CAST (t2.error AS DECIMAL) / t1.total * 100), 3) AS error_percent
	FROM (
		SELECT date(time) AS date, COUNT(status) AS total
		FROM log
		GROUP BY date) t1
	LEFT JOIN (
		SELECT date(time) AS date, COUNT(status) AS error
		FROM log
		WHERE status = '404 NOT FOUND'
		GROUP BY date) t2 ON t1.date = t2.date;
```
The script connects to the database using the psycopg2 library and then
performs three queries that answer the following questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

To run the script you can use the following command
```
python log_analysis.py
```
