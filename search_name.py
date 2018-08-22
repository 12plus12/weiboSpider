import requests
from pprint import pprint
from urllib.parse import urlencode


def search_name(name):
    base_url = 'https://m.weibo.cn/api/container/getIndex?'

    headers = {
        'Referer': 'https://m.weibo.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    parmas = {
        'containerid': '100103type=3&q={}&t=0'.format(name),
        'page_type': 'searchall',
    }

    url = base_url + urlencode(parmas, encoding='utf-8')

    response = requests.get(url, headers=headers)

    return response.json()


def parse(json_dict):
    items = json_dict.get('data').get('cards')

    for item in items:
        if item.get('card_type') == 11:
            first_name = item.get('card_group')[0].get('user').get('screen_name')
            while True:
                command = input('将要帮您爬取【{}】的微博，是否继续？(Y/N)\n'.format(first_name))
                if command.upper() == 'Y' or command.upper() == 'YES':
                    url = item.get('card_group')[0].get('scheme')
                    return url
                elif command.upper() == 'N' or command.upper() == 'NO':
                    return
                else:
                    continue


def search():
    name = input('请输入要爬取的用户名：\n')
    json_dict = search_name(name)
    url = parse(json_dict)
    return url

if __name__ == '__main__':
    url = search()
    print(url)
