from flask import Flask, render_template, url_for

from sql import connect_sql

app = Flask(__name__, template_folder="template")
import json

@app.route('/map_1')
def map_1():
    (conn, c) = connect_sql()
    sql='select * from "Housing Data"'
    c.execute(sql)
    result = c.fetchall()
    return render_template('map_1.html', title='Housing Data Display', result=result)

@app.route('/map_2')
def map_2():
    (conn, c) = connect_sql()
    sql='select "1_Location.latitude","1_Location.longitude","6_Decibel_reading" from "Housing Data"'
    c.execute(sql)
    result = c.fetchall()
    return render_template('map_2.html', title='Housing Data Display', result=result,resultLength=len(result))

@app.route('/map_3')
def map_3():
    (conn, c) = connect_sql()
    sql='select * from "Housing Data"'
    c.execute(sql)
    result = c.fetchall()
    return render_template('map_3.html', title='Housing Data Display', result=result)
@app.route('/')
def hello_world():
    return 'hello world'

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=80)