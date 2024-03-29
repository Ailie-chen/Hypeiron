import os

# 设置文件夹路径
folder_path = './outputsum/output1126/spec2k17'

# 要替换的字符串
string_to_replace = 'hashed_perceptron-no-vbertimix3-no-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-no---'
string_new = 'hashed_perceptron-no-vbertimix3p-no-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core-no---'
# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if True: #string_to_replace in filename:
        # 构造新文件名
        new_filename = filename.replace(string_to_replace, string_new)
        # 构造完整的旧文件和新文件路径
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_filename)
        # 重命名文件
        os.rename(old_file, new_file)
        print(f'Renamed: {old_file} to {new_file}')
