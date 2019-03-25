# -*- coding:utf-8 -*-
import pymysql

class Mysql(object):
    def __init__(self,host='localhost',port=3306,user='repository',passwd='repository',db='repository',charset='utf8'):
        """

        :param host:
        :param port:
        :param user:
        :param passwd:
        :param db:
        :param charset:
        """
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset

    def __str__(self):
        return str(vars(self))

    def get_db_conn(self):
        """

        :return:
        """
        return pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,charset=self.charset)

    def save_data(self, table='',key='',data={}):
        """

        :param table:
        :param key: 更新的关键字
        :param data: 要插入的数据,数据类型是字典
        :return: 无返回值
        """
        if not table or not key or not data:#如果数据为空
            return
        conn = self.get_db_conn()
        cur = conn.cursor()
        cur.execute("select * from %s where %s = \'%s\'"%(table, key, data[key]))
        rows = cur.fetchall()
        if len(rows) == 0:
            try:
                sql = "INSERT INTO %s(%s) values(%s)"%(table,(lambda d: ",".join(d.keys()))(data),','.join(['%s']*len(data)))
                cur.execute(sql,data.values())
                conn.commit()
            except Exception as e:
                print(e)
                conn.rollback()
        else:
            try:
                sql = "UPDATE %s SET %s WHERE url=\'%s\'"%(table,(lambda d: "=%s,".join(list(filter(lambda d: False if d == key else True, data.keys()))))(data)+'=%s',data[key])
                cur.execute(sql,list(data.get(k) for k in filter(lambda d:False if d == key else True, data.keys())))
                conn.commit()
            except Exception as e:
                print(e)
                conn.rollback()
        # 释放数据连接
        if cur:
            cur.close()
        if conn:
            conn.close()

    def query_data(self, table='',key='',key_value='',field=''):
        """

        :param table:
        :param key:
        :param key_value:
        :param field:
        :return:返回值是一个列表
        """
        if not table:
            print('table不可以为空!!!')
            return
        if not field:
            field = '*'
        conn = self.get_db_conn()
        cur = conn.cursor()
        if not key:
            cur.execute("select %s from %s"%(field,table))
        else:
            if not key_value:
                print('key_value不可以为空!!!')
                return
            else:
                cur.execute("select %s from %s where %s = %s" % (field, table,key,key_value))
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return rows