
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
# 定义数组A和数组B
arrayA = [31225, 31031, 13346, 8353, 5732, 5568, 3027, 2736, 2736, 2453, 506, 506, 506, 506, 506, 477, 476, 474, 473, 470, 426, 251, 241, 24, 6, 3]
arrayB = [5569, 5569, 5568, 5568, 5568, 5568, 5568, 5568, 5568, 5548, 5523, 5412, 5071, 3249, 2784, 2784, 2784, 2784, 2784, 2784, 2783, 2783, 2688, 2616, 2611, 2583, 2579, 918, 333, 164, 158, 109, 40, 12, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]

# 计算两个数组的和
sumA = sum(arrayA)
sumB = sum(arrayB)

# 检查两个数组的和是否相等
if sumA != sumB:
    print("unequal")
else:

    # 计算元素值与总和的比率
    ratioA = [x / sumA for x in arrayA]
    ratioB = [(0-x) / sumB for x in arrayB]

    c_page_point = 8
    c_ip_point = 24
    # 导入绘图库
    lengthA=len(arrayA)
    lengthB=len(arrayB)
    indexA_ratio = np.arange(1,c_page_point+1)
    indexB_ratio = np.arange(1,c_ip_point + 1)
    indexA_others = np.arange(c_page_point+1, lengthA+1)
    indexB_others = np.arange(c_ip_point+1, lengthB+1)

    # 设置柱状图的宽度
    bar_width = 1.0

    # 绘制柱状图
    plt.figure(figsize=(10,8),dpi=300)
    plt.bar(indexA_ratio, ratioA[0:c_page_point], width=bar_width, edgecolor='black',label='PMF of top $C_{PAGE\_point}$ pages',facecolor="grey",hatch="///",alpha=0.6)
    plt.bar(indexB_ratio, ratioB[0:c_ip_point], width=bar_width, edgecolor='black',label='PMF of top $C_{IP\_point}$ ip',facecolor="black",hatch="...",alpha=0.5)
    plt.bar(indexA_others, ratioA[c_page_point:lengthA], width=bar_width, edgecolor='black', label='PMF of other pages',facecolor="grey",alpha=0.6)
    plt.bar(indexB_others, ratioB[c_ip_point:lengthB], width=bar_width, edgecolor='black', label='PMF of other IP',facecolor="black",alpha=0.5)


    plt.annotate('',
             xy=(c_page_point+0.5, 0.08),  # 箭头的头部（箭头指向的位置）
             xytext=(c_page_point+0.5, 0.0),  # 箭头的尾部（箭头开始的位置）
             arrowprops=dict(# arrowstyle='-|>',  # 箭头的样式
                             facecolor='black',  
                             lw=0.03, # 线条宽度
                             headwidth=6,  # 箭头头部宽度
                             headlength=8,  # 箭头头部长度
                             width=1 # 箭头身体宽度
                            )
    )

    # 添加文本在“图例”项左侧
    text = plt.annotate('PAGE Cover Ratio: $ \sum $',
                        xy=(c_page_point-4.0, 0.10),
                        xycoords='data',
                        xytext=(0, 0),  # 文本在“图例”项右侧的位置
                        textcoords='offset points', 
                        ha='left',  # 左对齐
                        va='center')  # 垂直居中
    # 添加一个斜纹的“图例”项
    legend = plt.annotate('  ',
                        xy=(c_page_point+5.2, 0.098),  # “图例”项的位置
                        xycoords='data',
                        xytext=(0, 0),  # 无偏移
                        textcoords='offset points',
                        bbox=dict(boxstyle="square,pad=0.35", 
                                    hatch="///", 
                                    edgecolor="black", 
                                    facecolor="grey", 
                                    alpha=0.4,
                                    linewidth=1))
    # 添加文本在“图例”项右侧
    text = plt.annotate('$ \geq 0.9$',
                        xy=(c_page_point+6.2, 0.10),
                        xycoords='data',
                        xytext=(0, 0),  # 文本在“图例”项右侧的位置
                        textcoords='offset points', 
                        ha='left',  # 左对齐
                        va='center')  # 垂直居中
       # 添加文本在“图例”项左侧
    text = plt.annotate('$ C_{PAGE\_point} = 8 $',
                        xy=(c_page_point-1.0, 0.085),
                        xycoords='data',
                        xytext=(0, 0),  # 文本在“图例”项右侧的位置
                        textcoords='offset points', 
                        ha='left',  # 左对齐
                        va='center')  # 垂直居中




    ip_y_pos = -0.055
    plt.annotate('',
             xy=(c_ip_point+0.5, ip_y_pos+0.020),  # 箭头的头部（箭头指向的位置）
             xytext=(c_ip_point+0.5, 0.0),  # 箭头的尾部（箭头开始的位置）
             arrowprops=dict(# arrowstyle='-|>',  # 箭头的样式
                             facecolor='black',  
                             lw=0.03, # 线条宽度
                             headwidth=6,  # 箭头头部宽度
                             headlength=8,  # 箭头头部长度
                             width=1 # 箭头身体宽度
                            )
    )

    # 添加文本在“图例”项左侧
    text = plt.annotate('IP Cover Ratio: $ \sum $',
                        xy=(c_ip_point-4.0, ip_y_pos+0.015),
                        xycoords='data',
                        xytext=(0, 0),  # 文本在“图例”项右侧的位置
                        textcoords='offset points', 
                        ha='left',  # 左对齐
                        va='center')  # 垂直居中
    # 添加一个斜纹的“图例”项
    legend = plt.annotate('  ',
                        xy=(c_ip_point+3.7, ip_y_pos-0.002+0.015),  # “图例”项的位置
                        xycoords='data',
                        xytext=(0, 0),  # 无偏移
                        textcoords='offset points',
                        bbox=dict(boxstyle="square,pad=0.35", 
                                    hatch="...", 
                                    edgecolor="black", 
                                    facecolor="grey", 
                                    alpha=0.4,
                                    linewidth=1))
    # 添加文本在“图例”项右侧
    text = plt.annotate('$ \geq 0.9$',
                        xy=(c_ip_point+4.7, ip_y_pos+0.015),
                        xycoords='data',
                        xytext=(0, 0),  # 文本在“图例”项右侧的位置
                        textcoords='offset points', 
                        ha='left',  # 左对齐
                        va='center')  # 垂直居中
       # 添加文本在“图例”项左侧
    text = plt.annotate('$ C_{IP\_point} = 24 $',
                        xy=(c_ip_point-1.0, ip_y_pos),
                        xycoords='data',
                        xytext=(0, 0),  # 文本在“图例”项右侧的位置
                        textcoords='offset points', 
                        ha='left',  # 左对齐
                        va='center')  # 垂直居中


    def positive_formatter(x, pos):
        return str(abs(round(x, 2)))
    # 创建自定义格式化程序的实例
    y_axis_formatter = FuncFormatter(positive_formatter)
    # ... [绘制柱状图的代码]
    # 应用自定义格式化程序
    plt.gca().yaxis.set_major_formatter(y_axis_formatter)


    # 设置x轴的刻度，每10个显示一个
    max_length = max(lengthA, lengthB)
    tick_spacing = 10
    plt.xticks(np.arange(1, max_length + 1, tick_spacing), np.arange(1, max_length + 1, tick_spacing))
    plt.xlim(left=0.45) 
    plt.xlabel('ip/index number', ha='right', position=(1,0), x=1,fontsize=13)
    plt.ylabel('accesses in each page or with each IP / total accesses(PMF)',fontsize=13)
    plt.legend()
    # plt.grid(True)
    dpi=600
    plt.savefig('analysis_py/ip_page_distribution.png',dpi=300, format="png", bbox_inches='tight')
    plt.savefig('analysis_py/ip_page_distribution.pdf',dpi=300, format="pdf", bbox_inches='tight')
    plt.show()

