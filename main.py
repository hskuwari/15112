## 15-112 | Project
## Project Name: Coin Collector
## My project is inspired from "Subway Surfers" but a really simpler version of it.
## I decomposed everything in 8 classes; 5 classes for every screen, which I will explain more later, 2 classes for coin
## animations, and 1 class to run this.
## I used screens to change between "Start Screen", "Instructions Screen", "You-Lose Screen", and "Pause/Quit". In the screen classes,
## I added the widgets I wanted in the screen.
## I also have code in kivy language where I used to add some widgets in the classes like backgrounds and the coin animations. 

## -------------------------------------------------------------------------------------------------------

import kivy
kivy.require('1.9.1')

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
from kivy.uix.screenmanager import NoTransition
import random
from kivy.utils import platform
from kivy.core.audio import SoundLoader,Sound


## ----- kv language -------------------------------------------------------------------------------------

#### I can't comment inside so I'll comment here:
### canvas.before is mostly used for background and animation

## StartScreen contains background and a float layout that has two buttons: 'Play' and 'Instructions'
#       Buttons: "play" > # when pressed it goes to 'play' screen | "instructions" > # when pressed it goes
#       to 'instructions' screen

## Instructions Screen contains a grey background and a float layout that has the instructions of the game
#  and play button
#       Buttons: "play" > # when pressed it goes to 'play' screen | "back" > # when pressed it goes to main
#       screen (a.k.a, start screen)
#       Labels and Images: are used for explaining instructions

## "Play" screen contains the background and coins animations

## "Lose" screen and "Quit" contains only the background, the rest are in python language

## Both classes, "GoldCoin" and "BlackBall" have the widget that would be animated because it needs to
## be in a canvas

Builder.load_string('''


<StartScreen>
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'road1.png'
    FloatLayout:
        Button: 
            name: "B1"
            text: "Play"
            size_hint: (0.3,0.1)
            pos_hint: {'center_x':0.5, 'center_y':0.45}
            on_press: 
                root.manager.current = 'play'
        Button: 
            name: "B2"
            text: "Instuctions"
            size_hint: (0.3,0.1)
            pos_hint: {'center_x':0.5, 'center_y':0.3}
            on_press: 
                root.manager.current = 'inst'

<InstScreen>
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'Unknown.jpeg'
    FloatLayout: 
        Image: 
            source: "inst.zip"
            pos_hint: {'center_x': 0.5,'center_y':0.45}
        Label:
            text: "INSTRUCTIONS" 
            pos_hint: {'center_x':0.5, 'center_y':0.95}
        Label:
            text: "GET THE GOLD COINS TO SCORE POINTS"
            pos_hint: {'center_x':0.5,'center_y':0.85}
        Label:
            text: "AVOID BLACK COINS OR YOU'LL LOSE"
            pos_hint: {'center_x':0.5,'center_y':0.82}
        Label:
            text: "(sometimes there is a black coin hidden behind "
            pos_hint: {'center_x':0.5,'center_y':0.77}
        Label:
            text: "a gold one and it's a trap!)"
            pos_hint: {'center_x':0.5,'center_y':0.74}
        Label:
            text: "for PC users: use the arrows < and > to move left or right"
            pos_hint: {'center_x':0.5,'center_y':0.7}
        Button: 
            name: "instback"
            text: "Back"
            size_hint: (0.3,0.1)
            pos_hint: {'center_x':0.35, 'center_y':0.2}
            on_press:
                root.manager.current = 'start'
        Button: 
            name: "instplay"
            text: "Play"
            size_hint: (0.3,0.1)
            pos_hint: {'center_x':0.65, 'center_y':0.2}
            on_press: 
                root.manager.current = 'play'

<PlayTheGame>:
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'road1.png'
    BlackBall: # Black coin
        pos: self.width/2.,self.height/2.
    GoldCoin: # Gold coin
        pos: self.width/2.,self.height/2.

<youLose>
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'Unknown.jpeg'

<Quit>
    name: "quit"
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'Unknown.jpeg'

<GoldCoin>:
    canvas:
        Color:
            rgba: 1, 1,1, 1
        
        Ellipse:
            source: "yellow.png"
            pos: self.pos
            size: 50,50

<BlackBall>:
    canvas:
        Color:
            rgba: 0,0,0,1
        Ellipse:
            source: "yellow.png"
            pos: self.pos
            size: 50,50
''')

