#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from bottle import route, run, get, post, request, static_file
from bottle import TEMPLATE_PATH, jinja2_template as template

# index.pyが設置されているディレクトリの絶対パスを取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# テンプレートファイルを設置するディレクトリのパスを指定
TEMPLATE_PATH.append(BASE_DIR + "/templates")
STATIC_DIR = os.path.join(BASE_DIR, 'static')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets/vendors')

# static file CSS
@route('/assets/rin/<filename:path>')
def static_css(filename):
    return static_file(filename, root=ASSETS_DIR+"/Rin/dist")

@route('/')
def index():
    return template('index.tpl.html', autoescape=True)

@route('/hello')
def hello():
    return "Hello World!"


run(host='localhost', port=8080, debug=True)
