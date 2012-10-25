#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Piotr Grabowski
# ETO 2012 zestaw 2
#

import unittest
from packet import Packet
from workstation import Node, Workstation


class PacketTest(unittest.TestCase):
    def test_invalid_package(self):
        with self.assertRaises(AssertionError):
            Packet()
    
    def test_valid_package(self):
        Packet(content="content", sender="sender", receiver="receiver")
    
    def test_invalid_no_content_package(self):
        with self.assertRaises(AssertionError):
            Packet(sender="sender", receiver="receiver")

class NodeTest(unittest.TestCase):
    def test_next_node_is_node(self):
        n1 = Node(name="n1")
        n2 = Node(name="n2")
        try:
            n1.next_node = n2
        except:
            self.fail('Exception should not be raised')
    
    def test_next_node_is_not_node(self):
        n1 = Node(name="n1")
        with self.assertRaises(AssertionError): 
            n1.next_node = "n2"

    def test_has_not_next_node(self):
        w1 = Workstation(name="w1")
        self.assertFalse(w1.has_next_node())
    
    def test_has_next_node(self):
        w1 = Workstation(name="w1")
        w2 = Workstation(name="w2", next_node=w1)
        self.assertTrue(w2.has_next_node())


class LanTest(unittest.TestCase):
    def setUp(self):
        self.mac = Workstation(name="mac")
        self.sun = Workstation(name="sun", next_node=self.mac)
        self.node = Workstation(name="node", next_node=self.sun)
        self.pc = Workstation(name="pc", next_node=self.node)
        self.mac.next_node = self.pc

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
