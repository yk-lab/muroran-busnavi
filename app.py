#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from logging import basicConfig, getLogger, DEBUG, INFO
import bottle
from bottle import HTTPError
from bottle import static_file, get, post, request, response
from bottle import TEMPLATE_PATH, jinja2_template as template
from models import Page, db_init, Company, CompanyName, Stop, StopName, StopPosition, StopTime, ServiceID, Service, ServiceDate, Trip, FareRule
from sqlalchemy import or_, desc, func
from datetime import datetime, date, time, timedelta, timezone
import pendulum
from json_encoders import StopJSONEncoder
import json
import markdown
import re
import base64
import mimetypes, uuid
import numpy as np
import urllib.parse
import mercantile
import pymongo
from quadkey import QuadkeyUtils
from lat_lng import dist_on_sphere
from slacker import Slacker

# Imports the Google Cloud client library
from google.cloud import storage

# index.pyが設置されているディレクトリの絶対パスを取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# テンプレートファイルを設置するディレクトリのパスを指定
TEMPLATE_PATH.append(BASE_DIR + "/templates")
STATIC_DIR = os.path.join(BASE_DIR, 'static')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets/vendors')
PAGES_PATH = os.path.join(BASE_DIR, "pages")
FEEDBACK_FILE_DIR = os.path.join(BASE_DIR, "uploaded/feedback-files")

app = bottle.Bottle()
bottle.BaseRequest.MEMFILE_MAX = 5000000

# Instantiates a client
storage_client = storage.Client()

# 設定を読み込む
with open('./config.json') as fp:
    app.config.load_dict(json.load(fp))

bottle.debug(app.config.get('DEBUG', False))

if app.config.get('DEBUG', False):
    basicConfig(level=DEBUG)
else:
    basicConfig(level=INFO)

logger = getLogger(__name__)

db_init(None, app)

# jinja2のfilterを設定
from bottle import BaseTemplate
BaseTemplate.settings.update({'filters': {'tojson': lambda content: json.dumps(content)}})

UTC = timezone(timedelta(hours=+0), 'UTC')
JST = timezone(timedelta(hours=+9), 'JST')

# static files
@app.route('/static/<filename:path>')
def static(filename):
    return static_file(filename, root=STATIC_DIR)

@app.route('/page/<filename:path>')
def page(filename):
    body = None
    filepath = os.path.join(PAGES_PATH, filename)
    if os.path.isfile(filepath + ".md"):
        with open(filepath + ".md", "r") as file:
            body = markdown.markdown(file.read())
    if body != None:
        titles = []
        m = re.search(r'<h1>(.*?)</h1>', body)
        if m:
            titles.append(m.group(1))
        titles.append("むろらんバスなび")
        return template('page.tpl.html', page={"title":" - ".join(titles)}, body=body, autoescape=True)
    return HTTPError(404, 'Page not found.'+STATIC_DIR)

