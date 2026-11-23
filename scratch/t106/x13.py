import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_table_for_old_save_25.bin').read_bytes()
n=struct.unpack_from('<I',b,8)[0]
# count occurrences of each 4-byte pattern at stride candidates? Instead: histogram of 3-byte patterns frequency==n
cnt=collections.Counter()
for p in range(12,len(b)-3):
    cnt[b[p:p+3]]+=1
cands=[(k,v) for k,v in cnt.items() if v==n]
print('3B patterns with count==n:',len(cands),cands[:10])
cnt4=collections.Counter()
for p in range(12,len(b)-4):
    cnt4[b[p:p+4]]+=1
c4=[(k,v) for k,v in cnt4.items() if v==n]
print('4B patterns with count==n:',len(c4),c4[:10])
print('freq near n:',sorted([v for v in cnt.values() if abs(v-n)<n*0.02])[:5])
