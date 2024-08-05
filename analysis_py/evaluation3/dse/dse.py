import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
import math
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Patch
import matplotlib.patches as patches
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
import re
# 3.23 1.3
traces=["4suites"]
dic_suite={
    'spec2k06':'SPEC06',
    'spec2k17':'SPEC17',
    'gap':"GAP",
    'parsec':'PARSEC',
    '4suites':"Geomean"
}
axi_line_width = 0.3
fig_line_with = 0.75
# colors = ['#FEB3AE','#73bad6','#CD5C5C','#0E5378',"#0E5378",'#ef4143','#bd3752','#c4323f']
colors = ['#e6194B','#4363d8','#3cb44b','#0E5378',"#0E5378",'#ef4143','#bd3752','#c4323f']

fontsizes=6.5
metrics=['IPCI','L1D Accuracy','L1D Coverage']
legends={"ipcp_isca2020":"IPCP",
         "mlop_dpc3":"MLOP",
         "vberti":"Berti",
         "hyperion_hpc_aDiGHB_UTBh1_buffer8_8":"Hyperion",
         "bingo_dpc3":"Bingo",
         "ppf":'SPP-PPF'}
hatches = ['\\\\\\\\\\',   '', '', '', ''] #'xxxxx',
# colors = [ 'white','white','grey','black']


def get_col_data(data,metric):
    num_prefs = data.shape[0]-1
    prefs_name = data.iloc[1:,1].tolist()
    metric_data = data.loc[:,data.loc[0, :].str.contains(metric)]
    first_column_array = np.array(metric_data.iloc[:, 0])
    metric_data = metric_data.iloc[np.arange(1,num_prefs+1), :]
    # first_row_array = np.array(metric_data.iloc[0, :])
    first_column_array = np.array(metric_data.iloc[:, 0])
    first_column_array = np.where(first_column_array == '-', '0', first_column_array)
    # Convert the array back to its original numeric type if necessary  
    return first_column_array

def plot_hisnum(ax):
    prefs=[]
    date = '0331'
    data_file_path = 'evaluationmemtense/'+ traces[0] + '/'+'all_results/'
    data_pref = pd.read_csv(data_file_path + date + '.csv', header=None)
    prefs = get_col_data(data_pref,'Prefetcher')
    num_prefs = len(prefs)
    data_all = np.zeros((num_prefs, len(traces)))
    trace_idx = 0
    for trace in traces:
        data_file_path='evaluationmemtense/'+ trace + '/'+'all_results/'
        data = pd.read_csv(data_file_path + date + '.csv', header=None)
        data_IPCI = np.zeros((num_prefs, 1))     
        data_IPCI[0:num_prefs,0] = get_col_data(data,metrics[0])
        data_all[0:num_prefs,trace_idx] = data_IPCI[0:num_prefs,0]
        trace_idx = trace_idx + 1
    matplotlib.rcParams['hatch.linewidth'] = axi_line_width # 设置您想要的线宽

    #设置子图间隔
    # 设定条形图的宽度
    left_bar_pos = np.arange(len(prefs))
    print(left_bar_pos)
    legend_patch = []
    ax.plot(data_all[0:len(prefs),0],color=colors[1],marker='o', markerfacecolor='none', label='PC',linewidth=fig_line_with,markersize=2.5,zorder=2)   


    # 添加矩形到轴上
    ax.add_patch(patches.Rectangle((0.90, 1.40), 0.2, 0.18, linewidth=fig_line_with+0.2, edgecolor='darkgray', facecolor='none',alpha = 1.0,zorder=2))

    # 计算x轴刻度的位置
    x_ticks = left_bar_pos
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([4,8,16,32,64], fontsize=fontsizes)
    # axes[ay].set_xlabel('Benchmarks', fontsize=9)
    
    y_ticks=np.around(np.arange(1.0, 1.601, 0.06), decimals=2)
    y_ticks1=np.around(np.arange(1.0, 1.601, 0.12), decimals=2)

    ax.set_ylim(1.0, 1.60)
    ax_idx = 0
    for item in y_ticks:
        if(ax_idx % 2 == 0):
            ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=0.5,zorder=1)
        else:
            ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=0.5,zorder=1)
        ax_idx += 1   
    ax.set_yticks(y_ticks1)
    ax.set_yticklabels([format(item,'.2f') for item in y_ticks1], fontsize=fontsizes)

    # ax.set_ylabel("Geomean SpeedUp over no prefetching", fontsize=fontsizes)
    ax.text(-1.20,1.5,"SpeedUp",fontsize=fontsizes,ha='center',va='top',rotation = 90)
    # ax.text(-0.1,1.7,"over no prefetching",fontsize=fontsizes-1,ha='center',va='top',rotation = 90)


    # ax.set_title(dic_suite[trace], y=-0.28, fontsize=9) 

    ax.text(-0.6,0.77,r'(a) Number of histories for entries in HT',fontsize=fontsizes)

