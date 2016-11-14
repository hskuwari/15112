from kivy.base import runTouchApp
from kivy.lang import Builder

from kivy.uix.widget import Widget

from kivy.clock import Clock
from kivy.animation import Animation

from kivy.properties import ListProperty

from kivy.core.window import Window

from kivy.core.image import Image

import random

Builder.load_string('''
<Root>:
    canvas.before:
        Rectangle:
            source: 'road1.png'
            pos: self.pos
            size: self.size
    ClockRect:
##        pos_hint: {'center_x':0.5,'center_y':0.5}
        pos: self.width/2.,self.height/2.
##    AnimRect:
##        pos: 500, 300
<ClockRect>:
    canvas:
        Ellipse:
            source: "yellow.png"
            pos: self.pos
            size: 50,50
##<AnimRect>:
##    canvas:
####
####    FloatLayout:
####        Image:
####            source: "red.png"
####            pos: self.pos
####            size: self.size
##        
##        Rectangle:
##            source: "coin.gif"
##            pos: self.pos
##            size: self.size
''')


positions = ['mid','left','right']

class Root(Widget):
    pass

class ClockRect(Widget):
    global positions
    position = random.choice(positions)
    if position == "mid":
        velocity = ListProperty([0, 15])
    if position == 'right':
        velocity = ListProperty([-10, 10])
    if position == "left":
        velocity = ListProperty([10, 10])
 ##left:   velocity = ListProperty([10, 10])

    

    def __init__(self, **kwargs):
        super(ClockRect, self).__init__(**kwargs)
##        timeintervals = random.randint(1/60.,3/60.)
        Clock.schedule_interval(self.update, 1/60.)

    def update(self, *args):
        position = random.choice(positions)
        if position == "mid":
            velocity = ListProperty([0, 15])
        if position == 'right':
            velocity = ListProperty([-10, 10])
        if position == "left":
            velocity = ListProperty([10, 10])
##        if position == "mid":
            ##velocity = ListProperty([0, 15])
##            self.x -= self.velocity[0]
##            self.y -= self.velocity[1]
##
##            if self.x < 0 or (self.x + self.width) > Window.width:
##                self.velocity[0] *= 0
##                self.velocity[1] *= 0
##            if self.y < 0 or (self.y + self.height) > Window.height:
##                self.velocity[1] *= 0
##                self.velocity[0] *= 0
##        elif position == "left"
##        elif position == "right"
        self.x -= self.velocity[0]
        self.y -= self.velocity[1]
        
        if self.x < 0 or (self.x + self.width) > Window.width:
            if position == "mid":
                velocity = ListProperty([0, 15])
            if position == 'right':
                velocity = ListProperty([-10, 10])
            if position == "left":
                velocity = ListProperty([10, 10])
            self.pos = Window.width/2.,Window.height/2.
            self.x -= self.velocity[0]
            self.y -= self.velocity[1]
            self.update()
            
        if self.y < 0 or (self.y + self.height) > Window.height:
            if position == "mid":
                velocity = ListProperty([0, 15])
            if position == 'right':
                velocity = ListProperty([-10, 10])
            if position == "left":
                velocity = ListProperty([10, 10])
            self.pos = Window.width/2.,Window.height/2.
            self.x -= self.velocity[0]
            self.y -= self.velocity[1]
            self.update()



##class AnimRect(Widget):
##    def anim_to_random_pos(self):
##        Animation.cancel_all(self)
####        random_x = (Window.width - self.width)
##        random_y = (Window.height - self.height)
##        anim = Animation(y=random_y,
##                         duration=4,
##                         t='out_elastic')
##        
####        anim.start(self)
##
##    def FallsDown(self,random_y):
##        ry = random_y - 1
##        anim = Animation(y=ry,
##                         duration=4,
##                         t='out_elastic')
##        Clock.schedule_interval(self.FallsDown, 1/60.)
##        
##    def on_touch_down(self, touch):
##        if self.collide_point(*touch.pos):
##            self.anim_to_random_pos()

runTouchApp(Root())
