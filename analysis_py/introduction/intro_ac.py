import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter
import csv
import os
data_csv = 'evaluationmemtense/spec2k17/all_results/1155.csv'
figure_res = 'analysis_py/introduction/'
data = pd.read_csv(data_csv,header=None)
metrics=['IPCI','Accuracy','Global Coverage']
num_null = 0
prefetchers=['bingo_dpc3l2','ppfl2','null','ipcp_isca2020','mlop_dpc3','ip_stride','vberti']
Xlabel = ['Bingo(L2)','SPP-PPF(L2)','','IPCP(L1D)','MLOP(L1D)','IP-Stride(L1D)','Berti(L1D)']

prefetchers_coverage=['bingo_dpc3l2','ppfl2','null','ip_stride','mlop_dpc3','ipcp_isca2020','vberti']
Xlabel_coverage = ['Bingo(L2)','SPP-PPF(L2)','','IP-Stride(L1D)','MLOP(L1D)','IPCP(L1D)','Berti(L1D)']

Accuracy = []
for pref in prefetchers:
    if(pref == 'bingo_dpc3l2' or pref == 'ppfl2'):
        col_idx = data.iloc[0,:]=='L2C Accuracy'
        row_idx = data.loc[:,1]==pref
        metric_data = data.loc[row_idx,col_idx].values
        print(metric_data[0][0])
        Accuracy.append(float(metric_data[0][0]))
    elif(pref == 'null'):
         Accuracy.append(0)
    else:
        col_idx = data.iloc[0,:]=='L1D Accuracy'
        row_idx = data.loc[:,1]==pref
        metric_data = data.loc[row_idx,col_idx].values
        print(metric_data[0][0])
        Accuracy.append(float(metric_data[0][0]))
    
print("\n")
Coverage = []
for pref in prefetchers_coverage:
    if(pref == 'bingo_dpc3l2' or pref == 'ppfl2'):
        col_idx = data.iloc[0,:]=='L2C Coverage'
        row_idx = data.loc[:,1]==pref
        metric_data = data.loc[row_idx,col_idx].values
        print(metric_data[0][0])
        Coverage.append(float(metric_data[0][0]))
    elif(pref == 'null'):
         Coverage.append(0)
    else:
        col_idx = data.iloc[0,:]=='L1D Coverage'
        row_idx = data.loc[:,1]==pref
        metric_data = data.loc[row_idx,col_idx].values
        print(metric_data[0][0])
        Coverage.append(float(metric_data[0][0]))




fig, ax1 = plt.subplots(1,1, figsize=(2.5, 1.0))
bar_width = 1.0/(1)
left_bar_pos = np.arange(len(Xlabel)+num_null)
print(len(left_bar_pos))

ax1_ytick = np.around(np.arange(0.6, 1.01, 0.1), decimals=1)
ax1_ytick1 = np.around(np.arange(0.6, 1.01, 0.05), decimals=2)
ax1.bar(left_bar_pos , Accuracy, edgecolor ="black",width= bar_width,hatch="",facecolor="grey",label='Accuracy',zorder=2)
ax1.set_xticks(left_bar_pos)  
ax1.set_yticks(ax1_ytick)
ax1.set_xticklabels(Xlabel,fontsize=9,ha='right',rotation=45)
ax1.set_yticklabels(['60','70','80','90','100'],fontsize=9,ha='right')
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
ax1.set_ylim(0.6, 1.0)
plt.savefig(os.path.join(figure_res,'Intro_a.png'),dpi=300, format="png", bbox_inches='tight')
plt.savefig(os.path.join(figure_res,'Intro_a.pdf'),dpi=300, format="pdf", bbox_inches='tight')
plt.close()

fig, ax1 = plt.subplots(1,1, figsize=(2.5, 1.0))
bar_width = 1.0/(1)
left_bar_pos = np.arange(len(Xlabel)+num_null)
print(len(left_bar_pos))
ax1_ytick = np.around(np.arange(0.30, 0.91, 0.15), decimals=2)
print(ax1_ytick)
ax1_ytick1 = np.around(np.arange(0.3, 0.91, 0.075), decimals=3)
ax1.bar(left_bar_pos , Coverage, edgecolor ="black",width= bar_width,hatch="",facecolor="grey",label='Coverage',zorder=2)
ax1.set_xticks(left_bar_pos)  
ax1.set_yticks(ax1_ytick)
ax1.set_xticklabels(Xlabel_coverage,fontsize=9,ha='right',rotation=45)
ax1.set_yticklabels(['30','45','60','75','90'],fontsize=9,ha='right')
ax1.set_ylim(0.3, 0.9)
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

plt.savefig(os.path.join(figure_res,'Intro_c.png'),dpi=300, format="png", bbox_inches='tight')
plt.savefig(os.path.join(figure_res,'Intro_c.pdf'),dpi=300, format="pdf", bbox_inches='tight')