import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def walk(raw):
    n=struct.unpack_from('<I',raw,8)[0]
    pos=13; out=[]
    for _ in range(n):
        A=struct.unpack_from('<b',raw,pos+24)[0]
        p=pos+25+5*A
        B=struct.unpack_from('<i',raw,p)[0]; p+=4+28*B
        C=struct.unpack_from('<i',raw,p)[0]; p+=4+28*C
        D=struct.unpack_from('<i',raw,p)[0]; p+=4+12*D
        ord_,uid,uid2=struct.unpack_from('<III',raw,p)
        assert raw[p+12]==0, (p,raw[p+12])
        out.append((ord_,uid,pos,p-pos+13,raw[pos:p+13]))
        pos=p+13
    return out,pos

raw=K['load_payload'](lib.CODEC,'client','10')
rows,end=walk(raw)
print('nation rows',len(rows),'end',end,'len',len(raw),'footer at',len(raw)-8)
print('first 3',rows[0][:3], rows[0][3])
print('uids',[r[1] for r in rows[:8]])
print('row body sample hex', rows[0][4][:60].hex(' '))
