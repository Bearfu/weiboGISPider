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

    mysql_config = CONFIG['STORAGES']['MYSQL']

    if CONFIG['STORAGES']['MYSQL'].get('LOCAL_JUMP'):
        jump_config = CONFIG['STORAGES']['MYSQL']['LOCAL_JUMP']
        # client = paramiko.SSHClient()
        # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # client.load_system_host_keys()
        # client.connect(jump_config['SSH_IP'], username=jump_config['SSH_USER'])
        # transport = client.get_transport()
        # channel = transport.open_channel('direct-tcpip', (mysql_config['HOST'], mysql_config['PORT']),('localhost', 4144))
        # connection = pymysql.connect(database=mysql_config['DB'],
        #                              user=mysql_config['USER'],
        #                              port=mysql_config['PORT'],
        #                              passwd=mysql_config['PASS'],
        #                              charset=mysql_config['CHARSET'],
        #                              cursorclass=pymysql.cursors.DictCursor,
        #                              defer_connect=True)
        # connection.connect(channel)

        pool = PooledDB(pymysql, 5, **jump_config)
        cnx = pool.connection()
        return cnx


    else:
        connection = pymysql.connect(host=mysql_config['HOST'],
                                     user=mysql_config['USER'],
                                     port=mysql_config['PORT'],
                                     password=mysql_config['PASS'],
                                     db=mysql_config['DB'],
                                     charset=mysql_config['CHARSET'],
                                     cursorclass=pymysql.cursors.DictCursor)
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