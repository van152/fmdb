import sys,struct
sys.path.insert(0,'scratch/t85/work'); sys.stdout.reconfigure(encoding='utf-8')
import common as C
raw=C.payload('client','client_db/name_table_extra_0.dat',3837439)
print('len',len(raw),'head',raw[:16].hex())
# try [len u32][bytes] then [id u32]? and [id][len][bytes]
def try_grammar(raw,start,mode,n=6):
    p=start; out=[]
    for i in range(n):
        if mode=='len_id':
            if p+4>len(raw): break
            ln=struct.unpack_from('<I',raw,p)[0]
            s=raw[p+4:p+4+ln]
            if not (0<ln<64) or not all(32<=b<127 for b in s): break
            idv=struct.unpack_from('<I',raw,p+4+ln)[0]
            out.append((p,ln,s.decode(),idv)); p=p+8+ln
        else:
            if p+8>len(raw): break
            idv,ln=struct.unpack_from('<II',raw,p)
            s=raw[p+8:p+8+ln]
            if not (0<ln<64) or not all(32<=b<127 for b in s): break
            out.append((p,idv,ln,s.decode())); p=p+8+ln
    return out,p
for mode,st in (('len_id',16),('id_len',16),('len_id',17),('id_len',17)):
    o,p=try_grammar(raw,st,mode)
    print(mode,st,'->',o[:5],'end',p)
