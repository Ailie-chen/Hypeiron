import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
# 3.23 1.3
#dates=["1123"]
dates=["1230"]
traces=["spec2k17"]
metrics=['Prefetcher','IPCI']
# markers=['o', '.', ',', 'x', '+', '_', '|', 's', 'd', '^', 'v', '<', '>', 'p', '*', 'h', 'H']
markers=['o','d','d','o','s','s','o','s','o','s','s','o','s','s']
markerfacecolors=['white','white','white','grey','grey','grey','darkgrey','darkgrey','lightgrey','lightgrey','lightgrey','black','black','black']
legends={"ipcp_isca2020":"IPCP",
         "mlop_dpc3":"MLOP",
         "vberti":"Berti",
         "hyperion_hpc":"Hyperion",
         "bingo_dpc3":"Bingo",
         "ppf":'SPP-PPF'}
Benchs={"ipcp_isca2020":"IPCP",
         "bingo_dpc3l2":"Bingo",
         "ppfl2":'SPP-PPF',
         "mlop_dpc3":"MLOP",
         "mlop_dpc3+bingo_dpc3":"MLOP+Bingo",
        "mlop_dpc3+ppf":"MLOP+SPP-PPF",
        "ipcp_isca2020+ipcp_isca2020":"IPCP+IPCP",
        "vberti":"Berti",
        "vberti+bingo_dpc3":"Berti+Bingo",
        "vberti+ppf":"Berti+SPP-PPF",
        "hyperion_hpc":"Hyperion",
        "hyperion_hpc+bingo_dpc3":"Hyperion+Bingo",
        "hyperion_hpc+ppf":"Hyperion+SPP-PPF"}
storage={"ipcp_isca2020":0.895,
         "bingo_dpc3l2":124,
         "ppfl2":39.34,
         "mlop_dpc3":12.66,
         "mlop_dpc3+bingo_dpc3":12.66+124,
        "mlop_dpc3+ppf":12.66+39.34,
        "ipcp_isca2020+ipcp_isca2020":0.895*2,
        "vberti":2.55,
        "vberti+bingo_dpc3":2.55+124,
        "vberti+ppf":2.55+39.34,
        "hyperion_hpc":4.13,
        "hyperion_hpc+bingo_dpc3":4.13+124,
        "hyperion_hpc+ppf":4.13+39.34}
ha_offset = 1
text_pos={"ipcp_isca2020":[0.895+2,1.515],
         "bingo_dpc3l2":[127,1.523],
         "ppfl2":[39.34+3,1.54],
         "mlop_dpc3":[12.8+2,1.50],
         "mlop_dpc3+bingo_dpc3":[12.66+124-20,1.555],
        "mlop_dpc3+ppf":[12.66+39.34-15,1.563],
        "ipcp_isca2020+ipcp_isca2020":[0.895*2-2,1.56],
        "vberti":[2.55+3,1.538],
        "vberti+bingo_dpc3":[2.55+124-20,1.61],
        "vberti+ppf":[2.55+39.34-20,1.61],
        "hyperion_hpc":[4.65+ha_offset+1,1.59],
        "hyperion_hpc+bingo_dpc3":[4.65+124-20,1.645],
        "hyperion_hpc+ppf":[4.65+39.34-38,1.645]}
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
    print(first_column_array)
    return first_column_array

# 在这里替换为你想要的指标
if __name__ == "__main__":  
    for date in dates:
        ##get prefetcher name and data
        prefs=[]
        
        data_file_path = 'evaluationmemtense/'+ traces[0] + '/'+'all_results/'
        data_pref = pd.read_csv(data_file_path + date + 'storage.csv', header=None)
        prefs = get_col_data(data_pref,'Prefetcher')
        num_prefs = len(prefs)
        i = 0
        data_all = np.zeros((num_prefs, len(traces)))
        for trace in traces:
            data_file_path='evaluationmemtense/'+ trace + '/'+'all_results/'
            data = pd.read_csv(data_file_path + date + 'storage.csv', header=None)
            data_all[0:num_prefs,i] = get_col_data(data,'IPCI')
            i = i + 1
        

        ## 设置图像保存的路径
        figure_res='analysis_py/evaluation2/speedup_storage/'
        if not os.path.exists(figure_res):
                os.makedirs(figure_res)
        matplotlib.rcParams['hatch.linewidth'] = 0.75  # 设置您想要的线宽
        ###绘制图形
        fig_size = (5, 2.3)
        fig, ax = plt.subplots(figsize=fig_size)

        # 生成每个预取器的条形图
        # max_v, min_v = np.NINF, np.inf
        min_v = 1.48
        max_v = data_all.max().max() + 0.05
        ax_ytick1 = np.arange(1.48,1.68,0.02)
        ax_ytick = np.arange(1.48,1.68,0.04)
        ax_xtick1 = np.arange(0,210,20)
        for j in np.arange(1,num_prefs,1):
            print(prefs[j],data_all[j,0])
            ax.plot(storage[prefs[j]], data_all[j,0], marker=markers[j-1],
                markerfacecolor=markerfacecolors[j-1],markeredgecolor='black',
                markersize=3.5)  # 'o'是绘制点的标记
            ax.text(text_pos[prefs[j]][0], text_pos[prefs[j]][1], Benchs[prefs[j]], fontsize=9, ha='left', va='top')
            
            # if(prefs[j] != 'vberti+bingo_dpc3' and prefs[j] != 'vberti+ppf'):
            #     ax.text(storage[prefs[j]], data_all[j,0], Benchs[prefs[j]], fontsize=9, ha='left', va='top')

        # ##画纵轴的虚线
        ax_idx = 0
        for item in ax_ytick1:
            if(ax_idx % 2 == 0):
                ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=0.5,zorder=1)
            else:
                ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=0.5,zorder=1)
            ax_idx += 1
        ax_idx = 0
        for item in ax_xtick1:
            if(ax_idx % 2 == 0):
                ax.axvline(float(item), color='lightgray', linestyle='-', linewidth=0.5,zorder=1)
            else:
                ax.axvline(float(item), color='lightgray', linestyle='--', linewidth=0.5,zorder=1)
            ax_idx += 1


        # 旋转之后还需要向左平移
        plt.xticks(ax_xtick1, [f'{item:.0f}' for item in ax_xtick1], rotation=0, fontsize=8)
        plt.yticks(ax_ytick, [f'{item:.2f}' for item in ax_ytick], fontsize=8)
        plt.ylim(min_v, max_v)
        plt.xlim(-5, 160)
        # for label in ax.get_yticklabels():
        #     label.set_fontsize(8)
        ax.set_xlabel('Storage Overhead /KB', fontsize=8)
        ax.set_ylabel("SpeedUp", fontsize=8)
        # ax.set_title(f'IPCI', fontsize=8)
        # ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.52*fig_size[1]), ncol=num_prefs-1,fontsize=8,
        # handlelength=1.2,     # 控制图例句柄的长度
        # handletextpad=0.2,  # 控制图例句柄和文本之间的间距
        # columnspacing=0.5   )
        plt.savefig(f'{figure_res}/storage.png',dpi=800, format="png", bbox_inches='tight') 
        plt.savefig(f'{figure_res}/storage.pdf',dpi=800, format="pdf", bbox_inches='tight') 
        plt.close()   

        
