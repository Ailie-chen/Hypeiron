import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter
import csv
import os
data_csv = 'evaluationmemtense/spec2k17/all_results_figs/1155.csv'
figure_res = 'analysis_py/introduction/'
data = pd.read_csv(data_csv,header=None)
metrics=['IPCI','Accuracy','Global Coverage']
num_null = 0
prefetchers=['ip_stride','ipcp_isca2020','mlop_dpc3','bingo_dpc3l2','ppfl2','vberti','vbertimix3']
Xlabel = ['IP-Stride(L1D)','IPCP(L1D)','MLOP(L1D)','Bingo(L2)','SPP-PPF(L2)','Berti(L1D)','Hyperion(L1D)']

Accuracy = []
for pref in prefetchers:
    if(pref == 'bingo_dpc3l2' or pref == 'ppfl2'):
        metric_data = data.loc[:, (data.iloc[1,:].str.contains('L2C Accuracy')) & 
                                (data.iloc[0,:].str.contains(pref)) ]
        row = data.iloc[:,0].str.contains('Average')
        Accuracy.append(float((metric_data[row].values)[0][0]))
    elif(pref == 'null'):
         Accuracy.append(0)
    else:
        metric_data = data.loc[:, (data.iloc[1,:].str.contains('L1D Accuracy')) & 
                                (data.iloc[0,:].str.contains(pref)) ]
        row = data.iloc[:,0].str.contains('Average')
        Accuracy.append(float((metric_data[row].values)[0][0]))
    

Coverage = []
for pref in prefetchers:
    if(pref == 'null'):
        Coverage.append(0)
    else:
        metric_data = data.loc[:, (data.iloc[1,:].str.contains(metrics[2])) & 
                                (data.iloc[0,:].str.contains(pref)) ]
        row = data.iloc[:,0].str.contains('Average')
        Coverage.append(float((metric_data[row].values)[0][0]))




fig, ax1 = plt.subplots(1,1, figsize=(3.23, 1.3))
bar_width = 1.0/(2+1)
left_bar_pos = np.arange(len(Xlabel)+num_null)
print(len(left_bar_pos))

ax1_ytick = [0,0.25,0.50,0.75,1.00]
ax1_ytick1 = [0,0.125,0.25,0.375,0.50,0.625,0.750,0.875]
ax1.bar(left_bar_pos + bar_width , Accuracy, edgecolor ="black",width= bar_width,hatch="",facecolor="grey",label='Accuracy',zorder=2)
ax1.bar(left_bar_pos + bar_width+bar_width , Coverage, edgecolor ="black",width= bar_width,hatch="",facecolor="black",label='Coverage',zorder=2)
ax1.set_xticks([item+bar_width*1.5 for item in [0,1,2,3,4,5+num_null,6+num_null]])  
ax1.set_yticks(ax1_ytick)
ax1.set_xticklabels(Xlabel,fontsize=9,ha='right',rotation=45)
ax1.set_yticklabels(['0','25','50','75','100'],fontsize=9,ha='right')
# ax1.set_xlabel('(a).Accuracy and Coverage in SPEC-MemInt',fontsize=9,ha='center')
# ax1.xaxis.set_label_coords(0.45,-0.15)
# ax1.set_ylabel('Accuracy',fontsize=9,ha='right')
# ax1.yaxis.set_label_coords(-0.045, 1.0)
ax1_idx = 0
for item in ax1_ytick1:
    if(ax1_idx % 2 == 0):
        ax1.axhline(float(item), color='lightgray', linestyle='-', linewidth=1,zorder=1)
    else:
        ax1.axhline(float(item), color='lightgray', linestyle='--', linewidth=1,zorder=1)
    ax1_idx += 1
ax1.legend(bbox_to_anchor=(0.3, 1), loc='upper center', fontsize=6)

plt.savefig(os.path.join(figure_res,'Intro_ac.png'),dpi=300, format="png", bbox_inches='tight')
plt.savefig(os.path.join(figure_res,'Intro_ac.pdf'),dpi=300, format="pdf", bbox_inches='tight')

