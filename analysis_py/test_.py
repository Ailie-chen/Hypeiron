import re

text = "[1 120888640 1 {2 } P][-5 120888634 2 {3 } P][-2 120888637 2 {3 } P]"
pattern = r'(\d+) (\d+) (\d+)'

matches = re.findall(pattern, text)

# 提取所有的数字
result =  [match[1] for match in matches]

print(result)

