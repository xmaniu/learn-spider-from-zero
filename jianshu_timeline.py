import requests
from lxml import etree
import pymongo

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}
client = pymongo.MongoClient('localhost', 27017)
mydb = client['mydb']
timeline = mydb['timeline']

def get_time_info(url,page):
    print(url)
    user_id = url.split('/')
    user_id = user_id[4]
    if url.find('page='):
        page = page+1
    html = requests.get(url,headers=headers)
    selector = etree.HTML(html.text)
    infos = selector.xpath('//ul[@class="note-list"]/li')
    for info in infos:
        attention_time = info.xpath('div/div/div/span/@data-datetime')[0]
        type = info.xpath('div/div/div/span/@data-type')[0]
        print(attention_time,type)
        timeline.insert_one({'attention_time':attention_time,'type':type})

    id_infos = selector.xpath('//ul[@class="note-list"]/li/@id')
    if len(infos) > 1:
        feed_id = id_infos[-1]
        max_id = feed_id.split('-')[1]
        next_url = 'https://www.jianshu.com/users/%s/timeline?max_id=%s&page=%s' % (user_id, max_id, page)
        get_time_info(next_url, page)

if __name__ == '__main__':
    get_time_info('https://www.jianshu.com/users/a355fb89cfd6/timeline',1)
