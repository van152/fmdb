import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def get(n): return (D/(('payload_summary.bin') if n=='summary' else f'payload_server_{n}.bin')).read_bytes()

# name_table f0/f3 relationship
b=get('name_table_0'); rc=struct.unpack_from('<I',b,8)[0]
rows=[struct.unpack_from('<6H',b,12+i*12) for i in range(rc)]
e0=(D/'payload_server_name_table_extra_0.bin').read_bytes()
p=12; strs=[]
for i in range(rc):
    uid,ln=struct.unpack_from('<II',e0,p); strs.append(e0[p+8:p+8+ln]); p+=8+ln
byf3=collections.defaultdict(list)
for i,r in enumerate(rows): byf3[r[3]].append(strs[i].decode('utf-8','replace'))
for k in sorted(byf3, key=lambda k:-len(byf3[k]))[:6]:
    print('f3=%s n=%d sample=%s'%(k,len(byf3[k]),byf3[k][:8]))
print()
# f0 vs f3: for f0=2298
s=set((r[3],r[5]) for r in rows if r[0]==2298)
print('f0=2298 combos',list(s)[:6])
print('f0 non-sentinel values sample',sorted(set(r[0] for r in rows if r[0]!=65535))[:20])
print()
# common_name_links A range vs pools
c=get('common_name_links'); n=struct.unpack_from('<I',c,8)[0]
A=[struct.unpack_from('<I',c,12+i*10)[0] for i in range(n)]
sent=[a for a in A if a==0xFFFFFFFF]
real=[a for a in A if a!=0xFFFFFFFF]
print('cnl A: n',n,'sentinel',len(sent),'min',min(real),'max',max(real),'<245981',sum(1 for a in real if a<245981),'<542060',sum(1 for a in real if a<542060))
print('cnl byte4 counter',collections.Counter(c[12+i*10+4] for i in range(n)).most_common(4))
print('cnl u16@8 hi-byte dist',collections.Counter(struct.unpack_from('<H',c,12+i*10+8)[0]>>8 for i in range(n)).most_common(6))
print()
# club_links marker counts
cl=get('club_links'); m=struct.unpack_from('<I',cl,8)[0]
print('club_links 01006c07 count',cl.count(b'\x01\x00\x6c\x07'),'rows',m)
print('club_links u32@0 == u32@9 count',sum(1 for i in range(m) if struct.unpack_from('<I',cl,12+i*47)[0]==struct.unpack_from('<I',cl,12+i*47+9)[0]))
