import requests
import json
import time
import re
from urllib.parse import urlencode
from pprint import pprint
from pyquery import PyQuery as pq

import search_name


def weibo_spider(page, page_url, uid):

    base_url = 'https://m.weibo.cn/api/container/getIndex?'

    headers = {
        "Host": "m.weibo.cn",
        "MWeibo-Pwa": "1",
        "Referer": page_url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    parmas = {
        'type': 'uid',
        'value': uid,
        'containerid': '107603' + uid,
        'page': page
    }

    url = base_url+urlencode(parmas)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()

    except requests.ConnectionError as e:
        print('Error', e.args)


def parse(json_file):
    """解析"""
    if json:
        items = json_file.get('data').get('cards')

        for item in items:
            # 需要提取的是‘card_type为9的数据’
            if item.get('card_type') == 9:
                item = item.get('mblog')
                weibo = dict()

                # 提取该博主内容
                weibo['text'] = pq(item.get('text')).text()
                # 提取转发数
                weibo['reposts_count'] = item.get('reposts_count')
                # 提取评论数
                weibo['comments_count'] = item.get('comments_count')
                # 提取点赞数
                weibo['attitudes_count'] = item.get('attitudes_count')
                # 发布时间
                weibo['time'] = item.get('created_at')

                image = item.get('original_pic', None)
                if item.get('original_pic'):
                    weibo['image'] = image

                yield weibo


def save_to_file(weibo):
    """存储到文件"""
    with open('weibo.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(weibo, ensure_ascii=False) + '\n')


def main():

    # 调用按用户名找到微博的方法，获取第一页的url地址
    page_url = search_name.search()
    if not page_url:
        print("---结束---")
        return

    # 需要取出url中的查询参数拼接到base_url中，提交一个ajax请求
    pattern = re.compile(r'uid\=(\d+)\&')
    uid = pattern.search(page_url).group(1)

    for page in range(1, 10):
        json_file = weibo_spider(page, page_url, uid)

        for weibo in parse(json_file):
            save_to_file(weibo)
            # break
        # break
        time.sleep(1)


if __name__ == '__main__':
    main()
