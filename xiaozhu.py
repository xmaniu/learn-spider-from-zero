# 爬取小猪短租网信息
import requests
from bs4 import BeautifulSoup
import time

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

#判断用户的性别
def judgment_sex(class_name):
    if class_name == ['member_ico']:
        return '男'
    else:
        return '女'

#定义获取详情页面的URL
def get_links(url):
    wb_data = requests.get(url,headers=headers)

    soup = BeautifulSoup(wb_data.text,'lxml')
    links = soup.select('#page_list > ul > li > a')
    for link in links:
        href = link.get('href')
       # print(href)
        get_info(href)
        time.sleep(3)

#定义获取页面详细信息
def get_info(url):
    wd_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(wd_data.text,'lxml')
    titles = soup.select('div.pho_info > h4')
    addresses = soup.select('div.pho_info > p > span.pr5')
    prices = soup.select('#pricePart > div.day_l > span')
    imgs = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > a > img')
    names = soup.select('div.con_l > div.pho_info > h4 > em')
    sexs = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > div')

    for title,address,price,img,name,sex in zip(titles,addresses,prices,imgs,names,sexs):
        data = {
            'title' : title.get_text().strip(),
            'address' : address.get_text().strip(),
            'price' : price.get_text().strip(),
            'img' : img.get('src'),
            'name' : name.get_text().strip(),
            'sex': judgment_sex(sex.get('class'))
        }
        print(data)

if __name__ == '__main__':
    urls = ['http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(number) for number in range(1,14)]
    for single_url in urls:
        get_links(single_url)
        time.sleep(6)


