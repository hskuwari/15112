import kivy
kivy.require('1.9.1')

'''from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.layout import Layout
#from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.core.image import Image
#from kivy.graphics import BorderImage
from kivy.graphics import Color, Rectangle
#from kivy.uix.image import AsyncImage


## http://stackoverflow.com/questions/31179155/how-to-set-a-screen-background-image-in-kivy/31181960#31181960
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

class GameScreen(Screen):
    pass

class RootScreen(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootScreen()

if __name__ == "__main__":
    MainApp().run()'''

## http://stackoverflow.com/questions/32274842/how-do-i-set-the-background-of-my-main-screen-using-the-kv-file

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import ReferenceListProperty
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
import random

Builder.load_string('''

<BGScreen>:
    id: "background"
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'road1.png'

<StartScreen>
    id: "start"
    BGScreen:
        id: "background"
##    canvas:
##    
##        Rectangle:
##            source: 'coin.gif'
##            pos_hint: {'center_x':0.5,'center_y':0.5}
#   FloatLayout:
#       Image:
#           pos_hint: {'center_x':0.5,'y':0.5}
#           size_hint: 0.5,0.5
#           size: self.size
#source: 'logo.png'
''')

from kivy.config import Config
Config.set('graphics', 'width', '270') ## MAKE IT 1080
Config.set('graphics', 'height', '480') ## MAKE IT 1920

sm = ScreenManager()
StartScreen = Screen(name="start")
sm.add_widget(StartScreen)
f = FloatLayout()
fl = FloatLayout()
F = FloatLayout()
CF = FloatLayout()
pos1 = [0.15,0.15]
posofpic = "mid" 
pos2 = [0.5,0.15]
pos3 = [0.85,0.15]
#chara = Image(source="ham-running.gif",anim_delay= 0.05,pos_hint={'center_x':pos2[0], 'center_y':pos2[1]})
Jumping = False
#charaj = Image(source="ham-jumping.gif",anim_delay= 0.05,pos_hint={'center_x':pos2[0], 'center_y':pos2[1]})

JumpingCount = 0

# different character poses
charaleftJump = Image(source="ham-jumping.gif",anim_delay= 0.05,pos_hint={'center_x':pos1[0], 'center_y':pos1[1]+0.2})
charamidJump = Image(source="ham-jumping.gif",anim_delay= 0.05,pos_hint={'center_x':pos2[0], 'center_y':pos2[1]+0.2})
chararightJump = Image(source="ham-jumping.gif",anim_delay= 0.05,pos_hint={'center_x':pos3[0], 'center_y':pos3[1]+0.2})
charaleftRun = Image(source="ham-running.gif",anim_delay= 0.05,pos_hint={'center_x':pos1[0], 'center_y':pos1[1]})
charamidRun = Image(source="ham-running.gif",anim_delay= 0.05,pos_hint={'center_x':pos2[0], 'center_y':pos2[1]})
chararightRun = Image(source="ham-running.gif",anim_delay= 0.05,pos_hint={'center_x':pos3[0], 'center_y':pos3[1]})

currentCharacter = charamidRun

coinmid1 = Image(source="coin.gif",anim_delay= 0.05,pos_hint={'center_x':0.5, 'center_y':0.5})
coinmid2 = Image(source="coin.gif",anim_delay= 0.05,pos_hint={'center_x':0.5, 'center_y':0.45})
coinmid3 = Image(source="coin.gif",anim_delay= 0.05,pos_hint={'center_x':0.5, 'center_y':0.35})
coinmid4 = Image(source="coin.gif",anim_delay= 0.05,pos_hint={'center_x':0.5, 'center_y':0.25})
coinmid5 = Image(source="coin.gif",anim_delay= 0.05,pos_hint={'center_x':0.5, 'center_y':0.15})
coinmid = [coinmid1,coinmid2,coinmid3,coinmid4,coinmid5]
coinleft1 = Image(source="coin.gif",anim_delay= 0.05,pos_hint={'center_x':0.5, 'center_y':0.5})
coinleft2 = Image(source="coin.gif",anim_delay= 0.05,pos_hint={'center_x':0.45, 'center_y':0.45})
coinleft3 = Image(source="coin.gif",anim_delay= 0.05,pos_hint={'center_x':0.35, 'center_y':0.35})
coinleft4 = Image(source="coin.gif",anim_delay= 0.05,pos_hint={'center_x':0.25, 'center_y':0.25})
coinleft5 = Image(source="coin.gif",anim_delay= 0.05,pos_hint={'center_x':0.15, 'center_y':0.15})
coinleft = [coinleft1,coinleft2,coinleft3,coinleft4,coinleft5]
coinright1 = Image(source="coin.gif",anim_delay= 0.05,pos_hint={'center_x':0.5, 'center_y':0.5})
coinright2 = Image(source="coin.gif",anim_delay= 0.05,pos_hint={'center_x':0.60, 'center_y':0.45})
coinright3 = Image(source="coin.gif",anim_delay= 0.05,pos_hint={'center_x':0.65, 'center_y':0.35})
coinright4 = Image(source="coin.gif",anim_delay= 0.05,pos_hint={'center_x':0.75, 'center_y':0.25})
coinright5 = Image(source="coin.gif",anim_delay= 0.05,pos_hint={'center_x':0.85, 'center_y':0.15})
coinright = [coinright1,coinright2,coinright3,coinright4,coinright5]
posofcoin = ["left","right","mid"]
AddCoin = True


