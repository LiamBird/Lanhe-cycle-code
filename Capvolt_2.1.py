import os
import glob
import pandas as pd
import numpy as np
from numpy import median
from matplotlib import pyplot as plt


## Importing data from text file
path = r'C:\Users\laure\Dropbox\DATA\Capvolt\(0-0-1)(10-0)T'
filename = r'(0-0-1)(10-0)T_3'
f = path+'\\'+filename+'.txt'
data = np.asarray(pd.read_csv(f, sep='\t'))

## Column 0: Voltage (V)
## Column 1: Capacity (mAh)

cycles = 0
end_line = []
for i in range(len(data)-1):
    if data[i, 1] == 0 and data[i+1, 1] > 0:
        end_line.append(i)
        cycles = cycles+1                           # Can print cycles to check correct

cyc_length = np.zeros(shape=(len(end_line)), dtype=int)
for i in range(1, len(end_line)):
    cyc_length[i-1] = end_line[i]-end_line[i-1]


data_stack = np.full([max(cyc_length), 2, len(cyc_length)], np.nan)

for i in range(len(cyc_length)-1):
    data_stack[0:cyc_length[i], :, i] = data[end_line[i]:end_line[i+1], :]

discharge = data_stack[:, :, 0::2]
charge = data_stack[:, :, 1::2]

ax = plt.figure(1)
cycles_to_show = [0, 1, 9]
color_seq = ['k', 'r', 'b', 'g', 'c', 'm']

for i in cycles_to_show:
        plt.plot(discharge[:, 1, i], discharge[:, 0, i], label=i+1, color=color_seq[cycles_to_show.index(i)])
        plt.plot(charge[:, 1, i], charge[:, 0, i], color=color_seq[cycles_to_show.index(i)])

plt.legend()
plt.xlabel('Capacity (mAh)')
plt.ylabel('Voltage (V)')
plt.tick_params(axis='both', which='both', direction='in', labelright=False, right=True)
plt.minorticks_on()
plt.tick_params(which='minor', direction='in', right=True, left=True, bottom=True, top=True)
##plt.ylim([1.7, 2.8])
plt.show()


