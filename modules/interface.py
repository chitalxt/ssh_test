#!/usr/bin/env python
# -*- coding:utf-8 -*-


import logging
import json
import uuid
import traceback
import tornado.web
from tornado import gen

# 是否第一次获取客户号码
FIRST_GET_NUMBER = True

UUID_LIST = []


class Request(tornado.web.RequestHandler):
    """所有请求处理入口"""

    @gen.coroutine
    def get(self, *args):
        logging.info('get message[%s]',self.request.arguments)
        result = self.execute('GET', *args)
        logging.info('return message[%s]', result)
        if result:
            self.write(result)
            self.flush()


    @gen.coroutine
    def post(self, *args):
        logging.info('get message[%s]',self.request.arguments)
        result = self.execute('POST', *args)
        logging.info('return message[%s]', result)
        if result:
            self.write(result)
            self.flush()


    def execute(self, method, *args):
        try:
            action = self.get_argument('action', '')
            if action == 'sum':
                return self.execute_all(method, *args)

            elif action == 'numbers':
                return self.execute_count(method, *args)

            else:
                logging.error('action[%s] is wrong', action)

        except Exception as e:
            exc = traceback.format_exc()
            logging.error(exc)

    def argument_detection(self):
        '''检测必传的参数'''
        action = self.get_argument('action', '')
        requestid = self.get_argument('requestid', '')
        if not action or not requestid :
            logging.error('miss import arguments action[%s] requestid[%s]', action, requestid)
            return False
        return True

    def execute_all(self, method, *args):
        '''执行'''
        try:
            action = self.get_argument('action', '')
            requestid = self.get_argument('requestid', '')

            result = self.argument_detection()
            if not result:
                logging.error('arguments are error action[%s] requestid[%s]', action, requestid)
                return

            return self.create_response_all(requestid=requestid, sum=1)

        except Exception as e:
            exc = traceback.format_exc()
            logging.error(exc)

    def create_response_all(self, requestid, sum):
        '''发送回复信息'''
        data = {
            "requestid": requestid,
            "sum": sum
        }
        return json.dumps(data)

    def execute_count(self, method, *args):
        '''执行'''

        try:
            action = self.get_argument('action', '')
            requestid = self.get_argument('requestid', '')
            uuid_str = self.get_argument('uuid', '')
            count = self.get_argument('count', '')

            result = self.argument_detection_count()
            if not result:
                logging.error('arguments are error action[%s] requestid[%s] uuid[%s] count[%s]', action, requestid,
                              uuid_str, count)
                return

            global FIRST_GET_NUMBER
            if FIRST_GET_NUMBER and not uuid_str:
                # 第一次来请求
                uuid_str = str(uuid.uuid1())
                UUID_LIST.append(uuid_str)
                FIRST_GET_NUMBER = False

            elif uuid_str not in UUID_LIST:
                logging.error('uuid[%s] is wrong', uuid_str)

            return self.create_response_count(requestid=requestid, uuid=uuid_str, numbers=[])

        except Exception as e:
            exc = traceback.format_exc()
            logging.error(exc)

    def argument_detection_count(self):
        '''检测必传的参数'''
        if not self.argument_detection():
            return False

        uuid = self.get_argument('uuid', '')
        count = self.get_argument('count', '')
        if FIRST_GET_NUMBER:
            if not count:
                logging.error('miss import arguments count[%s]', count)
                return False
        elif not uuid or not count:
            logging.error('miss import arguments uuid[%s] count[%s]', uuid, count)
            return False

        return True

    def create_response_count(self, requestid, uuid, numbers):
        '''发送回复信息'''
        data = {
            "requestid": requestid,
            "uuid": uuid,
            'numbers': numbers,
        }
        return json.dumps(data)


