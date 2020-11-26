# _*_  coding:utf-8  _*_
# @ 时间    : 2020/8/6 2:09
# @ 文件名    : 1.py
# @ 功能描述：
# @ 作者：yagami_yue
# @ 版本信息：0.0.1
from wordcloud import WordCloud
import sqlite3
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
import jieba

conn = sqlite3.connect("movie.db")
cursor = conn.cursor()
sql = 'select inq from movie250'
data = cursor.execute(sql)
text = ''
for item in data:
    text += item[0]
cursor.close()
conn.close()
cut = jieba.cut(text)
words = ' '.join(cut)
img = Image.open("static/assets/img/1.jpg")
img_array = np.array(img)
wc = WordCloud(
    background_color="white",
    mask=img_array,
    font_path="simhei.ttf"  # 默认C:\windows\Fonts
)
wc.generate_from_text(words)

fig = plt.figure(1)
plt.imshow(wc)
plt.axis("off")  # 是否显示坐标轴
plt.savefig("static/assets/img/word2.jpg", dpi=600)