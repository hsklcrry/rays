# -*- coding: utf-8 -*-
"""
Created on Tue May 29 21:04:39 2018

@author: igeh
"""

x = 1

def f():
    global x
    x = 0
    print(x)
    
print(x)
f()
print(x)