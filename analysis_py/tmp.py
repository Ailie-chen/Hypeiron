import os
import math
import re
from collections import Counter
import multiprocessing
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import csv
import glob
# hashed_perceptron-no-vbertim-no-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-no---401.bzip2-277B.champsimtrace.xz
dir_base = 'outputsum/output1120/spec2k17/'
dir_new = 'outputsum/output1121/spec2k17/'
dir_new_res = 'outputsum/output1121/spec2k17/'
pattern = r"pc:(\d+).*offset:(\d+) baddr:(\d+) vpaddr:(\d+) ip:(\d+) (.*)"
def parse_file_new(filename_name):
    hit_pc_ip = Counter()
        result_name = re.search(r'(.*)\.champsimtrace\.xz', filename).group(1)
    with open(glob.glob.(os.path.join(dir_new,result_name)), 'r') as file:  
        lines = file.readlines()   
        for i in range(len(lines)):
            line = lines[i]
            if(1):
                pattern_match = re.match(pattern, line)
                if pattern_match:
                    if(pattern_match.group(6) == 'PH'):
                        hit_pc_ip[ip] += 1
    file.close()
    return hit_pc_ip
def parse_file_base(path):
    ###记录当前每一个出现的IP或者page
    vpaddr = {}
    ipaddr = {}
    addrs = []
    hit_pc_ip = Counter()
    ######同一个event上次访问的信息
    vpaddr_last = {}
    ipaddr_last = {}
    addr_last = 0

    #######同一个event对应的其他的信息
    ip_page_dic ={}
    ip_page_dic_tempo ={}

    last_offset = 0
    last_addr = 0
    filename = os.path.basename(path)
    result_name = re.search(r'(.*)\.champsimtrace\.xz', filename).group(1)
    with open(path, 'r') as file:  
        lines = file.readlines()   
        for i in range(len(lines)):
            line = lines[i]
            if(1):
                pattern_match = re.match(pattern, line)
                if pattern_match:
                    
                    ip = int(pattern_match.group(1))
                    page = int(pattern_match.group(4))
                    addr = int(pattern_match.group(3))
                    offset = int(pattern_match.group(2))
                    if(pattern_match.group(6) == 'PH'):
                        hit_pc_ip[ip] += 1

                    if page not in vpaddr:
                        vpaddr[page] = []
                        vpaddr_last[page]=0
                    vpaddr[page].append(offset - vpaddr_last[page])
                    if ip not in ipaddr:
                        ipaddr[ip] = []
                        ip_page_dic[ip] = set()
                        ip_page_dic_tempo[ip] = []
                        ipaddr_last[ip] = 0
                    ipaddr[ip].append(addr-ipaddr_last[ip])
                    ip_page_dic[ip].add(page)
                    ip_page_dic_tempo[ip].append((page,offset))
                    
                    addrs.append(addr - addr_last)

                    vpaddr_last[page] = offset
                    ipaddr_last[ip] = addr
                    addr_last = addr
    file.close()
    new_hit_ip = parse_file_new(filename)
    with open(glob.glob.(os.path.join(dir_new_res),f"{result_name}.txt")),'w') as file:
        # file.write(f"gloabl\n")
        # file.write(f"{addrs}\n")
        file.write(f"pagel\n")
        for key,value in vpaddr.items():
            file.write(f"{key}: {value}\n")
        file.write(f"ip\n")
        for key,value in ipaddr.items():
            file.write(f"{key}: {value}\n")
            # file.write(f" {ip_page_dic[key]}\n")
            # file.write(f" {ip_page_dic_tempo[key]}\n")


        all_misses = sum([len(value) for item,value in ipaddr.items()])
        for item, value in hit_pc_ip.most_common():
            file.write(f"{item}: miss_num:{len(ipaddr[item])}  cover_base:{format(value/len(ipaddr[item]), '.2f')} cover_new:{format(new_hit_ip[item]/len(ipaddr[item]), '.2f')}\n")
    file.close()

def main():


    len_pages_ip=[]

    all_files = glob.glob(os.path.join(dir_base,'*.*z'))
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        len_pages_ip = pool.map(parse_file, all_files)
        pool.close()
        pool.join()
    

if __name__ == "__main__":
    main()