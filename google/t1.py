#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lkjie'
import execjs

'''
BUG:
shift error:
different js
python: 821618011 << 3 is 6572944088
js:     821618011 << 3 is -2016990504

'''

def intToBin32(i, base=32):
    return (bin(((1 << base) - 1) & i)[2:]).zfill(base)

def bin32ToInt(s, base=32):
    return int(s[1:], 2) - int(s[0]) * (1 << base-1)

def uRightMove(a, b, base=32):
    b = b & 0x1F # js feature
    n = intToBin32(a)
    n = '0' * b + n[:base-b]
    return bin32ToInt(n)

def Fo(a, b):
    for c in range(0, len(b) - 2, 3):
        d = b[c+2]
        if "a" <= d:
            d = ord(d[0]) - 87
        else:
            d = int(d)
        if "+" == b[c+1]:
            d = uRightMove(a, d)
        else:
            d = a << d
        if "+" == b[c]:
            a = a + d & 4294967295
        else:
            a = a ^ d
    return a

def tk(query):
    c = "&tk="
    d = ["429673", "1496275672"]
    b = 429673
    e = ['' for i in range(len(query))]
    f = 0
    for g in range(0, len(query)):
        k = ord(query[g])
        if 128 > k:
            e[f] = k
            f+=1
        else:
            if 2048 > k:
                e[f] = k >> 6 | 192
                f += 1
            elif 55296 == (k & 64512) and g + 1 < len(query) and 56320 == (ord(query[g+1]) & 64512):
                k = 65536 + ((k & 1023) << 10) + (ord(query[g+1]) & 1023)
                g+=1
                e[f] = k >> 18 | 240
                f += 1
                e[f] = k >> 12 & 63 | 128
                f += 1
            else:
                e[f] = k >> 12 | 224
                f+=1
                e[f] = k >> 6 & 63 | 128
                f+=1
            e[f] = k & 63 | 128
            f+=1
    a = b
    for f in range(0, len(e)):
        a+=e[f]
        a = Fo(a, "+-a^+6")
    a = Fo(a, "+-3^+b+-f")
    a ^= int(d[1]) or 0
    if 0 > a:
        a = (a & 2147483647) + 2147483648
    a %= 1E6
    a = int(a)
    return c + (str(a) + "." + str(a ^ b))

import requests
import re

proxies = {
            'http': 'socks5://127.0.0.1:1080',
            'https': 'socks5://127.0.0.1:1080'
        }
page = requests.get('https://translate.google.com/', proxies=proxies)
tkk = re.search("tkk:'(.+?)'", page.text).group(1)
query = "We present some positive evidence that shows our goal is achieved."
tk = execjs.compile(open(r"translate_google.js").read()).call('Ho',query,tkk)
# sl:原始语言 tl:目标语言
url = 'https://translate.google.com/translate_a/single?client=webapp&sl=auto&tl=zh-CN&hl=en&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&otf=2&ssel=0&tsel=4&kc=1&tk=%s&q=%s'%(tk, query)
res_trans = requests.get(url, proxies=proxies)
res_trans = res_trans.json()[0]
res_trans_target = [i[0] for i in res_trans[:-1]]
res_trans_target = ''.join(res_trans_target)
print(res_trans_target)