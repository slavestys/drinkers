import re
import os

import yaml


reg = re.compile('#include ([\w\d\.]+)')

data = {
    'application.yml': 'a: 1',
    'x.yml': 'z: 1'
}

conf = '''
    #include application.yml
    x: 1
    y: 
        #include x.yml
'''

res = ''
for line in conf.splitlines():
    m = re.search(reg, line)
    points = m and (m.regs[1] if len(m.regs) > 1 else None)
    if points:
        key = line[points[0]:points[1]]
        val = data[key]
        replace_key = line[m.regs[0][0]:m.regs[0][1]]
        line = line.replace(replace_key, val)
    res += line + os.linesep

print(yaml.load(res))

