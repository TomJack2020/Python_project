# -*- coding: utf-8 -*- 
# @Time : 2021/4/3 13:37 
# @Author : Chenerping
# @File : 02.asyncio_craw.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os, time

def craw(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }
    wb_data = requests.get(url, headers=headers)
    wb_data.encoding = "utf-8"
    # 打印返回码为200即成功
    # print(wb_data)
    # 解析网页
    html = BeautifulSoup(wb_data.text, 'lxml')
    return html


def parse(html):
    titles = html.find_all('div', class_='hd')
    titles_0 = [title.find_all('span', class_="title")[0].string for title in titles]
    hrefs = [title.a['href'] for title in titles]
    # print(hrefs)
    rates = html.find_all('div', class_='star')
    rates_1 = [rate.find_all('span')[1].text for rate in rates]
    rates_3 = [rate.find_all('span')[3].text for rate in rates]
    df = pd.DataFrame(data={'Title of Movie': titles_0,
                            "Link of Movie": hrefs,
                            "Rate of Movie": rates_1,
                            "Rate of People": rates_3
                            })

    return df

urls = ["https://movie.douban.com/top250?start=" + str(n) + "&filter=" for n in range(0, 250, 25)]


start = time.time()
df_li = []
for url in urls:
    df = parse(craw(url))
    df_li.append(df)
    print(df, url)

df_all = pd.concat(df_li)

folder = r"C:\Users\Administrator\Desktop"
save_path = os.path.join(folder, 'douban.xlsx')
print('耗时：', time.time() - start)
df_all.to_excel(save_path, index=None)