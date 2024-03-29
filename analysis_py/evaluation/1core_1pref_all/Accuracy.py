import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
# 3.23 1.3
#dates=["1123"]
dates=["0101"]
traces=["spec2k17" ,"gap", "ligra" ,"cs"]
dic_suite={
    'spec2k17':'SPEC',
    'gap':"GAP",
    'ligra':"Ligra",
    'cs':"CloudSuite"
}
metrics=['Prefetcher','L1D Accuracy']
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
        i = 0
        data_all = np.zeros((num_prefs, len(traces)))
        for trace in traces:
            data_file_path='evaluationmemtense/'+ trace + '/'+'all_results/'
            data = pd.read_csv(data_file_path + date + '.csv', header=None)
            data_all[0:num_prefs,i] = get_col_data(data,'Accuracy')
            i = i + 1
        print(data_all)

        ## 设置图像保存的路径
        figure_res='analysis_py/evaluation/1core_1pref_all/'
        if not os.path.exists(figure_res):
                os.makedirs(figure_res)
        matplotlib.rcParams['hatch.linewidth'] = 0.75  # 设置您想要的线宽
        ###绘制图形
        fig_size = (3.23, 1.3)
        fig, ax = plt.subplots(figsize=fig_size)
        # 设定条形图的宽度
        bar_width = 1.0 / (num_prefs-1 + 1.5)
        left_bar_pos = np.arange(len(traces))

        # 生成每个预取器的条形图
        # max_v, min_v = np.NINF, np.inf
        min_v = 0
        max_v = data_all.max().max() + 0.1
        ax_ytick1 = np.arange(min_v,max_v,0.1)
        ax_ytick = np.arange(min_v,max_v,0.2)
        for i in np.arange(1,num_prefs):
            value = data_all[i,:]
            # value = value.replace('-', 0)
            piece = value.astype(float)
            # max_v = max(piece.max(), max_v)
            # min_v = min(piece.min(), min_v)
            ax.bar(left_bar_pos + bar_width * i, 
                piece, 
                width=bar_width, 
                label=legends[prefs[i]],
                edgecolor='black',  # 边框颜色
                color=colors[i-1],      # 填充颜色
                hatch=hatches[i-1],linewidth=0.75,zorder=3)
        

        # ##画纵轴的虚线
        ax_idx = 0
        for item in ax_ytick1:
            if(ax_idx % 2 == 0):
                ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=1,zorder=1)
            else:
                ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=1,zorder=1)
            ax_idx += 1


        # 旋转之后还需要向左平移
        plt.xticks(left_bar_pos + bar_width*((num_prefs-1)/2+0.5),  [dic_suite[item] for item in traces], rotation=0, fontsize=8)
        plt.yticks(ax_ytick, fontsize=9)
        plt.ylim(min_v, 1.0)
        for label in ax.get_yticklabels():
            label.set_fontsize(8)
        # ax.set_xlabel('Benchmarks', fontsize=8)
        ax.set_ylabel("Accuracy", fontsize=8)
        # ax.set_title(f'IPCI', fontsize=8)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.28), ncol=num_prefs-1,fontsize=8,
        handlelength=1.2,     # 控制图例句柄的长度
        handletextpad=0.2,  # 控制图例句柄和文本之间的间距
        columnspacing=0.5,
        edgecolor='black'   )
        plt.savefig(f'{figure_res}/1core_1pref_Accuracy.png',dpi=800, format="png", bbox_inches='tight') 
        plt.savefig(f'{figure_res}/1core_1pref_Accuracy.pdf',dpi=800, format="pdf", bbox_inches='tight') 
        plt.close()   

        
