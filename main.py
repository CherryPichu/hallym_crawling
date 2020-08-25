import sys
from bs4 import BeautifulSoup
from lib.hallym_view import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QUrl
from PyQt5.QtWidgets import *
from PyQt5 import uic
from lib.Seach import Seach
from PyQt5 import QtCore
import webbrowser
import pandas as pd

import re
import datetime

#사이트 태그만 바뀌어도 크롤링이 안되는 문제점이 있다 이 점을 나중에 수정해보자
class Main(QMainWindow, Ui_MainWindow): # form_class
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # #container > div > div:nth-child(5) > div.tbl-press > div > ul
        self.hally_sw = Seach(url = "https://hlsw.hallym.ac.kr/index.php?mp=5_2",
                              tag = "#bbsWrap > form:nth-child(2) > table > tbody > tr > td.tit > a", save_name = "File_SW.csv", tag_title ="title",
                              tag_href = "href", method = "attrs", date_tag = "#bbsWrap > form:nth-child(2) > table > tbody > tr > td:nth-child(4)")
        self.load_SW = pd.read_csv("log//File_SW.csv")

        self.hally_notic = Seach(url = "https://www.hallym.ac.kr/hallym_univ/sub05/cP3/sCP1",
                                tag = "#container > div > div:nth-child(5) > div.tbl-press > div > ul > li > span > span > a",
                                 save_name = "File_notic.csv", tag_title = "a" ,tag_href = 'href', method = 'get_text'
                                 , date_tag = "#container > div > div:nth-child(5) > div.tbl-press >\
                                    div > ul > li > span.col.col-5.tc > span:nth-child(2)")

        self.load_notice = pd.read_csv("log//File_notic.csv") # 다이너리 형식의 프린터들 반환
        self.load_SW.rank(ascending=True)

        self.init()

        self.pushButton.clicked.connect(QtCore.QCoreApplication.instance().quit) # 종료버튼


    def link_button_init(self, url, option):


        #반복문으로 만들면 왜인지 안됨.
        eval(str(option)+str(1)).clicked.connect(lambda : webbrowser.open_new(url[0]))
        eval(str(option) + str(2)).clicked.connect(lambda: webbrowser.open_new(url[1]))
        eval(str(option) + str(3)).clicked.connect(lambda: webbrowser.open_new(url[2]))
        eval(str(option) + str(4)).clicked.connect(lambda: webbrowser.open_new(url[3]))
        eval(str(option) + str(5)).clicked.connect(lambda: webbrowser.open_new(url[4]))
        eval(str(option) + str(6)).clicked.connect(lambda: webbrowser.open_new(url[5]))
        eval(str(option) + str(7)).clicked.connect(lambda: webbrowser.open_new(url[6]))
        eval(str(option) + str(8)).clicked.connect(lambda: webbrowser.open_new(url[7]))
        # 아래 코드가 안됨 나중에 분석히기.
        # self.link_list = []
        # for i in range(1, 9):
        #     self.link_list.append(lambda : webbrowser.open_new(url[i-1]))
        # for i in range(1,9) :
        #     d = option + str(i)
        #     eval(d).clicked.connect(lambda : webbrowser.open_new(url[i-1]))

    def init(self):
        self.print_view_webText(data = self.load_SW, option="self.web2_text_")
        self.print_view_webText(data = self.load_notice, option="self.web_text_")
        # 전처리
        url_link = []
        for i in list(self.load_SW.get('href')) :
            url_link.append('https://hlsw.hallym.ac.kr/' + str(i)) #SW 중심대학 링크는 https 링크로 안되어 있다.
        #버튼 이벤트
        self.link_button_init(url = url_link, option="self.Web_Button") # url 리스트를 던져줬네
        url_link2 = list(self.load_notice.get('href'))
        self.link_button_init(url = url_link2, option="self.Web2_Button")


    def print_view_webText(self, data, option):
        count = 0
        for i in list(data.get('제목'))[:8] :
            count += 1
            d = eval(option+str(count))
            d.setText(i) # 자동완성 불가능 eval로 문자열 만든 것은

        # count=0
        # for i in call_list[:8] :
        #     count += 1
        #     d = eval(str("self.web2_text_")+str(count))
        #     d.setText(i)


if __name__ == "__main__" :

    app = QApplication(sys.argv)
    you_viewer_main = Main()
    you_viewer_main.show()
    app.exec_()




