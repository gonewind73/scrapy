'''
Created on 2016年4月23日

@author: heguofeng
'''

'''
Created on 2016年4月17日 

189开放云使用接口

@author: heguofeng

App Key: 600102343
App Secret: 93c6a3491a5e1d93af0e44b47079814

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
import xml.etree.ElementTree as ET




class OAuth2(object):
    Provider="Cloud189Disk"
    ACCESS_TOKEN_URL = "http://cloud.189.cn/open/oauth2/accessToken.action"
    AUTHORIZE_URL = "http://cloud.189.cn/open/oauth2/authorize.action"
    AccessToken=""

    def __init__(self,app_key, app_secret, call_back_url):
        self.version = 1.0
        self.app_key = app_key
        self.app_secret = app_secret
        self.call_back_url = call_back_url
        self.app_secret="93c6a3491a5e1d93af0e44b470798148"
        self.app_key="600102343"
        
    #display = default|mobile|popup
    def authorize(self,response_type = "code",display = "default",state = ""):
        timestamp=str(int(time.time()))
        message="appKey="+self.app_key+"&timestamp="+timestamp
        appSignature=hmac.new(str.encode(self.app_secret),str.encode(message),hashlib.sha1).hexdigest()

        querystring = {"appKey":self.app_key,
                       "appSignature":appSignature,
                "callbackUrl":self.call_back_url,
                "responseType":response_type,
                "display":display,
                "timestamp":timestamp}
        if len(state) > 0:
            querystring["state"] = state
        #return OAuth2.AUTHORIZE_URL + "?" + urllib.urlencode(data)
        return querystring
    
    #grant_type = authorization_code|refresh_token
    def access_token(self,grant_type = "authorization_code",code = "",refresh_token = ""):
        timestamp=str(int(time.time()))

        #AppKey=b"600086127"
        #timestamp=b"1386060076658"
        #AppSecret="dcfc389d74c6a9f437a6fa4972f3ed69"
        message="appKey="+self.app_key+"&timestamp="+timestamp
        appSignature=hmac.new(str.encode(self.app_secret),str.encode(message),hashlib.sha1).hexdigest()
        #print(appSignature)
        
        querystring={
                     "appKey":self.app_key,
                     "appSignature":appSignature,
                     "grantType":grant_type,
                     "timestamp":timestamp,
                     
                     }
      
        return querystring
     
    
    '''
    #autologin
    1. get authorizeform
    2.
    '''    
        
    def autologin(self,username,password):
        
 
    
        '''
        1、http://cloud.189.cn/open/oauth2/authorize.action?  获得
        2、http://cloud.189.cn/udb/udb_login.jsp?pageId=6&pageKey=oauth&clientType=web&pageId=6&
        3、submit 重定向  http://open.e.189.cn/api/account/unifyAccountLogin.do? 
        4、http://open.e.189.cn/api/account/unifyAccountLogin.do?  
            Set-Cookie:SSON=; domain=.e.189.cn; path=/; expires=Thu,=
           Cookie:loginCookie=heguofeng%40189.cn 01-Dec-1994 16:00:00 GMT
        5、submit https://open.e.189.cn/api/common/loginSubmit.do 
            Set-Cookie:OPENINFO=33c28688ef52ce9e3a9ef87388047efbde5e3e2e4c7ef6ef267632468c7dfaf2c85b12f483a9eb44cceb3f09d0a7eff5815c2d680e450b431bce99161e62b91343521384863c6ce519f93e4c0ae9eee4c01708f0aa82aea2054f1d38a2f49b85; domain=.e.189.cn; path=/
            Set-Cookie:SSON=d1d5ab4963f93a9b5f3d8f316abad14777675f0914bea15451a526abab1d139e1eac4370795de72e86470c77238bf983c110f27046e4c01aa461e663681c37e4ffd6cefd5ac3fe64d123c301c5ff979885608b1b3132343cab823f853fe88cd2b39e25d27c718b090bb4058ac6fb9d53feae7e665ca2a6c5c8adb3e9df3accd9a592d51dd12aa182ab5d1b48f8279372764679959ea253c5e178d584afad30a7; domain=.e.189.cn; path=/
            Set-Cookie:JSESSIONID=aaaSaeyO1s_R2dp8-ebrv; path=/
        6、location http://open.e.189.cn/api/common/loginRedirect.do?result=0&msg=Success
        7、http://cloud.189.cn/callbackUnify.action? 
          Set-Cookie:COOKIE_LOGIN_USER=33A2AE7555726B4DC20E5F51AA44B6FDEAD3394B7B39567A8BDAFD61E0F2EA9F8D75CFC8D4C4954C6D75BED03B4EA1D4; domain=cloud.189.cn; path=/
    
        8、http://cloud.189.cn/open/oauth2/processAuth.action?
        9、http://127.0.0.1
        
        '''
        authorizeformdata={}
        cookies ={} 
        #1
        response=requests.get(self.AUTHORIZE_URL,params=self.authorize("token"),allow_redirects=False)
        #print("1 "+response.request.url)
        html=response.text
        match=re.findall(r'(?<=redirect_url\s\=\s\')[^\']*(?=\')',html)
        authorizeformdata["url"]=match[0]
        url2="http://cloud.189.cn/udb/udb_login.jsp?pageId=6&pageKey=oauth&clientType=web&redirectURL="+match[0]
        #print("2 "+url2)
        
        #2
        r=requests.get(url2,allow_redirects=False,cookies=cookies)
        ##print(r.headers)
        #print(r.cookies)
        url3=r.headers["Location"]
        #print("3 "+url3)
        cookies=r.cookies
        
        #3
        r=requests.get(url3,cookies=cookies)
        html=r.text
        match=re.findall(r'(?<=name\=\"returnUrl\"\svalue\=\")[^\"]*(?=\")',html)
        #print(match[0])
        url4="https://open.e.189.cn/api/common/loginSubmit.do"
        queryString={
                     "accountType":"01",
                     "appId":"cloud",
                     "returnUrl":match[0],
                     "userName":username,
                     "password":password,
                     "ValidateCode":""
                     }
        
        #4
        r=requests.post(url4,params=queryString,allow_redirects=False,cookies=cookies)
        #print(r.request.url)
        #print(r.cookies)
        cookies=r.cookies
        url5=r.headers["Location"]
        #print("5 "+url5)

        #5
        r=requests.get(url5,allow_redirects=False,cookies=cookies)
        #print(r.text)
        #print(r.cookies)
        cookies=r.cookies
        
        pr=urlparse(url5)
        qs=urllib.parse.parse_qs(pr.query)
        url6=qs["toUrl"][0]
        #print("6 "+url6)
        
        r=requests.get(url6,allow_redirects=False,cookies=cookies)
        #print(r.text)
        #print(r.cookies)
        cookies=r.cookies
        
        match=re.findall(r'(?<=redirect_url\s\=\s\')[^\']*(?=\')',r.text)
        #print("7:  "+match[0])
        
        #pr2=urlparse(url)
        #print(pr2.query)
        
        #match=re.findall(r'(?<=redirectURL\=)[^\"]*',pr2.query)
        #print(match[0])
        
        url7=match[0]
        r=requests.get(url7,cookies=cookies)
        #print(r.text)
        match=re.findall(r'(?<=redirect_url\s\=\s\')[^\']*(?=\')',r.text)
        url8=match[0]
        #print("8 "+url8)
        
        match=re.findall(r'(?<=\#accessToken\=)[^\&]*(?=\&)',url8)
        #print(match)
        
       
        #print(url)
        
        #http://open.e.189.cn/api/account/unifyAccountLogin.do?appId=cloud&version=v1.1&clientType=1&format=redirect&paras=6F367DC02D5986DE3E35FC059101D540D2B407C14C484958FEA557CDC8AB8DBC06C99A481E8329277EE0146E507848A1D65603E896A17240563148FE9051586C3E76C4B5CC979652D3F12A3FA40DC971E9B06791545DE40EE9FC695178BD6997D1A0FA0BF66E12EA130252077355CA86407200E3E2B40774A40C6E02740DD9E8390F1812B0010C8ED51D1DFDF6A66508440870A8DCB7BE9E3C3877319A3D593FEA1D13AF2C941C47167AA4907380C079CE37E987CFCD910517E12DAFDDA9EFA4F703F65BAE66C627751E1D98F9345C801110D664568E0224F5087E5AB7198C363AE61A9232994A43920FFBEAA60720A6321B758E5323761A98B19913F8C5F53A3ED2EF1186BFAD1963B57235F7B5343981FE695AD97F276DEA5D6CE7EF75507B8CDA06CDBC63B4E07D3FB0DE9560546AB26B3A8DD681ADCAF778685F0ECA5A7222A716DBB45B5FBA2FC1B920E11AC821F7ED8FE77CC4C60BD9BBB2BB87B172EBE7A995F14D00E971CBC8C3215C0D8190A34A3037A252EC17FC9946EAA48CD0305841D1BE8FCED81E1CFEC8C8D6217D370EAD1EA418E58955ED64AF9A59776FC2A7D73B555DADE3EA8DFED212C51F547E8F5FD5EDEBD6A8A387C18AA21C2AC731CEC2AA8158CFE5AAB82FF3436451F9B3168B58D59E4008239B533F5770ECF7251489BD70EFC610163861EB5A7FEFEDBF0E2712D27C91EB96C5735E343A12994B021ABA0E408CECB9E0B86918882EED4E077D8D2692A25A2BF500B8E25A4A1B9996996C579B9B83976FD96284EB1772A1D23FF66C9A73B324E2FDDA23D31B067AB1ABF5B4DA7860CAE26C452D46BE9317155759FCA3B25F057351C02A1FFD4CE8D5528B18C92741EC6C0263878ED199F1&sign=A3CFAD7BF7D200ED3E0CEA0C477D88D79CEA1C31
        self.AccessToken=match[0]
        return(self.AccessToken)
    
    def getAccessToken(self,username,password):
        
        '''
        querystring=self.access_token("e189_accessToken")
        querystring["e189AccessToken"]="a4d0e72c87f0ff741ca11c8c6db9ff0b1460155308624"
        '''
        querystring=self.access_token("password")
        querystring["loginName"]=username
        querystring["password"]=password
        
        
        #print(querystring)
        

        r=requests.get(self.ACCESS_TOKEN_URL,params=querystring)
        #print(r.json())
        self.AccessToken=r.json()["accessToken"]
        return(self.AccessToken)

  
        
        #189_passport
        #url+="&grantType=189_passport&timestamp="+str(timestamp)
        #url+="&account=heguofeng@189.cn"
        
        #url+="&display=default"+"&timestamp="+"&callbackUrl="
        

    
    #BADC9B24393F2AB867BF9A444EDB22B1  
    #08987207

    
class vDiskClient(object):
    AccessToken = ""
    AppSecret="93c6a3491a5e1d93af0e44b470798148"
    AppId="600102343"
    
    def __init__(self,token=""):
        self.setAccessToken(token)

    
    def setAccessToken(self,token):
        #self.AccessToken = "fe34416661iDpiR2XCKhG1HxVLR4166e"
        if token!="":
            self.AccessToken = token
            return True
        return False
    
    def getUserInfo(self):
        url="http://api.cloud.189.cn/getUserInfo.action"

        
        date=self.gmttime()
        signature=self.signature("GET", "/getUserInfo.action", date)
        headers = {'content-type':'application/json',"Accept":"application/json",
                   "AccessToken":self.AccessToken,
                   "Signature":signature,
                   "Date":date}
        
        r=requests.get(url,headers=headers)
        username=""
        tree=ET.fromstring(r.text)
        for s in tree.findall("loginName"):
            username=s.text
        print( username)
        
        return(r.text)    
    
    
    def listfiles(self):
        
        url="http://api.cloud.189.cn/listFiles.action"
        
        date=self.gmttime()
        signature=self.signature("GET", "/listFiles.action", date)
        headers = {'content-type':'application/json',"Accept":"application/json",
                   "AccessToken":self.AccessToken,
                   "Signature":signature,
                   "Date":date}
        queryString={
                     "orderBy":"filename",
                     "pageNum":"1",
                     "pageSize":"20"
                     }
        
        r=requests.get(url,params=queryString,headers=headers)
        return(r.text)    



    def getFileInfo(self,filename):
        
        url="http://api.cloud.189.cn/getFileInfo.action"
        
        date=self.gmttime()
        signature=self.signature("GET","/getFileInfo.action",date)
        
        headers = {
               "AccessToken":self.AccessToken,
               "Signature":signature,
               "Date":date
               
               }
        queryString={
                     "fileId":"",
                     "filePath":filename,
                     
                     }
    

        r=requests.get(url,headers=headers,params=queryString)
        
        print(r.text)     
        tree=ET.fromstring(r.text)
        fileid=""
        for s in tree.findall("id"):
            fileid=s.text
        
        #fileid="713231822902243"
        return fileid
    
        
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
                
        fileid=self.getFileInfo("//我的应用//safebox//"+filename)
       
        url="http://api.cloud.189.cn/getFileDownloadUrl.action"
        date=self.gmttime()
        signature=self.signature("GET","/getFileDownloadUrl.action",date)
        
        headers = {
               "AccessToken":self.AccessToken,
               "Signature":signature,
               "Date":date
               
               }
        queryString={
                     "fileId":fileid
                     }
    

        r=requests.get(url,headers=headers,params=queryString)
        
        #print(r.text)
        tree=ET.fromstring(r.text)
        if tree.tag !="fileDownloadUrl":
            return ""
        filedownloadurl=tree.text
        #print(filedownloadurl)
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
        
        #Cloud189Disk 不支持 multipart！！！MD5可以不带
        '''
        #for 189Disk must delete then put,else the filename will change
        fileid=self.getFileInfo("//我的应用//safebox//"+filename)
        self.delfile(fileid)
        
        url="http://upload.cloud.189.cn/uploadFile.action"
        
        
        files = {'file': (filename,data)}
        

        date=self.gmttime()
        signature=self.signature("PUT","/uploadFile.action",date)
        md5=hashlib.md5(data).hexdigest()
        print(md5)
        size=len(data)
        headers = {"Edrive-FileLength":size,
               "Edrive-FileName":filename,
               #"Edrive-ParentFolderId":"",
               #"Edriver-BaseFileId":"",
               #"Edrive-FileMD5":md5,
               #"Host": "api.cloud.189.cn",
               "AccessToken":self.AccessToken,
               "Signature":signature,
               "Date":date
               
               }
    
        #files={"file":("safedata",open("C://Users//heguofeng//Downloads//t.html", 'rb'))}
        r=requests.put(url,headers=headers,data=data)
        print(r.request.headers)
        print(r.request.body)

        
        return(r.text)    
    
    def delfile(self,fileid):
        url="http://api.cloud.189.cn/deleteFile.action"
        date=self.gmttime()
        signature=self.signature("POST","/deleteFile.action",date)
        
        headers = {
               "AccessToken":self.AccessToken,
               "Signature":signature,
               "Date":date
               
               }
        queryString={
                     "fileId":fileid
                     }
    
        r=requests.post(url,headers=headers,params=queryString)
        
        return(r.text)            
    
    def gmttime(self):
        return time.strftime("%a, %d %b %Y %H:%M:%S GMT",gmtime())
    
    def signature(self,operate,requestURI,date):
        message="AccessToken="+self.AccessToken  \
                    +"&Operate="+operate+"&RequestURI="+requestURI \
                    +"&Date="+date
        print(message)
        #message="AccessToken=AFED506D70B5047B4B1BA87CDACF1082&Operate=GET&RequestURI=/getUserInfo.action&Date=Tue, 03 Dec 2013 08:57:48 GMT"
        #AppSecret="ebc0a751e9154e5e0b0cd5a13d4bca9b"
 
        Signature=hmac.new(str.encode(self.AppSecret),str.encode(message),hashlib.sha1).hexdigest()
        print(Signature)
        return Signature

        
    

