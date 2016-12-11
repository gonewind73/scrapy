'''
Created on 2016年5月9日

@author: heguofeng
'''

import requests
import _thread
import threading
import csv
from datetime import datetime, date
import time
import sys

import re
from flask.testsuite import catch_stderr

import ssl
import socket

class domainsprider():
    
    def __init__(self,kw):
        self.list=[]
        self.csvfile=open('google.csv', 'w', newline='')
        fieldnames = ['title', 'baiduUrl',"realUrl","isURL","notAfter"]
        self.writer = csv.DictWriter(self.csvfile, fieldnames=fieldnames)
        self.writer.writeheader()
        self.keyword=kw
        pass
    
    def spride(self,url):
        self.list=[]
        header={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
        proxies={'http':'http://127.0.0.1:8787',
               'https':'https://127.0.0.1:8787'}
        r=requests.get(url,headers=header,proxies=proxies)
        html=r.text.encode(r.encoding).decode("utf-8","ignore")
        print(html)
        #Dl=re.findall(r'(?<=a\shref="/url\?q=)[^"]*(?=")',html)
        Dl=re.findall(r'(?<=a\shref="http)[^"]*(?=")',html)
        print(Dl)
        dts= list(set(Dl))  
        for i in range(0,len(dts)):
            dts[i]="http"+dts[i]
        #Dbaidu=re.findall(r'(?<=http://www.baidu.com/baidu.php\?url=)[^&]*(?=&)',html)
        #print(Dbaidu)
        #dts1= list(set(Dbaidu))  
        #for i in range(0,len(dts1)):
        #    dts.append("http://www.baidu.com/baidu.php?url="+dts1[i])
        print(dts)
            
        
        
        
        for i in range(0,len(dts)):
            item=dts[i]
            
            
            dict={"baiduUrl":item,
                  }
    
            self.list.append(dict)
            #try:
            
            t=(i,)
           
            
            _thread.start_new_thread(self.getRealUrl,t)
            #except:
            #   print( "Error: unable to start thread")
            #self.list[i].append(self.ishttps(self.list[i][0]))
            #print(r)
        running=True   
        count=0
        while running:
            running=False
            time.sleep(1)
            count=count+1
            print(count)
            if count>300 :
                break
            for i in range(0,len(self.list)):
                if((self.list[i]).get("isURL")==None):
                    running=True
                    
        print(self.list)   
        print("finish!")
        
    
    def getRealUrl(self,i):
        url=self.list[i]["baiduUrl"]
        try:
            header={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
            r=requests.get(url,headers=header)
            if r.status_code==200:
                html=r.text.encode(r.encoding).decode("utf-8")
                (self.list[i])["realUrl"]=r.request.url
                title=re.findall(r'(?<=<title>)[^>]*(?=</title>)',html)
                (self.list[i])["title"]=title[0]
                if html.find(self.keyword) > 0 :
                    (self.list[i])["isURL"]=True
                else:
                    (self.list[i])["isURL"]=False
                
        except Exception:
            (self.list[i])["isURL"]=False
        print(i)
        print(self.list[i])
 
        return 
        
 
        
    def getContact(self,i):
        url="http://whois.chinaz.com/"+(self.list[i])["domainname"]
        try:
            r=requests.get(url)
            #html=r.text.encode(r.encoding).decode("utf-8")
            email=re.findall(r'(?<=\<span\>)[\S]*@[\S]*(?=\</span\>)',r.text)
            (self.list[i])["email"]=email[0]
        except:
            pass
        
        return
        
    def savelist(self):   
        try:
            for i in range(0,len(self.list)):
                self.writer.writerow(self.list[i])
        except:
            print("Error:!!!")
            print(self.list[i])
        return
    
    def close(self):
        self.csvfile.close()

    def getPages(self,url):
        r=requests.get(url)
        html=r.text.encode(r.encoding).decode("utf-8")
        #<div class="ListPageWrap">
        pages=re.findall(r'(?<=\<div\sclass=\"ListPageWrap\"\>).*(?=\</div\>)',html)
        pageno=re.findall(r'\d+',pages[0])
        max=0
        for item in pageno:
            if int(item)>max:
                max=int(item)
        print(max)
        return max        
    
    def changetime(self):
        csvfile=open('domainr.csv', 'r', newline='')
        reader = csv.DictReader(csvfile)
        csvfilet=open('domaint.csv', 'w', newline='')
        fieldnames = ['title', 'baiduUrl',"email","isHttps","notAfter"]
        writer = csv.DictWriter(csvfilet, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if row["notAfter"]!="" :
                dt = datetime.strptime(row["notAfter"], "%b  %d %H:%M:%S %Y GMT")
                row["notAfter"]=dt.strftime("%Y/%m/%d")
            print(row)
            writer.writerow(row)
                
        csvfilet.close()
        csvfile.close()
      

                
    

if __name__ == '__main__':
    
    if len(sys.argv)>=2:
        keyword=sys.argv[1]
    else:
        keyword="视频会议" 
    
    ds=domainsprider(keyword)
    
    
    #url="http://top.chinaz.com/diqu/index_ShangHai.html"
    for i in range(0,10):
        url="https://www.google.com/search?q=视频会议&start="+str(i*10)
        print(url)
        #pages=ds.getPages(url)
    
    
        ds.spride(url)
        ds.savelist()

    
    
    ds.close()
    
    
    #ds.savelist()
    