#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lkjie'
import requests
import json
import os
import re
import hashlib
import time
import execjs
import urllib

from configures import *

FILE_PATH = os.path.split(os.path.realpath(__file__))[0]


class CiBa():
    '''
    金山词霸的翻译接口，推荐使用，感觉挺准的，优于谷歌有道
    '''

    def request(self, content, retries=3):
        '''
        请求网页得到翻译结果
        :param content: 
        :param timeout: 每次请求的超时秒数
        :param retries: 最大重试次数，请求失败后有效
        :return: {'out':'翻译结果','word_mean':'单词解释'} 两者选一
        '''
        for _ in range(retries):
            try:
                res = requests.post('http://fy.iciba.com/ajax.php?a=fy', data={'w': content}, **REQUEST_PARAMS).json()
                res = res.get('content', {})
                return res
            except Exception as e:
                pass
        return {}


class Google():
    '''
    谷歌的翻译接口，请自带翻墙代理，在下面proxies中配置
    '''

    def __init__(self):
        # get TKK
        self.update_tkk()

    def update_tkk(self):
        page = requests.get('https://translate.google.cn/', **REQUEST_PARAMS)
        self.tkk = re.search("tkk:'(.+?)'", page.text).group(1)
        self.tkk_updatetime = time.time()

    def request(self, content, retries=3):
        '''
        请求网页得到翻译结果
        :param content: 
        :param timeout: 每次请求的超时秒数
        :param retries: 最大重试次数，请求失败后有效
        :return: {'out':'翻译结果','word_mean':'单词解释'} 两者选一
        '''
        if time.time() - self.tkk_updatetime > 3600:
            self.update_tkk()
        for _ in range(retries):
            try:
                tk = execjs.compile(open(r"translate_google.js").read()).call('Ho', content, self.tkk)
                content = urllib.parse.quote(content)
                # sl:原始语言 tl:目标语言
                url = 'https://translate.google.cn/translate_a/single?client=webapp&sl=auto&tl=zh-CN&hl=en&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&otf=2&ssel=0&tsel=4&kc=1&tk=%s&q=%s' % (
                tk, content)
                res_trans = requests.get(url, **REQUEST_PARAMS)
                res_trans = res_trans.json()[0]
                res_trans_target = [i[0] for i in res_trans[:-1]]
                res_trans_target = ''.join(res_trans_target)
                return dict(out=res_trans_target)
            except Exception as e:
                pass
        return {}


class YouDao():
    '''
    有道的翻译接口，有个智能结果，是单词的话有详细解释
    注意：有道翻译是反爬的，需要定时更换cookie，cookie请自行更换，从浏览器中复制translate_o请求中的cookie即可
    '''

    def request(self, content, retries=3):
        '''
        请求网页得到翻译结果
        :param content: 
        :param timeout: 每次请求的超时秒数
        :param retries: 最大重试次数，请求失败后有效
        :return: 
        '''
        for _ in range(retries):
            try:
                url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
                ts = str(int(time.time() * 1000))
                salt = ts + "5"
                sign = hashlib.md5(("fanyideskweb" + content + salt + "p09@Bn{h02_BIEe]$P^nG").encode()).hexdigest()
                header = {
                    # "Accept": "application/json, text/javascript, */*; q=0.01",
                    # "Accept-Encoding": "gzip, deflate",
                    # "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
                    # "Connection": "keep-alive",
                    # "Content-Length": str(250+len(content)),
                    # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    # "Host": "fanyi.youdao.com",
                    # "Origin": "http://fanyi.youdao.com",
                    "Referer": "http://fanyi.youdao.com/",
                    "User-Agent": "5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                    # "X-Requested-With": "XMLHttpRequest"
                }
                header['Cookie'] = YOUDAO_COOKIES + ts
                bv = hashlib.md5(header['User-Agent'].encode()).hexdigest()
                data = {
                    "action": "FY_BY_REALTIME",
                    "bv": bv,
                    "client": "fanyideskweb",
                    "doctype": "json",
                    "from": "AUTO",
                    "i": content,
                    "keyfrom": "fanyi.web",
                    "salt": salt,
                    "sign": sign,
                    "smartresult": "dict",
                    "to": "AUTO",
                    "ts": ts,
                    "typoResult": False,
                    "version": "2.1"
                }

                res = requests.post(url=url, data=data, headers=header, **REQUEST_PARAMS).json()
                translateResult = res.get('translateResult', [])
                out = ''
                if translateResult:
                    out = ''.join([e.get('tgt', "") for e in translateResult[0]])
                smartResult = ''.join(res.get('smartResult', {}).get('entries', []))
                out = (out + smartResult).replace('\r\n', '\n')
                return dict(out=out)
            except Exception as e:
                pass
        return {}


class Translator:
    '''
    翻译类
    '''
    ciba = CiBa()
    youdao = YouDao()
    google = Google()
    engine = 'ciba'

    def __init__(self):
        self.RES_PATH = FILE_PATH + os.sep + 'translated.json'
        self.engine_dict = {'ciba': self.ciba,
                            'youdao': self.youdao,
                            'google': self.google}
        self.engine_name_dict = {'金山词霸': 'ciba',
                            '有道': 'youdao',
                                 '谷歌翻译': 'google'}
        try:
            self.translated = json.load(open(self.RES_PATH, encoding='utf8'))
        except Exception as e:
            self.translated = {k: {} for k in self.engine_dict.keys()}

    def getRequests(self, srcContent):
        '''
        请求网页得到翻译结果
        :param srcContent: 
        :param engine: 默认翻译引擎
        :return: {'out':'翻译结果','word_mean':'单词解释'} 两者选一
        '''
        if self.engine in self.engine_dict:
            return self.engine_dict[self.engine].request(srcContent)
        else:
            return self.ciba.request(srcContent)

    def textClean(self, textData, customRe=''):
        '''
        清理文本中的换行、-、空格等
        :param textData: 
        :return: 
        '''
        results = textData.replace('\n', ' ').replace('- ', '')
        if customRe:
            results = re.sub(customRe, ' ', results)
        results = re.sub(' +', ' ', results)
        return results.strip()

    def translate(self, textData):
        '''
        翻译函数，给定清理后的文本，得到翻译结果
        :param textData: 
        :return: 
        '''
        try:
            if textData in self.translated[self.engine]:
                return self.translated[self.engine][textData]
            content = self.getRequests(textData)
            if 'out' in content.keys():
                tranTxt = content['out']
            elif 'word_mean' in content.keys():
                tranTxt = '\n'.join(content['word_mean'])
            else:
                return '翻译错误！'
            # keep faster
            if len(self.translated[self.engine].keys()) > TRANS_SIZE:
                self.restore(path=self.RES_PATH + 'backup')
                self.translated[self.engine].clear()
            self.translated[self.engine][textData] = tranTxt
            return tranTxt
        except Exception as e:
            return str(e)

    def restore(self, path=None):
        if path:
            json.dump(self.translated, open(path, 'w', encoding='utf8'), ensure_ascii=False, indent=4)
        else:
            json.dump(self.translated, open(self.RES_PATH, 'w', encoding='utf8'), ensure_ascii=False, indent=4)
