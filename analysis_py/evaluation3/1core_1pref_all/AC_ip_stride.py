import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
import math
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Patch
import matplotlib.gridspec as gridspec
# 3.23 1.3
#dates=["1123"]
dates=["0326"]
traces=["spec2k06" ,"spec2k17","gap","parsec","4suites"]
dic_suite={
    'spec2k06':'SPEC06',
    'spec2k17':'SPEC17',
    'gap':"GAP",
    'parsec':'PARSEC',
    '4suites':"Geomean"
}
dic_suite1={
    'spec2k06':'SPEC06',
    'spec2k17':'SPEC17',
    'gap':"GAP",
    'parsec':'PARSEC',
    '4suites':"Average"
}
dic_suite2={
    'spec2k06':'SPEC06',
    'spec2k17':'SPEC17',
    'gap':"GAP",
    'parsec':'PARSEC',
    '4suites':"Geomean/Average"
}
metrics=['L1D Accuracy','L2C Accuracy','L1D Coverage','L2C Coverage','LLC Coverage']
legends={"no":"no",
        "ipcp_isca2020":"IPCP",
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
# hatches = ['\\\\\\\\\\',   '', '', '', ''] #'xxxxx',
fontsizes=7
colors = ['#FEB3AE','#73bad6','#CD5C5C','#0E5378',"#0E5378",'#ef4143','#bd3752','#c4323f']
y_min = 0.0
y_max = 1.00
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
        

        fig_size = (6.69, 1.5)
        fig= plt.figure(figsize=fig_size, dpi=600)
        gs = gridspec.GridSpec(2,4,width_ratios=[1,0.1, 1, 1],figure=fig)
        ax1 = fig.add_subplot(gs[0, 2:3])
        ax2 = fig.add_subplot(gs[0, 3:4])
        ax3 = fig.add_subplot(gs[1, 2:3])
        ax4 = fig.add_subplot(gs[1, 3:4])
        ax = fig.add_subplot(gs[0:1, 0])
        ax5 = fig.add_subplot(gs[1:2, 0])

        axs = ax1
        #设置子图间隔
        plt.subplots_adjust(left=0, right=1.0, bottom=0, top=1.0, wspace=0.02, hspace=0.04)
        # 设定条形图的宽度
        bar_width = 1.0 / (num_prefs+2.0)
        left_bar_pos = np.arange(len(traces))
        ## 设置图像保存的路径
        figure_res='analysis_py/evaluation3/1core_1pref_all/'
        if not os.path.exists(figure_res):
                os.makedirs(figure_res)
        
        data_all = np.zeros((num_prefs, len(traces)))
        
        trace_idx = 0
        for trace in traces:
            data_file_path='evaluationmemtense/'+ trace + '/'+'all_results/'
            data = pd.read_csv(data_file_path + date + '.csv', header=None)
            data_IPCI = np.zeros((num_prefs, 1))     
            data_IPCI[0:num_prefs,0] = get_col_data(data,'IPCI')
            data_all[0:num_prefs,trace_idx] = data_IPCI[0:num_prefs,0]
            trace_idx = trace_idx + 1

        matplotlib.rcParams['hatch.linewidth'] = 0.75  # 设置您想要的线宽
        #设置子图间隔
        # 设定条形图的宽度
        bar_width = 1.0 / (num_prefs + 2.0)
        left_bar_pos = np.arange(len(traces))
        legend_patch = []   
        for i in range(num_prefs):
            ax.bar(left_bar_pos + bar_width * i, 
                data_all[i,0:len(traces)], 
                width=bar_width, 
                edgecolor='none',  # 边框颜色
                color=colors[i],      # 填充颜色
                linewidth=0.75,zorder=3)
            
            # legend_patch.append(Patch(facecolor=colors[i], edgecolor='none',label=legends[prefs[i]]))



            # 计算x轴刻度的位置
        # x_ticks = left_bar_pos + bar_width * ((num_prefs)/2-0.5)
        # ax.set_xticks(x_ticks)
        # ax.set_xticklabels([])
        ax.set_xticks([])
        ax.set_xticklabels([])
        y_pos = 0.97
        # for x, label in zip(x_ticks, [dic_suite[trace] for trace in traces]):
        #         if(x == x_ticks[3]):
        #             ax.text(x-0.15,y_pos,label,fontsize=fontsizes,ha='center',va='top')
        #         else:
        #             ax.text(x,y_pos,label,fontsize=fontsizes,ha='center',va='top')
        # ax.set_xticklabels([dic_suite[trace] for trace in traces], fontsize=fontsizes)
        # axes[ay].set_xlabel('Benchmarks', fontsize=9)
        
        y_ticks=np.around(np.arange(0.9, 1.401, 0.05), decimals=2)
        y_ticks1=np.around(np.arange(0.9, 1.401, 0.10), decimals=1)

        ax.set_ylim(0.9, 1.401)
        ax_idx = 0
        for item in y_ticks:
            if(ax_idx % 2 == 0):
                ax.axhline(float(item), color='lightgray', linestyle='-', linewidth=0.5,zorder=1)
            else:
                ax.axhline(float(item), color='lightgray', linestyle='--', linewidth=0.5,zorder=1)
            ax_idx += 1   
        ax.set_yticks(y_ticks1)
        ax.set_yticklabels([f'{item}' for item in y_ticks1], fontsize=fontsizes)
        ax.set_title('(a) SpeedUp', y=0.75, fontsize=fontsizes+1) 

            # ax.set_ylabel("SpeedUp", fontsize=fontsizes)


        metric_idx = 0
        for metric in metrics:
            if(metric_idx == 0):
                axs = ax1
            elif(metric_idx == 1):
                axs = ax2
            elif(metric_idx == 2):
                axs = ax3
            elif(metric_idx == 3):
                axs = ax4
            else:
                axs = ax5
            ax = int(metric_idx / 2)
            if(metric_idx == 4):
                ax = metric_idx
            ay = metric_idx % 2
            metric_idx = metric_idx + 1
            data_all = np.zeros((num_prefs, len(traces)))
            trace_idx = 0
            for trace in traces:
                data_file_path='evaluationmemtense/'+ trace + '/'+'all_results/'
                data = pd.read_csv(data_file_path + date + '.csv', header=None)
                data_IPCI = np.zeros((num_prefs, 1))     
                data_IPCI[0:num_prefs,0] = get_col_data(data,metric)
                data_all[0:num_prefs,trace_idx] = data_IPCI[0:num_prefs,0]
                trace_idx = trace_idx + 1

            legend_patch = []  
            for i in range(num_prefs):
                legend_patch.append(Patch(facecolor=colors[i], edgecolor='none',label=legends[prefs[i]]))
                if(axs == ax1):
                    axs.legend(handles=legend_patch,loc='upper center', bbox_to_anchor=(0.5, 1.32), ncol=4, fontsize=fontsizes+1,
                    # y 参数控制标题的位置
                    handlelength=1.2,     # 控制图例句柄的长度
                    handletextpad=0.2,  # 控制图例句柄和文本之间的间距
                    columnspacing=1.0,
                    frameon=False,
                    edgecolor='none'   )
             
            for i in range(num_prefs):
                axs.bar(left_bar_pos + bar_width * i, 
                    data_all[i,0:len(traces)], 
                    width=bar_width, 
                    edgecolor='none',  # 边框颜色
                    color=colors[i],      # 填充颜色
                    linewidth=0.75,zorder=3)



            # 计算x轴刻度的位置
            x_ticks = left_bar_pos + bar_width * ((num_prefs)/2-0.5)
            if(ax == 1):
                axs.set_xticks(x_ticks)
                # axes[ax][ay].set_xticklabels([dic_suite[trace] for trace in traces], fontsize=fontsizes,rotation=0)
                axs.set_xticklabels([])
                y_pos = -0.30
                for x, label in zip(x_ticks, [dic_suite1[trace] for trace in traces]):
                    if(x == x_ticks[3]):
                        axs.text(x-0.1,y_pos,label,fontsize=fontsizes,ha='center',va='top')
                    else:
                        axs.text(x,y_pos,label,fontsize=fontsizes,ha='center',va='top')
            elif(ax == 4):
                axs.set_xticks(x_ticks)
                # axes[ax][ay].set_xticklabels([dic_suite[trace] for trace in traces], fontsize=fontsizes,rotation=0)
                axs.set_xticklabels([])
                y_pos = -0.30
                for x, label in zip(x_ticks, [dic_suite2[trace] for trace in traces]):
                    if(x == x_ticks[3]):
                        axs.text(x-0.1,y_pos,label,fontsize=fontsizes,ha='center',va='top')
                    elif(x == x_ticks[4]):
                        axs.text(x+0.25,y_pos,'Geo(a)/Ave(d)',fontsize=fontsizes,ha='center',va='top')
                        # axs.text(x,y_pos,'Average',fontsize=fontsizes,ha='center',va='top')
                    else:
                        axs.text(x,y_pos,label,fontsize=fontsizes,ha='center',va='top')
           
            else:
                axs.set_xticks([])
                axs.set_xticklabels([])
            # axes[ay].set_xlabel('Benchmarks', fontsize=9)
           
            y_ticks=np.around(np.arange(y_min, y_max+0.01, 0.1), decimals=3)
            y_ticks1=np.around(np.arange(y_min, y_max+0.01, 0.2), decimals=2)
            
            y_min1 = -0.2
            y_max1 = 0.8
            y_ticks2=np.around(np.arange(y_min1, y_max1+0.01, 0.1), decimals=3)
            y_tickss2=np.around(np.arange(y_min1, y_max1+0.01, 0.2), decimals=2)

            ax_idx = 0
            if(metric_idx <= 2):
                for item in y_ticks:
                    if(ax_idx % 2 == 0):
                        axs.axhline(float(item), color='lightgray', linestyle='-', linewidth=0.5,zorder=1)
                    else:
                        axs.axhline(float(item), color='lightgray', linestyle='--', linewidth=0.5,zorder=1)
                    ax_idx += 1
            else:
                for item in y_ticks2:
                    if(ax_idx % 2 == 0):
                        axs.axhline(float(item), color='lightgray', linestyle='-', linewidth=0.5,zorder=1)
                    else:
                        axs.axhline(float(item), color='lightgray', linestyle='--', linewidth=0.5,zorder=1)
                    ax_idx += 1
            
            if(ay == 0 and metric_idx <= 2):
                axs.set_yticks(y_ticks1)
                axs.set_yticklabels([f'{item}' for item in y_ticks1], fontsize=fontsizes)
                axs.set_ylim(y_min, y_max+0.15)
            elif(ay != 0 and metric_idx <= 2):
                axs.set_yticks([])
                axs.set_yticklabels([]) 
                axs.set_ylim(y_min, y_max+0.15)
            elif(ay == 0 and metric_idx > 2):
                axs.set_yticks(y_tickss2)
                axs.set_yticklabels([f'{item}' for item in y_tickss2], fontsize=fontsizes)
                axs.set_ylim(y_min1, y_max1+0.15)
            elif(ay != 0 and metric_idx > 2):
                axs.set_yticks([])
                axs.set_yticklabels([]) 
                axs.set_ylim(y_min1, y_max1+0.15)

            # ax.set_ylabel("SpeedUp", fontsize=fontsizes)
            if(metric == 'L1D Accuracy'):
                axs.set_title('(b) L1D Accuracy', y=0.75, fontsize=fontsizes+1) 
            elif(metric == 'L1D Coverage'):
                axs.set_title('(e) L1D Coverage', y=0.74, fontsize=fontsizes+1) 
            elif(metric == 'L2C Accuracy'):
                axs.set_title('(c) L2C Accuracy', y=0.74, fontsize=fontsizes+1) 
            elif(metric == 'L2C Coverage'):
                axs.set_title('(f) L2C Coverage', y=0.74, fontsize=fontsizes+1) 
            elif(metric == 'LLC Coverage'):
                axs.set_title('(d) LLC Coverage', y=0.74, fontsize=fontsizes+1) 
            
            

        plt.savefig(f'{figure_res}/L1D_AC.png',dpi=800, format="png", bbox_inches='tight') 
        plt.savefig(f'{figure_res}/L1D_AC.pdf',dpi=800, format="pdf", bbox_inches='tight') 
        plt.close()   

        
