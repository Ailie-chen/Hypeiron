import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter
import csv
import os
figure_res = 'analysis_py/motivation/'


Bdata = [0.48,0.35,0.58,0.44,0.46,0.36,0.37,0.0,0.58,0.51,0.57,0.46,0.61,0.61,0.53,0.0,0.61]
Cdata = [0.70,0.67,0.84,0.85,0.81,0.85,0.91,0.0,0.80,0.76,0.77,0.75,0.83,0.82,0.80,0.0,0.78]
Xlabel = ['global', 'offset','PC','page','PC+offset','page+offset','PC+page',' ',
'PC and global', 'page and global','PC and offset','page and offset', 'PC and page', 'PC and page+offset','page and PC+offset',
' ','PC and page and global']
fig, ax = plt.subplots(figsize=(6.5, 0.90),dpi=300)
plt.tick_params(axis='x', length=1.2)  # 设置 x 轴刻度线长度为 5
ax1=ax.twinx()
bar_width = 1.0 / (2 + 1.5)
left_bar_pos1 = np.arange(len(Xlabel))
left_bar_pos2 = np.arange(4,7,1)
print(left_bar_pos2)
#粉色：#E57B7F
#深蓝：#033250
#浅蓝：#4BACC6
ax.bar(left_bar_pos1, Bdata, edgecolor ="none",width= bar_width, label = 'Coverage',hatch="",facecolor="#0E5378",zorder=2)
ax.bar(left_bar_pos1 + bar_width * 1.0, Cdata, edgecolor ="none",width= bar_width, label = 'Accuracy',hatch="",facecolor="#4BACC6",zorder=2)
# plt.xticks(left_bar_pos1 + bar_width * 1.5, Xlabel, rotation=45,fontsize=9,ha='center')#

ax.set_xticks(left_bar_pos1+ bar_width *0.5)
print(left_bar_pos1+ bar_width *0.5)
none_names = ['' for item in Xlabel]
ax.set_xticklabels(none_names, fontsize=7,rotation = 10)#,ha ='right'
# 为每个位置添加文本
y_position =-0.015
for x, label in zip(left_bar_pos1+ bar_width * 0.5, Xlabel):
    ax.text(x+0.2, y_position, label, fontsize=7, rotation=25, ha='right', va='top')
ax.set_yticks([0,0.25,0.5,0.75,1.00])
ax.set_yticklabels(['0%','25%','50%','75%','100%'], fontsize=7)
# plt.yticks([0,0.25,0.5,0.75,1.00], ['0%','25%','50%','75%','100%'], fontsize=7,ha='right')
ax1.set_yticks([0.61,0.83])
ax1.set_yticklabels(['61%','83%'], fontsize=7)
ax_idx = 0
for item in [0,0.125,0.25,0.375,0.5,0.75,1.00]:
    if(ax_idx % 2 == 0):
        ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=0.4,zorder=1)
    else:
        ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=0.4,zorder=1)
    ax_idx += 1
ax.axhline(float(0.61), color='#E57B7F', linestyle='--', linewidth=0.5,zorder=1)
ax.axhline(float(0.83), color='#E57B7F', linestyle='--', linewidth=0.5,zorder=1)
for label in ax.get_yticklabels():
    label.set_fontsize(7)
# ax.set_xlabel('Events',fontsize=9,ha='right')
# ax.grid(which='major',axis='y')
ax.legend(loc='upper center', bbox_to_anchor=(0.51, 1.313), ncol=2,fontsize=8,
       handlelength=1.2,     # 控制图例句柄的长度
        handletextpad=0.2,  # 控制图例句柄和文本之间的间距
        columnspacing=0.5,
        edgecolor='none'   )
plt.savefig(os.path.join(figure_res,'1event.png'),dpi=300, format="png", bbox_inches='tight')
plt.savefig(os.path.join(figure_res,'1event.pdf'),dpi=300, format="pdf", bbox_inches='tight')

