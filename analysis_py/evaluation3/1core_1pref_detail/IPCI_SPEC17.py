import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
import math
from matplotlib.font_manager import FontProperties
# 3.23 1.3
#dates=["1123"]
dates=["0326"]
traces=["spec2k17"]
metrics=['L1D Coverage','L2C Coverage', "LLC Coverage"]
legends={"ipcp_isca2020":"IPCP",
         "mlop_dpc3":"MLOP",
         "vberti":"Berti",
         "hyperion_hpc_2table_UTBh1_buffer8_10":"Hyperion",
         "bingo_dpc3":"Bingo",
         "ppf":'SPP-PPF'}
Benchs={"ipcp_isca2020":"IPCP",
         "mlop_dpc3":"MLOP",
         "vberti":"Berti",
         "hyperion_hpc":"Hyperion",
         "bingo_dpc3":"Bingo",
         "ppf":'SPP-PPF'}
hatches = ['\\\\\\\\\\',   '', '', '', ''] #'xxxxx',
# colors = ['#FEB3AE','#73bad6','#CD5C5C','#0E5378',"#0E5378",'#ef4143','#bd3752','#c4323f']
# colors = ['#FF69B4','#3cb44b','#e6194B','#4363d8']
colors = ['#FF8C9B','#3cb44b','#e6194B','#4363d8']

