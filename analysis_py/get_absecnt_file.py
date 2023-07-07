import os

folder_path = "./outputsum/output0703/spec2k17/"  # 需要进行对比的文件夹
text_file = "./traces/spec2k17_name.txt"  # traces文件名

# 获取文本文件中的文件名
with open(text_file, "r") as file:
    text_file_names = set(file.read().splitlines())

# 遍历文本文件中的文件名，找出在另一个文件夹中没有包含该文件名的文件，并输出
for file_name in text_file_names:
    found = False
    for root, dirs, files in os.walk(folder_path):
        for name in files + dirs:
            if file_name in name and len(name) > len(file_name):
                found = True
                break
        if found:
            break
    if not found:
        print(file_name)
