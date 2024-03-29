import pickle 
from collections import Counter
path_ip = "./outputsum/output1024/pickles/ip.pkl"
path_page = "./outputsum/output1024/pickles/page.pkl"
ip_pages = []
page_ips = []
NUM_THRESHOLD = 8
DISTANCE_THRESHOLD = 16

with open(path_ip, 'rb') as f:
    while True:
        try:
            # 每次循环尝试加载一个对象
            ip_page= pickle.load(f)
            ip_pages.append(ip_page)
        except EOFError:
            # 文件末尾到达，结束循环
            break
with open(path_page, 'rb') as f:
    while True:
        try:
            # 每次循环尝试加载一个对象
            page_ip= pickle.load(f)
            page_ips.append(page_ip)
        except EOFError:
            # 文件末尾到达，结束循环
            break
###统计每个page被驱逐前平均访问的信息量
Lpage_sum = {}
Lpage_ave = Counter()
for item in page_ips:
    page, ip_cnt_arr = item
    if page not in Lpage_sum:        
        Lpage_sum[page] = []
    Lpage_sum[page].append(sum([row[1] for row in ip_cnt_arr]))
for page in Lpage_ave:
    Lpage_ave[page] = int(sum(Lpage_sum[page]) / len(Lpage_sum[page]))

ip_page_dict={}
for item in ip_pages:
    ip, page_cnt_arr = item
    ip_cnt = sum([row[1] for row in page_cnt_arr])
    if ip_cnt < NUM_THRESHOLD:
        if ip_cnt not in ip_page_dict:
            ip_page_dict[ip_cnt] = Counter()
        for page_cnt in page_cnt_arr:
            page, cnt = page_cnt
            ip_page_dict[ip_cnt][Lpage_ave[page]] += cnt

for cnt, values in ip_page_dict:
    print(cnt)
    for item, cnt in values:
        print(item, cnt)