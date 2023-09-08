import mysql.connector

conn = mysql.connector.connect(host="127.0.0.1",port='3303',user="root",password="lotus",database="madhavone_xcomp7")
c = conn.cursor(dictionary=True )
c.execute("Select * From so")
rows = c.fetchall()
for row in rows:
    print(row)
