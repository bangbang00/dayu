#!/bin/bash
#
#软件目录：/usr/local/mysql
#数据目录：/data/mysql
#设置好root用户的密码
#mysqlInstall.sh
#
#相关目录
MYSQL_HOME='/usr/local'
MYSQL_DATA='/data/mysql'
MYSQL_CONF='/etc/mysql'
MYSQL_TAR='mysql-5.7.30-linux-glibc2.12-x86_64.tar.gz'
MYSQL_UNZIP_FILE='mysql-5.7.30-linux-glibc2.12-x86_64'
CONF_FILE='my-sample.cnf'
MYSQL_SOCK='mysql.sock'
TIME=`date +%Y%m%d%H%M%S`
CURRENT_PATH=`pwd`


#检查安装用户是否是root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script, please use root to install"
    exit 1
fi

#安装依赖包
rpm=`rpm -qa libaio|awk -F "-" '{print $1}'`
if [ -z "$rpm" ];then
    yum -y install libaio
else
    echo -e "\033[40;31m libaio [found]\033[40;37m"
fi


#创建mysql用户
id mysql
if [  "0" == "$?" ];then
    echo "mysql用户存在，删除mysql用户和组"
    pid=`pidof mysqld`
    kill -9  $pid >/dev/null 2>&1
    /usr/sbin/userdel -r  mysql > /dev/null 2>&1
    echo "1创建mysql用户和组" && sleep 2
    /usr/sbin/groupadd mysql
    /usr/sbin/useradd -s /sbin/nologin -g mysql mysql
else
    echo "2创建mysql用户和组" && sleep 2
    /usr/sbin/groupadd mysql
    /usr/sbin/useradd -s /sbin/nologin -g mysql mysql
fi

#安装程序
#安装前准备
echo "unzip starting......"
tar -zxf $CURRENT_PATH/$MYSQL_TAR -C $MYSQL_HOME
#创建软链接
cd $MYSQL_HOME
ln -s $MYSQL_UNZIP_FILE mysql
#创建目录
echo "创建mysql相关文件目录" && sleep 2
mkdir -p $MYSQL_DATA $MYSQL_CONF
chown -R mysql:mysql $MYSQL_DATA
chmod -R 750 $MYSQL_DATA
#配置用户环境变量
echo "export PATH=/usr/local/mysql/bin:$PATH" >> /etc/profile
source /etc/profile

#配置文件(先备份后创建)
sudo cp $CURRENT_PATH/$CONF_FILE $MYSQL_CONF/my-3306.cnf
#初始化数据库
echo "initializing......"
mysqld --defaults-file=$MYSQL_CONF/my-3306.cnf --datadir=$MYSQL_DATA --basedir=$MYSQL_HOME/mysql --initialize --user=mysql
#启动数据库
mysqld_safe --defaults-file=$MYSQL_CONF/my-3306.cnf --basedir=$MYSQL_HOME/mysql --datadir=$MYSQL_DATA --user=mysql &

#查看安装是否有报错
echo "=============================="
grep 'error' $MYSQL_DATA/mysql.err
#查看是否启动mysql
echo "=============================="
ps -ef|grep mysql
#查看root随机密码
echo "==============================password"
cd $MYSQL_DATA
a1=`grep 'A temporary password' mysql.err | awk -F"root@localhost: " '{ print $2}' `
echo $a1
sleep 2
#登录数据库
mysql -uroot -p"${a1}" -h'127.0.0.1' --connect-expired-password <<EOF
set password = 'root123123';
create user 'root'@'%' identified by 'root123123';
grant all privileges on *.* to 'root'@'%' with grant option;
flush privileges;
exit
EOF
#重启mysql
sleep 1
systemctl restart mysql.server
echo "==============================install success"
#END
