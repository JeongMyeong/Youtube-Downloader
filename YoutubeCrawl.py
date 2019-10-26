import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from collections import OrderedDict
from itertools import repeat
from urllib import parse
# from pytube import YouTube # !pip install pytube
import pytube
class Youtube:
    def __init__(self):
        pass
    def search(self, word):
        target_url = 'https://www.youtube.com/results?search_query={}'.format(parse.quote(word))
        html = urllib.request.urlopen(target_url).read()
        soup = BeautifulSoup(html, 'html.parser')
        soup_tmp = soup.findAll('h3')
        href_title_dic = dict()
        for i in soup_tmp:
            tmp = i.find('a', {'rel': 'spf-prefetch'})
            # print(tmp['class'])
            if tmp != None and len(tmp['class'])==5:
                href_title_dic[tmp.text] = tmp['href']
        return href_title_dic


if __name__ == '__main__':
    # yt=pytube.YouTube('https://www.youtube.com/watch?v=7GBINtXaook')
    a = Youtube()
    # print(a.search('이석현'))
    games = ['이석현', '킴성태', '해물파전', '배그', '배틀그라운드','뜨뜨뜨뜨','인피쉰', '웅플', '개리형','개소주', '김명운TV']
    musics = ['노래','아이유', '빅뱅', '빈지노','비와이','발라드', '뮤직비디오', '볼빨간사춘기', '여자친구', '라붐', '레드벨벳']
    ITs = ['잇섭','엠알','라이브렉스','언더케이지', '서울리안','티비오미닛','아날로그미','이퓨 아이폰', '아이폰 리뷰', '갤럭시 리뷰']
    movie_reviews = ['홍시네마','콜라냥','찬스무비', '리뷰엉이',  '맛있는 영화', '영리남', '킬타','떠번의 영화소개','소개 해주는 남자', '지무비']
    # games=['오버워치', '오버워치 롤큐', '리그오브레전드 롤큐', '메이플스토리', '정글러', '원딜러', '서포터', '미드라이너', '탑라이너','탑신병자','롤 매드무비']
    # musics =['최신가요', '래퍼 노래', '인기가요', '쇼미더머니' ,'신나는노래', '뮤비', '걸그룹', '듀엣', '커버곡', 'ost 노래', '노래 직캠']
    # ITs = ['오만상사',  '인기', '아이패드' ,'갤럭시태블릿' ,'타블릿','cpu추천', '그래픽카드','키보드 추천', '마우스 추천', '블루투스 이어폰', '블루투스 마우스']
    # movie_reviews = ['메기무비 영화리뷰', '결말 포함 영화 리뷰','아무튼 영화 리뷰', '신의 한수 영화 리뷰', '겨울왕국 영화 리뷰', '영화 리뷰 결말', '해외 영화 리뷰', '평점 높은 영화','반전 영화', '로맨스 영화']
    subjects = [games, musics, ITs, movie_reviews]

    url = []
    label=[]

    for idx, subject in enumerate(subjects):
        for keyword in subject:
            urls = a.search(keyword).values()
            for i in list(urls):
                url.append(i)
                label.append(idx+1)
        print(len(url))

    df = pd.DataFrame({"url":url, "subject":label})
    df.drop_duplicates(inplace=True)
    df.to_csv('url_label1.csv',encoding='utf-8',index=False)


##### Crwaling Description and Title
    # df = pd.read_csv('url_label.csv', encoding='utf-8')
    # urls = list(df['url'])
    # title = []
    # description = []
    # print("총 {} 개".format(len(urls)))
    # for idx, url in enumerate(urls):
    #     if idx%10==0:
    #         print("{} 진행중".format(idx))
    #     try:
    #         yt=YouTube(url)
    #         title.append(yt.title)
    #         description.append(yt.description)
    #     except:
    #         title.append('LIVE')
    #         description.append('LIVE')
    # df['title'] = title
    # df['description'] = description
    # df.to_csv('url_title_description', encoding='utf-8', index=False)
    # df = pd.read_csv('url_title_description.csv', encoding='utf-8')
    # df.to_csv('url_title_description.csv', encoding='cp949', index=False)
    # print(df['title'])
