from __future__ import unicode_literals
import pandas as pd
import json
import jieba
import jieba.analyse

# 打开文件
f = pd.read_excel('./旅游景点.xlsx')
text = ''
# 拼接成整个字符转
for piece in f.iloc:
    text += str(piece['简介'])

# 分割词语
fenci_text = jieba.cut(text)

# 去除停用词
stopwords = {}.fromkeys([ line.rstrip() for line in open('stopwords.txt', encoding='utf-8') ])
final = ""
for word in fenci_text:
    if word not in stopwords.keys():
        if (word != "。" and word != "，") :
            final = final + " " + word

# 取出现概率前100
a = jieba.analyse.extract_tags(final, topK = 100, withWeight = True, allowPOS = ())
res = []
for w in a:
    mw = {'text': w[0], 'rate': w[1]}
    res.append(mw)

with open('./etw/public/mainWords.json', 'w', encoding='utf-8') as fs:
    fs.write(json.dumps(res, ensure_ascii=False, indent=4))
    fs.write('\n')
