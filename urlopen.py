'''
Created on 2016年4月3日

@author: heguofeng
'''
from _datetime import date
from time import gmtime
'''
Created on 2016年3月30日

@author: heguofeng
'''
import urllib.request  
import hashlib
import hmac
import time
import datetime
import requests
import json
import os.path

#hgf application

AppSecret="68a6d3dd1605f108d627472951f25ef7"
AppId="711690470000250948"
accessToken="a4d0e72c87f0ff741ca11c8c6db9ff0b1460155308624"

'''
app_id:711690470000250948
access_token:a4d0e72c87f0ff741ca11c8c6db9ff0b1460155308624


'''

#http://127.0.0.1/?access_token=a4d0e72c87f0ff741ca11c8c6db9ff0b1460155308624&expires_in=2592000&open_id=1453871169047000025294870&res_code=0&res_message=Success&state=mystate&scope=1

def CloudAuthorize():
    timestamp=str(int(time.time()))
    message="app_id="+AppId+"&timestamp="+timestamp
    appSignature=hmac.new(str.encode(AppSecret),str.encode(message),hashlib.sha1).hexdigest()
    
    #url="http://cloud.189.cn/open/oauth2/authorize.action"
    url="https://oauth.api.189.cn/emp/oauth2/v3/authorize"
    url+="?app_id="+str(AppId)
    url+="&app_secret="+AppSecret
    url+="&redirect_uri="+"http://127.0.0.1/"
    url+="&response_type=token"
    url+="&state=mystate"
    url+="&display=page"
    url+="&scope=1"
 
    #display: default for web,mobile for html5phone
    #responseType: code or token,default is code
    #state 用于保持请求和回调的状态，在 回调时会在Query Parameter中回传该参数 该参数为非必 须
    print(url)
    try:
        getAuthorize=urllib.request.urlopen(str(url))
        #print(getAuthorize.info())
        #print(getAuthorize.code())
        #print(getAuthorize.read().decode("utf8"))
        fd=open("C://Users//heguofeng//Downloads/t.html", 'wb')
        fd.write(getAuthorize.read())
        
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))
        



def CloudAccessToken():
    timestamp=str(int(time.time()))
    #timestamp=str(time.mktime(datetime.datetime.now().timetuple()))
    print((timestamp))
    #AppKey=b"600086127"
    #timestamp=b"1386060076658"
    #AppSecret="dcfc389d74c6a9f437a6fa4972f3ed69"
    message="appKey="+AppId+"&timestamp="+timestamp
    appSignature=hmac.new(str.encode(AppSecret),str.encode(message),hashlib.sha1).hexdigest()
    print(appSignature)
    
    #url="http://cloud.189.cn/open/oauth2/authorize.action"
    url="http://cloud.189.cn/open/oauth2/accessToken.action"
    url=url+"?appKey="+str(AppId)+"&appSignature="+appSignature
    #authorization_code
    url+="&grantType=authorization_code&timestamp="+str(timestamp)
    url+="&code=59046117"
    
    #189_passport
    #url+="&grantType=189_passport&timestamp="+str(timestamp)
    #url+="&account=heguofeng@189.cn"
    
    #url+="&display=default"+"&timestamp="+"&callbackUrl="
    
    print(url)
    try:
        getToken=urllib.request.urlopen(str(url))
        print(getToken.read().decode("utf8"))
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))

#BADC9B24393F2AB867BF9A444EDB22B1  
#08987207

