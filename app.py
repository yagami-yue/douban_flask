import sqlite3


import jieba
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/movie')
def movie():
    movies = []
    conn = sqlite3.connect('movie.db')
    cursor = conn.cursor()
    sql = "select * from movie250"
    data = cursor.execute(sql)
    for item in data:
        movies.append(item)
    cursor.close()
    conn.close()

    return render_template("movie.html", movies=movies)

@app.route('/team')
def team():
    return render_template("team.html")

@app.route('/word')
def word():
    return render_template("word.html")

@app.route('/rate')
def rate():
    score = []  # 评分
    score_number = []  # 评分数目
    conn = sqlite3.connect("movie.db")
    cursor = conn.cursor()
    sql = "select score,count(score) from movie250 group by score"
    data = cursor.execute(sql)
    for item in data:
        score.append(item[0])
        score_number.append(item[1])
    cursor.close()
    conn.close()
    return render_template("rate.html", score=score, num=score_number)

@app.route('/home')
def home():
    return index()


if __name__ == '__main__':
    app.run()
