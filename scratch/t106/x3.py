import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_table_for_old_save_23.bin').read_bytes()
n=278
s,k=15,14
rows=[]
for i in range(n):
    r=b[s+i*k:s+i*k+k]
    rows.append(r)
for i in range(8): print(i,' '.join('%02x'%x for x in rows[i]),struct.unpack('<3I',rows[i][:12]),struct.unpack('<H',rows[i][12:14]))
print('...')
for i in range(n-8,n): print(i,' '.join('%02x'%x for x in rows[i]),struct.unpack('<3I',rows[i][:12]),struct.unpack('<H',rows[i][12:14]))
print('tail after rows:',b[s+n*k:].hex())
# columns
for f in range(3):
    v=[struct.unpack_from('<I',r,f*4)[0] for r in rows]
    print('f%d'%f,'distinct',len(set(v)),'min',min(v),'max',max(v),'first10',v[:10],'last5',v[-5:])
v5=[struct.unpack_from('<H',r,12)[0] for r in rows]
print('f12u16 distinct',len(set(v5)),'top',collections.Counter(v5).most_common(8))
