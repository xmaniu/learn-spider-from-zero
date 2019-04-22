import requests
from lxml import etree
import time

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

urls = ['http://jandan.net/ooxx/page-{}'.format(str(i)) for i in range(0,20)]
path = 'D:/Projects/Python/learn-spider-from-zero/jandan/'

def get_photo(url):
    html = requests.get(url,headers=headers)
    selector = etree.HTML(html.text)
    photo_urls = selector.xpath('//p/a[@class="view_img_link"]/@href')

    for photo_url in photo_urls:
        print(photo_url)
        data = requests.get('http:'+photo_url,headers=headers)
        fp = open(path+photo_url[-10:],'wb') #打开文件
        fp.write(data.content) #把图片内容写入文件
        fp.close() #关闭文件
for url in urls:
    get_photo(url)
    time.sleep(2)
