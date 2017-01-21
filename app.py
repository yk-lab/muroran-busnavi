#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import bottle
from bottle import HTTPError
from bottle import static_file, get, post, request, response
from bottle import TEMPLATE_PATH, jinja2_template as template
from models import Page, db_init, Company, CompanyName, Stop, StopName, StopPosition, StopTime, ServiceID, Service, ServiceDate, Trip
from sqlalchemy import or_, desc
from pytz import timezone
from datetime import datetime, date, time
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
app.config['RELOAD']  = True
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
    jst_now = datetime.now(timezone("Asia/Tokyo"))
    return template(
        'index.tpl.html',
        page={
            "title":"むろらんバスなび - 道南バス、室蘭市内のバス停・バス時刻案内",
            "discription":"道南バスの室蘭市内線のバス停地図の表示やバスの時刻表検索を行えます。平日・土日祝日にダイヤ対応。"
        },
        params={"day": jst_now.date(), "time": "%d:%02d" % (jst_now.hour, jst_now.minute // 10 * 10)},
        autoescape=True
    )

@app.route('/signin/')
def login():
    return template('login.tpl.html', autoescape=True)

@app.route('/signin/success/')
def login_success():
    return template('login_success.tpl.html', autoescape=True)

# Routing /Company
@app.route('/company/')
def company():
    return "Coming Soon!"

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
    return "Comming Soon!"

@app.route('/stops/:id')
def stop_detail(id, db):
    format = request.params.format
    stop = db.query(Stop).get(id)
    print(stop)
    if format == "json":
        return "todo"
    return template('stop/details.tpl.html',
            page={
                "title":stop.now_name().name + " - 駅・停留所 - むろらんバスなび",
            },
            stop=stop, autoescape=True)

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
    return template('stop/search.tpl.html',
                page={
                    "title": "バス停検索 - むろらんバスなび",
                },
                autoescape=True)

@app.route('/stop_times/')
def stop_times(db):
    if request.params.f_id and request.params.t_id:
        dt_now = datetime.now(timezone('Asia/Tokyo'))
        time_sec = -1
        time_obj = time(hour=dt_now.hour, minute=dt_now.minute)
        if request.params.time:
            t = request.params.time.split(":")
            if t[0] and t[1] and t[0].isdigit() and t[1].isdigit():
                time_sec = int(t[0]) * 3600 + int(t[1]) * 60
                time_obj = time(hour=int(t[0]), minute=int(t[1]), tzinfo=timezone('Asia/Tokyo'))
        if not time and time < 0:
            time_sec = dt_now.hour * 3600 + dt_now.minute * 60
            # request.params.replace("time", "%d:%02d" % (dt_now.hour, dt_now.minute))

        dt = datetime.now(timezone('Asia/Tokyo'))
        if request.params.day:
            d = request.params.day.split("-")
            if d[0] and d[1] and d[2] and d[0].isdigit() and d[1].isdigit() and d[2].isdigit():
                dt = datetime.combine(date(int(d[0]), int(d[1]), int(d[2])), time_obj)
        # ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        a_service_dates = db.query(ServiceDate).filter(ServiceDate.date == dt.astimezone(timezone("Asia/Tokyo")).date())
        if dt.weekday() == 0:
            a_service_weekday = db.query(Service).filter(Service.monday == 1, Service.start_date<=dt.astimezone(timezone("UTC")), Service.end_date >= dt.astimezone(timezone("UTC")))
        elif dt.weekday() == 1:
            a_service_weekday = db.query(Service).filter(Service.tuesday == 1, Service.start_date<=dt.astimezone(timezone("UTC")), Service.end_date >= dt.astimezone(timezone("UTC")))
        elif dt.weekday() == 2:
            a_service_weekday = db.query(Service).filter(Service.wednesday == 1, Service.start_date<=dt.astimezone(timezone("UTC")), Service.end_date >= dt.astimezone(timezone("UTC")))
        elif dt.weekday() == 3:
            a_service_weekday = db.query(Service).filter(Service.thursday == 1, Service.start_date<=dt.astimezone(timezone("UTC")), Service.end_date >= dt.astimezone(timezone("UTC")))
        elif dt.weekday() == 4:
            a_service_weekday = db.query(Service).filter(Service.friday == 1, Service.start_date<=dt.astimezone(timezone("UTC")), Service.end_date >= dt.astimezone(timezone("UTC")))
        elif dt.weekday() == 5:
            a_service_weekday = db.query(Service).filter(Service.saturday == 1, Service.start_date<=dt.astimezone(timezone("UTC")), Service.end_date >= dt.astimezone(timezone("UTC")))
        else:
            a_service_weekday = db.query(Service).filter(Service.sunday == 1, Service.start_date<=dt.astimezone(timezone("UTC")), Service.end_date >= dt.astimezone(timezone("UTC")))

        a_service_code = {w.service_code: True for w in a_service_weekday}
        for s in a_service_dates:
            if s.exception_type == 2:
                a_service_code[s.service_code] = False
            elif s.exception_type == 1:
                a_service_code[s.service_code] = True

        trips = db.query(Trip.id).filter(Trip.service_code.in_([k for k, s in a_service_code.items() if s == True]))
        f_stop_positions = db.query(StopPosition.id).filter(StopPosition.stop_code == request.params.f_id)
        t_stop_positions = db.query(StopPosition.id).filter(StopPosition.stop_code == request.params.t_id)
        f_stop_times = db.query(StopTime.trip_code).filter(StopTime.stop_code.in_(f_stop_positions), StopTime.trip_code.in_(trips), StopTime.departure_time > time_sec)
        t_stop_times = db.query(StopTime).filter(StopTime.stop_code.in_(t_stop_positions), StopTime.trip_code.in_(trips), StopTime.trip_code.in_(f_stop_times)).order_by(StopTime.departure_time).limit(15)

        stop_times = list()
        for t_stop_time in t_stop_times:
            st = db.query(StopTime).filter(StopTime.stop_code.in_(f_stop_positions), StopTime.trip_code == t_stop_time.trip_code, StopTime.stop_sequence < t_stop_time.stop_sequence).order_by(StopTime.stop_sequence.desc()).first()
            if st != None and {"from": st, "to": t_stop_time} not in stop_times:
#                print({"from": st, "to": t_stop_time})
#                print(stop_times)
                stop_times.append({"from": st, "to": t_stop_time})
        return template('stop_times/list.tpl.html', stop_times = stop_times, params = request.params, autoescape=True)
    elif not request.params.from_q or not request.params.to_q:
      response.status = 302
      redirect_url = '{0}://{1}/'.format(
                      request.urlparts.scheme, request.urlparts.netloc)
      response.set_header('Location', redirect_url)
    elif request.params.f_id and not request.params.t_id:
        # select t_id
        stopnames = db.query(StopName).filter(StopName.name.contains(request.params.to_q)).all()
        return template('stop_times/select_stop.tpl.html', params = request.params, select="t_id", stopnames=stopnames, request=request, autoescape=True)
    elif not request.params.f_id:
        # select f_id
        stopnames = db.query(StopName).filter(StopName.name.contains(request.params.from_q)).all()
        return template('stop_times/select_stop.tpl.html', params = request.params, select="f_id", stopnames=stopnames, request=request, autoescape=True)
    return "False"

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


#if app.config.get('RELOAD'):
print("Reload: true")
app.run(host='0.0.0.0', port=8080, reload=True, reloader=True)
#else:
#    app.run(host='0.0.0.0', port=8080)
