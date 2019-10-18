#!/usr/bin/env python3.5
# coding:utf8


import os
import pymysql


def get_mysql_connection():
    """
    获取一个MySQL连接对象

    How to use:

        connection = get_mysql_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `test` WHERE `title`=%s"
                cursor.execute(sql, ('123',)).fetchone()
        finally:
            connection.close()

    :return: Object
    """

    connection = pymysql.connect(host="127.0.0.1",
                                 user='root',
                                 port=3306,
                                 password="134679852",
                                 db='weibo',
                                 charset="utf8",
                                 )

    return connection


def get_local_mysql_connection():
    config = yaml.safe_load(open("%s/configs/config.%s.yml" % (cur_path, "local")))
    config['env'] = "local"
    CONFIG = config
    mysql_config = CONFIG['STORAGES']['MYSQL']
    connection = pymysql.connect(host=mysql_config['HOST'],
                                 user=mysql_config['USER'],
                                 port=mysql_config['PORT'],
                                 password=mysql_config['PASS'],
                                 db=mysql_config['DB'],
                                 charset=mysql_config['CHARSET'],
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection
