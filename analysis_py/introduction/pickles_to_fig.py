import pickle 
from collections import Counter
import os
import glob
import multiprocessing
import re
from scipy.interpolate import interp1d
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import FuncFormatter, MaxNLocator
# path_ip = "./outputsum/output1024/pickles/607.cactuBSSN_s-4004B_ip.pkl"
# path_page = "./outputsum/output1024/pickles/607.cactuBSSN_s-4004B_page.pkl"
directory = "./outputsum/output1158/scatter_pickles/"
output_path_base = "analysis_py/introduction/RD_fig/"
if not os.path.exists(output_path_base):
    # 如果目录不存在，则创建该目录
    os.makedirs(output_path_base)
result_name = '403.gcc-17B_'
path_ip = os.path.join(directory,"scatter.pkl")
filename=''
rdip=[]
rdpage_of_ip=[[]]


with open(path_ip, 'rb') as f:
    data_pack= pickle.load(f)
    for item in data_pack:
        filename,rdip,rdpage_of_ip = item
f.close()
array_len=len(rdip)
rdip=[(item*(array_len-1)) for item in rdip]
rdip.append(0)
print(rdip)
print(rdpage_of_ip)
##########画图################
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
from matplotlib.colors import LinearSegmentedColormap
# 设置y轴的自定义刻度
# 1-7是一个刻度，然后每100一个刻度直到1000，然后是>1000
# y_tick_labels_ip = ['1']+['7'] + [f"{i}" for i in range(100, 901, 100)] + ['>=1000']+['']
# y_tick_labels_page = ['1']+['7'] + [f"{i}" for i in range(10, 51, 5)] + ['>=55']+['']

x_tick_labels_ip =  ['']+[f"{i}" for i in range(200, 2000, 200)] + ['>=2k']+['']
# x_tick_labels_ip =  ['']+['0.2k']+['0.4k']+['0.6k']+['0.8k']+['1k']+['1.2k']+['1.4k']+['1.6k']+['1.8k'] + ['>=2k']
y_tick_labels_page = [f"{i}" for i in range(0, 200, 20)] + ['>=200']+['']
# 计算y轴刻度的数量
grid_height = len(y_tick_labels_page)
# 横坐标的数量
grid_width = len(x_tick_labels_ip)



# 设置颜色映射
cmap = plt.cm.gray_r

fig, ax1 = plt.subplots(1,1,figsize=(3.23, 2.80))

for i in np.arange(0, array_len):
    for j in np.arange(0, array_len):
        if(rdip[i]==0):
            rect = patches.Rectangle((i, j), 1, 1,  # 此处假定每个方块的宽度和高度都是1
                                    linewidth=1,
                                    edgecolor='none',
                                    facecolor=plt.cm.gray_r(0))
        else:
            rect = patches.Rectangle((i, j), 1, 1,  # 此处假定每个方块的宽度和高度都是1
                                    linewidth=1,
                                    edgecolor='none',
                                    facecolor=plt.cm.gray_r(rdpage_of_ip[i][j]))
        # 添加矩形到图中
        ax1.add_patch(rect)

legend_rect = patches.Rectangle((9, 9), 1, 1, color=plt.cm.gray_r(0.5), label='$RD_{Page}$ distribution of same $RD_{PC}$')

# # 设置轴的刻度位置和标签
# ax1.plot(rdip, linestyle='-', marker='')  # linestyle='-' 表示实线

# 在每个数据点位置添加圆圈标记



# # 接下来，创建一个平滑的线条
# # 生成更多的x值以插值
# x = np.linspace(0, len(rdip) - 1, 300)
# # 创建一个插值函数
# f = interp1d(np.arange(len(rdip)), rdip, kind='cubic')
# # 使用插值函数得到平滑的y值
# smooth_y = f(np.linspace(0, len(rdip) - 1, 300))
# # 绘制平滑的灰色虚线
# ax1.plot(x + 0.5, smooth_y + 0.2, linestyle='--', color='gray')

# 设置x轴和y轴的范围
ax1.set_xlim(0, array_len)  # 假设你想让x轴的范围从0到数据长度
ax1.set_ylim(0, array_len)  # 可以根据需要调整y轴的范围