class BGScreen(FloatLayout):

    def __init__(self, **kwargs):
        super(BGScreen, self).__init__(**kwargs)

    
class StartScreen(Screen):
    def __init__(self, **kwargs):
        global fl,f,CF
        super(StartScreen, self).__init__(**kwargs)
        B1 = Button(text="Play",size_hint=(0.3,0.1),pos_hint={'center_x':0.5, 'center_y':0.45})
        B2 = Button(text="Instuction",size_hint=(0.3,0.1),pos_hint={'center_x':0.5, 'center_y':0.3})
        B3 = Button(text="Characters",size_hint=(0.3,0.1),pos_hint={'center_x':0.5, 'center_y':0.15})
        self.add_widget(f)
        f.add_widget(B1)
        f.add_widget(B2)
        f.add_widget(B3)
        B1.bind(on_press=lambda a:self.PlayTheGame())
        B2.bind(on_press=lambda a:self.InstScreen())
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.add_widget(fl)
        self.add_widget(CF)

    def _keyboard_closed(self):
        print 'My keyboard have been closed!'
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
        
    def backB(self):
        global fl
        fl.canvas.before.clear()
        self.remove_widget(fl)

    def InstPlay(self):
        global F,f
        global currentCharacter
        self.backB()
        self.remove_widget(f)
        self.add_widget(F)
        F.add_widget(currentCharacter)

    def InstScreen(self):
        global fl
        with fl.canvas.before:
            Color(0.5, 0.5, 0.5)
            Rectangle(pos_hint={'center_x':0.5,'center_y':0.5}, size=self.size)
        inst = Label(text="INSTRUCTIONS\n So you flick upward to jump,\n right or left to slide right or left.",pos_hint={'center_x':0.5,'center_y':0.5})
        pb = Button(text="Play",size_hint=(0.1,0.01),pos_hint={'center_x':0.4,'center_y':0.3})
        bb = Button(text="Back",size_hint=(0.1,0.01),pos_hint={'center_x':0.6,'center_y':0.3})
        pb.bind(on_press=lambda a:self.InstPlay())
        bb.bind(on_press=lambda a:self.backB())
        fl.add_widget(inst)
        fl.add_widget(pb)
        fl.add_widget(bb)
##        with self.canvas.after:
##            Color(0.5, 0.5, 0.5)
##            Rectangle(pos=(0, 0), size=(500, 500))
##            Label(text="INSTRUCTIONS\n So you flick upward to jump,\n downward to slide,\n right or left to slide right or left.",pos=(80,200))
##            Label(text="")
##            Button(text="Play",size=(50,30),pos=(150, 100),on_press=lambda a:backB())
##            Button(text="Back",size=(50,30),pos=(80,100),on_press=lambda a:backB())

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        global posofpic,pos1,pos2,pos3,chara,F,Jumping,JumpingCount
        if keycode[1] == 'left':
            if posofpic == "mid":
                posofpic = "left"
            elif posofpic == "right":
                posofpic = "mid"
        elif keycode[1] == 'right':
            if posofpic == "left":
                posofpic = "mid"
            elif posofpic == "mid":
                posofpic = "right"
        elif keycode[1] == 'up':
            Jumping = True
            #JumpingCount = 2
            #self.PlayGame()
        self.PlayGame()

    def PlayTheGame(self):
        global currentCharacter,F,Jumping,f
        self.remove_widget(f)
        self.add_widget(F)
        F.add_widget(currentCharacter)

    def Delete_Jumping(self):
        global F,charaj
        #F.remove_widget(charaj)
        self.PlayGame()

##    def Coins(self):
##        global CF
##        size = [0.1,0.1]
##        positions = ["left","mid","right"]
##        coin = Image(source="coin.gif",anim_delay=0.05,pos_hint={'center_x':0.5, 'center_y':0.5},size_hint=(size[0],size[1]))
##        CF.add_widget(coin)
##        #position = random.choice(positions)
##        #Clock.schedule_once(lambda a: self.MoveCoin(position,size,coin), 0.5)

    def MoveCoin(self):
        global CF,coinmid,coinleft,coinright,posofcoin,AddCoin
        position = random.choice(posofcoin)
        positiononroadleft = 0
        if posofcoin == "left":
            if AddCoin:
                AddCoin = False
                
            else:
                return
        
        
