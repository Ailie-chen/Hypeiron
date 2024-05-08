import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
import math
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Patch
import matplotlib.patches as patches
# 3.23 1.3
dates=["0341"]
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
metrics=['IPCI']
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
        fig_size = (2.23, 1.5)
        fig, ax = plt.subplots(figsize=fig_size)

        #设置子图间隔
        # 设定条形图的宽度
        left_bar_pos = np.arange(len(prefs))
        print(left_bar_pos)
        ## 设置图像保存的路径
        figure_res='analysis_py/evaluation3/PB/'
        if not os.path.exists(figure_res):
                os.makedirs(figure_res) 
        legend_patch = []
        ax.plot(data_all[0:len(prefs),0],color=colors[1],marker='o', markerfacecolor='none', label='PC',linewidth=fig_line_with,markersize=2.5,zorder=2)   


        # 添加矩形到轴上
        ax.add_patch(patches.Rectangle((3.8, 1.495), 0.4, 0.01, linewidth=fig_line_with, edgecolor=colors[3], facecolor='none',zorder=2))

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
        ax.set_yticklabels([f'{item}' for item in y_ticks1], fontsize=fontsizes)

        # ax.set_ylabel("Geomean SpeedUp over no prefetching", fontsize=fontsizes)
        ax.text(-2.0,1.495,"SpeedUp",fontsize=fontsizes,ha='center',va='top',rotation = 90)
        # ax.text(-0.1,1.7,"over no prefetching",fontsize=fontsizes-1,ha='center',va='top',rotation = 90)


            # ax.set_title(dic_suite[trace], y=-0.28, fontsize=9) 

        ax.set_xlabel("(f) size of prefetch buffer",  fontsize=fontsizes) 




        plt.savefig(f'{figure_res}/PB.png',dpi=800, format="png", bbox_inches='tight') 
        plt.savefig(f'{figure_res}/PB.pdf',dpi=800, format="pdf", bbox_inches='tight') 
        plt.close()   

        
