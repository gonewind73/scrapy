#!/usr/bin/env python
# encoding: utf-8
# author: heguofeng
# sina weipan openapi 

import time
import requests
import rsa
import re
import json
import binascii 
import base64
from dropbox.oauth import ProviderException

class OAuth2(object):
    Provider="SinaDisk"
    ACCESS_TOKEN_URL = "https://auth.sina.com.cn/oauth2/access_token"
    AUTHORIZE_URL = "https://auth.sina.com.cn/oauth2/authorize"
    AccessToken=""

    def __init__(self,app_key, app_secret, call_back_url):
        self.version = 1.0
        self.app_key = app_key
        self.app_secret = app_secret
        self.call_back_url = call_back_url
        self.app_key="2713303872"
        self.app_secret="0f86520e84849ef4d2df5879657159c6"
        
    #display = default|mobile|popup
    def authorize(self,response_type = "code",display = "default",state = ""):
        querystring = {"client_id":self.app_key,
                "redirect_uri":self.call_back_url,
                "response_type":response_type,
                "display":display}
        if len(state) > 0:
            querystring["state"] = state
        #return OAuth2.AUTHORIZE_URL + "?" + urllib.urlencode(data)
        return querystring
    
    #grant_type = authorization_code|refresh_token
    def access_token(self,grant_type = "authorization_code",code = "",refresh_token = ""):
        querystring = {"client_id":self.app_key,
                       "client_secret":self.app_secret,
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
        1、https://auth.sina.com.cn/oauth2/authorize?client_id=2713303872&redirect_uri=http://127.0.0.1/&response_type=token
        #Get 获得表单，包含一些随机数，后续在提交时需要用到
        
        2、https://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.15)&_=1460814917309
        #Get 获得服务器时间，随机数和服务器公钥及标识 
        #其中 _:为时间戳  int(time.time()*1000)
        #返回：
        sinaSSOController.preloginCallBack({
            "retcode": 0,
            "servertime": 1460814008, 
            "pcid": "gz-98988756a179ae3b1e8c80591022d5254d65",
            "nonce": "7R1PIL",
            "pubkey": "EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443",
            "rsakv": "1330428213",
            "exectime": 11
        })
        
        3、https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)&_=1460814928223
        #POST 登录 
        #其中 _:为时间戳  int(time.time()*1000)
        #FORM：
    
        sp: 
        entry:sinaoauth
        gateway:1
        from:
        savestate:0
        useticket:1
        pagerefer:
        vsnf:0
        s:1
        su: base64.b64encode(username)  #base编码用户名      
        service:sinaoauth
        servertime:1460814927   #2中返回
        nonce:H6PCNW            #2中返回
        pwencode:rsa2
        rsakv:1330428213        #2中返回
        sp:   rsa.encrypt(servertime&nonce&password,rsaPublicKey #加密密码
        sr:1366*768   
        encoding:UTF-8
        cdult:2
        domain:sina.com.cn
        prelt:39
        returntype:TEXT
        
        #返回 ticket
         {
            "retcode": "0",
            "ticket": "ST-MTE5MTQ5ODk0MQ==-1460862441-gz-0E0539C8D74CA99CB792F9482F14543E",
            "uid": "1191498941",
            "nick": "宁静思远-_-",
            "crossDomainUrlList": [
                "https://passport.weibo.com/wbsso/login?ticket=ST-MTE5MTQ5ODk0MQ%3D%3D-1460862441-gz-B9C5F8183CAA82721A066C313DE32756&ssosavestate=1460862441",
                "https://crosdom.weicaifu.com/sso/crosdom?action=login&savestate=1460862441",
                "https://passport.weibo.cn/sso/crossdomain?action=login&savestate=1"
            ]
        }
        
        4、https://auth.sina.com.cn/oauth2/authorize 
        POST 提交认证表单
        form：
        client_id:2713303872
        response_type:token
        redirect_uri:http://127.0.0.1/
        state:
        display:default
        0f6406ea4477d97e9298928015337a84:017e5f5ae6edff7ca0a1e6a4bc8b2601
        9f830b5f8c88f59d9e436eb4a2eb56ff:7a223b0d58b4fa23e6508b47f000f884
        77b5abedcd757126e756a9a3431cb02f:ab6c04517cac1a7cbe8df6e6d6fd6b95
        28e61972318fe4741b34292106dd5199:babaedf4ba803a6b6a358a88f27ad15d
        c54830f9a85cf15f0f81c2ae0cb936a8:47b8f656a368ed90eac7b0c4679da502
        f886be94bea700f722530bcef78a3162:8e46b8ab072160147397c1f384c8374b
        0fda1891942ecc2ebec9c84914c9df39:0573c5fafedc6d39d678e059633efae1
        regtime:1460851922
        57f3daa73501e674fda866036a0c6afc:14
        userid:gonewind73
        password:hgf020613
        ticket:ST-MTE5MTQ5ODk0MQ==-1460851937-gz-83F18D0210BFBD398FF6FA2404DEA2DF
        
        #返回 refreshurl，获得AccessToken
        
        '''
    
        
    def autologin(self,username,password):
        
        authorform=self.getAuthorizeform()
        
        url="https://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.15)&_="
        url+=str(int(time.time()*1000))
        #print(url)
        response=requests.get(url)
        #print(response.text)
        match=re.findall(r'(\{.*\})',response.text)
        #print((match[0]))
        params=json.loads(match[0])
        
        url="https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)&_="
        url+=str(int(time.time()*1000))
        #print(url)
        securepassword=self.get_pwd(password,params["servertime"],params["nonce"],params["pubkey"])
        #securepassword="35bd9ce436a648c40daa506ee35550011e24fb6f04e4fbf941a1b213c2888fea2b44d4e1830fb3f261956b16faebe7b5fa90c9de729e04b7aec3ee4b1d6499e2718fd5982baa84420012f4bf7eed8786a31477030bd3383a229fb1fe4bbdd760834f9e27676b94d847015b5b09d769f5fb1d6755118e098488686eed41f4cd8a"
        data={
              "entry":"sinaoauth",
              "gateway":1,
              "from":"",
              "savestate":0,
              "useticket":1,
                "pagerefer":"",
                "vsnf":0,
                "s":1,
                "su":base64.b64encode(username.encode("utf-8")),
                "service":"sinaoauth",
                "servertime":params["servertime"],
                "nonce":params["nonce"],
                "pwencode":"rsa2",
                "rsakv":params["rsakv"],
                "sp":securepassword,
                "sr":"1366*768",
                "encoding":"UTF-8",
                "cdult":2,
                "domain":"sina.com.cn",
                "prelt":39,
                "returntype":"TEXT",
              }
        #print(data["su"])
        #print(data["sp"])
        response=requests.post(url,data=data)
        params2=response.json()
        
        #print(response.text)
        
        #for u in params2["crossDomainUrlList"]:
        #    print(u)
        #    requests.get(u)

        url="https://auth.sina.com.cn/oauth2/authorize"
        data2={
               "client_id":self.app_key,
               "response_type":"token",
               "redirect_uri":self.call_back_url,
               "state":"",
               "display":"default",
                "userid":username,
                "password":password,
                "ticket":params2["ticket"],
                }
        
        authorform.update(data2)
        response=requests.post(url,data=authorform)
        #print(response.request.body)
        #print(response.headers)
        param3=response.headers
        #print(param3["Refresh"])
        result=re.findall(r'(?<=access_token\=)[\w]*(?=\&)',param3["Refresh"])
        self.AccessToken=result[0]
        print(self.AccessToken)
        return(self.AccessToken)
        
    def getAuthorizeform(self):
        authorizeformdata={}
        response=requests.get(self.AUTHORIZE_URL,params=self.authorize("token"))
        html=response.text
        #print(html)
        result=re.findall(r'(?<=input\stype\=\"hidden\"\sname\=\")[^<,^>]*(?=\"\>)',html)
        #print(result)
        for r in result:
            kv=re.split(r'\"\svalue\=\"',r)
            authorizeformdata[kv[0]]=kv[1]
        
        #print(authorizeformdata)
        return authorizeformdata
    
    def get_pwd(self, password, servertime, nonce, pubkey):  
        rsaPublickey = int(pubkey, 16)  
        key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥  
        #print(key)
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password) #拼接明文js加密文件中得到  
        #print(message)
        passwd = rsa.encrypt(message.encode("utf-8"), key) #加密  
        #print(message.encode("utf-8"))
        #print(passwd)
        passwd = binascii.b2a_hex(passwd) #将加密信息转换为16进制。  
        return passwd   
    



"""
The vdisk(weipan) client.
"""

class vDiskClient(object):
    
    AccessToken = ""

    def __init__(self):
        pass
    
    def setAccessToken(self,token):
        #self.AccessToken = "fe34416661iDpiR2XCKhG1HxVLR4166e"
        if token!="":
            self.AccessToken = token
            return True
        return False
    
        
    
    def getUserInfo(self):
        url="https://api.weipan.cn/2/account/info"
        payload={"access_token":self.AccessToken}
        headers = {'content-type':'application/json',"Accept":"application/json"}
        r=requests.get(url,params=payload,headers=headers)
        return(r.json())
       
        
    def metadata(self):
        #https://api.weipan.cn/2/metadata/<root>/<path> 
        url="https://api.weipan.cn/2/metadata/sandbox/"
        payload={"access_token":self.AccessToken}
        headers = {'content-type':'application/json',"Accept":"application/json"}
        r=requests.get(url,params=payload,headers=headers)
        #print(r.json())
        return(r.json())
        
    
    def isExist(self):
        #https://api.weipan.cn/2/search/sandbox?access_token=b8a7e96661iDpiR2XCKhG1HxVLRe9cec&query=safedata
        return True
    
    def createFolder(self,foldername):
        # https://api.weipan.cn/2/fileops/create_folder
        url="https://api.weipan.cn/2/fileops/create_folder"
        querystring={"access_token":self.AccessToken
                     }
        headers = {
                   'cache-control': "no-cache"
                   }
        # files = {'name': (<filename>, <file object>,<content type>, <per-part headers>)}
        # Content-Disposition: form-data; name=’name’;filename=<filename>
        # Content-Type: <content type>
        # <file object>
        #--boundary 
        #just for multipart / form-data
        files={'root':(None,'sandbox'),
               'path':(None,foldername),
               }
        response=requests.post(url,params=querystring,headers=headers,files=files)        
      
        return(response.json())
                    
        
    def putfile(self,files):
        #PUT http://upload-vdisk.sina.com.cn/2/files_put/<root>/<path> 
        url="http://upload-vdisk.sina.com.cn/2/files_put/sandbox/"+files["file"][0]
        #url="http://api.cloud.189.cn/getUserInfo.action"
        querystring={"access_token":self.AccessToken,
                 
                 }
        
       
        r=requests.put(url,params=querystring,files=files)
           
        return(r.json())

    def putFileFromData(self,filename,data):
        #PUT http://upload-vdisk.sina.com.cn/2/files_put/<root>/<path> 
        url="http://upload-vdisk.sina.com.cn/2/files_put/sandbox/"+filename
        #url="http://api.cloud.189.cn/getUserInfo.action"
        querystring={"access_token":self.AccessToken,
                 
                 }
        #b64=base64.encodebytes(data)
        files = {'file': (filename,data)}
       
        r=requests.put(url,params=querystring,files=files)
           
        return(r.json())    
    
    def getfile(self,files):
        #GET https://api.weipan.cn/2/files/<root>/<path> 
        #files = {"file":(cloudfilename,fopenhandle)}
        url="https://api.weipan.cn/2/files/sandbox/"+files["file"][0]
        #url="http://api.cloud.189.cn/getUserInfo.action"
        querystring={"access_token":self.AccessToken,
                 }       
        r=requests.get(url,params=querystring)
        #print(r.headers)
        file=files["file"][1]
        len=file.write(self.getDataFromMime(r.text))
        file.close()
        
        return len
    
    def getFiletoData(self,filename):
        #GET https://api.weipan.cn/2/files/<root>/<path> 
        url="https://api.weipan.cn/2/files/sandbox/"+filename
        #url="http://api.cloud.189.cn/getUserInfo.action"
        querystring={"access_token":self.AccessToken,
                 }       
        r=requests.get(url,params=querystring)
        #print(r.headers)
        
        #return base64.decodestring(self.getDataFromMime(r.text).encode())
        return self.getDataFromMime(r.text)
    
    def getDataFromMime(self,s):
        datas=re.findall(r'(?<=\r\n\r\n)[\s\S]*(?=\r\n\-\-)',s)
        #print(datas)
        
        return datas[0]
            
    def postfile(self):
        #http://upload-vdisk.sina.com.cn/2/files/<root>/<path>
        url="http://upload-vdisk.sina.com.cn/2/files/sandbox/"
        #url="http://api.cloud.189.cn/getUserInfo.action"
        payload={"access_token":self.AccessToken,
                 "path":"",
                 "overwrite":"true"
                 }
        files = {'file': open("C://Users//heguofeng//Downloads//safedata.txt", 'rb')}
        #print(files)
       
        r=requests.post(url,params=payload,files=files)
        #print(r.url)
        #print(r.request.headers)
        #print(r.request.body)
        #print(r.status_code)

        #print(r.url)
        
        #print(r.text)
        
if __name__ == '__main__':
    
    AppKey="2713303872"
    SecretKey="0f86520e84849ef4d2df5879657159c6"
    oauth2=OAuth2(AppKey,SecretKey,"http://127.0.0.1")
    #querystring=oauth2.authorize("token")
    #r=requests.get(OAuth2.AUTHORIZE_URL,params=querystring)
    #sp=oauth2.get_pwd("hgf020613", "1460850054", "3ROJWU", "EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443")
    #print(sp)
    #oauth2.getAuthorizeform()
    accesstoken=oauth2.autologin("gonewind73", "hgf020613")
    
    vdc=vDiskClient()
    vdc.setAccessToken(accesstoken)
    #print(vdc.getUserInfo())
    print(vdc.metadata())
    #ct,b=vdc.encode_multipart_formdata({"data":"date"}, [])
    #print(ct,b)
    #print(vdc.createFolder("safebox9"))
    file=open("C://Users//heguofeng//Downloads//data.pkl", 'rb')
    s1=file.read()
    file.close()
    #files = {'file': ("safedata9",base64.encodebytes(s1))}
    #print(vdc.putfile(files))
    #print(vdc.getfile("safedata8"))
    vdc.putFileFromData("safedata10", s1)
    file=open("C://Users//heguofeng//Downloads//data.pkl1", 'wb')
    s=vdc.getFiletoData("safedata10")
    #s2=base64.decodebytes(s.encode())
    print(len(s),s)
    file.write(s.encode())
    file.close()
    #vdc.postfile()
    
    
    '''    
    def encode_multipart_formdata(self, fields, files):
        
        #fields is a sequence of (name, value) elements for regular form fields.
        #files is a sequence of (name, filename, value) elements for data to be uploaded as files
        #Return (content_type, body) ready for httplib.HTTP instance
        
        BOUNDARY = '----------%s' % hex(int(time.time() * 1000))
        CRLF = '\r\n'
        L = []
        for key in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % str(key))
            L.append('')
            L.append(fields[key])
            
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (str(key), str(filename)))
            L.append('Content-Type: %s' % str(self.get_content_type(filename)))
            L.append('Content-Length: %d' % len(value))
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')

        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body
        '''


"""
class Client(object):
    log = logging.getLogger('api_client')
    API_URL = 'https://api.weipan.cn/2/'
    WEIBO_URL = 'https://api.weipan.cn/weibo/'
    UPLOAD_HOST = 'upload-vdisk.sina.com.cn'
    CONTENT_SAFE_URL = 'https://'+UPLOAD_HOST+'/2/'
    version = 1.0

    def __init__(self,root = "basic"):
        self.timeout = 10
        self.python_version_is_bigger_than_2_4 = float(sys.version[:3]) > 2.4
        self.root = root

    def setRoot(self,root):
        self.root = root

    def get(self, host, api, queries={}):
        try:
            '''
            if isinstance(api, unicode):
                api = api.encode('utf-8')
            else:
                api = str(api)
            '''
            url=host+api
            r=requests.get(url,payload=queries)
            return(r.text)
            '''
            url = host.strip('/') + '/' + urllib.quote(api.strip('/'))
            queries = self.encode_queries(queries)
            request = urllib2.Request('%s?%s' % (url, queries))
            # set timeout.
            if self.python_version_is_bigger_than_2_4:
                response = urllib2.urlopen(request, timeout=self.timeout)
            else:
                # http://stackoverflow.com/questions/2084782/timeout-for-urllib2-urlopen-in-pre-python-2-6-versions
                import socket
                socket.setdefaulttimeout(self.timeout)
                response = urllib2.urlopen(request)
            return Response(response)
        except e:
            return e.read()
            '''
        

    def post(self, host, api, data=[], files=[]):
        try:
           url=host+api
            r=requests.post(url,payload=queries)
            return(r.text)
            if isinstance(data, dict):
                data = data.items()
            content_type, body = self.encode_multipart_formdata(data, files)
            request = urllib2.Request(url, data=body)
            request.add_header('Content-Type', content_type)
            request.add_header('Content-Length', str(len(body)))
            if self.python_version_is_bigger_than_2_4:
                response = urllib2.urlopen(request, timeout=self.timeout)
            else:
                import socket
                socket.setdefaulttimeout(self.timeout)
                response = urllib2.urlopen(request)
            return Response(response)
        
        except e:
            return e.read()
    # used by non GET or POST method. such as PUT
    def request(self, method,host, api, data, headers = {}, use_safe = True):
        import httplib
        if isinstance(api, unicode):
            api = api.encode('utf-8')
        else:
            api = str(api)
        if isinstance(data, dict):
            data = self.encode_queries(data)
        try:
            if use_safe:
                conn = httplib.HTTPSConnection(host)
            else:
                conn = httplib.HTTPConnection(host)
            conn.request(method,api,data,headers)
            return Response(conn.getresponse())
        except e:
            print(e)
            return e.read()

    def get_content_type(self, filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    def encode_multipart_formdata(self, fields, files):
        
        #fields is a sequence of (name, value) elements for regular form fields.
        #files is a sequence of (name, filename, value) elements for data to be uploaded as files
        #Return (content_type, body) ready for httplib.HTTP instance
        
        BOUNDARY = '----------%s' % hex(int(time.time() * 1000))
        CRLF = '\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % str(key))
            L.append('')
            if isinstance(value, unicode):
                L.append(value.encode('utf-8'))
            else:
                L.append(value)
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (str(key), str(filename)))
            L.append('Content-Type: %s' % str(self.get_content_type(filename)))
            L.append('Content-Length: %d' % len(value))
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')

        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body

    def encode_queries(self, queries={}, **kwargs):
        queries.update(kwargs)
        args = []
        for k, v in queries.iteritems():
            if isinstance(v, unicode):
                qv = v.encode('utf-8')
            else:
                qv = str(v)
            args.append('%s=%s' % (k, urllib.quote(qv)))
        return '&'.join(args)

    def account_info(self,access_token):
        data = self.get(Client.API_URL,
                        'account/info',
                        {"access_token":access_token})
        return data

    def metadata(self,access_token,path):
        data = self.get(Client.API_URL,
                        'metadata/' + self.root + '/' + path,
                         {"access_token":access_token})
        return data

    def delta(self,access_token,cursor = ''):
        param = {"access_token":access_token}
        if len(cursor) > 0:
            param['cursor'] = cursor
        data = self.get(Client.API_URL,
                        'delta/' + self.root,
                         param)
        return data

    def files(self,access_token,path,rev = ''):
        param = {"access_token":access_token}
        if len(rev) > 0:
            param['rev'] = rev
        data = self.get(Client.API_URL,
                        'files/' + self.root + "/" + path,
                         param)
        return data

    def revisions(self,access_token,path):
        data = self.get(Client.API_URL,
                        'revisions/' + self.root + "/" + path,
                         {"access_token":access_token})
        return data
    #files = {"filename":filename,"content":"file content"}
    def files_post(self,access_token,path,files,overwrite = "true",sha1 = "",size = "", parent_rev = ""):
        param = {
                 "access_token":access_token,
                 "overwrite":overwrite
                 }
        if len(sha1) > 0:
            param["sha1"] = sha1
        if len(size) > 0:
            param["size"] = size
        if len(parent_rev) > 0:
            param["parent_rev"] = parent_rev
        queries = self.encode_queries(param)
        data = self.post(Client.CONTENT_SAFE_URL,
                        'files/'+self.root+"/"+path+"?"+queries,
                         [],
                         [("file",files["filename"],files["content"])])
        return data
    
    #content should be a file object or file raw content, such as: open("./filename","rb"), "rb" is prefered.
    
    def files_put(self,access_token,path,content,overwrite = "true",sha1 = "",size = "", parent_rev = ""):
        param = {
                 "access_token":access_token,
                 "overwrite":overwrite
                }
        if len(sha1) > 0:
            param["sha1"] = sha1
        if len(size) > 0:
            param["size"] = size
        if len(parent_rev) > 0:
            param["parent_rev"] = parent_rev
        data = self.request(
                        method="PUT",
                        host=Client.UPLOAD_HOST,
                        api='/2/files_put/'+self.root+"/"+path+"?"+self.encode_queries(param),
                        data=content)
        return data
    # 公开分享
    def shares(self,access_token,path,cancel = "false"):
        data = self.post(Client.API_URL,
                        'shares/'+self.root+"/"+path,
                         {"access_token":access_token,
                          "cancel":cancel
                          })
        return data

    def restore(self,access_token,path,rev = ""):
        param = {"access_token":access_token,
                 "path":path
                }
        if len(rev) > 0:
            param['rev'] = rev
        data = self.post(Client.API_URL,
                         'restore/'+self.root+"/"+path,
                         {"access_token":access_token})
        return data

    def search(self,access_token,path,query,file_limit = 1000,include_deleted = "false"):
        data = self.get(Client.API_URL,
                        'search/'+self.root+"/"+path,
                         {"access_token":access_token,
                          "path":path,
                          "query":query,
                          "file_limit":file_limit,
                          "include_deleted":include_deleted
                          })
        return data

    def copy_ref(self,access_token,path):
        data = self.post(Client.API_URL,
                         'copy_ref/'+self.root+"/"+path,
                          {"access_token":access_token,
                           "path":path})
        return data

    def media(self,access_token,path):
        data = self.get(Client.API_URL,
                        'media/'+self.root+"/"+path,
                         {"access_token":access_token,
                          "path":path})
        return data
    #s:60x60,m:100x100,l:640x480,xl:1027x768
    def thumbnails(self,access_token,path,size):
        data = self.get(Client.API_URL,
                        'thumbnails/'+self.root+"/"+path,
                         {"access_token":access_token,
                          "path":path,
                          "size":size})
        return data

    def fileops_copy(self,access_token,to_path,from_path = "",from_copy_ref = ""):
        param = {"access_token":access_token,
                 "root":self.root,
                 "to_path":to_path
                }
        if len(from_path) > 0:
            param['from_path'] = from_path
        if len(from_copy_ref) > 0:
            param['from_copy_ref'] = from_copy_ref
        data = self.post(Client.API_URL,
                         'fileops/copy',
                         param)
        return data

    def fileops_delete(self,access_token,path):
        data = self.post(Client.API_URL,
                         'fileops/delete',
                         {"access_token":access_token,
                          "root":self.root,
                          "path":path
                          })
        return data

    def fileops_move(self,access_token,from_path = "",to_path = ""):
        param = {"access_token":access_token,
                 "root":self.root
                 }
        if len(from_path) > 0:
            param['from_path'] = from_path
        if len(to_path) > 0:
            param['to_path'] = to_path
        data = self.post(Client.API_URL,
                         'fileops/move',
                         param)
        return data

    def fileops_create_folder(self,access_token,path):
        data = self.post(Client.API_URL,
                         'fileops/create_folder',
                         {"access_token":access_token,
                          "root":self.root,
                          "path":path
                          })
        return data

    def shareops_media(self,access_token,from_copy_ref):
        data = self.get(Client.API_URL,
                        'shareops/media', 
                        {"access_token":access_token,
                         "from_copy_ref":from_copy_ref})
        return data

"""
