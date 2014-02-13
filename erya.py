from flask import Flask, g, render_template, request, redirect
import conf
import sqlite3

############################################################
app = Flask(__name__)
app_debug = conf.debug

############################################################
@app.before_request
def before_request():
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect(conf.database)
        g.c = g.db.cursor()

############################################################
@app.teardown_request
def teardown_request(e):
    if hasattr(g, 'c'):
        g.c.close()
    if hasattr(g, 'db'):
        g.db.close()

############################################################
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/', methods = ['POST'])
def search():
    if not request.form['keyword']:
        return render_template('search.html')

    keyword = request.form['keyword']

    sql = 'select id, title, type, answer from erya where title like ? limit 30'
    g.c.execute(sql, ('%' + keyword + '%',) )
    results = [dict(id = it[0], title = it[1], type = it[2], answer = it[3]) for it in g.c.fetchall()]

    return render_template('search.html', results = results)

############################################################
if __name__ == '__main__':
    app.run()
