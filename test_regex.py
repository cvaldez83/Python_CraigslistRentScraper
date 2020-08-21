import re

a = '2.5Ba'
b = re.findall("(\d.\dBa|\dBa)",a)
print(b)
