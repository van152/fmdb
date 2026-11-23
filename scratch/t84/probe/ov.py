import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
raw=K['load_payload'](lib.CODEC,'client','25')
i=raw.find(struct.pack('<I',130026))
print('uid 130026 at',i)
print('ctx',raw[max(0,i-32):i+40].hex(' '))
# what row is this in? header 13, rows 127
print('row', (i-13)//127, 'rel', (i-13)%127)
