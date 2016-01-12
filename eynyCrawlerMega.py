#coding=utf-8

import requests
from bs4 import BeautifulSoup
import os
import re
requests.packages.urllib3.disable_warnings()


targetURL='http://www.eyny.com/forum-205-1.html'	
fileName='eyny-Movie-Mage.txt'


def patternMega(text):
    patterns = [ 'mega', 'mg','mu','ＭＥＧＡ','ＭＥ','ＭＵ','ｍｅ','ｍｕ','ｍｅｇａ']
    for pattern in patterns:
       if re.search(pattern, text, re.IGNORECASE):
          return True
			
if __name__ == "__main__":
    Page=10
    print 'Start parsing eyny movie....'
    rs=requests.session()  
    res=rs.get(targetURL,verify=False)
    soup=BeautifulSoup(res.text,'html.parser')
    pageURL=[]
    pagelinkALL=[]

    pagelinkALL=soup.select('.pg')[0].find_all('a')
    pageURL.append(targetURL)#first page

    for num in range(1,Page,1):
        #print pagelinkALL[num].text
        #print pagelinkALL[num]['href']
        pageURL.append('http://www.eyny.com/'+pagelinkALL[num]['href'])
	
   
    res=rs.get(targetURL,verify=False)
    soup=BeautifulSoup(res.text,'html.parser')  
    #print  soup.select('.common .xst')[5].text
    #print  soup.select('.common .xst')[5]['href']

    f=open(fileName,'wb')
    obj=''
    total=len(pageURL)
    count=0
    for URL in pageURL:
        count+=1       
        res=rs.get(URL,verify=False)
        soup=BeautifulSoup(res.text,'html.parser')   
        for titleURL in soup.select('.bm_c tbody .xst'):
            if(patternMega(titleURL.text)):
               #print titleURL['href']
               #print titleURL.text
               name_write=titleURL.text
               URL_write='http://www.eyny.com/'+titleURL['href']
               obj+=name_write+'\n'+URL_write+'\n\n'
        print "Crawler: " + str(100 * count / total ) + " %."
        obj+=u'----next page-----\n\n'

    f.write(obj.encode('utf-8'))
    f.close()

   
    print '----------END----------'
    path= os.path.abspath(fileName)
    #os.system('gedit '+path) #LINUX
    os.system(path)
