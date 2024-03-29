import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter
import csv
import os
figure_res = 'analysis_py/motivation/'

figsize=(3.23, 1.3)
Bdata = [0.59,0.58,0.59,0.61]
Cdata = [0.84,0.77,0.8,0.83]
Xlabel = ['PC(Berti)', 'PC and Offset','PC and Global','PC and Page']
# 8.20 cm , 3.30 cm
fig, ax = plt.subplots(figsize=(3.23, 1.3),dpi=300)
bar_width = 1.0 / (2 + 1.5)
left_bar_pos1 = np.arange(len(Xlabel))
ax.bar(left_bar_pos1 + bar_width * 1.0, Bdata, edgecolor ="black",width= bar_width, label = 'Coverage',hatch="",facecolor="grey",zorder=2)
ax.bar(left_bar_pos1 + bar_width * 2.0, Cdata, edgecolor ="black",width= bar_width, label = 'Accuracy',hatch="",facecolor="black",zorder=2)
plt.xticks(left_bar_pos1 + bar_width * 1.5, Xlabel,fontsize=8,rotation=12,ha='center')#rotation=45,


plt.yticks([0,0.25,0.5,0.75,1.00], ['0%','25%','50%','75%','100%'], fontsize=9,ha='right')
ax_idx = 0
for item in [0,0.25,0.5,0.75,1.00]:
    if(ax_idx % 2 == 0):
        ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=1,zorder=1)
    else:
        ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=1,zorder=1)
    ax_idx += 1

for label in ax.get_yticklabels():
    label.set_fontsize(9)
# ax.set_xlabel('Two Events',fontsize=9,ha='center')
# ax.grid(which='major',axis='y')
ax.legend(loc='upper center', bbox_to_anchor=(0.51, 1.30), ncol=2,fontsize=8,
       handlelength=1.2,     # 控制图例句柄的长度
        handletextpad=0.2,  # 控制图例句柄和文本之间的间距
        columnspacing=0.5,
        edgecolor='black'   )
plt.savefig(os.path.join(figure_res,'2event.png'),dpi=300, format="png", bbox_inches='tight')
plt.savefig(os.path.join(figure_res,'2event.pdf'),dpi=300, format="pdf", bbox_inches='tight')

