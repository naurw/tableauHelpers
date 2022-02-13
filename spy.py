#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 22:54:48 2022

@author: William
"""

import pandas as pd 
import requests 
import os 
import json

apiKey = 'insert_here'
endpoint = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=SPY&interval=5min&apikey=insert_here'
r = requests.get(endpoint)
status = r.status_code 
if status == 200: 
    print('Successful request. Status - {}'.format(status))
    spyJson = r.json() 
    print(spyJson)
else:
    print(f"Unsuccessful S3 get_object response. Status - {status}")
    

path = os.getcwd()
download = path + '/Desktop/spy02_12_22.json'

with open(download, 'w') as f: 
    json.dump(spyJson, f, indent = 4)
    
with open(download, 'r') as f: 
    csv = pd.DataFrame(json.load(f))
    csv.to_csv('/Users/William/Desktop/spy02_12_22.csv', index = None)


    

    
    