import sys, struct, re
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K

def show(raw, start, n, label):
    print(f'-- {label}')
    for i in range(n):
        b=raw[start+i*127:start+(i+1)*127] if label.startswith('comp') else None

# comp table_25: header 13, rows 127 client
raw=K['load_payload'](lib.CODEC,'client','25')
print('comp len',len(raw))
for i in range(3):
    body=raw[13+i*127:13+(i+1)*127]
    print('row',i,body[:40].hex(' '))
    print('   runs', [(m.start(), m.group()[:30]) for m in re.finditer(rb'[ -~]{4,}', body)])
# nation table_10
raw10=K['load_payload'](lib.CODEC,'client','10')
print('nation len',len(raw10), 'hdr', raw10[:14].hex(' '))
print(raw10[:200].hex(' '))
print('runs', [(m.start(), m.group()[:30]) for m in re.finditer(rb'[ -~]{4,}', raw10[:400])])
