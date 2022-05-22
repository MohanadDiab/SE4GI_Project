from flask import (
    Flask, render_template, request, redirect, flash, url_for, session, g
)

from werkzeug.security import check_password_hash, generate_password_hash

from werkzeug.exceptions import abort

from psycopg2 import (
        connect
)

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
        g.dbConn = connect(connStr)
    
    return g.dbConn

def close_dbConn():
    if 'dbConn' in g:
        g.dbComm.close()
        g.pop('dbConn')

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
            'SELECT * FROM blog_user WHERE user_name = %s', (username,)
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
            session['user_id'] = user[0]
            return redirect(url_for('Home'))

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
            conn = get_dbConn()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO users (user_name, user_password) VALUES (%s, %s)',
                (username, generate_password_hash(password))
            )
            cur.close()
            conn.commit()
            return redirect(url_for('signIn'))
        flash(error)
        
    return render_template('signUp.html')


if __name__ == '__main__':
    app.run(debug=True)