## -------------------------------------------------------------------------------------------------------

## PC users will have a specific window size
if platform != 'android':
    Window.size = (500, 800)


## This function gets the highest score from a textfile that saves scores
## and checks if current score is higher, so it would rewrite the file, else
## it would return the highest score in the text file
def getHighestScore():
    global score
    f = open("highestscore.txt","r")
    highestscore = f.readlines()
    highestscore = int(highestscore[0])
    if highestscore >= score: ## if highest score is greater that the current score 
        return highestscore 
    else: ## else, save the current score in the text file and return it
        highestscore = score
        f = open("highestscore.txt","w")
        f.write(str(highestscore))
        return highestscore

## ----- initializing variables --------------------------------------------------------------------------
    
f = FloatLayout() ## floatlayout for "lose" screen
fl = FloatLayout() ## floatlayout for "quit" screen
F = FloatLayout() ## floatlayout for "play" screen

## positions of character
pos1 = [0.15,0.15]
posofpic = "mid" 
pos2 = [0.5,0.15]
pos3 = [0.85,0.15]

## Label widgets for scores 
score = 0
# score label in 'play' screen
Score = Label(text="[b][color=00000]Score: "+str(score)+"[/b][/color]", markup=True,pos_hint={'center_x':0.85, 'center_y':0.95})
# score label in 'lose' screen 
ScoreLose = Label(text="[b]YOU LOST[/b]\n\nYour Score was "+str(score),markup=True,pos_hint={'center_x':0.5, 'center_y':0.5})
# score label in 'quit' screen
ScoreQuit = Label(text="Your Score was "+str(score),pos_hint={'center_x':0.5, 'center_y':0.5})
highestscore = getHighestScore()
# highest score labels in 'lose' and 'quit' screens
highscoreLose = Label(text="Overall Highest Score is: "+str(highestscore),pos_hint={'center_x':0.5, 'center_y':0.4})
highscorelabelQuit = Label(text="Overall Highest Score is: "+str(highestscore),pos_hint={'center_x':0.5, 'center_y':0.45})

# different character positions
charaleftRun = Image(source="ham-running.zip",anim_delay= 0.05,pos_hint={'center_x':pos1[0], 'center_y':pos1[1]})
charamidRun = Image(source="ham-running.zip",anim_delay= 0.05,pos_hint={'center_x':pos2[0], 'center_y':pos2[1]})
chararightRun = Image(source="ham-running.zip",anim_delay= 0.05,pos_hint={'center_x':pos3[0], 'center_y':pos3[1]})

currentCharacter = charamidRun


# position of black coin
whichpos_b = ""
# position of gold coin
whichpos_g = ""

positions = ['mid','left','right']
GoldBall = ""
BlackBallPos = ""

## ----- classes -----------------------------------------------------------------------------------------

## StartScreen: the widgets inside are described between kv language above.
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.size = Window.width,Window.height
        
