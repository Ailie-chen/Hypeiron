import os
import re

folder_path1 = "./output/spec2k17/"  # 文件夹A的路径
folder_path2 = "./outputsum/output0703/spec2k17/"  # 文件夹A的路径
keywords1 = ["ip_stride", "ipcp_isca2020", "mlop_dpc3", "vberti"]  # 关键词1列表
keywords2 = ["vbertim"]  # 关键词1列表
ipc_values = {keyword: [] for keyword in keywords1 + keywords2}  # 存储IPC值的字典

# 读取./traces/spec2k17_name.txt中的文件名列表
with open("./traces/spec2k17_name.txt", 'r') as file:
    file_names = file.read().splitlines()

for keyword in keywords1:
    # 遍历文件夹A中的文件
    for file_name in os.listdir(folder_path1):
        # 检查文件名是否同时包含关键词和文件名
        if keyword in file_name:
            file_path = os.path.join(folder_path1, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
                # 使用正则表达式匹配IPC值列表
                ipc_list = re.findall(r"CPU 0 cumulative IPC:(.*?)instructions:", file_content)
                if ipc_list:
                    ipc_values[keyword].extend(ipc_list)
                else:
                    ipc_values[keyword].append("IPC值未找到")

for keyword in keywords2:
    # 遍历文件夹A中的文件
    for file_name in os.listdir(folder_path2):
        # 检查文件名是否同时包含关键词和文件名
        if "vberti" in file_name:
            file_path = os.path.join(folder_path2, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
                # 使用正则表达式匹配IPC值列表
                ipc_list = re.findall(r"CPU 0 cumulative IPC:(.*?)instructions:", file_content)
                if ipc_list:
                    ipc_values[keyword].extend(ipc_list)
                else:
                    ipc_values[keyword].append("IPC值未找到")


# 输出每个文件名对应的5个IPC值到文本文件
output_file = "./outputsum/ipc_results.txt"
with open(output_file, 'w', encoding='utf-8') as file:
    for file_name in file_names:
        ipc_results = []
        for keyword in keywords1 + keywords2:
            ipc_list = ipc_values.get(keyword, ["关键词未找到"])
            ipc_results.append(ipc_list.pop(0) if ipc_list else "IPC值未找到")
        file.write(f"{file_name}: {', '.join(ipc_results)}\n")