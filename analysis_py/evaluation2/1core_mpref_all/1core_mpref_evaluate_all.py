# -*- coding: utf-8 -*-

import os
import re
import multiprocessing
# import multiprocessing as mp
import glob
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Tuple
from functools import lru_cache
from matplotlib.pyplot import MultipleLocator, ScalarFormatter, FormatStrFormatter, FixedFormatter, FuncFormatter, FixedLocator
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages
import json
import sys
from openpyxl import load_workbook, Workbook
from openpyxl.chart import LineChart, Reference


#import  draw_figs


# ========== SETTINGS ===============
#嵌套字典，第一层键为trace名称，第二层键为prefetcher名称
ROI_ORIGIN_STATS: Dict[str, Dict[str, Any]] = {}
CONFIGS: Dict[str, Any] = {}
#嵌套字典，用来对提取的信息进行绘图，第一层键是绘图的指标，第二层键是prefetcher的名称
FIG_STATS: Dict[str, Dict[str, Any]] = {}
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
# ========== SETTINGS ===============
benchmarks={
        "spec2006":[
                "400.perlbench-50B", "401.bzip2-277B", "403.gcc-48B", "410.bwaves-1963B",
                "416.gamess-875B", "429.mcf-217B", "433.milc-127B", "434.zeusmp-10B",
                "435.gromacs-111B", "436.cactusADM-1804B", "437.leslie3d-134B", "444.namd-120B",
                "445.gobmk-36B", "447.dealII-3B", "450.soplex-247B", "453.povray-252B",
                "454.calculix-460B", "456.hmmer-327B", "458.sjeng-1088B", "459.GemsFDTD-1169B",
                "462.libquantum-1343B", "464.h264ref-97B", "465.tonto-1914B", "470.lbm-1274B",
                "471.omnetpp-188B", "473.astar-359B", "481.wrf-196B", "482.sphinx3-1100B",
                "483.xalancbmk-716B", "600.perlbench_s-1273B",   
            ],
        "spec2017":[
                "602.gcc_s-2375B", "603.bwaves_s-5359B", "605.mcf_s-1644B", "607.cactuBSSN_s-4248B",
                "619.lbm_s-4268B", "620.omnetpp_s-874B", "621.wrf_s-8100B", "623.xalancbmk_s-700B",
                "625.x264_s-39B", "627.cam4_s-573B", "628.pop2_s-17B", "631.deepsjeng_s-928B",
                "638.imagick_s-10316B", "641.leela_s-1083B", "644.nab_s-12521B", "648.exchange2_s-1712B",
                "649.fotonik3d_s-10881B", "654.roms_s-1613B", "657.xz_s-4994B"
            ]
        }

benchemarks=[]
def read_config(path: str) -> Dict[str, Any]:
    global CONFIGS
    with open(path, 'r') as fw:
        CONFIGS = json.load(fw)
    CONFIGS["simulator_path"] = CURRENT_DIRECTORY+"/../../.."
    #CONFIGS["results_dir"] = CONFIGS["simulator_path"]+"/"+CONFIGS["results_dir"]
    CONFIGS["stats_dir"] = CONFIGS["simulator_path"]+"/"+CONFIGS["stats_dir"]
    
    return CONFIGS


#在保存结果的字典中加入每一个条目，双重字典，第一层字典为trace，第二层字典为prefetcher
#返回的entry也是一个字典类型的量
def add_entry(stats: Dict[str, Any], trace: str, prefetcher: str) -> Dict[str, Any]:
    if trace not in stats:
        stats[trace] = {}
    if prefetcher not in stats[trace]:
        stats[trace][prefetcher] = {}
    entry = stats[trace][prefetcher]
    for field in CONFIGS["metrics"]:
        if field not in entry:
            if trace == 'Average':
                entry[field] = []
            else:
                entry[field] = ['-'] * CONFIGS["core_num"]#初始化一个长度为core_num，内容为-的空列表
        
    return entry