# colors = ['#a9a9a9','#3cb44b','#CD5C5C','#0E5378',"#0E5378",'#ef4143','#bd3752','#c4323f']

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
        suite = 'spec2k17'
        ##get prefetcher name and data
        prefs=[]
        
        data_file_path = 'evaluationmemtense/'+ f'{traces[0]}' + '/'+'all_results_figs/'
        data_pref = pd.read_csv(data_file_path + date + f'.csv', header=None).T
        num_benchs = data_pref.shape[1]-2
        benchs_name = data_pref.iloc[0,2:].tolist()
        num_prefs = data_pref.iloc[:,1].tolist().count('IPCI')
        prefs = data_pref.iloc[:,0].loc[data_pref.iloc[:,1] == 'IPCI']
        prefs = np.array(prefs)
        print(prefs)
        
        data_all = np.zeros((num_prefs, len(benchs_name)))
        data_file_path = 'evaluationmemtense/'+ f'{traces[0]}' + '/'+'all_results_figs/'
        data = pd.read_csv(data_file_path + date + f'.csv', header=None).T
        i = 0
        print(prefs)
        print(f'all_traces:{len(benchs_name)-1}')
        hyperion_best=0
        hyperion_best_berti = 0
        for bench in benchs_name:                  
            data_all[0:num_prefs,i] = get_col_data(data,'IPCI',bench)
            column_slice = data_all[0:num_prefs, i]
            if (data_all[3,i]>=data_all[2,i]) and (data_all[3,i]>=data_all[1,i]) and (data_all[3,i]>=data_all[0,i]):
                hyperion_best += 1
            else:
                print(data_all[0:num_prefs,i])
            i = i + 1
            # if(column_slice[4] >= column_slice[3]):
            #         hyperion_best_berti += 1
        # for i in range(len(data_all[0,:])):
        #     print(data_all[:,i])
        #     if()
        print(f'hyperion_best:{hyperion_best}')
        print(f'hyperion_best_berti:{hyperion_best_berti}')
            
        min_v = 1.0
        max_v = 3.0
        matplotlib.rcParams['hatch.linewidth'] = 0.50  # 设置您想要的线宽
        fig_size = (7, 1.3)
        fig, ax = plt.subplots(figsize=fig_size)
        plt.tick_params(axis='x', length=1.2)  # 设置 x 轴刻度线长度为 5
        #设置子图间隔
        # 设定条形图的宽度
        bar_width = 1.0 / (num_prefs-1 + 2.0)
        left_bar_pos = np.arange(len(benchs_name))
        ## 设置图像保存的路径
        figure_res='analysis_py/evaluation3/1core_1pref_detail/'
        if not os.path.exists(figure_res):
                os.makedirs(figure_res)
        for i in np.arange(0,num_prefs):

            value = data_all[i,:]
            # value = value.replace('-', 0)
            piece = value.astype(float)
            # max_v = max(piece.max(), max_v)
            # min_v = min(piece.min(), min_v)
            ax.bar(left_bar_pos + bar_width * i, 
                piece, 
                width=bar_width, 
                label=legends[prefs[i]],
                edgecolor='none',  # 边框颜色
                color=colors[i],      # 填充颜色
                # hatch=hatches[i-1],
                linewidth=0.50,zorder=3)
        
            idx_pref = 0
            for item in value:

                if(item >= 3.16):
                    print(item)
                    print(left_bar_pos[len(benchs_name)-1] + bar_width * (len(prefs) -1))
                    print(i)
                    offset = (left_bar_pos[idx_pref]+bar_width*(i+1))/(left_bar_pos[len(benchs_name)-1]+bar_width*num_prefs)
                    pos_x =0.088+offset
                    pos_y1 = 0.823+0.028
                    pos_y2 = 0.88+0.028
                    ax.annotate(
                        f"{item:.2f}", 
                        xy=(pos_x, pos_y1), 
                        xytext=(pos_x-(3-i-1)*0.04, pos_y2),
                        xycoords='figure fraction', 
                        textcoords='figure fraction',
                        fontsize=8,
                        arrowprops=dict(
                            
                            facecolor='black', 
                            shrink=0.01,
                            headlength=1,  # 缩小箭头头部长度
                            headwidth=1.5,   # 缩小箭头头部宽度
                            width=0.005        # 缩小箭头身体宽度
                                # 如果可用，设置箭头与x轴的角度
                        )
                        # ha='center',  # 水平对齐
                        # va='center'  # 垂直对齐
                    )
                idx_pref += 1


        # 计算x轴刻度的位置
        x_ticks = left_bar_pos + bar_width * ((num_prefs - 1) / 2 )
        ax.set_xticks(x_ticks)
        
        benchs_name[len(benchs_name)-1] = 'Geomean'
        none_names = ['' for item in benchs_name]
        ax.set_xticklabels(none_names, fontsize=2,rotation = 90,ha ='right')
        # 为每个位置添加文本
        y_position = 0.80
        for x, label in zip(x_ticks, benchs_name):
            ax.text(x+0.5, y_position, label, fontsize=6, rotation=45, ha='right', va='top')
        # ax.set_xlabel('Benchmarks', fontsize=8)
        ax.set_ylim(min_v, max_v)
        ax.set_xlim(-0.2, num_benchs)
        
        if(max_v < 0.5):
            y_ticks = np.around(np.arange(0, 0.5, 0.1), decimals=1)
            y_ticks1 = np.around(np.arange(0, 0.5, 0.05), decimals=2)
        else:
            y_ticks = np.around(np.arange(0.8, 3.21, 0.4), decimals=1)
            y_ticks1 = np.around(np.arange(0.8, 3.21, 0.2), decimals=1)
        ax_idx = 0
        for item in y_ticks1:
            if(item == 1.0):
                ax.axhline(float(item), color='black', linestyle='-', linewidth=0.8,zorder=1)
            elif(ax_idx % 2 == 0):
                ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=0.33,zorder=1)
            else:
                ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=0.33,zorder=1)
            ax_idx += 1   
        ax.set_yticks(y_ticks)
        ax.set_yticklabels([f'{item}' for item in y_ticks], fontsize=8)

        current_yticks = ax.get_yticks()
        ax.set_yticklabels(current_yticks, fontsize=8)
        # ax.set_ylabel("Normalized performance", fontsize=)
        ax.text(-3.8, 1.5, 'SpeedUp', fontsize=8, rotation=90)

        # ax.set_title(f'IPCI', fontsize=8)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.30), ncol=num_prefs, fontsize=8,
            # y 参数控制标题的位置
            handlelength=1.2,     # 控制图例句柄的长度
            handletextpad=0.2,  # 控制图例句柄和文本之间的间距
            columnspacing=0.5 ,
            # frameon=False,
            edgecolor='none'  )
        # ax.set_title('SPEC', y=-0.55, fontsize=8) 





        plt.savefig(f'{figure_res}/1core_1pref_IPCI_{suite}.png',dpi=800, format="png", bbox_inches='tight') 
        plt.savefig(f'{figure_res}/1core_1pref_IPCI_{suite}.pdf',dpi=800, format="pdf", bbox_inches='tight') 
        plt.savefig(f'{figure_res}/{suite}.eps',dpi=800, format="eps", bbox_inches='tight') 
        plt.close()   

        
