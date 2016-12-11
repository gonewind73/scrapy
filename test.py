'''
Created on 2016年4月6日

@author: heguofeng
'''
# https://oauth.api.189.cn:443/emp/oauth2/v3/udblogin/232823620

import re
import requests
import urllib
from urllib.parse import urlparse
import urllib.parse


fd=open("C://Users//heguofeng//Downloads/t.html", 'rb')
#fd=open("c://safedata", 'r')
txt=fd.read()

#print(isinstance(txt, utf8) )
#print(txt.decode())
#txt=     ' <iframe src="https://oauth.api.189.cn:443/emp/oauth2/v3/udblogin/232823620" height="310px" frameborder="0" scrolling="no" class="iframe_show" allowtransparency="true"></iframe>'
match=re.findall(r'[a-zA-z]+://[\S]*udb[^\s|"]*',txt.decode())
print(match)

r=requests.get(match[0],allow_redirects=False)
#print(r.text)
#print(r.history)
print(r.headers)

location=r.headers['Location']
print(location)


         
r=requests.get(location)
print(r.headers)
#print(r.text)

'''
accountType:
appId:tyopen
returnUrl:
userName:heguofeng@189.cn
mail:@189.cn
password:hgf020613
ValidateCode:
'''
headers = {'content-type':'application/x-www-form-urlencoded',
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Referer":location,
           "Accept-Language":"zh-cn",
           "User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; MyIE9; BTRS123646; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
           "Accept-Encoding": "gzip, deflate",
           "Connection": "Keep-Alive",
           "Host": "open.e.189.cn",
           "Cookie":"loginCookie=heguofeng@189.cn"
           }

payload={"userName":"heguofeng@189.cn",
         "password":"hgf020613",
         "accountType":"",
         "appId":"tyopen",
         "mail":"@189.cn",
         "ValidateCode":""}

r=requests.post(location,allow_redirects=False,params=payload)
print(r.url)
print(r.headers)
location=r.headers['Location']
print(location)

#print(re.search(r'(?<=\?)[\S]*', location))
query=urlparse(location).query
querydict=urllib.parse.parse_qs(query)
print(querydict)
print(querydict["redirect_uri"][0])



headers = {'content-type':'application/x-www-form-urlencoded',
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Referer":location,
           "Accept-Language":"zh-cn",
           "User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; MyIE9; BTRS123646; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
           "Accept-Encoding": "gzip, deflate",
           "Connection": "Keep-Alive",
           "Host": "open.e.189.cn",
           "Cookie":"loginCookie=heguofeng@189.cn"
           }

payload={"paras":querydict["paras"],
         
         "appId":querydict["appId"],
         "sign":querydict["sign"],
         }

r=requests.get(querydict["redirect_uri"][0],allow_redirects=False,headers=headers,params=payload)
print(r.url)
print(r.headers)

location=r.headers['Location']
print(location)

#print(re.search(r'(?<=\?)[\S]*', location))
query=urlparse(location).query
querydict=urllib.parse.parse_qs(query)
print(querydict)
print(querydict["access_token"][0])
#print(r.text)


#txt="https://oauth.api.189.cn:443/emp/oauth2/v3/udblogin/232823620"
