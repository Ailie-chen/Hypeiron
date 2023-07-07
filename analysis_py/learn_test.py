import re

evaluate_cache = "L2C"
line = "L2C TIMELY PREFETCHES:       3766 LATE PREFETCHES: 0 DROPPED PREFETCHES: 0"
pattern3 = '^'+ evaluate_cache + '.*' + 'TIMELY PREFETCHES:\s+(\d+) LATE PREFETCHES:\s+(\d+)'
matches3 = re.search(pattern3, line)
print(matches3)
if matches3:
    print("m2")
    prefetch_request = matches3.group(2)
    print(prefetch_request)
