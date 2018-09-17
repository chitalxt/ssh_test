#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


import sys
import logging
from conf.settings import LOG_CONFIG
from cloghandler import ConcurrentRotatingFileHandler
from server.web import start


def daemon():
    import os
    # create - fork 1
    try:
        pid = os.fork()
        if pid > 0:
            return pid
    except OSError as error:
        logging.error('fork #1 failed: %d (%s)' % (error.errno, error.strerror))
        return -1
    # it separates the son from the father
    os.chdir('/opt/pbx')
    os.setsid()
    os.umask(0)
    # create - fork 2
    try:
        pid = os.fork()
        if pid > 0:
            return pid
    except OSError as error:
        logging.error('fork #2 failed: %d (%s)' % (error.errno, error.strerror))
        return -1
    sys.stdout.flush()
    sys.stderr.flush()
    si = open("/dev/null", 'r')
    so = open("/dev/null", 'ab')
    se = open("/dev/null", 'ab', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
    return 0


def setLog():
    rotateHandler = ConcurrentRotatingFileHandler(LOG_CONFIG['filepath'], "a", 20 * 1024 * 1024, 200)
    rotateHandler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '[%(asctime)s] [process:%(process)s] [%(filename)s:%(lineno)d]  %(levelname)s %(message)s')
    rotateHandler.setFormatter(formatter)
    log = logging.getLogger()
    log.addHandler(rotateHandler)
    log.setLevel(logging.INFO)


def main():
    setLog()
    pid = daemon()
    if pid:
        return pid
    # 程序启动
    start()


if __name__ == "__main__":
    main()
