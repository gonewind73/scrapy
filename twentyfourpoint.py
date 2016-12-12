from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

import random

from math import fabs


class Point24(object):
    '''
    24p game
    '''

    __author = "heguofeng"
    data = [0, 0, 0, 0]
    expression = ["", "", "", ""]
    results=[]

    def __init__(self, s):
        '''
        Constructor
        '''
        self.data = s
        for i in range(0, len(s)):
            self.expression[i] = str(self.data[i])
        return

    def search(self, n):
        if n == 1:
            if fabs(self.data[0] - 24) < 0.0001:
                print(self.expression[0])
                self.results.append(self.expression[0])
                return False
            else:
                return False
        else:
            for i in range(0, n):
                for j in range(i + 1, n):
                    a = self.data[i]
                    b = self.data[j]
                    expra = self.expression[i]
                    exprb = self.expression[j]
                    self.data[j] = self.data[n - 1]
                    self.expression[j] = self.expression[n - 1]
                    self.expression[i] = "(" + expra + "+" + exprb + ")"
                    self.data[i] = a + b
                    if (self.search(n - 1)):
                        return True
                    self.expression[i] = "(" + expra + "-" + exprb + ")"
                    self.data[i] = a - b
                    if (self.search(n - 1)):
                        return True
                    self.expression[i] = "(" + exprb + "-" + expra + ")"
                    self.data[i] = b - a
                    if (self.search(n - 1)):
                        return True
                    self.expression[i] = "(" + expra + "*" + exprb + ")"
                    self.data[i] = a * b
                    if (self.search(n - 1)):
                        return True
                    if (b != 0):
                        self.expression[i] = "(" + expra + "/" + exprb + ")"
                        self.data[i] = a / b
                        if (self.search(n - 1)):
                            return True
                    if (a != 0):
                        self.expression[i] = "(" + exprb + "/" + expra + ")"
                        self.data[i] = b / a
                        if (self.search(n - 1)):
                            return True
                    self.data[i] = a
                    self.data[j] = b
                    self.expression[i] = expra
                    self.expression[j] = exprb
            return False
        return

    def autorun(self):
        return self.search(4)

class Game24Paddle(Widget):
    score = NumericProperty(0)


class Game24Card(Widget):
    def __init(self,no,point):
        self.card_point = NumericProperty(point)
        self.card_no=no



class Game24p(FloatLayout):
    player=0
    cards=[0,0,0,0]

    def player1(self,*args):
        print("jst pressed")
        if(self.player==0):
            self.player=1
        return

    def player2(self,*args):
        print("jst pressed")
        if(self.player==0):
            self.player=2
        return

    def restart(self,*args):
        self.player=0
        self.cards[0] = random.randint(1,10)
        self.cards[1] = random.randint(1, 10)
        self.cards[2] = random.randint(1, 10)
        self.cards[3] = random.randint(1, 10)
        self.card0.text=str(self.cards[0])
        self.card1.text = str(self.cards[1])
        self.card2.text = str(self.cards[2])
        self.card3.text = str(self.cards[3])
        return

    def auto(self,*args):
        self.player=0
        p=Point24(self.cards)
        p.autorun()
        #print(p.results)
        content=""
        for i in range(0,len(p.results)):
            content=content+"\n"+p.results[i]
        print(content)
        pop = Popup(title='24p popup',
                    content=Label(text=content),
                    size_hint=(.5, .5))
        pop.open()
        return


    def __init__(self, **kwargs):
        self.cols=4

        super(Game24p, self).__init__(**kwargs)
        self.add_widget(Label(text="Game 24 Point",size_hint=(.2,.2),pos_hint={'center_x': .5, 'center_y': .9}), 2)
        player1button=Button(text="Player1",size_hint=(.2,.1),pos_hint={'center_x': .1, 'center_y': .7})
        self.add_widget(player1button,4)
        player1button.bind(on_press=self.player1)

        self.card0=Label(text="8",size_hint=(.2,.2),pos_hint={'center_x': .2, 'center_y': .5})
        self.card1=Label(text="7",size_hint=(.2,.2),pos_hint={'center_x': .4, 'center_y': .5})
        self.card2=Label(text="5",size_hint=(.2,.2),pos_hint={'center_x': .6, 'center_y': .5})
        self.card3=Label(text="6",size_hint=(.2,.2),pos_hint={'center_x': .8, 'center_y': .5})
        self.add_widget(self.card0,8)
        self.add_widget(self.card1,9)
        self.add_widget(self.card2,10)
        self.add_widget(self.card3,11)
        self.restart()

        restartbutton=Button(text="Restart",size_hint=(.1,.1),pos_hint={'center_x': .2, 'center_y': .3})
        restartbutton.bind(on_press=self.restart)
        self.add_widget(restartbutton, 13)
        autobutton = Button(text="Auto", size_hint=(.1, .1), pos_hint={'center_x': .4, 'center_y': .3})
        autobutton.bind(on_press=self.auto)
        self.add_widget(autobutton, 14)

        player2button=Button(text="Player2",size_hint=(.2,.1),pos_hint={'center_x': .9, 'center_y': .3})
        player2button.bind(on_press=self.player2)
        self.add_widget(player2button,15)

    def poke_card(self,point=1):
        pass

    def update(self, dt):
        pass


class Game24App(App):
    def build(self):
        game = Game24p()
        game.poke_card(1)
        return game


if __name__ == '__main__':
    Game24App().run()