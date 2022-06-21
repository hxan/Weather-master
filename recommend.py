# author:l
# contact: test@test.com
# datetime:2022/6/20 14:45
# software: PyCharm
# file    : recommend.py     
# description :推荐系统

import jieba
from gensim.models import doc2vec
from flask_login import current_user


def recommend_news(searchKeys, list_title, list_url):
    """
    简单推荐系统

    Parameters:
     param1 - 搜索记录列表
     param2 - 新闻标题列表

    Returns:
     返回结果

    Raises:
     None
    """

    train_set = []
    for i in range(0, len(list_title)):
        title = list_title[i]  # 拿到每一行
        word_list = jieba.lcut(title)  # 分词
        doc = doc2vec.TaggedDocument(word_list, tags=[i])
        train_set.append(doc)

    # 模型建立
    model = doc2vec.Doc2Vec(train_set, min_count=1, window=3, vector_size=300, sample=1e-3, workers=4)
    model.build_vocab(train_set)
    model.train(train_set, total_examples=model.corpus_count, epochs=model.epochs)

    vector = model.infer_vector(doc_words=searchKeys + jieba.lcut(current_user.address), alpha=0.25)
    similar_titles = model.docvecs.most_similar([vector], topn=3)

    #用于输出调试
    # for index, _ in similar_titles:
    #     print('http://data.cma.cn/' + list_url[index], list_title[index])

    return similar_titles


