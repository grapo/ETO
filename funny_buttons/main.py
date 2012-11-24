from os.path import dirname, abspath
import os.path

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

import pygst
pygst.require("0.10")
import gst


class Player(object):
    def __init__(self, music_files):
        self.music_files = music_files
        self.player = gst.element_factory_make("playbin2", "player")

    def play(self, number):
        self.player.set_state(gst.STATE_NULL)
        if number > len(self.music_files):
            number = len(self.music_files) - 1
        if number < 0:
            number = 0
        
        self.player.set_property("uri", "file://" + self.music_files[number])
        self.player.set_state(gst.STATE_PLAYING)


class MyApp(App):
    music_files = ['animals001.mp3', 'animals010.mp3', 'animals011.mp3']

    def __init__(self, *args, **kwargs):
        dirpath = dirname(abspath( __file__ ))
        mfiles = []
        for m_file in self.music_files:
            mfiles.append(os.path.join(dirpath, m_file))
        
        self.player = Player(mfiles) 
        super(MyApp, self).__init__(*args, **kwargs)

    def build(self):
        parent = BoxLayout(orientation='vertical')
       
        def make_play(number):
            def play(obj):
                self.player.play(number)    
            return play
        
        for i, f in enumerate(self.music_files):
            button = Button(text=str(f))
            button.bind(on_press=make_play(i))
            parent.add_widget(button)

        return parent


if __name__ == '__main__':
    MyApp().run()
