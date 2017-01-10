#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import bottle
from bottle import HTTPError
from bottle import static_file, get, post, request, response
from bottle import TEMPLATE_PATH, jinja2_template as template
from models import db_init, Company, CompanyName, Stop, StopName
from sqlalchemy import or_, desc
from datetime import datetime
from json_encoders import StopJSONEncoder
import json

# index.pyが設置されているディレクトリの絶対パスを取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# テンプレートファイルを設置するディレクトリのパスを指定
TEMPLATE_PATH.append(BASE_DIR + "/templates")
STATIC_DIR = os.path.join(BASE_DIR, 'static')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets/vendors')

app = bottle.Bottle()

# TODO: 0.13 が stable になったら使えるのでは？
# app.config.load_dict(ConfigDict().load_module('config'))
# それまでは直書き（時間があれば要改善）
app.config['SECRET_KEY'] = '9fpxcp7h'
app.config['DEBUG']   = True
app.config['RELOAD']  = False
app.config['BOTTLE_CHILD']   = True
app.config['DB.URL']   = 'mysql://bus_navi:bus_navi@db/bus_navi?charset=utf8mb4'
app.config['DB.ECHO']   = True
app.config['SQLALCHEMY_NATIVE_UNICODE'] = 'utf-8'

bottle.debug(app.config.get('DEBUG', False))
#TODO: os.environ['BOTTLE_CHILD']

db_init(app)

# static Rin files
@app.route('/assets/rin/<filename:path>')
def static_css(filename):
    return static_file(filename, root=ASSETS_DIR+"/Rin/dist")

# static files
@app.route('/static/<filename:path>')
def static(filename):
    return static_file(filename, root=STATIC_DIR)

@app.route('/')
def index():
    return template('index.tpl.html', autoescape=True)

@app.route('/signin/')
def login():
    return template('login.tpl.html', autoescape=True)

@app.route('/signin/success/')
def login_success():
    return template('login_success.tpl.html', autoescape=True)

@app.route('/hello')
def hello():
    return "Hello World!"

# Routing /Company
@app.route('/company/')
def company():
    return "Hello World!"

@app.route('/company/<id>/')
def company_detail(id, db):
    company = db.query(Company).first()
    if company:
        print(company)
        return template('company/details.tpl.html', company=company, autoescape=True)
    return HTTPError(404, 'Entity not found.')

# Routing /Company
@app.route('/stops/')
def stop():
    return "Hello World!"

@app.route('/stops/:id')
def stop_detail(id, db):
    format = request.params.format
    stop = db.query(Stop).get(id)
    print(stop)
    if format == "json":
        return "todo"
    return template('stop/details.tpl.html', stop=stop, autoescape=True)

@app.route('/stops/search/')
def stop_search(db):
    query = request.params.q
    format = request.params.format
    if query != None and query != "":
        # stops = db.query(Stop).filter(Stop.id.in_(db.query(StopName, StopName.stop_code).filter(StopName.name.contains(query))))
        print("query: %s" % query)
        stopnames = db.query(StopName).filter(StopName.name.contains(query)).all()
#        stopnames = db.query(StopName).filter(StopName.name.contains(query), StopName.application_start <= datetime.utcnow(), or_(StopName.application_end == None, StopName.application_end >= datetime.utcnow())).order_by(desc("stop_names.application_start")).all()
#        stops = db.query(Stop).filter(Stop.id.in_([i.stop_code for i in stopnames])).all()
        print(stopnames)
        if format == "json":
            response.content_type = 'application/json'
#            return json.dumps([stop.to_dict() for stop in stops])
            return json.dumps([{"stopname_id": stopname.id, "stop": stopname.stop.to_dict()} for stopname in stopnames])
        return template('stop/search_list.tpl.html', query = query, stopnames=stopnames, autoescape=True)
    return template('stop/search.tpl.html', autoescape=True)

@app.route('/stops/<id>/')
def stop_detail(id, db):
    stops = db.query(Stop).filter_by(id = id).first()
    if stops:
        print(stop)
        return template('stop/details.tpl.html', stop=stop, autoescape=True)
    return HTTPError(404, 'Stop not found.')

# Routing /admin
@app.route('/admin/stop/')
def admin_stop():
    return HTTPError(404, 'page not found.')

@app.route('/admin/stop/list/')
def admin_stop_list():
    return HTTPError(404, 'page not found.')

@app.route('/admin/stop/add/')
def admin_stop_add():
    return HTTPError(404, 'page not found.')


if app.config.get('RELOAD', False):
    print("Reload: true")
    app.run(host='0.0.0.0', port=8080, reload=True)
else:
    app.run(host='0.0.0.0', port=8080)
