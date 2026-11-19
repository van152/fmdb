import os,pathlib,runpy,struct,sys,re
from collections import Counter
ROOT=pathlib.Path(r'D:\tmp2b\fm24-db'); sys.path.append(r'D:\tmp2b\fm24\tools\python')
import zstandard as z
codec=runpy.run_path(r'D:\tmp2b\fm24\scripts\modding_read_dbdat.py')
DB=pathlib.Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
P={}
for side in ('client','server'):
    db=(DB/f'{side}_db.dat').read_bytes(); lay=codec['_archive_layout'](db); base=lay['data_base']
    es={(x['path'].split('/')[-1]):x for x in lay['entries']}
    e=es['table_extra_9.dat']; P[side]=z.ZstdDecompressor().decompressobj().decompress(db[base+e['offset']:base+e['offset']+e['packed_size']])
c,s=P['client'],P['server']
print('client len',len(c),'server len',len(s))
print('same suffix?',c[-64:]==s[-64:])
# common prefix length
i=0
while i<min(len(c),len(s)) and c[i]==s[i]: i+=1
print('common prefix bytes',i)
def dump(b,off,n=200):
    for k in range(0,n,32):
        chunk=b[off+k:off+k+32]
        print(f'  {off+k:6d} {chunk.hex()}  {"".join(chr(x) if 32<=x<127 else "." for x in chunk)}')
print('--- client extra_9 0..320'); dump(c,0,320)
print('--- server extra_9 0..320'); dump(s,0,320)
# ASCII runs
def runs(b,minlen=3):
    out=[];i=0
    while i<len(b):
        j=i
        while j<len(b) and 32<=b[j]<127: j+=1
        if j-i>=minlen: out.append((i,b[i:j].decode()))
        i=max(j,i+1)
    return out
rc=runs(c); rs=runs(s)
print('client ascii runs',len(rc),'server',len(rs))
print('client first 8',rc[:8])
print('server first 8',rs[:8])
print('client last 4',rc[-4:])
print('server last 4',rs[-4:])
