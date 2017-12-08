import re
import os

import yaml


class YamlExtended:
    reg = re.compile('#include ([\w\d\.]+)')

    @staticmethod
    def prepare(file_name, root_dir):
        file_path = root_dir + file_name
        res = ''
        with open(file_path) as file:
            for line in file.read().splitlines():
                m = re.search(YamlExtended.reg, line)
                points = m and (m.regs[1] if len(m.regs) > 1 else None)
                if points:
                    key = line[points[0]:points[1]]
                    val = YamlExtended.prepare(key, root_dir)
                    replace_key = line[m.regs[0][0]:m.regs[0][1]]
                    line = line.replace(replace_key, val)
                res += line + os.linesep
        return res

    @staticmethod
    def load(file_name, root_dir):
        return yaml.load(YamlExtended.prepare(file_name, root_dir))
