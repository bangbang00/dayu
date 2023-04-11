from flask import Flask, Blueprint, render_template, session, url_for,request
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename
import pymysql
import json
import os
import time
from mysqlConnect import db_config, querydata, queryinsert, queryUpdate, Logger
import logging
import traceback

core=Blueprint('core',__name__)

app=Flask(__name__)

app.config.from_pyfile('settings.py')

logFile = app.config["LOGFILE"]
dbHost = app.config["DBHOST"]
dbPort = app.config["DBPORT"]
dbUser = app.config["DBUSER"]
dbPwd = app.config["DBPWD"]
dbName = app.config["DBNAME"]

@core.route('/modify_pdf_info',methods=['GET'])
def modifyPdfInfo():

    LoggerPrint = Logger( logFile, logging.INFO, logging.DEBUG)
    # 获取变量
    taskProgress = request.args.get('progress')
    pdfPath = request.args.get('pdf_path')
    taskID = request.args.get('id')

    taskStatus = 'progress'
    if taskProgress == '100':
        taskStatus = 'success'

    updateSQL = "update task set pdf_path='{path}',progress={progress},status='{status}' where id={id}".format(path=pdfPath, progress=taskProgress, status=taskStatus, id=taskID)
    
    # 执行变更
    config = db_config(dbHost, dbPort, dbUser, dbPwd, dbName)

    code, msg = queryUpdate(updateSQL, config)
    if code == 0:
        LoggerPrint.error("taskID: {id}, failed to modify task, error:{msg}".format(id=taskID, msg=msg))
        return_dict = {'code': 400, 'status': 'failed','data' : {},'message':'failed to modify task'}
        return json.dumps(return_dict, default=str)


    # 返回结果精细化
    LoggerPrint.info("task {id} modify success, current progress is {progress}.".format(id=taskID, progress=taskProgress))
    return_dict = {'code': 0, 'status': 'success','data' : {},'message':''}
    return json.dumps(return_dict, default=str)

