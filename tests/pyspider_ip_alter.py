# -*- coding:utf-8 -*-

import pymysql

conn = pymysql.connect(host='122.224.129.35', port=23306, user='repository', passwd='repository', db='repository', charset='utf8')
cur = conn.cursor()

cur.execute("select id,context from website where context like '%img src=%' and context not like '%122.224.129.35%'")
for data in cur.fetchall():
    # context = data[1].replace('10.1.17.25:5000', '122.224.129.35:28080')
    context = data[1].replace('img src="/picture_hzz', 'img src="http://122.224.129.35:28080/picture_hzz')
    cur.execute("update website set context='%s' where id='%s'"%(context,data[0]))
    print(context)
    # print(data[0])
conn.commit()
cur.close()
conn.close()