def plot_table_size(ax):
    date = '0338'
    directory = f"./evaluationmemtense/4suites/all_results/{date}.csv"

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
        matches = re.match(r'hyperion_2table_size_(\d+)_(\d+)_(\d+)_(\d+)',pref)
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
    left_bar_pos1 = [item for item in np.arange(1,len(xlabel),1)]
    left_bar_pos = [item for item in np.arange(0,len(xlabel),1)]
    left_bar_pos2 = [item for item in np.arange(0,len(xlabel)-1,1)]
    #粉色：#E57B7F
    #深蓝：#033250
    #浅蓝：#4BACC6
    #深蓝："#0E5378"

    # blue1 = '#4BACC6'
    # red = '#bf1e2e'
    # blue2 = '#4A60F7'
    blue1 = colors[0]
    red = colors[1]
    blue2 = colors[2]
    colors1 = [blue1,blue1,blue1,blue1,
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
        ax.plot(left_bar_pos1, dics[i], linestyle='-', marker=markers[i], markerfacecolor='none',color=colors1[i], label=labels[i],linewidth=0.8,markersize=1.5,zorder=4)
    for i in range(4, 8):
        ax.plot(left_bar_pos, dics[i], linestyle='-', marker=markers[i], markerfacecolor='none',color=colors1[i], label=labels[i],linewidth=0.8,markersize=1.5,zorder=3)  
    for i in range(8, 12):
        ax.plot(left_bar_pos2, dics[i], linestyle='-', marker=markers[i], markerfacecolor='none',color=colors1[i], label=labels[i],linewidth=0.8,markersize=1.5,zorder=2)  


    ax.add_patch(patches.Rectangle((2.95, 1.40), 0.12, 0.18, linewidth=fig_line_with+0.2, edgecolor='darkgray', facecolor='none',alpha = 1.0,zorder=5))
    # ax.plot(2.0,1.45,linestyle='-', marker=markers[1], markerfacecolor='none',color=colors[3], linewidth=fig_line_with,markersize=1.5,zorder=4)
    # ax.plot(2.0,1.55,linestyle='-', marker=markers[1], markerfacecolor='none',color=colors[3], linewidth=fig_line_with,markersize=1.5,zorder=4)

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
    ax.set_xticklabels(xlabel,fontsize=fontsizes,ha='center')
    # ax.set_xlabel(r'(b) Entries in $HT_{page}$',fontsize=fontsizes)


    y_ticks=np.around(np.arange(1.0, 1.601, 0.06), decimals=2)
    y_ticks1=np.around(np.arange(1.0, 1.601, 0.12), decimals=2)

    ax.set_ylim(1.0, 1.600)
    ax_idx = 0
    for item in y_ticks:
        if(ax_idx % 2 == 0):
            ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=0.5,zorder=1)
        else:
            ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=0.5,zorder=1)
        ax_idx += 1   
    ax.set_yticks(y_ticks1)
    ax.set_yticklabels([format(item,'.2f') for item in y_ticks1], fontsize=fontsizes)

    first_legend = ax.legend(handles=legend_patch,loc='upper center', bbox_to_anchor=(0.3, 0.60), ncol=1, fontsize=fontsizes-1,
                # y 参数控制标题的位置
            handlelength=1.2,     # 控制图例句柄的长度
            handleheight=0.1,
            labelspacing=0.00,  # 控制图例句柄和文本之间的间距
            columnspacing=0.7,
            # frameon=False,
            edgecolor='none'   )
    ax.add_artist(first_legend)
    ax.legend(handles=legend_patch2,loc='upper center', bbox_to_anchor=(0.70, 0.65), ncol=1, fontsize=fontsizes-1,
                # y 参数控制标题的位置
            handlelength=1.2,     # 控制图例句柄的长度
            handleheight=0.1,
            labelspacing=0.0,  # 控制图例句柄和文本之间的间距
            columnspacing=0.5,
            frameon=False,
            edgecolor='none'   )
    ax.text(-0.705,1.42,"SpeedUp",fontsize=fontsizes,ha='center',va='top',rotation = 90)
    ax.text(2.8,0.77 ,r'(b) Entries in $HT_{page}$',fontsize=fontsizes,ha='center')

