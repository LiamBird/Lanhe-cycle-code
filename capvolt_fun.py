import pandas as pd
import numpy as np
from numpy import median
import xlsxwriter
from matplotlib import pyplot as plt

def capvolt_fun(path, filename, cycles_to_show):
    f = path+'\\'+filename+'.txt'
    data = np.asarray(pd.read_csv(f, sep='\t'))

    cycles = 0
    end_line = []
    for i in range(len(data)-1):
        if data[i, 1] == 0 and data[i+1, 1] > 0:
            end_line.append(i)
            cycles = cycles+1

    cyc_length = np.zeros(shape=(len(end_line)), dtype=int)
    for i in range(1, len(end_line)):
        cyc_length[i-1] = end_line[i]-end_line[i-1]


    data_stack = np.full([max(cyc_length), 2, len(cyc_length)], np.nan)

    for i in range(len(cyc_length)-1):
        data_stack[0:cyc_length[i], :, i] = data[end_line[i]:end_line[i+1], :]

    discharge = data_stack[:, :, 0::2]
    charge = data_stack[:, :, 1::2]

    ax = plt.figure(1, figsize=(16,12))
    color_seq = ['k', 'r', 'b', 'g', 'c', 'm']

    for i in cycles_to_show:
            plt.plot(discharge[:, 1, i-1], discharge[:, 0, i-1], label=i, color=color_seq[cycles_to_show.index(i)])
            plt.plot(charge[:, 1, i-1], charge[:, 0, i-1], color=color_seq[cycles_to_show.index(i)])

    plt.legend()
    plt.xlabel('Capacity (mAh)')
    plt.ylabel('Voltage (V)')
    plt.tick_params(axis='both', which='both', direction='in', labelright=False, right=True)
    plt.minorticks_on()
    plt.tick_params(which='minor', direction='in', right=True, left=True, bottom=True, top=True)
    plt.savefig(path+'\\'+filename+'.eps')
    ax.savefig(path+'\\'+filename+'.png')

    capvolt = np.full((max(cyc_length), 4, cycles+1), np.nan)
    for k in range(charge.shape[2]):
        capvolt[:charge.shape[0], 0, k] = charge[:, 0, k]
        capvolt[:charge.shape[0], 1, k] = charge[:, 1, k]
        capvolt[:discharge.shape[0], 2, k] = discharge[:, 0, k]
        capvolt[:discharge.shape[0], 3, k] = discharge[:, 1, k]

    col_titles = ['Voltage (V)', 'Capacity (mAh/g)', 'Voltage (V)', 'Discharge (mAh/g)']
    writer = pd.ExcelWriter(path+'\\'+filename+'_processed.xlsx', engine='xlsxwriter')

    for k in range(charge.shape[2]):
        capvolt_export = pd.DataFrame(capvolt[:, :, k], columns=col_titles)
        capvolt_export.to_excel(writer, sheet_name='Cycle'+str(k+1))
    writer.save()
