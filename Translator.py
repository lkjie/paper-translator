#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liwenjie'
import requests
import json
import os
import re

FILE_PATH = os.path.split(os.path.realpath(__file__))[0]


class Translator:
    '''
    翻译类
    '''

    def __init__(self):
        self.RES_PATH = FILE_PATH + 'translated.json'
        try:
            self.translated = json.load(open(self.RES_PATH))
        except Exception as e:
            self.translated = {}

    def getRequests(self, results, timeout=3, retries=3):
        '''
        请求网页得到翻译结果
        :param results: 
        :param timeout: 每次请求的超时秒数
        :param retries: 最大重试次数，请求失败后有效
        :return: 
        '''
        for _ in range(retries):
            try:
                return requests.post('http://fy.iciba.com/ajax.php?a=fy', data={'w': results}, timeout=timeout).json()
            except Exception as e:
                pass
        return {'content': {'out': results}}

    def textClean(self, textData):
        '''
        清理文本中的换行、-、空格等
        :param textData: 
        :return: 
        '''
        results = textData.replace('\n', ' ').replace('- ', '')
        return re.sub(' +', ' ', results)

    def translate(self, textData):
        '''
        翻译函数，给定清理后的文本，得到翻译结果
        :param textData: 
        :return: 
        '''
        try:
            if textData in self.translated:
                return self.translated[textData]
            resTran = self.getRequests(textData)
            content = resTran.get('content', {})
            if 'out' in content.keys():
                tranTxt = content['out']
            elif 'word_mean' in content.keys():
                tranTxt = '\n'.join(content['word_mean'])
            else:
                return ''
            # keep faster
            if len(self.translated.keys()) > 100000:
                os.rename('translated.json', 'translated.json.bak')
                self.translated.clear()
            self.translated[textData] = tranTxt
            json.dump(self.translated, open(self.RES_PATH, 'w'), ensure_ascii=False, indent=4)
            return tranTxt
        except Exception as e:
            return str(e)
