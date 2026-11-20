import sys, struct, collections
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
raw=lib.load_member('lang_update','8_3.dat')
# Collect every occurrence of 00 xx 00 preceded by a string end and followed by plausible uid
terms=collections.Counter()
pos=12
while True:
    i=raw.find(b'\x00',pos)
    if i<0 or i+3>len(raw): break
    t=raw[i:i+3]
    nxt=struct.unpack_from('<I',raw,i+3)[0] if i+7<=len(raw) else None
    terms[t.hex()]+=1
    pos=i+1
print('all 00xx00 counts', terms.most_common(8))
# targeted: show bytes around 4 known boundaries
for off in (94,96,378,380,387):
    print(off, raw[off-6:off+12].hex(' '))