#定义中的->应该是返回结果的类型
#应该是对跑出的结果进行提取
def parse_file(file: str) -> Tuple[str, str, int, Dict[str, Any]]:
    global ROI_ORIGIN_STATS
    level = 1
    #提取文件名称中的关键词
    match_prefetcher = re.search(r"-(\w+)-(\w+)-no", file)
    if not match_prefetcher:
        match_prefetcher = match_prefetcher = re.search(r"-(\w+)\-no", file)
        if not match_prefetcher:
            print("no match_prefetcher");
            return '', '', -1, {}
        else:
            level = 1
    else:
        level = 2
    match_trace = re.search(r'---(.+)(\.champsimtrace\.xz|\.trace\.gz|\.trace\.xz)', file)
    if not match_trace:
        print("no match_trace");
        return '', '', -1, {}



    #判断trace是否在output_workloads中，以及output_workloads是否存在 
    trace = match_trace.group(1)
    if not CONFIGS["output_workloads"] or trace not in CONFIGS["output_workloads"]:
        return '', '', -1, {}
    #提取prefetcher并判断
    if(level == 1):
        prefetcher = match_prefetcher.group(1)
        # print(match_prefetcher[0])
    else:
        # print(match_prefetcher[0][0])
        prefetcher = f'{match_prefetcher.group(1)}+{match_prefetcher.group(2)}'
    
    # print(prefetcher)
    if prefetcher != 'no' and CONFIGS["output_prefetchers"] and prefetcher not in CONFIGS["output_prefetchers"]:
        return '', '', -1, {}
    
    CONFIGS["insts_num"]="80M"

    #还没开始提取文本文件中的数据，首先加入每一个的trace和prefetcher空条目
    entry=add_entry(ROI_ORIGIN_STATS,trace, prefetcher)
    cpu=-1

    #在读取cs时由于UNIQUE_ASID[0] = �这里会错误，所以需要加上, errors='ignore'
    with open(file, mode='r', errors='ignore') as f:
        current_cpu = -1
        for line in f.readlines():
            line = line.strip()
            regex = re.search(r'CPU ([0-3]) cumulative IPC: (.*) instructions: (.*) c', line)
            if regex:
                cpu = int(regex.group(1))
                current_cpu = cpu
                val = float(regex.group(2))
                entry['IPC'][cpu] = val
                val = float(regex.group(3))
                entry['Instructions'][cpu] = val
            

            # print(CONFIGS["evaluate_cache"], line)
            
            for evaluate_cache in ["L1D","L2C","LLC"]:
                # pattern = '^' + evaluate_cache +'.*'+'LOAD' + '\s+' + 'ACCESS:\s+(\d+)\s+HIT:\s+(\d+)\s+MISS:\s+(\d+)'
                pattern = '^' + evaluate_cache + '.*' + 'LOAD' + '\s+' + 'ACCESS:\s+(\d+)\s+HIT:\s+(\d+)\s+MISS:\s+(\d+).*MPKI:\s+(\d+\.\d+)'
                matches = re.search(pattern, line)
                if matches:
                    load_request = int(matches.group(1))
                    load_hit = int(matches.group(2))
                    load_miss = int(matches.group(3))
                    load_mpki = float(matches.group(4))
                    entry[evaluate_cache+" Accesses"][current_cpu] = load_request
                    entry[evaluate_cache+" Misses"][current_cpu] = load_miss
                    
                pattern2 = '^' + evaluate_cache + '.*' + 'PREFETCH' + '.*' + 'REQUESTED:\s+(\d+)\s+ISSUED:\s+(\d+)\s+USEFUL:\s+(\d+)\s+USELESS:\s+(\d+)\s*$'
                matches2 = re.search(pattern2, line)
                if matches2:
                    prefetch_request = int(matches2.group(1))
                    prefetch_issue = int(matches2.group(2))
                    prefetch_useful = int(matches2.group(3))
                    prefetch_useless = int(matches2.group(4))
                    entry[evaluate_cache+" Prefetches"][cpu] = prefetch_useful + prefetch_useless
                    entry[evaluate_cache+" Prefetch Hits"][cpu] = prefetch_useful
                    entry[evaluate_cache+" Non-useful Prefetches"][current_cpu] = prefetch_useless

                pattern_pref_miss =  '^' + evaluate_cache  + ' PREFETCH  ACCESS:' + '.*' + 'MISS:\s+(\d+)'
                matches_pattern_pref_miss = re.search(pattern_pref_miss, line)
                if(matches_pattern_pref_miss):
                    entry[evaluate_cache+" Prefetch Miss"][cpu] = int(matches_pattern_pref_miss.group(1))
                    # print(int(matches_pattern_pref_miss.group(1)))
                pattern_pref_access =  '^' + evaluate_cache  + ' PREFETCH  ACCESS:\s+(\d+)'
                matches_pattern_pref_access = re.search(pattern_pref_access, line)
                if(matches_pattern_pref_access):
                    entry[evaluate_cache+" Prefetch Access"][cpu] = int(matches_pattern_pref_access.group(1))
                    # print(int(matches_pattern_pref_access.group(1)))
                # pattern_pref_miss =  '^' + evaluate_cache  + ' PREFETCH  ACCESS:' + '.*' + 'MISS:\s+(\d+)'
                # matches_pattern_pref_miss = re.search(pattern_pref_miss, line)
                # if(matches_pattern_pref_miss):
                #     entry[evaluate_cache+" Prefetch Miss"][cpu] = int(matches_pattern_pref_miss.group(1))  

                pattern3 = '^'+ evaluate_cache + '.*' + 'TIMELY PREFETCHES:\s+(\d+) LATE PREFETCHES:\s+(\d+)'
                matches3 = re.search(pattern3, line)
                if matches3:
                    prefetch_late = int(matches3.group(1))
                    entry[evaluate_cache+" prefetch_late"][current_cpu] = prefetch_late
                
                pattern4 = r"^L1D USEFUL LOAD.*?(\d+\.\d+)$"
                matches4 = re.search(pattern4,line)
                if matches4:
                    entry[evaluate_cache+" LOAD_ACCURACY"][current_cpu] = float(matches4.group(1))
            # pattern_DRAMaccess = r'LLC TOTAL(\s+)ACCESS:(\s+)(\d+)  HIT:(\s+)(\d+)  MISS:(\s+)(\d+)  HIT %:'
            pattern_DRAMaccess = r'LLC TOTAL(\s+)ACCESS:(\s+)(\d+)  HIT:(\s+)(\d+)  MISS:(\s+)(\d+)  HIT %:'
            # pattern_DRAMaccess = r'RQ ROW_BUFFER_HIT:(\s+)(\d+)  ROW_BUFFER_MISS:(\s+)(\d+)'
            matches_DRAMaccess = re.search(pattern_DRAMaccess,line)
            if matches_DRAMaccess:
                entry["DRAM Access"][cpu] = int(matches_DRAMaccess.group(3))
                # if entry["DRAM Access"][current_cpu] == 0:
                #     entry["DRAM Access"][current_cpu] = 1

    return trace, prefetcher, cpu, entry

