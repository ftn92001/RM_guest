import requests
from bs4 import BeautifulSoup
import sys


PTT_URL = 'https://www.ptt.cc'


def get_web_page(url):
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text


def get_articles(dom):
    soup = BeautifulSoup(dom, 'html5lib')

    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']

    articles = []
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        if 'SBS Running Man' in d.find('div', 'title').text:
            if d.find('a'):
                href = d.find('a')['href']
                title = d.find('a').text
                author = d.find('div', 'author').text if d.find('div', 'author') else ''
                articles.append({
                    'title': title,
                    'href': href,
                    'author': author
                })

    return articles, prev_url

def find_guest(rm_page):
    soup = BeautifulSoup(rm_page, 'html5lib')

    spans = soup.find_all('span')
    for s in spans:
      if ('來賓：' in s.text):
        print(s.text)

if __name__ == '__main__':
    current_page = get_web_page(PTT_URL + '/bbs/KR_Entertain/index.html')
    ep = int(sys.argv[1])
    if current_page:
        articles = []
        counts = []
        current_articles, prev_url = get_articles(current_page)
        while len(articles) < ep :
            articles += current_articles
            current_page = get_web_page(PTT_URL + prev_url)
            if current_articles:
                rm_page = get_web_page(PTT_URL + current_articles[0]['href'])
                print(current_articles[0]['title'])
                find_guest(rm_page)
            current_articles, prev_url = get_articles(current_page)