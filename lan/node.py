#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Piotr Grabowski
# ETO 2012
#

import logging
logging.basicConfig(level=logging.INFO)

class Node(object):
    def __init__(self, name, next_node=None):
        self._name = name
        self.next_node = next_node
        self._last_packet = None

    @property 
    def next_node(self):
        return self._next_node

    @next_node.setter
    def next_node(self, value):
        assert value is None or isinstance(value, Node)
        self._next_node = value

    def has_next_node(self):
        return bool(self._next_node)
    
    @property 
    def last_packet(self):
        return self._last_packet

    @property 
    def name(self):
        return self._name

    def drop_packet(self, packet):
        pass

    def accept(self, packet):
        self._last_packet = packet
        if packet.receiver == self._name:
            self.accepted_packet(packet)
        else:
            packet.hop()
            if packet.is_looped():
                self.drop_packet(packet)
                return
            self.send(packet)

    def accepted_packet(self, packet):
        pass

    def send(self, packet):
        if self.has_next_node():
            self.next_node.accept(packet)


class Workstation(Node):
    def accepted_packet(self, packet):
        logging.info("Received: %s" % (packet))

    def originate(self, packet):
        packet.sender = self._name
        self.send(packet)


class Printer(Node):
    def accepted_packet(self, packet):
        logging.info("Print packet: %s" % (packet))


class Fileserver(Node):
    def __init__(self, *args, **kwargs):
        super(Fileserver, self).__init__(*args, **kwargs)
        self.storage = []

    def accepted_packet(self, packet):
        self.storage.append(packet)
        logging.info("Save packet: %s" % (packet))