## QuitScreen: it contains the score scored in the game and the highest score scored
## overall the whole game. It updates the score every 0.01 second so it won't miss any
## new score made. It also contains button whether the user wants to play again or go
## back to the main screen.
class Quit(Screen):
    def __init__(self, **kwargs):
        super(Quit, self).__init__(**kwargs)
        self.size = Window.width,Window.height
        global fl,score,ScoreQuit,highscorelabelQuit
        self.add_widget(fl)
        fl.add_widget(ScoreQuit)
        fl.add_widget(highscorelabelQuit)
        playbtn = Button(text="Play again",size_hint= (0.3,0.1),pos_hint= {'center_x':0.65, 'center_y':0.3}) # play button
        mainbtn = Button(text="Main Screen",size_hint= (0.3,0.1),pos_hint= {'center_x':0.35, 'center_y':0.3}) # main screen button
        fl.add_widget(playbtn)
        fl.add_widget(mainbtn)
        # when play button pressed the screen switches to "play screen"
        playbtn.bind(on_press=lambda a: self.switchscreen('play'))
        # when main screen button pressed the screen switches to "play screen"
        mainbtn.bind(on_press=lambda a: self.switchscreen('start'))
        Clock.schedule_interval(lambda a: self.updateScore(), 0.01) # timer for the score to update

    ## this function removes the widget and re-adds it with the current score as well
    ## as highest score.
    def updateScore(self):
        global score,fl,ScoreQuit,highscorelabelQuit
        a = score
        fl.remove_widget(ScoreQuit)
        fl.remove_widget(highscorelabelQuit)
        b = getHighestScore()
        highscorelabelQuit = Label(text="Overall Highest Score is: "+str(b),pos_hint={'center_x':0.5, 'center_y':0.45})
        fl.add_widget(highscorelabelQuit)
        ScoreQuit = Label(text="Your Score was "+str(a),pos_hint={'center_x':0.5, 'center_y':0.5})
        fl.add_widget(ScoreQuit)

    ## this is used to switch screens for the buttons as well as resets the score back to 0 
    def switchscreen(self,towhat):
        global sm,score
        score = 0
        sm.current = towhat

## LoseScreen: it contains the score scored in the game and the highest score scored
## overall the whole game. It updates the score every 0.01 second so it won't miss any
## new score made. It also contains button whether the user wants to play again or go
## back to the main screen.
class youLose(Screen):
    def __init__(self, **kwargs):
        super(youLose, self).__init__(**kwargs)
        self.size = Window.width,Window.height
        global f,score,ScoreLose,highscoreLose
        self.add_widget(f)
        f.add_widget(ScoreLose)
        f.add_widget(highscoreLose)
        playbtn = Button(text="Play again",size_hint= (0.3,0.1),pos_hint= {'center_x':0.65, 'center_y':0.3}) # play button
        mainbtn = Button(text="Main Screen",size_hint= (0.3,0.1),pos_hint= {'center_x':0.35, 'center_y':0.3}) # main screen button
        f.add_widget(playbtn)
        f.add_widget(mainbtn)
        # when play button pressed the screen switches to "play screen"
        playbtn.bind(on_press=lambda a: self.switchscreen('play'))
        # when main screen button pressed the screen switches to "play screen"
        mainbtn.bind(on_press=lambda a: self.switchscreen('start'))
        Clock.schedule_interval(lambda a: self.updateScore(), 0.01) # timer for the score to update

    ## this function removes the widget and re-adds it with the current score as well
    ## as highest score.
    def updateScore(self):
        global score,f,ScoreLose,highscoreLose,HF
        a = score
        f.remove_widget(ScoreLose)
        f.remove_widget(highscoreLose)
        b = getHighestScore()
        highscoreLose = Label(text="Overall Highest Score is: "+str(b),pos_hint={'center_x':0.5, 'center_y':0.4})
        f.add_widget(highscoreLose)
        ScoreLose = Label(text="[b]YOU LOST[/b]\n\nYour Score was "+str(a),markup=True,pos_hint={'center_x':0.5, 'center_y':0.5})
        f.add_widget(ScoreLose)

    ## this is used to switch screens for the buttons as well as resets the score back to 0 
    def switchscreen(self,towhat):
        global sm,score
        score = 0
        sm.current = towhat

