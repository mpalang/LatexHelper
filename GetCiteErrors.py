import re

with open('Log.txt','r') as f:
    Log=f.readlines()

CiteWarnings=set()
CiteWarningsAll=set()

for line in Log:
    if 'Warning' and 'Citation' in line:
        CiteWarningsAll.add(line)

for line in CiteWarningsAll:
    CiteWarnings.add(re.search(r"(?<=`)\w+",line).group())

with open('CiteWarnAll.txt', 'a') as f:
    f.truncate(0)
    for line in sorted(list(CiteWarningsAll)):
       f.write(line)

with open('CiteWarn.txt', 'a') as f:
    f.truncate(0)
    f.write('Number of missing Citations: {} \n'.format(str(len(CiteWarnings))))
    for line in sorted(list(CiteWarnings), key=lambda v: v.upper()):
        f.write(line+'\n')
