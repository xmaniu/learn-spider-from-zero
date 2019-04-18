#爬取起点小说名称
import xlwt
import requests
from lxml import etree
import  time

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

all_info_lists =[]
def get_info(url):
    html = requests.get(url,headers)
    print(url)
    print(html.status_code)
    selector = etree.HTML(html.text)
    infos = selector.xpath('//ul[@class="all-img-list cf"]/li')
    w = selector.xpath('/html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/p[3]/span/span/')

    for info in infos:
        print(info)
        title = info.xpath('div[2]/h4/a/text()')[0]
        author = info.xpath('div[2]/p[1]/a[1]/text()')[0]
        style_1 = info.xpath('div[2]/p[1]/a[2]/text()')[0]
        style_2 = info.xpath('div[2]/p[1]/a[3]/text()')[0]
        style = style_1+'·'+style_2
        complete = info.xpath('div[2]/p[1]/span/text()')[0]
        introduce = info.xpath('div[2]/p[2]/text()')[0].strip()
        word = info.xpath('div[2]/p[3]/span/text()')[0].strip('万字') #数字转成了图片，暂未解决
        info_list= [title,author,style,complete,introduce,word]
        print(info_list)
        all_info_lists.append(info_list)
    time.sleep(1)

if __name__ == '__main__':
    urls = ['https://www.qidian.com/all?page={}'.format(str(i)) for i in range(1,3)]
    for url in urls:
        get_info(url)

    header = ['title','author','style','complete','introduce','word']
    book = xlwt.Workbook(encoding='uft-8')
    sheet = book.add_sheet('Sheet1')
    for h in range(len(header)):
        sheet.write(0,h,header[h])

    i = 1
    for list in all_info_lists:
        j = 0
        for data in list:
            sheet.write(i,j,data)
            j += 1
        i += 1
    book.save('xiaoshuo.xlsx')