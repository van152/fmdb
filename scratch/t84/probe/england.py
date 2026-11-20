import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
raw=K['load_payload'](lib.CODEC,'client','3')
i=0; n=0
while True:
    i=raw.find(b'England',i)
    if i<0: break
    n+=1
    if n<=6:
        print(f'hit {i}: {raw[max(0,i-28):i+16].hex(" ")}')
        print(f'         ascii {raw[max(0,i-28):i+16]!r}')
    i+=1
print('total England occurrences',n,'in client table_3')
# is it inside a length-prefixed name? check prefix
i=raw.find(b'England')
print('prefix4', struct.unpack_from('<I',raw,i-4)[0])