## PlayScreen: it contains the quit button top left the screen and the score top right the screen. As well as the
## chara running and the animations (which were added in kv language). This function checks if the user is using
## his/her PC or android phone to play. It also contains the inputs for keyboard, if the user was playing with PC,
## or touchscreen, of the user was playing with android.
class PlayTheGame(Screen):
    def __init__(self, **kwargs):
        super(PlayTheGame, self).__init__(**kwargs)
        if platform != 'android': ## checks for the user if its using PC or android
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.add_widget(F)
        QuitButton1 = Button(text="X",size_hint= (0.1,0.05),pos_hint= {'center_x':0.05, 'center_y':0.95})
        F.add_widget(QuitButton1)
        QuitButton1.bind(on_press=lambda a: self.switchscreen('quit'))
        F.add_widget(currentCharacter)
        F.add_widget(Score)

    ## this is used to switch screens for the buttons as well as resets the score back to 0 s
    def switchscreen(self,towhat):
        global sm,score
        score = 0
        sm.current = towhat

    ## help from: http://stackoverflow.com/questions/17280341/how-do-you-check-for-keyboard-events-with-kivy
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    ## checks for keyboard events from user. If right arrow, the character goes right
    ## and if left the character goes left.
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        global posofpic,pos1,pos2,pos3,chara,F,Jumping,JumpingCount,sm
        if sm.current == "play":
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
##            elif keycode[1] == 'up':
##                Jumping = True
        self.PlayGame()

    ## for touch events: if the user touches the right half of the screen the
    ## character goes right and vice versa. 
    def on_touch_down(self,touch):
        global posofpic,pos1,pos2,pos3,chara,F,Jumping,JumpingCount,sm
        if platform == 'android':
            if touch.pos[0] < Window.width/2 and touch.pos[1] < abs(Window.height - Window.height/8):
                if posofpic == "mid":
                    posofpic = "left"
                elif posofpic == "right":
                    posofpic = "mid"
            if touch.pos[0] > Window.width/2 and touch.pos[1] < abs(Window.height - Window.height/8):
                if posofpic == "left":
                    posofpic = "mid"
                elif posofpic == "mid":
                    posofpic = "right"
        ## this is for the quit button because for some reason it is buggy and cannot be clicked
        if touch.pos[1] > abs(Window.height - Window.height/8) and touch.pos[0] < Window.width/8:
            sm.current = 'quit'
##        if touch.pos[1] > touch.opos[1]:
##            Jumping = True

        self.PlayGame()

    ## this function makes the character go right or left. it removes the character everytime
    ## the user clickes the keyboard or touches the screen
    def PlayGame(self):
        global posofpic,pos1,pos2,pos3,currentCharacter,F,Jumping,charamidRun,chara
        global charaleftRun, chararightRun,score, sm
        F.remove_widget(currentCharacter)
        if posofpic == "mid":
            currentCharacter = charamidRun
            F.add_widget(currentCharacter)
        elif posofpic == "left":
            currentCharacter = charaleftRun
            F.add_widget(currentCharacter)
        elif posofpic == "right":
            currentCharacter = chararightRun
            F.add_widget(currentCharacter)       

        
##InstructionsScreen: everything was explained inside kv language above.
class InstScreen(Screen):
    pass

