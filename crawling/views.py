import csv
import requests
from django.shortcuts import render, redirect
from datetime import datetime
from bs4 import BeautifulSoup
from .forms import QueryForm
from django.http import HttpResponse
# Create your views here.


def index(request):
    query = QueryForm()
    return render(request, 'crawling/index.html', {'query': query})


def crawling(request):
    if request.method == 'POST':
        query = request.POST['query']
        if len(query) > 0:

            LIMIT = 0

            csv_file = open('네이버 뉴스 스크랩.csv', 'w')
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['뉴스 제목', '뉴스 링크', '언론사', '날짜'])

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
                        date = span[-1].get_text().replace('.',
                                                           '-').rstrip('-')
                    else:
                        date = span[0].get_text().replace('.', '-').rstrip('-')

                    if '분 전' in date or '시간 전' in date:
                        date = f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day}'
                    elif '일 전' in date and int(date[0]) > 0:
                        date = f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day - int(date[0])}'

                    csv_writer.writerow([title, link, press, date])

                LIMIT += 1
            return render(request, 'crawling/greeting.html')
        else:
            query = QueryForm()
            alert = '검색 키워드는 한 글자 이상이어야만 합니다.'
            return render(request, 'crawling/index.html', {'alert': alert})


def export(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="네이버 뉴스 스크랩.csv"'},
    )

    writer = csv.writer(response)
    csv_file = open('네이버 뉴스 스크랩.csv', 'r')
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        writer.writerow(line)
    return response


def greeting(request):
    return render(request, 'crawling/greeting.html')
