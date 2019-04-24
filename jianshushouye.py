#多线程抓取简书首页投稿信息
import requests
from lxml import etree
import re
import time
import pymongo
from multiprocessing import Pool

client = pymongo.MongoClient('localhost', 27017)
mydb = client['mydb']
jianshu_shouye = mydb['jianshu_shouye']

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

def get_jianshu_info(url):
    wb_data = requests.get(url,headers=headers)
    #print(wb_data.text)
    selector = etree.HTML(wb_data.text)
   # print(etree.tostring(selector))
    infos = selector.xpath('//*[@id="list-container"]/ul/li')
    for info in infos:
        try:
            author = info.xpath('div/div/a[1]/text()')[0]
            title = info.xpath('div/a/text()')[0]
            content = info.xpath('div/p/text()')[0]
            rewards = info.xpath('div/div/span[3]/text()')
            if len(rewards) == 0:
                reward = '无'
            else:
                reward = rewards[0].strip()
            comment = info.xpath('div/div/a[2]/text()')[1].strip()
            likes = info.xpath('div/div/span[2]/text()')
            if len(likes) == 0:
                like = '无'
            else:
                like = likes[0].strip()
            data = {
                'author':author,
                'title':title,
                'content':content,
                'like':like,
                'comment':content,
                'reward':reward
            }
            print(author,title,content,reward,comment,like)
            jianshu_shouye.insert_one(data)
            time.sleep(1)
        except IndexError:
            pass

if __name__ == '__main__':
    urls = ['http://www.jianshu.com/c/bDHhpK?order_by=added_at&page={}'.format(str(i)) for i in range(1, 10001)]
    pool = Pool(processes=4)
    pool.map(get_jianshu_info,urls)
