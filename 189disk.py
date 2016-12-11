'''
Created on 2016年4月17日 

189开放云使用接口

@author: heguofeng
'''

from time import gmtime
import time
import requests
import rsa
import re
import json
import binascii 
import base64
from urllib.parse import urlparse
import urllib
import hashlib
import hmac


class OAuth2(object):
    ACCESS_TOKEN_URL = "https://oauth.api.189.cn/emp/oauth2/v3/access_token"
    AUTHORIZE_URL = "https://oauth.api.189.cn/emp/oauth2/v3/authorize"
    AccessToken=""

    def __init__(self,app_key, app_secret, call_back_url):
        self.version = 1.0
        self.app_key = app_key
        self.app_secret = app_secret
        self.call_back_url = call_back_url
        
    #display = default|mobile|popup
    def authorize(self,response_type = "code",display = "page",state = ""):
        querystring = {"app_id":self.app_key,
                       "app_secret":self.app_secret,
                "redirect_uri":self.call_back_url,
                "response_type":response_type,
                "display":display}
        if len(state) > 0:
            querystring["state"] = state
        #return OAuth2.AUTHORIZE_URL + "?" + urllib.urlencode(data)
        return querystring
    
    #grant_type = authorization_code|refresh_token
    def access_token(self,grant_type = "authorization_code",code = "",refresh_token = ""):
        querystring = {"app_id":self.app_key,
                       "app_secret":self.app_secret,
                       "grant_type":grant_type}
        if grant_type == "authorization_code":
            querystring["code"] = code
            querystring["redirect_uri"] = self.call_back_url
        elif grant_type == "refresh_token":
            querystring["refresh_token"] = refresh_token
        try:
            response = requests.get(OAuth2.ACCESS_TOKEN_URL,params=querystring)
            return response.json()
        except requests.exceptions:
            return requests.exceptions
     
    
    '''
    #autologin
    1. get authorizeform
    2.
    '''    
        
    def autologin(self,username,password):
        
        authorform=self.getAuthorizeform()
        
        r=requests.get(authorform["url"],allow_redirects=False)
        print(r.headers)

        location=r.headers['Location']
        print(location)
        
        r=requests.get(location)
        print(r.headers)
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
        
        self.AccessToken=querydict["access_token"][0]
        return(self.AccessToken)
    
    def getAuthorizeform(self):
        authorizeformdata={}
        #print(self.authorize("token"))
        response=requests.get(self.AUTHORIZE_URL,params=self.authorize("token"),allow_redirects=False)
        print(response.request.url)
        #print(response.request.headers)
        html=response.text
        #print(html)
        match=re.findall(r'[a-zA-z]+://[\S]*udb[^\s|"]*',html)
        print(match)
        authorizeformdata["url"]=match[0]
        
        return authorizeformdata
    
