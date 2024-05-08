import os

folder_path = "./traces/parsec/"  # 文件夹路径
output_file = "./traces/parsec_name.txt"  # 输出文件路径

# 遍历文件夹并获取文件名
file_names = []
for file_name in os.listdir(folder_path):
    file_names.append(file_name)

# 保存文件名到文本文件
with open(output_file, "w") as file:
    for file_name in file_names:
        file.write(file_name + "\n")

with open(output_file, "r") as file:
    file_names = file.read().splitlines()

# 对文件名进行排序
# sorted_file_names = sorted(file_names, key=lambda x: (int(x.split('.')[0]), x.split('-')[1]))

# # 将排序后的文件名重新写入文本文件
# with open(output_file, "w") as file:
#     file.write("\n".join(sorted_file_names))
