import json
import os
from bingo_evaluate import bingo_evaluate

# 定义要更改的日期列表
dates_modify=['0703','0704','0705','0706','0708','0709','0710',
              '0711','0712','0713','0714','0715','0716','0717','0718']
#dates_modify=['0703']
# 遍历日期列表
for date in dates_modify:
    # 打开json文件
    with open('analysis_py/1core_spec2k17_compare_mem_tense.json', 'r') as json_file:
        data = json.load(json_file)

    # 修改json文件中的"date"和"results_dir"
    data['date'] = date
    data['results_dir'] = ["outputsum/output0702/spec2k17","outputsum/output"+date+"/spec2k17"]

    # 保存修改后的json文件
    with open('analysis_py/1core_spec2k17_compare_mem_tense.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    # 运行bingo_evaluate()函数
    bingo_evaluate()
