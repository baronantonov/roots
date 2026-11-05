#!/usr/bin/env python3
import re
import subprocess
import tempfile

for fn in ['dashboard.html', 'index.html']:
    with open(fn, 'r', encoding='utf-8') as f:
        s = f.read()

    def fix_field(match):
        story_content = match.group(1)
        fixed = story_content.replace('\r\n', '\\n').replace('\n', '\\n')
        return 'story: "' + fixed + '"'

    s = re.sub(r'story:\s*"(.*?)"', fix_field, s, flags=re.DOTALL)

    with open(fn, 'w', encoding='utf-8') as f:
        f.write(s)
    print(f'Processed {fn}')

# Validate syntax
with open('dashboard.html') as f:
    html = f.read()

scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
print(f'Found {len(scripts)} inline script blocks')
for i, sc in enumerate(scripts):
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as tf:
        tf.write(sc)
        tf_name = tf.name
    res = subprocess.run(['node', '--check', tf_name], capture_output=True, text=True)
    if res.returncode != 0:
        print(f'Error in script {i}:', res.stderr[:300])
    else:
        print(f'Script {i}: Syntax OK ✓')
