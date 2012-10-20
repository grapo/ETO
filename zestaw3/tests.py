#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Piotr Grabowski
# ETO 2012 zestaw 2
#

import unittest
from packet import Packet
from workstation import Workstation


class PacketTest(unittest.TestCase):
    def test_invalid_package(self):
        with self.assertRaises(AssertionError):
            Packet()
    
    def test_valid_package(self):
        Packet(content="content", sender="sender", receiver="receiver")
    
    def test_invalid_no_content_package(self):
        with self.assertRaises(AssertionError):
            Packet(sender="sender", receiver="receiver")

class WorkstationTest(unittest.TestCase):
    def test_has_not_next_node(self):
        w1 = Workstation(name="w1")
        self.assertFalse(w1.hasNextNode())
    
    def test_has_next_node(self):
        w1 = Workstation(name="w1")
        w2 = Workstation(name="w2", nextNode=w1)
        self.assertTrue(w2.hasNextNode())


class LanTest(unittest.TestCase):
    def setUp(self):
        self.mac = Workstation(name="mac")
        self.sun = Workstation(name="sun", nextNode=self.mac)
        self.pc = Workstation(name="pc", nextNode=self.sun)
        self.mac.nextNode = self.pc

    def test_good_receiver_packet(self):
        p = Packet(content="x", sender="mac", receiver="sun")
        self.mac.send(p)
        self.assertEquals(self.sun.last_packet, p)

    def test_good_path_packet(self):
        p = Packet(content="x", sender="mac", receiver="sun")
        self.mac.send(p)
        self.assertEquals(self.pc.last_packet, p)
        


if __name__ == "__main__":
    unittest.main()
