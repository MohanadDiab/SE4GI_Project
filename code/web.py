import os
import time
from flask import (
    Flask, render_template, request, redirect, flash, url_for, session, g
)

from werkzeug.security import check_password_hash, generate_password_hash

from psycopg2 import (
    connect
)

import json

# setup db connection (generic connection path to the server Li setup)
# hostname='104.168.68.237'
# database='postgres'
# username='postgres'
# pwd='Always30Points'
# port_id=5432

app = Flask(__name__, template_folder="templates")

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


### functions section ###
def get_dbConn():
    if 'dbConn' not in g:
        myFile = open('dbConfig.txt')
        txt = myFile.readline()
        connJson = json.loads(txt)
        g.dbConn = connect(database=connJson['database'], user=connJson['user'], password=connJson['password'], host=connJson['host'],port=connJson['port'])
    return g.dbConn


def close_dbConn():
    if 'dbConn' in g:
        g.dbComm.close()
        g.pop('dbConn')


### Guest section ###
## home page, login, logout, sign up ##

# Welcome page (get started)

@app.route('/', methods=['GET'])
def Home():
    if 'user_id' in session:
        return render_template('Home_logged_in.html')
    else:
        return render_template('Home.html')


# Sign in page

@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
    if 'user_id' in session:
        error = 'You are already signed in!'
        flash(error)
        return render_template('signIn_ex.html')
    else:
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

                return redirect(url_for('maps'))

            flash(error)

        return render_template('signIn.html')


# sign up page

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if 'user_id' in session:
        error = 'You are already signed in!, You can sign up a new account when you sign out!'
        flash(error)
        return render_template('signUp_ex.html')
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            repassword = request.form['repassword']
            error = None

            if not username:
                error = 'Username is required.'
            elif len(username)<5:
                error = 'Username should be at least 5 characters long'
            elif ' ' in username:
                error = 'Uername cannot contain spaces, use underscore instead'
            elif not password:
                error = 'Password is required.'
            elif ' ' in password:
                error = 'Password cannot contain spaces, use underscore instead'
            elif repassword != password:

                error= 'Passwords do not match'
            elif len(password) < 5:
                    error = 'Password should be at least 5 characters long'
            else:
                conn = get_dbConn()
                cur = conn.cursor()
                cur.execute(
                    'SELECT user_id FROM users WHERE user_name = %s', (username,))
                if cur.fetchone() is not None:
                    error = 'Username {} is already taken.'.format(username)
                    cur.close()

            if error is None:
                error = 'Account created successfully!'
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
    if 'user_id' in session:
        session.clear()
        error = 'logged out seccessfully'
        flash(error)
    else:
        error = 'You were not logged in'
        flash(error)
    return redirect(url_for('signIn'))


@app.route('/index')
def index():
    if 'user_id' in session:
        return 'hello ' + session['user_id']
    else:
        return 'not logged in'


@app.route('/about')
def about():
    if 'user_id' in session:
        return render_template('about_logged_in.html')
    else:
        return render_template('about.html')


### Normal user section ###

## Profile section ##

@app.route('/profile')
def profile():
    if 'user_id' in session:
        return render_template('profile.html',user_name=session['user_id'])
    else:
        return render_template('blocked.html')
    
@app.route('/myRequests',methods=['GET','POST'])
def myRequests():
    if 'user_id' in session:
        if request.method == 'POST':
            northing = request.form['coord']
            conn = get_dbConn()
            cur = conn.cursor()
            cur.execute(
                'DELETE FROM "Housing Data" WHERE ec5_uuid = %s AND "1_Location.latitude" = %s ',(session['user_id'],northing,)
                )
            cur.close()
            conn.commit()
            return redirect(url_for('myRequests'))
            
        conn = get_dbConn()
        cur = conn.cursor()
        cur.execute(
            'SELECT "3_Dwelling_type","4_Number_of_trees","5_Distance_to_major_","6_Decibel_reading","8_Age_of_Property","9_Quality_of_housing","1_Location.latitude" FROM "Housing Data" WHERE ec5_uuid = %s', (session['user_id'],)
        )
        requests = cur.fetchall()
        cur.close()
        conn.commit()
        return render_template('my_requests.html',requests=requests)
    else:
        return render_template('blocked.html')
    
@app.route('/changepw',methods=['GET','POST'])
def changepw():
    if 'user_id' in session:
        if request.method == 'POST':
            oldPassword = request.form['oldPassword']
            newPassword = request.form['newPassword']
            reNewPassword=request.form['reNewPassword']
            conn = get_dbConn()
            cur = conn.cursor()
            error = None
            cur.execute(
                'SELECT * FROM users WHERE user_name = %s', (session['user_id'],)
            )
            user = cur.fetchone()
            cur.close()
            conn.commit()

            if not check_password_hash(user[2], oldPassword):
                error = 'Incorrect password.'
            elif ' ' in newPassword:
                error = 'Password cannot contain spaces, use underscore instead'
            elif reNewPassword != newPassword:
                error= 'Passwords do not match'
            elif len(newPassword) < 5:
                    error = 'Password should be at least 5 characters long'

            if error is None:
                conn = get_dbConn()
                cur = conn.cursor()
                error = 'Password changed successfully'
                cur.execute(
                    'UPDATE users SET user_password=%s WHERE user_name = %s', (generate_password_hash(newPassword),session['user_id'],)
                )
                cur.close()
                conn.commit()
                flash(error)
                return redirect(url_for('changepw')) 
                
            flash(error)

        return render_template('changepw.html')
    else:
        return render_template('blocked.html')

