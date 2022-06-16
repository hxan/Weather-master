# author:l
# contact: test@test.com
# datetime:2022/6/13 14:13
# software: PyCharm
# file    : test.py
# description :
import uuid
import datetime

import pandas as pd
import flask
import useful_functions
import pymysql
db_user_action = pymysql.connect(host=useful_functions.HOST, user=useful_functions.USER,
                     password=useful_functions.PASSWORD,
                     port=useful_functions.PORT, database=useful_functions.DATABASE,
                     charset=useful_functions.CHAREST)
user_cursor = db_user_action.cursor()
print(str(datetime.datetime.now()))
sql = """INSERT INTO user_action(Username,
         Userid, SearchKey, SelectPlace, ActionTime)
         VALUES ('高巨', 'gaoju123', '陕西', NULL, '2022-06-16 12:32:21.724457')"""
user_cursor.execute(sql)
db_user_action.commit()