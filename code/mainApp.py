from flask import (
    Flask, render_template, request, redirect, flash, url_for, session, g
)

from werkzeug.security import check_password_hash, generate_password_hash

from werkzeug.exceptions import abort

from psycopg2 import (
        connect
)

import json

# setup db connection (generic connection path to the server Li setup)
#hostname='104.168.68.237'
#database='postgres'
#username='postgres'
#pwd='Always30Points'
#port_id=5432

app=Flask(__name__,template_folder="templates")

app.secret_key= b'_5#y2L"F4Q8z\n\xec]/'

### functions section ###
def get_dbConn():
    if 'dbConn' not in g:
        myFile = open('dbConfig.txt')
        connStr = myFile.readline()
        g.dbConn = connect(database="postgres", user="postgres", password="Always30Points", host="104.168.68.237", port="5432")
    
    return g.dbConn

def close_dbConn():
    if 'dbConn' in g:
        g.dbComm.close()
        g.pop('dbConn')


### Guest section ###
## home page, login, logout, sign up ##

# Welcome page (get started)

@app.route('/',methods=['GET'])
def Home():
    return render_template('Home.html')

# Sign in page

@app.route('/signIn',methods=['GET','POST'])
def signIn():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_dbConn()
        cur = conn.cursor()
        error = None
        cur.execute(
            'SELECT * FROM users WHERE user_name = %s', (username,)
        )
        user = cur.fetchone()
        cur.close()
        conn.commit()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[1]
            
            return 'welcome '+session['user_id']#redirect(url_for('Home')) 
            

        flash(error)

    return render_template('signIn.html')

# sign up page

@app.route('/signUp',methods=['GET','POST'])
def signUp():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        repassword=request.form['repassword']
        error = None
        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif repassword != password:
            error= 'Passwords do not match'
        else :
            conn = get_dbConn()
            cur = conn.cursor()
            cur.execute(
            'SELECT user_id FROM users WHERE user_name = %s', (username,))
            if cur.fetchone() is not None:
                error = 'Username {} is already taken.'.format(username)
                cur.close()
        
        if error is None:
            error='Account created successfully!'
            conn = get_dbConn()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO users (user_name, user_password) VALUES (%s, %s)',
                (username, generate_password_hash(password))
            )
            cur.close()
            conn.commit()
            flash(error)
            return redirect(url_for('signIn'))
        flash(error)
        
    return render_template('signUp.html')


# Sign out function

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signIn'))

### Normal user section ###
## Maps functions ##

# Normal map function

@app.route('/map_1')
def map_1():
    conn = get_dbConn()
    cur = conn.cursor()
    sql='select * from "Housing Data"'
    cur.execute(sql)
    result = cur.fetchall()
    return render_template('map_1.html', title='Housing Data Display', result=result)

# Normal map function

@app.route('/map_2')
def map_2():
    conn = get_dbConn()
    cur = conn.cursor()
    sql='select "1_Location.latitude","1_Location.longitude","6_Decibel_reading" from "Housing Data"'
    cur.execute(sql)
    result = cur.fetchall()
    return render_template('map_2.html', title='Housing Data Display', result=result,resultLength=len(result))

# Normal map function

@app.route('/map_3')
def map_3():
    conn = get_dbConn()
    cur = conn.cursor()
    sql='select * from "Housing Data"'
    cur.execute(sql)
    result = cur.fetchall()
    return render_template('map_3.html', title='Housing Data Display', result=result)



if __name__ == '__main__':
    app.debug = True
    app.run(port=80)