if __name__ == '__main__':
    


    AppSecret="93c6a3491a5e1d93af0e44b470798148"
    AppId="600102343"
    oauth2=OAuth2(AppId,AppSecret,"http://127.0.0.1/")
    #accesstoken=oauth2.getAccessToken("heguofeng@189.cn", "hgf020613")
    accesstoken=oauth2.autologin("heguofeng@189.cn", "hgf020613")
    vdc=vDiskClient()
    vdc.setAccessToken(accesstoken)
    print(vdc.getUserInfo())
    #print(vdc.metadata())
    print(vdc.listfiles())
    #ct,b=vdc.encode_multipart_formdata({"data":"date"}, [])
    #print(ct,b)
    #print(vdc.createFolder("safebox9"))
    fileid=vdc.getFileInfo("//我的应用//safebox//safedata")
    print(fileid)
    print(vdc.delfile(fileid))
    files={"file":("safedata",open("C://Users//heguofeng//Downloads//t.html", 'rb'))}
    print(vdc.putfile(files))
    #s1=file.read()
    #file.close()
    #files = {'file': ("safedata9",base64.encodebytes(s1))}
    #print(vdc.putfile(files))
    #print(vdc.getfile("safedata8"))
    #vdc.putFileFromData("safedata10", s1)
    
    #713231822902243
    files={"file":("//我的应用//safebox//safedata",open("C://Users//heguofeng//Downloads//t.txt", 'wb'))}
    vdc.getfile(files)
    #s=vdc.getFiletoData("safedata10")
    #s2=base64.decodebytes(s.encode())
    #print(len(s),s)
    #file.write(s.encode())
    #file.close()
    #vdc.postfile()
    
    
    pass