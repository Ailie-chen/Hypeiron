import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
from matplotlib.patches import Patch
# 3.23 1.3
#dates=["1123"]
dates=["0326"]
metrics=["IPCI"]
traces=["spec2k06_4core" ,"spec2k17_4core","gap4core","parsec4core","homo","hete","4core_all"]
dic_suite={
    'spec2k06_4core':'SPEC06',
    'spec2k17_4core':'SPEC17',
    'gap4core':"GAP",
    'parsec4core':'PARSEC',
    'homo':"Homo",
    'hete':"Heter",
    "4core_all":"Geomean"
}
fontsizes=7
legends={"ipcp_isca2020":"IPCP",
         "mlop_dpc3":"MLOP",
         "vberti":"Berti",
         "hyperion_hpc_2table_UTBh1_buffer9_2":"Hyperion",
         "bingo_dpc3":"Bingo",
         "ppf":'SPP-PPF'}

hatches = ['//////','','\\\\\\\\\\', '//////','','\\\\\\\\\\',  '', '...','\\\\\\\\\\'] #'xxxxx',
colors = ['#FEB3AE','#73bad6','#CD5C5C','#0E5378',"#0E5378",'#ef4143','#bd3752','#c4323f']

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
        fig_size = (3.2, 0.75)
        fig, ax = plt.subplots(figsize=fig_size)
        #设置子图间隔
        # 设定条形图的宽度
        bar_width = 1.0 / (num_prefs + 2.0)
        left_bar_pos = np.arange(len(traces))
        print(left_bar_pos)
        ## 设置图像保存的路径
        figure_res='analysis_py/evaluation3/4core/'
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
            ax.set_xticklabels(['' for trace in traces], fontsize=fontsizes)

        for x, label in zip(x_ticks, [dic_suite[trace] for trace in traces]):
            if(x == x_ticks[0]):
                ax.text(x-0.7, 0.50, label, fontsize=fontsizes, rotation=0)
            elif(x == x_ticks[2]):
                ax.text(x-0.3, 0.50, label, fontsize=fontsizes, rotation=0)
            elif(x == x_ticks[3]):
                ax.text(x-0.6, 0.50, label, fontsize=fontsizes, rotation=0)
            elif(x == x_ticks[4]):
                ax.text(x-0.4, 0.50, label, fontsize=fontsizes, rotation=0)
            elif(x == x_ticks[5]):
                ax.text(x-0.4, 0.50, label, fontsize=fontsizes, rotation=0)
            else:
                ax.text(x-0.5, 0.50, label, fontsize=fontsizes, rotation=0)
            # axes[ay].set_xlabel('Benchmarks', fontsize=9)
            # axes[ay].set_xlabel('Benchmarks', fontsize=9)
           
            y_ticks=np.around(np.arange(0.8, 1.801, 0.1), decimals=1)
            y_ticks1=np.around(np.arange(0.8, 1.801, 0.2), decimals=1)

            ax.set_ylim(0.8, 1.8)
            ax_idx = 0
            for item in y_ticks:
                if(ax_idx % 2 == 0):
                    ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=0.2,zorder=1)
                else:
                    ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=0.2,zorder=1)
                ax_idx += 1   
            ax.axhline(float(1.0), color='#000000', linestyle='-', linewidth=0.4,zorder=1)
            ax.set_yticks(y_ticks1)
            ax.set_yticklabels([f'{item}' for item in y_ticks1], fontsize=fontsizes)

            ax.set_ylabel("SpeedUp", fontsize=fontsizes)
            ax.legend(handles=legend_patch,loc='upper center', bbox_to_anchor=(0.5, 1.40), ncol=4, fontsize=fontsizes,
             # y 参数控制标题的位置
        handlelength=1.2,     # 控制图例句柄的长度
        handletextpad=0.2,  # 控制图例句柄和文本之间的间距
        columnspacing=0.5,
        edgecolor='none'   )
            # ax.set_title(dic_suite[trace], y=-0.28, fontsize=9) 

        plt.savefig(f'{figure_res}/4core.png',dpi=800, format="png", bbox_inches='tight') 
        plt.savefig(f'{figure_res}/4core.pdf',dpi=800, format="pdf", bbox_inches='tight') 
        plt.savefig(f'{figure_res}/4core.eps',dpi=800, format="eps", bbox_inches='tight')
        plt.close()   

        
