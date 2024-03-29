import os
import math
import re
from collections import Counter
import multiprocessing
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import csv
import glob

pattern = r"pc:(\d+).*offset:(\d+) baddr:(\d+) vpaddr:(\d+)"
# directory = "./outputsum/output1158/spec2k17/-vbertimix4-no---436.cactusADM-1804B.champsimtrace.xz"
directory = "./outputsum/output1158/spec2k17/-vberti_trace-no---605.mcf_s-484B.champsimtrace.xz"

page1 = []
addr1 = []
last_addr = 0
delta = []
ips = Counter()
vps = Counter()
start = 0
cnt_addr = 0
with open(directory,'r') as file:
    lines = file.readlines()
    for i in range(len(lines)):
        line = lines[i]
        pattern_match = re.search(pattern, line)
        if pattern_match:
            ip = int(pattern_match.group(1))
            page = int(pattern_match.group(4))
            addr = int(pattern_match.group(3))
            offset = int(pattern_match.group(2))
            # pc:4254020 offset:18 baddr:415890 vpaddr:6498
            if(start == 1):
                ips[ip] += 1
                vps[page] += 1
                cnt_addr += 1
            if(ip == 4206610 and page == 6498 and addr == 415890 ):
                start = 1
            
            
            if(cnt_addr == 30):
                print(len(ips))
                print("\n")
                print(len(vps))
                break