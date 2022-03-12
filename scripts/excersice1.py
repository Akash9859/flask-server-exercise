
from sys import exc_info
from flask import jsonify, request
import json
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from bs4 import BeautifulSoup


def init(configs):
    global configs_dict
    configs_dict = configs

def exchange_rate(request_json):
    try:
        df_part1 = get_exchange_rate(request_json,'GBP')
        # return_json = {
        #     'data': df_part1,
        #     'status': 'succesful operation'
        # }
        return df_part1
    except Exception as exe:
        a,b,c =exc_info()
        print('error in line no::',c.tb_lineno)
        print(a)
        print(b)
        # return_json = {
        #     'data': '',
        #     'status': 'failed operation'
        # }
    return 'Failed Operation in exercise 1'

def get_exchange_rate(request_json,contry_name,target="EUR"):
    try:
        modified_url = request_json['url'].replace('GBP',contry_name)
        response = requests.get(request_json['url'])
        data = response.text
        tree = ET.ElementTree(ET.fromstring(data))
        root = tree.getroot()
        # ar = [elem.tag for elem in root.iter()]
        # print(ar)
        date = []        
        for val in root.iter('{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}ObsDimension'):
            val1 = val.attrib
            date.append(val1['value'])
        
        exch_rate = []
        for val in root.iter('{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}ObsValue'):
            val1 = val.attrib
            exch_rate.append(val1['value'])
        # print(len(date),len(exch_rate))
        # print(date)
        # print(exch_rate)
        df = pd.DataFrame({
            'TIME_PERIOD':date,
            'OBS_VALUE':exch_rate
        })
        df['OBS_VALUE']=pd.to_numeric(df["OBS_VALUE"])
        html_df = df.to_html()
        print(html_df)
        return html_df
    except Exception as exe:
        a,b,c =exc_info()
        print('error in line no::',c.tb_lineno)
        print(a)
        print(b)
        return c