def plot_thresh_L1D(ax):
    prefs=[]
    date = '0337'
    data_file_path = 'evaluationmemtense/'+ traces[0] + '/'+'all_results/'
    data_pref = pd.read_csv(data_file_path + date + '.csv', header=None)
    prefs = get_col_data(data_pref,'Prefetcher')
    num_prefs = len(prefs)
    print(num_prefs)
    data_all = np.zeros((num_prefs, len(metrics)))
    
    metric_idx = 0
    for metric in metrics:
        data_file_path='evaluationmemtense/'+ '4suites' + '/'+'all_results/'
        data = pd.read_csv(data_file_path + date + '.csv', header=None)
        data_IPCI = np.zeros((num_prefs, 1))     
        data_IPCI[0:num_prefs,0] = get_col_data(data,metric)
        data_all[0:num_prefs,metric_idx] = data_IPCI[0:num_prefs,0]
        metric_idx = metric_idx + 1

    matplotlib.rcParams['hatch.linewidth'] = axi_line_width # 设置您想要的线宽
    ax2 = ax.twinx()
    #设置子图间隔
    # 设定条形图的宽度
    left_bar_pos = np.arange(len(prefs))
    print(left_bar_pos)
    ## 设置图像保存的路径
    figure_res='analysis_py/evaluation3/thresh_L1D/'
    if not os.path.exists(figure_res):
            os.makedirs(figure_res) 
    legend_patch = []
    ax.plot(data_all[0:len(prefs),0],color=colors[1],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='Speedup')   
    ax2.plot([(data-0.45)/0.5*(0.4)+1.4 for data in data_all[0:len(prefs),1]],color=colors[2],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2)   
    ax2.plot([(data-0.45)/0.5*(0.4)+1.4 for data in data_all[0:len(prefs),2]],color=colors[0],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2)   
    print(data_all[0:len(prefs),1])
    legend_patch = []
    legend_patch.append(Line2D([0], [0], color=colors[1],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='Speedup'))
    legend_patch.append(Line2D([0], [0], color=colors[2],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='L1D Accuracy'))
    legend_patch.append(Line2D([0], [0], color=colors[0],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='L1D coverage'))


    # 添加矩形到轴上
    ax.add_patch(patches.Rectangle((2.9, 1.43), 0.2, 0.36, linewidth=fig_line_with+0.2, edgecolor='darkgray', facecolor='none',alpha = 1.0,zorder=2))

    # 计算x轴刻度的位置
    x_ticks = left_bar_pos
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([0.5,0.6,0.7,0.8,0.9], fontsize=fontsizes)
    # axes[ay].set_xlabel('Benchmarks', fontsize=9)
    
    y_ticks=np.around(np.arange(1.4, 1.801, 0.04), decimals=2)
    y_ticks1=np.around(np.arange(1.4, 1.801, 0.08), decimals=2)

    ax.set_ylim(1.4, 1.80)
    ax_idx = 0
    for item in y_ticks:
        if(ax_idx % 2 == 0):
            ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=0.5,zorder=1)
        else:
            ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=0.5,zorder=1)
        ax_idx += 1   
    ax.set_yticks(y_ticks1)
    ax2.set_yticks(y_ticks1)

    print(y_ticks1)
    ax.set_yticklabels([format(item,'.2f') for item in y_ticks1], fontsize=fontsizes)
    y_ticks2 = np.around(np.arange(0.45, 0.96, 0.10), decimals=2)
    print(y_ticks1)
    # ax2.set_yticks(y_ticks1)
    ax2.set_yticklabels([format(item,'.2f') for item in y_ticks2], fontsize=fontsizes)
    # ax2.set_yticklabels([' ' for item in y_ticks1], fontsize=fontsizes)


    ax.legend(handles=legend_patch,loc='upper center', bbox_to_anchor=(0.30, 0.84), ncol=1, fontsize=fontsizes,
            # y 参数控制标题的位置
    handlelength=1.2,     # 控制图例句柄的长度
    handleheight=0.1,
    labelspacing=0.00,  # 控制图例句柄和文本之间的间距
    columnspacing=0.7,
    # frameon=False,
    edgecolor='none'   )

    # ax.set_ylabel("Geomean SpeedUp over no prefetching", fontsize=fontsizes)
    ax.text(-1.2,1.68,"SpeedUp",fontsize=fontsizes,ha='center',va='top',rotation = 90)
    # ax.text(-0.1,1.7,"over no prefetching",fontsize=fontsizes-1,ha='center',va='top',rotation = 90)
    ax.text(5.20,1.86,"Accuracy and Coverage",fontsize=fontsizes,ha='center',va='top',rotation = 90)
    # ax.text(5.4,1.79,"L1D Coverage",fontsize=fontsizes,ha='center',va='top',rotation = 90)
    
    ax.text(2.0,1.25,"(c) CONF_THRESHOLD_L1D",fontsize=fontsizes,ha='center')

