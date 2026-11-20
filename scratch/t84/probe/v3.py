import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

raw3=K['load_payload'](lib.CODEC,'client','3')
rows=list(K['walk_club_block'](raw3))

# Hypothesis: body+26 = u32 len, body+30 = full name ; then next u32 len, then short name
ok=ok2=0; bad=[]
for i,off,body in rows[:5000]:
    if len(body)<34: bad.append((i,'short')); continue
    L=struct.unpack_from('<I',body,26)[0]
    if not (1<=L<=120 and 30+L+4<=len(body)): bad.append((i,'len',L)); continue
    try: full=body[30:30+L].decode('utf-8')
    except Exception: bad.append((i,'utf8')); continue
    L2=struct.unpack_from('<I',body,30+L)[0]
    if not (0<=L2<=120 and 30+L+4+L2<=len(body)): bad.append((i,'len2',L2)); continue
    try: short=body[30+L+4:30+L+4+L2].decode('utf-8')
    except Exception: bad.append((i,'utf8b')); continue
    ok+=1
    if short and len(short)<len(full)+1: ok2+=1
print(f'club full@30 short@(30+L+4): {ok}/5000 closed; short shorter: {ok2}')
print('bad first', bad[:3])
for i in (0,460,542):
    off,body=rows[i][1],rows[i][2]
    L=struct.unpack_from('<I',body,26)[0]
    print(f'  row{i} full={body[30:30+L].decode("utf-8","replace")!r}')
