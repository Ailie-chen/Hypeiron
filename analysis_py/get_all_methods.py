import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 定义路径和参数
base_path = 'evaluationmemtense/'
save_path = 'memtensefigures_res/all_methods_compare/spec2k17/'
if not os.path.exists(save_path):
 # 如果目录不存在，则创建该目录
    os.makedirs(save_path)
traces = ['spec2k17']
dates = ['0703','0966','0967']
#dates = ['0703','0704',]
#metrics = ['IPC','IPCI','L1D Accuracy','L1D Coverage']
metrics = ['IPC','IPCI','L1D LOAD_ACCURACY','L1D MPKI','L1D Overprediction','L1D traffic']
dic = dict([ ('vberti', 'IP'),
        ('0703', 'IP+pages'),
        ('0704', 'IP+pages+bingo_bop(16)'),
        ('0705', 'IP+bingo_bop(16)'),
        ('0706', 'IP+pages+bingo_bop(32)'),
        ('0707', 'IP+bingo_bop(32)'),
        ('0708', 'IP+pages+cp_bingo_bop(32)'),
        ('0709', 'cp_bingo_bop(32)'),
        ('0710', 'bingo_bop(32)'),
        ('0713', 'IP+pages+bingo_bop(32)'),
        ('0816', 'IP+Bingo'),
        ('0817', 'IP+Bingo+Bop'),
        ('0822', 'Bingo'),
        ('0821', 'Berti+nextline'),
        ('0825', 'Berti_PP'),
        ('0826', 'Berti_pp+Berti'),
        ('0828', 'Berti_pp+nextline+Berti'),
        ('0830', 'Berti_pp+nextline+Berti(32)'),
        ('0831', 'Berti_pp+nextline+Berti+Bop(32)'),
        ('0901', 'Berti_pp+nextline+Berti(mix)'),
        ('0903', 'Berti_pp+berti_ip+bop'),
        ('0904', 'Berti_pp+nextline+berti_ip+bop'),
        ('0908', 'Berti_pp(lose_page)'),
        ('0909', 'Berti_pp(lose_ip)'),
        ('0913', 'Berti_pp+berti_ip+bop(2)'),
        ('0914', 'nextline'),
        ('0916', 'Berti_pp+nextline+bingo'),
        ('0919', 'Berti_ip+bingo+berti_pp'),
        ('0920', 'Berti_ip+bingo+berti_pp+nextline'),
        ('0924', 'Bingo_delta(1)'),
        ('0935', 'PMP'),
        ('0936', 'Berti_pp+nextline+Berti'),
        ('0930', 'PMP(Best)'),
        ('0952', 'berti_ip+bingo'),
        ('0967', 'berti_ip+berti_PP'),
        ('0966', 'berti_ip+berti_ip+global_page_delta')

])

# 遍历所有的trace和日期
for trace in traces:
    data = {}
    for date in dates:
        # 读取数据
        file_path = os.path.join(base_path, trace, 'all_results_figs', date + '.csv')
        df = pd.read_csv(file_path, header=None)
        if date == '0966':
            benchmarks_name = df.iloc[2:, 0].tolist() 
            num_benchmarks = len(benchmarks_name)      # remove prefetcher_name and metric name
        # 如果日期是'0703'，还需要提取vberti的metrics数据
        # if date == '0703':
        #     for metric in metrics:
        #         for column in df.columns:
        #             if 'vberti' == df[column].iloc[0] and metric == df[column].iloc[1]:
        #                 data[('vberti', metric)] = df[column].iloc[2:].values

        # 提取vbertim的metrics数据
        for metric in metrics:
            for column in df.columns:             
                if 'vbertim' == df[column].iloc[0] and metric == df[column].iloc[1]:
                    data[(date, metric)] = df[column].iloc[2:].values



          

    # 绘制图形
    for metric in metrics:
        
        fig, ax = plt.subplots(figsize=(40, 12))
        bar_width = 2.0 / (len(dates)+1.5)
        bar_pos = np.arange(num_benchmarks)*2.0

        # max_v = max(df.max() for df in data.values())
        # min_v = min(df.min() for df in data.values())

        k = 0
        for idx, key in enumerate(data.keys()):
            if key[1]== metric:
                values = data[key]
                for i in range(len(values)):
                    if values[i] == '-':
                        values[i] = 0
                values = values.astype(float)
                ax.bar(bar_pos + bar_width * k, values, width=bar_width, label=dic[key[0]])
                #ax.bar(bar_pos + bar_width * k, values, width=bar_width, label=key[0])
                k = k + 1
        plt.subplots_adjust(bottom=0.2)
        plt.xticks(bar_pos + bar_width * len(dates)/2, benchmarks_name, rotation=45, fontsize=15, ha='right')
        #plt.ylim(min_v,max_v)
        ax.set_xlabel('Trace')
        ax.set_title(f'{metric}', fontsize=25)
        ax.legend()

        # 保存图像
        plt.savefig(os.path.join(save_path, f'{metric}.png'),dpi=300)

        # 关闭图像
        plt.close()