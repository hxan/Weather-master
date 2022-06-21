import utils
import recommend
import UserFlask
import spider_news
import spider_modul
import useful_functions
from flask import request
from model.forms import SearchForm
from flask_login import LoginManager
from flask_login import login_user, logout_user
from flask_login import current_user, login_required
from flask import Flask, render_template, redirect, url_for, jsonify, flash

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

login_manager = LoginManager()  # 实例化登录管理对象
login_manager.init_app(app)  # 初始化应用
login_manager.login_view = 'user_login'  # 设置用户登录视图函数 endpoint


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
@login_required
def search_page():
    form = SearchForm()
    searchKeys = useful_functions.get_action_by_name(current_user.username)
    searchKeys = list(x[0] for x in searchKeys)
    newsList = spider_news.spider_news()
    list_title, list_url = newsList.getDC()
    return render_template('search.html', form=form, str_list=searchKeys,
                           similar_titles=recommend.recommend_news(searchKeys, list_title, list_url),
                           list_title=list_title, list_url=list_url
                           )


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
    return render_template('/html/profile.html')


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


@app.route('/user_register', methods=['POST', 'GET'])
def user_register():
    all_username = useful_functions.get_all_username()

    all_username = tuple(x[0] for x in all_username)

    if (request.method == 'GET'):
        return render_template('user_register.html')
    elif (request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        if username not in all_username:
            user_temp = UserFlask.User(username, password, '中国')
            useful_functions.insert_user(user_temp.username, user_temp.get_id(), user_temp.password_hash, '中国')
            return '注册成功'
        else:
            return '注册失败，用户名已经被占用'


@app.route('/user_login', methods=['POST', 'GET'])
def user_login():
    if (request.method == 'GET'):
        if current_user.is_authenticated:
            return '你已经登录，如果要登录请先退出'
        else:
            return render_template('user_login.html')
    elif (request.method == 'POST'):

        username = request.form.get('username')
        password = request.form.get('password')
        all_username = useful_functions.get_all_username()
        all_username = tuple(x[0] for x in all_username)
        if username not in all_username:
            return '不存在的用户名'
        if password != useful_functions.get_password_by_name(username):
            return '用户名或者密码错误'

        user_temp = UserFlask.User(username, password, address=useful_functions.get_address_by_name(username))
        UserFlask.USERS.append(user_temp)
        if login_user(user_temp):
            print('Logged in successfully.')
        else:
            print('Fail to logged in .')
        return redirect(url_for('index'))


@app.route('/user_logout')
@login_required
def user_logout():
    logout_user()
    return '用户已经退出'


@app.route('/login', methods=['POST', 'GET'])
def login():
    if (request.method == 'GET'):
        return render_template('login.html')
    elif (request.method == 'POST'):
        print(request.form.get('username'))
        return redirect(url_for('backstage'))


@app.route('/user_info')
@login_required
def user_info():
    print('current_user.username is ' + current_user.username)
    print('current_user.address is ' + current_user.address)

    address_new = request.args.get('address')
    print('address_new is ' + str(address_new))

    if address_new != None and address_new != current_user.address:
        current_user.address = address_new
        print("current_user.address" + str(current_user.address))
        useful_functions.set_address_by_name(username=current_user.username, address=current_user.address)

    return render_template('/html/profile.html', username=current_user.username, user_address=current_user.address)


@login_manager.user_loader
def load_user(userid):
    for temp in UserFlask.USERS:
        if temp.get_id() == userid:
            return temp


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
@login_required
def newsResult_page():
    result = []
    newsList = spider_news.spider_news()
    keyword = request.form.get('query')

    useful_functions.insert_action(current_user.username, current_user.id, keyword)

    list_title, list_url = newsList.getDC()
    for i in range(len(list_title)):
        if list_title[i].__contains__(keyword):
            result.append((i + 1, list_title[i], 'http://data.cma.cn' + list_url[i]))
    return render_template('news_result.html', form=result)


if __name__ == '__main__':
    app.run(debug=True)
