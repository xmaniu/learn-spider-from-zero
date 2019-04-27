##通过百度翻译接口将中文翻译为英文，传到pexels下载图片
import requests
from bs4 import BeautifulSoup
import hashlib
import json
import random

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

#图片保存路径
path = 'D:/Projects/Python/learn-spider-from-zero/img'

#百度翻译接口地址
url="http://api.fanyi.baidu.com/api/trans/vip/translate"
appid = ''  # 你的appid
secretKey = ''  # 你的密钥
salt = random.randint(32768, 65536)

def get_tra_res(q,fromLang='cht',toLang='en'):
#生成签名
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
#post请求参数
    data = {
        "appid": appid,
        "q": q,
        "from": 'zh',
        "to" : 'en',
        "salt" : str(salt),
        "sign" : sign,
    }
#post请求
    res = requests.post(url, data=data)
#返回时一个json
    trans_result = json.loads(res.content).get('trans_result')[0].get("dst")
    return trans_result

#获取图片
def get_img(url):
    res = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text,'lxml')
    imgs = soup.select('article > a.js-photo-link.photo-item__link > img')

    #下载图片
    for img in imgs:
        img_url = img.get('data-big-src').split('?')[0]
        print(img_url)
        img_data = requests.get(img_url,headers=headers)
        f = open('img/'+img_url[-10:],'wb')
        f.write(img_data.content)
        f.close()

if __name__ == '__main__':
    word = input('请输入名称：')
    print(get_tra_res(word))
    url = 'https://www.pexels.com/search/'+get_tra_res(word).split()[0]
    urls = [(url+'?page={}').format(str(i)) for i in range(1,10)]
    for url in urls:
        print(url)
        get_img(url)