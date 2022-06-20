import pymysql
from collections import defaultdict
import jieba.analyse
import datetime

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = '123456'
PORT = 3306
DATABASE = 'weather'
CHAREST = 'utf8'

db_user = pymysql.connect(host=HOST, user=USER,
                          password=PASSWORD,
                          port=PORT, database=DATABASE,
                          charset=CHAREST)
user_cursor = db_user.cursor()


def insert_action(username, userid, searchKey):
    sql = """INSERT INTO user_action(Username,
             Userid, SearchKey, ActionTime)
             VALUES ('%s', '%s', '%s', '%s')""" % (
        username, userid, searchKey, str(datetime.datetime.now()))

    user_cursor.execute(sql)
    db_user.commit()

def get_action_by_name(username):
    sql = "select SearchKey from weather.user_action where Username='%s'" % (username)
    user_cursor.execute(sql)
    results = user_cursor.fetchall()
    return results

def insert_user(username, id, password, address):
    sql = """INSERT INTO user(Username,
                 Userid, Password, RegisterTime,Address)
                 VALUES ('%s', '%s', '%s', '%s','%s')""" % (
        username, id, password, str(datetime.datetime.now()), address)

    user_cursor.execute(sql)
    db_user.commit()


def get_all_username():
    sql = """SELECT username FROM weather.user;"""
    user_cursor.execute(sql)
    results = user_cursor.fetchall()
    return results


def get_password_by_name(username):
    sql = "select Password from weather.user where Username='%s'" % (username)
    user_cursor.execute(sql)
    results = user_cursor.fetchall()
    return results[0][0]


def get_address_by_name(username):
    sql = "select Address from weather.user where Username='%s'" % (username)
    user_cursor.execute(sql)
    results = user_cursor.fetchall()
    return results[0][0]


def set_address_by_name(username, address):
    sql = "update weather.user set Address='%s' where Username='%s'" % (address, username)
    user_cursor.execute(sql)
    db_user.commit()


# 连接数据库并提取数据库内容
def get_datalist():
    datalist = []
    cnn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, port=PORT, database=DATABASE,
                          charset=CHAREST)
    cursor = cnn.cursor()
    sql = 'select * from weather where hour=0 order by id;'
    cursor.execute(sql)
    for item in cursor.fetchall():
        datalist.append(item)
    cursor.close()
    cnn.close()
    return datalist


# 对数据库文本内容进行分词，并返回 data_inf0 = [区站号(字符) 日 时 气压 最高气压 最低气压 温度/气温 最高气温 最低气温 相对湿度 水汽压 过去1小时降水量 最大风速 最大风速的风向 极大风速的风向 极大风速 最小相对湿度
#                                                          日 时 百帕 百帕    百帕     摄氏度(℃) 摄氏度(℃) 摄氏度(℃) 百分率 百帕 毫米           米/秒   度           度              米/秒"  百分率] 
def get_datalist_info(datalist):
    datainfo = []
    citykey = []
    for item in datalist:
        citykey.append(str(item[1]))
        tup = (
            item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10], item[11], item[12],
            item[13],
            item[14], item[15], item[16], item[17], item[18])
        datainfo.append(tup)
    return dict(zip(citykey, datainfo))


# 对输入文本进行分词，并返回词汇权重
def get_word_weights(string, topK):
    words = []
    weights = []
    for x, w in jieba.analyse.textrank(string, withWeight=True, topK=topK):
        words.append(x)
        weights.append(w)
    return words, weights


# 得到气温走势曲线
def get_lineData_temp():
    line_data = []
    cnn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, port=PORT, database=DATABASE,
                          charset=CHAREST)
    cursor = cnn.cursor()
    sql = 'select Station_Id_C, Day, max(TEM),min(TEM) from weather group by Station_Id_C ,Day;'  # 对温度求最大值和最小值 group by day, cityKey;
    cursor.execute(sql)
    line_dict = defaultdict(list)
    for item in cursor.fetchall():
        line_data.append(item)  # 返回Days相同的所有地区七天的最高/最低温度数据

    for Id, Day, mAx, mIn in line_data:
        Id = str(Id)
        line_dict[Id].append((Day, mAx, mIn))
    cursor.close()
    cnn.close()

    return line_dict


# 得到湿度走势曲线
def get_lineData_humd():
    line_data = []
    cnn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, port=PORT, database=DATABASE,
                          charset=CHAREST)
    cursor = cnn.cursor()
    sql = 'select Station_Id_C, Day, max(RHU),min(RHU) from weather group by Station_Id_C ,Day;'  # 对温度求最大值和最小值 group by day, cityKey;
    cursor.execute(sql)
    line_dict = defaultdict(list)
    for item in cursor.fetchall():
        line_data.append(item)  # 返回Days相同的所有地区七天的最高/最低温度数据

    for Id, Day, mAx, mIn in line_data:
        Id = str(Id)
        line_dict[Id].append((Day, mAx, mIn))
    cursor.close()
    cnn.close()

    return line_dict


# # 文本关键字提取
# def get_keyword_from_content(content):
#     print(content)
#     cut = jieba.cut(content)
#     string = ' '.join(cut)
#     words,_=get_word_weights(string, topK=5)
#     return words.append('（自动生成）')


if __name__ == '__main__':
    datalist = get_lineData_temp()
    print(datalist['52681'])
