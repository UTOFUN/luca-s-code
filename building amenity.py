# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 10:34:56 2018

@author: admin
"""
import pandas as pd
from nltk.corpus import wordnet as wn
import wikipedia as wk



df=pd.read_csv(r'C:\Users\admin\Desktop\building feature.csv')

'''
Bike Room
Parking Available
Storage Available
Virtual Doorman
Balcony
Deck
Roof Deck
Terrace
Doorman
Live-in Super
Elevator

Pets Allowed

Washer/Dryer In-Unit
Garage Parking
Gym
Laundry in Building
Central Air Conditioning
Dishwasher
Storage Available
Balcony
'''



# Building Amenity




# OUTDOOR SPACE






















columns=['intercom','doorman','superintendent','concierge','elevator','fios',
         'basement','pets allowed','gym','sport court','parking available',
         'patio','roof deck','cold storage','storage space',
         'pool','walk-up','children playroom','fireplace','garden',
         'washer/dryer in unit','laundary room','package room',
         'central air contioning','balcony','lobby','bike storage'

         ]

dict_={i:0 for i in columns}






def foo(string,feature_dict):
    features = feature_dict.copy()
    for i in string.split('\n'):
        if 'intercom' or 'virtual doorman' in i:
            features['intercom']+=1
        if 'virtual doorman' not in i and ('doorman' in i or 'super' in i or 'concierge' in i):
            features['doorman']+=1
        
        if 'super' in i:
            features['superintendent']+=1
        
        if 'bike' in i or 'bicycle' in i:
            features['bike storage']+=1
        
        if 'concierge' in i:
            features['concierge']+=1
        
            
        if 'elevator' in i:
            features['elevator']=+1
        if 'fios' in i:
            features['fios']+=1
        if re.search('(?<!no )basement',i):
            features['basement']+=1
        if 'not pet' not in i and 'no pet' not in i and ('pet' in i or 'dog' in i or 'cat' in i or 'no pit bull' in i):
            features['pets allowed']+=1
        if 'gym' in i or 'fitness' in i or 'yoga' in i or 'exercise' in i or 'pilate' in i:
            features['gym']+=1
        if re.search('court(!=s?yard)',i): # basketball court, tennis court
            features['sport court']+=1
        
        if 'parking' in i or 'garage' in i:
            features['parking available']+=1
        
        #    if 'patio' in i or re.search('((roof.?top)?(roof ?deck)?)+',i) or 'garden' in i or 'yard' in i or 'terrace' in i or 'porch' in i:
        #        features[10]=1
        
        if 'patio' in i or 'terrace' in i and 'roof' not in i:
            features['patio'] +=1
        
        if 'roof' in i:
            features['roof deck']+=1
        
        if 'storage' in i:
            if 'cold' in i:
                features['cold storage']+=1
            elif 'bike' in i or 'bicycle' in i:
                pass
            else:
                features['storage space']+=1
        
        if 'pool' in i:
            features['pool']+=1
        
        if 'walk' in i and 'up' in i:
            features['walk-up']+=1
        
        if 'children' in i and 'play' in i:
            features['children playroom']+=1
        
        if 'fireplace' in i:
            features['fireplace']+=1
            
        
            
        if 'garden' in i or 'yard' in i:
            features['garden']+=1
        
        if 'in' in i and ('unit' in i or 'room' in i or 'apartment' in i or 'home' in i) \
        and ('washer/dryer' in i or 'w/d' in i or 'laundary' in i):
            features['washer/dryer in unit']+=1
            
        if 'laundary' in i:
            features['laundary room']+=1
        #    if 'community' in i or 'recreation' in i or 'entertain' in i or 'lounge' in i \
        #    or re.search('(party|media|game|play|club|billard|cinema|golf|sitting|screening|karaoke|ping pong|theater|music).*room',i):
        #        features[12]=1
        
        #    if 'meeting' in i or 'confrence' in i or 'business' in i or 'conference' in i or 'board room' in i:
        #        features[13]=1
        if 'package' in i or 'mail' in i:
            features['package room']+=1
        
        if re.search(r'central (air|a.?c)',i):
            features['central air contioning']+=1
        if 'balcony' in i:
            features['balcony']+=1
        if 'lobby' in i or 'parlor' in i or 'reception' in i:
            features['lobby']+=1
    return features
    


import json
import requests
import csv
import time

def get_building_info(houseNumber, street, zipcode):
    GEO_CLIENT_ADDRESS_QUREY_URL = 'https://api.cityofnewyork.us/geoclient/v1/address.json?houseNumber={0}&street={1}&zip={2}&app_id={3}&app_key={4}'

    GEOCLIENT_APPID = '35348ee9'
    GEOCLIENT_APPKEY = '874bc0a8aaafe29bbe84abaeb78fd57d'


    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36',
        'Content-Type': 'application/json',
    }
    url = GEO_CLIENT_ADDRESS_QUREY_URL.format(houseNumber,
                                              street,
                                              zipcode,
                                              GEOCLIENT_APPID,
                                              GEOCLIENT_APPKEY)
    try:
        response = requests.get(url, headers=HEADERS)
        bin_=response.json()['address']['buildingIdentificationNumber']
        return bin_
    except:
        return None
    
    
    



Building=pd.read_excel(r'C:\Users\admin\Downloads\Buidling_Features.xlsx')

BIN=Building.apply(lambda row:get_building_info(row.Street_NUM,row.Street,row.Zipcode),axis=1)

Building['bin']=BIN_

Building.to_excel(r'C:\Users\admin\Downloads\Buidling_Features.xlsx',index=False)

g=Building.groupby('bin')


Building = Building.fillna('') # for the convinience of string operation

for i in range(1,6):
    Building['Bldg_Feature'+str(i)] = Building['Bldg_Feature'+str(i)].astype('str')

def apply_func(row):
    string=''
    for i in range(1,6):
        s=row['Bldg_Feature'+str(i)].lower()
        if s!='' and 'zoned' not in s and 'far' not in s and 'f.a.r.':
            string+= s+'\n'
        
        if 'time' in row['Doorman_Type']:
            string+=row['Doorman_Type']+'doorman\n'
        if row['Garage']=='Y':
            string+='garage\n'
        if row['Heat']!='':
            string+='heat\n'
        if row['Pet_Type']!='':
            string+='Pet Allowed\n'
        
        if row['B_Pet']:#?????
            pass
        if row['Pied_A_Terrace']=='Y':
            string+='Pied_A_Terrace\n'
        if row['Parking_Type']!='' and row['Parking_Type']!='None':
            string+='Parking Available\n'
        if row['Mail_Delivery']=='Y':
            string+='Mail_Delivery'
                
    return string

features=Building.apply(lambda row:apply_func(row),axis=1)

Building['features']=features

# doorman type




def groupby_func(df):
    string=''
    for i in range(df.shape[0]):
        s=df.iloc[i]['features']
        if s!='':
            string+=s
    return string


Building_g=Building.groupby('bin').apply(lambda df:groupby_func(df))

features=[]
for i in range(len(Building_g)):
    features.extend(Building_g[i].split('\n'))

features=pd.Series(features)
features_stat = features.value_counts().reset_index()
    

result = 






























