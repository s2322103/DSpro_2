import requests
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

#urlを取得
url = 'https://www.pref.mie.lg.jp/DATABOX/26804004046.htm'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')


#webサイトからデータを取得
td_list = soup.find_all('td', align='right')

element_36 = td_list[36]
element_45 = td_list[45]
element_54 = td_list[54]
element_63 = td_list[63]

print(element_36)
print(element_45)
print(element_54)
print(element_63)


#element_36のデータ型を確認
type(element_36)


#データベースの作成・接続
dbname = 'sleep.db'
database_path = '/content/sleep.db'
conn = sqlite3.connect(database_path + dbname)


#テーブルを作成
cur = conn.cursor()
sql_create_table_sleeptime = ('CREATE TABLE sleeptime(day TEXT, average TEXT, myself REAL)')
cur.execute(sql_create_table_sleeptime)


#テーブルに挿入
sql_insert_many = "INSERT INTO sleeptime VALUES (?, ?, ?)"

sleeptime_list = [
    ('whole week', element_36.text, 7.00),
    ('weekdays', element_45.text, 7.20),
    ('saturday', element_54.text, 6.30),
    ('sunday', element_63.text, 6.30)
]

cur.executemany(sql_insert_many, sleeptime_list)


#テーブルを表示
cur.execute('SELECT * FROM sleeptime')
data = cur.fetchall()

conn.close()

print(data)


#データを可視化
days, average_time_text, myself_time = zip(*data)
average_time = [float(average_time) for average_time in average_time_text]

plt.bar(days, average_time, label='average', color='blue')
plt.bar(days, myself_time, label='myself', color='orange', alpha=0.7)

plt.title('Average sleeptime')
plt.xlabel('Days')
plt.ylabel('Time')

plt.legend()

plt.show()