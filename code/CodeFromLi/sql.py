import psycopg2

def connect_sql():
    conn = psycopg2.connect(database="postgres", user="postgres", password="Always30Points", host="104.168.68.237", port="5432")
    c = conn.cursor()
    return (conn,c)

if __name__ == '__main__':
    (conn,c) = connect_sql()