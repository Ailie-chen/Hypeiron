import os
import math
import re
from collections import Counter
import multiprocessing
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import csv
import glob
import pickle
pattern = r"pc:(\d+) .* offset:(\d+) baddr:(\d+) vpaddr:(\d+)"
directory = "./outputsum/output1024/spec2k17_test/"
output_ip_pkl = "./outputsum/output1024/pickles/ip.pkl"
output_page_pkl = "./outputsum/output1024/pickles/page.pkl"
DISTANCE_THRESHOLD = 16
NUM_THRESHOLD = 8
def parse_file(path):
    page_addr_counter = Counter()
    page_addr_counter_iter = Counter()
    page_addr_counter_before_evicted = {}
    page_evicted_lt8_pages_arr = []
    page_ip_dict = {} #每次page被剔除时，访问对应的ip
    page_scatter_sets_dict = {}
    page_scatter_sets_len_dict={}
    page_one_access_num_lines={}
    page_scatter_len_ave = {}
    page_all_scatter_len_ave = 0
    page_get_threshold_ratio = 0.0
    page_ip_dict_num = {}
    page_ip_dict_scatter = {}
    

    ip_addr_counter = Counter()
    ip_addr_counter_iter = Counter()
    ip_addr_counter_before_evicted = {}
    ip_evicted_lt8_ips_arr = []
    ip_page_dict = {} #每次page被剔除时，访问对应的ip
    ip_scatter_sets_dict = {}
    ip_scatter_sets_len_dict={}
    ip_one_access_num_lines={}
    ip_scatter_len_ave = {}
    ip_all_scatter_len_ave = 0
    ip_get_threshold_ratio=0.0
    ip_page_dict_num = {}
    ip_page_dict_scatter = {}

    block_addr_counter = Counter()

    num_lines = 0

    with open(path, 'r') as file, open(output_ip_pkl, 'wb') as fip, open(output_page_pkl, 'wb') as fpage:
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i]
            # If line starts with a digit
            pattern_match = re.match(pattern, line)
            if pattern_match:
                num_lines += 1

                ip = int(pattern_match.group(1))
                page = int(pattern_match.group(4))
                addr = int(pattern_match.group(3))
             
                if(ip_addr_counter[ip] == 0):    
                    ip_scatter_sets_dict[ip] = set()              
                    ip_scatter_sets_len_dict[ip] = []
                    ip_one_access_num_lines[ip] = num_lines
                    ip_addr_counter_before_evicted[ip] = []
                    ip_page_dict[ip] = Counter()
                else:
                    ip_scatter_sets_len_dict[ip].append(len(ip_scatter_sets_dict[ip]))               
                for key in ip_scatter_sets_dict:
                    if(key != ip):
                        ip_scatter_sets_dict[key].add(ip)
                        len_scatter_key = len(ip_scatter_sets_dict[key])
                        if(len_scatter_key > 0 and len_scatter_key % DISTANCE_THRESHOLD == 0 and ip_addr_counter_iter[key] != 0):
                            ip_addr_counter_before_evicted[key].append(ip_addr_counter_iter[key])
                            ip_addr_counter_iter[key] = 0
                            if(ip_addr_counter_iter[key] < NUM_THRESHOLD):
                                page_num_arr = []
                                for page1,count1 in ip_page_dict[key].most_common():
                                    page_num_arr.append([page1,count1])
                                pickle.dump((key,page_num_arr),fip)
                                ip_page_dict[key] = Counter()
                ip_scatter_sets_dict[ip] = set()


                if(page_addr_counter[page] == 0):  
                    page_scatter_sets_dict[page] = set()                
                    page_scatter_sets_len_dict[page] = []
                    page_one_access_num_lines[page] = num_lines
                    page_addr_counter_before_evicted[page] = []
                    page_ip_dict[page] = Counter()
                else:
                    page_scatter_sets_len_dict[page].append(len(page_scatter_sets_dict[page]))
                for key in page_scatter_sets_dict:
                    if(key != page):
                        page_scatter_sets_dict[key].add(page)
                        len_scatter_key = len(page_scatter_sets_dict[key])
                        if(len_scatter_key > 0 and len_scatter_key % DISTANCE_THRESHOLD == 0 and page_addr_counter_iter[key] != 0):
                            page_addr_counter_before_evicted[key].append(page_addr_counter_iter[key])
                            page_addr_counter_iter[key] = 0
                            if(page_addr_counter_iter[key] < NUM_THRESHOLD):
                                ip_num_arr=[]
                                for ip1,count1 in page_ip_dict[key].most_common():
                                    ip_num_arr.append([ip1,count1])
                                pickle.dump((key,ip_num_arr), fpage)
                page_scatter_sets_dict[page] = set()

                ip_addr_counter[ip] += 1
                block_addr_counter[addr] += 1
                page_addr_counter[page] += 1

                ip_addr_counter_iter[ip] += 1
                page_addr_counter_iter[page] += 1

                for ip in ip_page_dict:
                    ip_page_dict[ip][page] += 1
                
                for page in page_ip_dict:
                    page_ip_dict[page][ip] += 1
    file.close()


def main():



    len_pages_ip=[]

    all_files = glob.glob(os.path.join(directory,'*.*z'))
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        len_pages_ip = pool.map(parse_file, all_files)
        pool.close()
        pool.join()


if __name__ == "__main__":
    main()
