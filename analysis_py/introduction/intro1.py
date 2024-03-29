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
prefetchers=['ipcp_isca2020','mlop_dpc3','bingo_dpc3l2','ppfl2','vberti','vbertimix3']
Xlabel = ['IPCP L1D','MLOP L1D','Bingo L2','SPP-PPF L2','Berti L1D','Hyperion L1D']

IPCI = []
for pref in prefetchers:
    metric_data = data.loc[:, (data.iloc[1,:].str.contains(metrics[0])) & 
                            (data.iloc[0,:].str.contains(pref)) ]
    row = data.loc[:,0].str.contains('Average')
    IPCI.append(float((metric_data[row].values)[0][0])-1.3)
print(len(IPCI))
print(IPCI[0])
Accuracy = []
for pref in prefetchers:
    if(pref == 'bingo_dpc3l2' or pref == 'ppfl2'):
        metric_data = data.loc[:, (data.iloc[1,:].str.contains('L2C Accuracy')) & 
                                (data.iloc[0,:].str.contains(pref)) ]
    else:
        metric_data = data.loc[:, (data.iloc[1,:].str.contains('L1D Accuracy')) & 
                                (data.iloc[0,:].str.contains(pref)) ]
    row = data.iloc[:,0].str.contains('Average')
    Accuracy.append(float((metric_data[row].values)[0][0]))

Coverage = []
for pref in prefetchers:
    metric_data = data.loc[:, (data.iloc[1,:].str.contains(metrics[2])) & 
                            (data.iloc[0,:].str.contains(pref)) ]
    row = data.iloc[:,0].str.contains('Average')
    Coverage.append(float((metric_data[row].values)[0][0]))



fig, (ax2,ax3,ax1) = plt.subplots(1,3, figsize=(13, 3.5))
bar_width = 0.75
left_bar_pos = np.arange(len(Xlabel))
print(len(left_bar_pos))

ax1_ytick = [0.0,0.10,0.20,0.30,0.4]

ax1.bar(left_bar_pos + bar_width , IPCI, edgecolor ="black",width= bar_width,hatch="",facecolor="grey",zorder=2)
ax1.set_xticks(left_bar_pos+bar_width)  
ax1.set_yticks(ax1_ytick)
ax1.set_xticklabels(Xlabel,fontsize=12,rotation=45,ha='right')
ax1.set_yticklabels(['1.3','1.4','1.5','1.6','1.7'],fontsize=12,ha='right')
ax1.set_xlabel('(c).IPCI',fontsize=12,ha='center')
ax1.xaxis.set_label_coords(0.45,-0.37)
ax1.set_ylabel('IPCI',fontsize=12,ha='right')
ax1.yaxis.set_label_coords(-0.13, 1.0)
ax1_idx = 0
for item in ax1_ytick:
    if(ax1_idx % 2 == 0):
        ax1.axhline(float(item), color='lightgray', linestyle='-', linewidth=1,zorder=1)
    else:
        ax1.axhline(float(item), color='lightgray', linestyle='--', linewidth=1,zorder=1)
    ax1_idx += 1

# 可选：调整标签的垂直对齐和旋转（根据需要）
# ax1.yaxis.label.set_verticalalignment('bottom')  # 将标签对齐到底部（实际上是顶部，因为它旋转了）
# ax1.yaxis.label.set_rotation(0)  # 将标签旋转为水平

ax2_ytick = [0,0.25,0.50,0.75,1.00]
ax2.bar(left_bar_pos + bar_width , Accuracy, edgecolor ="black",width= bar_width,hatch="",facecolor="grey",zorder=2)
ax2.set_xticks(left_bar_pos+bar_width)  
ax2.set_yticks(ax2_ytick)
ax2.set_xticklabels(Xlabel,fontsize=12,rotation=45,ha='right')
ax2.set_yticklabels(['0','25','50','75','100'],fontsize=12,ha='right')
ax2.set_xlabel('(a).Accuracy',fontsize=12,ha='center')
ax2.xaxis.set_label_coords(0.45,-0.37)
ax2.set_ylabel('Accuracy',fontsize=12,ha='right')
ax2.yaxis.set_label_coords(-0.13, 1.0)
ax2_idx = 0
for item in ax2_ytick:
    if(ax2_idx % 2 == 0):
        ax2.axhline(float(item), color='lightgray', linestyle='-', linewidth=1,zorder=1)
    else:
        ax2.axhline(float(item), color='lightgray', linestyle='--', linewidth=1,zorder=1)
    ax2_idx += 1

ax3_ytick = [0,0.25,0.50,0.75,1.00]
ax3.bar(left_bar_pos + bar_width , Coverage, edgecolor ="black",width= bar_width,hatch="",facecolor="grey",zorder=2)
ax3.set_xticks(left_bar_pos+bar_width)  
ax3.set_yticks(ax3_ytick)
ax3.set_xticklabels(Xlabel,fontsize=12,rotation=45,ha='right')
ax3.set_yticklabels(['0','25','50','75','100'],fontsize=12,ha='right')
ax3.set_xlabel('(b).L1D+L2 Coverage',fontsize=12,ha='center')
ax3.xaxis.set_label_coords(0.45,-0.37)
ax3.set_ylabel('L1D+L2 Coverage',fontsize=12,ha='right')
ax3.yaxis.set_label_coords(-0.13, 1.0)
ax3_idx = 0
for item in ax3_ytick:
    if(ax3_idx % 2 == 0):
        ax3.axhline(float(item), color='lightgray', linestyle='-', linewidth=1,zorder=1)
    else:
        ax3.axhline(float(item), color='lightgray', linestyle='--', linewidth=1,zorder=1)
    ax3_idx += 1

plt.savefig(os.path.join(figure_res,'Intro_ac.png'),dpi=300, format="png", bbox_inches='tight')
plt.savefig(os.path.join(figure_res,'Intro_ac.pdf'),dpi=300, format="pdf", bbox_inches='tight')

