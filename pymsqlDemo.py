import config
import time


def insertDB(kwargs):
    db = config.get_mysql_connection()

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句
    sql = """INSERT INTO weiboGis(msg_id,address,content,msg_time,msg_timestamp,tools,transmi_count,comment_count,
                    praise_count,lng,lat,created_at,updated_at)
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())"""
    try:
        # 执行sql语句
        cursor.execute(sql, (kwargs.get("msg_id"),
                             kwargs.get("address"),
                             kwargs.get("content"),
                             kwargs.get("msg_time"),
                             kwargs.get("msg_timestamp"),
                             kwargs.get("tools"),
                             kwargs.get("transmi_count"),
                             kwargs.get("comment_count"),
                             kwargs.get("praise_count"),
                             kwargs.get("lng"),
                             kwargs.get("lat"),
                             ))
        # 提交到数据库执行
        db.commit()
        print("success insert")
    except Exception as e:
        # 如果发生错误则回滚
        print(e)
        db.rollback()

    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    pass

