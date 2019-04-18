#爬取豆瓣图书Top250
import requests
from lxml import etree
import csv

fp = open(r'C:\Users\Administrator\Desktop\doubanbook.csv','wt',newline='',encoding='utf-8')
writer = csv.writer(fp)
writer.writerow(('name','url','author','publisher','date','price','rate','comment'))
urls = ['https://book.douban.com/top250?start={}'.format(str(i)) for i in range(0,250,25)]

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

for url in urls:
    html = requests.get(url,headers=headers)
    selector = etree.HTML(html.text)
    infos = selector.xpath('//tr[@class="item"]')
    for info in infos:
        name = info.xpath('td/div/a/@title')[0]
        url = info.xpath('td/div/a/@href')[0]
        bookinfos = info.xpath('td/p/text()')[0]
        author = bookinfos.split('/')[0]
        publisher = bookinfos.split('/')[-3]
        date = bookinfos.split('/')[-2]
        price = bookinfos.split('/')[-1]
        rate = info.xpath('td/div/span[2]/text()')[0]
        comments = info.xpath('td/p/span/text()')
        comment = comments[0] if len(comments) !=0 else '空'
        print(name,url,author,publisher,date,price,rate,comment)
        writer.writerow((name,url,author,publisher,date,price,rate,comment))

fp.close()
