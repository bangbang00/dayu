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
import requests
from requests import ReadTimeout

upload=Blueprint('upload',__name__)    #蓝图使用方法，参数里给定文件名，还可以给定url前缀

app=Flask(__name__)

app.config.from_pyfile('settings.py')

npyPath = app.config["NPYPATH"]
logFile = app.config["LOGFILE"]
dbHost = app.config["DBHOST"]
dbPort = app.config["DBPORT"]
dbUser = app.config["DBUSER"]
dbPwd = app.config["DBPWD"]
dbName = app.config["DBNAME"]
coreServer = app.config["CORESERVER"]

@upload.route('/upload',methods=['POST', 'GET'])   #使用user 的路由配置
def upLoad():

    LoggerPrint = Logger( logFile, logging.INFO, logging.DEBUG)
    taskName = request.args.get('name')
    taskDetail = request.args.get('detail')
    taskCreator = request.args.get('creator')

    # 生成随机文件夹
    curTime = int(round(time.time() * 1000000))
    curPath = "{}/{}".format(npyPath, curTime)
    if os.path.exists(curPath):
        LoggerPrint.error("PATH: {dir}, Directory already exists, please try again".format(dir=curPath))
        return_dict = {'code': 400, 'status': 'failed','data' : {},'message':'Directory already exists, please try again'}
        return json.dumps(return_dict, default=str)
    else:
        os.mkdir(curPath)

    # 获取传参信息
    feature_files = request.files.getlist("feature")[0]
    label_files = request.files.getlist("label")[0]

    # 创建任务
    createSQL = "insert into task(name,detail,creator,status,feature_file,label_file,npy_path) values('{name}','{detail}','{creator}','progress','{feature}','{label}','{npy}')".format(name=taskName, detail=taskDetail, creator=taskCreator, feature=feature_files.filename,label=label_files.filename,npy=curPath)

    config = db_config(dbHost, dbPort, dbUser, dbPwd, dbName)

    code, msg = queryinsert(createSQL, config)

    if code == 0:
        LoggerPrint.error("failed to create task, error:{msg}".format(msg=msg))
        return_dict = {'code': 400, 'status': 'failed','data' : {},'message':'failed to create task, error:{msg}'.format(msg=msg)}
        return json.dumps(return_dict, default=str)

    # 保存文件
    try:
        feature_files.save(os.path.join(curPath, feature_files.filename))
    except:
        err0=traceback.format_exc()
        LoggerPrint.error("taskID: {id}, failed to save feature file, error:{msg}".format(id=code, msg=err0))
        modifySQL = "update task set status='failed' where id={id};".format(id=code)
        modifyCode, modifyMsg = queryUpdate(modifySQL, config)
        if modifyCode == 0:
            LoggerPrint.error("taskID: {id}, failed to modify task status, error:{msg}".format(id=code, msg=modifyMsg))
        return_dict = {'code': 400, 'status': 'failed','data' : {},'message':'failed to save feature file, error:{msg}'.format(msg=err0)}
        return json.dumps(return_dict, default=str)

    try:
        label_files.save(os.path.join(curPath, label_files.filename))
    except:
        err1=traceback.format_exc()
        LoggerPrint.error("taskID: {id}, failed to save label file, error:{msg}".format(id=code, msg=err1))
        modifySQL = "update task set status='failed' where id={id};".format(id=code)
        modifyCode2, modifyMsg2 = queryUpdate(modifySQL, config)
        if modifyCode2 == 0:
            LoggerPrint.error("taskID: {id}, failed to modify task status, error:{msg}".format(id=code, msg=modifyMsg2))
        return_dict = {'code': 400, 'status': 'failed','data' : {},'message':'failed to save label file, error:{msg}'.format(msg=err1)}
        return json.dumps(return_dict, default=str)

    # 发送信息
    sendCode, err = sendInfoToCore(int(code), curPath)
    if sendCode == 0:
        LoggerPrint.error("taskID: {id}, failed to send info to core, error:{msg}".format(id=code, msg=err))
        modifySQL = "update task set status='failed' where id={id};".format(id=code)
        modifyCode3, modifyMsg3 = queryUpdate(modifySQL, config)
        if modifyCode3 == 0:
            LoggerPrint.error("taskID: {id}, failed to modify task status, error:{msg}".format(id=code, msg=modifyMsg3))
        return_dict = {'code': 400, 'status': 'failed','data' : {},'message':'failed to save label file'}
        return json.dumps(return_dict, default=str)
    
    # 返回结果精细化
    LoggerPrint.info("task {id} upload success".format(id=code))
    return_dict = {'code': 0, 'status': 'success','data' : {},'message':''}
    return json.dumps(return_dict, default=str)

# 发送信息给到核心处理程序
def sendInfoToCore(id, path):

    url = "{coreServer}?id={id}&path={path}".format(coreServer=coreServer, id=id, path=path)
    payload={}
    headers = {}

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
    except:
        err=traceback.format_exc()
        return 0, err

    # 获取结果
    result = response.json()
    
    if result["code"] != 0:
        err = "code is not 0, {err}".format(err=result["message"])
        print(err)
        return 0, err

    return 1, ''

# example
@upload.route('/send_core', methods=['GET'])
def sendCore():
    path = request.args.get('path')
    taskID = request.args.get('id')

    if 10 > 20:
        return_dict = {'code': 400, 'status': 'failed','data' : {},'message':'failed to receive info'}
        return json.dumps(return_dict, default=str)
    return_dict = {'code': 0, 'status': 'success','data' : {},'message':''}
    return json.dumps(return_dict, default=str)
