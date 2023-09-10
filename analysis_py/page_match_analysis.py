
import os

def extract_bench_name(filename):
    # Extract the bench name from the filename
    # Assumes the format: ...---BENCHNAME.champsimtrace.xz
    parts = filename.split('---')
    if len(parts) > 1:
        bench_name = parts[-1].split('.champsimtrace.xz')[0]
        return bench_name
    return None

def count_keyword_proportions(file_path, keywords):
    keyword_counts = {keyword: 0 for keyword in keywords}
    total_lines = 0
    
    with open(file_path, 'r', errors='replace') as file:
        for line in file:
            total_lines += 1
            for keyword in keywords:
                if keyword in line:
                    keyword_counts[keyword] += 1
    
    keyword_proportions = {keyword: count / total_lines for keyword, count in keyword_counts.items()}
    return keyword_proportions

def main():
    # Define the directory containing the files and the output file
    directory = './outputsum/output0922/spec2k17/'  # Modify this to the path of your directory
    output_file_path = 'output_results.txt'
    keywords = ["ip P", "ip F", "pgo P", "pgo F", "ip+offset P", "ip+offset F", 
                "hot_page P", "hot_page F", "record_page F", "record_page P", "no match"]
    
    with open(output_file_path, 'w') as output_file:
        for filename in sorted(os.listdir(directory)):
            if filename.endswith(".champsimtrace.xz"):  # Check for the correct file extension
                bench_name = extract_bench_name(filename)
                if bench_name:
                    file_path = os.path.join(directory, filename)
                    proportions = count_keyword_proportions(file_path, keywords)
                    sorted_proportions = sorted(proportions.items(), key=lambda x: x[1], reverse=True)  # Sort by proportions
                    output_line = bench_name + ',' + ','.join([f"{keyword}:{value:.2%}  " for keyword, value in sorted_proportions])
                    output_file.write(output_line)
                    output_file.write('\n')

if __name__ == "__main__":
    main()

