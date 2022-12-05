from __future__ import unicode_literals
import pandas as pd
import json


f = pd.read_excel('./旅游景点.xlsx')

data = []
for i in range(f.shape[0]):
    piece = f.iloc[i]
    d = {}
    d['id'] = i + 1
    d['city'] = str(piece['城市'])
    d['name'] = str(piece['名称'])
    d['level'] = str(piece['星级'])
    d['score'] = float(piece['评分'])
    d['price'] = float(piece['价格'])
    d['sales'] = int(piece['销量'])
    d['divisions'] = str(piece['省/市/区']).replace('·', '/')
    d['coordinate'] = {'lat': float(str(piece['坐标']).split(',')[1]),'lng': float(str(piece['坐标']).split(',')[0])}
    d['introduction'] = str(piece['简介'])
    d['free'] = bool(piece['是否免费'])
    d['address'] = str(piece['具体地址'])
    data.append(d)

with open('./etw/public/旅游景点.json', 'w', encoding='utf-8') as fs:
    fs.write(json.dumps(data, ensure_ascii=False, indent=4))
    fs.write('\n')
