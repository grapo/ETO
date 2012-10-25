#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Piotr Grabowski
# ETO 2012
#

class Packet(object):
    MAX_HOP = 16
    def __init__(self, sender=None, receiver=None, content=None):
        self.content = content
        self.receiver = receiver
        self.sender = sender
        self._hopcounter = 0
        assert self.invariant()

    def invariant(self):
        return self.content and self.receiver
    
    def __unicode__(self):
        return self.content

    def __str__(self):
        return self.content

    def hop(self):
        self._hopcounter += 1

    def is_looped(self):
        return self._hopcounter >= self.MAX_HOP

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value
    
    @property
    def receiver(self):
        return self._receiver

    @receiver.setter
    def receiver(self, value):
        self._receiver = value
    
    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, value):
        self._sender = value
    
