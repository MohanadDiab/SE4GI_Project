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
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
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
    cur.execute(
        """SELECT blog_user.user_name, post.title, post.body 
        FROM blog_user, post WHERE 
        blog_user.user_id = post.author_id"""
        )
    posts = cur.fetchall()
    print(posts)
    cur.close()
    conn.commit()
    return render_template('index3.html', title='Home', user=user, posts=posts)

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