#用多线程来对函数结果进行parse
#使用map的方法，将parse_file应用于res_files(all_files)中的每一个文件
def parse_origin_results() -> None:
    global ROI_ORIGIN_STATS
    res_files1 = glob.glob(os.path.join(CONFIGS["baseline_results_dir"], '*.*z'))
    all_files = res_files1
    for res_files in CONFIGS["results_dir"]:
        all_files += glob.glob(os.path.join(res_files, '*.*z'))
    #CONFIGS["results_dir"] = CONFIGS["simulator_path"]+"/"+CONFIGS["results_dir"]
    #res_files2 = glob.glob(os.path.join(CONFIGS["results_dir"], '*.xz'))
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        results = pool.map(parse_file, all_files)
        pool.close()
        pool.join()
    #遍历结果列表中的每个元素，其中每个元素
    #包含了解析结果中的 trace、prefetcher、cpu 和 entry
    for trace, prefetcher, cpu, entry in results:
        if cpu == -1 or not entry:
            continue
        # print(trace,prefetcher,entry)
        # print(ROI_ORIGIN_STATS)

        #调用 add_entry 函数，将当前元素的 trace 
        #和 prefetcher 添加到 ROI_ORIGIN_STATS 字典中
        add_entry(ROI_ORIGIN_STATS,trace, prefetcher)
        #将当前元素的 entry 存储到 ROI_ORIGIN_STATS 字典的相应位置
        ROI_ORIGIN_STATS[trace][prefetcher] = entry

def arith_mean(x):
    x = [v for v in x if v != '-']
    if not x:
        return '-'
    return 1.0 * sum(x) / len(x)

def geo_mean(x):
    x = [v for v in x if v != '-']
    if not x:
        return '-'
    prod = 1.0

    for val in x:
        # print("val: ",val)
        prod *= val
        # print("prod: ",prod)

    # print("prod: ",prod)
    return prod ** (1.0 / len(x))

