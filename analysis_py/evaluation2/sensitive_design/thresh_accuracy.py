import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
import math
from matplotlib.font_manager import FontProperties
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import FuncFormatter, MaxNLocator
import re
# path_ip = "./outputsum/output1024/pickles/607.cactuBSSN_s-4004B_ip.pkl"
# path_page = "./outputsum/output1024/pickles/607.cactuBSSN_s-4004B_page.pkl"
directory = "./evaluationmemtense/spec2k17/all_results/1226.csv"
output_path_base = "analysis_py/evaluation2/sensitive_design/"
if not os.path.exists(output_path_base):
    # 如果目录不存在，则创建该目录
    os.makedirs(output_path_base)

L1_dic = {'0.50':0.5,
            '0.60':0.6,
            '0.70':0.7,
            '0.80':0.8}
L2_dic = {'0.1':0.1,
            '0.2':0.2,
            '0.3':0.3,
            '0.4':0.4,
            '0.5':0.5}

###########读出参数值和加速比
data = pd.read_csv(directory, header=None)
prefs_name = data.loc[:,data.loc[0, :].str.contains('Prefetcher')]
prefs_name = np.array(prefs_name.iloc[:, 0])
prefs_name = prefs_name[2:len(prefs_name)]

speedup = data.loc[:,data.loc[0, :].str.contains('L1D Accuracy')]
speedup = np.array(speedup.iloc[:, 0])
speedup = speedup[2:len(speedup)]
speedup = [float(item) for item in speedup]
print(speedup[0])
########绘图，将数据加入小方格
fig, [ax1,ax2] = plt.subplots(1,2,figsize=(6.46, 1.5))
plt.subplots_adjust(left=0, right=1.0, bottom=0, top=1.0, wspace=0.25, hspace=0.45)

i = 0
for pref in prefs_name:
    pattern = r"\d+\.\d+"
    matches = re.findall(pattern, pref)
    threshs = []
    if matches:
        for thresh in matches:
            threshs.append(thresh)
    # print(threshs)
    if(threshs[2] == '0.70' and threshs[3] == '0.1'):
        if(L1_dic[threshs[0]] > L2_dic[threshs[1]]):
            rect = patches.Rectangle((L1_dic[threshs[0]], L2_dic[threshs[1]]), 0.1, 0.1,  # 此处假定每个方块的宽度和高度都是1
                                    linewidth=1,
                                    edgecolor='white',
                                    facecolor=plt.cm.gray_r((speedup[i]-0.80)*10))
            ax1.add_patch(rect)
            ax1.text(L1_dic[threshs[0]] + 0.05,  # x坐标
                        L2_dic[threshs[1]] + 0.05,  # y坐标
                        str(f"{speedup[i]:.3f}"),  # 要添加的文本
                        color='white',  # 文本颜色
                        ha='center',  # 水平居中
                        va='center')  # 垂直居中
    if(threshs[0] == '0.70' and threshs[1] == '0.1'):
        if(L1_dic[threshs[2]] > L2_dic[threshs[3]]):
            rect = patches.Rectangle((L1_dic[threshs[2]], L2_dic[threshs[3]]), 0.1, 0.1,  # 此处假定每个方块的宽度和高度都是1
                                    linewidth=1,
                                    edgecolor='white',
                                    facecolor=plt.cm.gray_r((speedup[i]-0.80)*10))
            ax2.add_patch(rect)
            ax2.text(L1_dic[threshs[2]] + 0.05,  # x坐标
                        L2_dic[threshs[3]] + 0.05,  # y坐标
                        str(f"{speedup[i]:.3f}"),  # 要添加的文本
                        color='white',  # 文本颜色
                        ha='center',  # 水平居中
                        va='center')  # 垂直居中
    i = i + 1

# 设置x轴和y轴的范围
x_tick_labels = ['0.5','0.6','0.7','0.8']
y_tick_labels = ['0.1','0.2','0.3','0.4','0.5']


ax1.set_xlim(0.5, 0.90)  # 假设你想让x轴的范围从0到数据长度
ax1.set_ylim(0.1, 0.60)  # 可以根据需要调整y轴的范围

ax1.set_xticks(np.arange(0.5, 0.85, 0.1)+0.05)  
ax1.set_yticks(np.arange(0.1, 0.55, 0.1)+0.05)
# ax1.set_xticklabels(x_tick_labels_ip,fontsize=9,rotation=45,ha='right')
ax1.set_xticklabels(x_tick_labels,fontsize = 9)
ax1.set_yticklabels(y_tick_labels,fontsize=9)

ax2.set_xlim(0.5, 0.90)  # 假设你想让x轴的范围从0到数据长度
ax2.set_ylim(0.1, 0.60)  # 可以根据需要调整y轴的范围

ax2.set_xticks(np.arange(0.5, 0.85, 0.1)+0.05)  
ax2.set_yticks(np.arange(0.1, 0.55, 0.1)+0.05)
# ax1.set_xticklabels(x_tick_labels_ip,fontsize=9,rotation=45,ha='right')
ax2.set_xticklabels(x_tick_labels,fontsize = 9)
ax2.set_yticklabels(y_tick_labels,fontsize=9)
# for i, label in enumerate(x_tick_labels_ip):
#     ax1.text(i-0.2, -0.02, label, rotation=45,ha='center', va='top', transform=ax1.get_xaxis_transform())

# 设置坐标轴标签
# 设置坐标轴标签
ax1.set_xlabel('L1D threshold',fontsize=9)
ax1.set_ylabel('L2 threshold',fontsize=9)
# ax1.set_title('(a) Thresholds of Page',va='bottom')
ax2.set_xlabel('L1D threshold',fontsize=9)
ax2.set_ylabel('L2 threshold',fontsize=9)

ax1.text(0.5, -0.30, 'Thresholds for pages', transform=ax1.transAxes, fontsize=9,  va='top', ha='center')
ax2.text(0.5, -0.30, 'Thresholds for PCs', transform=ax2.transAxes, fontsize=9, va='top', ha='center')
# ax2.set_title('(b) Thresholds of PC')

# ax1.xaxis.set_label_coords(1.1, -0.04)  # 将x轴标签移到轴的末端
# ax1.yaxis.set_label_coords(-0.05, 1.05)  # 将y轴标签移到轴的顶部

# ax1.text(0.5, -0.12, '(a)', transform=ax1.transAxes, fontsize=24, fontweight='bold', va='top', ha='center')

# 显示图像

# 设置颜色条
# 创建一个ScalarMappable并初始化与图中用到的归一化对象和颜色映射
cmap = LinearSegmentedColormap.from_list('custom_gray', ['#f0f0f0', '#101010'], N=256)
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
norm = Normalize(vmin=0.80, vmax=0.90)
sm = ScalarMappable(cmap=plt.cm.gray_r, norm=norm)
sm.set_array([])  # 只是为了满足函数需求
cbar = plt.colorbar(sm, ax=[ax1,ax2],pad=0.02)
cbar.outline.set_edgecolor('none')
def format_func(x, pos):
    return '{:.2f}'.format(x)
cbar.ax.yaxis.set_major_formatter(FuncFormatter(format_func))
cbar.ax.yaxis.set_major_locator(MaxNLocator(nbins=5)) 
# cbar.set_label('Accesses ratio with same $Q_{IP}$(a) and $Q_{Page}$(b) ',fontsize=30)
plt.show()
plt.savefig(os.path.join(output_path_base,'thresh_accuracy.png'),dpi=800, format="png", bbox_inches='tight')
plt.savefig(os.path.join(output_path_base,'thresh_accuracy.pdf'),dpi=800, format="pdf", bbox_inches='tight')