import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

#dates=["0826"]
dates=["0826"]
traces=["spec2k17"]
# metrics=['IPC','IPCI','L1D LOAD_ACCURACY','L1D MPKI']
metrics=['IPC','IPCI']



def print_for_metric(data, metric):
    print('\n')
    print(f"{metric}\n")
    # 获得标签，并提取相对应的metric的数据
    benchmarks_name = data.iloc[0, 2:].tolist()
    num_benchmarks = data.shape[1] - 2       # remove prefetcher_name and metric name
    prefetcher_range = [0, 1, 2, 3, 4]
    # prefecher_range =[],0代表ip_stride,1代表ipcp, 2代表dpc3_mlop,3代表vberti，4代表vbertim
    num_prefetchers = len(prefetcher_range)

    metric_data = data[data.iloc[:, 1].str.contains(metric)]
    metric_data = metric_data.iloc[prefetcher_range, :]


    metric_data_df = metric_data.iloc[:,2:2+num_benchmarks]
    metric_data_df = metric_data_df.replace('-', 0).astype(float)

    vberti_value = metric_data.iloc[3,2:2+num_benchmarks]
    vberti_value = vberti_value.replace('-', 0)
    vberti_value = vberti_value.astype(float)
    vbertim_value = metric_data.iloc[4,2:2+num_benchmarks]
    vbertim_value = vbertim_value.replace('-', 0)
    vbertim_value = vbertim_value.astype(float)
    
    for i in range(len(vberti_value)):
        # print(f"{benchmarks_name[i]} {vberti_value[i]} {vbertim_value[i]} \n")    
        if(benchmarks_name[i]=="Average"):
            improve = (vbertim_value[i+2].astype(float) - vberti_value[i+2].astype(float))/vberti_value[i+2].astype(float)*100
            print(f"{dates} {traces} {metric} {benchmarks_name[i]} vberti:{vberti_value[i+2]} vbertim:{vbertim_value[i+2]} improve:{improve}%\n")
        else:
            print(f"{dates} {traces} {metric} {benchmarks_name[i]} vberti:{vberti_value[i+2]} vbertim:{vbertim_value[i+2]}\n")


# 在这里替换为你想要的指标
if __name__ == "__main__":  
    for date in dates:
        for trace in traces:
            data_file_path='evaluationmemtense/'+ trace + '/'+'all_results_figs/'
            data = pd.read_csv(data_file_path + date + '.csv', header=None).T
            for metric in metrics:
                print_for_metric(data,metric)