def cal_final_results():
    for trace in ROI_ORIGIN_STATS:
        # print(trace)
        baseline = ROI_ORIGIN_STATS[trace]["no"]

        # print(ROI_ORIGIN_STATS[trace]['no'])
        for prefetcher in ROI_ORIGIN_STATS[trace]:
            # print(ROI_ORIGIN_STATS[trace])
            entry = ROI_ORIGIN_STATS[trace][prefetcher]
            # print(trace,prefetcher)
            for cpu in range(CONFIGS["core_num"]):
                
                #IPCI是相对于baseline的IPC比
                for evaluate_cache in ["L1D","L2C","LLC"]:
                    # print("TRAFFIC: ", entry['Accesses'][cpu], entry['Prefetches'][cpu], baseline['Accesses'][cpu])
                    #scale_coef: baseline的cache的访问次数，除以prefetch的访问次数
                    if isinstance(entry[evaluate_cache+' Accesses'][cpu], str):
                        # print("entry_Access:")
                        # print(evaluate_cache,trace,prefetcher,entry[evaluate_cache+' Accesses'][cpu])
                        entry[evaluate_cache+' Accesses'][cpu]=1
                    if isinstance(baseline[evaluate_cache+' Accesses'][cpu], str):
                        # print("entry_Access:")
                        # print(evaluate_cache,trace,prefetcher,entry[evaluate_cache+' Accesses'][cpu])
                        baseline[evaluate_cache+' Accesses'][cpu]=1
                    scale_coef = 1.0 * (baseline[evaluate_cache+' Accesses'][cpu] / entry[evaluate_cache+' Accesses'][cpu])
                    #print(entry[evaluate_cache+' Accesses'][cpu], entry[evaluate_cache+' Prefetches'][cpu], baseline[evaluate_cache+' Accesses'][cpu])
                    
                    
                    # entry['IPCI Speedup'][cpu] = entry['IPCI'][cpu] - 1
                    if(baseline[evaluate_cache+' Misses'][cpu] == 0 or baseline[evaluate_cache+' Misses'][cpu] == '-'):
                        baseline[evaluate_cache+' Misses'][cpu] = 1
                        # print(trace)
                        # print(prefetcher)
                        # print(evaluate_cache)
                    if isinstance(entry[evaluate_cache+' Misses'][cpu], str):
                        # print(evaluate_cache,prefetcher, "scale_coef: ", scale_coef,baseline[evaluate_cache+ ' Misses'][cpu],entry[evaluate_cache+ ' Misses'][cpu])
                        entry[evaluate_cache+ ' Misses'][cpu]=1
                    if isinstance(entry[evaluate_cache+' Prefetch Miss'][cpu], str):
                        # print(evaluate_cache,prefetcher, "scale_coef: ", scale_coef,baseline[evaluate_cache+ ' Misses'][cpu],entry[evaluate_cache+ ' Misses'][cpu])
                        entry[evaluate_cache+ ' Prefetch Miss'][cpu]=0
                    if isinstance(entry[evaluate_cache+' Prefetch Access'][cpu], str):
                        # print(evaluate_cache,prefetcher, "scale_coef: ", scale_coef,baseline[evaluate_cache+ ' Misses'][cpu],entry[evaluate_cache+ ' Misses'][cpu])
                        entry[evaluate_cache+ ' Prefetch Access'][cpu]=0
                    entry[evaluate_cache+ ' Coverage'][cpu] = 1.0 - 1.0 * entry[evaluate_cache+ ' Misses'][cpu] / baseline[evaluate_cache+' Misses'][cpu] * scale_coef
                    
                    entry[evaluate_cache+' Uncovered'][cpu] = 1.0 - entry[evaluate_cache+' Coverage'][cpu]
                    entry[evaluate_cache+' Overprediction'][cpu] = 1.0 * entry[evaluate_cache+' Non-useful Prefetches'][cpu] / baseline[evaluate_cache+' Misses'][cpu] * scale_coef
                    
                    if entry[evaluate_cache+' Prefetch Hits'][cpu] + entry[evaluate_cache+' Non-useful Prefetches'][cpu] == 0:
                        entry[evaluate_cache+' Accuracy'][cpu] = '-'
                    else:
                        entry[evaluate_cache+' Accuracy'][cpu] = 1.0 * entry[evaluate_cache+' Prefetch Hits'][cpu] / (entry[evaluate_cache+' Prefetch Hits'][cpu] + entry[evaluate_cache+' Non-useful Prefetches'][cpu])
                    
                    entry[evaluate_cache+ ' MPKI'][cpu] = 1000.0 * entry[evaluate_cache+' Misses'][cpu] / entry['Instructions'][cpu]
                    # if(prefetcher == 'vberti' and evaluate_cache == 'L1D' and entry[evaluate_cache+ ' MPKI'][cpu] >= 5.0):
                    #     print(f"\"{trace}\",")

                    # entry[evaluate_cache+' traffic'][cpu] = 1.0 * (entry[evaluate_cache+' Accesses'][cpu]+ entry[evaluate_cache+' Prefetches'][cpu])  / baseline[evaluate_cache+' Accesses'][cpu]
                    if(baseline[evaluate_cache+" Accesses"][cpu] == 1):
                        entry[evaluate_cache+' traffic'][cpu] = 1
                    else:
                        entry[evaluate_cache+' traffic'][cpu] = 1.0 * (entry[evaluate_cache+" Misses"][cpu] + entry[evaluate_cache+" Prefetch Miss"][cpu])  / baseline[evaluate_cache+" Misses"][cpu]
                        # entry[evaluate_cache+' traffic'][cpu] = 1.0 * (entry[evaluate_cache+' Prefetch Access'][cpu]+entry[evaluate_cache+' Accesses'][cpu])  / baseline[evaluate_cache+' Accesses'][cpu]
                        # entry[evaluate_cache+' traffic'][cpu] = 1.0 + entry[evaluate_cache+' Overprediction'][cpu]
                entry['Global Coverage'][cpu] = entry['L1D Coverage'][cpu] + (1 - entry['L1D Coverage'][cpu] )*(entry['L2C Coverage'][cpu] )
                
                entry['IPCI'][cpu] = 1.0 * entry['IPC'][cpu] / baseline['IPC'][cpu]
                entry['DRAM traffic'][cpu] = 1.0 * (entry['LLC Misses'][cpu] + entry['LLC Prefetch Miss'][cpu]) / baseline['LLC Misses'][cpu]
                
                if "TIME PC+Address Prefetches" in entry and  entry['TIME PC+Address Prefetches'][cpu] != '-':
                    entry['Prefetches'][cpu] = max(entry['Prefetches'][cpu],1)
                    entry['Non-useful Prefetches'][cpu] = max(entry['Non-useful Prefetches'][cpu],1)
                    entry['Prefetch Hits'][cpu] = max(entry['Prefetch Hits'][cpu],1)
                    
                    entry['TIME PC+Address Prefetches (%)'][cpu] = entry['TIME PC+Address Prefetches'][cpu] / entry['Prefetches'][cpu]
                    entry['TIME PC+Address Covered Misses (%)'][cpu] = entry['TIME PC+Address Covered Misses'][cpu] / entry['Prefetch Hits'][cpu]
                    entry['TIME PC+Address Overpredictions (%)'][cpu] = entry['TIME PC+Address Overpredictions'][cpu] / entry['Non-useful Prefetches'][cpu]
                
                if 'PC+Address Prefetches' in entry.keys() and entry['PC+Address Prefetches'][cpu] != '-':
                    entry['Prefetches'][cpu] = max(entry['Prefetches'][cpu],1)
                    entry['Non-useful Prefetches'][cpu] = max(entry['Non-useful Prefetches'][cpu],1)
                    entry['Prefetch Hits'][cpu] = max(entry['Prefetch Hits'][cpu],1)
                    
                    entry['PC+Address Prefetches (%)'][cpu] = entry['PC+Address Prefetches'][cpu] / entry['Prefetches'][cpu]
                    entry['PC+Offset Prefetches (%)'][cpu]  = entry['PC+Offset Prefetches'][cpu]  / entry['Prefetches'][cpu]
                    entry['PC+Address Covered Misses (%)'][cpu] = entry['PC+Address Covered Misses'][cpu] / entry['Prefetch Hits'][cpu]
                    entry['PC+Offset Covered Misses (%)'][cpu]  = entry['PC+Offset Covered Misses'][cpu]  / entry['Prefetch Hits'][cpu]
                    entry['PC+Address Overpredictions (%)'][cpu] = entry['PC+Address Overpredictions'][cpu] / entry['Non-useful Prefetches'][cpu]
                    entry['PC+Offset Overpredictions (%)'][cpu]  = entry['PC+Offset Overpredictions'][cpu]  / entry['Non-useful Prefetches'][cpu]

                # if(entry)
    # print("Each IPC",ROI_ORIGIN_STATS["mix1"]["bingo"]['Each IPC'])
    # Get the average value between cores
    
    for trace in ROI_ORIGIN_STATS:
        baseline_origin = ROI_ORIGIN_STATS[trace]["no"]
        for prefetcher in ROI_ORIGIN_STATS[trace]:
            entry = ROI_ORIGIN_STATS[trace][prefetcher]
            # print(trace,prefetcher,entry["PHT Match Probability"])
            for field in CONFIGS["metrics"]:
                # print(field)
                if field == 'Each IPC' or "Each IPC" in field :
                    continue
                if field == 'IPC':
                    # if(CONFIGS["core_num"] > 1):
                    #     entry['Each IPC'] = "_".join(map(str,entry[field]))
                    # if(CONFIGS["core_num"] > 1 and field == "IPC"):
                    #             # print(entry[field])
                    #     entry['Each IPC'] = "_".join(map(lambda x: "{:.2f}".format(x), entry[field]))
                    entry[field]= geo_mean(entry[field])

                else:
                    if(CONFIGS["core_num"] > 1 and field == "IPCI"):
                        # print(entry[field])
                        # entry['Each IPC'] = "_".join(map(lambda x: "{:.2f}".format(x), entry[field]))
                        entry['Each IPC 0'] = entry[field][0]
                        entry['Each IPC 1'] = entry[field][1]
                        entry['Each IPC 2'] = entry[field][2]
                        entry['Each IPC 3'] = entry[field][3]
                        
                        # print(entry['Each IPC'])
                    # print(trace,prefetcher,entry["PHT Match Probability"])
                    # print(field,entry[field])
                    entry[field] = arith_mean(entry[field])
            
    # print("Each IPC",ROI_ORIGIN_STATS["mix1"]["bingo"]['Each IPC'])
    # calculate average statistics from all benchmarks
    #在这个地方，外层是trace循环，内层是prefetch循环，每次对一个prefetch有一个条目，所有当
    #遍历外层循环之后，每个prefetch的entry就会有所有trace的数据
    ROI_ORIGIN_STATS['Average'] = {}
    for trace in ROI_ORIGIN_STATS:
        if trace == 'Average':
            continue
        for prefetcher in ROI_ORIGIN_STATS[trace]:
            entry = ROI_ORIGIN_STATS[trace][prefetcher]
            avg_entry = add_entry(ROI_ORIGIN_STATS,'Average', prefetcher)
            for field in CONFIGS["metrics"]:
                if field == 'Each IPC' or "Each IPC" in field:
                    continue
                avg_entry[field].append(entry[field])
                # print(field,  prefetcher, trace, avg_entry[field])
    for prefetcher in ROI_ORIGIN_STATS['Average']:
        entry = ROI_ORIGIN_STATS['Average'][prefetcher]
        for field in CONFIGS["metrics"]:
            if field == 'Each IPC' or "Each IPC" in field:
                continue
            if field == 'IPCI':
                # print(entry[field])
                entry[field] = geo_mean(entry[field])
                # print(entry[field])
            else:
                
                entry[field] = arith_mean(entry[field])

    for trace in ROI_ORIGIN_STATS:
        max_ipci = 0
        best_ipc=None
        if CONFIGS["my_prefetcher"] not in ROI_ORIGIN_STATS[trace]:
            break
        for prefetcher in ROI_ORIGIN_STATS[trace]:
            # print(trace,prefetcher)
            entry = ROI_ORIGIN_STATS[trace][prefetcher]
            if prefetcher == CONFIGS["my_prefetcher"]:
                continue
            # print(prefetcher,trace)
            # print(entry['IPCI'])
            entry['Delta'] = entry['IPCI'] - ROI_ORIGIN_STATS[trace][CONFIGS["my_prefetcher"]]["IPCI"]
            if (max_ipci < entry['IPCI']):
                max_ipci = entry['IPCI']
                best_ipc = prefetcher
            # max_ipci = max(max_ipci, entry['IPCI'])
            # print(trace,prefetcher,max_ipci,entry['IPCI'],CONFIGS["my_prefetcher"])
        entry = ROI_ORIGIN_STATS[trace][CONFIGS["my_prefetcher"]]
        
        entry['Delta IPCI'] = entry['IPCI'] - max_ipci
        if(best_ipc):
            best_prefetcher_entry = ROI_ORIGIN_STATS[trace][best_ipc]
            best_prefetcher_entry['Delta IPCI'] = max_ipci - entry['IPCI'] 
   
