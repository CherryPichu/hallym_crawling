from bs4 import BeautifulSoup
import re
import pickle
import urllib.request as req
import sys
sys.setrecursionlimit(10000) # 파이썬 재귀 함수 제한 풀기




class Seach :
    def __init__(self, url):
        print("완료!")
        self.url = url #self.url로 클래스 필드 변수를 공유합니다.
        self.seach(url) # init 내부에서 seach를 호출합니다.

    def seach(self, url_se) :
        res = req.urlopen(url_se).read()
        sw_hally_soup = BeautifulSoup(res, "html.parser")
        self.html_parser = sw_hally_soup

    def save_call(self , url_parser, savename): # 파싱할 태그를 select로 url_parser에 던진다, savemname은 저장 장소를 받는다.
        self.url_parser = url_parser

        with open(savename, 'wb') as savefile: # savename 장소에 다이너리 형태로 파일을 저장한다.

            for unpack_url in hally_sw_select:
                for unpack2_url in unpack_url.select("a") :
                    pickle.dump(unpack2_url.string, savefile)

    def save_print(self, savename): # 저장 장소의 파일을 프린트 해준다.
        with open(savename, 'rb') as f:  # 이것은 직렬화 파일을 리스트로 반환해주는 소스이다.
            count = 0
            obj = []
            while True:
                try:
                    d = pickle.load(f)
                    count += 1
                except:
                    break
                obj.append(d)

        for i in obj: # 리스트의 이터럴 속성을 이용해서 프린트 해보자
            print(i)


if __name__ == "__main__" :
    hally_sw = Seach("https://hlsw.hallym.ac.kr/index.php?mp=5_2")

    re_se = re.compile('\w+')

    #url 피싱 클래스 접근
    hally_sw_select = hally_sw.html_parser.select("#bbsWrap > form:nth-child(2) > table > tbody")
    i = 1

    # 파싱을 할 url 태그와 저장할 장소를 함수를 이용해서 간단하게 처리하게 만들었다.
    # 하지만 이 구조는 매번 접속해야하는 문제가 있다.
    # 파싱을 하고 새로운 정보만 add하는 코드를 짜야만 한다. 20-07-11
    url_parser = "#bbsWrap > form:nth-child(2) > table > tbody"
    savename = "C:/Users/uskaw/Desktop/File.bin"
    hally_sw.save_call(url_parser ,savename)

    hally_sw.save_print(savename) # 다이너리 파일을 불러와서  프린트한다.




