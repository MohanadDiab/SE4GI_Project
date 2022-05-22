from psycopg2 import (connect)
from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    )

# setup db connection (generic connection path to the server Li setup)
#hostname='104.168.68.237'
#database='postgres'
#username='postgres'
#pwd='Always30Points'
#port_id=5432

# connection on local databse
hostname='localhost'
database='se4g'
username='postgres'
pwd='flairspot1'
port_id=5432


app=Flask(__name__,template_folder="templates")

app.secret_key= b'_5#y2L"F4Q8z\n\xec]/'

### functions section ###

# Welcome page (get started)
@app.route('/',methods=['GET'])
def Home():
    return render_template('Home.html')
# Sign in page
@app.route('/signIn',methods=['GET','POST'])
def signIn():
    if request.method=='POST':
        new_user=request.form['username']
        new_password=request.form['password']
        conn = connect(host=hostname,database=database,user=username,password=pwd)
        cur = conn.cursor()
        sqlInsert = """INSERT INTO users(user_name, user_password)
        VALUES(%s, %s) RETURNING user_id;"""
        cur.execute(sqlInsert, (new_user, new_password))
        cur.close()
        conn.commit()
        conn.close() 
        return redirect(url_for('Home'))
    return render_template('signIn.html')

# sign up page
@app.route('/signUp',methods=['GET','POST'])
def signUp():
    if request.method=='POST':
        new_user=request.form['username']
        new_password=request.form['password']
        conn = connect(host=hostname,database=database,user=username,password=pwd)
        cur = conn.cursor()
        sqlInsert = """INSERT INTO users(user_name, user_password)
        VALUES(%s, %s) RETURNING user_id;"""
        cur.execute(sqlInsert, (new_user, new_password))
        cur.close()
        conn.commit()
        conn.close()
        return redirect(url_for('signIn'))
    return render_template('signUp.html')


if __name__ == '__main__':
    app.run(debug=True)