
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter
import csv
import os

# 计算两个数组的和
data_file_path_NIR='outputsum/output1028/statistic/1028_NIR.csv'
data_file_path_NCSR='outputsum/output1028/statistic/1028_NCSR.csv'
figure_res='outputsum/output1028/statistic/'
data_NIR = pd.read_csv(data_file_path_NIR, header=None).T
benchmarks_name_NIR = data_NIR.iloc[0,1:].tolist()
benchmarks_name_NIR.append('Average')
NIR = data_NIR.iloc[1,1:]
NIR = NIR.astype(float)
NIR = NIR.append(pd.Series(NIR.mean()), ignore_index=True)
non_zero_indices = [i for i, x in enumerate(NIR) if x != 0]
NIR = [NIR[i] for i in non_zero_indices]
benchmarks_name_NIR = [benchmarks_name_NIR[i] for i in non_zero_indices]

data_NCSR = pd.read_csv(data_file_path_NCSR, header=None).T
benchmarks_name_NCSR = data_NCSR.iloc[0,1:].tolist()
benchmarks_name_NCSR.append('Average')
NCSR = data_NCSR.iloc[1,1:]
NCSR = NCSR.astype(float)
NCSR = NCSR.append(pd.Series(NCSR.mean()), ignore_index=True)
non_zero_indices = [i for i, x in enumerate(NCSR) if x != 0]
NCSR = [NCSR[i] for i in non_zero_indices]
benchmarks_name_NCSR = [benchmarks_name_NCSR[i] for i in non_zero_indices]

fig, (ax1,ax2) = plt.subplots(2,1,figsize=(32,30),gridspec_kw={'hspace': 0.36})
bar_width = 1.0 / (1 + 0.5)
left_bar_pos_NIR = np.arange(len(benchmarks_name_NIR))
ax1.bar(left_bar_pos_NIR + bar_width * 0, NIR, color ="black",width= bar_width, label = 'NIR',facecolor="grey")
ax1.set_xticks(left_bar_pos_NIR + bar_width * 0.5)  # 设置x轴刻度位置在条形图的中间
ax1.set_xticklabels(benchmarks_name_NIR, rotation=45, fontsize=22, fontweight='bold', ha='right')
for label in ax1.get_yticklabels():
    label.set_fontsize(23)
ax1.text(0.5, -0.32, '(a).NIR', transform=ax1.transAxes, fontsize=24, fontweight='bold', va='bottom', ha='center')


left_bar_pos_NCSR = np.arange(len(benchmarks_name_NCSR))
ax2.bar(left_bar_pos_NCSR + bar_width * 0, NCSR, color ="black",width= bar_width, label = 'NCSR',facecolor="grey")
ax2.set_xticks(left_bar_pos_NCSR + bar_width * 0.5)  # 设置x轴刻度位置在条形图的中间
ax2.set_xticklabels(benchmarks_name_NCSR, rotation=45, fontsize=22,fontweight='bold', ha='right')
for label in ax2.get_yticklabels():
    label.set_fontsize(23)
ax2.text(0.5, -0.36, '(b).NCSR', transform=ax2.transAxes, fontsize=24, fontweight='bold', va='bottom', ha='center')


plt.savefig(os.path.join(figure_res,'berti_NIR_NIR.png'),dpi=600, format="png", bbox_inches='tight')
plt.savefig(os.path.join(figure_res,'berti_NIR_NCSR.pdf'),dpi=600, format="pdf", bbox_inches='tight')

