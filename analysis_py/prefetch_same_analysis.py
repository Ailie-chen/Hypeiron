import os
import re

def process_file(filepath):
    # Define the regular expression patterns
    pattern_block = r"\[\d+ \d+ \d+ \{(\[[\d]+,\d+\] ?)+\} P\]"
    pattern_numbers = r"\[(\d+),\d+\]"

    # Read the file content
    with open(filepath, 'r') as f:
        content = f.read()

    # Extracting all blocks fitting the format
    blocks = re.findall(pattern_block, content)

    # Initializing counts for individual numbers and combinations
    counts = {'0': 0, '1': 0, '2': 0, '3': 0, '5': 0}
    count_2_and_3 = 0
    count_2_and_5 = 0
    count_3_and_5 = 0
    count_2_3_and_5 = 0

    # Processing each block
    for block in blocks:
        numbers_in_block = re.findall(pattern_numbers, block)
        for num in numbers_in_block:
            counts[num] += 1
        if '2' in numbers_in_block and '3' in numbers_in_block:
            count_2_and_3 += 1
        if '2' in numbers_in_block and '5' in numbers_in_block:
            count_2_and_5 += 1
        if '3' in numbers_in_block and '5' in numbers_in_block:
            count_3_and_5 += 1
        if '2' in numbers_in_block and '3' in numbers_in_block and '5' in numbers_in_block:
            count_2_3_and_5 += 1

    # Return the results
    return counts, count_2_and_3, count_2_and_5, count_3_and_5, count_2_3_and_5

def main():
    directory = "./outputsum/output0922/spec2k17/"
    result_file = "results_prefetch.txt"

    with open(result_file, 'w') as rf:
        # Iterate through every file in the directory
        for filename in sorted(os.listdir(directory)):
            if filename.endswith(".xz"):
                filepath = os.path.join(directory, filename)
                parts = filename.split('---')
                if len(parts) > 1:
                    unique_name = parts[-1].split('.champsimtrace.xz')[0]
                #unique_name = re.search(r'(\d+\.gcc_s-\d+B)', filename).group(1)
                counts, count_2_and_3, count_2_and_5, count_3_and_5, count_2_3_and_5 = process_file(filepath)

                # Write the results to the result file
                rf.write(f"Results for {unique_name}:\n")
                rf.write(f"Counts: {counts}\n")
                rf.write(f"2 and 3 together: {count_2_and_3}\n")
                rf.write(f"2 and 5 together: {count_2_and_5}\n")
                rf.write(f"3 and 5 together: {count_3_and_5}\n")
                rf.write(f"2, 3, and 5 together: {count_2_3_and_5}\n\n")

if __name__ == "__main__":
    main()
