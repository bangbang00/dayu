from flask import Blueprint, render_template, session, url_for,request
from werkzeug.utils import redirect

user=Blueprint('user',__name__)    #蓝图使用方法，参数里给定文件名，还可以给定url前缀

@user.route('/login')   #使用user的路由配置
# @user.route('/loginProcess',methods=['POST','GET'])   #使用user 的路由配置
def loginProcesspage():
    if request.method=='POST':
        return 'post'
    else:
        return 'the username or userpwd does not match!'
