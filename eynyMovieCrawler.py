import os
import re
import requests
from bs4 import BeautifulSoup
from sys import platform


class Crawler:
    rs = requests.session()

    def __init__(self, target_url):
        print('Start Crawler....{}'.format(self.__class__.__name__))
        self.url = target_url
        self.content = self.analyze()

    def analyze(self):
        res = self.rs.get(self.url, verify=False)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup


class EynyMovie(Crawler):

    def __init__(self, target_url, parser_page):
        super().__init__(target_url)
        self.parser_page = parser_page
        self.pages = self.page_links

    @property
    def page_links(self):
        page_urls = [self.url]  # first page
        all_page_urls = self.content.select('.pg')[0].find_all('a')
        # 得到每頁的 page link
        for index in range(1, self.parser_page, 1):
            # print(all_page_urls[index].text)  # title
            # print(all_page_urls[index]['href'])  # href
            page_urls.append('http://www.eyny.com/{}'.format(all_page_urls[index]['href']))
        return page_urls

    def parser(self):
        content = ''
        count = 0
        total_pages = len(self.pages)
        for page in self.pages:
            crawler = Crawler(page)
            for data in crawler.content.select('.bm_c tbody .xst'):
                href = data['href']
                title = data.text
                if '11379780-1-3' in href:
                    continue
                if self.pattern_mega(title):
                    content += '{}\nhttp://www.eyny.com/{}\n\n'.format(title, href)
            count += 1
            print('Crawler: {:.2%}'.format(count / total_pages))
            content += u'----next page-----\n\n'

        return content

    @staticmethod
    def pattern_mega(text):
        patterns = [
            'mega', 'mg', 'mu', 'ＭＥＧＡ', 'ＭＥ', 'ＭＵ',
            'ｍｅ', 'ｍｕ', 'ｍｅｇａ', 'GD', 'MG', 'google',
        ]
        match = False
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                match = True
                break
        return match


class WriteFile:
    def __init__(self, file_name, data):
        self.file_name = file_name
        self.data = data
        self.write_data()

    def write_data(self):
        with open(self.file_name, 'wb') as f:
            f.write(self.data.encode('utf8'))

    def open(self):
        path = os.path.abspath(self.file_name)
        os_mapping = {
            "linux": "gedit ",  # LINUX
            "linux2": "gedit ",  # LINUX
            "win32": ""  # Windows
        }
        os.system(os_mapping.get(platform) + path)  # LINUX


if __name__ == "__main__":
    url = 'http://www.eyny.com/forum-205-1.html'
    FileName = 'eyny-Movie-Mage.txt'
    crawler_page = 10  # 網頁爬的頁數，預設為10頁
    eyny_movie = EynyMovie(url, crawler_page)
    movie_data = eyny_movie.parser()
    write_file = WriteFile(FileName, movie_data)
    write_file.open()
