import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,Blueprint, render_template
from werkzeug.utils import secure_filename, redirect
import json
import pymysql

view=Blueprint('view',__name__)

@view.route('/uploads/<filename>')
def uploaded_file(filename):
  dir = 'uploads/'
  return send_from_directory(dir,
                filename)

@view.route('/uploads/')
def uploaded():
  pathDir = os.listdir('uploads/')
  #return send_from_directory(app.config['UPLOAD_FOLDER'], pathDir[0])
  return render_template('upload.html', filenames=pathDir)
