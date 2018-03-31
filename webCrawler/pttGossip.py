import bs4
import requests
import re
import pandas as pd

class pttGossip():
    def __init__(self,url,baseUrl,cookies):
        self.url=url
        self.baseUrl=baseUrl
        self.cookies=cookies
    def getSoup(self,url):
        r=requests.get(url,cookies=self.cookies)
        soup=bs4.BeautifulSoup(r.text,"html5lib")
        return soup
    def getNextPage(self,soup):
        test=soup.find('div',attrs={'class':'btn-group btn-group-paging'})
        try:
            nextPage=test.findAll('a')[2]
        except KeyError:
            nextPage=''
        targetUrl=nextPage.attrs['href']
        returnSoup=self.getSoup(self.baseUrl+targetUrl)
        return returnSoup
    def getLastPage(self,soup):
        test=soup.find('div',attrs={'class':'btn-group btn-group-paging'})
        lastPage=test.findAll('a')[1]
        targetUrl=lastPage.attrs['href']
        returnSoup=self.getSoup(self.baseUrl+targetUrl)
        return returnSoup
    def getData(self,soup):
        test=soup.find_all('div',attrs={"class":"r-ent"})
        titleList,dateList,authorList=[],[],[]
        for hello in test:
            title=hello.find('div',attrs={"class":"title"}).text.replace('\t',"").replace('\n',"")
            date=hello.find('div',attrs={"class":"date"}).text.replace('\t',"").replace('\n',"")
            author=hello.find('div',attrs={"class":"author"}).text.replace('\t',"").replace('\n',"")
            
            titleList.append(title)
            dateList.append(date)
            authorList.append(author)
        return titleList,dateList,authorList

url='https://www.ptt.cc/bbs/Gossiping/index.html'
cookies = dict(_gat="1",
               __cfduid="d82284aa11c852646ee80c6ae92466a601521305274",
               _ga="GA1.2.877770158.1521305275",
               over18="1",
               _gid="GA1.2.52858989.1521305275")
baseUrl='https://www.ptt.cc'

titleList=[]
dateList=[]
authorList=[]

pttGossip=pttGossip(url,baseUrl,cookies)
soup=pttGossip.getSoup(url)
soup1=pttGossip.getLastPage(soup)
soup2=pttGossip.getNextPage(soup1)

titleList,dateList,authorList=pttGossip.getData(soup2)
for i in range(2):
    soup2=pttGossip.getLastPage(soup2)
    a,b,c=pttGossip.getData(soup2)
    titleList=a+titleList
    dateList=b+dateList
    authorList=c+authorList

title2List=[]
catList=[]
reList=[]
for i,entry in enumerate(titleList):
    if entry[:2]=='Re':
        titleList[i]=entry[4:]
        reList.append('Y')
    else:
        reList.append('N')
    test=re.split('\[|\]',titleList[i])
    if len(test)<2:
        catList.append('-')
        title2List.append(test[0])
    else:
        title2List.append(test[-1].replace('\u3000',' '))
        catList.append(test[-2])

import pandas as pd
df=pd.DataFrame({"date":dateList,"author":authorList,"re[Y/N]":reList,"category":catList,"title":title2List})
df=df[['date','author','re[Y/N]','category','title']]
df=df[:-5]
print(df)