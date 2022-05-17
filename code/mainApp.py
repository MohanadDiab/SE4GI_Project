from psycopg2 import (connect)
from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    )

app=Flask(__name__,template_folder="templates")

app.secret_key= b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/viewMap')
def viewMap():
    return render_template('viewMap.html')

@app.route('/viewMap2')
def viewMap2():
    return render_template('viewMap2.html')

@app.route('/reserveBike',methods=['GET','POST'])
def reserveBike():
    if request.method=='POST':
        return 'Reserved bike number: ' + request.form['bikeNumber']
    return '''
<form method="post">
<p><label>Insert bike number: </label><input type=text name=bikeNumber>
<p><input type=submit value=Ok>
</form> '''



if __name__ == '__main__':
    app.run(debug=True)