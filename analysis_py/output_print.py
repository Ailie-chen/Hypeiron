import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

#dates=["0315"]
dates=["0315"]
traces=["spec","spec2k06","spec2k17","ligra","gap"]

# metrics=['IPC','IPCI','L1D LOAD_ACCURACY','L1D MPKI']
metrics=['Prefetcher','IPCI', "L1D Accuracy"]
# ,"L2C Accuracy","L2C MPKI","L1D Coverage"]
# metrics=['Prefetcher','IPCI','Global Coverage',"L1D Coverage", "L1D Accuracy","L2C Accuracy",]


def print_for_metric(data,trace):
    # 获得标签，并提取相对应的metric的数据
    num_prefs = data.shape[0]-1
    prefetcher_range=np.arange(1,data.shape[0])
    metric_data = pd.DataFrame(index=prefetcher_range, columns=metrics)
    for row_idx in prefetcher_range:
        if(trace == '4suites'):
            for metric in metrics + ['L1D MPKI', 'L2C MPKI', 'LLC MPKI']:
                metric_data_idx = data.iloc[0, :] == metric
                # Extract and assign the metric data for the current row and metric
                metric_data.at[row_idx, metric] = data.loc[row_idx, metric_data_idx].values
        else:
            for metric in metrics:
                metric_data_idx = data.iloc[0, :] == metric
                # Extract and assign the metric data for the current row and metric
                metric_data.at[row_idx, metric] = data.loc[row_idx, metric_data_idx].values

    # Print the final organized metric data
    print(metric_data)



# 在这里替换为你想要的指标
if __name__ == "__main__":  
    for date in dates:
        for trace in traces:
            print(trace)
            data_file_path='evaluationmemtense/'+ trace + '/'+'all_results/'
            data = pd.read_csv(data_file_path + date + '.csv', header=None)
            print_for_metric(data,trace)
