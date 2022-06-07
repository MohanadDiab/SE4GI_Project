from psycopg2 import(connect)

# setup db connection (generic connection path to the server Li setup)
#hostname='104.168.68.237'
#database='postgres'
#username='postgres'
#pwd='Always30Points'
#port_id=5432

# connection on local databse
conn = connect(database="postgres", user="postgres", password="Always30Points", host="104.168.68.237", port="5432")


if conn is None:
    print ("Connection not established")
else:
    print ("Connection established")
cur = conn.cursor()

cleanup=(
    'DROP TABLE IF EXISTS users CASCADE'
    )

command="""
    CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(255) UNIQUE NOT NULL,
    user_password VARCHAR(255) NOT NULL
    )
    """
    

sqlCommands=(
    'INSERT INTO users (user_name, user_password) VALUES (%s, %s) RETURNING user_id'
    )


cur.execute(cleanup)
    
cur.execute(command)
    
cur.execute(sqlCommands, ('Giuseppe', '3ety3e7'))
userId = cur.fetchone()[0]
print(cur.fetchall())
cur.close()
conn.commit()
conn.close() 

  
    