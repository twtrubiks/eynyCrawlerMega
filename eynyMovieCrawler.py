import os
import re

import requests
from bs4 import BeautifulSoup

targetURL = 'http://www.eyny.com/forum-205-1.html'
fileName = 'eyny-Movie-Mage.txt'


def pattern_mega_google(text):
    patterns = [
        'mega', 'mg', 'mu', 'ＭＥＧＡ', 'ＭＥ', 'ＭＵ',
        'ｍｅ', 'ｍｕ', 'ｍｅｇａ', 'GD', 'MG', 'google',
    ]

    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True


if __name__ == "__main__":
    # 變數 "Page" 為要對網頁爬的頁數，預設為10頁
    page = 10
    print('Start parsing eyny movie....')
    rs = requests.session()
    res = rs.get(targetURL, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    page_url, page_link_all = [], []

    # first page
    page_url.append(targetURL)
    page_link_all = soup.select('.pg')[0].find_all('a')
    # 得到每頁的page link
    for index in range(1, page, 1):
        # print(page_link_all[index].text)  # title
        # print(page_link_all[index]['href'])  # href
        page_url.append('http://www.eyny.com/' + page_link_all[index]['href'])

    content = ''
    total_page = len(page_url)
    count = 0
    # 得到每篇包含 mega 的文章
    for url in page_url:
        res = rs.get(url, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        for title_url in soup.select('.bm_c tbody .xst'):
            if pattern_mega_google(title_url.text):
                name_write = title_url.text
                url_write = 'http://www.eyny.com/{}'.format(title_url['href'])
                content += '{}\n{}\n\n'.format(name_write, url_write)
        count += 1
        print('Crawler: {:.2%}'.format(count / total_page))
        content += u'----next page-----\n\n'

    with open(fileName, 'wb') as f:
        f.write(content.encode('utf8'))

    print('----------END----------')
    path = os.path.abspath(fileName)

    # os.system('gedit ' + path)  # LINUX
    os.system(path)  # Windows
