import requests
from lxml import etree
import time
import pymongo
import re

client = pymongo.MongoClient('localhost', 27017)
mydb = client['mydb']
tongcheng_url = mydb['tongcheng_url']
tongcheng_info = mydb['tongcheng_info']

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Connection':'keep-alive'
}

def get_links(channel,pages):
    list_view = '{}pn{}/'.format(channel,str(pages))
    print(list_view)
    try:
        html = requests.get(list_view,headers=headers)
        time.sleep(5)
        selector = etree.HTML(html.text)
        if selector.xpath('//tr'):
            infos = selector.xpath('//tr')
            for info in infos:
                if info.xpath('td[2]/a/@href'):
                    url = info.xpath('td[2]/a/@href')[0]
                    tongcheng_url.insert_one({'url':url})
                else:
                    pass
        else:
            pass
    except requests.exceptions.ConnectionError:
        pass

def get_info(url):
    html = requests.get(url,headers=headers)
    #time.sleep(5)
    selector = etree.HTML(html.text)
    try:
        title = selector.xpath('//*[@id="basicinfo"]/div[1]/h1/text()')[0].strip()
        #if selector.xpath('//span[@class="price_now"]/i/text()'):
        if selector.xpath('//*[@id="basicinfo"]/div[3]/div[1]/div[2]/span/text()'):
            price = selector.xpath('//*[@id="basicinfo"]/div[3]/div[1]/div[2]/span/text()')[0].strip()
        else:
            price = "无"
        if selector.xpath('//*[@id="basicinfo"]/div[3]/div[3]/div[2]/a/text()'):
            area = selector.xpath('//*[@id="basicinfo"]/div[3]/div[3]/div[2]/a/text()')[0].strip()
        else:
            area = "无"
        #view = selector.xpath('//*[@id="totalcount"]/text()')
        published = re.findall('<div class="detail-title__info__text">(.*?) 发布</div>',html.text)[0]
        if selector.xpath('//*[@id="basicinfo"]/div[3]/div[4]/div[2]/a[1]/text()'):
            contact = selector.xpath('//*[@id="basicinfo"]/div[3]/div[4]/div[2]/a[1]/text()')[0]
        else:
            contact = "无"
        info = {
            'tittle':title,
            'price':price,
            'published':published,
            'area':area,
            #'view':view,
            'contact':contact,
            'url':url
        }
        print(info)
        tongcheng_info.insert_one(info)
    except IndexError:
        pass

#get_info('https://sh.58.com/shouji/37864002989595x.shtml')