ax1.set_xticks(np.arange(0, grid_width ))  
ax1.set_yticks(np.arange(0, grid_height))
# ax1.set_xticklabels(x_tick_labels_ip,fontsize=9,rotation=45,ha='right')
ax1.set_xticklabels(['']*grid_width)
ax1.set_yticklabels(y_tick_labels_page,fontsize=9)
for i, label in enumerate(x_tick_labels_ip):
    ax1.text(i-0.2, -0.02, label, rotation=45,ha='center', va='top', transform=ax1.get_xaxis_transform())

# 设置坐标轴标签
ax1.set_xlabel('$RD_{PC}$',fontsize=9, fontweight='bold')
ax1.set_ylabel('$RD_{Page}$',fontsize=9, fontweight='bold')

ax1.xaxis.set_label_coords(1.1, -0.04)  # 将x轴标签移到轴的末端
ax1.yaxis.set_label_coords(-0.05, 1.05)  # 将y轴标签移到轴的顶部

# ax1.text(0.5, -0.12, '(a)', transform=ax1.transAxes, fontsize=24, fontweight='bold', va='top', ha='center')

# 显示图像

# 设置颜色条
# 创建一个ScalarMappable并初始化与图中用到的归一化对象和颜色映射
cmap = LinearSegmentedColormap.from_list('custom_gray', ['#f0f0f0', '#101010'], N=256)
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
norm = Normalize(vmin=0, vmax=1.0)
sm = ScalarMappable(cmap=plt.cm.gray_r, norm=norm)
sm.set_array([])  # 只是为了满足函数需求
cbar = plt.colorbar(sm, ax=[ax1])
cbar.outline.set_edgecolor('none')
def format_func(x, pos):
    return '{:.1f}'.format(x)
cbar.ax.yaxis.set_major_formatter(FuncFormatter(format_func))
cbar.ax.yaxis.set_major_locator(MaxNLocator(nbins=5)) 
# cbar.set_label('Accesses ratio with same $Q_{IP}$(a) and $Q_{Page}$(b) ',fontsize=30)
# cbar.set_label('Accesses ratio with same $Q_{IP}$(a) and $Q_{Page}$(b) ',fontsize=30)
plt.savefig(os.path.join(output_path_base,'grid.png'),dpi=800, format="png", bbox_inches='tight')
plt.savefig(os.path.join(output_path_base,'grid.pdf'),dpi=800, format="pdf", bbox_inches='tight')
plt.close()


y_ticks = np.around(np.arange(0.0, 1.01, 0.2), decimals=1)
y_label = np.around(np.arange(0, 101, 20), decimals=0)
fig, ax1 = plt.subplots(1,1,figsize=(3.23, 1.3))

for i, value in enumerate(rdip):
    print(value)
    ax1.bar(i + 0.5, value/10,zorder=2, edgecolor ="black",facecolor="grey",linewidth=1)  # i + 0.5 将圆圈右移0.5个单位 #,label='distribution of $RD_{PC}' if i==0 else ""
ax1.set_xticks(np.arange(0, grid_width ))  
ax1.set_yticks(y_ticks)
# ax1.set_xticklabels(x_tick_labels_ip,fontsize=9,rotation=45,ha='right')
ax1.set_xticklabels(['']*grid_width)
ax1.set_yticklabels(['0'] +[f'{item}%' for item in y_label[1:len(y_label)]])
ax1.set_xlim(0, array_len)  # 假设你想让x轴的范围从0到数据长度
ax1.set_ylim(0, 1.0)  # 可以根据需要调整y轴的范围
ax_idx = 0
for item in np.around(np.arange(0.0, 1.01, 0.1), decimals=1):
    if(ax_idx % 2 == 0):
        ax1.axhline(float(item), color='lightgray', linestyle='-', linewidth=1,zorder=1)
    else:
        ax1.axhline(float(item), color='lightgray', linestyle='--', linewidth=1,zorder=1)
    ax_idx += 1
for i, label in enumerate(x_tick_labels_ip):
    ax1.text(i-0.2, -0.02, label, rotation=45,ha='center', va='top', transform=ax1.get_xaxis_transform())
plt.savefig(os.path.join(output_path_base,'rdpc.png'),dpi=800, format="png", bbox_inches='tight')
plt.savefig(os.path.join(output_path_base,'rdpc.pdf'),dpi=800, format="pdf", bbox_inches='tight')

# 显示图形