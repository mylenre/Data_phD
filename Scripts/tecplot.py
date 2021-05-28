# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 15:25:27 2021

@author: s1995204
"""
from os import path
from numpy import histogram
import tecplot 
if '-c' in sys.argv:
    tecplot.session.connect()

tecplot.new_layout()
with tecplot.session.suspend():
        ds = tecplot.active_frame().dataset
        air_rem = ds.zone('')