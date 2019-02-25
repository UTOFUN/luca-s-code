# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:39:12 2018

@author: admin
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from proxybroker import Broker
import asyncio
from fake_useragent import UserAgent
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.command import Command


def getProxy(count):
    proxyList = []
    async def show(proxies):
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            proxyList.append('{}:{}'.format(proxy.host, proxy.port))
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(
        broker.find(types=['HTTP'], limit=count),
        show(proxies))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)
    proxy_type='free'

    return proxyList,proxy_type



def initializechrome(proxy=None,headless = False):
    # set the chrome not to accept picture
    user_agent=['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16']

    chrome_options = webdriver.ChromeOptions()
    prefs = {#"profile.managed_default_content_settings.images":2,
             #'download.default_directory': filepath,
             }
    chrome_options.add_argument('blink-settings=imagesEnabled=false') # headless 模式下也生效
    chrome_options.add_argument("--start-maximized")
    if proxy is not None:
        # free proxy
        chrome_options.add_argument('--proxy-server=%s' % proxy)
        
    chrome_options.add_experimental_option("prefs",prefs)
    if headless:
        # see https://stackoverflow.com/questions/46920243/how-to-configure-chromedriver-to-initiate-chrome-browser-in-headless-mode-throug
        
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--log-level=3");
        chrome_options.add_argument("--silent")
    #chrome_options.add_argument('--user-agent="%s"'%UserAgent().random)
    chrome_options.add_argument('--user-agent="%s"'%random.sample(user_agent,1)[0])
    global browser
    browser = webdriver.Chrome(r'C:\Users\admin\AppData\Local\Google\Chrome\Application\chromedriver.exe',
                               chrome_options=chrome_options)
    global wait
    wait=WebDriverWait(browser,7)
    
    
    

    


if __name__ == '__main__':
    df = pd.read_excel(r'C:\Users\admin\Downloads\result.xlsx',encoding='utf-8') 
    n=df.finished[0]
    proxyList,proxy_type = getProxy(100)
    print(proxyList)
    user_agent=['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16']
    for proxy_i in proxyList: 
        
        # get cookie
        try:
            initializechrome(proxy_i,True)
            browser.execute(Command.SET_TIMEOUTS, {
                            'ms': float(15 * 1000),
                            'type': 'page load'})
            browser.get('https://www.realtor.com/')
        except KeyboardInterrupt as e:
            break
        except TimeoutException as e:
            try:
                browser.get('https://www.realtor.com/')
            except KeyboardInterrupt as e:
                break
            except TimeoutException as e: 
                browser.quit()
                continue
            
        if 'block' in browser.current_url:
            print('ip blocked')
            browser.quit()
            continue   
        cookie_list=[]
        if len(browser.get_cookies())>0:
            for i in browser.get_cookies():
                cookie_list.append('{0}={1}'.format(i['name'],i['value']))

            cookie_string='; '.join(cookie_list)
            print('cookie fetched')
            browser.quit()
        else:
            print('no internet')
            browser.quit()
            continue
        

        # initialize cookies headers
        proxy={'http':'http://'+proxy_i,
               'https':'https://'+proxy_i}
        
        HEADERS = {
            #'User-Agent':UserAgent().random,
            'User-Agent':random.sample(user_agent,1)[0],
            #'cookie': cookie_string,
            'cookie': cookie_string,
            'Content-Type':'application/json',
            'pragma':'no-cache',
            'upgrade-insecure-requests':'1',
            'cache-control':'no-cache',
            'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
            'accept-encoding':'gzip, deflate, br'}  
        while n<=df.shape[0]-1:
            try:
                time.sleep(0.5)
                address=df.iloc[n]['key']
                
                # get detail page address
                request_url = r'https://www.realtor.com/api/v1/geo-landing/parser/suggest/?input={}&area_types=address&area_types=neighborhood&area_types=city&area_types=county&area_types=postal_code&area_types=street&area_types=building&area_types=school&area_types=building&area_types=school&area_types=building&limit=10&includeState=false'
                request_url_temp = request_url.format(address)
                response = requests.get(request_url_temp,headers=HEADERS,proxies=proxy)
                search_response = response.json()['result'][0]
                detail_url_part1 = r'https://www.realtor.com/realestateandhomes-detail/'
                try:
                    house_url_id='M'+search_response['mpr_id'][:5]+'-'+search_response['mpr_id'][5:]
                except:
                    n+=1
                    continue
                detail_url_part2='_'.join([search_response['line'],search_response['city'],
                                           search_response['state_code'],search_response['postal_code'],house_url_id])
                detail_url_part2 = detail_url_part2.replace(' ','-')
                detail_url = detail_url_part1+detail_url_part2   
                response = requests.get(detail_url,headers=HEADERS,proxies=proxy)
                
                
                # check detail page response content
                if 'Blocked IP Address' in response.text:
                    print('ip blocked')
                if 'Property Price' in response.text:
                    text=''
                    soup = BeautifulSoup(response.text, 'html.parser')
                    rows = soup.find_all("div", class_="listing-subsection listing-subsection-price")[0].find_all('tr')
                    for row in rows:
                        cols = row.find_all('td')
                        for col in cols:
                            text+=col.text.strip()+'\n'
                        text+='------------\n'
                    df.loc[n,'price history new']=text
                    print(n)
                    n+=1
                else:
                    df.loc[n,'price history new']=''
                    n+=1
                    break
                
                if n%10 ==0:
                    print('{} records complete'.format(n))
                    
                if (n-49)%50 ==0:
                    df['finished']=n
                    df.to_excel(r'C:\Users\admin\Downloads\result.xlsx',encoding='utf-8',index=False)
                    print('table stored')
                    
                    
                    
            except Exception as e:
                print(e)
                break

    df.to_excel(r'C:\Users\admin\Downloads\result.xlsx',encoding='utf-8',index=False)
    
    

        
        
        
        
        
        
        
        
        
        







