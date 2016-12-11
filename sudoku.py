'''
Created on 2016年4月5日

@author: heguofeng
'''
import random

class Sudoku(object):
    '''
    sudoku game
    '''

    __author="heguofeng"
    __start=[[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]]
    __curdata=[[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]]
    

    def __init__(self,s):
        '''
        Constructor
        '''
        self.set(s)
        return
     
    def __copyto(self,s,d):
        for i in range(0,9):
            for j in range(0,9):
                d[i][j]=s[i][j]
        return
       
    def set(self,s):
        self.__copyto(s,self.__start)
        self.__copyto(s,self.__curdata)
        return
                
    def setij(self, i,j,v):
        self.__curdata[i][j]=v
        return
    
    def getij(self, i,j):
        return self.__curdata[i][j]
        
    def get(self):
        return self.__curdata
    
    def check9(self, s):
        result=[0,0,0,0,0,0,0,0,0,0]
        #print(s) 
        for i in range(0,9):
            result[s[i]] += 1
        for j in range(1,10):
            if result[j]>1:
                return False
        return True
        
    def __getblock(self,i):
        t=[0,0,0,0,0,0,0,0,0]
        for j in range(0,3):
            for k in range(0,3):
                t[j*3+k]=self.__curdata[(i//3)*3+j][(i%3)*3+k]
        return t
    
    def checki(self,i):
        ''' check ith value is acceptable?
        '''
        t=[0,0,0,0,0,0,0,0,0]
        if not self.check9(self.__curdata[i//9]): 
            return False
        for j in range(0,9):
            #print(i%9,j)
            t[j]=self.__curdata[j][i%9]
        if not self.check9(t):
            return False
        t=self.__getblock((i//27)*3+(i%9)//3)
        return self.check9(t)
    
        

    def check(self):
        '''check global
        '''
        #check row
        t=[0,0,0,0,0,0,0,0,0]
        for i in range(0,9):
            if not self.check9(self.__curdata[i]):
                #print "row" + str(i) + "false"
                return False
        #check col
        for i in range(0,9):
            for j in range(0,9):
                t[j]=self.__curdata[j][i]
            if not self.check9(t):
                #print "col" + str(i) + "false"
                return False
        #check block
        for i in range(0,9):
            t=self.__getblock(i)
            if not self.check9(t):
                #print "block" + str(i) + "false"
                return False
        return True
    
    def print9g(self):
        print("start data")
        for i in range(0,9):
            print(self.__start[i])
        print("curdata")
        for i in range(0,9):
            print(self.__curdata[i])
        return

    def search(self,deep):
        #print deep

        if self.check():
            if deep==81 :
                #self.print9g()
                return True
            else:
                if(self.__start[deep//9][deep%9]!=0):
                    self.__curdata[deep//9][deep%9]=self.__start[deep//9][deep%9]
                    return self.search(deep+1)
                else:
                    for i in range(1,10):
                        self.__curdata[deep//9][deep%9]=i
                        #self.print9g()
                        if self.search(deep+1):
                            return True
                        else:
                            self.__curdata[deep//9][deep%9]=0
                    return False
        else:
            return False
    
    def autorun(self):
        self.__copyto(self.__curdata,self.__start) 
        #backup start
        return self.search(0)
            
        
        return
    
    def randominit(self,level=3):   
        '''
        for i in range(0,9):
            for j in range(0,9):
                self.__curdata[i][j]=0
        i=0        
        while  i < level*9:
            a=random.randint(0,8)
            b=random.randint(0,8)
            c=random.randint(1,9)
            print(i,a,b,c)
            if self.__curdata[a][b] == 0:
                self.__curdata[a][b]=c
                if not self.checki(a*9+b):
                    self.__curdata[a][b]=0
                    i=i-1
            else:
                i=i-1
            i=i+1
        '''
        for i in range(0,81):
            self.__curdata[i//9][i%9]=0
        if level==0:  #level0 userdefine grid
            return
        l=[1,2,3,4,5,6,7,8,9]
        for i in range(0,9):
            a=random.randint(0,9-i-1)
            #print(i,a,len(l),l)
            self.__curdata[0][i]=l[a]
            del l[a]
        #print(self.__curdata[0])
        if self.autorun():
            for i in range(0,level*9):
                a=random.randint(0,80)
                self.__curdata[a//9][a%9]=0
        
        return 
        
        
        

if __name__ == '__main__':
    start=[[8,0,0,0,0,0,0,0,0],[0,0,3,6,0,0,0,0,0],[0,7,0,0,9,0,2,0,0],[0,5,0,0,0,7,0,0,0],[0,0,0,0,4,5,7,0,0],[0,0,0,1,0,0,0,3,0],[0,0,1,0,0,0,0,6,8],[0,0,8,5,0,0,0,1,0],[0,9,0,0,0,0,4,0,0]]
    sudo=Sudoku(start)
    #sudo.set(start)
    
    sudo.print9g()
    sudo.autorun()