import sys, struct, re
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K

for a in ('client','server'):
    raw=K['load_payload'](lib.CODEC,a,'3')
    print('==',a,'len',len(raw),'hdr',raw[:13].hex(' '))
    i=raw.find(b'Liverpool')
    print('  Liverpool at',i, raw[i-40:i+20].hex(' '))
