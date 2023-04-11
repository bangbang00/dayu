from flask import Flask,Blueprint, render_template, session, url_for,request
from werkzeug.utils import redirect
import pymysql
import json
from mysqlConnect import db_config, querydata, queryinsert, queryUpdate, Logger
import logging

get_task=Blueprint('get_task',__name__)    #蓝图使用方法，参数里给定文件名，还可以给定url前缀

app=Flask(__name__)

app.config.from_pyfile('settings.py')

logFile = app.config["LOGFILE"]
dbHost = app.config["DBHOST"]
dbPort = app.config["DBPORT"]
dbUser = app.config["DBUSER"]
dbPwd = app.config["DBPWD"]
dbName = app.config["DBNAME"]

@get_task.route('/get_task',methods=['GET'])
def getTask():
    LoggerPrint = Logger( logFile, logging.INFO, logging.DEBUG)
    # todo: 加分页
    #sql = "select id, name, detail, creator, status, ctime, mtime,deleted from task"
    sql = "select * from task where "

    name = request.args.get("name")
    status = request.args.get("status")
    sql = "{sql} status like '%{status}%' and name like '%{name}%'".format(sql=sql,status=status,name=name)
    print(sql)

    config = db_config(dbHost, dbPort, dbUser, dbPwd, dbName)

    code, result = querydata(sql, config)

    if code == 0:
        LoggerPrint.error("failed to get task, error:{msg}".format(msg=result))
        return_dict = {'code': 400, 'status': 'failed','data' : {},'message':'failed to get task'}
        return json.dumps(return_dict, default=str)

    return_dict = {'code': 0, 'status': 'success','data' : result, 'message': ''}
    return json.dumps(return_dict, default=str)

@get_task.route('/get_task_detail',methods=['POST','GET'])
def getTaskDetail():
    # todo: 加分页
    taskID = request.values.get('task_id')
    sql = "select id, name, task_id, name, status, path, ctime, mtime,deleted from sub_task where task_id=%s"
    connection = pymysql.connect(host='localhost',user='root',password='123123', db='data_canal',cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    cursor.execute(sql,taskID)
    result = cursor.fetchall()
    for i in result:
        if i["name"] == "shengcheng pdf":
            print(i["path"])
        else:
            print('no')
    return_dict = {'code': 0, 'status': 'success','data' : result}
    return json.dumps(return_dict, default=str)