def CloudGetUserInfo():
    #http://api.cloud.189.cn/getUserInfo.action
    
    curdate=time.strftime("%a, %d %b %Y %H:%M:%S GMT",gmtime())
    print(curdate)
    #AccessToken=AFED506D70B5047B4B1BA87CDACF1082&Operate=GET&RequestURI=/getUserInfo.action&Date=Tue, 03 Dec 2013 08:57:48 GMT,
    accessToken="a4d0e72c87f0ff741ca11c8c6db9ff0b1460155308624"
    
    message="AccessToken="+accessToken+"&Operate=GET&RequestURI=/getUserInfo.action"
    message+="&Date="+curdate
    print(message)
    #message="AccessToken=AFED506D70B5047B4B1BA87CDACF1082&Operate=GET&RequestURI=/getUserInfo.action&Date=Tue, 03 Dec 2013 08:57:48 GMT"
    #AppSecret="ebc0a751e9154e5e0b0cd5a13d4bca9b"
    Signature=hmac.new(str.encode(AppSecret),str.encode(message),hashlib.sha1).hexdigest()
    print(Signature)
    
    url="http://api.189.cn/ChinaTelecom/getUserInfo.action"
    #url="http://api.cloud.189.cn/getUserInfo.action"
    payload={"access_token":accessToken,"app_id":AppId}
    headers = {'content-type':'application/json',"Accept":"application/json"}
    r=requests.get(url,params=payload,headers=headers)
    
    print(r.url)
    print( r.status_code)
    print(r.text)
    print(r.headers)
   
    #url="http://api.cloud.189.cn/getUserInfo.action"
    #url+="?AccessToken="+str(accessToken)+"&Signature="+Signature
    #url+="&Date="+str(curdate)
    #display: default for web,mobile for html5phone
    #responseType: code or token,default is code
    #state 用于保持请求和回调的状态，在 回调时会在Query Parameter中回传该参数 该参数为非必 须
    #print(url)
    '''try:
        #getUserInfoRes=urllib.request.urlopen(str(url))
        #print(getAuthorize.info())
        #print(getAuthorize.code())
        #print(getAuthorize.read().decode("utf8"))
        
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))
    '''

def CloudGetFileList(fileid="0",orderBy="filename",pageNum=0,pageSize=20):
    
    url="http://api.189.cn/ChinaTelecom/listFiles.action"
    payload={"access_token":accessToken,
             "app_id":AppId,"folderId":fileid,
             "orderBy":orderBy,
             "pageNum":pageNum,"pageSize":pageSize,
             "descending":"true","fileType":0}
    headers = {'content-type':'application/json',"Accept":"application/json"}
    r=requests.get(url,params=payload,headers=headers)
    
    print(r.url)
    print( r.status_code)
    print(r.text)
    return
   
def CloudGetFolderInfo(fileId="",folderPath="保险箱"):
    
    url="http://api.189.cn/ChinaTelecom/getFolderInfo.action"
    payload={"access_token":accessToken,
             "app_id":AppId,
             "folderId":fileId,
             "folderPath":folderPath}
    headers = {'content-type':'application/json',"Accept":"application/json"}
    r=requests.get(url,params=payload,headers=headers)
    
    print(r.url)
    print( r.status_code)
    print(r.text)
    return



def CloudGetFileInfo(fileId="",filePath="保险箱/test.txt"):
    
    url="http://api.189.cn/ChinaTelecom/getFileInfo.action"
    payload={"access_token":accessToken,
             "app_id":AppId,
             "fileId":fileId,
             "filePath":filePath}
    headers = {'content-type':'application/json',"Accept":"application/json"}
    r=requests.get(url,params=payload,headers=headers)
    
    print(r.url)
    print( r.status_code)
    print(r.text)
    return


def CloudGetFileDownloadUrl(fileId):
    
    url="http://api.189.cn/ChinaTelecom/getFileDownloadUrl.action"
    payload={"access_token":accessToken,
             "app_id":AppId,
             "fileId":fileId,
             "short":"false"}
    headers = {'content-type':'application/json',"Accept":"application/json"}
    r=requests.get(url,params=payload,headers=headers)
    
    print(r.url)
    print( r.status_code)
    print(r.text)
    s=json.loads(r.text)
    print( s.keys())
    for (k,v) in s.items():
        print(k,v)
    return

def CloudGetFile(url):
    
    r=requests.get(url)
    
    print(r.url)
    print( r.status_code)
    print(r.text)
    return 

