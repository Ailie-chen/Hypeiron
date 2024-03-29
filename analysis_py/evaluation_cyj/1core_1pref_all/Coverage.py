import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
import math
from matplotlib.font_manager import FontProperties
# 3.23 1.3
#dates=["1123"]
dic_suite={
    'spec2k17':'SPEC',
    'gap':"GAP",
    'ligra':"Ligra",
    'cs':"CloudSuite"
}
dates=["0106"]
traces=["spec2k17" ,"gap", "ligra" ,"cs"]
metrics=['L1D Coverage','L2C Coverage']
legends={"ipcp_isca2020":"IPCP",
         "mlop_dpc3":"MLOP",
         "vberti":"Berti",
         "hyperion_hpc":"Hyperion",
         "bingo_dpc3":"Bingo",
         "ppf":'SPP-PPF'}
Benchs={"ipcp_isca2020":"IPCP",
         "mlop_dpc3":"MLOP",
         "vberti":"Berti",
         "hyperion_hpc":"Hyperion",
         "bingo_dpc3":"Bingo",
         "ppf":'SPP-PPF'}
hatches = ['\\\\\\\\\\',   '', '', '', ''] #'xxxxx',
colors = [ 'white','white','grey','black']
font = {
        "family": "Arial",
        "color": "black",
        "weight": "normal",
        "size": 8,
    }
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
    print(first_column_array)
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
        data_all = np.zeros((num_prefs, len(traces)))
        matplotlib.rcParams['hatch.linewidth'] = 0.75  # 设置您想要的线宽
        fig_size = (6.5, 1.2)
        fig, axes = plt.subplots(1,4,figsize=fig_size)
        #设置子图间隔
        plt.subplots_adjust(left=0, right=1.0, bottom=0, top=1.0, wspace=0.3, hspace=0.37)
        # 设定条形图的宽度
        bar_width = 1.0 / (num_prefs-1 + 2.0)
        left_bar_pos = np.arange(len(metrics))
        ## 设置图像保存的路径
        figure_res='analysis_py/evaluation2/1core_1pref_all/'
        if not os.path.exists(figure_res):
                os.makedirs(figure_res)
        
        trace_idx = 0
        for trace in traces:
            ax = math.floor(trace_idx / 4) 
            ay = trace_idx % 4
            trace_idx += 1
            data_all = np.zeros((num_prefs, len(metrics)))
            data_file_path='evaluationmemtense/'+ trace + '/'+'all_results/'
            data = pd.read_csv(data_file_path + date + '.csv', header=None)
            i = 0
            for metric in metrics:       
                data_all[0:num_prefs,i] = get_col_data(data,metric)
                i = i + 1
            min_v = 0
            max_v = (data_all.max().max() )
            
            for i in np.arange(1,num_prefs):

                value = data_all[i,:]
                # value = value.replace('-', 0)
                piece = value.astype(float)
                # max_v = max(piece.max(), max_v)
                # min_v = min(piece.min(), min_v)
                axes[ay].bar(left_bar_pos + bar_width * i, 
                    piece, 
                    width=bar_width, 
                    label=legends[prefs[i]],
                    edgecolor='black',  # 边框颜色
                    color=colors[i-1],      # 填充颜色
                    hatch=hatches[i-1],linewidth=0.75,zorder=3)
            



            # 计算x轴刻度的位置
            x_ticks = left_bar_pos + bar_width * ((num_prefs - 1) / 2 + 0.5)
            axes[ay].set_xticks(x_ticks)
            axes[ay].set_xticklabels(['L1D','L2C'], fontsize=9)
            # axes[ay].set_xlabel('Benchmarks', fontsize=9)
            
            
            if(max_v < 0.5):
                y_ticks = np.around(np.arange(0, 0.51, 0.1), decimals=1)
                y_ticks1 = np.around(np.arange(0, 0.51, 0.05), decimals=2)
                max_v = 0.5
            else:
                y_ticks = np.around(np.arange(0, 1.01, 0.2), decimals=1)
                y_ticks1 = np.around(np.arange(0, 1.01, 0.1), decimals=1)
                max_v = 1.0

            axes[ay].set_ylim(min_v, max_v)
            ax_idx = 0
            for item in y_ticks1:
                if(ax_idx % 2 == 0):
                    axes[ay].axhline(float(item), color='lightgray', linestyle='-', linewidth=1,zorder=1)
                else:
                    axes[ay].axhline(float(item), color='lightgray', linestyle='--', linewidth=1,zorder=1)
                ax_idx += 1   
            axes[ay].set_yticks(y_ticks)
            axes[ay].set_yticklabels([f'{item}' for item in y_ticks], fontsize=9)

            current_yticks = axes[ay].get_yticks()
            axes[ay].set_yticklabels(current_yticks, fontsize=9)
            if(ay == 0):
                axes[ay].set_ylabel("Coverage", fontsize=9)
            # ax.set_title(f'IPCI', fontsize=9)
            if(ax== 0 and ay == 0):
                axes[ay].legend(loc='upper center', bbox_to_anchor=(2.45, 1.30), ncol=4, fontsize=9,
             # y 参数控制标题的位置
        handlelength=1.2,     # 控制图例句柄的长度
        handletextpad=0.2,  # 控制图例句柄和文本之间的间距
        columnspacing=0.5,
        edgecolor='black'   )
            axes[ay].set_title(dic_suite[trace], y=-0.36, fontsize=9) 





        plt.savefig(f'{figure_res}/1core_1pref_coverage.png',dpi=800, format="png", bbox_inches='tight') 
        plt.savefig(f'{figure_res}/1core_1pref_coverage.pdf',dpi=800, format="pdf", bbox_inches='tight') 
        plt.close()   

        
