import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter
import csv
import os
import re
from matplotlib.lines import Line2D
import math

directory = "./evaluationmemtense/spec/all_results/0335.csv"
figure_res = 'analysis_py/evaluation3/table_size/'

data = pd.read_csv(directory, header=None)
prefs_name = data.loc[:,data.loc[0, :].str.contains('Prefetcher')]
prefs_name = np.array(prefs_name.iloc[:, 0])
prefs_name = prefs_name[1:len(prefs_name)]

speedup = data.loc[:,data.loc[0, :].str.contains('IPCI')]
speedup = np.array(speedup.iloc[:, 0])
speedup = speedup[1:len(speedup)]
speedup = [float(item) for item in speedup]


xlabel = ['4','8','16','32','64','128']
dics = []
for i in range(0, 4):
    dics.append([0] * 5)  # 对于前4个元素，每个子列表包含5个0
for i in range(4, 8):
    dics.append([0] * 6)  # 对于接下来的4个元素，每个子列表包含6个0
for i in range(8, 12):
    dics.append([0] * 5) 
#字典有1维，第一维表示线条
#1-4：表示pc为page的1/2
#5-8: 表示pc和page一样多
#9-12：表示pc是page的两倍
#第二维，1：表示delta page的个数和page一样，pc是pc的一样
#第二维：2：表示delta page的个数是page两倍，pc是pc的一样
#第三维：3：表示delta page的个数和page一样，pc是pc的两倍
#第二维：4：表示delta page和pc的个数都是两倍
idx = 0
for pref in prefs_name:
    matches = re.match(r'hyperion_hpc_size_(\d+)_(\d+)_(\d+)_(\d+)',pref)
    if matches:
        pc_his= int(matches.group(1))
        page_his = int(matches.group(3))
        pc_delta = int(matches.group(2))
        page_delta = int(matches.group(4))
        idx2 = int(math.log2(page_his)-2)
        if pc_his == page_his / 2:
            idx2 = idx2-1
            if(pc_delta == 1 and page_delta == 1):
                dics[0][idx2]=speedup[idx]
            elif(page_delta == 2 and pc_delta == 1):
                dics[1][idx2]=speedup[idx]
            elif(page_delta == 1 and pc_delta == 2):
                dics[2][idx2]=speedup[idx]
            elif(page_delta == 2 and pc_delta == 2):
                dics[3][idx2]=speedup[idx]
        elif pc_his == page_his:
            if(pc_delta == 1 and page_delta == 1):
                print(pc_his,page_his,pc_delta,page_delta,idx2)
                dics[4][idx2]=speedup[idx]
            elif(page_delta == 2 and pc_delta == 1):
                dics[5][idx2]=speedup[idx]
            elif(page_delta == 1 and pc_delta == 2):
                dics[6][idx2]=speedup[idx]
            elif(page_delta == 2 and pc_delta == 2):
                dics[7][idx2]=speedup[idx]
        elif pc_his == page_his*2 :
            if(pc_delta == 1 and page_delta == 1):
                dics[8][idx2]=speedup[idx]
            elif(page_delta == 2 and pc_delta == 1):
                dics[9][idx2]=speedup[idx]
            elif(page_delta == 1 and pc_delta == 2):
                dics[10][idx2]=speedup[idx]
            elif(page_delta == 2 and pc_delta == 2):
                dics[11][idx2]=speedup[idx]
    idx += 1
print(dics[3])
print(dics[4])
fig, ax = plt.subplots(figsize=(3.5, 1.3),dpi=300)
left_bar_pos1 = [item for item in np.arange(1,len(xlabel),1)]
left_bar_pos = [item for item in np.arange(0,len(xlabel),1)]
left_bar_pos2 = [item for item in np.arange(0,len(xlabel)-1,1)]
#粉色：#E57B7F
#深蓝：#033250
#浅蓝：#4BACC6
#深蓝："#0E5378"
blue1 = '#4BACC6'
red = '#bf1e2e'
blue2 = '#4A60F7'
colors = [blue1,blue1,blue1,blue1,
        red,red,red,red,
        blue2,blue2,blue2,blue2]
labels = ['pc/2,dpc*1,dpage*1','pc/2,dpc*1,dpage*2','pc/2,dpc*2,dpage*1','pc/2,dpc*2,dpage*2',
        'pc,dpc*1,dpage*1','pc,dpc*1,dpage*2','pc,dpc*2,dpage*1','pc,dpc*2,dpage*2',
        'pc*2,dpc*1,dpage*1','pc*2,dpc*1,dpage*2','pc*2,dpc*2,dpage*1','pc*2,dpc*2,dpage*2']
markers=['^','o','d','s',
        '^','o','d','s',
        '^','o','d','s',
        '^','o','d','s']
for i in range(0, 4):
    ax.plot(left_bar_pos1, dics[i], linestyle='-', marker=markers[i], markerfacecolor='none',color=colors[i], label=labels[i],linewidth=0.8,markersize=1.5,zorder=4)
