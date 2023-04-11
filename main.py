from flask import Flask, render_template, url_for, request, redirect, session, send_from_directory, helpers
from werkzeug.utils import secure_filename
import os
from core import core
from get_task import get_task
from upload import upload
from download import download
import base64,json

app=Flask(__name__)

app.config.from_pyfile('settings.py')

print(app.config["DBUSER"])

app.secret_key='any random string'
urls=[core,get_task,upload,download]      #将路由构建数组
for url in urls:
    app.register_blueprint(url)   #将路由均实现蓝图注册到主app应用上

@app.route('/')
def index():
  return render_template('index.html')

if __name__=="__main__":
    print(app.url_map)                 #打印url结构图
    app.run(port=app.config["SERVERPORT"],host=app.config["SERVERHOST"],debug=app.config["DBUSER"])
