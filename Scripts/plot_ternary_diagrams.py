# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 12:20:00 2020

@author: s1995204
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import seaborn as sns
import pandas as pd
import ternary
import os

os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\NEW')
df=pd.read_csv('ternary_digrams.txt', delimiter=',', index_col=0)
df['Heat Capacity'] = df['Specific Heat Capacity'].mul(df['Rock Density'])

scenario = list(df.index)
properties = list(df .keys())

# scale all properties between 0 and 100
dfmax = df.max(axis=0)
dfmin = df.min(axis=0)
y = 100/(dfmax-dfmin)
offset = y * dfmin
df_new = df.mul(y) - offset
#thermal
data = {'Heat Conductivity': ['HC1','HC2','HC3','HC4','HC5'],     # 0
        'Specific Heat Capacity': ['Hc1','Hc2'],                  # 1
        'Geothermal Gradient': ['G1','G2'],                       # 2
        'Hydraulic Conductivity Rock': ['KR1','KR2','KR3','HC4'],       # 3
        'Hydraulic Conductivity Seams': ['KS1','KS2','KS3','KS4'],     # 4
        'Head Gradient':['H1','H2','H3'],                         # 5
        'Rock Density': ['HD1','HD2'],                            # 6
        'Rock Porosity' : ['Pr1','Pr2'],                          # 7
        'Seam Porosity': ['Ps1','Ps2','Ps3','Ps4'],               # 8
        'Pumping Depth': ['B1','B2'],                             # 9
        'Pumping Rate': ['PR1','PR2','PR3','PR4'],                # 10
        'Mined Volume ': ['MV1','MV2', 'MV3','MV4'],             # 11
        'Heat Capacity': ['Hc1','Hc2']}               # 12
scenario = ['S1','S2','S3','S4']
unit = {'Heat Conductivity': ' (W/°C.m)',
        'Specific Heat Capacity': ' 9(J/Kg.°C)',
        'Geothermal Gradient': ' $\\alpha_{th} $ (°C/km)',
        'Hydraulic Conductivity Rock': ' $K_{h}^r$ (m/s)',
        'Hydraulic Conductivity Seams': ' $K_{h}^s$ (m/s)',
        'Head Gradient':' $\\alpha_h$ (m)',
        'Rock Density': ' (kg/m^3)',
        'Rock Porosity' : ' (%)',
        'Seam Porosity': ' (%)',
        'Pumping Depth': ' (m)',
        'Pumping Rate': ' $(m^3/s)$',
        'Mined Volume ': ' $(m^3)$',
        'Heat Capacity': ' $J/°C.m^3$'}

a = list(data.keys())[10]
b = list(data.keys())[9]
c = list(data.keys())[2]

title = "Ternary diagram"
fontsize = 10
name='thermal_5'
#%% calculate ternary plots heat properties
sample= df_new[[a, b, c]] 
tt = sample.sum(axis=1)
sample_ = sample.div(tt,axis='index') * 100
sample_['Energy Change'] = df['Energy Change']
select = sample_.loc[data[a]+data[b]+data[c]]
val = select['Energy Change']

fig, tax = ternary.figure(scale=100)
fig.set_size_inches(6, 5)
tax.scatter(select[[a , b, c]].values, c=val, cmap='Spectral_r', vmin=min(val), vmax=max(val))

# Draw Boundary and Gridlines
tax.boundary(linewidth=2.0)
tax.gridlines(color="black", multiple=10)

# Set Axis labels and Title
tax.set_title(title, fontsize=fontsize)
tax.left_axis_label(c + unit[a], fontsize=fontsize)
tax.bottom_axis_label(a + unit[a], fontsize=fontsize)
tax.right_axis_label(b + unit[b], fontsize=fontsize)
# Set ticks
tax.ticks(axis='lbr', multiple=10, linewidth=0.1,fontsize=8)
# Remove default Matplotlib Axes
tax.clear_matplotlib_ticks()
tax.get_axes().axis('off')

for label,x,y,z in zip(list(select.index), select[a], select[b], select[c]):
    tax.annotate(label, # this is the text
                 (x,y,z), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(-5,-5), # distance from text to points (x,y)
                 ha='center',
                 fontsize=8) # horizontal alignment can be left, right or center
#figure, tax = ternary.figure(scale=scale)
#tax.heatmap(data, scale, cmap = None, style="hexagonal", use_rgba=True)
#tax.boundary()
#%%
ai = np.array(select[c])
bi = np.array(select[a])
ci = np.array(select[b])
v = np.array(val)
# translate the data to cartesian corrds
x = 50 * ( 2.*bi+ci ) / ( ai+bi+ci )
y = 50*np.sqrt(3) * ci / (ai+bi+ci)

# create a triangulation out of these points
T = tri.Triangulation(x,y)

# plot the contour
plt.tricontourf(x,y,T.triangles,v)

# create the grid
corners = np.array([[0, 0], [100, 0], [50,  np.sqrt(3)*50]])
triangle = tri.Triangulation(corners[:, 0], corners[:, 1])

# creating the grid
refiner = tri.UniformTriRefiner(triangle)
trimesh = refiner.refine_triangulation(subdiv=0)

#plotting the mesh
plt.triplot(trimesh, alpha=0.2)
plt.set_cmap('hot_r')

#tax.savefig('ternary_hf_'+str(name)+'.png', facecolor='w')
