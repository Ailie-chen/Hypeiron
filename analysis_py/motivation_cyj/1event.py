import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter
import csv
import os
figure_res = 'analysis_py/motivation_cyj/'


Bdata = [0.59,0.5,0.46,0.37]
Cdata = [0.84,0.67,0.70,0.85]
Xlabel = ['PC(Berti)', 'Offset','Global','Page']
fig, ax = plt.subplots(figsize=(3.23, 1.3),dpi=300)
bar_width = 1.0 / (2 + 1.5)
left_bar_pos1 = np.arange(len(Xlabel))
left_bar_pos2 = np.arange(4,7,1)
print(left_bar_pos2)
ax.bar(left_bar_pos1 + bar_width * 1.0, [0.55,0.26,0.45,0.42], edgecolor ="#4472C4",width= bar_width, label = 'Coverage',hatch="",facecolor="#4472C4",zorder=2)
ax.bar(left_bar_pos1 + bar_width * 2.0, [0.84,0.65,0.71,0.84], edgecolor ="#ED7D31",width= bar_width, label = 'Accuracy',hatch="",facecolor="#ED7D31",zorder=2)
plt.xticks(left_bar_pos1 + bar_width * 1.5, ['PC(Berti)', 'Offset','Global','Page'], fontsize=9,ha='center')#rotation=45,


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
# ax.set_xlabel('Events',fontsize=9,ha='right')
# ax.grid(which='major',axis='y')
ax.legend(loc='upper center', bbox_to_anchor=(0.51, 1.30), ncol=2,fontsize=8,
       handlelength=1.2,     # 控制图例句柄的长度
        handletextpad=0.2,  # 控制图例句柄和文本之间的间距
        columnspacing=0.5,
        edgecolor='black'   )
plt.savefig(os.path.join(figure_res,'1event.png'),dpi=300, format="png", bbox_inches='tight')
plt.savefig(os.path.join(figure_res,'1event.pdf'),dpi=300, format="pdf", bbox_inches='tight')