# def record_results(sort_item=None):
    # print(CONFIGS["stats_dir"] + '/'+CONFIGS["output_name"] + '.csv')
    # output stats as csv file
    # print(ROI_ORIGIN_STATS)
    
    
    # res_name = CONFIGS["stats_dir"] + '/'+ str(CONFIGS["core_num"]) + "core_" + CONFIGS["output_name"] + "_"+CONFIGS["benchmark"] +"_"+ CONFIGS["insts_num"] + '.csv'
    # print(res_name)
    
    # sort_stat={}
    # # print(sort_item)
    # if(sort_item):
    #     for trace in CONFIGS["output_workloads"] +['Average']:
    #         if(sort_item=="output_prefetchers"):
    #             sort_stat[trace] = CONFIGS["output_prefetchers"]
    #             continue
    #         entry = ROI_ORIGIN_STATS[trace]
    #         sort_prefetchers = {}
    #         for prefetcher in  entry:
    #             # print(trace, prefetcher, entry[prefetcher]["IPC"], entry[prefetcher][sort_item])
    #             if(entry[prefetcher][sort_item] == "-"):
    #                 sort_prefetchers[prefetcher] = 0
    #             else:
    #                 sort_prefetchers[prefetcher] = float(entry[prefetcher][sort_item])
    #             # print(entry[prefetcher][sort_item], entry[prefetcher]["IPC"])
            
    #         # print(sort_prefetchers)
    #         sort_prefetchers = sorted(sort_prefetchers.items(), key=lambda x:x[1], reverse=True)
    #         # print(sort_prefetchers)
    #         sort_prefetchers =[prefetcher[0] for prefetcher in sort_prefetchers]
    #         sort_stat[trace] = sort_prefetchers
    # else:
    #     sort_stat = ROI_ORIGIN_STATS
    
    # if(sort_item=="output_prefetchers"):
    #     sort_stat[trace] = CONFIGS["output_prefetchers"]
    # # print(CONFIGS["output_prefetchers"])
    #     # print(ROI_ORIGIN_STATS[trace]["no"])
    # # print(sort_stat)
    # # exit()
    
    
    
    # with open(res_name, 'w') as f:
    #     print(','.join(['Trace', 'Prefetcher'] + CONFIGS["output_metrics"]), file=f)
    #     row = []
    #     already_trace=[]
    #     for trace in CONFIGS["output_workloads"] +['Average']:
    #         # print(ROI_ORIGIN_STATS[trace]["no"])
    #         # print(already_trace)
    #         row.append(trace) 
    #         first_trace = True 
    #         for prefetcher in sort_stat[trace] :
    #             if(trace not in ROI_ORIGIN_STATS or prefetcher not in ROI_ORIGIN_STATS[trace] or prefetcher not in CONFIGS["output_prefetchers"]):
    #                 continue
    #             row.append(prefetcher)
    #             entry = ROI_ORIGIN_STATS[trace][prefetcher] 
    #             for field in CONFIGS["output_metrics"]:
    #                 # row.append(entry[field])    
    #                 if( field =="Each IPC"):
    #                     row.append(('%.30s' % entry[field]) )
    #                 else:
    #                     row.append(entry[field])
            
    #             # if(first_trace):
    #             #     first_trace = False
    #             # else:
    #             #     row[0]=" "
             
    #             data = ','.join([str(x) for x in row])
    #             print(data, file=f)
    #             for field in CONFIGS["output_metrics"]:
    #                 row.pop()
    #             row.pop()
    #         row.pop()
            
