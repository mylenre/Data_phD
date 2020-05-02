# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 19:58:32 2019

@author: Boris & Mylene
"""
import os
import numpy as np
os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\2D_Mine_Models\Benchmark\TH\Layers')
filename = "Complex.geo"

# Initialising a dictionary to store the variables, a dictionary is a container where you access a value with a key: ex to add an entry mydict["Boris"] = 27; access the entry: print(mydict["Boris"] ) -> and it will display 27
variables = {}
# I will first store my points into a list. Just remember that point (1) will be 0
Point = []
Point_name = []

with open(filename, 'r') as glifile: 
  for line in glifile:
    # print(line)
    # I am jsut reading the variables so far, break will break the loop when the condition is reached
    if("//" in line):
      break
    # I fmy line is empty or only contains a space, I ignore it
    if(len(line)<=1):
      continue
    #Alright, here I am (i) getting rid of the spaces, (ii) getting rid of the ; and (iii) transforming w=1000 into a python list of string ["w","1000"]
    this_line = line.replace(" ","").replace(";","").split("=")
    try:
      variables[this_line[0]]=float(this_line[1])
    except ValueError:
      # Eval is used to take a string (expression) and return the result. You can provide a dictionarry of string which will be converted to variables within that eval
      this_val = eval(this_line[1], variables)
      variables[this_line[0]]=this_val
# There is a bug that add a key to the dictionary from some reason (not bad but annoying when you print all the values as follow)
variables.pop("__builtins__",None)
for key,val in variables.items():
  print("key:", key,"val",val)

# Alright We now have loaded our values, let's read the rest
with open(filename, 'r') as glifile: 
  for line in glifile:
    if "Point(" in line:
      # weeeeeeeeeeeeeeeeeeeee
      this_line_pt = line.replace(" ", "").replace(";","").replace("{","").replace("}","").split("=")[0]
      this_line = line.replace(" ", "").replace(";","").replace("{","").replace("}","").split("=")[1].split(",") # output of line 12 -> [0,0,0,lc]
      this_point = []
      for i in range(len(this_line)):
        this_point.append(eval(this_line[i],variables))
      Point.append(this_point)
      Point_name.append(this_line_pt)
      
# We have all the point, lets convert it to a numpy array
Point = np.array(Point)
# Array a 2 dimension: chaque ligne correspond a un point

#Access to the first col ( is it x ??)
print(Point[:,0]) # -> I want all the lines (:) but just the first col (0)

nb = np.arange(len(Point))
x = Point[:,0]
y = Point[:,1]
z = Point[:,2]
tab=np.vstack((nb,x,y,z)).T
#tab = Point.reshape((len(Point),4))
#np.savetxt(filename+'.gli', tab, fmt='%s')


with open(filename+'.gli', 'w') as outfile:
    outfile.write('# POINT\n')
    np.savetxt(outfile, tab, fmt='%d %s %s %s') #
    outfile.write('# STOP\n')
                  