def plot_thresh_L2C(ax):
    date = '0339'
    prefs=[]
    metrics=['IPCI','L2C Accuracy','L2C Coverage']
    data_file_path = 'evaluationmemtense/'+ traces[0] + '/'+'all_results/'
    data_pref = pd.read_csv(data_file_path + date + '.csv', header=None)
    prefs = get_col_data(data_pref,'Prefetcher')
    num_prefs = len(prefs)
    print(num_prefs)
    data_all = np.zeros((num_prefs, len(metrics)))
    
    metric_idx = 0
    
    for metric in metrics:
        data_file_path='evaluationmemtense/'+ '4suites' + '/'+'all_results/'
        data = pd.read_csv(data_file_path + date + '.csv', header=None)
        data_IPCI = np.zeros((num_prefs, 1))     
        data_IPCI[0:num_prefs,0] = get_col_data(data,metric)
        data_all[0:num_prefs,metric_idx] = data_IPCI[0:num_prefs,0]
        metric_idx = metric_idx + 1

    matplotlib.rcParams['hatch.linewidth'] = axi_line_width # 设置您想要的线宽
    ax2 = ax.twinx()
    #设置子图间隔
    # 设定条形图的宽度
    left_bar_pos = np.arange(len(prefs))
    print(left_bar_pos)
    ## 设置图像保存的路径
    legend_patch = []
    ax.plot(data_all[0:len(prefs),0],color=colors[1],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='Speedup')   
    ax2.plot([(data-0.0)/0.75*(0.4)+1.4 for data in data_all[0:len(prefs),1]],color=colors[2],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2)   
    ax2.plot([(data-0.0)/0.75*(0.4)+1.4 for data in data_all[0:len(prefs),2]],color=colors[0],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2)   
    print(data_all[0:len(prefs),1])
    legend_patch = []
    legend_patch.append(Line2D([0], [0], color=colors[1],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='Speedup'))
    legend_patch.append(Line2D([0], [0], color=colors[2],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='L2C Accuracy'))
    legend_patch.append(Line2D([0], [0], color=colors[0],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='L2C coverage'))


    # 添加矩形到轴上
    ax.add_patch(patches.Rectangle((0.9, 1.42), 0.2, 0.34, linewidth=fig_line_with+0.2, edgecolor='darkgray', facecolor='none',alpha = 1.0,zorder=2))

    # 计算x轴刻度的位置
    x_ticks = left_bar_pos
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([0.1,0.2,0.3,0.4,0.5], fontsize=fontsizes)
    # axes[ay].set_xlabel('Benchmarks', fontsize=9)
    
    y_ticks=np.around(np.arange(1.4, 1.801, 0.04), decimals=2)
    y_ticks1=np.around(np.arange(1.4, 1.801, 0.08), decimals=2)

    ax.set_ylim(1.4, 1.60)
    ax_idx = 0
    for item in y_ticks:
        if(ax_idx % 2 == 0):
            ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=0.5,zorder=1)
        else:
            ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=0.5,zorder=1)
        ax_idx += 1   
    ax.set_yticks(y_ticks1)
    ax2.set_yticks(y_ticks1)
    print(y_ticks1)
    ax.set_yticklabels([format(item,'.2f') for item in y_ticks1], fontsize=fontsizes)
    y_ticks2 = np.around(np.arange(0.0, 0.76, 0.15), decimals=2)
    ax2.set_yticks(y_ticks1)
    ax2.set_yticklabels([format(item,'.2f') for item in y_ticks2], fontsize=fontsizes)

    ax.legend(handles=legend_patch,loc='upper center', bbox_to_anchor=(0.7, 0.82), ncol=1, fontsize=fontsizes,
            # y 参数控制标题的位置
    handlelength=1.2,     # 控制图例句柄的长度
    handleheight=0.1,
    labelspacing=0.00,  # 控制图例句柄和文本之间的间距
    columnspacing=0.7,
    # frameon=False,
    edgecolor='none'   )

    # ax.set_ylabel("Geomean SpeedUp over no prefetching", fontsize=fontsizes)
    ax.text(-1.25,1.68,"SpeedUp",fontsize=fontsizes,ha='center',va='top',rotation = 90)
    # ax.text(-0.1,1.7,"over no prefetching",fontsize=fontsizes-1,ha='center',va='top',rotation = 90)


    ax.text(0.4,1.25,"(d) CONF_THRESHOLD_L2C",  fontsize=fontsizes) 
    ax.text(5.2,1.86,"Accuracy and Coverage",fontsize=fontsizes,ha='center',va='top',rotation = 90)
    # ax.text(5.4,1.71,"L2C Coverage",fontsize=fontsizes,ha='center',va='top',rotation = 90)