##        with CF.canvas:
##            pos_hint({'center_x':0.5,'center_y':0.5})
##            Rectangle(source="coin.gif")
##        random_y = 100
##        random_y = random_y - 0.1
##        anim = Animation(y=random_y,
##                         duration=4,
##                         t='out_elastic')
##        anim.start(self.CF)
##        print "coin?"


##    def MoveCoin(self,position,size,coin):
##        global CF,cpos1,cpos2,cpos3
##        size[0] = size[0] + 0.01
##        size[1] = size[1] + 0.01
##        if position == "left":
##            cpos1[0] = cpos1[0] - 0.05
##            cpos1[1] = cpos1[1] - 0.05
##            coin = Image(source="coin.gif",anim_delay=0.05,pos_hint={'center_x':cpos1[0], 'center_y':cpos1[1]},size_hint=(size[0],size[1]))
##            F.add_widget(coin)
##        elif position == "mid":
##            cpos2[0] = cpos2[0] - 0.05
##            cpos2[1] = cpos2[1] - 0.05
##            coin = Image(source="coin.gif",anim_delay=0.05,pos_hint={'center_x':cpos2[0], 'center_y':cpos2[1]},size_hint=(size[0],size[1]))
##            F.add_widget(coin)
##        elif position == "right":
##            cpos3[0] = cpos3[0] - 0.05
##            cpos3[1] = cpos3[1] - 0.05
##            coin = Image(source="coin.gif",anim_delay=0.05,pos_hint={'center_x':cpos3[0], 'center_y':cpos3[1]},size_hint=(size[0],size[1]))
##            F.add_widget(coin)
##        Clock.schedule_interval(lambda a: self.MoveCoin(position,size,coin), 1)
                             
    def PlayGame(self):
        global posofpic,pos1,pos2,pos3,currentCharacter,F,Jumping,charamidRun,chara
        global charaleftRun, chararightRun,charaleftJump, charamidJump,chararightJump
        global JumpingCount
        F.remove_widget(currentCharacter)
        Clock.schedule_interval(lambda a: self.MoveCoin(), 5)
        print "In PlayGame"
        if Jumping:
            
            #if JumpingCount > 0:
            #    print JumpingCount
            #    F.add_widget(currentCharacter)
            #    JumpingCount = JumpingCount - 1 
            #else:
            Jumping = False                                                            
            if posofpic == "mid":
                print "mid Jumping"
                currentCharacter = charamidJump
                F.add_widget(currentCharacter)
                #Clock.schedule_once(lambda a: self.Delete_Jumping(), 0.5)               
            elif posofpic == "left":
                currentCharacter = charaleftJump
                F.add_widget(currentCharacter)
                #Clock.schedule_once(lambda a: self.Delete_Jumping(), 0.5)
            elif posofpic == "right":
                currentCharacter = chararightJump
                F.add_widget(currentCharacter)
            Clock.schedule_once(lambda a: self.PlayGame(), 0.35)
        else:
            #F.remove_widget(chara)
            if posofpic == "mid":
                print "in Mid"
                currentCharacter = charamidRun
                F.add_widget(currentCharacter)
            elif posofpic == "left":
                print "in Left"
                currentCharacter = charaleftRun
                F.add_widget(currentCharacter)
            elif posofpic == "right":
                currentCharacter = chararightRun
                F.add_widget(currentCharacter)
 


            
##        charaj = Image(source="ham-jumping.gif",anim_delay= 0.05,pos_hint={'center_x':pos2[0], 'center_y':pos2[1]})
####        chara = I
        
##            Label(text="INSTRUCTIONS\n So you flick upward to jump,\n downward to slide,\n right or left to slide right or left.",size=(10,10),pos=(130,200))
##            Button(text="Play",size=(50,30),pos=(150, 100))
##            self.add_widget(instlabel)
##            self.add_widget(backButton)
##            self.add_widget(playButton)
##            backButton.bind(on_press= lambda a:self.backB(instlabel,backButton,playButton))
    
##
##class Inst_Screen(Screen):
##    def __init__(self, **kwargs):
##        super(InstScreen, self).__init__(**kwargs)
##        IL = Label(text="INSTRUCTIONS\n So you flick upward to jump,\n downward to slide,\n right or left to slide right or left.",pos_hint={'center_x':0.5, 'center_y':0.15})
##        self.add_widget(IL)

    

class TestApp(App):
    pass

    def build(self):
        return StartScreen()

if __name__=='__main__':
    TestApp().run()
    
