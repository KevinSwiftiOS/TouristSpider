# -*- coding:utf-8 -*-

import re
_str = '奥斯卡级hi空间大撒545谎单价(8)'
print(re.sub(r'([^(]+)\([^)]+\)',r'\1',_str))
print(re.sub(r'[^(]+\(([^)]+)\)',r'\1',_str))
