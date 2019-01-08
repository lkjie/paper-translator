#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lkjie'

# 组合框的保存字符串最大长度
COMBO_SIZE = 50

# 组合框每个字符串最大长度，超过用“...”代替
COMBO_STRLEN = 70

# 翻译结果保存时间间隔（毫秒），每分钟保存一次翻译结果
STORE_INTERVAL = 60000

# 剪切板检测间隔（毫秒），值越小越灵敏
TRANS_INTERVAL = 1000

# 翻译结果最大条目，超过条目会清空内存中保存的条目
TRANS_SIZE = 100000

# 请求参数
REQUEST_PARAMS = {
    'timeout': 3,
    # 需要代理可以在此配置
    # 'proxies': {
    #     'http': 'socks5://127.0.0.1:1080',
    #     'https': 'socks5://127.0.0.1:1080'
    # }
}

# 请求失败重试次数
REQUEST_RETRIES = 3

# 有道cookie，如果有道无法使用，请更换cookie，利用chrome查看http://fanyi.youdao.com/中的ranslate_o?smartresult=dict&smartresult=rule接口携带cookie即可
YOUDAO_COOKIES = "OUTFOX_SEARCH_USER_ID=237475211@10.169.0.83; JSESSIONID=aaadamaKQd46s6cpvyRGw; OUTFOX_SEARCH_USER_ID_NCOO=1761207998.1990373; ___rl__test__cookies="
