# from crypt import methods
from flask import Flask, render_template, redirect, url_for, jsonify
import pymysql
from model.forms import SearchForm
from flask import request
import useful_functions
import spider_modul
import spider_news
import utils
import time

# 这里对数据库内容进行提取
# spider_modul.run()
datalist = useful_functions.get_datalist()

# 这里分析数据库内容，提炼出数据库信息，并对文本内容分词

datainfo = useful_functions.get_datalist_info(datalist)

line_data_temp = useful_functions.get_lineData_temp()
line_data_humd = useful_functions.get_lineData_humd()

# 计算 topK=8 的词汇对应的词频
# words,weights = useful_functions.get_word_weights(string, topK=8)

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"


# 首页重定位
@app.route('/index')
def home_page():
    return index()


@app.route('/temp')
def temp_page():
    return index()


# 首页
@app.route('/')
def index():
    return render_template("index.html")


# 新闻缩略页
@app.route('/info')
def news_page():
    global data_info
    global line_data_humd
    global line_data_temp
    data_info = datainfo
    return render_template("info.html", news=data_info, line_data_temp=line_data_temp, line_data_humd=line_data_humd)


# 数据
@app.route('/info1')
def info_page():
    global data_info
    global line_data_humd
    global line_data_temp
    data_info = datainfo
    return render_template("info1.html", news=data_info, line_data_temp=line_data_temp, line_data_humd=line_data_humd)


@app.route('/kepler_map')
def kepler_map():
    return render_template("kepler_map.html")


# 搜索界面
@app.route('/search', methods=['GET', 'POST'])
def search_page():
    form = SearchForm()
    return render_template('search.html', form=form, str_list=str_list)


# 登录页面
@app.route('/html/new')
def new():
    return render_template('/html/new.html')


@app.route('/html/news')
def news():
    return render_template('/html/news.html')


@app.route('/html/old')
def old():
    return render_template('/html/old.html')


@app.route('/forcast')
def forcast():
    return render_template('/forcast.html')


@app.route('/html/forcasts')
def forcasts():
    return render_template('/html/forcasts.html')


@app.route('/html/welcome')
def welcome():
    return render_template('/html/welcome.html')


@app.route('/backstage')
def backstage():
    return render_template('backstage.html')


@app.route('/user')
def user():
    return render_template('user.html')


@app.route('/html/dashboard')
def dashboard():
    return render_template('/html/dashboard.html')


@app.route('/new_a')
def new_a():
    return render_template('/new_a.html')


@app.route('/old_a')
def old_a():
    return render_template('/old_a.html')


@app.route('/html/profile')
def profile():
    return render_template('/html/profile.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if (request.method == 'GET'):
        return render_template('login.html')
    elif (request.method == 'POST'):
        print(request.form.get('username'))
        # time.sleep(1000000)
        return redirect(url_for('backstage'))


# 获取分页历史统计数据
@app.route('/old/list', methods=["POST"])
def old_list():
    get_data = request.form.to_dict()
    page_size = get_data.get('page_size')
    page_no = get_data.get('page_no')
    param = get_data.get('param')
    data, count, page_list, max_page = utils.get_old_list(int(page_size), int(page_no), param)
    return jsonify({"data": data, "count": count, "page_no": page_no, "page_list": page_list, "max_page": max_page})


# 修改历史统计数据
@app.route('/old/edit', methods=["POST"])
def old_edit():
    get_data = request.form.to_dict()
    city = get_data.get('city')
    TEM = get_data.get('TEM')
    TEM_MAX = get_data.get('TEM_MAX')
    TEM_MIN = get_data.get('TEM_MIN')
    RHU = get_data.get('RHU')
    VAP = get_data.get('VAP')
    PRE_1h = get_data.get('PRE_1h')
    WIN_S_Max = get_data.get('WIN_S_Max')
    WIN_S_Inst_Max = get_data.get('WIN_S_Inst_Max')
    utils.edit_old(city, TEM, TEM_MAX, TEM_MIN, RHU, VAP, PRE_1h, WIN_S_Max, WIN_S_Inst_Max)
    return '200'


# 获取分页区域统计数据
@app.route('/new/list', methods=["POST"])
def new_list():
    get_data = request.form.to_dict()
    page_size = get_data.get('page_size')
    page_no = get_data.get('page_no')
    param = get_data.get('param')
    data, count, page_list, max_page = utils.get_new_list(int(page_size), int(page_no), param)
    return jsonify({"data": data, "count": count, "page_no": page_no, "page_list": page_list, "max_page": max_page})


# 修改区域统计数据
@app.route('/new/edit', methods=["POST"])
def new_edit():
    get_data = request.form.to_dict()
    city = get_data.get('city')
    Day = get_data.get('Day')
    Hour = get_data.get('Hour')
    TEM = get_data.get('TEM')
    TEM_MAX = get_data.get('TEM_MAX')
    TEM_MIN = get_data.get('TEM_MIN')
    RHU = get_data.get('RHU')
    VAP = get_data.get('VAP')
    PRE_1h = get_data.get('PRE_1h')
    WIN_S_Max = get_data.get('WIN_S_Max')
    WIN_S_Inst_Max = get_data.get('WIN_S_Inst_Max')
    utils.edit_new(city, Day, Hour, TEM, TEM_MAX, TEM_MIN, RHU, VAP, PRE_1h, WIN_S_Max, WIN_S_Inst_Max)
    return '200'


# 搜索结果返回界面，返回时展示页数（每页50条数据），（id、新闻文本、新闻url）
str_list = []


@app.route('/news_result', methods=['POST', 'GET'])
def newsResult_page():
    result = []
    newsList = spider_news.spider_news()
    keyword = request.form.get('query')

    # add by lws 历史功能
    if keyword not in str_list:
        str_list.append(keyword)
    # end add

    list_title, list_url = newsList.getDC()
    for i in range(len(list_title)):
        if list_title[i].__contains__(keyword):
            result.append((i + 1, list_title[i], 'http://data.cma.cn' + list_url[i]))
    return render_template('news_result.html', form=result)


if __name__ == '__main__':
    app.run(debug=True)
