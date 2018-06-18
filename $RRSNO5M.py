# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import requests
import ssl
import socket
from datetime import datetime
from lxml import html
from OpenSSL.crypto import load_certificate,FILETYPE_PEM
import multiprocessing

class ShecaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    domain = scrapy.Field()
    url = scrapy.Field()


class DomainItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    isHttps = scrapy.Field()
    issuer = scrapy.Field()
    subject = scrapy.Field()
    notAfter = scrapy.Field()
    contactor = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    
    def setDomainItem(self,name,url,ishttps=False,issuer="",subject =  "", notafter="",contactor="",email="",phone=""):

        self["name"] = name
        self["url"] = url 
        self["isHttps"] = ishttps
        self["issuer"] = issuer
        self["subject"] = subject
        self["notAfter"] = notafter
        self["contactor"] = contactor
        self["email"] = email
        self["phone"] = phone
         
    def ishttps(self,url):
        try:
            r=requests.get(url,verify=False,timeout=10)
            if r.status_code == 200:
                return True
        except Exception:
            return False
    
    def getHeaderHtml(self):
        if self["isHttps"]:
            url="https://" + self["url"]
            try:
                r=requests.get(url,verify=False,timeout=10)
                if r.status_code == 200:
                    return r.headers,r.text
            except Exception:
                return "",""
        return "",""
        
             
    def getDomainInfo(self):
        url="https://" + self["url"]
        if self.ishttps(url):
            self["isHttps"] = True
        else:
            url="https://www." + self["url"]
            self["isHttps"] = self.ishttps(url)
            if self["isHttps"]:
                self["url"]='www.'+self["url"]
        if self["isHttps"]:
            self.getCertInfo()
        self.getContactInfo()
        return 
    
    def getCommonName(self,certer):
        #print(certer)
        for item in certer:
            #print(item)
            if item[0][0] == "organizationName":
                return item[0][1]
          
    def getCertInfo(self):    
        hostname= self["url"]
        certpem =  ""
        try:
#             ctx = ssl.create_default_context()
#             s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
#             s.connect((hostname, 443))
#             cert = s.getpeercert() 
#             #print(cert)
#             dt = datetime.strptime(cert['notAfter'], "%b  %d %H:%M:%S %Y GMT")
#             self["notAfter"] = dt.strftime("%Y/%m/%d")
#             self["issuer"] = self.getCommonName(cert["issuer"])
#             self["subject"] = self.getCommonName(cert["subject"])
            certpem = ssl.get_server_certificate((hostname, 443))
            x509cert = load_certificate(FILETYPE_PEM,certpem)
            
            self["issuer"] = dict(x509cert.get_issuer().get_components())[b'CN'].decode()
            self["subject"] = dict(x509cert.get_subject().get_components())[b'CN'].decode()
            self["notAfter"] = x509cert.get_notAfter().decode()
            
        except ssl.CertificateError:
            self["isHttps"] = True
        except: 
            self["isHttps"] = False
        return certpem
    
          
    def getContactInfo(self):
        print("getContactInfo")
#        yield scrapy.Request("https://www.whois.com/whois/" + self["url"], callback=self.whoisParse)
        #request = scrapy.Request("http://whois.chinaz.com/" + self["url"], callback=self.chinaZWhoisParse)
#         process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
#         process.crawl(WhoisSpider,domain=self["url"])
#         result = process.start() # the script will block here until the crawling is finished   
#         print(result)
             
        #yield request
        response = requests.get("http://whois.chinaz.com/" + self["url"])
        tree = html.fromstring(response.text)
        names = tree.xpath("//div[@class='fl WhLeList-left']/text()")
        values = tree.xpath("//div[@class='fr WhLeList-right']/span/text()|//div[@class='fr WhLeList-right block ball lh24']/span/text()|//div[@class='fr WhLeList-right']/div/span/text()")
        nvs = dict(zip(names,values))
        self["email"] = nvs.get("联系邮箱","")
        self["phone"] = nvs.get("联系电话","")
        self["contactor"] = nvs.get("联系人","")
        pass
        
def getDomainItemDetail(line):
    di = DomainItem()
    print(line.strip())
    di.setDomainItem(line.strip(), line.strip(), True)
    certpem = di.getCertInfo()
    header,html=di.getHeaderHtml()
    return ("%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(di["url"],di["issuer"],di["subject"],di["notAfter"],certpem,header,html))
    
def saveData(s):
    with open("ipcertdetail.txt","a+") as f:
        f.write(s)
     
        
if __name__ == '__main__':
    f = open("ip.txt","r")
    lines = f.readlines()
#     fo = open("ipcertdetail.txt","w")
    pool = multiprocessing.Pool(processes=10)
    count = 0
    for line in lines:
        print(count)
        count += 1
#         di = DomainItem()
#         di.setDomainItem(line.strip(), line.strip(), True)
#         certpem = di.getCertInfo()
#         header,html=di.getHeaderHtml()
#         fo.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(di["url"],di["issuer"],di["subject"],di["notAfter"],certpem,header,html))
        pool.apply_async(getDomainItemDetail, (line,), callback=saveData)
#         fo.write(getDomainItemDetail(line))
#     fo.close()
    pool.close()
    pool.join()
    f.close()

    pass
                