@app.route('/')
def index():
    jst_now = datetime.now(JST)
    return template(
        'index.tpl.html',
        page={
            "title":"むろらんバスなび - 道南バス、室蘭市内のバス停・バス時刻案内",
            "discription":"道南バスの室蘭市内線のバス停地図の表示やバスの時刻表検索を行えます。平日・土日祝日にダイヤ対応。"
        },
        params={"day": jst_now.date(), "time": "%02d:%02d" % (jst_now.hour, jst_now.minute // 10 * 10)},
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
        logger.debug(company)
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
    lat = sum([sp.lat for sp in stop.positions if sp.availability])/len([sp.lat for sp in stop.positions if sp.availability])
    lng = sum([sp.lng for sp in stop.positions if sp.availability])/len([sp.lng for sp in stop.positions if sp.availability])
    dl = QuadkeyUtils.search_LoD_lat(500, float(lat))
    quadkey = mercantile.quadkey(
            *mercantile.tile(float(lng), float(lat), dl)
    )

    quadkeys = QuadkeyUtils.neighbors_quadkey(
        mercantile.quadkey_to_tile(
            QuadkeyUtils.cut_key(
                quadkey,
                dl
            )
        )
    )

    neighbor_stops = db.query(Stop).filter(
            Stop.id.in_(
                db.query(StopPosition.stop_code).filter(
                        or_(
                            StopPosition.quadkey.startswith(quadkeys[0]),
                            StopPosition.quadkey.startswith(quadkeys[1]),
                            StopPosition.quadkey.startswith(quadkeys[2]),
                            StopPosition.quadkey.startswith(quadkeys[3]),
                            StopPosition.quadkey.startswith(quadkeys[4]),
                            StopPosition.quadkey.startswith(quadkeys[5]),
                            StopPosition.quadkey.startswith(quadkeys[6]),
                            StopPosition.quadkey.startswith(quadkeys[7]),
                            StopPosition.quadkey.startswith(quadkeys[8])
                        )
                )
            )
    )

    n_stops = []
    for ns in neighbor_stops.all():
        if ns.id != stop.id:
            a_lat = sum([sp.lat for sp in ns.positions if sp.availability])/len([sp.lat for sp in ns.positions if sp.availability])
            a_lng = sum([sp.lng for sp in ns.positions if sp.availability])/len([sp.lng for sp in ns.positions if sp.availability])
            dist = dist_on_sphere((lat, lng), (a_lat, a_lng))
            if dist <= 0.500:
                n_stops.append({"stop": ns, "dist": int(round(dist * 1000, -1))})
        if n_stops:
            n_stops.sort(key=lambda x:x["dist"])

    #logger.debug("stops: %s" % neighbor_stops.all())

    if format == "json":
        return "todo"
    return template('stop/details.tpl.html',
            page={
                "title":stop.now_name().name + " - 駅・停留所 - むろらんバスなび",
            },
            stop=stop,
            neighbor_stops=n_stops, autoescape=True)

@app.route('/stops/search/')
def stop_search(db):
    query = request.params.q
    format = request.params.format
    if query != None and query != "":
        # stops = db.query(Stop).filter(Stop.id.in_(db.query(StopName, StopName.stop_code).filter(StopName.name.contains(query))))
        logger.debug("query: %s" % query)
        stopnames = db.query(StopName).filter(StopName.name.contains(query)).order_by(func.char_length(StopName.name))
#        stopnames = db.query(StopName).filter(StopName.name.contains(query), StopName.application_start <= datetime.utcnow(), or_(StopName.application_end == None, StopName.application_end >= datetime.utcnow())).order_by(desc("stop_names.application_start")).all()
#        stops = db.query(Stop).filter(Stop.id.in_([i.stop_code for i in stopnames])).all()
        logger.debug(stopnames)
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
        if request.params.f_id:
            stop = db.query(Stop).get(request.params.f_id)
            if stop.now_name().name != request.params.from_q:
                querys = []
                for key in request.query:
                    if key == "from_q":
                        querys.append((key, stop.now_name().name))
                    else:
                        querys.append((key, request.query.getunicode(key)))
                response.status = 302
                redirect_url = '{0}://{1}/stop_times/?{2}'.format(
                                request.urlparts.scheme, request.urlparts.netloc, urllib.parse.urlencode(querys))
                response.set_header('Location', redirect_url)
                return response
        if request.params.t_id:
            stop = db.query(Stop).get(request.params.t_id)
            if stop.now_name().name != request.params.to_q:
                querys = []
                for key in request.query:
                    if key == "to_q":
                        querys.append((key, stop.now_name().name))
                    else:
                        querys.append((key, request.query.getunicode(key)))
                response.status = 302
                redirect_url = '{0}://{1}/stop_times/?{2}'.format(
                                request.urlparts.scheme, request.urlparts.netloc, urllib.parse.urlencode(querys))
                response.set_header('Location', redirect_url)
                return response

        dt_now = datetime.now(JST)
        time_sec = -1
        time_obj = time(hour=dt_now.hour, minute=dt_now.minute)
        if request.params.time:
            t = request.params.time.split(":")
            if t[0] and t[1] and t[0].isdigit() and t[1].isdigit():
                time_sec = int(t[0]) * 3600 + int(t[1]) * 60
                time_obj = time(hour=int(t[0]), minute=int(t[1]), tzinfo=JST)
        if time_sec < 0:
            time_sec = dt_now.hour * 3600 + dt_now.minute * 60
            # request.params.replace("time", "%d:%02d" % (dt_now.hour, dt_now.minute))

        dt = datetime.now(JST)
        if request.params.day:
            d = request.params.day.split("-")
            if d[0] and d[1] and d[2] and d[0].isdigit() and d[1].isdigit() and d[2].isdigit():
                dt = datetime.combine(date(int(d[0]), int(d[1]), int(d[2])), time_obj)
        # ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        a_service_dates = db.query(ServiceDate).filter(ServiceDate.date == dt.astimezone(JST).date())
        if dt.weekday() == 0:
            a_service_weekday = db.query(Service).filter(Service.monday == 1, Service.start_date<=dt.astimezone(UTC), Service.end_date >= dt.astimezone(UTC))
        elif dt.weekday() == 1:
            a_service_weekday = db.query(Service).filter(Service.tuesday == 1, Service.start_date<=dt.astimezone(UTC), Service.end_date >= dt.astimezone(UTC))
        elif dt.weekday() == 2:
            a_service_weekday = db.query(Service).filter(Service.wednesday == 1, Service.start_date<=dt.astimezone(UTC), Service.end_date >= dt.astimezone(UTC))
        elif dt.weekday() == 3:
            a_service_weekday = db.query(Service).filter(Service.thursday == 1, Service.start_date<=dt.astimezone(UTC), Service.end_date >= dt.astimezone(UTC))
        elif dt.weekday() == 4:
            a_service_weekday = db.query(Service).filter(Service.friday == 1, Service.start_date<=dt.astimezone(UTC), Service.end_date >= dt.astimezone(UTC))
        elif dt.weekday() == 5:
            a_service_weekday = db.query(Service).filter(Service.saturday == 1, Service.start_date<=dt.astimezone(UTC), Service.end_date >= dt.astimezone(UTC))
        else:
            a_service_weekday = db.query(Service).filter(Service.sunday == 1, Service.start_date<=dt.astimezone(UTC), Service.end_date >= dt.astimezone(UTC))

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
        t_stop_times = db.query(StopTime).filter(StopTime.stop_code.in_(t_stop_positions), StopTime.trip_code.in_(trips), StopTime.trip_code.in_(f_stop_times)).order_by(StopTime.arrival_time).limit(20)

        stop_times = list()
        for t_stop_time in t_stop_times:
            st = db.query(StopTime).filter(StopTime.stop_code.in_(f_stop_positions), StopTime.trip_code == t_stop_time.trip_code, StopTime.stop_sequence < t_stop_time.stop_sequence, StopTime.departure_time > time_sec).order_by(StopTime.stop_sequence.desc()).first()
            if st != None and {"from": st, "to": t_stop_time} not in stop_times:
               # logger.debug({"from": st, "to": t_stop_time})
               # logger.debug(stop_times)
                stop_times.append({"from": st, "to": t_stop_time})
        fare = {(i.route_code, i.origin_code, i.destination_code): i for i in db.query(FareRule).filter(
            FareRule.application_start <= dt.astimezone(UTC),
            or_(
                FareRule.application_end == None,
                FareRule.application_end >= dt.astimezone(UTC)
            ),
            FareRule.origin_code.in_(f_stop_positions),
            FareRule.destination_code.in_(t_stop_positions)
        ).all()}
        return template('stop_times/list.tpl.html', stop_times=stop_times, fare=fare, params=request.params, autoescape=True)
    elif not request.params.from_q or not request.params.to_q:
      response.status = 302
      redirect_url = '{0}://{1}/'.format(
                      request.urlparts.scheme, request.urlparts.netloc)
      response.set_header('Location', redirect_url)
    elif request.params.f_id and not request.params.t_id:
        # select t_id
        if request.params.f_id:
            stop = db.query(Stop).get(request.params.f_id)
            if stop.now_name().name != request.params.from_q:
                querys = []
                for key in request.query:
                    if key == "from_q":
                        querys.append((key, stop.now_name().name))
                    else:
                        querys.append((key, request.query.getunicode(key)))
                response.status = 302
                redirect_url = '{0}://{1}/stop_times/?{2}'.format(
                                request.urlparts.scheme, request.urlparts.netloc, urllib.parse.urlencode(querys))
                response.set_header('Location', redirect_url)
                return response
        stopnames = db.query(StopName).filter(StopName.name.contains(request.params.to_q)).order_by(func.char_length(StopName.name))
        return template('stop_times/select_stop.tpl.html', params = request.params, select="t_id", stopnames=stopnames, request=request, autoescape=True)
    elif not request.params.f_id:
        # select f_id
        stopnames = db.query(StopName).filter(StopName.name.contains(request.params.from_q)).order_by(func.char_length(StopName.name))
        return template('stop_times/select_stop.tpl.html', params = request.params, select="f_id", stopnames=stopnames, request=request, autoescape=True)
    return "False"

@app.get('/passing_times/:trip_id')
def passing_times(trip_id, db):
    dt = None
    try:
        dt = pendulum.parse(request.params.datetime)
    except Exception as e:
        pass
    dt = dt if dt != None else pendulum.now()

    origin = int(request.params.origin) if request.params.origin and request.params.origin.isdigit() else 0
    if request.params.destination and request.params.destination.isdigit():
        destination = int(request.params.destination)
        stop_times = db.query(StopTime).filter(StopTime.trip_code == trip_id, StopTime.stop_sequence >= origin, StopTime.stop_sequence <= destination)
    else:
        stop_times = db.query(StopTime).filter(StopTime.trip_code == trip_id, StopTime.stop_sequence >= origin)
    stop_times = stop_times.order_by(StopTime.stop_sequence).all()
    destination = stop_times[-1].stop_sequence if len(stop_times) > 0 else 0

    fare = {i.destination_code: i for i in db.query(FareRule).filter(
        FareRule.application_start <= dt.in_tz("UTC"),
        or_(
            FareRule.application_end == None,
            FareRule.application_end >= dt.in_tz("UTC")
        ),
        FareRule.route_code == db.query(Trip).get(trip_id).route_code,
        FareRule.origin_code == stop_times[0].stop_code,
        FareRule.destination_code.in_([stop_time.stop_code for stop_time in stop_times])
    ).all()}

    return template('passing_times/modaal.html.j2', stop_times=stop_times, fare=fare, datetime=dt, origin=origin, destination=destination, now=pendulum.now(), autoescape=True)


# Routing /feedback
@app.post('/feedback/')
def post_feedback():
    if not request.get_header('Referer').startswith('https://muroran.bus-navi.yk-lab.net/'):
        # 投稿元が違うため
        return HTTPError(404, 'page not found.')
    if not request.get_header('User-Agent') or len(request.get_header('User-Agent')) < 10:
        # user agent チェック
        # ここは時間を見てしっかりやりたい
        return HTTPError(404, 'page not found.')
    # TODO: IP Address フィルタリング
    # TODO: 串ハネ

    data = request.json

    client = pymongo.MongoClient(host=app.config['FEEDBACK.DB.HOST'], port=app.config['FEEDBACK.DB.PORT'])
    feedback_db = client.feedback
    fb = feedback_db.feedback

    if fb.count_documents({'info.remote_addr': request.remote_addr, 'body.registered_on': {'$gt': datetime.now(UTC) - timedelta(hours=3)}}) > 5:
        # 同一 IP 連投規制
        return HTTPError(404, 'page not found.')
    if fb.count_documents({'body.registered_on': {'$gt': datetime.now(UTC) - timedelta(seconds=5)}}) > 1:
        # 全体の連投規制
        return HTTPError(404, 'page not found.')

    prefix, body = data['screenshot'].split(',', 2)
    matchOB = re.match(r"^data:([^;]+);(\w+)", prefix)
    if matchOB.group(2) == "base64":
        body = base64.b64decode(body)

    bucket_name = 'muroran-bn-feedback'
    ext = mimetypes.guess_extension(matchOB.group(1))
    filename = str(uuid.uuid4().hex) + ext
    file_url = f'https://storage.cloud.google.com/{bucket_name}/{filename}'
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_string(body, content_type=matchOB.group(1))

    result = fb.insert_one({
        "type": "issue",
        "body": {
            "text": data.get('description', ''),
            "file": filename,
            "registered_on": datetime.utcnow()
        },
        "status": "new",
        "info": {
            "user-agent": request.get_header('User-Agent'),
            "remote_addr": request.remote_addr
        }
    })

    if app.config.get('FEEDBACK.SLACK.TOKEN'):
        slack = Slacker(app.config['FEEDBACK.SLACK.TOKEN'])
        slack.chat.post_message(app.config['FEEDBACK.SLACK.CHANNEL'], "Feedback: "+ str(result.inserted_id))
        if data.get('description', ''):
            slack.chat.post_message(app.config['FEEDBACK.SLACK.CHANNEL'], data.get('description', ''))
        slack.chat.post_message(app.config['FEEDBACK.SLACK.CHANNEL'], "File: " + file_url)

    return str(result.inserted_id)

@app.get('/admin/feedback/')
def get_feedback():
    client = pymongo.MongoClient(host=app.config['FEEDBACK.DB.HOST'], port=app.config['FEEDBACK.DB.PORT'])
    feedback_db = client.feedback
    fb = feedback_db.feedback

    #return fb.find()[0]["body"]["text"]
    return HTTPError(404, 'page not found.')


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

@app.route('/api/v1.0/stop_search')
def api_v1_0_stop_search(db):
    response.content_type = 'application/json'
    search_type = request.params.type
    if search_type == "latlng":
        try:
            lat = float(request.params.lat)
            lng = float(request.params.lng)
        except ValueError:
            response.status = 400
            return json.dumps({"Error":[
                {"message": "Missed Required Params"}
            ]})
        try:
            radius = float(request.params.radius)
        except ValueError:
            radius = 750
        if radius < 30:
            radius = 30
        if lat >= -90 and lat <= 90 and lng >= -180 and lng <= 180:
            dl = QuadkeyUtils.search_LoD_lat(radius, lat)
            quadkeys = QuadkeyUtils.neighbors_quadkey(
                mercantile.quadkey_to_tile(
                    QuadkeyUtils.cut_key(
                        mercantile.quadkey(*mercantile.tile(lng, lat, dl)),
                        dl
                    )
                )
            )

            near_stops = db.query(Stop).filter(
                    Stop.id.in_(
                        db.query(StopPosition.stop_code).filter(
                                or_(
                                    StopPosition.quadkey.startswith(quadkeys[0]),
                                    StopPosition.quadkey.startswith(quadkeys[1]),
                                    StopPosition.quadkey.startswith(quadkeys[2]),
                                    StopPosition.quadkey.startswith(quadkeys[3]),
                                    StopPosition.quadkey.startswith(quadkeys[4]),
                                    StopPosition.quadkey.startswith(quadkeys[5]),
                                    StopPosition.quadkey.startswith(quadkeys[6]),
                                    StopPosition.quadkey.startswith(quadkeys[7]),
                                    StopPosition.quadkey.startswith(quadkeys[8])
                                )
                        )
                    )
            )

            stops = []
            for ns in near_stops.all():
                a_lat = sum([sp.lat for sp in ns.positions if sp.availability])/len([sp.lat for sp in ns.positions if sp.availability])
                a_lng = sum([sp.lng for sp in ns.positions if sp.availability])/len([sp.lng for sp in ns.positions if sp.availability])
                dist = dist_on_sphere((lat, lng), (a_lat, a_lng)) * 1000
                if dist <= radius:
                    stops.append({"stop_data": ns, "dist": int(round(dist, -1))})
            if stops:
                stops.sort(key=lambda x:x["dist"])
            logger.debug(stops)
            return template(
                "api/v1.0/stop_search.json",
                stops=stops,
                query={
                    "lat": lat,
                    "lng": lng,
                    "radius": radius
                },
                autoescape=True
            )
    else:
        response.status = 400
        return json.dumps({"Error":[
            {"message": "Unsupported Type"}
        ]})
    response.status = 400
    return json.dumps({"Error":[
        {"message": "Bad Request"}
    ]})

if __name__ == "__main__":
    if app.config.get('RELOAD', False):
        logger.debug("Reload: true")
    app.run(host='0.0.0.0', port=80, reload=app.config.get('RELOAD', False), reloader=app.config.get('RELOAD', False))
    #else:
    #    app.run(host='0.0.0.0', port=8080)
