#
# Autor: Piotr Grabowski
# Zadanie wykonywane w ramach ETO 2012
#

import pygst
pygst.require("0.10")
import gst


class Player(object):
    def __init__(self, music_file):
        self.player = gst.element_factory_make("playbin2", "player")
        self.player.set_property("uri", "file://" + music_file)

    def play(self):
        self.player.set_state(gst.STATE_NULL)
        self.player.set_state(gst.STATE_PLAYING)


