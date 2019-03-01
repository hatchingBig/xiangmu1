# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 15:26:11 2019

@author: Administrator
"""
import urllib
import re

def get_stock_list():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    ff = urllib.request.urlopen(stock_list_url)
    d = ff.read().decode('gbk')   
    start_p = d.index('股票代码查询一览表：') 
    stop_p = d.index('<!-- footer-2016 -->')
    content = d[start_p:stop_p]
    pattern = re.compile(u"href=\"(.*?)\">")
    tlist = pattern.findall(content)[2:]
    return tlist