import os
import math
import re
from collections import Counter
import multiprocessing
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import csv
import glob
pattern = r"valid_ways: (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)"
directory = "./outputsum/output1209/spec2k17/"

def parse_file(path):
    valid_ways = [0 for i in range(13)]
    with open(path, 'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i]
            # If line starts with a digit
            pattern_match = re.match(pattern, line)
            if pattern_match:
                for j in range(13):
                    valid_ways[j] = int(pattern_match.group(j+1))
    print(path, 'A',' ', valid_ways)
    file.close
    return valid_ways




        
def main():

    all_valid_ways = []
    valid_ways = [0 for i in range(13)]
    all_files = glob.glob(os.path.join(directory,'*.*z'))
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        all_valid_ways = pool.map(parse_file, all_files)
        pool.close()
        pool.join()
    for item in all_valid_ways:
        for i in range(13):
            valid_ways[i] += item[i]
    for i in range(13):
        valid_ways[i] = math.ceil(valid_ways[i]/len(all_valid_ways))
    print(len(all_valid_ways))
    print(valid_ways)
if __name__ == "__main__":
    main()