def record_results(sort_item=None):
    res_name = CONFIGS["stats_dir"] + '/'+ CONFIGS["date"] + '.csv'
    print(res_name)
    fig_stat_name = CONFIGS["stats_dir"]+ "_figs" + '/' + CONFIGS["date"] + '.csv'
    
    sort_stat={}
    #sort_stat的第一层键值为trace，第二层键值为prefetcher
    
    if(sort_item):
        for trace in CONFIGS["output_workloads"] +['Average']:
            if(sort_item=="output_prefetchers"):
                sort_stat[trace] = CONFIGS["output_prefetchers"]
                continue
            entry = ROI_ORIGIN_STATS[trace]
            sort_prefetchers = {}
            for prefetcher in  entry:
                if(prefetcher not in CONFIGS["output_prefetchers"]):
                    continue
                # print(trace, prefetcher, entry[prefetcher]["IPC"], entry[prefetcher][sort_item])
                if(entry[prefetcher][sort_item] == "-"):
                    sort_prefetchers[prefetcher] = 0
                else:
                    sort_prefetchers[prefetcher] = float(entry[prefetcher][sort_item])
                # print(entry[prefetcher][sort_item], entry[prefetcher][sort_item])
            
            # print(sort_prefetchers)
            sort_prefetchers = sorted(sort_prefetchers.items(), key=lambda x:x[1], reverse=True)
            # print(sort_prefetchers)
            sort_prefetchers =[prefetcher[0] for prefetcher in sort_prefetchers]
            sort_stat[trace] = sort_prefetchers
            if(len(sort_stat[trace]) != len(CONFIGS["output_prefetchers"])):
                #print(trace)
                diff = list(set(CONFIGS["output_prefetchers"]) - set(sort_stat[trace]))
                #print(diff)
                # print(sort_stat[trace])
                # print(CONFIGS["output_prefetchers"])
                # assert(0)
            
            # print(trace, sort_stat[trace])
    else:
        sort_stat = ROI_ORIGIN_STATS
    
    # if(sort_item=="output_prefetchers"):
    #     sort_stat[trace] = CONFIGS["output_prefetchers"]
       
    with open(fig_stat_name, 'w') as f:
        
        print(','.join(['Trace'] + sort_stat[trace] * len(CONFIGS["output_metrics"])), file=f)        
        title_metric = []
        row = []
        already_trace=[]
        for field in CONFIGS["output_metrics"]:
            title_metric = title_metric + ([field]*len(sort_stat[trace]))       
            #print(title_metric)
            #带有title的metric，每一个mertic有4个,对应不同的prefetcher
        
        print(','.join(['Trace'] + title_metric ), file=f)
        for trace in CONFIGS["output_workloads"] +['Average']:
            if(trace not in ROI_ORIGIN_STATS):
                print(trace,  "no trace")
                #assert(0)
                continue
            
            row.append(trace) 
            first_trace = True 
            
            line = []
            # print(trace)
            for field in CONFIGS["output_metrics"]:
                for prefetcher in sort_stat[trace] :
                   
                    if(prefetcher not in ROI_ORIGIN_STATS[trace] or prefetcher not in CONFIGS["output_prefetchers"] ):
                        print(trace, prefetcher, "no trace")
                        print("ROI_ORIGIN_STATS", prefetcher in ROI_ORIGIN_STATS[trace])
                        print("CONFIGS" ,CONFIGS["output_prefetchers"])
                        assert(0)
                        continue
                    
                    metric_value = ROI_ORIGIN_STATS[trace][prefetcher][field]
                    # print(trace,prefetcher,metric_value)
                    # line.append(metric_value)
                    if(field == "IPCI"):
                        line.append(metric_value)
                    else:
                        line.append(metric_value)
            print(','.join([trace] + [str(value) for value in line] ), file=f)

    
    # exit()
    
    with open(res_name, 'w') as f:
        print(','.join(['Trace', 'Prefetcher'] + CONFIGS["output_metrics"]), file=f)
        row = []
        already_trace=[]
        # for trace in CONFIGS["output_workloads"] +['Average']:
        
        for trace in ['Average']:
            # print(ROI_ORIGIN_STATS[trace]["no"])
            # print(already_trace)
            row.append(trace) 
            first_trace = True 
            
            for prefetcher in sort_stat[trace] :
           
                if(trace not in ROI_ORIGIN_STATS or prefetcher not in ROI_ORIGIN_STATS[trace] or prefetcher not in CONFIGS["output_prefetchers"]):
                    
                    print(trace, prefetcher)
                    print("exist: ",(trace not in ROI_ORIGIN_STATS), (prefetcher not in ROI_ORIGIN_STATS[trace]), (prefetcher not in CONFIGS["output_prefetchers"]))
                    assert(0)
                row.append(prefetcher)
                entry = ROI_ORIGIN_STATS[trace][prefetcher] 
                for field in CONFIGS["output_metrics"]:
                    # row.append(entry[field])    
                    if( field =="Each IPC"):
                        row.append(('%.30s' % entry[field]) )
                    else:
                        row.append(entry[field])
            
                # if(first_trace):
                #     first_trace = False
                # else:
                #     row[0]=" "
             
                data = ','.join([str(x) for x in row])
                print(data, file=f)
                for field in CONFIGS["output_metrics"]:
                    row.pop()
                row.pop()
            row.pop()

