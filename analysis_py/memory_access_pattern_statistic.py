
import os
import math
import re
from collections import Counter
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import csv
pattern = r"pc:(\d+) .* offset:(\d+) baddr:(\d+) vpaddr:(\d+)"

def parse_file(path, output_directory_txt,output_directory_png):
    page_addr_counter = Counter()
    ip_addr_counter = Counter()
    offset_counter = Counter()
    block_addr_counter = Counter()
    num_lines = 0
    output_content = []
    most_page_access = 0
    most_ip_access = 0

    with open(path, 'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i]
            # If line starts with a digit
            pattern_match = re.match(pattern, line)
            if pattern_match:
                num_lines += 1
                ip_addr_counter[int(pattern_match.group(1))] += 1
                offset_counter[int(pattern_match.group(2))] += 1
                block_addr_counter[int(pattern_match.group(3))] += 1
                page_addr_counter[int(pattern_match.group(4))] += 1
                
            if(len(block_addr_counter) >= 768):
                break

    filename = os.path.basename(path)
    result_name = re.search(r'---(.*)\.champsimtrace\.xz', filename).group(1)
    output_path = os.path.join(output_directory_txt, f"{result_name}.txt")

    pages_fre = []
    ip_fre = []
    page_counter = 0
    ip_counter = 0
    len_pages = 0
    len_ip = 0
    page_c_point=0
    page_cover=0
    ip_c_point=0
    ip_cover=0
    len_pages = len(page_addr_counter)
    len_ip = len(ip_addr_counter)
    with open(output_path, 'w') as file:
        file.write(f"Total number of lines starting with a digit: {num_lines}\n")

        len_pages = len(page_addr_counter)
        len_ip = len(ip_addr_counter)

        file.write(f"Page distribution:{len_pages}\n")
        file.write(f"Ip distribution:{len_ip}\n")

        for page, count in page_addr_counter.most_common():
            if((page_cover/num_lines < 0.9) and ((page_cover+count)/num_lines >= 0.9)):
                file.write(f"90% cover point of page is {page_counter}\n")
                page_c_point = page_counter + 1
            page_cover += count
            page_counter += 1
        page_counter = 0

        for pc, count in ip_addr_counter.most_common():
            if((ip_cover/num_lines < 0.9) and ((ip_cover+count)/num_lines >= 0.9)):
                file.write(f"90% cover point of ip is {ip_counter}\n")
                ip_c_point = ip_counter + 1
            ip_cover += count
            ip_counter += 1
        ip_counter=0
        
        file.write(f"Page distribution:{len_pages}\n")
        for page, count in page_addr_counter.most_common():
            file.write(f"{page}:{count}\n")
            if(page_counter < 20):
                most_page_access += count
            page_counter += 1
            # if(count > 0):
            #     pages_fre.append(count)
        file.write(f"Ip distribution:{len_ip}\n")
        for pc, count in ip_addr_counter.most_common():
            file.write(f"{pc}:{count}\n")
            if(ip_counter < 20):
                most_ip_access += count
            ip_counter += 1
    file.close()
    # 1:pages 2:ip 3:approximate
    c_point_type=0
    if ((abs(page_c_point-ip_c_point)/max(page_c_point,ip_c_point)) < 0.1):
        c_point_type = 3
    elif(page_c_point < ip_c_point):
        c_point_type = 1
    else:
        c_point_type = 2
    return len_pages, len_ip, 100.0*most_page_access/num_lines, 100.0*most_ip_access/num_lines, c_point_type,num_lines

    

def main():
    directory = "./outputsum/output1021/spec2k17/"
    output_directory_txt = "./outputsum/output1021/statistic"
    output_directory_png = "./outputsum/output0729/spec2k19_statistic_png/"
    if not os.path.exists(output_directory_txt):
    # 如果目录不存在，则创建该目录
        os.makedirs(output_directory_txt)
    if not os.path.exists(output_directory_png):
    # 如果目录不存在，则创建该目录
        os.makedirs(output_directory_png)

    # with ThreadPoolExecutor() as executor:
    #     for filename in os.listdir(directory):
    #         if filename.endswith(".champsimtrace.xz"):
    #             executor.submit(parse_file, os.path.join(directory, filename), output_directory_txt,output_directory_png)
    len_pages_ip=[]
    c_point_page=0
    c_point_ip=0
    c_point_approximate=0
    sum_len_pages=0
    sum_len_ips=0
    low_page=[]
    high_page=[]
    low_ip=[]
    high_ip=[]
    hip_lpage=[]
    hpage_lip=[]
    for filename in os.listdir(directory):
        if filename.endswith(".champsimtrace.xz"):
            match_trace = re.search(r'---(.+)(\.champsimtrace\.xz|\.trace\.gz|\.trace\.xz)', filename)
            len_pages_ip.append((match_trace.group(1),parse_file(os.path.join(directory, filename), output_directory_txt,output_directory_png)))
    
    with open("./outputsum/output1021/all_statistic/all_traces.txt",'w') as file:
        len_pages_distribution=[0,0,0,0,0,0,0,0,0,0,0]
        len_ip_distribution=[0,0,0,0,0,0,0,0,0,0,0]
        
        pages_l20_percentage=0
        ip_l20_percentage=0
        for items in len_pages_ip:
            filename, item = items
            if(item[0] <= 100):
                low_page.append((filename,item[0],item[5]))
            else:
                high_page.append((filename,item[0],item[5]))
            if(item[1] <= 100):
                low_ip.append((filename,item[1],item[5]))
            else:
                high_ip.append((filename,item[1],item[5]))
            if(item[0]/item[1] > 10):
                hpage_lip.append((filename,item[0],item[1],item[5]))
            elif (item[1]/item[0] > 10):
                hip_lpage.append((filename,item[0],item[1],item[5]))
        file.write(f"low_pages num:{len(low_page)}\n")
        for item in low_page:
            file.write(f"{item}\n")

        file.write(f"high_pages num:{len(high_page)}\n")
        for item in high_page:
            file.write(f"{item}\n")

        file.write(f"low_ip num:{len(low_ip)}\n")
        for item in low_ip:
            file.write(f"{item}\n")

        file.write(f"high_ip num:{len(high_ip)}\n")
        for item in high_ip:
            file.write(f"{item}\n")

        file.write(f"hpage_lip num:{len(hpage_lip)}\n")
        for item in hpage_lip:
            file.write(f"{item}\n")

        file.write(f"hip_lpage num:{len(hip_lpage)}\n")
        for item in hip_lpage:
            file.write(f"{item}\n")
    file.close()
    with open("./outputsum/output1021/all_statistic/types.csv",'w',newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 写入多行数据
        writer.writerow(["trace_name","LOG2(pages/ips)","pages num","ips num","total accesses"])
        for items in len_pages_ip:
            filename, item = items
            row=[filename, math.log(item[0]/item[1]),item[0],item[1],item[5]]
            writer.writerow(row)
    with open("./outputsum/output1021/statistic/all_traces.txt",'w') as file:
        len_pages_distribution=[0,0,0,0,0,0,0,0,0,0,0]
        len_ip_distribution=[0,0,0,0,0,0,0,0,0,0,0]
        
        pages_l20_percentage=0
        ip_l20_percentage=0
        for items in len_pages_ip:
            filename, item = items
            sum_len_pages += item[0]
            sum_len_ips += item[1]
        file.write(f"average_pages:{sum_len_pages/187}\n")
        file.write(f"average_ips:{sum_len_ips/187}\n")
        for items in len_pages_ip:
            filename, item = items
            if(item[4] == 1):
                c_point_page += 1
            elif(item[4] == 2):
                c_point_ip += 1
            else:
                c_point_approximate += 1
            print(item[0],item[1])
            if(item[0] < 100):
                len_pages_distribution[math.floor(item[0]/10)] += 1
            else:
                len_pages_distribution[10] += 1
            if(item[1] < 100):
                len_ip_distribution[math.floor(item[1]/10)] += 1
            else:
                len_ip_distribution[10] += 1
            pages_l20_percentage += item[2]
            ip_l20_percentage += item[3]
        file.write(f"c_point_page:{c_point_page}\n")
        file.write(f"c_point_ip:{c_point_ip}\n")
        file.write(f"c_point_approximate:{c_point_approximate}\n")
        file.write(f"pages_l20_percentage:{pages_l20_percentage/187}\n")
        file.write(f"ip_l20_percentage:{ip_l20_percentage/187}\n")

        file.write("page_len_distribution:\n")
        for i in range(len(len_pages_distribution)):
            len_pages_distribution[i] =  len_pages_distribution[i]* 100.0 / 187
            sum_pages_distribution=0
            for j in range(i+1):
                sum_pages_distribution += len_pages_distribution[j]
            if(i <= 9):
                file.write(f"0-{i*10+10}:{sum_pages_distribution} \n")
            else:
                file.write(f"others:{sum_pages_distribution} \n")
        file.write("page_ip_distribution:\n")
        for i in range(len(len_ip_distribution)):
            len_ip_distribution[i] = len_ip_distribution[i] * 100.0 / 187
            sum_ip_distribution=0
            for j in range(i+1):
                sum_ip_distribution += len_ip_distribution[j]
            file.write(f"0-{i*10+10}:{sum_ip_distribution}\n")
    

if __name__ == "__main__":
    main()
