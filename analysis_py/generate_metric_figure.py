import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

#dates=["0924"]
dates=["0924"]
traces=["spec2k17"]
metrics=['IPC','IPCI','L1D LOAD_ACCURACY','L1D MPKI']



def draw_chart_for_metric(data, metric,figure_res):
    font = {
        "family": "Arial",
        "color": "black",
        "weight": "normal",
        "size": 20,
    }

    # 获得标签，并提取相对应的metric的数据
    benchmarks_name = data.iloc[0, 2:].tolist()
    num_benchmarks = data.shape[1] - 2       # remove prefetcher_name and metric name
    prefetcher_range = [0, 1, 2, 3, 4]
    num_prefetchers = len(prefetcher_range)

    metric_data = data[data.iloc[:, 1].str.contains(metric)]
    metric_data = metric_data.iloc[prefetcher_range, :]

    # 创建一个新的图形
    fig, ax = plt.subplots(figsize=(40, 12))
    # 设定条形图的宽度
    bar_width = 1.0 / (num_prefetchers + 0.5)
    left_bar_pos = np.arange(num_benchmarks)

    # 生成每个预取器的条形图
    # max_v, min_v = np.NINF, np.inf
    metric_data_df = metric_data.iloc[:,2:2+num_benchmarks]
    metric_data_df = metric_data_df.replace('-', 0).astype(float)
    max_v = metric_data_df.max().max()
    min_v = metric_data_df.min().min()
    for i in range(num_prefetchers):
        value = metric_data.iloc[i,2:2+num_benchmarks]
        value = value.replace('-', 0)
        piece = value.astype(float)
        if(metric == 'IPCI'):
            piece = piece
        # max_v = max(piece.max(), max_v)
        # min_v = min(piece.min(), min_v)
        ax.bar(left_bar_pos + bar_width * i, 
               piece, 
               width=bar_width, 
               label=metric_data.iloc[i, 0])
        
    # 旋转之后还需要向左平移
    plt.xticks(left_bar_pos + bar_width * 1.5, benchmarks_name, rotation=90, fontsize=10)
    # plt.yticks([-1, -0.5, 0, 0.5, 1], font=font["family"], fontsize=16)
    plt.ylim(min_v, max_v)
    for label in ax.get_yticklabels():
        label.set_fontsize(20)
    ax.set_xlabel('Benchmarks')
    ax.set_title(f'{metric}', fontsize=25)
    ax.legend()
    plt.savefig(f'{figure_res}/{date}/{metric}.png',dpi=300) 
    plt.close()

# 在这里替换为你想要的指标
if __name__ == "__main__":  
    for date in dates:
        for trace in traces:
            data_file_path='evaluationmemtense/'+ trace + '/'+'all_results_figs/'
            figure_res='memtensefigures_res/'+ trace + '/'
            data = pd.read_csv(data_file_path + date + '.csv', header=None).T
            if not os.path.exists(figure_res + date + '/'):
                os.makedirs(figure_res + date + '/')
            for metric in metrics:
                draw_chart_for_metric(data,metric,figure_res)
