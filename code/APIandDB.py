from psycopg2 import (connect)
import pandas as pd

###
command="""
    Create  TABLE test(
        test_id SERIAL PRIMARY KEY,
        test_name VARCHAR(255) NOT NULL,
        num integer
        )
"""

###
sqlInsert= """ 
    INSERT INTO test(test_name, num)
    VALUES(%s,%s) RETURNING test_id;
"""

sqlQuery= """SELECT * FROM test;"""

###
hostname='localhost'
database='Demo'
username='postgres'
pwd='flairspot1'
port_id=5432

conn = connect(
    host=hostname,
    dbname=database,
    user=username,
    password=pwd,
    port=port_id
    )
cur = conn.cursor()
cur.execute(command)

for i in range(10):
    name = input('insert a tuple name: ')
    num = int(input('insert a number: '))
    cur.execute(sqlInsert, (name, num))
    test_id = cur.fetchone()[0]
    print(test_id, '\n')
    
cur.execute(sqlQuery)
print(cur.fetchall())
cur.close()
conn.commit()
conn.close()
