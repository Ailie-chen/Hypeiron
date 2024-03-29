import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter
import csv
import os
import re
import matplotlib.gridspec as gridspec
directory = "./evaluationmemtense/spec2k17/all_results/1228table_size.csv"
figure_res = 'analysis_py/evaluation2/sensitive_design/'
match_datas=[32,8,96,8,16,8,16,8]
dic_size={
    4:0,
    8:1,
    16:2,
    32:3,
    64:4,
    96:5,
    128:6,
    256:7,
    512:8
}
design_nums = len(match_datas)
markers=['o','s','d','x','o','s','d','x']
markercolors=['lightgray','gray','black','black','lightgray','gray','black','black']
labels=['Size(Page History Table)','Num(PageOffsets)','Size(Page Delta Table)','Num(PageDeltas)',
'Size(PC History Table)','Num(PCAddrs)','Size(PC Delta Table)','Num(PCDeltas)']
data_all={}
for i in np.arange(0, len(match_datas)):
    data_all[i] = []

data = pd.read_csv(directory, header=None)
prefs_name = data.loc[:,data.loc[0, :].str.contains('Prefetcher')]
prefs_name = np.array(prefs_name.iloc[:, 0])
prefs_name = prefs_name[2:len(prefs_name)]

speedup = data.loc[:,data.loc[0, :].str.contains('IPCI')]
speedup = np.array(speedup.iloc[:, 0])
speedup = speedup[2:len(speedup)]
speedup = [float(item) for item in speedup]

# accuracy = data.loc[:,data.loc[0, :].str.contains('L1D Accuracy')]
# accuracy = np.array(accuracy.iloc[:, 0])
# accuracy = accuracy[2:len(accuracy)]
# accuracy = [(float(item)-0.85)*(0.90-0.85)/(1.60-1.55)+1.55 for item in accuracy]

pref_idx = 0
base_pref_speedup = 0
for pref in prefs_name:
    xlabel = []
    matches = re.findall(r'(\d+)',pref)
    if matches:
        for item in matches:
            xlabel.append(int(item))
    k_idx = 0
    for i in np.arange(0,design_nums):
        if match_datas[i] != xlabel[i]:
            k_idx = i+1
            break
    if(k_idx == 0):
        base_pref_speedup = speedup[pref_idx]
    else:
        k_idx = k_idx - 1
        data_all[k_idx].append([xlabel[k_idx],speedup[pref_idx]])
    pref_idx+= 1
print(base_pref_speedup)
fig = plt.figure(figsize=(7, 1.5), dpi=300)
gs = gridspec.GridSpec(1, 6, figure=fig)
ax1 = fig.add_subplot(gs[0, 0:2])
ax2 = fig.add_subplot(gs[0, 3:5],sharey=ax1)
ax3 = fig.add_subplot(gs[0, 2:3],sharey=ax1)
ax4 = fig.add_subplot(gs[0, 5:6],sharey=ax1)
# 可以选择关闭共享y轴图的y轴刻度，以避免重叠
plt.setp(ax3.get_yticklabels(), visible=False)
plt.setp(ax2.get_yticklabels(), visible=False)
plt.setp(ax4.get_yticklabels(), visible=False)

plt.subplots_adjust(left=0, right=1.0, bottom=0, top=1.0, wspace=0.1, hspace=0.85)
left_bar_pos1 = [item+0.5 for item in np.arange(0,9)]
for i in np.arange(0,len(match_datas)):
    
    data_all[i].append([match_datas[i],base_pref_speedup])
    data_all[i] = sorted(data_all[i], key=lambda x: x[0])
    size = []
    speedup = []
    for item in data_all[i]:
        size.append(item[0])
        speedup.append(item[1])
    left_bar_pos= [dic_size[item]+0.5 for item in size]
    if(i == 0):
        ax1.plot(left_bar_pos, speedup, linestyle='-', marker=markers[i],
        label=labels[i],
        markerfacecolor=markercolors[i], linewidth=1,markersize=5,zorder=2,color='gray') 
    elif(i == 2):
        ax1.plot(left_bar_pos, speedup, linestyle='--', marker=markers[i],
        label=labels[i],
        markerfacecolor=markercolors[i], linewidth=1,markersize=5,zorder=2,color='black') 
    elif(i == 4 ):
        ax2.plot(left_bar_pos, speedup, linestyle='-', marker=markers[i],
        label=labels[i],markerfacecolor=markercolors[i], linewidth=1,markersize=5,zorder=2,color='gray') 
    elif(i == 6) :
        ax2.plot(left_bar_pos, speedup, linestyle='--', marker=markers[i],
        label=labels[i],markerfacecolor=markercolors[i], linewidth=1,markersize=5,zorder=2,color='black') 
    elif( i == 1):
        ax3.plot(left_bar_pos, speedup, linestyle='-', marker=markers[i],
        label=labels[i],
        markerfacecolor=markercolors[i], linewidth=1,markersize=5,zorder=2,color='gray') 
    elif( i ==3):
        ax3.plot(left_bar_pos, speedup, linestyle='--', marker=markers[i],
        label=labels[i],
        markerfacecolor=markercolors[i], linewidth=1,markersize=5,zorder=2,color='black') 
    elif( i == 5):
        ax4.plot(left_bar_pos, speedup, linestyle='-', marker=markers[i],
        label=labels[i],markerfacecolor=markercolors[i], linewidth=1,markersize=5,zorder=2,color='gray') 
    elif( i == 7):
        ax4.plot(left_bar_pos, speedup, linestyle='--', marker=markers[i],
        label=labels[i],markerfacecolor=markercolors[i], linewidth=1,markersize=5,zorder=2,color='black') 



