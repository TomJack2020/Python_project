# -*- coding: utf-8 -*- 
# @Time : 2021/4/3 13:14 
# @Author : Chenerping
# @File : 01.craw_test.py

import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import time

# url = "https://movie.douban.com/top250"
'''
https://movie.douban.com/top250?start=0&filter=
https://movie.douban.com/top250?start=25&filter=
https://movie.douban.com/top250?start=50&filter=
多页数据把每一页的链接 做成列表
'''

start = time.time()
url = "https://movie.douban.com/top250?start=0&filter="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
}
# 注意加header 防止报错
wb_data = requests.get(url, headers=headers)
wb_data.encoding = "utf-8"
# 打印返回码为200即成功
# print(wb_data)
# 解析网页
soup = BeautifulSoup(wb_data.text, 'lxml')
# 打印解析的网页
# print(soup)

# 电影标题
# print(items.find_all('span', class_="title")[0].string)
# print(items.find_all('span', class_="title")[1].string)  # 部分影片没有第二标题

items = soup.find_all('div', class_='hd')
titles_0 = [title.find_all('span', class_="title")[0].string for title in items]
# print(titles_0)

hrefs = [title.a['href'] for title in items]
# print(hrefs)
rates = soup.find_all('div', class_='star')
rates_1 = [rate.find_all('span')[1].text for rate in rates]
rates_3 = [rate.find_all('span')[3].text for rate in rates]
# print(rates_3)

folder = r"C:\Users\Administrator\Desktop"
save_path = os.path.join(folder, 'douban.xlsx')

df = pd.DataFrame(data={'Title of Movie':titles_0,
                        "Link of Movie":hrefs,
                        "Rate of Movie":rates_1,
                        "Rate of People":rates_3
                        })

end = time.time()
print("耗时：", end - start)

print(df)
# df.to_excel(save_path,index=None)





