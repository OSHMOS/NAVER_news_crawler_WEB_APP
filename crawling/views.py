import csv
import time
import requests
from django.shortcuts import render, redirect
from datetime import datetime
from bs4 import BeautifulSoup
# Create your views here.


def news_scrap():
    start = time.time()

    csv_file = open('네이버 뉴스 스크랩.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['뉴스 제목', '뉴스 링크', '언론사', '날짜'])

    LIMIT = 0

    print('안녕하세요. 오스모스가 제작한 네이버 뉴스 크롤러입니다.')
    query = input('모으고 싶은 네이버 뉴스 키워드를 입력해주세요. : ')

    while True:
        url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={query}&sort=1&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:all,a:all&start={LIMIT}1'
        if 'start=4001' in url:  # 네이버는 기사를 최대 4,000건까지만 제공한다.
            break

        response = requests.get(url)
        search_page = response.text

        soup = BeautifulSoup(search_page, 'html.parser')

        news_titles = soup.select('a.news_tit')
        info_group = soup.select('div.info_group')
        for news_title, info in zip(news_titles, info_group):
            title = news_title.get_text()
            link = news_title.get('href')
            a = info.select_one('a.info.press')
            press = a.get_text()
            span = info.select('span.info')

            if len(span) > 1:
                date = span[-1].get_text().replace('.', '-').rstrip('-')
            else:
                date = span[0].get_text().replace('.', '-').rstrip('-')

            if '분 전' in date or '시간 전' in date:
                date = f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day}'
            elif '일 전' in date and int(date[0]) > 0:
                date = f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day - int(date[0])}'

            csv_writer.writerow([title, link, press, date])

        LIMIT += 1
    csv_file.close()

    end = time.time()
    print(f'현재 환경에서는 {end - start}초가 걸립니다.')
    print("'네이버 뉴스 스크랩.csv'를 윈도우는 시작에서 맥은 Finder에서 검색해주세요.")


def index(request):
    return render(request, 'crawling/index.html')


def crawling(request):
    news_scrap()
    ans = input("계속 사용을 원하시면 O를 입력해주세요. 이외의 것을 입력하시면 자동 종료됩니다. : ")
    if ans == 'O':
        news_scrap()
    else:
        print('프로그램이 종료되었습니다. 감사합니다.')
    return redirect()
