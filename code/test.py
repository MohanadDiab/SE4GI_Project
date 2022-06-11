from psycopg2 import (
    connect
)
import json

myFile = open('dbConfig.txt')
txt = myFile.readline()
connJson = json.loads(txt)
dbConn = connect(database=connJson['database'], user=connJson['user'], password=connJson['password'], host=connJson['host'],port=connJson['port'])
    



cur = dbConn.cursor()

cur.execute(
    'SELECT "3_Dwelling_type","4_Number_of_trees","5_Distance_to_major_","6_Decibel_reading","8_Age_of_Property","9_Quality_of_housing" FROM "Housing Data" WHERE ec5_uuid = %s', ('mohanad',)
)
requests = cur.fetchall()
cur.close()
dbConn.commit()

test=requests[0]
test2=requests[1]

