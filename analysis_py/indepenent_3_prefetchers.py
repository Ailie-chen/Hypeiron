# import os
# import re
# from collections import Counter
# from concurrent.futures import ThreadPoolExecutor
# import matplotlib.pyplot as plt
# import numpy as np

# figure_res = './memtensefigures_res/all_methods_compare/spec2k17/'

# def plot_figure(array_n,benchs,arrays,labels,name):
#     # 创建一个新的图形
#     fig, ax = plt.subplots(figsize=(40, 12))
#     # 设定条形图的宽度
#     bar_width = 2.0 / (array_n + 0.5)
#     left_bar_pos = np.arange(len(benchs))*2
#     for i in range(array_n):
#         ax.bar(left_bar_pos + bar_width * i, 
#                arrays[i], 
#                width=bar_width, 
#                label=labels[i])
#     plt.subplots_adjust(bottom=0.2)
#     plt.xticks(left_bar_pos + bar_width * int(array_n/2), benchs, rotation=45, fontsize=15, ha='right')
#     for label in ax.get_yticklabels():
#         label.set_fontsize(20)
#     ax.set_xlabel('Benchmarks')
#     ax.set_title(f'{name}', fontsize=25)
#     ax.legend()
#     plt.savefig(f'{figure_res}/{name}.png',dpi=300) 
#     plt.close()

# def main():
#     directory = "./outputsum/output0728/spec2k17/"
#     benchs = []
#     ip_uses = []
#     ip_totals = []
#     ip_accs = []
#     ip_pq_fulls =[]
#     pages_uses = []
#     pages_totals = []
#     pages_accs = []
#     pages_pq_fulls = []
#     bop_uses = []
#     bop_totals = []
#     bop_accs = []
#     bop_pq_fulls = []
#     total_accuracys = []
#     ip_pages_accuracys = []

#     # 获取目录下所有文件列表并按照文件名进行排序
#     file_list = os.listdir(directory)
#     sorted_file_list = sorted(file_list)

#     for filename in sorted_file_list:
#         match_trace = re.search(r'---(.+)(\.champsimtrace\.xz|\.trace\.gz)', os.path.join(directory, filename))
#         benchs.append(match_trace.group(1))
#         with open(os.path.join(directory, filename), 'r') as file:
#             lines = file.readlines()
#             ip_use = 0
#             ip_total = 0
#             ip_pq_full = 0
#             pages_use = 0
#             pages_total = 0
#             pages_pq_full = 0
#             bop_use = 0
#             bop_total = 0
#             bop_pq_full = 0
#             for i in range(len(lines)):
#                 line = lines[i]
#                 match_ip_use = re.search(r"^\s*ip_useful\s+(\d+)", line)
#                 if match_ip_use:
#                     ip_use = int(match_ip_use.group(1))

#                 match_ip_total = re.search(r"^\s*ip_to_lower_level\s+(\d+)", line)
#                 if match_ip_total:
#                     ip_total = int(match_ip_total.group(1))

#                 match_ip_pq_full = re.search(r"^\s*ip_pq_full\s+(\d+)", line)
#                 if match_ip_pq_full:
#                     ip_pq_full = int(match_ip_pq_full.group(1))

#                 match_pages_use = re.search(r"^\s*pages_useful\s+(\d+)", line)
#                 if match_pages_use:
#                     pages_use = int(match_pages_use.group(1))

#                 match_pages_total = re.search(r"^\s*pages_to_lower_level\s+(\d+)", line)
#                 if match_pages_total:
#                     pages_total = int(match_pages_total.group(1))
                
#                 match_pages_pq_full = re.search(r"^\s*pages_pq_full\s+(\d+)", line)
#                 if match_pages_pq_full:
#                     pages_pq_full = int(match_pages_pq_full.group(1))

#                 match_bop_use = re.search(r"^\s*bop_useful\s+(\d+)", line)
#                 if match_bop_use:
#                     bop_use = int(match_bop_use.group(1))

#                 match_bop_total = re.search(r"^\s*bop_to_lower_level\s+(\d+)", line)
#                 if match_bop_total:
#                     bop_total = int(match_bop_total.group(1))

#                 match_bop_pq_full = re.search(r"^\s*bop_pq_full\s+(\d+)", line)
#                 if match_bop_pq_full:
#                     bop_pq_full = int(match_bop_pq_full.group(1))
#             ip_accuracy = 100.0 * float(ip_use)/ ip_total
#             pages_accuracy = 100.0 * float(pages_use)/ pages_total
#             bop_accuracy = 100.0 * float(bop_use)/ bop_total
#             ip_pages_accuracy = 100.0 * float(ip_use + pages_use)/(ip_total+pages_total)
#             total_accuracy = 100.0 * float(ip_use + pages_use + bop_use)/(ip_total+pages_total + bop_total)
#             ip_uses.append(ip_use)
#             ip_totals.append(ip_total)
#             ip_accs.append(ip_accuracy)
#             ip_pq_fulls.append(ip_pq_full)
#             pages_uses.append(pages_use)
#             pages_totals.append(pages_total)
#             pages_accs.append(pages_accuracy)
#             pages_pq_fulls.append(pages_pq_full)
#             bop_uses.append(bop_use)
#             bop_totals.append(bop_total)
#             bop_accs.append(bop_accuracy)
#             bop_pq_fulls.append(bop_pq_full)
#             ip_pages_accuracys.append(ip_pages_accuracy)
#             total_accuracys.append(total_accuracy)
            
