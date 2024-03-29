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
            # pc:4206610 delta and page
            # [(2181780218643, 34090315916), (23315077, 34090680214), (-31086765, 34090194483), 
            # (12, 34090194483), (14, 34090194484), (89, 34090194485), (118, 34090194487), 
            # (712, 34090194498), (6641, 34090194602), (7590, 34090194720), (15178, 34090194957), 
            # (30357, 34090195432), (60714, 34090196380), (121428, 34090198278), (242856, 34090202072), 
            # (485712, 34090209662), (971424, 34090224840), (1942849, 34090255197), (3885698, 34090315911), 
            # (7771397, 34090437339), (-15542789, 34090194483), (26, 34090194484), (89, 34090194485), (118, 34090194487),
            #  (712, 34090194498), (6641, 34090194602), (22770, 34090194957), (91078, 34090196381), (121437, 34090198278), (242874, 34090202073)]
            ###page:34090194483
            [2181772446954, 1, 1, -3, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 3, 1, -1, 7, -8, 9, 0, -1, 1, -12, 1, -2, -1, 0, 0, 0]
            ###page:34090194484
            # [2181772446982, 1, -2, 1, 29, 1, -2, 1, -29, 1, -2, 1, 29, 1, -2, 1, -29, 1, -2, 1, 29, 1, -2, 1, -29, 1, -2, 1, 29, 1]
            ###page:34090194485
            #[2181772447070, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1]
            ###page == 34090194487
            #[2181772447189, 1, -2, 1, 0, 1, -2, 1, -1, 1, 1, -2, 1, 0, 1, -2, 1, 0, 1, -2, 1, 0, 1, -2, 1, 0, 1, -2, 1, 0]
            ###page == 34090194498
            #[2181772447900, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1]
            ###page == 34090194602
            #[2181772454542, 1, -2, 1, 0, 1, -2, 1, 0, 1, -1, -1, 1, 1, -2, 1, 0, 1, -2, 1, 0, 1, -2, 1, 0, 1, -2, 1, 0, 1]
            ###page == 34090194720
            #[2181772462131, 1, -1, -1, 1, 0, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1]

            if(page == 34090680214):

                delta = addr - last_addr
                addr1.append(delta)
                cnt_addr += 1
                last_addr = addr
            
            if(cnt_addr == 30):
                print(addr1)
                break