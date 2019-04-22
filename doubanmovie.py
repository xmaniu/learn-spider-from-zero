#抓取豆瓣电影Top250信息
import requests
import re
from lxml import etree
import pymysql
import time
# 表结构
# CREATE TABLE IF NOT EXISTS `doubanmovie` (
#   `name` text NOT NULL,
#   `director` text NOT NULL,
#   `actor` text NOT NULL,
#   `style` text NOT NULL,
#   `country` text NOT NULL,
#   `release_time` text NOT NULL,
#   `time` text NOT NULL,
#   `score` text NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

conn = pymysql.connect(host='localhost', user='root', passwd='', db='mydb', port=3306, charset='utf8')
cursor = conn.cursor()

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

def get_movie_url(url):
    wb_data = requests.get(url,headers=headers)
    selector = etree.HTML(wb_data.text)
    movie_hrefs = selector.xpath('//div[@class="hd"]/a/@href')
    for movie_href in movie_hrefs:
        get_movie_info(movie_href)

def get_movie_info(url):
    wd_data = requests.get(url,headers=headers)
    selector = etree.HTML(wd_data.text)
    try:
        name = selector.xpath('//*[@id="content"]/h1/span[1]/text()')[0]
        director = selector.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')[0]
        actors = selector.xpath('//*[@id="info"]/span[3]/span[2]')[0]
        actor = actors.xpath('string(.)')
        style = re.findall('<span property="v:genre">(.*?)</span>',wd_data.text,re.S)[0]
        country = re.findall('<span class="pl">制片国家/地区:</span> (.*?)<br/>',wd_data.text,re.S)[0]
        release_time = re.findall('上映日期:</span>.*?>(.*?)</span>',wd_data.text,re.S)[0]
        time = re.findall('片长:</span>.*?>(.*?)</span>',wd_data.text,re.S)[0]
        score = selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')[0]
        print(name,director,actor,style,country,release_time,time,score)
        cursor.execute(
            "insert into doubanmovie (name,director,actor,style,country,release_time,time,score) values(%s,%s,%s,%s,%s,%s,%s,%s)",
            (str(name), str(director), str(actor), str(style), str(country), str(release_time), str(time), str(score)))

    except IndexError:
        pass

if __name__ == '__main__':
    urls = ['https://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0, 250, 25)]
    for url in urls:
        get_movie_url(url)
        time.sleep(2)
    conn.commit()