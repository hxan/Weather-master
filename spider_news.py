import requests
from lxml import  etree
import time
# https://data.cma.cn/article/getList/cateId/4/page/2.html气象科普
# https://data.cma.cn/article/getList/cateId/3/page/2.html 动态咨询
# https://data.cma.cn/article/getList/cateId/6/page/2.html服务快报
# https://data.cma.cn/article/getServiceCase/cateId/9.html服务案列
# https://data.cma.cn/article/getList/cateId/5.html 标准规范

class spider_news:
    def __init__(self):
        self.header = {
        'authority': 'data.cma.cn',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://data.cma.cn/article/getList/cateId/6.html',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'PHPSESSID=224v4fbis45cf71j5ff1m6ldm2; Hm_lvt_d9508cf73ee2d3c3a3f628fe26bd31ab=1647950882,1648214570; login_id_chat=0; _pk_testcookie.6.dd70=1; _pk_ses.6.dd70=1; _pk_ses.1.dd70=*; Hm_lpvt_d9508cf73ee2d3c3a3f628fe26bd31ab=1648216164; _pk_id.6.dd70=2572837100a0a746.1647950883.2.1648216164.1648214570.; _pk_id.1.dd70=a249de4b9adaf60f.1647950883.2.1648216164.1647951306.; login_name_chat=0',
        'sec-gpc': '1',
    }

    # 气象科普 动态咨询 服务快报
    def do_get_news(self,url,beginP,endP):
        res_title = []
        res_url = []
        for i in range(beginP,endP+1):
            rep = requests.get(url+str(i)+'.html', headers=self.header, timeout=5)
            rep.encoding = 'utf-8'
            tree = etree.HTML(rep.text)
            temp = tree.xpath('//div[@class="body-content-right"]//ul[@class="list1229"]//li//a//text()')
            temp_url = tree.xpath('//div[@class="body-content-right"]//ul[@class="list1229"]//li//a//@href')
            res_title.extend(temp)
            res_url.extend(temp_url)
            # for j in range(0,len(res_url):
            # 	res_url[j] = 'https://data.cma.cn/'+res_url[j]
            time.sleep(0.1)
        return res_title,res_url


    #气象科普 Meteorological science
    def getMS(self):
        return self.do_get_news('http://data.cma.cn/article/getList/cateId/4/page/',56,59)

    #动态咨询 Dynamic consulting
    def getDC(self):
        return self.do_get_news('http://data.cma.cn/article/getList/cateId/3/page/', 40, 51)

    #服务快报 Service letters
    def getSL(self):
        return self.do_get_news('http://data.cma.cn/article/getList/cateId/6/page/',1,11)

    # 服务案例 Service Case
    def getSC(self):
        rep = requests.get('http://data.cma.cn/article/getServiceCase/cateId/9.html', headers=self.header, timeout=5)
        rep.encoding = 'utf-8'
        tree = etree.HTML(rep.text)
        temp = tree.xpath('//div[@class="case_name"]//text()')
        return temp                                                                                                

    #标准规范 Stadard Specification
    def getSS(self):
        return self.do_get_news('http://data.cma.cn/article/getList/cateId/5/page/',1,1)

if __name__ =='__main__':

    t = spider_news()

    print('气象科普',t.getMS())
    # print('气象科普',t.getDC())
    # print('服务快报',t.getSL())
    # print('服务案例',t.getSC())
    # print('标准规范',t.getSS())

