import os

# folder_path = "./output/spec2k17/"  # 文件夹路径
# keywords = ["403.gcc","vberti"]  # 文件名中包含的关键词

folder_path = "./outputsum/output0703/spec2k17/"  # 文件夹路径
keywords = ["403.gcc","vberti"]  # 文件名中包含的关键词
output_file = "./analysis_py/output.txt"  # 输出文件路径

# 遍历文件夹中的文件
with open(output_file, "a") as out_file: #w覆盖写入，a追加写入
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # 仅处理包含关键词的文件
        if all(keyword in file_name for keyword in keywords):
            out_file.write(f"\n")
            out_file.write(f"{file_name}:\n")
            with open(file_path, "r") as file:
                # 逐行读取文件内容
                for line_number, line in enumerate(file, 1):
                    if ("CPU 0 cumulative IPC:") in line:
                        out_file.write(f"Line {line_number}: {line.strip()}\n")
                    if line.startswith("L1D TOTAL     ACCESS"):
                        out_file.write(f"Line {line_number}: {line.strip()}\n")
                    if line.startswith("L1D LOAD      ACCESS"):
                        out_file.write(f"Line {line_number}: {line.strip()}\n")
                    if line.startswith("L1D PREFETCH  ACCESS"):
                        out_file.write(f"Line {line_number}: {line.strip()}\n")
                    if line.startswith("L1D USEFUL LOAD PREFETCHES"):
                        out_file.write(f"Line {line_number}: {line.strip()}\n")
                    if line.startswith("L1D TIMELY PREFETCHES"):
                        out_file.write(f"Line {line_number}: {line.strip()}\n")
                    if line.startswith("L1D AVERAGE MISS LATENCY"):
                        out_file.write(f"Line {line_number}: {line.strip()}\n")