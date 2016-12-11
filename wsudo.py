'''
Created on 2016年4月5日

@author: heguofeng
'''
from tkinter import *
import tkinter
import tkinter.messagebox
#from tkinter.messagebox import *
from sudoku import Sudoku 
from _ast import Try
from warnings import catch_warnings




class wsudo(Sudoku):
    top = tkinter.Tk()
    values=[]
    entrylist=[]
    sudovalues=[]
    framelist=[]
   
    def __init__(self,s):
        '''
        Constructor
        '''
        # 进入消息循环
        self.top.title("数独   using python by gonewind @2016")
        for i in range(0,81):
            self.values.append(StringVar())
            self.values[i].set(str(i))
            if ((i//27)*3+(i%9)//3)%2==0:
                bgcolor="#d0ffff"
            else:
                bgcolor="#ffd0d0"
            self.entrylist.append(tkinter.Entry(self.top,name=str(i),width=3,bg=bgcolor,bd=2,font="Arial 20 bold",justify=CENTER,state=NORMAL,textvariable=self.values[i]))
            self.entrylist[i].bind('<Tab>', self.valuechanged)
        j=0
        for item in self.entrylist:    
            item.grid(row=j//9,column=j%9)
            #item.pack(side=LEFT)
            j+=1
        
        l1=tkinter.Label(self.top,text="等级：")
        l1.grid(row=11,column=0)
        sv1=StringVar()
        sv1.set("10")
        self.entrylist.append(tkinter.Entry(self.top,name="level",width=3,bd=2,font="Arial 16",justify=CENTER,state=NORMAL,textvariable=sv1))
        self.entrylist[81].grid(row=11,column=1)
        b2=tkinter.Button(self.top,text="换盘",command=self.reset)
        b2.grid(row=11,column=2)
        b1=tkinter.Button(self.top,text="重做",command=self.replay)
        b1.grid(row=11,column=4)
        b3=tkinter.Button(self.top,text="检查",command=self.checkup)
        b3.grid(row=11,column=5)
        b4=tkinter.Button(self.top,text="自动",command=self.auto)
        b4.grid(row=11,column=6)       
        b5=tkinter.Button(self.top,text="帮助",command=self.help)
        b5.grid(row=11,column=8)          #b5.tkinter.Entry()
        Sudoku.__init__(self,s)
        self.reload(1)
        
        return
    
    def valuechanged(self,event):
        #print(event.widget.winfo_name()+' : ' + event.widget.get())
        return
    
    def run(self):
        self.top.mainloop()
        
        
    def reset(self):
        Sudoku.randominit(self, int(self.entrylist[81].get()))
        s=self.get()
        for i in range(0,9):
            for j in range(0,9):
                start[i][j]=s[i][j]
        self.reload(1)
        
    def replay(self):
        self.set(start)
        self.reload(1)
        
    def undo(self):
        pass
    
        
    # mode = 0 only reload data  mode =1 reload data and change the grid
    def reload(self,mode=0):
        sudovalues=self.get()
        for i in range(0,9):
            for j in range(0,9):
                if sudovalues[i][j] !=0 :
                    self.values[i*9+j].set(str(sudovalues[i][j]))
                    if mode==1:
                        #self.entrylist[i*9+j]=tkinter.Entry(self.top,width=4,bd=2,justify=CENTER,state=DISABLED,textvariable=self.values[i*9+j]).grid(row=i,column=j)
                        self.entrylist[i*9+j].config(state=DISABLED)
                else:
                    self.values[i*9+j].set("")
                    if mode == 1:
                        #self.entrylist[i*9+j]=tkinter.Entry(self.top,width=4,bd=2,justify=CENTER,state=NORMAL,textvariable=self.values[i*9+j],command=self.valuechanged(i*9+j)).grid(row=i,column=j)
                        self.entrylist[i*9+j].config(state=NORMAL)
        return             
                
    def setsudo(self): 
        completed=1
        for i in range(0,81):
            s=self.entrylist[i].get()
            try:
                v=int(s)
                Sudoku.setij(self, i//9, i%9, v)
            except:
                Sudoku.setij(self, i//9, i%9, 0)
                completed=0
        return completed
    
    def checkup(self):
        
        complete=self.setsudo()
        '''cur=self.get()
        for i in range(0,9):
            print(cur[i])'''
        if self.check() and complete==1:
            tkinter.messagebox.showinfo(title="恭喜",message="完成")
        else:
            tkinter.messagebox.showinfo(title="提示",message="还有错误！")
        return
        
    
    def auto(self):
        #s=[[8,0,0,0,0,0,0,0,0],[0,0,3,6,0,0,0,0,0],[0,7,0,0,9,0,2,0,0],[0,5,0,0,0,7,0,0,0],[0,0,0,0,4,5,7,0,0],[0,0,0,1,0,0,0,3,0],[0,0,1,0,0,0,0,6,8],[0,0,8,5,0,0,0,1,0],[0,9,0,0,0,0,4,0,0]]
        #sudo=sudoku.sudoku(s)
        #sudo.autorun()
        self.setsudo()
        if not self.autorun():
            tkinter.messagebox.showinfo(title="提示",message="无解！")
        else:
            self.reload()
        return
    
    def help(self):
        message="等级： 1-20 1代表最容易，20最难 ；\n "
        message=message+"换盘：根据等级初始化  等级为0时，用户自行定义初始数据  ；\n"
        message=message+"重做：回到初始状态 ； \n"
        message=message+"检查：查看答题是否正确 ； \n"
        message=message+"自动：根据目前的盘面，自动完成数独 ； \n"
        message=message+"帮助：此帮助! \n\n"
        message=message+"数独 version 1.0 @2016 \n"
        message=message+"反馈  gonewind08@qq.com \n"
        
        tkinter.messagebox.showinfo(title="帮助",message=message)
        return
        
if __name__ == '__main__':
    start=[[8,0,0,0,0,0,0,0,0],[0,0,3,6,0,0,0,0,0],[0,7,0,0,9,0,2,0,0],[0,5,0,0,0,7,0,0,0],[0,0,0,0,4,5,7,0,0],[0,0,0,1,0,0,0,3,0],[0,0,1,0,0,0,0,6,8],[0,0,8,5,0,0,0,1,0],[0,9,0,0,0,0,4,0,0]]

    ws=wsudo(start)
    ws.run()
 