#处理文件
def process_file(var):
    print("var: ",var)
    if isinstance(var, str):#用来检查var是否是一个字符串
        #bingo_setting(f"all_benchmarks/{var}")
        bingo_setting(f"{var}")
    else:
        #bingo_setting(f"all_benchmarks/{var[0]}",var[1])
        bingo_setting(f"{var[0]}",var[1])

#对于p = multiprocessing.Process(target=process_file, args=(filename,))
#相当于每个进程调用process_file函数，参数为filename
def traverse_files_and_parse(filenames):
    processes = []
    #print("tt")
    
    for filename in filenames:
        print(filename)
        p = multiprocessing.Process(target=process_file, args=(filename,))
        p.start()
        processes.append(p)
    for p in processes:
        #p.join() 方法的作用是阻塞主进程，
        #直到进程 p 执行完成。主进程会等待进程 p 结束后才会继续执行下面的代码。
        p.join()

def traverse_files_and_call_function(directory):
    processes = []
    config_path = CURRENT_DIRECTORY + "/../settings/" + directory
    filenames = [f.name.replace(".json", "") for f in os.scandir(config_path) if f.is_file()]
    # print(filenames)
    # exit()
    num_cores = multiprocessing.cpu_count()
    max_processes = 10  # 指定最大进程数
    processes = []     # 用于存储所有已经启动的进程对象
    for filename in filenames:
        p = multiprocessing.Process(target=process_file, args=((filename,"output_prefetchers"),))
        p.start()
        processes.append(p)
        
        # 如果已经达到最大进程数，则等待它们全部完成后再启动下一批进程
        if len(processes) == max_processes:
            for p in processes:
                p.join()
            processes = []
            
    # 等待剩余的进程完成
    for p in processes:
        p.join()
              
