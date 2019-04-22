#抓取妹子图
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

download_links = []
path = 'D:/Projects/Python/learn-spider-from-zero/mzitu/'
url = 'https://www.mzitu.com/'
res = requests.get(url,headers=headers)
soup = BeautifulSoup(res.text,'lxml')
imgs = soup.select('#pins > li > a > img')
for img in imgs:
    print(img.get('data-original'))
    download_links.append(img.get('data-original'))
for item in download_links:
    #有问题
    urlretrieve(item,path + item[-10:])
