import requests
from requests.exceptions import ConnectionError
from proxypool.setting import PROXY_POOL_URL
base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


def get_page(url, options={}):
    """
    抓取代理
    :param url:
    :param options:
    :return:
    """
    headers = dict(base_headers, **options)
    print('正在抓取', url)
    try:
        response = requests.get(url, headers=headers)
        print('抓取成功', url, response.status_code)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        try:
            proxies = {
                "http": "http://{proxy}".format(proxy=get_proxy()),
                "https": "http://{proxy}".format(proxy=get_proxy()),
            }
            response = requests.get(url, headers=headers, proxies=proxies)
            print('抓取成功', url, response.status_code)
            if response.status_code == 200:
                return response.text

        except ConnectionError:
            print('抓取失败', url)
            return None
