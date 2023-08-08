# import os
# import shutil

# # 指定的一级子文件夹列表
# #target_folders = ['0702']

# target_folders = ['0702','0703','0706','0713','0714','0715','0716','0717','0718']
# # 指定的二级子文件夹
# target_subfolder = 'spec2k17'
# # 指定要查找的文件名称的部分字符串
# target_file_name = "605.mcf_s-484B.champsimtrace.xz"
# # 目的路径
# destination_path = 'outputsum/output0718_test/compare/'

# # 创建目的路径（如果不存在）
# os.makedirs(destination_path, exist_ok=True)
# # 删除目的路径（如果存在）

# # 创建空的目的路径
# #os.makedirs(destination_path)

# # 遍历一级子文件夹
# for folder in target_folders:
#     # 构建一级子文件夹的完整路径
#     folder_path = os.path.join('outputsum', 'output'+folder)
#     # 构建二级子文件夹的完整路径
#     subfolder_path = os.path.join(folder_path, target_subfolder)
#     # 遍历二级子文件夹
#     for root, dirs, files in os.walk(subfolder_path):
#         # 检查文件名称是否包含目标字符串
#         for file in files:
            
#             if target_file_name in file:
#                 # 构建源文件的完整路径
#                 source_file_path = os.path.join(root, file)               
#                 # 构建目的文件的完整路径
#                 destination_file_name = folder +'_'+ target_file_name
#                 destination_file_path = os.path.join(destination_path, destination_file_name)
#                 print(source_file_path)
#                 print(destination_file_path)
#                 # 复制文件到目的路径
#                 shutil.copy(source_file_path, destination_file_path)
import os
import re

target_file_names = ["654.roms_s-294B.champsimtrace.xz", 
                    "623.xalancbmk_s-700B.champsimtrace.xz",
                    "623.xalancbmk_s-592B.champsimtrace.xz",
                    "623.xalancbmk_s-10B.champsimtrace.xz",
                    "620.omnetpp_s-874B.champsimtrace.xz",
                    "620.omnetpp_s-141B.champsimtrace.xz",
                    "619.lbm_s-3766B.champsimtrace.xz",
                    "619.lbm_s-2766B.champsimtrace.xz"]
target_folders = ['0702', '0703', '0704','0705','0706', '0713', '0714', '0715', '0716', '0717', '0718','0722','0723','0724']
target_subfolder = 'spec2k17'
res_path = 'outputsum/output0724_test/compare/'
os.makedirs(res_path, exist_ok=True)
inform1 = ['CPU 0 cumulative IPC',
        'L1D TOTAL     ACCESS',
        'L1D LOAD      ACCESS',
        'L1D RFO       ACCESS',
        'L1D PREFETCH',
        'L1D AVERAGE MISS LATENCY',
        'L2C DATA LOAD MPKI:',
        'L2C TOTAL     ACCESS',
        'L2C LOAD      ACCESS',
        'L2C PREFETCH  ACCESS',
        'L2C AVERAGE MISS LATENCY:']
inform2 = [
            'CPU 0 cumulative IPC',
            'L1D',
            'L2C'
]
for a in target_file_names:
    result_file_path = os.path.join(res_path,a + '.txt')
    result_file = open(result_file_path, 'w')
    for folder in target_folders:
        folder_path = os.path.join('outputsum', 'output' + folder)
        subfolder_path = os.path.join(folder_path, target_subfolder)        
        # 遍历文件夹中的文件
        for file_name in os.listdir(subfolder_path):
            if a in file_name:
                result_file.write(folder+'\n')
                file_path = os.path.join(subfolder_path, file_name)
                with open(file_path, 'r') as file:
                    for line in file:
                        p_ipc= r"CPU \d+ cumulative IPC: (\d+\.\d+)"
                        match8 = re.search(p_ipc,line)
                        if(match8):
                            result_file.write('IPC: '+match8.group(1)+'\n')

                        p_l1dloadmiss = r'L1D LOAD\s+ACCESS:\s+\S+\s+HIT:\s+\S+\s+MISS:\s+\S+\s+HIT %:\s+\S+\s+MISS %:\s+(\S+)'
                        match1 = re.search(p_l1dloadmiss,line)
                        if(match1):
                            result_file.write('L1D LOAD MISS: '+match1.group(1)+' ')

                        p_l1d_pref = r'L1D PREFETCH\s+REQUESTED:\s+\S+\s+ISSUED:\s+(\S+)\s+USEFUL:\s+\S+\s+USELESS:\s+(\S+)'
                        match2 = re.search(p_l1d_pref,line)               
                        if(match2):
                            result_file.write('L1D PREF_USEFUL: '+match2.group(1)+' '+'L1D PREF_USELESS: '+match2.group(2)+' ')

                        p_l1d_2_llc = r'L1D USEFUL LOAD PREFETCHES:\s+\S+\s+PREFETCH ISSUED TO LOWER LEVEL:\s+(\S+)'
                        match3 = re.search(p_l1d_2_llc,line)
                        if(match3):
                            result_file.write('L1D TO LowerLevel: '+match3.group(1)+' ')

                        p_l1d_mp= r'L1D AVERAGE MISS LATENCY:\s+(\S+)'
                        match4 = re.search(p_l1d_mp,line)
                        if(match4):
                            result_file.write('L1D MP: '+match4.group(1)+'\n')

                        p_l2cload_miss= r'L2C LOAD\s+ACCESS:\s+\S+\s+HIT:\s+\S+\s+MISS:\s+\S+\s+HIT %:\s+\S+\s+MISS %:\s+(\S+)'
                        match5 = re.search(p_l2cload_miss,line)
                        if(match5):
                            result_file.write('L2C LOAD MISS: '+match5.group(1)+' ')

                        p_l2c_pref_miss= r'L2C PREFETCH\s+ACCESS:\s+\S+\s+HIT:\s+\S+\s+MISS:\s+\S+\s+HIT %:\s+\S+\s+MISS %:\s+(\S+)'
                        match6 = re.search(p_l2c_pref_miss,line)
                        if(match6):
                            result_file.write('L2C PREF MISS: '+match6.group(1)+' ')
                        
                        p_l2c_mp= r'L2C AVERAGE MISS LATENCY:\s+(\S+)'
                        match7 = re.search(p_l2c_mp,line)
                        if(match7):
                            result_file.write('L2C MP: '+match7.group(1)+'\n')
                        

    result_file.close()
