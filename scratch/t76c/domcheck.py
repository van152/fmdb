"""t76c scratch: are the reference UID domains contiguous ranges or sparse sets?"""
import json
from pathlib import Path

D = json.loads(Path('scratch/t76c/domains_client.json').read_text())
for nm, v in D.items():
    u = v['uid_set']
    s = sorted(u)
    span = s[-1] - s[0] + 1
    print(f'{nm:14} n={len(s):<7} min={s[0]:<8} max={s[-1]:<8} span={span:<8} '
          f'density={len(s)/span:.4f} contiguous={len(s)==span}')
    print('   first12', s[:12], '...')
