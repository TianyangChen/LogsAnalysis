#! /usr/bin/env python
import psycopg2

# init some variables
DBNAME = "news"
QUERY1 = """
SELECT A.title, count(*) as num
FROM articles A,
    (SELECT RIGHT(log.path, POSITION('/' in REVERSE(log.path)) -1 ) as path
    FROM log) L
WHERE A.slug=L.path
GROUP BY A.title
ORDER BY num DESC LIMIT 3;
"""
QUERY2 = """
SELECT A.title, count(*) as num
FROM articles A, log L
WHERE A.slug=L.path
GROUP BY A.title
ORDER BY num DESC LIMIT 3;
"""
QUERY3 = """
SELECT date, percentage
FROM
    (SELECT ER.date,
    ROUND(CAST(100*ER.num as numeric)/CAST(AL.num as numeric),1)
        as percentage
    FROM
        (SELECT DATE(time) as date, count(*) as num
        FROM log
        WHERE status<>'200 OK'
        GROUP BY DATE(time)) ER,
        (SELECT DATE(time) as date, count(*) as num
        FROM log
        GROUP BY DATE(time)) AL
        WHERE ER.date=AL.date) ANS
WHERE percentage>1;
"""


# This function connect to database DBNAME
def connect(DBNAME):
    try:
        pg = psycopg2.connect("database={}".format(DBNAME))
        cursor = pg.cursor()
        return pg, cursor
    except:
        print "<error: cannot connect to database {}>".format(DBNAME)


# This function execute QUERY and return results
def execute_query(QUERY, DBNAME):
    db, cursor = connect(DBNAME)
    cursor.execute(QUERY)
    posts = cursor.fetchall()
    db.close()
    return posts

# run our 3 queries
posts1 = execute_query(QUERY1, DBNAME)
posts2 = execute_query(QUERY2, DBNAME)
posts3 = execute_query(QUERY3, DBNAME)

# format the output
print ""
print "***************************************"
print "Most popular three articles of all time"
print "***************************************"
for x in posts1:
    print x[0]+" -- "+str(x[1])+" views"
print ""
print "****************************************"
print "Most popular article authors of all time"
print "****************************************"
for x in post2:
    print x[0]+" -- "+str(x[1])+" views"
print ""
print "***************************************"
print "More than 1% of requests lead to errors"
print "***************************************"
for x in post3:
    print str(x[0])+" -- "+str(x[1])+"% errors"
print ""
