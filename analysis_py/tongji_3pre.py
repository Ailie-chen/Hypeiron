import os
import re
from collections import Counter


# 指定路径进行处理
path = "outputsum/output0724_test/spec2k17/"

# 将结果写入文本文件
output_file = "outputsum/output0724_test/spec2k17/result.txt"

def extract_numbers(line):
    # 使用正则表达式提取数字
    match = re.search(r'\d+', line)
    if match:
        return int(match.group())
    return None

def process_file(file_path):
    ip_nums = []
    bop_nums = []
    pages_nums = []
    
    with open(file_path, 'r') as file:
        for line in file:
            if 'IP NUMS' in line:
                num = extract_numbers(line)
                if num is not None and num > 0 and num <= 32:
                    ip_nums.append(num)
            elif 'BOP NUMS' in line:
                num = extract_numbers(line)
                if num is not None and num > 0 and num <= 32:
                    bop_nums.append(num)
            elif 'PAGES NUMS' in line:
                num = extract_numbers(line)
                if num is not None and num > 0 and num <= 32:
                    pages_nums.append(num)
    
    return ip_nums, bop_nums, pages_nums

def process_directory(path):
    ip_counter = Counter()
    bop_counter = Counter()
    pages_counter = Counter()
    
    total_sum = 0

    ip_sum = 0
    bop_sum = 0
    pages_sum = 0

    with open(output_file, 'w') as file_out:
        pass

    # 将结果写入文本文件
    with open(output_file, 'a') as file_out:
    
        for root, dirs, files in os.walk(path):
            for file in files:
                file_out.write(file+'\n')
                file_path = os.path.join(root, file)
                ip_counter = Counter()
                bop_counter = Counter()
                pages_counter = Counter()
                ip_nums, bop_nums, pages_nums = process_file(file_path)
                
                ip_counter.update(ip_nums)
                bop_counter.update(bop_nums)
                pages_counter.update(pages_nums)

                ip_sum = sum(element * count for element, count in ip_counter.items())
                bop_sum = sum(element * count for element, count in bop_counter.items())
                pages_sum = sum(element * count for element, count in pages_counter.items())
                file_out.write("IP NUMS fenbu:\n")
                file_out.write(str(ip_counter) + '\n')
                file_out.write("IP NUMS all:"+str(ip_sum)+'\n')
                file_out.write("BOP NUMS fenbu:\n")
                file_out.write(str(bop_counter) + '\n')
                file_out.write("BOP NUMS all:"+str(bop_sum)+'\n')
                file_out.write("PAGES NUMS fenbu:\n")
                file_out.write(str(pages_counter) + '\n')
                file_out.write("PAGES NUMS all:"+str(pages_sum)+'\n')
                
    
    return None

process_directory(path)
