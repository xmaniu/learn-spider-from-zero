import requests
import json
import time

headers = {
    'Cookie':'',
    'User_Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

f = open('C:/Users/Administrator/Desktop/weibo.txt','a+',encoding='utf-8')

def get_info(url,page):
    html = requests.get(url,headers=headers)
    print(html.status_code)
    json_data = json.loads(html.text)
    #print(json_data)
    card_groups = json_data['data']['statuses']
    #print(card_groups)
    for card_group in card_groups:
        print(card_group['text'])
        f.write(card_group['text'].split(' ')[0].strip()+'\n')

    next_cursor = json_data['data']['next_cursor']

    if page<90:
        next_url = 'https://m.weibo.cn/feed/friends?max_id='+str(next_cursor)
        page = page + 1
        get_info(next_url,page)
        time.sleep(2)
    else:
        pass
        f.close()

if __name__ == '__main__':
    url = 'https://m.weibo.cn/feed/friends?max_id=4366165947821581'
    get_info(url,1)