## Maps functions ##

@app.route('/maps')
def maps():
    if 'user_id' in session:
        return render_template('maps.html')
    else:
        return render_template('blocked.html')

## Charts functions ##

@app.route('/charts')
def charts():
    if 'user_id' in session:
        return render_template('charts.html')
    else:
        return render_template('blocked.html')


# Normal map function

@app.route('/map_1')
def map_1():
    if 'user_id' in session:
        conn = get_dbConn()
        cur = conn.cursor()
        sql = 'select * from "Housing Data"'
        cur.execute(sql)
        result = cur.fetchall()
        return render_template('map_1.html', title='Housing Data Display', result=result)
    else:
        return render_template('blocked.html')


# Normal map function

@app.route('/map_2')
def map_2():
    if 'user_id' in session:
        conn = get_dbConn()
        cur = conn.cursor()
        sql = 'select "1_Location.latitude","1_Location.longitude","6_Decibel_reading" from "Housing Data"'
        cur.execute(sql)
        result = cur.fetchall()
        return render_template('map_2.html', title='Housing Data Display', result=result, resultLength=len(result))
    else:
        return render_template('blocked.html')


# Normal map function

@app.route('/map_3')
def map_3():
    if 'user_id' in session:
        conn = get_dbConn()
        cur = conn.cursor()
        sql = 'select * from "Housing Data"'
        cur.execute(sql)
        result = cur.fetchall()
        return render_template('map_3.html', title='Housing Data Display', result=result)
    else:
        return render_template('blocked.html')


# Normal map function
@app.route('/map_4')
def map_4():
    if 'user_id' in session:
        conn = get_dbConn()
        cur = conn.cursor()
        sql = 'select * from "Housing Data"'
        cur.execute(sql)
        result = cur.fetchall()
        return render_template('map_4.html', title='Housing Data Adding', result=result)
    else:
        return render_template('blocked.html')
    
@app.route('/guide')
def guide():
    if 'user_id' in session: 
        return render_template('guide.html')

    else:
        return render_template('blocked.html')

# line chart
@app.route('/chart_1')
def chart_1():
    if 'user_id' in session:
        conn = get_dbConn()
        cur = conn.cursor()
        sql = 'select "8_Age_of_Property",count(*) from "Housing Data" group by "8_Age_of_Property" order by "8_Age_of_Property" asc'
        cur.execute(sql)
        result = cur.fetchall()
        return render_template('chart_1.html', result=result)
    else:
        return render_template('blocked.html')


# pie chart
@app.route('/chart_2')
def chart_2():
    if 'user_id' in session:
        conn = get_dbConn()
        cur = conn.cursor()
        sql = 'select "4_Number_of_trees",count(*) from "Housing Data" group by "4_Number_of_trees"'
        cur.execute(sql)
        result = cur.fetchall()
        return render_template('chart_2.html', result=result)
    else:
        return render_template('blocked.html')


# bar chart
@app.route('/chart_3')
def chart_3():
    if 'user_id' in session:
        conn = get_dbConn()
        cur = conn.cursor()
        sql = 'select "5_Distance_to_major_",count(*) from "Housing Data" group by "5_Distance_to_major_"'
        cur.execute(sql)
        result = cur.fetchall()
        return render_template('chart_3.html', result=result)
    else:
        return render_template('blocked.html')


@app.route('/submitData', methods=['POST'])
def submitData():
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    img = request.files.get('photo')
    ht = request.form.get('ht', '')
    _not = request.form.get('not', '')
    d2mr = request.form.get('d2mr', '')
    dr = request.form.get('dr', '')
    aop = request.form.get('aop', '')
    if (img.filename == '' or ht == '' or _not == '' or d2mr == '' or dr == '' or aop == ''):
        return '<script>alert("Uploaded unsuccessfully!Check the values you input.");window.location.href = "./map_4";</script>'
    conn = get_dbConn()
    cur = conn.cursor()
    suffix = '.' + img.filename.split('.')[-1]
    basedir = os.path.abspath(os.path.dirname(__file__))
    photo = '/static/uploads/' + str(int(time.time())) + suffix
    img_path = basedir + photo
    img.save(img_path)
    print(img_path)
    print(photo, ht, _not)
    sql = 'insert into "Housing Data" (ec5_uuid,"2_Take_photo","3_Dwelling_type","4_Number_of_trees","5_Distance_to_major_","6_Decibel_reading","8_Age_of_Property","9_Quality_of_housing","1_Location.latitude","1_Location.longitude")values(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'-1\',\'{}\',\'{}\')'.format(
        session['user_id'], photo, ht, _not, d2mr, dr, aop, lat, lng)
    cur.execute(sql)
    conn.commit()
    return '<script>alert("Uploaded successfully!");window.location.href = "./map_4";</script>'


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=80)