import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
import math
from matplotlib.font_manager import FontProperties
# 3.23 1.3
#dates=["1123"]
dates=["0106"]
traces=["cs"]
metrics=['L1D Coverage','L2C Coverage', "LLC Coverage"]
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
def get_col_data(data,metric,bench):
    # 找出第0列包含'A'的行
    rows_with_A = data.iloc[:, 1] == metric
    cols_with_B = data.iloc[0, :] == bench

    metric_data = data.loc[rows_with_A, cols_with_B]
    first_column_array = np.array(metric_data)
    first_column_array = first_column_array[:,0]
    # first_column_array = np.where(first_column_array == '-', '0', first_column_array)
    # Convert the array back to its original numeric type if necessary  
    # print(first_column_array)
    return first_column_array

# 在这里替换为你想要的指标
if __name__ == "__main__":  
    for date in dates:
        ##get prefetcher name and data
        prefs=[]
        
        data_file_path = 'evaluationmemtense/'+ traces[0] + '/'+'all_results_figs/'
        data_pref = pd.read_csv(data_file_path + date + 'merge.csv', header=None).T
        num_benchs = data_pref.shape[1]-2
        benchs_name = data_pref.iloc[0,2:].tolist()
        num_prefs = data_pref.iloc[:,1].tolist().count('IPCI')
        prefs = data_pref.iloc[:,0].loc[data_pref.iloc[:,1] == 'IPCI']
        prefs = np.array(prefs)
        print(prefs)
        
        data_all = np.zeros((num_prefs, len(benchs_name)))
        data_file_path = 'evaluationmemtense/'+ traces[0] + '/'+'all_results_figs/'
        data = pd.read_csv(data_file_path + date + 'merge.csv', header=None).T
        i = 0
        for bench in benchs_name:   
            data_all[0:num_prefs,i] = get_col_data(data,'IPCI',bench)
            i = i + 1


        min_v = 1.0
        max_v = 1.1
        matplotlib.rcParams['hatch.linewidth'] = 0.75  # 设置您想要的线宽
        fig_size = (3.45, 1.2)
        fig, ax = plt.subplots(figsize=fig_size)
        #设置子图间隔
        # 设定条形图的宽度
        bar_width = 1.0 / (num_prefs-1 + 1.2)
        left_bar_pos = np.arange(len(benchs_name))
        ## 设置图像保存的路径
        figure_res='analysis_py/evaluation2/1core_1pref_detail/'
        if not os.path.exists(figure_res):
                os.makedirs(figure_res)
        for i in np.arange(1,num_prefs):

            value = data_all[i,:]
            # value = value.replace('-', 0)
            piece = value.astype(float)
            # max_v = max(piece.max(), max_v)
            # min_v = min(piece.min(), min_v)
            print(prefs[i])
            ax.bar(left_bar_pos + bar_width * i, 
                piece, 
                width=bar_width, 
                
                label=legends[prefs[i]],
                edgecolor='black',  # 边框颜色
                color=colors[i-1],      # 填充颜色
                hatch=hatches[i-1],linewidth=0.75,zorder=3)
        



        # 计算x轴刻度的位置
        x_ticks = left_bar_pos + bar_width * ((num_prefs - 1) / 2 + 0.5)
        ax.set_xticks(x_ticks)
        benchs_name[len(benchs_name)-1] = 'Geomean'
        ax.set_xticklabels(benchs_name, fontsize=9,rotation = 20,ha ='right')
        # ax.set_xlabel('Benchmarks', fontsize=9)
        
        ax.set_xlim(-0.2, num_benchs)
        
        if(max_v < 0.5):
            y_ticks = np.around(np.arange(0, 0.51, 0.1), decimals=1)
            y_ticks1 = np.around(np.arange(0, 0.51, 0.05), decimals=2)
            max_v=0.5
        else:
            y_ticks = np.around(np.arange(0.8, 1.21, 0.08), decimals=2)
            y_ticks1 = np.around(np.arange(0.8, 1.21, 0.04), decimals=2)
        ax_idx = 1.10
        ax.set_ylim(min_v, max_v)
        ax_idx=0
        for item in y_ticks1:
            if(item == 1.0):
                ax.axhline(float(item), color='black', linestyle='-', linewidth=1,zorder=1)
            elif(ax_idx % 2 == 0):
                ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=1,zorder=1)
            else:
                ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=1,zorder=1)
            ax_idx += 1   
        ax.set_yticks(y_ticks)
        ax.set_yticklabels([f'{item}' for item in y_ticks], fontsize=9)

        current_yticks = ax.get_yticks()
        ax.set_yticklabels(current_yticks, fontsize=9)
        ax.set_ylabel("SpeedUp", fontsize=9)
        # ax.set_title(f'IPCI', fontsize=9)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.35), ncol=4, fontsize=9,
            # y 参数控制标题的位置
            handlelength=1.2,     # 控制图例句柄的长度
            handletextpad=0.2,  # 控制图例句柄和文本之间的间距
            columnspacing=0.5,
            edgecolor='black'   )
        # ax.set_title(traces[0], y=-0.70, fontsize=9) 

        # ax.set_title('', y=-3, fontsize=9)



        plt.savefig(f'{figure_res}/1core_1pref_IPCI_{traces[0]}.png',dpi=800, format="png", bbox_inches='tight') 
        plt.savefig(f'{figure_res}/1core_1pref_IPCI_{traces[0]}.pdf',dpi=800, format="pdf", bbox_inches='tight') 
        plt.close()   

        
