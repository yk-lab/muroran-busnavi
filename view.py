# -*- coding:utf-8 -*-

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('./templates', encoding='utf8'))

def __init__(self, tpl):
    self.tpl = env.get_template(tpl)

def html_render(charset="utf-8", **keyword_arguments):
    html = tpl.render(keyword_arguments)
    print 'Content-Type: text/html; charset=%s\n' % charset
    print html.encode(charset)
