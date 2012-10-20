#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Piotr Grabowski
# Michał Karpiński
# ETO 2012 zestaw 3
#

class Packet(object):
    def __init__(self, sender=None, receiver=None, content=None):
        self.content = content
        self.receiver = receiver
        self.sender = sender

        assert self.invariant()

    def invariant(self):
        return self.content and self.receiver and self.sender

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
    
