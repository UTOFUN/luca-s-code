# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 23:23:15 2018

@author: admin
"""

import pandas
    
    
    
    
result=[]    
for index,item in enumerate(items):
    try:
        title=item.find('h3',class_='details-title').find('a')
        price=item.find('span',class_='price')
        est_monthly_payment=item.find('span',class_='EstimateCalculator-price monthly_payment')
        beds=item.find('li',class_='first_detail_cell')
        baths=item.find('li',class_='detail_cell')
        size=item.find('li',class_='last_detail_cell')
        house_type=item.find('li',class_='details_info')
        listed=item.find('li',class_='details_info details-info-flex')
        if listed:
            if 'Listed' not in listed.text:
                listed=None
        detail=[title,price,est_monthly_payment,beds,baths,size,house_type,listed]
        detail_1=[i.text.strip('\n').strip(' ') if i else None for i in detail ]
        result.append(detail_1)
    except:
        print(index)
import pandas as pd
df=pd.DataFrame(result,columns=['address','price','est_monthly_pay','beds','baths','size',
                                'house_type','list by'])