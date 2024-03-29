import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
from matplotlib.patches import Patch
# 3.23 1.3
#dates=["1123"]
dates=["0102"]
metrics=["L1D traffic","L2C traffic","LLC traffic"]
metrics=["L1D traffic" ,"L2C traffic","LLC traffic","DRAM traffic"]

dic_suite={
    'L1D traffic':"L1D",
    'L2C traffic':"L2C",
    'LLC traffic':"LLC",
    "DRAM traffic":"DRAM"
}
legends={"mlop_dpc3":"MLOP",
        "mlop_dpc3+bingo_dpc3":"MLOP+Bingo",
        "mlop_dpc3+ppf":"MLOP+SPP-PPF",
        "vberti":"Berti",
        "vberti+bingo_dpc3":"Berti+Bingo",
        "vberti+ppf":"Berti+SPP-PPF",
        "hyperion_hpc":"Hyperion",
        "hyperion_hpc+bingo_dpc3":"Hyperion+Bingo",
        "hyperion_hpc+ppf":"Hyperion+SPP-PPF"}

hatches = ['//////','','\\\\\\\\\\', '//////','','\\\\\\\\\\',  '', '...','\\\\\\\\\\'] #'xxxxx',
colors = [ 'white','white','white','grey','grey','grey','black','black','black']


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
        
        data_file_path = 'evaluationmemtense/'+ '4suites' + '/'+'all_results/'
        data_pref = pd.read_csv(data_file_path + date + '.csv', header=None)
        prefs = get_col_data(data_pref,'Prefetcher')
        num_prefs = len(prefs)
        i = 0
        data_all = np.zeros((num_prefs, len(metrics)))
        for metric in metrics:
            data_file_path='evaluationmemtense/'+ '4suites' + '/'+'all_results/'
            data = pd.read_csv(data_file_path + date + '.csv', header=None)
            data_all[0:num_prefs,i] = get_col_data(data,metric)
            i = i + 1
        print(data_all)

        ## 设置图像保存的路径
        figure_res='analysis_py/evaluation2/1core_mpref_all/'
        if not os.path.exists(figure_res):
                os.makedirs(figure_res)
        matplotlib.rcParams['hatch.linewidth'] = 0.75  # 设置您想要的线宽
        ###绘制图形
        fig_size = (3.23, 1.3)
        fig, ax = plt.subplots(figsize=fig_size)
        # 设定条形图的宽度
        bar_width = 1.0 / (num_prefs-1 + 1.5)
        left_bar_pos = np.arange(len(metrics))

        # 生成每个预取器的条形图
        # max_v, min_v = np.NINF, np.inf
        min_v = 1.0
        max_v = 2.0
        ax_ytick1 = np.arange(min_v,max_v+0.01,0.1)
        ax_ytick = np.arange(min_v,max_v+0.01,0.2)
        legend_patch=[]
        for i in np.arange(1,num_prefs):
            value = data_all[i,:]
            # value = value.replace('-', 0)
            piece = value.astype(float)
            # max_v = max(piece.max(), max_v)
            # min_v = min(piece.min(), min_v)
            if(colors[i-1] == 'black'):
                ax.bar(left_bar_pos + bar_width * i, 
                piece, 
                width=bar_width, 
                edgecolor='black',  # 边框颜色
                color=colors[i-1],      # 填充颜色
                linewidth=0.75,zorder=2)
                ax.bar(left_bar_pos + bar_width * i,piece,width=bar_width, color='none', edgecolor='white',hatch=hatches[i-1], linewidth=0,zorder=3)
                legend_patch.append(Patch(facecolor ='black', edgecolor='white', hatch=hatches[i-1], label=legends[prefs[i]]))
            else:
                ax.bar(left_bar_pos + bar_width * i, 
                piece, 
                width=bar_width, 
                edgecolor='black',  # 边框颜色
                color=colors[i-1],      # 填充颜色
                hatch=hatches[i-1],linewidth=0.75,zorder=3)
                legend_patch.append(Patch(facecolor=colors[i-1], edgecolor='black', hatch=hatches[i-1], label=legends[prefs[i]]))
        

        # ##画纵轴的虚线
        ax_idx = 0
        for item in ax_ytick1:
            if(ax_idx % 2 == 0):
                ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=1,zorder=1)
            else:
                ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=1,zorder=1)
            ax_idx += 1


        # 旋转之后还需要向左平移
        plt.xticks(left_bar_pos + bar_width*((num_prefs-1)/2+0.5),  [dic_suite[item] for item in metrics], rotation=0, fontsize=8)
        plt.yticks(ax_ytick, fontsize=9)
        plt.ylim(min_v, 2.0)
        for label in ax.get_yticklabels():
            label.set_fontsize(8)
        # ax.set_xlabel('Benchmarks', fontsize=8)
        ax.set_ylabel("Normalized Traffic", fontsize=8)
        # ax.set_title(f'IPCI', fontsize=8)
        ax.legend(handles=legend_patch,loc='upper center', bbox_to_anchor=(0.5, 1.95), ncol=2,fontsize=8,
       handlelength=1.2,     # 控制图例句柄的长度
        handletextpad=0.2,  # 控制图例句柄和文本之间的间距
        columnspacing=0.5,
        edgecolor='black'   )
        plt.savefig(f'{figure_res}/1core_mpref_Traffic.png',dpi=800, format="png", bbox_inches='tight') 
        plt.savefig(f'{figure_res}/1core_mpref_Traffic.pdf',dpi=800, format="pdf", bbox_inches='tight') 
        plt.close()   

        
