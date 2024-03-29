import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter
import csv
import os
figure_res = 'analysis_py/motivation_cyj/'
# <IP*1> long: 0.43 conf:0.33
# <IP*1,Page*1> long:0.5 conf:0.43
# <IP*2> long 0.46 conf:0.35
# <IP*2, Page*2> long 0.58 conf:0.49
# <IP*4> long 0.49 conf 0.37
# <Ip*4, Page*4> long 0.63 conf 0.53
# <IP*8> long 0.51 conf 0.37
# <IP*8, Page*8> long 0.67 conf 0.55
# <IP*16> long 0.53 conf 0.38
0.88,0.86,0.89,0.85,0.83


A1data = [0.27,0.28,0.29,0.29,0.29]
B1data = [0.26,0.32,0.34,0.36,0.39]
A2data = [0.55,0.57,0.59,0.59,0.59]
B2data = [0.47,0.59,0.6,0.62,0.62]
A3data = [0.86,0.88,0.87,0.86,0.84]
B3data = [0.88,0.86,0.89,0.85,0.83]

Xlabel = ['16', '32','64','128','256']
fig, (ax2,ax3) = plt.subplots(1,2, figsize=(3.23, 1.3))
plt.subplots_adjust(left=0, right=1.0, bottom=0, top=1.0, wspace=0.3, hspace=0.37)

left_bar_pos = np.arange(len(Xlabel))
left_bar_pos1 = np.arange(1,len(Xlabel),1)
ax2.plot(left_bar_pos, [item*100 for item in A2data], linestyle='-', marker='o', markerfacecolor="#4472C4",color="#4472C4", label='PC',linewidth=1.0,markersize=2.5,zorder=2) 
ax2.plot(left_bar_pos, [item*100 for item in B2data], linestyle='-', marker='s', markerfacecolor="#ED7D31",color="#ED7D31", label='PC+Page',linewidth=1.0,markersize=2.5,zorder=2)
ax3.plot(left_bar_pos, [item*100 for item in A3data], linestyle='-', marker='o', markerfacecolor="#4472C4",color="#4472C4", label='PC',linewidth=1.0,markersize=2.5,zorder=2) 
ax3.plot(left_bar_pos, [item*100 for item in B3data], linestyle='-', marker='s', markerfacecolor="#ED7D31",color="#ED7D31", label='PC+Page',linewidth=1.0,markersize=2.5,zorder=2)

ax2_yticks1=np.arange(40,71,6)
ax2_yticks=np.arange(40,71,3)

ax3_yticks1=np.arange(50,101,10)
ax3_yticks=np.arange(50,101,5)

ax2.set_xticks(left_bar_pos)  
ax2.set_yticks(ax2_yticks1)
ax2.set_xticklabels(Xlabel,fontsize=9,ha='center')
ax2.set_yticklabels(ax2_yticks1,fontsize=9,ha='right')
ax3.set_xticks(left_bar_pos)  
ax3.set_yticks(ax3_yticks1)
ax3.set_xticklabels(Xlabel,fontsize=9,ha='center')
ax3.set_yticklabels(ax3_yticks1,fontsize=9,ha='right')

# plt.xticks(left_bar_pos, Xlabel,  fontsize=9,ha='center')#rotation=45,
# plt.yticks([0,0.25,0.5,0.75,1.00], ['0%','25%','50%','75%','100%'], fontsize=9,ha='right')
# for label in ax.get_yticklabels():
#     label.set_fontsize(16)
ax2.set_title('Coverage',fontsize=9,ha='center')
ax3.set_title('Accuracy',fontsize=9,ha='center')
ax2.set_xlabel('Entries',fontsize=9,ha='center')
ax3.set_xlabel('Entries',fontsize=9,ha='center')

ax2.set_ylim(40,70)
ax3.set_ylim(50,100)
ax2.legend(loc='upper center', bbox_to_anchor=(0.51, 0.4), ncol=1,fontsize=8,
       handlelength=1.2,     # 控制图例句柄的长度
        handletextpad=0.2,  # 控制图例句柄和文本之间的间距
        columnspacing=0.5,
        edgecolor='black'   )
ax3.legend(loc='upper center', bbox_to_anchor=(0.51, 0.4), ncol=1,fontsize=8,
       handlelength=1.2,     # 控制图例句柄的长度
        handletextpad=0.2,  # 控制图例句柄和文本之间的间距
        columnspacing=0.5,
        edgecolor='black'   )
ax2_idx = 0
for item in ax2_yticks1:
    if(ax2_idx % 2 == 0):
        ax2.axhline(float(item), color='lightgray', linestyle='-', linewidth=1.0,zorder=1)
    else:
        ax2.axhline(float(item), color='lightgray', linestyle='--', linewidth=1.0,zorder=1)
    ax2_idx += 1
ax3_idx = 0
for item in ax3_yticks1:
    if(ax3_idx % 2 == 0):
        ax3.axhline(float(item), color='lightgray', linestyle='-', linewidth=1.0,zorder=1)
    else:
        ax3.axhline(float(item), color='lightgray', linestyle='--', linewidth=1.0,zorder=1)
    ax3_idx += 1
plt.savefig(os.path.join(figure_res,'AC.png'),dpi=300, format="png", bbox_inches='tight')
plt.savefig(os.path.join(figure_res,'AC.pdf'),dpi=300, format="pdf", bbox_inches='tight')

