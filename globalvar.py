#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
Lock = threading.Lock()


def _init():
    global _global_dict
    _global_dict = {}

def set_value(name, value):
    name = str(name)
    Lock.acquire()
    _global_dict[name] = value
    Lock.release()

def get_value(name, defValue=None):
    name = str(name)
    if name not in _global_dict:
        return None
    else:
        Lock.acquire()    
        a = _global_dict[name]
        Lock.release()
        return a


def get_gl():
    Lock.acquire()    
    a = _global_dict
    Lock.release()    
    return a