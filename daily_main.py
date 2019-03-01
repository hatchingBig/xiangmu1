# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 15:21:21 2019

@author: Administrator
"""

import re
import base64
import urllib
import struct  
import pandas as pd
import os
from dateutil.parser import parse
import datetime
import time as tag
from GetList import get_stock_list

def ParseStock(url):
    islabel = True
    while islabel:
        try:
            fp = urllib.request.urlopen(url, timeout=5)
            content = fp.read().decode("gb2312")
            patt = re.compile(r'\"(.*)\"')
            m = patt.search(content)
            start = m.start() + 1 
            end = m.end() - 1 
            cach_avg = []
            cach_price = []
            cach_amount = []
            while start < end:
                min = (content[start:start+16])
                start += 16
                b = base64.b64decode(min)
        
                avg = struct.unpack('<L', bytes(b[:4]))[0] / 1000.0
                price = struct.unpack('<L', bytes(b[4:8]))[0] / 1000.0
                amount = struct.unpack('<L', bytes(b[8:12]))[0]
                
                cach_avg.append(avg)
                cach_price.append(price)
                cach_amount.append(amount)
            islabel = False
        except:
            print('{}_sleep60'.format(str(datetime.datetime.now())))
            tag.sleep(60)
            
    dic = {'avg':cach_avg, 'price':cach_price, 'amount':cach_amount}
    df = pd.DataFrame(dic)
    return df

def main():
    date = input('请输入日期：')
    data_repos = input('请输入股票数据的存放位置：')
    date = str(parse(date))[:10].replace('-','')
    true_flag = os.path.exists('{}\{}'.format(data_repos,date))
    if true_flag:
        print('输入的日期已有文件存在！')
        raise ValueError
    small_sleep = 0.5
    try:
        os.makedirs('{}\{}\stock'.format(data_repos,date))
    except:
        pass
    try:
        os.makedirs('{}\{}\etf'.format(data_repos,date))
    except:
        pass
    try:
        os.makedirs('{}\{}\zhishu'.format(data_repos,date))
    except:
        pass    
    tlist = get_stock_list()
    compare_list_index = ['sz399','sh0']
    compare_list_stock = ['sh6','sz0','sz3']
    compare_list_etf = ['sh5','sz1']
    dic = {1:compare_list_index,2:compare_list_stock,3:compare_list_etf}
    dic_os = {1:'zhishu',2:'stock',3:'etf'}
    dic_name = {1:'指数',2:'股票',3:'基金'}
    count = 0
    for item in tlist:
        islabel = True
        try:
            item_new = item.replace('.html','')
            this_stock = item_new.split('/')[-1]  
        except:
            this_stock = item  
        flag = os.path.exists('{}\{}\zhishu\{}.csv'.format(data_repos,date,this_stock)) or \
               os.path.exists('{}\{}\stock\{}.csv'.format(data_repos,date,this_stock)) or \
               os.path.exists('{}\{}\etf\{}.csv'.format(data_repos,date,this_stock))
        this_flag = 0
        for init in sorted(dic):
            if this_stock[:5] in dic[init]:
                this_flag = init
                break
            elif this_stock[:3] in dic[init]:
                this_flag = init
                break
        if flag == False and this_flag != 0:
            the_url = 'http://hq.sinajs.cn/list=ml_{}'.format(this_stock)
            this_df = ParseStock(the_url)             
            while islabel:
                try:
                    with open('{}\{}\log.txt'.format(data_repos,date),'a') as log:
                        if this_df.shape[0]>200:
                            this_df.to_csv('{}\{}\{}\{}.csv'.format(data_repos,date,dic_os[this_flag],this_stock))   
                            print('{}_{}配置成功,已完成{}项，还有{}项,预计还需{}分钟'.format(this_stock,dic_name[init],count+1,len(tlist)-count-1,small_sleep*(len(tlist)-count-1)//60))
                            log.write('{}_{}配置成功,已完成{}项，还有{}项,预计还需{}分钟\n'.format(this_stock,dic_name[init],count+1,len(tlist)-count-1,small_sleep*(len(tlist)-count-1)//60))
                        else:
                            print('{}_{}数据过少,还有{}项,预计还需{}分钟'.format(this_stock,dic_name[init],len(tlist)-count-1,small_sleep*(len(tlist)-count-1)//60))
                            log.write('{}_{}数据过少,还有{}项,预计还需{}分钟\n'.format(this_stock,dic_name[init],len(tlist)-count-1,small_sleep*(len(tlist)-count-1)//60))
                        log.close()
                    tag.sleep(small_sleep)
                    islabel = False
                except:
                    tag.sleep(20)
        count += 1

main()
