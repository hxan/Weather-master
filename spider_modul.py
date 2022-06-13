import requests
import queue
import pymysql
import json
from lxml import etree
import threading
import re
import useful_functions
import fake_user_agent
from tqdm import tqdm

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
# }

dateRange = "20220330000000,20220401000000"

cityOfID = {}
with open('static/assets/geojson/Id.json', 'r', encoding='utf-8') as f:
    cityOfID = json.load(f)
    f.close()

# 代理池
headers = fake_user_agent.useragent_random()

# 爬取线程
class MyThread(threading.Thread):
    def __init__(self, url_queue):
        super(MyThread, self).__init__()
        self.url_queue = url_queue
        self.urls = [] 

        # 连接Mysql数据库
        self.cnn = pymysql.connect(host='127.0.0.1', user='root', password='123456', port=3306, database='weather',
                                   charset='utf8')
        self.cursor = self.cnn.cursor()
        #                                               0     1    2    3      4           5   6          7      8   9    10      11       12          13              14            15         16      17   
        self.sql = "insert into weather(Station_Id_C, city, Day, Hour, PRS, PRS_Max, PRS_Min, TEM, TEM_Max, TEM_Min, RHU, VAP, PRE_1h, WIN_S_Max, WIN_D_S_Max, WIN_D_INST_Max, WIN_S_Inst_Max, RHU_Min,url) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # 获取已爬取的url数据并写入列表，用于判断
        sql = 'select url from weather'
        self.cursor.execute(sql)
        for url in self.cursor.fetchall():
            self.urls.append(url[0])
            
    def run(self):
        self.spider()

    def spider(self):
        while not self.url_queue.empty():
            item = {}
            url = self.url_queue.get()
            if self.check_url(url):   #url是否存在
                #文件下载地址
                f=requests.get(url, stream=True)
                data = f.content.decode('utf-8')
                data = json.loads(data, encoding='utf-8')
                if 'DS' in data.keys():
                    for i in range(len(data['DS'])):
                        item['Station_Id_C'] = data['DS'][i]['Station_Id_C']
                        item['city'] = cityOfID[item['Station_Id_C']]
                        item['Day'] = data['DS'][i]['Day']
                        item['Hour'] = data['DS'][i]['Hour']
                        item['PRS'] = data['DS'][i]['PRS']
                        item['PRS_Max'] = data['DS'][i]['PRS_Max']
                        item['PRS_Min'] = data['DS'][i]['PRS_Min']
                        item['TEM'] = data['DS'][i]['TEM']
                        item['TEM_Max'] = data['DS'][i]['TEM_Max']
                        item['TEM_Min'] = data['DS'][i]['TEM_Min']
                        item['RHU'] = data['DS'][i]['RHU']
                        item['VAP'] = data['DS'][i]['VAP']
                        item['PRE_1h'] = data['DS'][i]['PRE_1h']
                        item['WIN_S_Max'] = data['DS'][i]['WIN_S_Max']
                        item['WIN_D_S_Max'] = data['DS'][i]['WIN_D_S_Max']
                        item['WIN_D_INST_Max'] = data['DS'][i]['WIN_D_INST_Max']
                        item['WIN_S_Inst_Max'] = data['DS'][i]['WIN_S_Inst_Max']
                        item['RHU_Min'] = data['DS'][i]['RHU_Min']
                        item['url'] = url[163:207]
                        self.save(item)
                    print('dataline saved : ' + item['Station_Id_C']  +' .')
                    
    def save(self, item):
        self.cursor.execute(self.sql,
                            [item['Station_Id_C'], item['city'], item['Day'], item['Hour'], item['PRS'], item['PRS_Max'], item['PRS_Min'], \
                             item['TEM'], item['TEM_Max'], item['TEM_Min'], item['RHU'], item['VAP'], item['PRE_1h'], \
                             item['WIN_S_Max'], item['WIN_D_S_Max'], item['WIN_D_INST_Max'], item['WIN_S_Inst_Max'], item['RHU_Min'], item['url']])
        self.cnn.commit()

    def check_url(self, url):
        # 查看数据库中是否存在当前爬取的url，如果存在则放弃爬取
        if url[163:207] in self.urls:
            # print(f'{url}已存在')
            return False
        else:
            self.urls.append(url[163:207])
            return True

    def get_news(self, text, item):
        # 获取js渲染后的网址并请求
        str = re.search('window.location.href=".*?"', text).group()
        link = re.split('"', str)[1] + '&page=0'

        response = requests.get(url=link, headers=headers, stream=True)
        response.encoding = "utf-8"
        html = etree.HTML(response.text)
        item['author'] = \
        html.xpath('//div[contains(@class,"article-content")]/div[2]/div[@class="user-main"]/h4/a/text()')[0]

        item['title'] = html.xpath('//div[@class="article-content"]/h1/text()')[0]

        item['publish_time'] = html.xpath('//span[@class="time1"]/text()')[0]

        content = html.xpath('//div[@class="article-txt-content"]/p/text()')
        content = ''.join(content)
        content = re.sub('\s', '', content)
        item['content'] = content

        key_word = html.xpath("//div[@class='key-word fix mt15']/a/text()")
        key_word = ",".join(key_word)
        if not key_word:
            key_word = useful_functions.get_keyword_from_content(content)
            if not key_word:
                key_word = '无关键词'
            else:
                key_word.append()
                key_word = ", ".join(key_word)
        item['key_word'] = key_word

# 将获取到的url添加到队列中去
def add_urls(queue):
    cities = json.load(open('static/assets/geojson/city.json', encoding='utf-8'))
    for key, value in cities.items():
        url = 'http://api.data.cma.cn:8090/api?userId=64808365801564beD&pwd=Kzy6B3A&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR&timeRange=[' + dateRange + ']&staIDs=' + str(value) + '&elements=Station_Id_C,Day,Hour,PRS,PRS_Max,PRS_Min,TEM,TEM_Max,TEM_Min,RHU,VAP,PRE_1h,WIN_S_Max,WIN_D_S_Max,WIN_D_INST_Max,WIN_S_Inst_Max,RHU_Min'
        queue.put(url)

# 爬虫运行程序
def run():
    threads = []
    url_que = queue.Queue()
    add_urls(url_que)

    for i in range(10):
        thread = MyThread(url_que)
        threads.append(thread)
        thread.start()

if __name__ == '__main__':
    run()