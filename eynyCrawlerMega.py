#coding=utf-8

import requests
from bs4 import BeautifulSoup
import os
import re
requests.packages.urllib3.disable_warnings()


targetURL = 'http://www.eyny.com/forum-205-1.html'	
fileName = 'eyny-Movie-Mage.txt'


def patternMega(text):
    patterns = [ 'mega', 'mg','mu','ＭＥＧＡ','ＭＥ','ＭＵ','ｍｅ','ｍｕ','ｍｅｇａ']
    for pattern in patterns:
       if re.search(pattern, text, re.IGNORECASE):
          return True
			
if __name__ == "__main__":
    #變數 "Page" 為要對網頁爬的頁數，預設為10頁
    Page = 10
    print 'Start parsing eyny movie....'
    rs = requests.session()  
    res = rs.get(targetURL,verify=False)
    soup = BeautifulSoup(res.text,'html.parser')
    pageURL, pagelinkALL = [] , []

    #first page
    pageURL.append(targetURL)
    pagelinkALL = soup.select('.pg')[0].find_all('a')
    #得到每頁的page link
    for index in range(1,Page,1):
        #print pagelinkALL[index].text //title
        #print pagelinkALL[index]['href'] //href       
        pageURL.append('http://www.eyny.com/'+pagelinkALL[index]['href'])
	
 
    content = ''
    totalpage = len(pageURL)
    count = 0
    #得到每篇包含 mega 的文章
    for URL in pageURL:       
        res = rs.get(URL,verify=False)
        soup = BeautifulSoup(res.text,'html.parser')   
        for titleURL in soup.select('.bm_c tbody .xst'):
            if ( patternMega(titleURL.text) ):
               name_write = titleURL.text
               URL_write = 'http://www.eyny.com/'+titleURL['href']
               content += name_write+'\n'+URL_write+'\n\n'
        count+=1
        print "Crawler: " + str(100 * count / totalpage ) + " %."
        content += u'----next page-----\n\n'

    with open(fileName,'wb') as f:
          f.write( content.encode('utf8') )   
  
    print '----------END----------'
    path = os.path.abspath(fileName)

    os.system('gedit '+path) #LINUX
    #os.system(path) #Windows





