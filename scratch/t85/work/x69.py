import json,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_client_extra_9.rows.jsonl',encoding='utf-8')]
h0=collections.Counter(); h4=collections.Counter(); h5=collections.Counter(); h7=collections.Counter(); trail=collections.Counter(); ok=0; noitem=[]
for r in rows:
    b=bytes.fromhex(r['raw_hex']); nl=r['marker']['name_len']; t=b[8+nl:]
    h0[t[0]]+=1; h4[int.from_bytes(t[1:5],'little')]+=1; h5[t[5]]+=1; h7[t[7]]+=1
    n=t[6]; s=8
    if (len(t)-s)!=n*27+14: noitem.append((r['row'],len(t),n)); continue
    if t[6]==n: ok+=1
    trail[t[s+27*n:]]+=1
print('rows with tail == 8+27n+14:',251-len(noitem),'/251 ; failures',noitem[:6])
print('tail[0] hist',h0.most_common(8)); print('tail[1:5] u32',h4.most_common(6))
print('tail[5]',h5.most_common(4)); print('tail[7]',h7.most_common(4))
print('trailer distinct',len(trail),'top',trail.most_common(3))
