# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 01:12:49 2019

@author: mylen
"""

import os
import numpy as np
import matplotlib.pyplot as plt
#os.chdir(r'c:\Users\s1995204\Documents_LOCAL\Modeling\Modeling_results\1D_models\input_files')

dt_d=1
dt_s=3600*24

t_y=3
t_d=dt_d*365.25*t_y
t_s=dt_s*365.25*t_y

Tmax=10
ref=5


time = np.arange(0, t_d, dt_d)
time_s= np.arange(0, t_s, dt_s)
amplitude   = ref-Tmax*np.cos(2*np.pi*(time/t_d*t_y))

plt.plot(time, amplitude)
plt.title('Sine wave')
plt.xlabel('Time (days)')
plt.ylabel('Amplitude = temperature')
plt.grid(True, which='both')
plt.axhline(y=0, color='k')
plt.show()

data=np.stack((time_s, amplitude), axis=-1)
np.savetxt('sinT_'+str(ref)+'_'+str(Tmax)+'.txt', data)

