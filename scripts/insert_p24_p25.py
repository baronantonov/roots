#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

with open('/home/brnv/projects/ROOTS/dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

from scripts.extend_baronov_branch import P_0025_OBJ, P_0024_OBJ

# Insert P-0025 after P-0010 if id: "P-0025" not in html
if 'id: "P-0025"' not in html:
    p10_pat = re.compile(r'(id:\s*\"P-0010\"[\s\S]*?story:\s*\"[\s\S]*?\"\s*\})(,)', re.MULTILINE)
    m10 = p10_pat.search(html)
    if m10:
        html = html[:m10.end(1)] + ",\n" + P_0025_OBJ + html[m10.end(2):]
        print("Inserted P-0025 successfully!")
    else:
        print("ERROR: could not find P-0010!")

# Insert P-0024 after P-0020 if id: "P-0024" not in html
if 'id: "P-0024"' not in html:
    p20_pat = re.compile(r'(id:\s*\"P-0020\"[\s\S]*?story:\s*\"[\s\S]*?\"\s*\})(,)', re.MULTILINE)
    m20 = p20_pat.search(html)
    if m20:
        html = html[:m20.end(1)] + ",\n" + P_0024_OBJ + html[m20.end(2):]
        print("Inserted P-0024 successfully!")
    else:
        print("ERROR: could not find P-0020!")

with open('/home/brnv/projects/ROOTS/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Finished inserting P-0025 and P-0024!")