def plot_L1D_off(ax):
    prefs=[]
    date = '0340'
    metrics=['IPCI','L1D Accuracy','L1D Coverage']
    data_file_path = 'evaluationmemtense/'+ traces[0] + '/'+'all_results/'
    data_pref = pd.read_csv(data_file_path + date + '.csv', header=None)
    prefs = get_col_data(data_pref,'Prefetcher')
    num_prefs = len(prefs)
    print(num_prefs)
    data_all = np.zeros((num_prefs, len(metrics)))
    
    metric_idx = 0
    for metric in metrics:
        data_file_path='evaluationmemtense/'+ '4suites' + '/'+'all_results/'
        data = pd.read_csv(data_file_path + date + '.csv', header=None)
        data_IPCI = np.zeros((num_prefs, 1))     
        data_IPCI[0:num_prefs,0] = get_col_data(data,metric)
        data_all[0:num_prefs,metric_idx] = data_IPCI[0:num_prefs,0]
        metric_idx = metric_idx + 1

    matplotlib.rcParams['hatch.linewidth'] = axi_line_width # 设置您想要的线宽
    ax2 = ax.twinx()
    #设置子图间隔
    # 设定条形图的宽度
    left_bar_pos = np.arange(len(prefs))
    print(left_bar_pos)
    ## 设置图像保存的路径
    legend_patch = []
    ax.plot(data_all[0:len(prefs),0],color=colors[1],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='Speedup')   
    ax2.plot([(data-0.2)/0.8*(0.4)+1.4 for data in data_all[0:len(prefs),1]],color=colors[2],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2)   
    ax2.plot([(data-0.2)/0.8*(0.4)+1.4 for data in data_all[0:len(prefs),2]],color=colors[0],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2)   
    print(data_all[0:len(prefs),1])
    legend_patch = []
    legend_patch.append(Line2D([0], [0], color=colors[1],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='Speedup'))
    legend_patch.append(Line2D([0], [0], color=colors[2],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='L1D Accuracy'))
    legend_patch.append(Line2D([0], [0], color=colors[0],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='L1D coverage'))


    # 添加矩形到轴上
    ax.add_patch(patches.Rectangle((5.8, 1.46), 0.4, 0.33, linewidth=fig_line_with+0.2, edgecolor='darkgray', facecolor='none',alpha = 1.0,zorder=2))

    # 计算x轴刻度的位置
    x_ticks = left_bar_pos
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([0,'',0.2,' ',0.4,' ',0.6,' ',0.8,' '], fontsize=fontsizes)
    # axes[ay].set_xlabel('Benchmarks', fontsize=9)
    
    y_ticks=np.around(np.arange(1.4, 1.801, 0.04), decimals=2)
    y_ticks1=np.around(np.arange(1.4, 1.801, 0.08), decimals=2)

    ax.set_ylim(1.4, 1.60)
    ax_idx = 0
    for item in y_ticks:
        if(ax_idx % 2 == 0):
            ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=0.5,zorder=1)
        else:
            ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=0.5,zorder=1)
        ax_idx += 1   
    ax.set_yticks(y_ticks1)
    ax2.set_yticks(y_ticks1)
    print(y_ticks1)
    ax.set_yticklabels([format(item,'.2f') for item in y_ticks1], fontsize=fontsizes)
    y_ticks2 = np.around(np.arange(0.2, 1.01, 0.16), decimals=2)
    ax2.set_yticks(y_ticks1)
    ax2.set_yticklabels([format(item,'.2f') for item in y_ticks2], fontsize=fontsizes)

    ax.legend(handles=legend_patch,loc='upper center', bbox_to_anchor=(0.3, 0.90), ncol=1, fontsize=fontsizes-1,
            # y 参数控制标题的位置
    handlelength=1.2,     # 控制图例句柄的长度
    handleheight=0.15,
    labelspacing=0.00,  # 控制图例句柄和文本之间的间距
    columnspacing=0.7,
    # frameon=False,
    edgecolor='none'   )

    # ax.set_ylabel("Geomean SpeedUp over no prefetching", fontsize=fontsizes)
    ax.text(-2.8,1.68,"SpeedUp",fontsize=fontsizes,ha='center',va='top',rotation = 90)
    ax.text(11.8,1.84,"Accuracy and Coverage",fontsize=fontsizes,ha='center',va='top',rotation = 90)
    # ax.text(12.1,1.70,"L1D Coverage",fontsize=fontsizes,ha='center',va='top',rotation = 90)
    
    # ax.text(-0.1,1.7,"over no prefetching",fontsize=fontsizes-1,ha='center',va='top',rotation = 90)
    # ax.set_xlabel("(e) L1D_off_threshold",  fontsize=fontsizes) 
    ax.text(0.0,1.25,"(e) L1D_ACCURACY_THRESHOLD",  fontsize=fontsizes) 

        # ax.set_title(dic_suite[trace], y=-0.28, fontsize=9) 

