from bs4 import BeautifulSoup
import re
import requests
import pandas as pd

# sys.setrecursionlimit(10000) # 파이썬 재귀 함수 제한 풀기
class Seach : #tag_href는 안쓰고 있다 현제 08-23
    def __init__(self, url, tag, save_name, date_tag, tag_title = None, tag_href = None, method = None):
        self.tag_title = tag_title
        self.tag_href = tag_href
        self.tag = tag
        self.url = url #self.url로 클래스 필드 변수를 공유합니다.

        self.html_parser = self.html_parsing(url) # init 내부에서 seach를 호출하여  파싱한 정보를 html_parser에 저장한다.

        self.html_select = self.html_parser.select(tag)  # 제목

        date = self.date_time(date_tag)
        self.DataFrame_file = self.seach_text(method, date)# 제목 href 날짜별 딕셔너리 형태로 저장한다.
        save_path = 'log//'
        self.save_csv(self.DataFrame_file , save_path, save_name) #정렬해서 저장한다.
        # 데이터 프레임 형식으로 만들었다. 이제 이것을 csv로 저장하고 call할때 리스트로 넘겨주자.


    # def init_option(self, save_name): # self.addional_tag는 타이틀과 href 있는 태그이다.
    #     self.html_select = self.html_parser.select(self.tag)  # 제목
        # 파싱을 하고 새로운 정보만 add하는 코드를 짜야만 한다. 20-07-11

        # self.save_print(save_path)  # 다이너리 파일을 불러와서  프린트한다.

    def html_parsing(self, url_se) :
        res = requests.get(url_se).text
        sw_hally_soup = BeautifulSoup(res, "html.parser")
        return sw_hally_soup

    def date_time(self, tag):
        date_list = []
        p = re.compile('[^-]')
        for i in self.html_parser.select(tag):
            if i.get_text() is "":
                continue
            date_list.append(int("".join(p.findall(i.get_text()))))
        date = {'날짜' : date_list}
        return date

    def seach_text(self, method, date): # pandas를 이용해 DataFrame 식으로 저장한다.
        title = []
        href = []
        if method is "get_text" :
            for unpack_url in self.html_select:
                p = re.compile('[^\t\n\r\f\v]+')
                if unpack_url.get_text() is "":
                    continue
                title.append(p.findall(unpack_url.get_text())[0])
                href.append(unpack_url.attrs['href'])
            result = {'제목': title, 'href': href}
            result.update(date)
            result_pd = pd.DataFrame(result, index=list(date.values()))
            return result_pd.sort_index(ascending=False)

        if method is "attrs":
            for unpack_url in self.html_select:
                title.append(unpack_url.attrs[self.tag_title])
                href.append(unpack_url.attrs['href'])
            result = {'제목': title, 'href': href}
            result.update(date)
            result_pd = pd.DataFrame(result, index=list(date.values()))
            return result_pd.sort_index(ascending=False) # 내림차순 정렬

        raise NameError('no method name, plz rechack method name')
        return None

    def save_csv(self, data , save_path, save_name): # 세이브 방식은 pandas
        count = 0
        p = re.compile('[^\t\n\r\f\v]+')
        # print(count, "     ", p.findall(data.iloc[0, 0])[0], '        ',
        #       p.findall(list(pd.read_csv(save_path + save_name).iloc[:, 1])[0])[0])
        # for i in list(pd.read_csv(save_path+save_name).iloc[:, 1]) :
        #     if p.findall(i[0])[0] is p.findall(data.iloc[0, 0])[0] :
        #         break
        #     else :
        #         count += 1

        data.to_csv(save_path + save_name, mode='w', encoding='utf-8-sig')

    def load_csv(self, path , name):
        data = pd.read_csv(path + name)
        return data

    """ 다이너리 형태의 (구)저장 방식 이제는 사용 안함.  이유: 자료저장에 불리함.
    def save_file(self , url_parser, save_path, save_name): # 파싱할 태그를 select로 url_parser에 던진다, savemname은 저장 장소를 받는다.
        self.url_parser = url_parser
        count = 0
        with open(save_path + save_name, 'wb') as savefile: # save_path 장소에 다이너리 형태로 파일을 저장한다.
            if self.tag_href is None :
                try :
                    for unpack_url in self.hally_sw_select:
                        pickle.dump(unpack_url.attrs[self.tag_title], savefile)
                except KeyError : # 개 병신같은 코드임 이 부분 나중에 수정하삼 공지상황을 가져오는 태그 방식이 달라서 이렇게 만듬. 08-16
                    p = re.compile('[^\t\n\r\f\v]+')
                    for unpack_url in self.hally_sw_select:
                        if unpack_url.get_text() is "":
                            continue
                        pickle.dump(''.join(p.findall(unpack_url.get_text())), savefile)

            elif self.tag_href is not None : # 이걸로 작동한다. 다이너리 형태로 저장한다. {제목 : href}
                try:
                    for unpack_url in self.hally_sw_select:
                        pickle.dump({unpack_url.attrs[self.tag_title] : unpack_url.attrs[self.tag_href]}, savefile)
                        count += 1
                except KeyError:  # 개 병신같은 코드임 이 부분 나중에 수정하삼 공지상황을 가져오는 태그 방식이 달라서 이렇게 만듬. 08-16
                    p = re.compile('[^\t\n\r\f\v]+')
                    for unpack_url in self.hally_sw_select:
                        if unpack_url.get_text() is "":
                            continue
                        pickle.dump({''.join(p.findall(unpack_url.get_text())) : unpack_url.attrs['href']}, savefile)
                        count += 1
    """
    
    """ 다이너리 형태 세이브 파일 로드 (구)방식
    def call_file(self, save_path, save_name): # 저장 장소의 파일을 프린트 해준다.
        with open(str(save_path + save_name), 'rb') as f:  # 이것은 직렬화 파일을 반환해주는 소스이다. ( 여기서는 딕셔너리 형태 {제목 :  href}
            count = 0
            obj = {}
            while True:
                try:
                    d = pickle.load(f)
                    count += 1
                except:
                    break
                obj.update(d)
            
        return obj
    """
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
    save_path = "..//log//File.bin"
    hally_sw.save_call(url_parser ,save_path)

    hally_sw.save_print(save_path) # 다이너리 파일을 불러와서  프린트한다.