def bingo_setting(config_name: str, sort_item: Any = None) -> None:
    
    
    global ROI_ORIGIN_STATS, CONFIGS
    ROI_ORIGIN_STATS.clear()
    CONFIGS.clear()
    #config_path = CURRENT_DIRECTORY+"/../settings/"+config_name+".json"
    #json路径
    config_path = CURRENT_DIRECTORY+"/"+config_name+".json"
    read_config(config_path)
    parse_origin_results()
    cal_final_results()
    
    if(sort_item):
            # print(sort_item)
        record_results(sort_item)
    else:
        record_results()
        
    # record_results()
    # record_results()
    # print(CONFIGS)
    # print(ROI_ORIGIN_STATS)      
    
def bingo_evaluate():
    
    # traverse_files_and_call_function("spec_all")


#     187 traces(93 spec2006 94spec2017 )  91 memory-intensive(46 spec2006 ,45 spec2017)   96 no memory-intensive
#     
    # exit()
    var=[
        
        
    # ("1core_all_max_compare_80M", "output_prefetchers"),
    # ("1core_all_PQ_32_compare_80M", "output_prefetchers"),
    # ("4core_all_PQ_32_compare_80M", "output_prefetchers"),
    #  ("1core_bingo_analyse_80M", "output_prefetchers"),  
     
    # ("1core_mpki_spec06_80M", "output_prefetchers"),  
    # ("1core_mpki_spec17_80M", "output_prefetchers"),  
    # ("1core_mpki_specall_80M", "output_prefetchers"),  
     

    #  ("1core_PQ_32_compare_spec17_80M", "output_prefetchers"),
    
    
    
    # ("1core_all_miss_rate_80M", "output_prefetchers"),
    
    #("1core_spec_compare_all_80M", "output_prefetchers"),
    #("1core_spec2k17_compare_mem_tense","output_prefetchers"),
     ("1core_mpref_all","output_prefetchers"),
    #  (f"1core_hyperion_tmp","output_prefetchers"),
    #  (f"1core_hyperion_tmp","output_prefetchers"),

    # (f"1core_{sys.argv[1]}_compare_all_80M","output_prefetchers"),

    # ("1core_rate", "output_prefetchers"),
    
    
    # ("1core_PQ_32_compare_epoch_80M", "output_prefetchers"),  
    # ("1core_PQ_32_compare_pht_80M", "output_prefetchers"), 
    
    # ("1core_pht_size", "output_prefetchers"), 
    
    
    # ("1core_merge_size", "output_prefetchers"), 

    # ("1core_PQ_32_cloudsuit_mpki_80M", "output_prefetchers"),
    
    #  ("1core_PQ_32_cloudsuit_cassandra_80M", "output_prefetchers"),
    #  ("1core_PQ_32_cloudsuit_classification_80M", "output_prefetchers"),
    #  ("1core_PQ_32_cloudsuit_cloud9_80M", "output_prefetchers"),
    #  ("1core_PQ_32_cloudsuit_nutch_80M", "output_prefetchers"),
    #  ("1core_PQ_32_cloudsuit_streaming_80M", "output_prefetchers"),
    #  ("1core_PQ_32_cloudsuit_all_80M", "output_prefetchers"),
    
    

    ]
    # var=[
    #     "1core_all_compare_80M", 
    #     "1core_all_hpsp_epoch_80M",
    # ]
    # print(len(var),type(var))
    
    traverse_files_and_parse(var);
    # bingo_setting("spec_all/1core_all_hpsp_epoch_80M","output_prefetchers")
if __name__ == "__main__":
    
    bingo_evaluate()