##BlackBall: this is for the black coin animations. 
class BlackBall(Widget):
    def __init__(self, **kwargs):
        super(BlackBall, self).__init__(**kwargs)
        self.pos = Window.width/2.,Window.height/2.
        Clock.schedule_once(lambda a: self.anim_to_random_pos(), 3/60.)   

    ## when the animation completes, it executes this function.
    ## it checks whether the character was on the same position as the black coin
    ## if it is, it would switch to 'lose' screen.
    def callback(self):
        global whichpos_b,currentCharacter,charamidRun,charaleftRun,chararightRun,sm,posofpic,BlackBallPos
        global GoldBall
        if sm.current == "play":
            if whichpos_b == "mid" and posofpic == "mid" and GoldBall != "mid":
                sm.current = "lose"
            elif whichpos_b == "left" and posofpic == "left" and GoldBall != "left":
                sm.current = "lose"
            elif whichpos_b == "right" and posofpic == "right" and GoldBall != "right":
                sm.current = "lose"
        self.anim_to_random_pos()
            
    ## this animates the black coin. it generates a random position for the coin then
    ## goes animates in the position that initialized in the if statement.
    ## if the animation finishes it goes to callback function where it checks if
    ## the character loses or continues and then starts animation all again
    def anim_to_random_pos(self):
        global positions,GoldBall,BlackBallPos,whichpos_b
        Animation.cancel_all(self)
        self.pos = Window.width/2.,Window.height/2.
        position = random.choice(positions)
        whichpos_b = ""
        while position == GoldBall:
            position = random.choice(positions)
        if position == "mid" and GoldBall != "mid":
            BlackBallPos = "mid"
            random_x = Window.width/2 
            random_y = 50
        elif position == "left" and GoldBall != "left":
            BlackBallPos = "left"
            random_x = Window.width/9
            random_y = 50
        elif position == "right" and GoldBall != "right":
            BlackBallPos = "right"
            random_x = Window.width - Window.width/8
            random_y = 50
        whichpos_b = position
        anim = Animation(x=random_x,y=random_y,
                         duration=1)
        anim.bind(on_complete= lambda x,y:self.callback())
        anim.start(self)

##GoldCoin: this is for the gold coin animations. 
class GoldCoin(Widget):
    def __init__(self, **kwargs):
        super(GoldCoin, self).__init__(**kwargs)
        self.pos = Window.width/2.,Window.height/2.
        Clock.schedule_once(lambda a: self.anim_to_random_pos(), 2/60.) 
        
    ## when the animation completes, it executes this function.
    ## it checks whether the character was on the same position as the gold coin
    ## if it is, it would add 1 to the score 
    def callback(self):
        global whichpos_g,currentCharacter,charamidRun,charaleftRun,chararightRun,score,sm
        if sm.current == "play":
            if whichpos_g == "mid" and currentCharacter == charamidRun:
                score = score + 1
                self.updateScore()
            elif whichpos_g == "left" and currentCharacter == charaleftRun:
                score = score + 1
                self.updateScore()
            elif whichpos_g == "right" and currentCharacter == chararightRun:
                score = score + 1
                self.updateScore()
        self.anim_to_random_pos()

    ## this is so it would update the score label everytime the user scores 
    def updateScore(self):
        global score,Score,F
        F.remove_widget(Score)
        Score = Label(text="[b][color=00000]Score: "+str(score)+"[/b][/color]", markup=True,pos_hint={'center_x':0.85,'center_y':0.95})
        F.add_widget(Score)

    ## this animates the gold coin. it generates a random position for the coin then
    ## goes animates in the position that initialized in the if statement.
    ## if the animation finishes it goes to callback function where it checks if
    ## the character scores and then starts animation all again
    def anim_to_random_pos(self):
        global positions,GoldBall
        global whichpos_g
        Animation.cancel_all(self)
        self.pos = Window.width/2.,Window.height/2.
        position = random.choice(positions)
        if position == "mid":
            GoldBall = "mid"
            random_x = Window.width/2 
            random_y = 30
        elif position == "left":
            GoldBall = "left"
            random_x = Window.width/9
            random_y = 50
        elif position == "right":
            GoldBall = "right"
            random_x = Window.width - Window.width/8
            random_y = 50
        whichpos_g = position
        anim = Animation(x=random_x,y=random_y,
                         duration=1)
        anim.bind(on_complete= lambda x,y:self.callback())
        anim.start(self)
        
## ----- initializing the screens ------------------------------------------------------------------------
        
sm = ScreenManager(transition=NoTransition())
sm.add_widget(StartScreen(name="start"))
sm.add_widget(PlayTheGame(name="play"))
sm.add_widget(InstScreen(name="inst"))
sm.add_widget(youLose(name="lose"))
sm.add_widget(Quit(name='quit'))

## -------------------------------------------------------------------------------------------------------

# for running the program
class CoinCollectorApp(App):
    pass

    def build(self):
        return sm

if __name__=='__main__':
    CoinCollectorApp().run()
