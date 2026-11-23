import sys, struct, re
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
for a,t in (('client','41'),('server','41')):
    raw=K['load_payload'](lib.CODEC,a,t)
    print(f'== {a} table_{t} len={len(raw)} cnt@8={struct.unpack_from("<I",raw,8)[0]}')
    print('  head', raw[:48].hex(' '))
    for nd in (b'England',b'Suriname',b'Bhutan',b'Vanuatu',b'Tahiti',b'China PR',b'Brazil'):
        i=raw.find(nd)
        if i>=0: print(f'   {nd.decode():12s} at {i}: {raw[max(0,i-16):i+len(nd)+8].hex(" ")}')
