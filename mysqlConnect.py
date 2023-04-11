#!/usr/bin/python
#-*-coding: utf-8-*-

# Script Description:
# -----------------------------------------------------------------------------------------------------
# 数据库连接&操作
# -----------------------------------------------------------------------------------------------------

import pymysql
import traceback
import time
import os
import sys
import logging
import json
import hashlib
import datetime


#timeExt = time.strftime("%Y%m%d.%H%M%S")
#baseName      = os.path.basename(__file__).split('.')[0]
#scriptsPath   = os.path.dirname(os.path.abspath(__file__))
#logPath       = '{}/logs'.format(scriptsPath)
#logFile       = '{}/{}.log-{}'.format(logPath,baseName,timeExt)

sys.path.append('./')

class Logger:
    def __init__(self, logfile, clevel, Flevel):
        self.logger = logging.getLogger(logfile)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')

        #Console print
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)

        #Log file print
        fh = logging.FileHandler(logfile)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self,message):
        self.logger.debug(message)
    def info(self,message):
        self.logger.info(message)
    def war(self,message):
        self.logger.warn(message)
    def error(self,message):
        self.logger.error(message)

# 连接信息
def db_config(host, port, user, password, dbname):
    config = {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'db': dbname,
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor
    }
    return config


# select执行
def querydata(sql, dbconfig, *args, **kwargs):

    try:
        conn = pymysql.connect(**dbconfig)
        cursor = conn.cursor()
    except:
        erro = traceback.format_exc()
        errmsg = 'error! connect {host} - {port} failed!! \n{erro} '.format(host=dbconfig['host'], port=dbconfig['port'], erro=erro)
        return 0, errmsg
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return 1, result
    except :
        erro = traceback.format_exc()
        errmsg = 'error! {host} - {port}: select {sql} failed!! \n{erro} '.format(host=dbconfig['host'], port=dbconfig['port'], sql=sql, erro=erro)
        return 0, errmsg

# insert 执行
def queryinsert(sql, db_config, *args, **kwargs):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
    except:
        erro = traceback.format_exc()
        errmsg = 'error! connect {host} - {port} failed!! \n{erro} '.format(host=dbconfig['host'], port=dbconfig['port'], erro=erro)
        # LoggerPrint.error(errmsg)
        return 0, errmsg
    try:
        cursor.execute(sql)
        conn.commit()
        return cursor.lastrowid, ''
    except :
        errmsg = 'error! exec failed!! \n%s'%(traceback.format_exc())
        return 0, errmsg
    finally:
        conn.close()

# update 执行
def queryUpdate(sql, db_config, *args, **kwargs):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
    except:
        erro = traceback.format_exc()
        errmsg = 'error! connect {host} - {port} failed!! \n{erro} '.format(host=dbconfig['host'], port=dbconfig['port'], erro=erro)
        # LoggerPrint.error(errmsg)
        return 0, errmsg
    try:
        cursor.execute(sql)
        conn.commit()
        return 1, ''
    except :
        errmsg = 'error! exec failed!! \n%s'%(traceback.format_exc())
        return 0, errmsg
    finally:
        conn.close()