if __name__ == '__main__':
    searchKeys = ['河北', '广西', '极端天气', '雨']
    list_title = ['江南江淮等地将迎强对流、黄渤海及东海北部海域起风又起雾！',
                  '气象科普|春天每年变短30秒！', '小据推书|世间万物与植物、星辰、动物的相遇',
                  '国家气象中心为西藏气象预报员提供智能网格预报培训', '华南暴雨试验2020年度高空加密观测和雷达观测启动 首次全程采用远程方式 多种探测手段协同观测',
                  '湖南：开展天气现象视频智能观测仪安装及维护培训', '2020珠峰高程测量正式启动 西藏气象部门将开展高空探测保障服务', '五月的昆明，又见蓝花绽',
                  '小据看天气|中东部新一轮降雨全面开启',
                  'UNEP与IUCN联合建立基于生态系统的气候变化适应基金', '资产中心利用数据库技术生成多维度账务方法和系统 获国家知识产权局发明专利授权', '甘肃：推进“天翼云”大数据云平台建设',
                  '气象预警|强对流天气又来了！', '立夏的到来真的意味着夏天来了吗？', '小据看天气|凉风送爽北方“退烧” 江南大范围降雨“上岗”', '立夏丨时光如梭，立夏已至',
                  '五四青年节——无奋斗，不青春！', '“五一”小长假，在线看美景', '这个“五一”，高温与大雾同行！', '小据看天气|“五一”假期北方先热后凉 南方雨水频繁', '气象预警|大雾黄色预警',
                  '小据推书|天空的美 云知道', '山西：全面推进气象现代化2020年重点工作', '小据看天气|云南多阴雨 华北黄淮迎高温', '中国气象局将大力发展气候预测智能技术',
                  '甘肃：加强培训 提升全省观测质量管理能力', '陕西：高性能计算机系统硬件部署工作完成', '山西：推进智能网格气象预报业务建设', '关于台风，了解台风',
                  '华北黄淮喜提首个高温日，夏天就要来了！', '风云气象卫星防灾减灾国际培训项目获批', '河北：三项成果获2019年度省科学技术进步奖', '惊艳！！！天空现美景，不妨来看看！',
                  '江西：分钟级降水客观预报产品投入应用 服务汛期', '岳阳：三部门联合举办气象行业职业技能竞赛', '风云三号D星广角极光成像仪： 八年攻关首次实现低轨大视场极光观测',
                  '春天是最短的季节吗？',
                  'NASA发布全球地下水地图监测全球干旱状况', '知识科普|世界上第一个给风定级的科学家', '气象谚语知多少？', '陕西：两项研究荣获省科学技术进步奖',
                  '小据看天气|北方气温波动起伏 华南云南阴雨缠绵冷意足', '天津：自主研发软件实现地面观测数据实时自动备份', '打好气候这张“牌” ——宁夏气象局创新工作室发展侧记',
                  '雨一直下，你不是我认识的重庆', '世界地球日，请保护好我们共同的家园', '小据看天气|华北东北大风还将吹三天 云南将迎甘霖解渴', '2019年西北太平洋热带气旋最佳路径发布',
                  '一个四月，惊艳了时光', '四川西昌突发山火！', '全球变暖加剧骤旱风险', '搭乘4月列车，“get”天气气候对花期的影响',
                  '小据看天气|“全能型”冷空气到！北方“换季式”降温 南方暴雨“车轮战”', '黔东南：举行“三温三雨”仪器设备安装现场培训', '中央气象台组织3月下旬南方强对流预报技术交流',
                  '青海：柴达木盆地典型湖泊面积持续增大', '杭州让“纸面”专利迈出“高阁” ——疏通气象科技成果转化中的痛点、堵点、难点', '这不是你印象里的云南！',
                  '强对流天气又、双、叒 、叕来！专家解析近期强对流天气', '第九届全国台风及海洋气象专家工作组第二次会议召开', '黄泛区：小麦良种繁育气象保障标准化示范区获国标委立项',
                  '各地不一样的春雨“小性格”，值得一看！', '江南江淮要入夏？降雨：“你想多了”', '气象预警|沙尘暴天气、强对流天气继续预警', '湖南：完成“天脸”观测数据与CIMISS传输对接',
                  '黑龙江：明确七方面18项举措科技创新技术攻关措施', '庆阳：开展春玉米区域联合试验 提升服务能力', '辽宁：省气象局与省自然资源厅签署合作协议',
                  '强对流天气预报 |云南等地将有强对流天气',
                  '小据看天气|全国降水减少，江南宛如初夏', '“乱花渐欲迷人眼”，赏花知识已上线！', '四月飞雪！山东再次入春失败？', '广西：通过项目研究建立甘蔗智能精准服务新模式',
                  '国家气象中心组织召开暴雨预报技术视频交流会', '高分卫星内蒙古赤峰分中心获批成立', '多雨的春季，健康防护小知识来喽~', '南方又迎强降水，沙尘袭击西北部',
                  '福建：省气象局与国睿科技签署合作协议', '青海：发布云水资源精细化评估报告', '小据看天气 | 南方将迎新一轮降雨天气']
    list_url = ['/site/article/id/39936.html', '/site/article/id/39935.html', '/site/article/id/39934.html',
                '/site/article/id/39938.html', '/site/article/id/39940.html', '/site/article/id/39941.html',
                '/site/article/id/39942.html', '/site/article/id/39931.html', '/site/article/id/39930.html',
                '/site/article/id/40397.html', '/site/article/id/39932.html', '/site/article/id/39933.html',
                '/site/article/id/39928.html', '/site/article/id/39927.html', '/site/article/id/39925.html',
                '/site/article/id/39924.html', '/site/article/id/39921.html', '/site/article/id/39919.html',
                '/site/article/id/39918.html', '/site/article/id/39917.html', '/site/article/id/39916.html',
                '/site/article/id/39915.html', '/site/article/id/39914.html', '/site/article/id/39906.html',
                '/site/article/id/39907.html', '/site/article/id/39908.html', '/site/article/id/39909.html',
                '/site/article/id/39910.html', '/site/article/id/39902.html', '/site/article/id/39903.html',
                '/site/article/id/40398.html', '/site/article/id/39904.html', '/site/article/id/39898.html',
                '/site/article/id/39899.html', '/site/article/id/39900.html', '/site/article/id/39901.html',
                '/site/article/id/39892.html', '/site/article/id/40399.html', '/site/article/id/39891.html',
                '/site/article/id/39893.html', '/site/article/id/39894.html', '/site/article/id/39888.html',
                '/site/article/id/39889.html', '/site/article/id/39890.html', '/site/article/id/39885.html',
                '/site/article/id/39879.html', '/site/article/id/39880.html', '/site/article/id/39883.html',
                '/site/article/id/39873.html', '/site/article/id/39875.html', '/site/article/id/39867.html',
                '/site/article/id/39866.html', '/site/article/id/39865.html', '/site/article/id/39868.html',
                '/site/article/id/39870.html', '/site/article/id/39869.html', '/site/article/id/39871.html',
                '/site/article/id/39864.html', '/site/article/id/39859.html', '/site/article/id/39860.html',
                '/site/article/id/39861.html', '/site/article/id/39855.html', '/site/article/id/39854.html',
                '/site/article/id/39853.html', '/site/article/id/39857.html', '/site/article/id/39856.html',
                '/site/article/id/39852.html', '/site/article/id/39847.html', '/site/article/id/39844.html',
                '/site/article/id/39843.html', '/site/article/id/39842.html', '/site/article/id/39833.html',
                '/site/article/id/39836.html', '/site/article/id/39837.html', '/site/article/id/39838.html',
                '/site/article/id/39829.html', '/site/article/id/39830.html', '/site/article/id/39831.html',
                '/site/article/id/39832.html', '/site/article/id/39825.html']

    recommend_news(searchKeys, list_title, list_url)
