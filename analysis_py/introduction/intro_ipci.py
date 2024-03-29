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
prefetchers=['ip_stride','ipcp_isca2020','mlop_dpc3','bingo_dpc3l2','ppfl2','vberti','vbertimix3']
Xlabel = ['IP-Stride(L1D)','IPCP(L1D)','MLOP(L1D)','Bingo(L2)','SPP-PPF(L2)','Berti(L1D)','Hyperion(L1D)']

IPCI = []
for pref in prefetchers:
    metric_data = data.loc[:, (data.iloc[1,:].str.contains(metrics[0])) & 
                            (data.iloc[0,:].str.contains(pref)) ]
    row = data.loc[:,0].str.contains('Average')
    IPCI.append(float((metric_data[row].values)[0][0])-1.2)
print(len(IPCI))
print(IPCI[0])


fig, ax1 = plt.subplots(1,1, figsize=(3.23, 1.2))
bar_width = 0.7
left_bar_pos = np.arange(len(Xlabel))
print(len(left_bar_pos))

ax1_ytick = [0.0,0.10,0.20,0.30,0.40,0.50]

ax1.bar(left_bar_pos + bar_width , IPCI, edgecolor ="black",width= bar_width,hatch="",facecolor="grey",zorder=2)
ax1.set_xticks(left_bar_pos+bar_width)  
ax1.set_yticks(ax1_ytick)
ax1.set_xticklabels(Xlabel,fontsize=9,rotation=45,ha='right')
ax1.set_yticklabels(['1.2','','1.4','','1.6',''],fontsize=9,ha='right')
ax1.set_ylabel('SpeedUp',fontsize=9,ha='right')
ax1.yaxis.set_label_coords(-0.13, 1.0)
ax1_idx = 0
for item in ax1_ytick:
    if(ax1_idx % 2 == 0):
        ax1.axhline(float(item), color='lightgray', linestyle='-', linewidth=1,zorder=1)
    else:
        ax1.axhline(float(item), color='lightgray', linestyle='--', linewidth=1,zorder=1)
    ax1_idx += 1


plt.savefig(os.path.join(figure_res,'Intro_ipci.png'),dpi=300, format="png", bbox_inches='tight')
plt.savefig(os.path.join(figure_res,'Intro_ipci.pdf'),dpi=300, format="pdf", bbox_inches='tight')

