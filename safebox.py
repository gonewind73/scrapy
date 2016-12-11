'''
Created on 2016年4月8日

@author: heguofeng

数据格式：tag url name password 

流程：
    登录189
    输入保护密码
    获得列表
    显示列表

功能：
    登录,搜索
    加密密码设置/修改
    数据列表
    新增/删除/修改/
    帮助
    
'''
from tkinter import *
import pickle

import tkinter.messagebox
from cloud189Disk import vDiskClient, OAuth2

from Crypto import Random
from Crypto.Cipher import AES
import base64


class record(object):
    Field=['tag','uri','username','password','ref']
    CField=['标记','uri','用户名','密码','备注']
    modified=False
    
    
    #record=('id','tag','uri','username','password','ref')
    def __init__(self,rid="",tag="",uri="",username="",password="",ref=""):
        self.rid=rid
        self.tag=tag
        self.uri=uri
        self.username=username
        self.password=password
        self.ref=ref
        
        
    def get(self):
        record=(self.rid,self.tag,self.uri,self.username,self.password,self.ref)
        return record
    
    def getdict(self):
        return {"rid":self.rid,
                "tag":self.tag,
                "uri":self.uri,
                "username":self.username,
                "password":self.password,
                "ref":self.ref}
    
    def getString(self):
        s= "%5s    %-20s      %-20s" % (self.rid,self.tag,self.uri)
        return s
    
    def set(self,record):
        self.rid=record[0]
        self.tag=record[1]
        self.uri=record[2]
        self.username=record[3]
        self.password=record[4]
        self.ref=record[5]
        
    def update(self):
        self.tag=self.stringVars[0].get()
        self.uri=self.stringVars[1].get()
        self.username=self.stringVars[2].get()
        self.password=self.stringVars[3].get()
        self.ref=self.stringVars[4].get()
        self.modified=True
        #todo save to pickle
        self.popup.destroy()
        return self.get()
    
    def cancel(self):
        self.popup.destroy()
        return
        
    def show(self,root):

        self.popup=tkinter.Toplevel(root)
        self.popup.attributes("-topmost", 1)
        self.popup.title("记录")
        self.popup.focus()
        self.popup.geometry("280x180+500+200")
        #self.popup.positionfrom("program")
        labels=[]
        self.stringVars=[]
        entrys=[]
        for i in range(0,len(self.CField)):
            labels.append(tkinter.Label(self.popup,text=self.CField[i],justify=LEFT))
            self.stringVars.append(StringVar())
            entrys.append(tkinter.Entry(self.popup,name=self.Field[i],width=20,bd=2,font="Arial 16 bold",justify=LEFT,state=NORMAL,textvariable=self.stringVars[i]))

        btnUpdate=tkinter.Button(self.popup,text="确定",command=self.update)
        btnCancel1=tkinter.Button(self.popup,text="取消",command=self.cancel)
        
        for i in range(0,len(self.CField)):
            labels[i].grid(row=i,column=0)
            entrys[i].grid(row=i,column=1)
        
        btnUpdate.grid(row=i+1,column=0)
        btnCancel1.grid(row=i+1,column=1)
        
        self.stringVars[0].set(self.tag)
        self.stringVars[1].set(self.uri)
        self.stringVars[2].set(self.username)
        self.stringVars[3].set(self.password)
        self.stringVars[4].set(self.ref)
        
        '''screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight() - 100    #under windows, taskbar may lie under the screen
        self.popup.resizable(False,False)
        self.popup.deiconify()    #now window size was calculated
        self.popup.withdraw() 
        self.popup.geometry('%sx%s+%s+%s' % (self.popup.winfo_width() + 10, self.popup.winfo_height() + 10, (screen_width - self.popup.winfo_width())/2, (screen_height - self.popup.winfo_height())/2) )    #center window on desktop
        '''
        self.popup.wait_window()
        
        return True
        