class vDiskClient(object):
    API_URL = 'https://api.weipan.cn/2/'
    AccessToken = ""
    AppId="711690470000250948"
    AppSecret="68a6d3dd1605f108d627472951f25ef7"
    
    def __init__(self,token=""):
        self.setAccessToken(token)
        if self.AccessToken!="":
            self.metadata()
    
    def setAccessToken(self,token):
        #self.AccessToken = "fe34416661iDpiR2XCKhG1HxVLR4166e"
        if token!="":
            self.AccessToken = token
            return True
        return False
    
    def getUserInfo(self):
        url="http://api.189.cn/ChinaTelecom/getUserInfo.action"
        payload={"access_token":self.AccessToken,
                 "app_id":self.AppId,
                 }
        headers = {'content-type':'application/json',"Accept":"application/json"}
        r=requests.get(url,params=payload,headers=headers)
        return(r.json())    
    
    def metadata(self):
        
        url="http://api.189.cn/ChinaTelecom/getFolderInfo.action"
        payload={"access_token":self.AccessToken,
                 "app_id":self.AppId,
                 }
        headers = {'content-type':'application/json',"Accept":"application/json"}
        r=requests.get(url,params=payload,headers=headers)
        self.folderId=r.json()["id"]
        self.folderPath=r.json()["path"]
        return(r.json())
    
    
    def listfiles(self):
        
        url="http://api.189.cn/ChinaTelecom/listFiles.action"
        payload={"access_token":self.AccessToken,
                 "app_id":self.AppId,
                 "orderBy":"filename",
                 "pageNum":"1",
                 "pageSize":"20"
                 }
        headers = {'content-type':'application/json',"Accept":"application/json"}
        r=requests.get(url,params=payload,headers=headers)
        return(r.json())
    

    def getfileid(self,filename):
        
        url="http://api.189.cn/ChinaTelecom/getFileInfo.action"
        payload={"access_token":self.AccessToken,
                 "app_id":self.AppId,
                 "filePath":filename,
                 }
        headers = {'content-type':'application/json',"Accept":"application/json"}
        r=requests.get(url,params=payload,headers=headers)
        rjson=r.json()
        print(r.json())
        
        fileid=rjson["id"]
        return(rjson["id"])
    
        
    def getfile(self,files):
        #GET http://api.189.cn/ChinaTelecom/getFileInfo.action 
        #files = {"file":(cloudfilename,fopenhandle)}
        #1\get fileid
        #2\get downloadurl
        #3\download file
        
        data=self.getFiletoData(files["file"][0])
        
        #print(r.headers)
        file=files["file"][1]
        len=file.write(data.encode())
        file.close()
        
        return len   
 
    def getFiletoData(self,filename):
                
        fileid=self.getfileid(filename)
        
        url="http://api.189.cn/ChinaTelecom/getFileDownloadUrl.action"
        querystring={"access_token":self.AccessToken,
                 "app_id":self.AppId,
                 "fileId":fileid,
                 }
        headers = {'content-type':'application/json',"Accept":"application/json"}
        r=requests.get(url,params=querystring,headers=headers)
        #print(r.json())
        filedownloadurl=r.json()["fileDownloadUrl"]
        print(filedownloadurl)
        
        r=requests.get(filedownloadurl)
        
        return r.text   
    
    def putfile(self,files):
        #PUT http://upload-vdisk.sina.com.cn/2/files_put/<root>/<path> 
        r=self.putFileFromData(files["file"][0], files["file"][1].read())
        return(r)

    def putFileFromData(self,filename,data):
        '''
        #1\get upload url
        #headers - >> PUT /uploadFile.action?param=eqiIe9A1C7jnEv2E3&app_id=12437572&access_token=HCabctl7NpZcgk7MT8OVbSnQy317 HTTP/1.1
        headers - >> Host: upload.cloud.189.cn
        headers - >> Edrive-ParentFolderId: 1234
        headers - >> Edrive-FileName: test.txt
        headers - >> Edrive-FileMD5: 9999999999999999999999999999999
        headers - >> Content-Length: 1024
        AccessToken
        '''
        url="http://api.189.cn/ChinaTelecom/getFileUploadUrl.action"
        #url="http://api.cloud.189.cn/getUserInfo.action"
        querystring={"access_token":self.AccessToken,
                 "app_id":self.AppId,
                 }
        headers = {'content-type':'application/json',"Accept":"application/json"}
        r=requests.get(url,params=querystring,headers=headers)
        #print(r.json())
        fileUploadUrl=r.json()["FileUploadUrl"]
        print(fileUploadUrl)
        
        querystring={"access_token":self.AccessToken,
                 "app_id":self.AppId,
                 }

        #b64=base64.encodebytes(data)
        files = {'file': (filename,data)}
        
        curdate=time.strftime("%a, %d %b %Y %H:%M:%S GMT",gmtime())
        print(curdate)

            
        message="AccessToken="+self.AccessToken+"&Operate=PUT&RequestURI=/uploadFile.action"
        message+="&Date="+curdate
        print(message)
        
        signature=self.signature(message)
        md5=hashlib.md5(data).hexdigest()
        size=len(data)
        headers = {"Edrive-FileLength":size,
               "Edrive-FileName":"safedata.txt",
               "Edrive-ParentFolderId":self.folderId,
               "Edrive-FileMD5":md5,
               "Host": "upload.cloud.189.cn",
               "AccessToken":self.AccessToken,
               "app_id":self.AppId,
               "Signature":signature,
               "Date":curdate
               #"Content-Length":1024
               }
    
        fileUploadUrl="http://upload.cloud.189.cn/uploadFile.action"
        r=requests.put(fileUploadUrl,headers=headers,files=files)
        print(r.request.url)
        print(r.request.headers)
        
        print(r.text)
        return(r.json())    
    
    def signature(self,message):
        #message="AccessToken=AFED506D70B5047B4B1BA87CDACF1082&Operate=GET&RequestURI=/getUserInfo.action&Date=Tue, 03 Dec 2013 08:57:48 GMT"
        #AppSecret="ebc0a751e9154e5e0b0cd5a13d4bca9b"
        Signature=hmac.new(str.encode(self.AppSecret),str.encode(message),hashlib.sha1).hexdigest()
        print(Signature)
        return Signature

        
    

if __name__ == '__main__':
    
    AppSecret="68a6d3dd1605f108d627472951f25ef7"
    AppId="711690470000250948"
    oauth2=OAuth2(AppId,AppSecret,"http://127.0.0.1/")
    accesstoken=oauth2.autologin("heguofeng@189.cn", "hgf020613")
    vdc=vDiskClient()
    vdc.setAccessToken(accesstoken)
    print(vdc.getUserInfo())
    print(vdc.metadata())
    print(vdc.listfiles())
    #ct,b=vdc.encode_multipart_formdata({"data":"date"}, [])
    #print(ct,b)
    #print(vdc.createFolder("safebox9"))
    files={"file":("safedata",open("C://Users//heguofeng//Downloads//t.html", 'rb'))}
    print(vdc.putfile(files))
    #s1=file.read()
    #file.close()
    #files = {'file': ("safedata9",base64.encodebytes(s1))}
    #print(vdc.putfile(files))
    #print(vdc.getfile("safedata8"))
    #vdc.putFileFromData("safedata10", s1)
    
    files={"file":("//我的应用//天翼开放平台应用//数据宝//test.txt",open("C://Users//heguofeng//Downloads//t.txt", 'wb'))}
    vdc.getfile(files)
    #s=vdc.getFiletoData("safedata10")
    #s2=base64.decodebytes(s.encode())
    #print(len(s),s)
    #file.write(s.encode())
    #file.close()
    #vdc.postfile()
    
    
    pass