ax1.set_xticks(left_bar_pos1)  
ax1.set_yticks(np.arange(150, 161,1)/100)
ax1.set_xticklabels([4,8,16,32,64,96,128,256,512],fontsize=9,ha='center')
ax1.set_title('(a)Size of tables for Page', x=0.5,y=-0.3, fontsize=9) 
ax1.set_yticklabels(['{:.2f}'.format(item) for item in np.arange(150, 161,1)/100],fontsize=9,ha='right')
ax1.set_ylabel('SpeedUp') 

ax2.set_xticks(left_bar_pos1)  
# ax2.set_yticks(np.arange(150, 161,1)/100)
ax2.set_xticklabels([4,8,16,32,64,96,128,256,512],fontsize=9,ha='center')
ax2.set_title('(c)Size of tables for PC', x=0.5,y=-0.3, fontsize=9)
# ax2.set_yticklabels(['{:.2f}'.format(item) for item in np.arange(150, 161,1)/100],fontsize=9,ha='right')
# ax2.set_ylabel('SpeedUp')

ax3.set_xticks(np.arange(0,5)+0.5)  
# ax3.set_yticks(np.arange(150, 161,1)/100)
ax3.set_xticklabels([4,8,16,32,64],fontsize=9,ha='center')
ax3.set_title('(b)entry size for Page', y=-0.3, fontsize=9) 
# ax3.set_yticklabels(['{:.2f}'.format(item) for item in np.arange(150, 161,1)/100],fontsize=9,ha='right')
# ax3.set_ylabel('SpeedUp') 

ax4.set_xticks(np.arange(0,5)+0.5)  
# ax2.set_yticks(np.arange(150, 161,1)/100)
ax4.set_xticklabels([4,8,16,32,64],fontsize=9,ha='center')
ax4.set_title('(d)entry size for PC', y=-0.3, fontsize=9)
# ax2.set_yticklabels(['{:.2f}'.format(item) for item in np.arange(150, 161,1)/100],fontsize=9,ha='right')
# ax2.set_ylabel('SpeedUp')

ax1.set_ylim(1.53, 1.60) 
ax2.set_ylim(1.53, 1.60) 
# ax3.set_ylim(1.53, 1.58) 
# ax4.set_ylim(1.53, 1.58) 

ax_idx = 0
for item in np.arange(1500, 1601,5)/1000:
    if(ax_idx % 2 == 0):
        ax1.axhline(float(item), color='lightgray', linestyle='-', linewidth=1,zorder=1)
        ax2.axhline(float(item), color='lightgray', linestyle='-', linewidth=1,zorder=1)
        ax3.axhline(float(item), color='lightgray', linestyle='-', linewidth=1,zorder=1)
        ax4.axhline(float(item), color='lightgray', linestyle='-', linewidth=1,zorder=1)
    else:
        ax1.axhline(float(item), color='lightgray', linestyle='--', linewidth=1,zorder=1)
        ax2.axhline(float(item), color='lightgray', linestyle='--', linewidth=1,zorder=1)
        ax3.axhline(float(item), color='lightgray', linestyle='--', linewidth=1,zorder=1)
        ax4.axhline(float(item), color='lightgray', linestyle='--', linewidth=1,zorder=1)
    ax_idx += 1
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.35), ncol=1, fontsize=9,
             # y 参数控制标题的位置
        handlelength=1.2,     # 控制图例句柄的长度
        handletextpad=0.2,  # 控制图例句柄和文本之间的间距
        columnspacing=0.5,
        edgecolor='black'   )
ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.35), ncol=1, fontsize=9,
             # y 参数控制标题的位置
        handlelength=1.2,     # 控制图例句柄的长度
        handletextpad=0.2,  # 控制图例句柄和文本之间的间距
        columnspacing=0.5,
        edgecolor='black'   )
ax3.legend(loc='upper center', bbox_to_anchor=(0.5, 1.35), ncol=1, fontsize=9,
             # y 参数控制标题的位置
        handlelength=1.2,     # 控制图例句柄的长度
        handletextpad=0.2,  # 控制图例句柄和文本之间的间距
        columnspacing=0.5,
        edgecolor='black'   )
ax4.legend(loc='upper center', bbox_to_anchor=(0.4, 1.35), ncol=1, fontsize=9,
             # y 参数控制标题的位置
        handlelength=1.2,     # 控制图例句柄的长度
        handletextpad=0.2,  # 控制图例句柄和文本之间的间距
        columnspacing=0.5,
        edgecolor='black'   )

plt.savefig(os.path.join(figure_res,'table_size.png'),dpi=300, format="png", bbox_inches='tight')
plt.savefig(os.path.join(figure_res,'table_size.pdf'),dpi=300, format="pdf", bbox_inches='tight')