def plot_PB(ax):
    date = '0341'
    prefs=[]     
    data_file_path = 'evaluationmemtense/'+ traces[0] + '/'+'all_results/'
    data_pref = pd.read_csv(data_file_path + date + '.csv', header=None)
    prefs = get_col_data(data_pref,'Prefetcher')
    num_prefs = len(prefs)
    print(num_prefs)
    data_all = np.zeros((num_prefs, len(traces)))
    
    trace_idx = 0
    for trace in traces:
        data_file_path='evaluationmemtense/'+ trace + '/'+'all_results/'
        data = pd.read_csv(data_file_path + date + '.csv', header=None)
        data_IPCI = np.zeros((num_prefs, 1))     
        data_IPCI[0:num_prefs,0] = get_col_data(data,metrics[0])
        data_all[0:num_prefs,trace_idx] = data_IPCI[0:num_prefs,0]
        trace_idx = trace_idx + 1

    matplotlib.rcParams['hatch.linewidth'] = axi_line_width # 设置您想要的线宽

    #设置子图间隔
    # 设定条形图的宽度
    left_bar_pos = np.arange(len(prefs))
    print(left_bar_pos)
    ## 设置图像保存的路径
    ax.plot(data_all[0:len(prefs),0],color=colors[1],marker='o', markerfacecolor='none', label='PC',linewidth=fig_line_with,markersize=2.5,zorder=2)   


    # 添加矩形到轴上
    ax.add_patch(patches.Rectangle((3.85, 1.49), 0.3, 0.18, linewidth=fig_line_with+0.2, edgecolor='darkgray', facecolor='none',alpha = 1.0,zorder=2))

    # 计算x轴刻度的位置
    x_ticks = left_bar_pos
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([0,4,8,16,32,64,128,256], fontsize=fontsizes)
    # axes[ay].set_xlabel('Benchmarks', fontsize=9)
    
    y_ticks=np.around(np.arange(1.46, 1.511, 0.005), decimals=3)
    y_ticks1=np.around(np.arange(1.46, 1.511, 0.01), decimals=2)

    ax.set_ylim(1.46, 1.51)
    ax_idx = 0
    for item in y_ticks:
        if(ax_idx % 2 == 0):
            ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=0.5,zorder=1)
        else:
            ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=0.5,zorder=1)
        ax_idx += 1   
    ax.set_yticks(y_ticks1)
    ax.set_yticklabels([format(item,'.2f') for item in y_ticks1], fontsize=fontsizes)

    # ax.set_ylabel("Geomean SpeedUp over no prefetching", fontsize=fontsizes)
    ax.text(-2.10,1.495,"SpeedUp",fontsize=fontsizes,ha='center',va='top',rotation = 90)
    # ax.text(-0.1,1.7,"over no prefetching",fontsize=fontsizes-1,ha='center',va='top',rotation = 90)


        # ax.set_title(dic_suite[trace], y=-0.28, fontsize=9)  
    ax.text(1.0,1.44,"(f) size of prefetch buffer",  fontsize=fontsizes) 

