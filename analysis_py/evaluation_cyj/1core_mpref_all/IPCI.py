import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
import math
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Patch
# 3.23 1.3
#dates=["1123"]
dates=["0102"]
traces=["spec2k17" ,"gap", "ligra","cs"]
dic_suite={
    'spec2k17':'SPEC',
    'gap':"GAP",
    'ligra':"Ligra",
    'cs':"CloudSuite"
}
metrics=['IPCI']
legends={"mlop_dpc3":"MLOP",
        "mlop_dpc3+bingo_dpc3":"MLOP+Bingo",
        "mlop_dpc3+ppf":"MLOP+SPP-PPF",
        "ipcp_isca2020":"IPCP",
        "ipcp_isca2020+ipcp_isca2020":"IPCP+IPCP",
        "vberti":"Berti",
        "vberti+bingo_dpc3":"Berti+Bingo",
        "vberti+ppf":"Berti+SPP-PPF",
        "hyperion_hpc":"Hyperion",
        "hyperion_hpc+bingo_dpc3":"Hyperion+Bingo",
        "hyperion_hpc+ppf":"Hyperion+SPP-PPF"}

hatches = ['','/////','\\\\\\\\\\', '--','...','', '/////','\\\\\\\\\\',  '', '/////','\\\\\\\\\\'] #'xxxxx',
colors = [ 'white','white','white','white','white','grey','grey','grey','black','black','black']
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
        fig_size = (7, 1.25)
        fig, axes = plt.subplots(1,4,figsize=fig_size)
        #设置子图间隔
        plt.subplots_adjust(left=0, right=1.0, bottom=0, top=1.0, wspace=0.3, hspace=0.37)
        # 设定条形图的宽度
        bar_width = 1.0 / (num_prefs-1 + 2.0)
        left_bar_pos = np.arange(len(metrics))
        ## 设置图像保存的路径
        figure_res='analysis_py/evaluation2/1core_mpref_all/'
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
            min_v = 1.0
            max_v = data_all[1:num_prefs,:].max().max()
            legend_patch = []
            for i in np.arange(1,num_prefs):
                value = data_all[i,:]
                # value = value.replace('-', 0)
                piece = value.astype(float)
                # max_v = max(piece.max(), max_v)
                # min_v = min(piece.min(), min_v)
                if(colors[i-1] == 'black'):
                    axes[ay].bar(left_bar_pos + bar_width * i, 
                    piece, 
                    width=bar_width*0.95, 
                    edgecolor='black',  # 边框颜色
                    color=colors[i-1],      # 填充颜色
                    linewidth=0.75,zorder=2)
                    axes[ay].bar(left_bar_pos + bar_width * i,piece,width=bar_width, color='none', edgecolor='white',hatch=hatches[i-1], linewidth=0,zorder=3)
                    legend_patch.append(Patch(facecolor ='black', edgecolor='white', hatch=hatches[i-1], label=legends[prefs[i]]))
                else:
                    axes[ay].bar(left_bar_pos + bar_width * i, 
                    piece, 
                    width=bar_width*0.95, 
                    edgecolor='black',  # 边框颜色
                    color=colors[i-1],      # 填充颜色
                    hatch=hatches[i-1],linewidth=0.75,zorder=3)
                    legend_patch.append(Patch(facecolor=colors[i-1], edgecolor='black', hatch=hatches[i-1], label=legends[prefs[i]]))
                if(i==5):
                        legend_patch.append(Patch(facecolor ='white', edgecolor='none', hatch='', label=''))
            



            # 计算x轴刻度的位置
            x_ticks = left_bar_pos + bar_width * ((num_prefs - 1) / 2 + 0.5)
            axes[ay].set_xticks(x_ticks)
            axes[ay].set_xticklabels([''], fontsize=9)
            # axes[ay].set_xlabel('Benchmarks', fontsize=9)
           

            if(max_v < 1.10):
                y_ticks = np.around(np.arange(1.0, 1.25, 0.05), decimals=2)
                y_ticks1 = np.around(np.arange(1.0, 1.25, 0.025), decimals=3)
                min_v = 1.0
            elif(max_v < 1.3):
                y_ticks = np.around(np.arange(1.1, 1.3, 0.04), decimals=2)
                y_ticks1 = np.around(np.arange(1.1, 1.3, 0.02), decimals=2)
                min_v = 1.1
            elif(max_v < 1.4):
                y_ticks = np.around(np.arange(1.2, 1.4, 0.04), decimals=2)
                y_ticks1 = np.around(np.arange(1.2, 1.4, 0.02), decimals=2)
                min_v = 1.2
            elif(max_v < 1.7):
                y_ticks = np.around(np.arange(1.38, 1.7, 0.08), decimals=2)
                y_ticks1 = np.around(np.arange(1.38, 1.7, 0.04), decimals=2)
                min_v = 1.38
            elif(max_v < 100):
                y_ticks = np.around(np.arange(0, 110, 20), decimals=0)
                y_ticks1 = np.around(np.arange(0, 110, 10), decimals=0)
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
                axes[ay].set_ylabel("SpeedUp", fontsize=9)
            # ax.set_title(f'IPCI', fontsize=9)
            if(ax== 0 and ay == 0):
                axes[ay].legend(handles=legend_patch,loc='upper center', bbox_to_anchor=(2.15, 1.63), ncol=4, fontsize=9,
             # y 参数控制标题的位置
        handlelength=1.2,     # 控制图例句柄的长度
        handletextpad=0.2,  # 控制图例句柄和文本之间的间距
        columnspacing=0.5,
        edgecolor='black'   )
            axes[ay].set_title(dic_suite[trace], y=-0.28, fontsize=9) 





        plt.savefig(f'{figure_res}/1core_mpref_IPCI.png',dpi=800, format="png", bbox_inches='tight') 
        plt.savefig(f'{figure_res}/1core_mpref_IPCI.pdf',dpi=800, format="pdf", bbox_inches='tight') 
        plt.close()   

        