class safebook(object):
    #record=('id','tag','uri','username','password','ref')
    #list of record,id don't need encrypt
    
    def __init__(self,key):
        self.recordlist=[]
        #self.securelist=[]
        self.setkey(key)
        
    def new(self):
        self.recordlist.clear()
        self.append(record("safebox","version","1.0","","","0"))
        
    def getid(self):
        re=self.recordlist[0]
        currentid= str(int(re.ref,10)+1)
        re.ref=currentid
        self.recordlist[0]=re
        return currentid
        
    def setkey(self,key):
        self.key=key
        self.aesCipher=AESCipher(key)
        #todo if has data need re-encrpty
        
    def encrypt(self,record):
        #todo 
        srecord=record
        return srecord
    
    def decrypt(self,srecord):
        #todo 
        record=srecord
        return record
        
    def append(self,record):
        #Todo encrypt with self.key
        self.recordlist.append(record)
       
    def getbyid(self,rid):
        
        for i in range(0,len(self.recordlist)):
            if rid==self.recordlist[i].get()[0] :
                record=self.decrypt(self.recordlist[i])
        return record
 
    def get(self,index):
        record=self.decrypt(self.recordlist[index+1])
        return record   
    
    def deletebyid(self,rid):
        for i in range(0,len(self.recordlist)):
            if rid==self.recordlist[i].get()[0]:
                del self.recordlist[i]
                return True
        return False
    
    def delete(self,index):
        del self.recordlist[index+1]
        return


        
    def setbyid(self,rid,record):   
        for i in range(0,len(self.recordlist)):
            if rid==self.recordlist[i].get()[0]:
                #todo encrypt
                self.recordlist[i]=self.encrypt(record)
                return self.recordlist[i]
        return NONE

    def set(self,index,record):   
        self.recordlist[index+1]=self.encrypt(record)
        return 
     
        
    def len(self):
        return len(self.recordlist)-1

    def savetobyte(self):
        d=[]
        for i in range(0,len(self.recordlist)):
            r=self.recordlist[i].get()
            d.append(r)
        return pickle.dumps(d)
        
    def save(self):
        data=self.savetobyte()
        file=open('C:\\Users\\heguofeng\\Downloads\\data.pkl', 'wb')
        file.write(data)
        file.close()
        
    def saveToEncryptByte(self):
        data=self.savetobyte()
        return self.aesCipher.encrypt(data)
      
    def load(self):
        file=open('C:\\Users\\heguofeng\\Downloads\\data.pkl1', 'rb')
        s=file.read()
        #print(s)
        self.loadsfrombytes(s)
        file.close()
        
    def loadsfrombytes(self,s):
        
        d=pickle.loads(s)
        self.recordlist.clear()
        for i in range(0,len(d)):
            re=record()
            re.set(d[i])
            self.recordlist.append(re)
            
    def loadFromEncrptedBytes(self,encrpted):
        raw=self.aesCipher.decrypt(encrpted)
        return self.loadsfrombytes(raw)
        
            
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()
unpad = lambda s : s[0:-(s[-1])]


class AESCipher:

    def __init__( self, key ):      
        self.key = pad(key.encode())
        #print(self.key)

    def encrypt( self, raw ):
        raw = pad(raw)
        #print(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        data=cipher.decrypt( enc[16:] )
        #print(data)
        return unpad(data)    
     

