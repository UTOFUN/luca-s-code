# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 18:50:42 2018

@author: admin
"""
import mysql.connector    
from dateutil.relativedelta import relativedelta 
import pandas as pd 
import datetime
import gc

# transform date to the first day of the month
def to_year_month(date):
    return(datetime.datetime(date.year,date.month,1))

        
def len2(file,df,fill):
    merge = pd.concat([df,fill],ignore_index = True) # fill p_id is easily removed
    merge_p = merge.pivot('property_id','doc_date','document_amount')
    merge_p = merge_p[merge_p.index!='None']


#两两配对    
def repeat(df_hier_index,p_id):    
    gc.disable()
    result = []
    append = result.append
    for pid in p_id:
        sub = df_hier_index[pid]
        index = sub.index
        for i in range(sub.shape[0] - 1):
            # 两两配对
            for slide in range(3):   
                # 滑动2个
                time1 = index[i] - relativedelta(months = slide)
                time2 = index[i+1] - relativedelta(months = slide) 
                append({'property_id' : pid,
                    time1 : sub[index[i]],
                    time2 : sub[index[i+1]]})
    gc.enable() 
    return(result)
        
user='luca'
password='Utofunluca'
host='mysql-utofun-housemining.cmf6rynp1q2h.us-east-1.rds.amazonaws.com'  
conn=mysql.connector.connect(host=host,user=user,passwd=password,charset="utf8")
cursor=conn.cursor() 
   
query='''
set @p = (SELECT polygon FROM property.boundary
where neighborhood_name = 'Long Island City');
select l.property_id,m.doc_date,m.document_amount from closing.legals l,closing.master m
where m.document_amount>50000
and m.doc_date>'1995-1-1'
and m.multiple_units = 0
and l.document_id=m.document_id;
'''

cursor.execute(query)
df=pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
df = df.drop_duplicates(df.columns[:2])
df = df.dropna()


#创造前两个月,同时保证月份连续
sort_date = df.doc_date.sort_values()
min_date = to_year_month(sort_date.iloc[0])
max_date = to_year_month(sort_date.iloc[-1])

temp = datetime.datetime(min_date.year+1,1,1)
month_delta1 = (temp - min_date).days//30
month_delta2 = (max_date.year-temp.year)*12 + max_date.month-temp.month
month_delta = month_delta1 + month_delta2
date_range = [min_date + relativedelta(months = i) for i in range(-2,month_delta+1)]


# transform the date
df.doc_date=df.doc_date.map(lambda x:to_year_month(x))



# delete pid which only has one transaction
group_len = df[['property_id','doc_date']].groupby('property_id').count()
group_len = group_len.sort_values('doc_date',ascending=False)
# become series
group_len = group_len['doc_date']
g_index = group_len[group_len==1].index
len_boolean = df.property_id.map(lambda x:False if x in g_index else True)
df = df[len_boolean]

# delete invalid pid
not_none_boolean = df.property_id.map(lambda x:False if 'None' in x else True)
df = df[not_none_boolean]
for i in ['4000000','2000000','3000000','1000000']:
    df = df[df.property_id != i]


# make look up time O(1)
df = df.sort_values(['property_id','doc_date'])
df_hier_index = df.set_index(['property_id','doc_date'])['document_amount']


p_id = set(df.property_id)
result = repeat(df_hier_index,p_id)


df_fill = pd.DataFrame(result,columns=['property_id']+date_range)
fill_column = df_fill.columns.tolist()[1:]
fill_column = [str(i)[:7] for i in fill_column]
df_fill.columns = ['property_id'] + fill_column
df_fill.to_csv(r'D:\case shiller data\wide-format.csv',index=False)







'''

#row = merge_wide.iloc[0].values.tolist()



df_repeat = df_repeat.columns.tolist()    
        
f=open(r'D:\case shiller data\wide-format.csv','w',encoding='utf-8')


#f.write('property_id,')
f.write(','.join(wide_column)+'\n')

for i in range(df_repeat.shape[0]):
    #name=df_repeat.iloc[i].name
    row_ori=list(df_repeat.iloc[i].values)
    row = str(row_ori)[1:-1]
    row = row.replace('nan','')
    row = row.replace(' ','')
    f.write(row+'\n')
    for i in range(1,3):
        row_ori.pop(1)
        row = str(row_ori)[1:-1]
        row = row.replace('nan','')
        row = row.replace(' ','')
        f.write(row+','*i+'\n')
f.close()
'''