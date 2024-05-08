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
# 3.23 1.3
dates=["0337"]
traces=["4suites"]
dic_suite={
    'spec2k06':'SPEC06',
    'spec2k17':'SPEC17',
    'gap':"GAP",
    'parsec':'PARSEC',
    '4suites':"Geomean"
}
axi_line_width = 0.5
fig_line_with = 0.75
colors = ['#FEB3AE','#73bad6','#CD5C5C','#0E5378',"#0E5378",'#ef4143','#bd3752','#c4323f']
fontsizes=7
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

# 在这里替换为你想要的指标
if __name__ == "__main__":  
    for date in dates:
        ##get prefetcher name and data
        prefs=[]
        
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
        fig_size = (2.23, 1.5)
        fig, ax = plt.subplots(figsize=fig_size)
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
        ax.add_patch(patches.Rectangle((2.8, 1.42), 0.4, 0.34, linewidth=fig_line_with, edgecolor=colors[3], facecolor='none',zorder=2))

        # 计算x轴刻度的位置
        x_ticks = left_bar_pos
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([0.5,0.6,0.7,0.8,0.9], fontsize=fontsizes)
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
        y_ticks2 = np.around(np.arange(0.45, 0.96, 0.10), decimals=2)
        ax2.set_yticks(y_ticks1)
        ax2.set_yticklabels([format(item,'.2f') for item in y_ticks2], fontsize=fontsizes)

        ax.legend(handles=legend_patch,loc='upper center', bbox_to_anchor=(0.30, 0.70), ncol=1, fontsize=fontsizes,
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
        ax.text(5.2,1.75,"L1D Accuracy and",fontsize=fontsizes,ha='center',va='top',rotation = 90)
        ax.text(5.5,1.71,"L1D Coverage",fontsize=fontsizes,ha='center',va='top',rotation = 90)
        

        ax.set_xlabel("(c) L1D_threshold",  fontsize=fontsizes) 





        plt.savefig(f'{figure_res}/L1D.png',dpi=800, format="png", bbox_inches='tight') 
        plt.savefig(f'{figure_res}/L1D.pdf',dpi=800, format="pdf", bbox_inches='tight') 
        plt.close()   

        