class safebox():
    top = tkinter.Tk()
    values=[]
    entrylist=[]
    buttonlist=[]
    logon=FALSE
    
    def __init__(self):
        self.safebook=safebook("")
        #self.safebook.append(record("safebox","version","1.0","","","1"))
        #self.safebook.append(record("1","sina","www.sina.com.cn","heguofeng","password","none"))
        #self.safebook.load()
        
    
    def SafeBoxUI(self):

        self.top.title("密码保险箱 --新浪微盘加密存储 @2016  何国锋")
        self.top.geometry("465x290+500+200")
        labelframe = tkinter.LabelFrame(self.top,text="")
        svSearch=StringVar()
        entry=tkinter.Entry(labelframe,name="searchitem",width=35,bd=2,font="Arial 16 bold",justify=LEFT,state=NORMAL,textvariable=svSearch)
        self.searchbutton=tkinter.Button(labelframe,text="搜索",state=DISABLED,command=self.search)
        labelframe.pack(fill=X )
        entry.pack(side=LEFT)
        self.searchbutton.pack(side = RIGHT )
        
        middleframe= tkinter.LabelFrame(self.top,text="欢迎使用密码保险箱 ！\n序号      标记                                URL  ")
        middleframe.pack(fill=X)

        scrollbar = tkinter.Scrollbar(middleframe)
        scrollbar.pack( side = RIGHT, fill=Y )
        self.mylist = Listbox(middleframe, yscrollcommand = scrollbar.set,width=63 )
        for i in range(0,self.safebook.len()):
            self.mylist.insert(END, self.safebook.get(i).getString())
        
        self.mylist.pack( side = LEFT, fill = BOTH )
        scrollbar.config( command =self.mylist.yview )

        bottomframe=tkinter.Frame(self.top)
        bottomframe.pack(fill=X)
        
        self.addbutton=tkinter.Button(bottomframe,text="新增",state=DISABLED,command=self.add)
        self.addbutton.grid(row=0,column=0,padx=20)
        self.delbutton=tkinter.Button(bottomframe,text="删除",state=DISABLED,command=self.delete)
        self.delbutton.grid(row=0,column=1,padx=20)
        self.modifybutton=tkinter.Button(bottomframe,text="修改",state=DISABLED,command=self.modify)
        self.modifybutton.grid(row=0,column=2,padx=20)       
        self.loginbutton=tkinter.Button(bottomframe,text="登录",command=self.loginShow)
        self.loginbutton.grid(row=0,column=4,padx=20)       
        self.savebutton=tkinter.Button(bottomframe,text="保存",state=DISABLED,command=self.save)
        self.savebutton.grid(row=0,column=5,padx=20)       
        b6=tkinter.Button(bottomframe,text="帮助",command=self.help)
        b6.grid(row=0,column=6,padx=20)          #b5.tkinter.Entry()
        
        
        self.top.mainloop()
        return  
    
    def refresh(self,index):  
        self.mylist.delete(0, END)
        for i in range(0,self.safebook.len()):
            self.mylist.insert(END, self.safebook.get(i).getString())
        self.mylist.select_set(index)
    
    def run(self):
        self.SafeBoxUI()
        return 
       
    def add(self):
        re=record(self.safebook.getid())
        re.show(self.top)
        
        if re.modified:   
            #self.mylist.insert(END,re.getString())
            self.safebook.append(re)
            self.refresh(END)
            
            #self.safebook.save()
        return
            
    def modify(self):
        index=self.mylist.curselection()
        #print(index)
        re=self.safebook.get(index[0])   # 0 is version line
        #print(re.getString())
        re.show(self.top)
        
        if re.modified:   
            #self.mylist.delete(index[0])
            #self.mylist.insert(index[0],re.getString())
            self.safebook.set(index[0],re)
            self.refresh(index[0])
            #self.safebook.save()
        return
    
    def delete(self):
        index=self.mylist.curselection()
        #print(index)
        re=self.safebook.get(index[0])   # 0 is version line
        #print(re.getString())
        if tkinter.messagebox.askokcancel("确认", "你确定要删除吗？"):
            #self.mylist.delete(index[0])
            self.safebook.delete(index[0])
            self.refresh(index[0])
            
            #self.safebook.save()
        return
    
    def load(self):
        data=self.vdc.getFiletoData("safedata.dat")  #get pikle then display in lists
        #print(data)
        if data=="":
            if tkinter.messagebox.askokcancel("确认", "是否创建密码本？"):
                self.safebook.new()
        else :
            self.safebook.loadFromEncrptedBytes(data)
        return
        
    def save(self):
        if self.logon:
            enc=self.safebook.saveToEncryptByte()
            self.vdc.putFileFromData("safedata.dat", enc)
        else:
            tkinter.messagebox.showinfo("信息", "请先登录！")
        return
    
    def search(self):
       
        return
    
    def help(self):
        tkinter.messagebox.showinfo("信息", "欢迎使用密码保险箱！\n Version 1.0 \n By heguofeng@189.cn\n\n一定要记住保险箱密码，没有密码无法打开密码本！")
        return
    

    def loginShow(self):
        if not self.logon: 
            self.loginUI(self.top)
                  
    
    def loginUI(self,root):
        Field=['username','password','secret']
        CField=['用户名','密码','保险密钥']
       

        #self.popup=tkinter.Tk()
        self.loginPopup=tkinter.Toplevel(root)
        self.loginPopup.attributes("-topmost", 1)
        self.loginPopup.title("登录")
        self.loginPopup.geometry("300x130+500+200")
        self.loginPopup.focus()
        #self.popup.positionfrom("program")
        labels=[]
        self.LoginStringVars=[]
        entrys=[]
        for i in range(0,len(CField)):
            labels.append(tkinter.Label(self.loginPopup,text=CField[i],justify=LEFT))
            self.LoginStringVars.append(StringVar())
            entrys.append(tkinter.Entry(self.loginPopup,name=Field[i],width=20,bd=2,font="Arial 16 bold",justify=LEFT,state=NORMAL,textvariable=self.LoginStringVars[i]))
        
        entrys[1]['show']="*"
        entrys[2]['show']="*"
        btnLogin=tkinter.Button(self.loginPopup,text="登录",command=self.login)
        btnCancel1=tkinter.Button(self.loginPopup,text="取消",command=self.cancel)
        
        for i in range(0,len(CField)):
            labels[i].grid(row=i,column=0)
            entrys[i].grid(row=i,column=1)
        
        btnLogin.grid(row=i+1,column=0,padx=30)
        btnCancel1.grid(row=i+1,column=1,padx=30)
        
        
        self.loginPopup.wait_window()
        
        return True
    
    def login(self):
        
        username=self.LoginStringVars[0].get()
        password=self.LoginStringVars[1].get()
        secret=self.LoginStringVars[2].get()
        if username=="" or password=="" or secret=="":
            tkinter.messagebox.showinfo("信息", "请输入用户名\密码和密钥")
            return
        
        #SinaDisk
        #self.AppKey="2713303872"
        #self.SecretKey="0f86520e84849ef4d2df5879657159c6"
        
        #cloud189Disk
        self.SecretKey="93c6a3491a5e1d93af0e44b470798148"
        self.AppKey="600102343"
        self.loginPopup.destroy()
        try:
            self.oauth2=OAuth2(self.AppKey,self.SecretKey,"http://127.0.0.1") 
            accesstoken=self.oauth2.autologin(username, password)
            self.vdc=vDiskClient()  
            if self.vdc.setAccessToken(accesstoken):
                self.safebook.setkey(secret)
                self.load()
                self.refresh(0)
                self.logon=True
                self.loginbutton['state']=DISABLED
                self.addbutton['state']=NORMAL
                self.modifybutton['state']=NORMAL
                self.delbutton['state']=NORMAL
                self.savebutton['state']=NORMAL
                self.searchbutton['state']=NORMAL
        except:
            tkinter.messagebox.showerror("出错了！", "请检查用户名\密码和密钥")
            
            #print(self.vdc.getUserInfo())
        
        #self.aesCipher=AESCipher(secret)
        return
    
    def cancel(self):
        
        self.loginPopup.destroy()
        return
   
        

