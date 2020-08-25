import urllib.request as req
from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    , "Referer": "https://www.hallym.ac.kr/hallym_univ/sub05/cP3/sCP1.html"
}
url = requests.get("https://www.hallym.ac.kr/hallym_univ/sub05/cP3/sCP1").text
res = BeautifulSoup(url, "html.parser")
soup = res.select("#container > div > div:nth-child(5) > div.tbl-press > div > ul > li > span > span > a")

table = pd.read_html('한림대학교SW중심대학사업단__공지사항.html')
print(len(table))
failures = table[0]
print(failures.head())
failures.to_csv('name.csv', mode='w', encoding='utf-8-sig')



# date_list = []
# d = re.compile('[^-]')
# for i in res.select( "#container > div > div:nth-child(5) > div.tbl-press >\
#                                     div > ul > li > span.col.col-5.tc > span:nth-child(2)") :
#     if i.get_text() is "":
#         continue
#     date_list.append(int("".join(d.findall(i.get_text()))))
#
#
# # print(soup)
# # # p = re.compile('[^\t\n\r\f\v]+')
# # for i in soup :
# #     if i.get_text() is "" :
# #         continue
# #     print(i.get_text())
#
# title = []
# href = []
# for unpack_url in soup:
#     p = re.compile('[^\t\n\r\f\v]+')
#     if unpack_url.get_text() is "":
#         continue
#     title.append(p.findall(unpack_url.get_text())[0])
#     href.append(unpack_url.attrs['href'])
# #, 'href' : href
# d = {'제목' : title, '날짜' : date_list}
# d.update({'href' : href})
#
# parsing_file = pd.DataFrame(d)
# parsing_file.to_csv("save.csv", mode = 'w', encoding='utf-8-sig')
# data = pd.read_csv('save.csv')
# for i in list(data.get('제목'))[:8] :
#     print(i)
#






