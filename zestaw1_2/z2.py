#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Piotr Grabowski
# ETO 2012 zestaw 2
#
from collections import Hashable
import traceback


def conditions(fn):
    """
    Przed wywołaniem metody udekorowanej tym dekoratorem
    zostanie sprawdzony warunek początkowy (jeśli isteniej)
    Po wywołaniu zostanie sprawdzony warunek końcowy (jeśli istnieje)
    oraz inwariant
    """
    def wrapped(self, *args, **kwargs):
        pre = getattr(self, fn.__name__ + "__pre", None)
        if pre is not None:
            pre(*args, **kwargs) 
        ret =  fn(self, *args, **kwargs)
        post = getattr(self, fn.__name__ + "__post", None)
        if post is not None:
            post(*args, **kwargs)
        inv = getattr(self, 'invariant', None)
        if inv is not None:
            inv()
        return ret
    return wrapped


class Set(object):
    def __init__(self):
        self.container = {}

    def invariant(self):
        isinstance(self.container, dict)

    def add__pre(self, obj):
        assert isinstance(obj, Hashable)

    def add__post(self, obj):
        assert self.contains(obj)
    
    @conditions
    def add(self, obj):
        if not self.contains(obj):
            self.container[hash(obj)] = obj
        return obj

    def remove__pre(self, obj):
        assert self.contains(obj)

    def remove__post(self, obj):
        assert self.contains(obj) == False

    @conditions
    def remove(self, obj):
        del self.container[hash(obj)]

    @conditions
    def contains(self, obj):
        return hash(obj) in self.container

    @conditions
    def isEmpty(self):
        return self.size() == 0

    @conditions
    def size(self):
        return len(self.container)


class TestDriver(object):
    """
    Testuje obiekty
    Tę klasę należy dziedziczyć i dopisać własne metody testowe
    zaczynające się od przedrostka 'test'
    Metoda setUp będzie wykonana przed każdym testem,
    Metoda tearDown będzie wykonana po każdym teście

    Aby uruchomić zbiór testów należy wywołać metodę start
    """
    def start(self):
        """
        Przeprowadza testy wywołując metody testowe klasy
        """
        counter = 0
        errors = {}
        passed = 0
        setup = getattr(self, "setUp", None)
        down = getattr(self, "tearDown", None)
        for method in dir(self):
            if method.startswith('test'):
                counter +=1
                try:
                    if setup:
                        setup()
                    getattr(self, method)()
                    if down:
                        down()
                    passed += 1
                    print '.',
                except AssertionError:
                   print 'F',
                   errors[method] = traceback.format_exc()

                except Exception:
                   print 'E',
                   errors[method] = traceback.format_exc()
        print # new line
        for key, value in errors.items():
            print "========="
            print "Test: ", key, "nie powiódł się"
            print value
        print "========="
        print "Wykonano testów: %s. Błędów: %s" % (counter, counter-passed)


class SetTest(TestDriver):
    def setUp(self):
        self.set = Set()
    
    def test_empty_set(self):
        assert self.set.isEmpty()
    
    def test_not_empty_set(self):
        self.set.add(1)
        assert self.set.isEmpty() == False
        
    def test_empty_set_size(self):
        assert self.set.size() == 0
    
    def test_non_empty_set_size(self):
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        assert self.set.size() == 3
    
    def test_add_same_element_dont_change_size(self):
        self.set.add(1)
        self.set.add(1)
        assert self.set.size() == 1

    def test_contains_empty_set(self):
        assert self.set.contains(1) == False

    def test_contains_non_empty_set(self):
        self.set.add(2)
        assert self.set.contains(1) == False

    def test_add_and_contains(self):
        self.set.add(2)
        assert self.set.contains(2) == True

    def test_add_remove(self):
        self.set.add(2)
        self.set.remove(2)
        assert self.set.isEmpty()

    def test_remove_non_exist(self):
        try:
            self.set.remove(1)
            raise Exception('Should raise exception')
        except:
            pass

    def test_add_non_hashable(self):
        try:
            self.set.add([])
            raise Exception('Should raise exception')
        except:
            pass

        
if __name__ == "__main__":
    SetTest().start()
