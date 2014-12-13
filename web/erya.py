#-*- coding:utf-8 -*-

from flask import Flask, g, render_template, request, make_response, abort, jsonify
from hashlib import md5
import MySQLdb
import memcache
import conf

############################################################
app = Flask(__name__)
app_debug = conf.debug

############################################################
def sql_query(keyword):
    if not hasattr(g, 'db'):
        g.db = MySQLdb.connect(
                host    = conf.db_host,
                port    = conf.db_port,
                user    = conf.db_user,
                passwd  = conf.db_passwd,
                db      = conf.db_name,
                charset = 'utf8')
    c = g.db.cursor()

    sql = '''select title, type, answer from `erya` where title like %s limit 30'''
    c.execute(sql, ('%' + unicode(keyword) + '%', ))
    result = [dict(title = it[0], type = it[1], answer = it[2]) for it in c.fetchall()]
    return result

############################################################
def get_data(keyword):
    key = md5(unicode(keyword).encode('utf-8')).hexdigest()
    if not hasattr(g, 'mc'):
        g.mc = memcache.Client(conf.memcached)
    mc = g.mc

    data = mc.get(key)
    if data == None:
        data = sql_query(keyword)
        mc.add(key, data)
    return data

############################################################
@app.teardown_request
def teardown_request(e):
    if hasattr(g, 'db'):
        g.db.close()

############################################################
@app.route('/', methods = ['GET', 'POST'])
def index():
    response = None

    if request.method == 'GET':
        response = make_response(render_template('index.html'))

    if request.method == 'POST':
        # if not request.referrer.startswith('https://example.com/'):
        #     abort(403)

        result = []
        keyword = request.form.get('keyword')
        result = get_data(keyword)

        response = jsonify(keyword = keyword, result = result)

    # response.headers['Access-Control-Allow-Origin'] = 'https://example.com'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response

############################################################
if __name__ == '__main__':
    app.run(host='0.0.0.0')
