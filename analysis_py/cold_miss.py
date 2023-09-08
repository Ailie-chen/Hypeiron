import os
import re
import sys

# 定义正则表达式模式
pc_pattern = r'pc:(\d+) .* baddr:(\d+) vpaddr:(\d+) M$'
pc_pattern_all = r'pc:(\d+) .* baddr:(\d+) vpaddr:(\d+)'
pref_pattern = r'(\d+) (\d+) (\d+)'
#pref_pattern = r'\[-?(\d+) (\d+) (\d+) \{(\d+) .*\} P\]'
#r'\[(\d+) \d+ \d+ \{(\d+) \} P\]'

# 获取输入文件夹路径
input_dir = 'outputsum/output0902/spec2k17'

# 获取输出文件夹路径pu
output_dir = 'outputsum/output0902/spec2k17_ana'

# 确保输出文件夹存在
os.makedirs(output_dir, exist_ok=True)

# 遍历输入文件夹中的所有文件
for filename in os.listdir(input_dir):
    if filename.endswith(".xz"):
        input_file_path = os.path.join(input_dir, filename)
        output_file_path = os.path.join(output_dir, filename.replace(".xz", "_ana.txt"))
        print(filename)

        # 初始化变量
        SUM_MISS = 0
        COLD_MISS = 0
        MISS_PREF = 0
        real_miss = 0
        vpaddr_history = []
        baddr_history = []
        pc_lines = []
        pref_vector = []

        # 读取文件内容
        with open(input_file_path, 'r') as file:
            lines = file.readlines()

        # 打开输出文件
        with open(output_file_path, 'w') as output_file:
            # 遍历文件中的每一行
            for line_number, line in enumerate(lines, start=1):
                if(line_number <= 100000):
                    # 匹配pc行
                    pc_match_b = re.match(pc_pattern_all, line)
                    if pc_match_b:
                        if(len(pref_vector) > 0):
                            pc_lines.append(pref_vector)
                            pref_vector = []
                        pref_vector.append(line_number) 
                        pref_vector.append(int(pc_match_b.group(1))) 
                        pref_vector.append(int(pc_match_b.group(2))) 
                        pref_vector.append(int(pc_match_b.group(3)))
                        pref_vector.append(1)
                    else:
                        pref_matches = re.findall(pref_pattern, line)
                        if(pref_matches):
                            for pref in pref_matches:
                                pref_vector.append(int(pref[1]))
                    pc_match = re.match(pc_pattern, line)
                    if pc_match:
                        pc = int(pc_match.group(1))
                        baddr = int(pc_match.group(2))
                        vpaddr = int(pc_match.group(3))

                        SUM_MISS += 1
                        
                        # 如果vpaddr不在历史记录中，或者baddr与历史记录中的不匹配，增加COLD_MISS计数
                        if (any(pair[1] == baddr for pair in vpaddr_history)) or (all(pair[0] != vpaddr for pair in vpaddr_history)):
                            COLD_MISS += 1
                        else:
                            found_miss_pref = 0

                            output_file.write(f"{line_number} {pc} {baddr} {vpaddr}\n")

                            # for pc_data in pc_lines[:-1]:
                            #     if ((pc_data[3] == vpaddr) or (pc_data[1] == pc)) and (line_number-pc_data[0])<=1000:
                            #         if (any( pref_addr == baddr for pref_addr in pc_data[5:])):
                            #             found_miss_pref = 1
                            # if(found_miss_pref == 1):
                            #     MISS_PREF += 1

                            for pc_data in pc_lines[:-1]:
                                if  (line_number-pc_data[0])<=1000 and (pc_data[3] == vpaddr or pc_data[1] == pc) and any( pref_addr == baddr for pref_addr in pc_data[5:]):
                                    found_miss_pref = 1
                                    break
                            if(found_miss_pref == 0):
                                output_file.write("page_start:\n")
                                for pc_data in pc_lines[:-1]:
                                    if pc_data[3] == vpaddr and (line_number-pc_data[0])<=1000:
                                        output_file.write(f"{pc_data}\n")
                                output_file.write("ip_start:\n")
                                for pc_data in pc_lines[:-1]:
                                    if pc_data[1] == pc and (line_number-pc_data[0])<=1000:
                                        output_file.write(f"{pc_data}\n")
                            output_file.write(" \n")

                            if found_miss_pref == 1 :
                                MISS_PREF += 1 
                            if found_miss_pref == 0 :
                                real_miss += 1 
                        # 更新vpaddr的历史记录
                        if all(pair[0] != vpaddr for pair in vpaddr_history):
                            vpaddr_history.append([vpaddr,baddr])

                    

            # 输出结果到文件
            output_file.write(f"SUM_MISS: {SUM_MISS}\n")
            output_file.write(f"COLD_MISS: {COLD_MISS}\n")
            output_file.write(f"MISS_PREF: {MISS_PREF}\n")
            output_file.write(f"REAL_MISS: {SUM_MISS-COLD_MISS-MISS_PREF}\n")

