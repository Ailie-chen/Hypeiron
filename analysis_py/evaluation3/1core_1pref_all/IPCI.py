import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
import math
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Patch
# 3.23 1.3
dates=["0326"]
traces=["spec2k06" ,"spec2k17","gap","parsec","4suites"]
dic_suite={
    'spec2k06':'SPEC06',
    'spec2k17':'SPEC17',
    'gap':"GAP",
    'parsec':'PARSEC',
    '4suites':"Geomean"
}
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

        matplotlib.rcParams['hatch.linewidth'] = 0.75  # 设置您想要的线宽
        fig_size = (3.5, 1.5)
        fig, ax = plt.subplots(figsize=fig_size)
        #设置子图间隔
        # 设定条形图的宽度
        bar_width = 1.0 / (num_prefs + 2.0)
        left_bar_pos = np.arange(len(traces))
        print(left_bar_pos)
        ## 设置图像保存的路径
        figure_res='analysis_py/evaluation3/1core_1pref_all/'
        if not os.path.exists(figure_res):
                os.makedirs(figure_res) 
        legend_patch = []   
        for i in range(num_prefs):
            ax.bar(left_bar_pos + bar_width * i, 
                data_all[i,0:len(traces)], 
                width=bar_width, 
                edgecolor='none',  # 边框颜色
                color=colors[i],      # 填充颜色
                linewidth=0.75,zorder=3)
            legend_patch.append(Patch(facecolor=colors[i], edgecolor='none',label=legends[prefs[i]]))



            # 计算x轴刻度的位置
            x_ticks = left_bar_pos + bar_width * ((num_prefs)/2-0.5)
            ax.set_xticks(x_ticks)
            ax.set_xticklabels([dic_suite[trace] for trace in traces], fontsize=fontsizes)
            # axes[ay].set_xlabel('Benchmarks', fontsize=9)
           
            y_ticks=np.around(np.arange(1.0, 1.7, 0.1), decimals=1)
            y_ticks1=np.around(np.arange(1.0, 1.7, 0.2), decimals=1)

            ax.set_ylim(1.0, 1.7)
            ax_idx = 0
            for item in y_ticks:
                if(ax_idx % 2 == 0):
                    ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=0.5,zorder=1)
                else:
                    ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=0.5,zorder=1)
                ax_idx += 1   
            ax.set_yticks(y_ticks1)
            ax.set_yticklabels([f'{item}' for item in y_ticks1], fontsize=fontsizes)

            ax.set_ylabel("SpeedUp", fontsize=fontsizes)
            ax.legend(handles=legend_patch,loc='upper center', bbox_to_anchor=(0.5, 1.20), ncol=4, fontsize=fontsizes,
             # y 参数控制标题的位置
        handlelength=1.2,     # 控制图例句柄的长度
        handletextpad=0.2,  # 控制图例句柄和文本之间的间距
        columnspacing=0.5,
        edgecolor='none'   )
            # ax.set_title(dic_suite[trace], y=-0.28, fontsize=9) 





        plt.savefig(f'{figure_res}/1core_1pref_IPCI.png',dpi=800, format="png", bbox_inches='tight') 
        plt.savefig(f'{figure_res}/1core_1pref_IPCI.pdf',dpi=800, format="pdf", bbox_inches='tight') 
        plt.close()   

        