def plot_MAX_PF(ax):
    date = '0342'
    metrics=['IPCI','L1D Accuracy','L1D Coverage']
    prefs=[]     
    data_file_path = 'evaluationmemtense/'+ traces[0] + '/'+'all_results/'
    data_pref = pd.read_csv(data_file_path + date + '.csv', header=None)
    prefs = get_col_data(data_pref,'Prefetcher')
    num_prefs = len(prefs)
    print(num_prefs)
    data_all = np.zeros((num_prefs, len(metrics)))
    ax2=ax.twinx()
    trace_idx = 0
    for metric in metrics:
        data_file_path='evaluationmemtense/'+ traces[0] + '/'+'all_results/'
        data = pd.read_csv(data_file_path + date + '.csv', header=None)
        data_IPCI = np.zeros((num_prefs, 1))     
        data_IPCI[0:num_prefs,0] = get_col_data(data,metric)
        data_all[0:num_prefs,trace_idx] = data_IPCI[0:num_prefs,0]
        trace_idx = trace_idx + 1

    matplotlib.rcParams['hatch.linewidth'] = axi_line_width # 设置您想要的线宽

    #设置子图间隔
    # 设定条形图的宽度
    left_bar_pos = np.arange(len(prefs))
    print(left_bar_pos)
    ## 设置图像保存的路径
    legend_patch = []
    ax.plot(data_all[0:len(prefs),0],color=colors[1],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='Speedup')   
    ax2.plot([(data-0.2)/0.8*(0.4)+1.4 for data in data_all[0:len(prefs),1]],color=colors[2],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2)   
    ax2.plot([(data-0.2)/0.8*(0.4)+1.4 for data in data_all[0:len(prefs),2]],color=colors[0],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2)   
    print(data_all[0:len(prefs),1])
    legend_patch = []
    legend_patch.append(Line2D([0], [0], color=colors[1],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='Speedup'))
    legend_patch.append(Line2D([0], [0], color=colors[2],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='L1D Accuracy'))
    legend_patch.append(Line2D([0], [0], color=colors[0],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='L1D coverage'))

    # 添加矩形到轴上
    ax.add_patch(patches.Rectangle((4.85, 1.48), 0.3, 0.30, linewidth=fig_line_with+0.2, edgecolor='darkgray', facecolor='none',alpha = 1.0,zorder=2))

    # 计算x轴刻度的位置
    x_ticks = left_bar_pos
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([2,4,6,8,10,12,14,16], fontsize=fontsizes)
    # axes[ay].set_xlabel('Benchmarks', fontsize=9)
    
    y_ticks=np.around(np.arange(1.4, 1.801, 0.04), decimals=2)
    y_ticks1=np.around(np.arange(1.4, 1.801, 0.08), decimals=2)

    ax.set_ylim(1.4, 1.60)
    ax_idx = 0
    for item in y_ticks:
        if(ax_idx % 2 == 0):
            ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=0.5,zorder=1)
        else:
            ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=0.5,zorder=1)
        ax_idx += 1   
    ax.set_yticks(y_ticks1)
    ax2.set_yticks(y_ticks1)
    print(y_ticks1)
    ax.set_yticklabels([format(item,'.2f') for item in y_ticks1], fontsize=fontsizes)
    y_ticks2 = np.around(np.arange(0.2, 1.01, 0.16), decimals=2)
    ax2.set_yticks(y_ticks1)
    ax2.set_yticklabels([format(item,'.2f') for item in y_ticks2], fontsize=fontsizes)

    ax.legend(handles=legend_patch,loc='upper center', bbox_to_anchor=(0.3, 0.90), ncol=1, fontsize=fontsizes-1,
            # y 参数控制标题的位置
    handlelength=1.2,     # 控制图例句柄的长度
    handleheight=0.15,
    labelspacing=0.00,  # 控制图例句柄和文本之间的间距
    columnspacing=0.7,
    # frameon=False,
    edgecolor='none'   )

    # ax.set_ylabel("Geomean SpeedUp over no prefetching", fontsize=fontsizes)
    ax.text(-2.2,1.68,"SpeedUp",fontsize=fontsizes,ha='center',va='top',rotation = 90)
    # ax.text(-0.1,1.7,"over no prefetching",fontsize=fontsizes-1,ha='center',va='top',rotation = 90)
    ax.text(9.1,1.86,"Accuracy and Coverage",fontsize=fontsizes,ha='center',va='top',rotation = 90)

        # ax.set_title(dic_suite[trace], y=-0.28, fontsize=9)  
    ax.text(-0.3,1.25,"(g) max number of used deltas",  fontsize=fontsizes) 

