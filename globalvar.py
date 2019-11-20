#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
Lock = threading.Lock()


def _init():
    global _global_dict
    _global_dict = {}

def set_value(name, value):
    Lock.acquire()
    _global_dict[name] = value
    Lock.release()

def get_value(name, defValue=None):
    try:
        Lock.acquire()    
        a = _global_dict[name]
        Lock.release()
        return a
    except KeyError:
        return defValue


def get_gl():
    Lock.acquire()    
    a = _global_dict[name]
    Lock.release()    
    return a