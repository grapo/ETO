#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#
# Piotr Grabowski
# ETO 2012
#

import unittest
import logging

from packet import Packet
from node import Link, Workstation, Printer, Fileserver, Finder
from node import Node as NodeBase

# mock w celu testowanie metod NodeBase
class Node(NodeBase):
    def accepted_packet(self, packet):
        pass

class FunctionCalledChecker(object):
    """
    Sprawdza czy funkcja została wywołana
    """
    def __init__(self, method):
        self.meth = method
        self.was_called = False

    def __call__(self, *args, **kwargs):
        self.meth(*args, **kwargs)
        self.was_called = True


class PacketTest(unittest.TestCase):
    def test_invalid_package(self):
        with self.assertRaises(AssertionError):
            Packet()
    
    def test_valid_package(self):
        Packet(content="content", receiver="receiver")
    
    def test_invalid_no_content_package(self):
        with self.assertRaises(AssertionError):
            Packet(sender="sender", receiver="receiver")

    def test_valid_packet_counter(self):
        p = Packet(content="content", receiver="receiver")
        self.assertFalse(p.is_looped())
        for i in range(Packet.MAX_HOP - 1):
            p.hop()

        self.assertFalse(p.is_looped())
    
    def test_invalid_packet_counter(self):
        p = Packet(content="content", receiver="receiver")
        for i in range(Packet.MAX_HOP + 1):
            p.hop()

        self.assertTrue(p.is_looped())


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
        w1 = Node(name="w1")
        self.assertFalse(w1.has_next_node())
    
    def test_has_next_node(self):
        w1 = Node(name="w1")
        w2 = Node(name="w2", next_node=w1)
        self.assertTrue(w2.has_next_node())

    def test_accept_packet_to_node(self):
        w1 = Node(name="w1")
        p = Packet(content="X", receiver="w1", sender="w2")
        w1.accepted_packet = FunctionCalledChecker(w1.accepted_packet)
        w1.accept(p)
        self.assertTrue(w1.accepted_packet.was_called)

    def test_accepted_packet_is_not_resend(self):
        w1 = Node(name="w1")
        p = Packet(content="X", receiver="w1", sender="w2")
        w1.send = FunctionCalledChecker(w1.send)
        w1.accept(p)
        self.assertFalse(w1.send.was_called)

    def test_drop_old_packet(self):
        w1 = Node(name="w1")
        p = Packet(content="X", receiver="w2", sender="w3")
        p._hopcounter = p.MAX_HOP
        w1.drop_packet = FunctionCalledChecker(w1.drop_packet)
        w1.accept(p)
        self.assertTrue(w1.drop_packet.was_called)


class WorkstationTest(unittest.TestCase):
    def test_originate_packet(self):
        w1 = Workstation(name="w1")
        p = Packet(content="X", receiver="w2")
        w1.originate(p)
        self.assertEquals(p.sender, w1.name)


class FileserverTest(unittest.TestCase):
    def test_store_packet(self):
        w1 = Fileserver(name="w1")
        p = Packet(content="X", receiver="w1", sender="w2")
        w1.accept(p)
        self.assertTrue(p in w1.storage)


class LanTest(unittest.TestCase):
    def setUp(self):
        self.mac = Workstation(name="mac")
        self.sun = Workstation(name="sun", next_node=self.mac)
        self.link = Link(name="link", next_node=self.sun)
        self.printer = Printer(name="printer", next_node=self.link)
        self.fileserver = Fileserver(name="fileserver", next_node=self.printer)
        self.pc = Workstation(name="pc", next_node=self.fileserver)
        self.mac.next_node = self.pc

    def test_good_receiver_packet(self):
        p = Packet(content="x", receiver="sun")
        self.mac.originate(p)
        self.assertEquals(self.sun.last_packet, p)

    def test_good_path_packet(self):
        p = Packet(content="x", receiver="sun")
        self.mac.originate(p)
        self.assertEquals(self.pc.last_packet, p)

    def test_loop_in_lan(self):
        # samo to, że ta funkcja działa  świadczy o 
        # tym, że pętle w sieci są obsługiwane
        p = Packet(content="x", receiver="nobody")
        self.mac.originate(p)
        self.assertEquals(p._hopcounter, Packet.MAX_HOP)
        
class FinderTest(unittest.TestCase):
    def setUp(self):
        self.all_stations = ['mac', 'sun', 'printer', 'fileserver', 'pc', 'none']
        self.present_stations = ['mac', 'sun', 'printer', 'fileserver', 'pc']
        class MyFinder(Finder):
            devices = self.all_stations
        
        self.mac = Workstation(name="mac")
        self.sun = Workstation(name="sun", next_node=self.mac)
        self.link = Link(name="link", next_node=self.sun)
        self.printer = Printer(name="printer", next_node=self.link)
        self.finder = MyFinder(name="finder", next_node=self.printer)
        self.fileserver = Fileserver(name="fileserver", next_node=self.finder)
        self.pc = Workstation(name="pc", next_node=self.fileserver)
        self.mac.next_node = self.pc

    def test_none_not_in_all_stations(self):
        self.finder.check_all_nodes()
        nodes = self.finder.list_devices()
        self.assertTrue('none' not in set(nodes))
        
    def test_stations_in_all_stations(self):
        self.finder.check_all_nodes()
        nodes = self.finder.list_devices()
        self.assertTrue(set(nodes) == set(self.present_stations))


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.level = logging.ERROR
    unittest.main()
