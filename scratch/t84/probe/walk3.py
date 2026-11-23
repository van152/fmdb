import sys, struct, re
sys.path.insert(0,'scratch/t84/probe')
import lib, runpy
K=lib.K

def rows_client3():
    raw = K['load_payload'](lib.CODEC,'client','3')
    return raw, list(K['walk_club_block'](raw))

raw, rows = rows_client3()
print('count walk', len(rows), 'len', len(raw))
for i,(i2,off,body) in enumerate(rows[:4]):
    print('row',i2,'off',off,'len',len(body))
    print('  ', body.hex(' '))
    for m in re.finditer(rb'[ -~]{3,}', body):
        print('    run at', m.start(), m.group()[:60])
