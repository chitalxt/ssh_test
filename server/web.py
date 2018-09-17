#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
import logging
import time
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from modules import interface


# 自动外呼api端口号
WEB_CONFIG = {
    'host': '127.0.0.1',
    'port': 8002
}

# 声明端口
define("port", default=WEB_CONFIG['port'], help="run on the given port", type=int)

# 访问url
url = [
    (r'^/taskphone$', interface.Request),  # 获取客户号码
]

# 模板路径
settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "statics"),
    static_url_prefix=os.path.join(os.path.dirname(__file__), "/static/"),
    cookie_secret=os.path.join(os.path.dirname(__file__), "asdfasdfasdfasdfasdfasdf"),
    login_url=os.path.join(os.path.dirname(__file__), "/login.html"),
)


def start():
    while True:
        try:            
            logging.info('start web services interface port:%s', WEB_CONFIG['port'])
            tornado.options.parse_command_line()
            application = tornado.web.Application(handlers=url, **settings)
            http_server = tornado.httpserver.HTTPServer(application)
            http_server.listen(options.port)
            tornado.ioloop.IOLoop.current().start()
        except Exception as e:
            logging.error(e)
            time.sleep(10)
