import json
import sys

# 从命令行参数获取新的output_prefetchers数组，跳过第一个参数（脚本名称）
# 分别获取命令行参数
# new_values = sys.argv[1:-2]  # 倒数第二个参数之前的所有参数为output_prefetchers的新值
# new_date = sys.argv[-2]  # 倒数第二个参数为date的新值
# new_version = sys.argv[-1]  # 最后一个参数为version的新值
new_values = sys.argv[1:-1]  # 倒数第二个参数之前的所有参数为output_prefetchers的新值
new_date = sys.argv[-1]  # 倒数第二个参数为date的新值

# 文件路径
traces = ["spec","gap","ligra","spec2k06","spec2k17"]

for trace in traces:
# 读取原始JSON数据
    file_path = f'analysis_py/evaluation3/sensitive_design/1core_1pref_{trace}.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
    # 更新output_prefetchers的值
    data['output_prefetchers'] = new_values
    # 更新date的值
    data['date'] = new_date
    # 更新version的值
    if(f"{trace}" == "spec2k06" or f"{trace}" == "spec2k17" ):
        data['results_dir'] = [f"outputsum/output{new_date}/spec"]
    else:
        data['results_dir'] = [f"outputsum/output{new_date}/{trace}"]

    # 将修改后的数据写回文件
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
