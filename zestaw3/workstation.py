#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Piotr Grabowski
# Michał Karpiński
# ETO 2012 zestaw 3
#

class Workstation(object):
    def __init__(self, name=None, nextNode=None):
        self._name = name
        self.nextNode = nextNode
        self._last_packet = None

    @property 
    def nextNode(self):
        return self._nextNode

    @nextNode.setter
    def nextNode(self, value):
        assert value is None or isinstance(value, Workstation)
        self._nextNode = value

    def hasNextNode(self):
        return bool(self._nextNode)
    
    @property 
    def last_packet(self):
        return self._last_packet

   
    def accept(self, packet):
        self._last_packet=packet
        if packet.receiver == self._name:
            print "Receiver: %s, packet: %s" % (self._name, packet.content)
        else:
            self.send(packet)

    def send(self, packet):
        if self.hasNextNode():
            self.nextNode.accept(packet)

    def originate(self, packet):
        self.send(packet)

