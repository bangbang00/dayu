from flask import Flask, Blueprint, render_template, session, url_for,request,send_from_directory
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename
import pymysql
import json
import os
import time
from mysqlConnect import db_config, querydata, queryinsert, queryUpdate, Logger
import logging
import traceback

download=Blueprint('download',__name__)    #蓝图使用方法，参数里给定文件名，还可以给定url前缀

app=Flask(__name__)

app.config.from_pyfile('settings.py')

npyPath = app.config["NPYPATH"]
logFile = app.config["LOGFILE"]

@download.route('/download/<filename>')
def downloadPdf(filename):
    pdfPath = request.args.get('pdf_path')
    return send_from_directory(pdfPath, filename)

# 返回文件
@download.route('/get_pdf_list/')
def getPdfList():
    LoggerPrint = Logger( logFile, logging.INFO, logging.DEBUG)
    pdfPath = request.args.get('pdf_path')
    taskID = request.args.get('id')

    try:
        pathDir = os.listdir(pdfPath)
    except:
        err = traceback.format_exc()
        LoggerPrint.error("taskID: {id}, failed to get pdf list, error:{msg}".format(id=taskID, msg=err))
        return_dict = {'code': 400, 'status': 'failed','data' : {},'message':'failed to get pdf list'}
        return json.dumps(return_dict, default=str)

    # 返回结果精细化
    return_dict = {'code': 0, 'status': 'success','data' : pathDir,'message':''}
    return json.dumps(return_dict, default=str)
