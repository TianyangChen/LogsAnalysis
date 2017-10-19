import psycopg2

DBNAME = "news"

pg = psycopg2.connect(database=DBNAME)
c = pg.cursor()
c.execute(
    """UPDATE log
       SET path=RIGHT(log.path, POSITION('/' in REVERSE(log.path)) -1 );"""
)
c.execute(
    """SELECT A.title, count(*) as num
       FROM articles A, log L
       WHERE A.slug=L.path
       GROUP BY A.title
       ORDER BY num DESC LIMIT 3;"""
)
posts = c.fetchall()
c.execute(
    """SELECT AU.name, count(*) as num
       FROM articles AR, authors AU, log L
       WHERE AR.author=AU.id AND AR.slug=L.path
       GROUP BY AU.name
       ORDER BY num DESC;"""
)
post2 = c.fetchall()
c.execute(
    """SELECT date, percentage
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
       WHERE percentage>1;"""
)
post3 = c.fetchall()
pg.close()
print ""
print "***************************************"
print "Most popular three articles of all time"
print "***************************************"
for x in posts:
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
