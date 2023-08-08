
import os
import re
from collections import Counter
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

def parse_file(path, output_directory_txt,output_directory_png):
    page_addr_counter = Counter()
    ip_addr_counter = Counter()
    num_lines_starting_with_digit = 0
    output_content = []

    with open(path, 'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i]
            # If line starts with a digit
            if re.match(r'^\d+', line):
                num_lines_starting_with_digit += 1
                parts = line.split()
                page_addr_counter[parts[0]] += 1
                ip_addr_counter[parts[1]] += 1
            # If line contains "L1D"
            elif re.match(r"^L1D$", line):
                output_content.extend(lines[i:i+25])

    filename = os.path.basename(path)
    result_name = re.search(r'---(.*)\.champsimtrace\.xz', filename).group(1)
    output_path = os.path.join(output_directory_txt, f"{result_name}.txt")

    pages_fre = []
    ip_fre = []
    with open(output_path, 'w') as file:
        file.write(f"Total number of lines starting with a digit: {num_lines_starting_with_digit}\n")

        len_pages = len(page_addr_counter)
        len_ip = len(ip_addr_counter)
        file.write(f"Page_addr distribution:{len_pages}\n")
        file.write(f"Ip_addr distribution:{len_ip}\n")
        for addr, count in page_addr_counter.most_common():
            file.write(f"{addr}: {count}\n")
            if(count > 0):
                pages_fre.append(count)
        file.write(f"Ip_addr distribution:{len_ip}\n")
        for addr, count in ip_addr_counter.most_common():
            file.write(f"{addr}: {count}\n")
            if(count > 0):
                ip_fre.append(count)
        file.write("Lines after 'L1D':\n")
        file.writelines(output_content)
    
    # len_pages = len(pages_fre)
    # len_ip = len(ip_fre)
    # fig, ax = plt.subplots()
    # # ax.bar(range(len(pages_fre)), pages_fre, label=f'Page_addr len({len(pages_addr_counter)})', alpha=0.5)
    # # ax.bar(range(len(ip_fre)), ip_fre, label=f'Ip_addr len({len(ip_addr_counter)})', alpha=0.5)
    # ax.bar(range(len(pages_fre)), pages_fre, label=f'Page_addr len{len_pages}', alpha=0.5)
    # ax.bar(range(len(ip_fre)), ip_fre, label=f'Ip_addr len{len_ip}', alpha=0.5)
    # max_range = max(len(pages_fre),len(ip_fre))
    # print(max_range)
    # # ax.ylim(0,max(max(pages_fre),max(ip_fre)))
    # ax.set_xticks(range(max_range))
    # #ax.set_xticklabels(range(1, max_range+1),fontsize=4)
    # ax.legend()

    # # Save the plot to a file
    # plt.savefig(os.path.join(output_directory_png, f"{result_name}_bar_chart.png"),dpi=300)
    # plt.close()
    

def main():
    directory = "./outputsum/output0729/spec2k17/"
    output_directory_txt = "./outputsum/output0729/spec2k19_statistic_txt/"
    output_directory_png = "./outputsum/output0729/spec2k19_statistic_png/"
    if not os.path.exists(output_directory_txt):
    # 如果目录不存在，则创建该目录
        os.makedirs(output_directory_txt)
    if not os.path.exists(output_directory_png):
    # 如果目录不存在，则创建该目录
        os.makedirs(output_directory_png)

    # with ThreadPoolExecutor() as executor:
    #     for filename in os.listdir(directory):
    #         if filename.endswith(".champsimtrace.xz"):
    #             executor.submit(parse_file, os.path.join(directory, filename), output_directory_txt,output_directory_png)
    for filename in os.listdir(directory):
        if filename.endswith(".champsimtrace.xz"):
            parse_file(os.path.join(directory, filename), output_directory_txt,output_directory_png)


if __name__ == "__main__":
    main()

# import os
# import re
# from collections import Counter
# from concurrent.futures import ThreadPoolExecutor

# def parse_file(path):
#     with open(path, 'a+') as file:
#         file.seek(0) 
#         lines = file.readlines()
#         ip_use = 0
#         ip_total = 0
#         pages_use = 0
#         pages_total = 0
#         bop_use = 0
#         bop_total = 0
#         for i in range(len(lines)):
#             line = lines[i]
#             match_ip_use = re.search(r"^\s*ip_useful\s+(\d+)", line)
#             if match_ip_use:
#                 ip_use = int(match_ip_use.group(1))

#             match_ip_total = re.search(r"^\s*ip_to_lower_level\s+(\d+)", line)
#             if match_ip_total:
#                 ip_total = int(match_ip_total.group(1))

#             match_pages_use = re.search(r"^\s*pages_useful\s+(\d+)", line)
#             if match_pages_use:
#                 pages_use = int(match_pages_use.group(1))

#             match_pages_total = re.search(r"^\s*pages_to_lower_level\s+(\d+)", line)
#             if match_pages_total:
#                 pages_total = int(match_pages_total.group(1))

#             match_bop_use = re.search(r"^\s*bop_useful\s+(\d+)", line)
#             if match_bop_use:
#                 bop_use = int(match_bop_use.group(1))

#             match_bop_total = re.search(r"^\s*bop_to_lower_level\s+(\d+)", line)
#             if match_bop_total:
#                 bop_total = int(match_bop_total.group(1))
#         ip_accuracy = 100.0 * float(ip_use)/ ip_total
#         pages_accuracy = 100.0 * float(pages_use)/ pages_total
#         bop_accuracy = 100.0 * float(bop_use)/ bop_total
#         ip_pages_accuracy = 100.0 * float(ip_use + pages_use)/(ip_total+pages_total)
#         total_accuracy = 100.0 * float(ip_use + pages_use + bop_use)/(ip_total+pages_total + bop_total)
#         file.write(f"IP Accuracy:{ip_accuracy}\n")
#         file.write(f"pages Accuracy:{pages_accuracy}\n")
#         file.write(f"bop Accuracy:{bop_accuracy}\n")
#         file.write(f"IP+Pages Accuracy:{ip_pages_accuracy}\n")
#         file.write(f"total Accuracy:{total_accuracy}\n")


# def main():
#     directory = "./outputsum/output0727/spec2k17_statistic/"

#     # with ThreadPoolExecutor() as executor:
#     #     for filename in os.listdir(directory):
#     #         if filename.endswith(".champsimtrace.xz"):
#     #             executor.submit(parse_file, os.path.join(directory, filename), output_directory)
#     for filename in os.listdir(directory):
#         parse_file(os.path.join(directory, filename))


# if __name__ == "__main__":
#     main()


# import os
# import re
# from collections import Counter
# from concurrent.futures import ThreadPoolExecutor

# def parse_file(path):
#     page_addr_counter = Counter()
#     ip_addr_counter = Counter()
#     num_lines_starting_with_digit = 0
#     output_content = []

#     with open(path, 'r') as file:
#         lines = file.readlines()
#         for i in range(len(lines)):
#             line = lines[i]
#             # If line doesn't start with a digit
#             if not re.match(r'^\d+', line):
#                 output_content.append(line)

#     # Overwrite the original file with the lines not starting with a digit
#     with open(path, 'w') as file:
#         file.writelines(output_content)

# def parse_directory(directory_path, num_threads=48):
#     executor = ThreadPoolExecutor(max_workers=num_threads)
#     for root, dirs, files in os.walk(directory_path):
#         for filename in files:
#             if filename.endswith('.champsimtrace.xz'):
#                 filepath = os.path.join(root, filename)
#                 executor.submit(parse_file, filepath)

# parse_directory('./outputsum/output0728/spec2k17/')