#     plot_figure(3,benchs,[ip_uses,pages_uses,bop_uses],['ip_uses','pages_uses','bop_uses'],'uses')
#     plot_figure(3,benchs,[ip_totals,pages_totals,bop_totals],['ip_totals','pages_totals','bop_totals'],'pf_to_lower')
#     plot_figure(5,benchs,[ip_accs,pages_accs,bop_accs,ip_pages_accuracys,total_accuracys],['ip_accs','pages_accs','bop_accs','ip_pages_accuracys','total_accuracys'],'accuracy')



# if __name__ == "__main__":
#     if not os.path.exists(figure_res):
#     # 如果目录不存在，则创建该目录
#         os.makedirs(figure_res)
#     main()


import os
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import numpy as np

figure_res = './memtensefigures_res/all_methods_compare/spec2k17/'


def plot_figure2(array_n1, arrays1,labels1,array_n2, arrays2,labels2,benchs,name):
    # 创建一个新的图形，包含两个子图
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(40, 24), sharex=True)
    
    # 设定条形图的宽度
    bar_width = 2.0 / (array_n + 0.5)
    left_bar_pos = np.arange(len(benchs)) * 2

    for i in range(array_n):
        # 分别在两个子图上绘制条形图
        axes[0].bar(left_bar_pos + bar_width * i, arrays[i], width=bar_width, label=labels[i])
        axes[1].bar(left_bar_pos + bar_width * i, arrays[i], width=bar_width, label=labels[i])

    # 调整子图的布局
    plt.subplots_adjust(bottom=0.2)

    # 设置 x 轴刻度标签
    plt.xticks(left_bar_pos + bar_width * int(array_n / 2), benchs, rotation=45, fontsize=15, ha='right')

    # 设置 y 轴刻度标签的字体大小
    for label in axes[0].get_yticklabels():
        label.set_fontsize(20)
    for label in axes[1].get_yticklabels():
        label.set_fontsize(20)

    # 设置子图的标题和共享的 x 轴标签
    axes[0].set_title(f'{name}', fontsize=25)
    axes[1].set_xlabel('Benchmarks')
    axes[0].legend()
    axes[1].legend()

    # 保存图形并关闭图窗口
    plt.savefig(f'{figure_res}/{name}.png', dpi=300)
    plt.close()

def plot_figure(array_n,benchs,arrays,labels,name):
    # 创建一个新的图形
    fig, ax = plt.subplots(figsize=(40, 12))
    # 设定条形图的宽度
    bar_width = 2.0 / (array_n + 0.5)
    left_bar_pos = np.arange(len(benchs))*2
    for i in range(array_n):
        ax.bar(left_bar_pos + bar_width * i, 
               arrays[i], 
               width=bar_width, 
               label=labels[i])
    plt.subplots_adjust(bottom=0.2)
    plt.xticks(left_bar_pos + bar_width * int(array_n/2), benchs, rotation=45, fontsize=15, ha='right')
    for label in ax.get_yticklabels():
        label.set_fontsize(20)
    ax.set_xlabel('Benchmarks')
    ax.set_title(f'{name}', fontsize=25)
    ax.legend()
    plt.savefig(f'{figure_res}/{name}.png',dpi=300) 
    plt.close()

def custom_sort(file_name):
        # 使用正则表达式提取两个数字
        numbers = re.findall(r'\d+', file_name)
        if len(numbers) == 2:
            num1, num2 = int(numbers[0]), int(numbers[1])
            return num1, num2
        else:
            # 如果没有找到两个数字，则返回默认排序值
            return float('inf'), float('inf')

def main():
    directory = "./outputsum/output0729/spec2k19_statistic_txt/"
    benchs = []
    ip_nums = []
    pages_nums = []

    file_names = []
    # 获取目录下所有文件列表并按照文件名进行排序
    for file_name in os.listdir(directory):
        file_names.append(file_name)
    

# 使用自定义排序函数进行排序
    sorted_file_names = sorted(file_names, key=custom_sort)


    for filename in sorted_file_names:
        match_trace = re.search(r"^(.*)(?=\.txt$)", filename)
        if match_trace:
            benchs.append(match_trace.group(1))
            
        with open(os.path.join(directory, filename), 'r') as file:
            lines = file.readlines()

            for i in range(len(lines)):
                line = lines[i]
                match_pages = re.search(r"^Page_addr distribution:(\d+)", line)
                if match_pages:
                    
                    pages_nums.append(int(match_pages.group(1)))

                match_ip = re.search(r"^Ip_addr distribution:(\d+)", line)
                if match_ip:
                    ip_nums.append(int(match_ip.group(1)))
                    break

    print(len(benchs),len(pages_nums),len(ip_nums))
    plot_figure(2,benchs,[ip_nums,pages_nums],['ip_nums','pages_nums'],'access_pattern')


if __name__ == "__main__":
    if not os.path.exists(figure_res):
    # 如果目录不存在，则创建该目录
        os.makedirs(figure_res)
    main()