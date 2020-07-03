from bs4 import BeautifulSoup
import re
import urllib.request as req




class Seach :
    def __init__(self, url):
        print("완료!")
        self.url = url #self.url로 클래스 필드 변수를 공유합니다.
        self.seach(url) # init 내부에서 seach를 호출합니다.

    def seach(self, url_se) :
        res = req.urlopen(url_se).read()
        sw_hally_soup = BeautifulSoup(res, "html.parser")
        self.html_parser = sw_hally_soup


if __name__ == "__main__" :
    hally_sw = Seach("https://hlsw.hallym.ac.kr/index.php?mp=5_2")

    re_se = re.compile('\w+')

    hally_sw_select = hally_sw.html_parser.select("#bbsWrap > form:nth-child(2) > table > tbody")
    i = 1

    for unpack_url in hally_sw_select :
        for unpack2_url in unpack_url.select("a") :
            print(i, ">>>",unpack2_url.string)
            i += 1


