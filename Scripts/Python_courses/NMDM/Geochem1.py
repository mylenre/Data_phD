# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 15:58:08 2019

@author: s1995204
"""

string = input('Type some text and hit return:') #  input() function reads text typed by the user (you in this case), with a string argument that will be printed on the screen to ask for inputprint(string)
print(string)
print(len(string))

number = eval(input('Enter a number:')) # for numeric inputs
print(number+number) # addition

#mathematical functions:
    #np.cos(x), np.sin(x), np.tan(x) with angles as arguments (in radians)
    #np.arccos(x) ...
    #np.deg2rad(x), np.rad2deg(x)
    #np.exp(x), np.log(x) 
    #np.sqrt(x), np.log10(x)

import numpy as np
x=[0,45,90]
x_rad=np.deg2rad(x)
x_sin = np.sin(x_rad)

print(x_rad)
print(x_sin)

np.arccos(np.deg2rad(1/np.sqrt(2)))