if __name__ == '__main__':
    sf=safebox()
    sf.run()
    f=open("C:\\Users\\heguofeng\\Downloads\\data.pkl","rb")
    d=f.read()
    
    
    pass


'''
checkboxframe=tkinter.LabelFrame(middleframe,text="")
checkboxframe.pack(side=LEFT,fill=Y,expand=YES)
for i in range(0,11):
    tkinter.Checkbutton(checkboxframe).pack()
    
middlerightframe=tkinter.LabelFrame(middleframe,text="")
middlerightframe.pack(side=RIGHT)

contentframe=tkinter.Frame(middlerightframe)
contentframe.pack(side=LEFT)
l1=tkinter.Label(contentframe,text="欢迎使用！",justify=LEFT)
l1.grid(row=0,column=0)
for i in range(0,40):
    self.values.append(StringVar())
    self.values[i].set(str(i))
    if (i//4)%2==0:
        bgcolor="#d0ffff"
    else:
        bgcolor="#ffd0d0"
    self.entrylist.append(tkinter.Entry(contentframe,name=str(i),width=10,bd=2,font="Arial 16 bold",justify=LEFT,state=NORMAL,textvariable=self.values[i]))
    #self.entrylist[i].bind('<Tab>', self.valuechanged)
j=0
for item in self.entrylist:    
    item.grid(row=j//4+1,column=j%4)
    #item.pack(side=LEFT)
    j+=1


 
scrollframe=tkinter.Frame(middlerightframe)
scrollframe.pack(side=RIGHT,fill=Y)
tkinter.Scrollbar(scrollframe).pack(fill=Y,expand=YES)
'''