# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 10:42:57 2018

@author: admin
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
    
columns = ['name','region','cell phone','wechat','company','licence number','brif description','detail description',]
dictionary = {i:'' for i in columns}
main_page = requests.get('https://www.meifang8.com/house_agent/')
soup = BeautifulSoup(main_page.text,'html.parser')
items = soup.find_all('div',class_='BrokerItem')
data=[]
for item in items:
    try:
        dictionary_copy=dictionary.copy()
        detail=item.find_all('span')
        
        dictionary_copy['region']=detail[2].text
        link=item.find('a')['href']
        agent_page=requests.get(link)
        agent_page_soup = BeautifulSoup(agent_page.text,'html.parser')
        detail=agent_page_soup.find('div',class_='CenterGrbox').find_all('li')
        dictionary_copy['name']=detail[0].text
        dictionary_copy['brif description']= detail[1].attrs['title']
        dictionary_copy['company']=detail[3].attrs['title']
        if '证件号：' in detail[-1].text:
            dictionary_copy['licence number']=detail[-1].text[4:]  
        if '微信：' in detail[5].text:
            dictionary_copy['wechat']=detail[5].text[3:]
        if '手机：' in detail[4].text:
            dictionary_copy['cell phone'] = detail[4].text[3:]  
        dictionary_copy['detail description'] = agent_page_soup.find('div','jrForm').find('span').text    
        data.append(dictionary_copy)
    except:
        print(item.text)
    
df =pd.DataFrame(data)