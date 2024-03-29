import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter
import csv
import os
import re
from matplotlib.lines import Line2D

directory = "./evaluationmemtense/spec2k17/all_results/1229_page_size.csv"
figure_res = 'analysis_py/evaluation2/sensitive_design/'

data = pd.read_csv(directory, header=None)
prefs_name = data.loc[:,data.loc[0, :].str.contains('Prefetcher')]
prefs_name = np.array(prefs_name.iloc[:, 0])
prefs_name = prefs_name[2:len(prefs_name)]

speedup = data.loc[:,data.loc[0, :].str.contains('IPCI')]
speedup = np.array(speedup.iloc[:, 0])
speedup = speedup[2:len(speedup)]
speedup = [float(item) for item in speedup]

accuracy = data.loc[:,data.loc[0, :].str.contains('L1D Accuracy')]
accuracy = np.array(accuracy.iloc[:, 0])
accuracy = accuracy[2:len(accuracy)]
accuracy = [(float(item)-0.85)*(0.90-0.85)/(1.60-1.55)+1.55 for item in accuracy]

xlabel = []
for pref in prefs_name:
    matches = re.match(r'hyperion_PAGE_(\d+)',pref)
    if matches:
        xlabel.append(matches.group(1))


fig, ax = plt.subplots(figsize=(3.23, 1.3),dpi=300)
left_bar_pos = [item+0.5 for item in np.arange(0,len(xlabel),1)]
ax.plot(left_bar_pos, speedup, linestyle='-', marker='o', markerfacecolor='none',color='black', linewidth=1,markersize=2.5,zorder=2) 
ax2 = ax.twinx()
ax2.plot(left_bar_pos, accuracy, linestyle='-', marker='s', markerfacecolor='grey',color='grey', linewidth=1,markersize=2.5,zorder=2) 

legend_patch = []
legend_patch.append(Line2D([0], [0], linestyle='-', marker='o', markerfacecolor='none', color='black', lw=1, markersize=2.5, label='Speedup'))
legend_patch.append(Line2D([0], [0], linestyle='-', marker='s', markerfacecolor='grey', color='grey', lw=1, markersize=2.5, label='Accuracy'))

ax.set_xticks(left_bar_pos)  
ax.set_yticks(np.arange(155, 161,1)/100)
ax.set_xticklabels(xlabel,fontsize=9,ha='center')
ax.set_xlabel('Regions/KB')
ax.set_yticklabels(['{:.2f}'.format(item) for item in np.arange(155, 161,1)/100],fontsize=9,ha='right')
ax.set_ylabel('SpeedUp') 
ax2.set_yticks(np.arange(155, 161,1)/100)
ax2.set_yticklabels(['{:.2f}'.format(item) for item in np.arange(85, 91,1)/100],fontsize=9,ha='left')
ax2.set_ylabel('L1D Accuracy') 

ax.set_ylim(1.55, 1.60) 

ax.legend(handles=legend_patch,loc='upper center', bbox_to_anchor=(0.5, 1.3), ncol=3, fontsize=8,
             # y 参数控制标题的位置
        handlelength=1.2,     # 控制图例句柄的长度
        handletextpad=0.2,  # 控制图例句柄和文本之间的间距
        columnspacing=0.5,
        edgecolor='black'   )
ax_idx = 0
for item in np.arange(1550, 1610,5)/1000:
    if(ax_idx % 2 == 0):
        ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=1,zorder=1)
    else:
        ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=1,zorder=1)
    ax_idx += 1

plt.savefig(os.path.join(figure_res,'page_size.png'),dpi=300, format="png", bbox_inches='tight')
plt.savefig(os.path.join(figure_res,'page_size.pdf'),dpi=300, format="pdf", bbox_inches='tight')

