# _*_  coding:utf-8  _*_
# @ 功能描述：
# @ 作者：yagami_yue
# @ 版本信息：0.0.1
import sqlite3
import urllib.error
import urllib.request
import re
import xlwt
from bs4 import BeautifulSoup


def gethtml(url):
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3766.400 QQBrowser/10.6.4163.400',
    }
    request = urllib.request.Request(url, headers=head)
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        return html
    except urllib.error.URLError as e:
        if hasattr(e, "code") and hasattr(e, "reason"):
            print(e.reason)
            print(e.code)


def dealhtml(baseurl):
    alldata = []
    # 正则匹配
    pat_name = re.compile('<span class="title">(.*)</span>')
    pat_link = re.compile('<a href="(.*?)">')
    pat_img = re.compile(r'<img.*src="([\S]*\.jpg)".*>', re.S)
    pat_rate = re.compile('<span class="rating_num" property="v:average">(.*)</span>')
    pat_pnumber = re.compile(r'<span>(\d*)人评价</span>')
    pat_inp = re.compile('<span class="inq">(.*)</span>')
    # 注意加问号改为非贪心算法
    pat_content = re.compile('<p class="">(.*?)</p>', re.S)
    for i in range(0, 10):
        # 拼接url
        url = baseurl + str(i * 25)
        html = gethtml(url)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):
            data = []
            item = str(item)
            name = pat_name.findall(item)
            if len(name) == 2:
                name = name[:1]
            data.append(name[0])
            link = pat_link.findall(item)[0]
            data.append(link)
            img = pat_img.findall(item)[0]
            data.append(img)
            rate = pat_rate.findall(item)[0]
            data.append(rate)
            pnumber = pat_pnumber.findall(item)[0]
            data.append(pnumber)
            inq = pat_inp.findall(item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append(" ")
            content = pat_content.findall(item)[0]
            # 除去空格和无关字符
            content = re.sub(r'<br(\s+)?/>(\s+)?', " ", content)
            content = re.sub(r'/', " ", content)
            content = content.strip()
            data.append(content)
            # print(data)
            alldata.append(data)

    return alldata


def dbcreate(dbpath):
    sql = """
            create table movie250
            (
            id integer  primary key autoincrement,
            movie_name varchar ,
            img_link text,
            link text,
            score numeric ,
            pnumber numeric ,
            inq text,
            info text 
            )
    """
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def savedatadb(datalist, dbpath):
    dbcreate(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 3 or index == 4:
                continue
            data[index] = '"' + data[index] + '"'

        sql = """
            insert into movie250(
            movie_name,link,img_link,score,pnumber,inq,info)
            values(%s)""" % ",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    baseurl = "https://movie.douban.com/top250?start="
    datalist = dealhtml(baseurl)
    dbpath = "movie.db"
    savedatadb(datalist, dbpath)
    # excel保存数据
    # book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    # sheet = book.add_sheet("豆瓣电影top250", cell_overwrite_ok=True)
    # col = ("电影名称", "电影图片链接", "电影链接", "评分", "评论人数", "简评", "概况")
    # for i in range(0, 7):
    #     sheet.write(0, i, col[i])
    # for i in range(0, 250):
    #     data = datalist[i]
    #     for j in range(0, 7):
    #         sheet.write(i+1, j, data[j])
    # book.save("movie.xls")