def plot_page_size(ax):
    prefs=[]
    date = '0343'
    metrics=['IPCI','L1D Accuracy','L1D Coverage']
    data_file_path = 'evaluationmemtense/'+ traces[0] + '/'+'all_results/'
    data_pref = pd.read_csv(data_file_path + date + '.csv', header=None)
    prefs = get_col_data(data_pref,'Prefetcher')
    num_prefs = len(prefs)
    print(num_prefs)
    data_all = np.zeros((num_prefs, len(metrics)))
    
    metric_idx = 0
    for metric in metrics:
        data_file_path='evaluationmemtense/'+ '4suites' + '/'+'all_results/'
        data = pd.read_csv(data_file_path + date + '.csv', header=None)
        data_IPCI = np.zeros((num_prefs, 1))     
        data_IPCI[0:num_prefs,0] = get_col_data(data,metric)
        data_all[0:num_prefs,metric_idx] = data_IPCI[0:num_prefs,0]
        metric_idx = metric_idx + 1

    matplotlib.rcParams['hatch.linewidth'] = axi_line_width # 设置您想要的线宽
    ax2 = ax.twinx()
    #设置子图间隔
    # 设定条形图的宽度
    left_bar_pos = np.arange(len(prefs))
    print(left_bar_pos)
    ## 设置图像保存的路径
    legend_patch = []
    ax.plot(data_all[0:len(prefs),0],color=colors[1],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='Speedup')   
    ax2.plot([(data-0.2)/0.76*(0.4)+1.4 for data in data_all[0:len(prefs),1]],color=colors[2],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2)   
    ax2.plot([(data-0.2)/0.76*(0.4)+1.4 for data in data_all[0:len(prefs),2]],color=colors[0],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2)   
    print(data_all[0:len(prefs),1])
    legend_patch = []
    legend_patch.append(Line2D([0], [0], color=colors[1],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='Speedup'))
    legend_patch.append(Line2D([0], [0], color=colors[2],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='L1D Accuracy'))
    legend_patch.append(Line2D([0], [0], color=colors[0],marker='o', markerfacecolor='none', linewidth=fig_line_with,markersize=2.5,zorder=2,label='L1D coverage'))


    # 添加矩形到轴上
    ax.add_patch(patches.Rectangle((3.85, 1.45), 0.3, 0.345, linewidth=fig_line_with+0.2, edgecolor='darkgray', facecolor='none',alpha = 1.0,zorder=2))

    # 计算x轴刻度的位置
    x_ticks = left_bar_pos
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([2,4,8,16,32,64,128,256], fontsize=fontsizes)
    # axes[ay].set_xlabel('Benchmarks', fontsize=9)
    
    y_ticks=np.around(np.arange(1.4, 1.801, 0.04), decimals=2)
    y_ticks1=np.around(np.arange(1.4, 1.801, 0.08), decimals=2)

    ax.set_ylim(1.4, 1.60)
    ax_idx = 0
    for item in y_ticks:
        if(ax_idx % 2 == 0):
            ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=0.5,zorder=1)
        else:
            ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=0.5,zorder=1)
        ax_idx += 1   
    ax.set_yticks(y_ticks1)
    ax2.set_yticks(y_ticks1)
    print(y_ticks1)
    ax.set_yticklabels([format(item,'.2f') for item in y_ticks1], fontsize=fontsizes)
    y_ticks2 = np.around(np.arange(0.2, 0.96, 0.15), decimals=2)
    ax2.set_yticks(y_ticks1)
    ax2.set_yticklabels([format(item,'.2f') for item in y_ticks2], fontsize=fontsizes)

    ax.legend(handles=legend_patch,loc='upper center', bbox_to_anchor=(0.3, 0.90), ncol=1, fontsize=fontsizes-1,
            # y 参数控制标题的位置
    handlelength=1.2,     # 控制图例句柄的长度
    handleheight=0.1,
    labelspacing=0.00,  # 控制图例句柄和文本之间的间距
    columnspacing=0.7,
    # frameon=False,
    edgecolor='none'   )

    # ax.set_ylabel("Geomean SpeedUp over no prefetching", fontsize=fontsizes)
    ax.text(-2.2,1.68,"SpeedUp",fontsize=fontsizes,ha='center',va='top',rotation = 90)
    ax.text(9.1,1.86,"Accuracy and Coverage",fontsize=fontsizes,ha='center',va='top',rotation = 90)
    # ax.text(9.5,1.70,"L1D Coverage",fontsize=fontsizes,ha='center',va='top',rotation = 90)
    
    # ax.text(-0.1,1.7,"over no prefetching",fontsize=fontsizes-1,ha='center',va='top',rotation = 90)
    # ax.set_xlabel("(e) L1D_off_threshold",  fontsize=fontsizes) 
    ax.text(1.0,1.25,"(h) logical page size /KB",  fontsize=fontsizes) 

        # ax.set_title(dic_suite[trace], y=-0.28, fontsize=9) 


if __name__ == "__main__":  
    ##get prefetcher name and data
    prefs=[]
    fig_size = (6.69, 3.2)
    fig= plt.figure(figsize=fig_size, dpi=600)
    gs = gridspec.GridSpec(3,6,width_ratios=[1,0.44, 1,0.44, 1,0.24],figure=fig)
    ax1 = fig.add_subplot(gs[0, 0:1])#his_num
    ax2 = fig.add_subplot(gs[0, 2:6])#table_size
    ax3 = fig.add_subplot(gs[1, 0:1])#conf1
    ax4 = fig.add_subplot(gs[1, 2:3])#conf2
    ax5 = fig.add_subplot(gs[1, 4:5])#off
    ax6 = fig.add_subplot(gs[2, 0:1])#PB
    ax7 = fig.add_subplot(gs[2, 2:3])#pf_num
    ax8 = fig.add_subplot(gs[2, 4:5])#page_size
    plot_hisnum(ax1)
    plot_table_size(ax2)

    plot_thresh_L1D(ax3)
    plot_thresh_L2C(ax4)
    plot_L1D_off(ax5)
    plot_PB(ax6)
    
    plot_MAX_PF(ax7)
    plot_page_size(ax8)

    plt.subplots_adjust(left=0, right=1.0, bottom=0, top=1.0, wspace=0.08, hspace=0.6)

    ## 设置图像保存的路径
    figure_res='analysis_py/evaluation3/dse/'
    if not os.path.exists(figure_res):
        os.makedirs(figure_res)
    
   
    plt.savefig(f'{figure_res}/dse.png',dpi=800, format="png", bbox_inches='tight') 
    plt.savefig(f'{figure_res}/dse.pdf',dpi=800, format="pdf", bbox_inches='tight') 
    plt.savefig(f'{figure_res}/dse.eps',dpi=300, format="eps", bbox_inches='tight') 
    plt.close()   

        
