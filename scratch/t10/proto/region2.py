import json
from pathlib import Path
hits = json.loads(Path("scratch/t10/proto/hits.json").read_text())
hits.sort()
sel=[(o,c) for o,c in hits if 0xe82000<=o<0xe8e000]
print(len(sel))
for o,c in sel[:120]:
    print(f'{o:#08x} {c}')
