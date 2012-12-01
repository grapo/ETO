#
# Autor: Piotr Grabowski
# Zadanie wykonywane w ramach ETO 2012
#

from os.path import dirname, abspath
import os.path

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton

from player import Player

class Line(Widget):
    velocity_x = NumericProperty(1)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class Dot(object):
    def __init__(self, pos, sound):
        self.x, self.y = map(int, pos)
        self.sound = sound

    def touch(self):
        self.sound.play()


class SoundDots(Widget):
    SIZE = 20
    def __init__(self, *args, **kwargs):
        self.dots = []
        return super(SoundDots, self).__init__(*args, **kwargs)

    def on_touch_down(self, touch):
        # nacisniecie przyciksu w obszarze rysowania tworzy kropke z dzwiekiem
        # jest jakis przycisk radio jest zaznaczony

        with self.canvas:
            buttons = ToggleButton.get_widgets('sounds')
            for button in buttons:
                if button.state == 'down':
                    pos = (touch.x - self.SIZE / 2, touch.y - self.SIZE / 2)
                    self.create_dot(pos, button.color, button.player)
            del buttons

    def create_dot(self, pos, color, player):
        Color(*color, mode='rgb')
        Ellipse(pos=pos, size=(self.SIZE, self.SIZE))
        self.dots.append(Dot(pos,player))


class Stave(Widget):
    SPEED = 4 # predkosc poruszania sie lini
    line = ObjectProperty(None)
    sound_dots = ObjectProperty(None)

    def line_position(self):
        self.line.pos = self.pos
        self.line.velocity = Vector(Stave.SPEED,0)

    def update(self, dt):
        self.line.move()
        # jesli napotkam krokpe na drodze to wykonuje akcje
        for dot in self.sound_dots.dots:
            if self.line.x in range(dot.x-1, dot.x+Stave.SPEED-1):
                dot.touch()
        if self.line.right > self.width:
            return False
        

class Controller(BoxLayout):
    stave = ObjectProperty(None)

    def start(self):
        self.stave.line_position()
        Clock.unschedule(self.stave.update)
        Clock.schedule_interval(self.stave.update, 1.0/60.0)


class MyApp(App):
    music_files = ['1.mp3', '2.mp3', '3.mp3']

    def __init__(self, *args, **kwargs):
        dirpath = dirname(abspath( __file__ ))
        self.players = []
        # dla kazdego pliku dzwiekowego tworze odtwarzacz
        for m_file in self.music_files:
            file_path = os.path.join(dirpath, m_file)
            self.players.append(Player(file_path))

        super(MyApp, self).__init__(*args, **kwargs)

    def build(self):
        controller = Controller()
        # przypisuje odtwarzacze do przycisku zeby potem mozne je bylo latwo odnalezc
        buttons = ToggleButton.get_widgets('sounds')
        for i, button in enumerate(buttons):
            if len(self.players) > i:
                button.player = self.players[i]
            else:
                button.player = self.players[-1]
        # z jakiegos powodu w kivy trzeba to usunac explicite
        del buttons

        return controller


Factory.register("Line", Line)
Factory.register("SoundDots", SoundDots)
Factory.register("Stave", Stave)

if __name__ == '__main__':
    MyApp().run()
