import os
import pandas as pd
import numpy as np
np.set_printoptions(formatter={'float': '{:.7f}'.format})

dates = ['0702','0703']
benchmark='429.mcf-217B'
prefetcher='vberti'
metrics = ['IPCI','L1D Coverage', 'L1D Accuracy', 'L1D Overprediction', 'L1D Prefetches', 'L1D traffic']
file_base_path = 'evaluation/all_results_figs/'


results = [metrics]
print(metrics)
for date in dates:
    data_file_path = os.path.join(file_base_path + date + '.csv')
    data = pd.read_csv(data_file_path, header=None)
    # 获取指标所在的列索引
    idx_col1 = data.iloc[0, :].str.contains(prefetcher)
    idx_col2 = [any(metric in col for metric in metrics) for col in data.iloc[1, :]]
    idx_col = [col1 and col2 for col1, col2 in zip(idx_col1, idx_col2)]
    # 获取特定基准和预取器的数据
    benchmark_data = data[data.iloc[:, 0].str.contains(benchmark)]
    selected_data = benchmark_data.iloc[:,idx_col].values.astype(float)
    results.append(selected_data)
    print(selected_data)

# 打印结果
    # print(results[0])
    # print(results[1])
    # print(results[2])

    