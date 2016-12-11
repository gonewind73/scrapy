'''
Created on 2016年7月22日

@author: heguofeng

todo:改成event模式 7.22 
'''
from _overlapped import NULL
class room(object):
    roomid=""
    def __init__(self,roomid="",users=[],messages=[],roomsize=2):
        self.roomid=roomid[:]
        self.roomsize=roomsize
        self.users=users[:]
        self.messages=messages[:]
        self.messageids=[]
        self.currentid=0
        
    def getroomid(self):
        return self.roomid
    
    def subscribe(self,user):
        if(len(self.users)>self.roomsize-1):
            return False
        self.users.append(user)
        
    def unsubscribe(self,user):
        self.users.remove(user)
        
    def publish(self,message):
        self.messages.append(message)
        self.messageids.append(str(self.currentid))
        self.currentid+=1
        
        
    def getmessage(self,index=0):        
        if((len(self.messages))>0):
            message=(self.messages[0])[:]
            messageid=(self.messageids[0])[:]
            #print("getmessage 1")
            #print(message)
            return(message,messageid)
        return("","0")
    
    def delmessage(self,messageid):
        try:
            index=self.messageids.index(messageid)
            del self.messages[index]
            del self.messageids[index]
            return True
        except:
            return False
        
        

class rooms(object):
    
    def __init__(self,roomlimit=100):
        self.roomlimit=roomlimit
        self.rooms=[]
        
    def getroom(self,roomid):
        #print(len(self.rooms))
        for i in range(0,len(self.rooms)):
            r=self.rooms[i]
            
            if(r.roomid==roomid):
                return(r)
        return(NULL)
        
    def subscribe(self,roomid,user):
        for r in self.rooms:
            if(r.roomid==roomid):
                return(r.subscribe(user))
        if(len(self.rooms)<self.roomlimit-1):
            r=room(roomid,[user])
            self.rooms.append(r)
            return True
        return False
    
    def unsubscrible(self,roomid,user):
        for r in self.rooms:
            if(r.getroomid()==roomid):
                r.unsubscribe(user)
                if(len(r.users)==0):
                    del r
                return True
        return False
        
    def getmessage(self,roomid):
        for r in self.rooms:
            if(r.roomid==roomid):
                return r.getmessage()
        return ""