for i in range(4, 8):
    ax.plot(left_bar_pos, dics[i], linestyle='-', marker=markers[i], markerfacecolor='none',color=colors[i], label=labels[i],linewidth=0.8,markersize=1.5,zorder=3)  
for i in range(8, 12):
    ax.plot(left_bar_pos2, dics[i], linestyle='-', marker=markers[i], markerfacecolor='none',color=colors[i], label=labels[i],linewidth=0.8,markersize=1.5,zorder=2)  

# ax2 = ax.twinx()
# ax2.plot(left_bar_pos, accuracy, linestyle='-', marker='s', markerfacecolor='grey',color='grey', linewidth=1,markersize=2.5,zorder=2) 

legend_patch = []
legend_patch2 = []
# legend_patch.append(Line2D([0], [0], linestyle='-', marker='o', markerfacecolor='none', color='black', lw=1, markersize=2.5, label='Speedup'))
# legend_patch.append(Line2D([0], [0], linestyle='-', marker='s', markerfacecolor='grey', color='grey', lw=1, markersize=2.5, label='Accuracy'))
legend_patch.append(Line2D([0], [0], linestyle='-', color=blue1, lw=1,  label=r'$HT_{PC}=\frac{HT_{page}}{2}$'))
legend_patch.append(Line2D([0], [0], linestyle='-', color=red, lw=1,  label=r'$HT_{PC}=HT_{page}$'))
legend_patch.append(Line2D([0], [0], linestyle='-', color=blue2, lw=1,  label=r'$HT_{PC}=HT_{page}\times2$'))
legend_patch2.append(Line2D([0], [0], linestyle='-', marker='^', markerfacecolor='gray', color='grey', lw=1, markersize=2.5, label=r'$DT_{PC}=HT_{PC},DT_{page}=HT_{page}$'))
legend_patch2.append(Line2D([0], [0], linestyle='-', marker='o', markerfacecolor='gray', color='grey', lw=1, markersize=2.5, label=r'$DT_{PC}=HT_{PC},DT_{page}=HT_{page}\times2$'))
legend_patch2.append(Line2D([0], [0], linestyle='-', marker='d', markerfacecolor='gray', color='grey', lw=1, markersize=2.5, label=r'$DT_{PC}=HT_{PC}\times2,DT_{page}=HT_{page}$'))
legend_patch2.append(Line2D([0], [0], linestyle='-', marker='s', markerfacecolor='gray', color='grey', lw=1, markersize=2.5, label=r'$DT_{PC}=HT_{PC}\times2,DT_{page}=HT_{page}\times2$'))



ax.set_xticks(left_bar_pos)  
ax.set_yticks(np.arange(130, 161,10)/100)
ax.set_xticklabels(xlabel,fontsize=7,ha='center')
ax.set_xlabel(r'$HT_{page}$(Entries of different pages in GHB)',fontsize=7)
ax.set_yticklabels(['{:.1f}'.format(item) for item in np.arange(130, 161,10)/100],fontsize=7,ha='right')
ax.set_ylabel('SpeedUp',fontsize=7) 
# ax2.set_yticks(np.arange(155, 161,1)/100)
# ax2.set_yticklabels(['{:.2f}'.format(item) for item in np.arange(85, 91,1)/100],fontsize=9,ha='left')
# ax2.set_ylabel('L1D Accuracy') 

ax.set_ylim(1.30, 1.61) 

first_legend = ax.legend(handles=legend_patch,loc='upper center', bbox_to_anchor=(0.60, 0.90), ncol=1, fontsize=6,
             # y 参数控制标题的位置
        handlelength=1.2,     # 控制图例句柄的长度
        handleheight=0.1,
        labelspacing=0.00,  # 控制图例句柄和文本之间的间距
        columnspacing=0.7,
        edgecolor='none'   )
ax.add_artist(first_legend)
ax.legend(handles=legend_patch2,loc='upper center', bbox_to_anchor=(0.68, 0.53), ncol=1, fontsize=6,
             # y 参数控制标题的位置
        handlelength=1.2,     # 控制图例句柄的长度
        handleheight=0.1,
        labelspacing=0.0,  # 控制图例句柄和文本之间的间距
        columnspacing=0.5,
        edgecolor='none'   )
# ax.legend(handles=legend_patch,loc='upper center', bbox_to_anchor=(1.6, 1.1),fontsize=7)
ax_idx = 0
for item in np.arange(1300, 1610,500)/1000:
    if(ax_idx % 2 == 0):
        ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=1,zorder=1)
    else:
        ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=1,zorder=1)
    ax_idx += 1

plt.savefig(os.path.join(figure_res,'page_size.png'),dpi=300, format="png", bbox_inches='tight')
plt.savefig(os.path.join(figure_res,'page_size.pdf'),dpi=300, format="pdf", bbox_inches='tight')