#http://api.189.cn/ChinaTelecom/getFileUploadUrl.action
def CloudPutFile1(filename):
    files = {'file': open(filename, 'r')}
    filesize=os.path.getsize(filename)
    fd=open(filename, 'r')
    filemd5=hashlib.md5(fd.read().encode()).hexdigest()
    
    
    url="http://api.189.cn/ChinaTelecom/getFileUploadUrl.action"
    payload={"access_token":accessToken,
             "app_id":AppId,
             #"parentFolderId":"",
             #"baseFileId":"",
             #"filename":filename,
             #"size":filesize,
             #"md5":filemd5
             #"lastWrite":"2000-12-12 12:12:12",
             #"localPath":""
             }
    headers = {'content-type':'application/json',"Accept":"application/json"}
    r=requests.get(url,params=payload,headers=headers)   
    rj=r.json()
    print(rj)
   
    fileUploadUrl=rj["FileUploadUrl"]
    
    print(fileUploadUrl)
    
    print(filemd5)
    payload={"access_token":accessToken,
             "app_id":AppId,
             }
    headers = {"Edrive-FileLength":filesize,
               "Edrive-FileName":"safedata.txt",
               "Edrive-FileMD5":filemd5,
               #"Content-Length":1024
               }
    
    r=requests.put(fileUploadUrl,headers=headers,params=payload,files=files)
    print(r.url)
    print(r.request.headers)
    print(r.request.body)
    print(r.status_code)
    print(filesize)
    print(r.url)
    
    print(r.text)
    
  


def CloudPutFile(filename):
    '''http://api.189.cn/ChinaTelecom/createUploadFile.action   获得 uploadFileId
    /v4/uploadFileData.action   //上传
    /v4/commitUploadFile.action?
    '''
    files = {'file': open(filename, 'rb')}
    filesize=os.path.getsize(filename)
    fd=open(filename, 'r')
    filemd5=hashlib.md5(fd.read().encode()).hexdigest()
    
    
    url="http://api.189.cn/ChinaTelecom/createUploadFile.action"
    payload={"access_token":accessToken,
             "app_id":AppId,
             #"parentFolderId":"",
             #"baseFileId":"",
             "filename":filename,
             "size":filesize,
             "md5":filemd5
             #"lastWrite":"2000-12-12 12:12:12",
             #"localPath":""
             }
    headers = {'content-type':'application/json',"Accept":"application/json"}
    r=requests.get(url,params=payload,headers=headers)   
    rj=r.json()
    print(rj)
    uploadFileId=rj["uploadFileId"]
    fileUploadUrl=rj["fileUploadUrl"]
    fileCommitUrl=rj["fileCommitUrl"]
    fileDataExists=rj["fileDataExists"]
    print(uploadFileId,fileUploadUrl,fileCommitUrl,fileDataExists)
    
    print(filemd5)
    payload={"access_token":accessToken,
             "app_id":AppId,
             "uploadFileId":uploadFileId}
    headers = {"Edrive-UploadFileId":uploadFileId,"Edrive-FileLength":filesize,
               "Edrive-FileName":"safedata",
               "Edrive-FileMD5":filemd5
               }
    
    r=requests.put(fileUploadUrl,headers=headers,params=payload,files=files)
    print(filesize)
    print(r.url)
    
    print(r.text)
    
    
    
def getdata():  
    url="http://www.baidu.com"  
    data=urllib.request.urlopen(url).read()  
    print(data.decode('UTF-8'))  
    #print(data)
  
if __name__ == '__main__':
    #CloudAuthorize()
    #CloudGetUserInfo()
    #CloudGetFileList("413651782618293", "lastOpTime", 1, 20)
    #CloudGetFolderInfo()
    #CloudGetFileInfo()
    #CloudGetFileDownloadUrl("913811779498969")
    #CloudGetFile("http://download.cloud.189.cn/v5/downloadFile.action?downloadRequest=1_0024D823C2BEA0FA2663C88EF3CDA771B05CD432D76F59004AEAF5E35B21C6DE01755A7B21070A769033873E933BA10F38AC95C3AC2E0C9E35108C7609BC14B81C8D490AA67427F263A289331523E1453EF615B802550428EEFCCB3F00E986A3EE157D251AA45633C8C2B462C1A7E7CFA7CCF2A2F3222D5146527D0086793D81564E6BF7")   #413651782618293 
    CloudPutFile("C://Users//heguofeng//Downloads//safedata.txt")
    