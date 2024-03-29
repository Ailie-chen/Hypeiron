import pickle 
from collections import Counter
import os
import glob
import multiprocessing
import re
import numpy as np
import math
directory = "./outputsum/output1158/ip_couple_page/"
output_path_base = "./outputsum/output1158/scatter_pickles"
##########统计每个测试程序的scatter的分布###########
pattern_ip = r'ip:(\d+).*count:(\d+).*ave_scatter_len:([\d.]+)'
pattern_page = r'page:(\d+).*count:(\d+).*ave_scatter_len:([\d.]+)'
page_nums_of_ip_pattern = r'\[(\d+)\s(\d+)\]'

scatter_stride_ip = 200
scatter_maximam_ip = 2000

scatter_stride_page = 20
scatter_maximam_page = scatter_stride_page*(scatter_maximam_ip/scatter_stride_ip)

array_len = int(scatter_maximam_ip/scatter_stride_ip) + 1


def get_array(path):
    ip_scatter = np.zeros(array_len)
    page_scatter = np.zeros(array_len)
    sum_ip_scatter = 0
    sum_ip_count = 0
    sum_page_scatter = 0
    sum_page_count = 0

    rdpage_of_ip=[[0 for _ in range(array_len)] for _ in range(array_len)]
    rdpage={}

    filename = os.path.basename(path)
    result_name = re.search(r'(.*)\.txt', filename).group(1)

    with open(path,'r') as file:
        lines=file.readlines()
        #首先获得每一个page的rd
        for i in range(len(lines)):
            line = lines[i]        
            page_match = re.match(pattern_page, line)
            if page_match:
                scatter = float(page_match.group(3))
                page = int(page_match.group(1))
                rdpage[page]=scatter


        for i in range(len(lines)):
            line = lines[i]

            ip_match = re.match(pattern_ip, line)
            page_nums_of_ip_matches = re.findall(page_nums_of_ip_pattern, line)
            
            if ip_match and page_nums_of_ip_matches:
                scatter = float(ip_match.group(3))
                count = int(ip_match.group(2))
                sum_ip_scatter += scatter*count
                sum_ip_count += count
                ip_grid=0
                if(count > 1):
                    if(scatter >= scatter_maximam_ip):
                        ip_grid=array_len-1                          
                    else:
                        ip_grid=math.floor(scatter/scatter_stride_ip)

                    ip_scatter[ip_grid] += count

                for page_nums in page_nums_of_ip_matches:

                    page = int(page_nums[0])
                    page_num =int(page_nums[1])
                    page_grid=0
                    if(rdpage[page] >= scatter_maximam_page):
                        page_grid=array_len-1
                    else:
                        page_grid=math.floor(rdpage[page]/scatter_stride_page)
                    rdpage_of_ip[ip_grid][page_grid]+=page_num
        #计算rdip中每个rdpage的比值
        for j in np.arange(0,array_len):
            sum_ip=sum(rdpage_of_ip[j])
            if sum_ip != 0:
                for k in np.arange(0,array_len):
                    rdpage_of_ip[j][k]=rdpage_of_ip[j][k]/sum_ip

            # if page_match:
            #     scatter = float(page_match.group(3))
            #     count = int(page_match.group(2))
            #     sum_page_scatter += scatter * count
            #     sum_page_count += count
            #     if(count > 1):
            #         if(scatter >= scatter_maximam):
            #             page_scatter[array_len-1] += count
            #         else:
            #             page_scatter[math.floor(scatter/scatter_stride)] += count
    file.close()
    sum_ip_scatter = sum(ip_scatter)
    sum_page_scatter = sum(page_scatter)
    ip_scatter = [item/sum_ip_scatter for item in ip_scatter]
    page_scatter = [item/sum_page_scatter for item in page_scatter]
    return result_name, ip_scatter, rdpage_of_ip

def extract_numbers(s):
    matches = re.findall(r'(\d+)', s)
    return tuple(int(x) for x in matches)

def custom_sort(item):
    name = item[0]
    return extract_numbers(name)


def main():
    page_ip_scatter=[]
    all_files = glob.glob(os.path.join(directory,'*'))
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        page_ip_scatter = pool.map(get_array,all_files)
        pool.close()
        pool.join()
    page_ip_scatter = sorted(page_ip_scatter, key=custom_sort)
    print(page_ip_scatter)
    if not os.path.exists(output_path_base):
    # 如果目录不存在，则创建该目录
        os.makedirs(output_path_base)
    with open(output_path_base+'/scatter.pkl','wb') as f:
        pickle.dump(page_ip_scatter,f)
if __name__ == "__main__":
    main()