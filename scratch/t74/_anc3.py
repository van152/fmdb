import sys; sys.path.insert(0,'scripts')
import t74_frames_part2 as P
from t74_row_frames9 import payload, codec
import struct
c=codec()
# 核对 fm24_dump FIELDS 覆盖哪些本任务表
import runpy
d=runpy.run_path('scripts/fm24_dump.py')
F=d['FIELDS']
for tid in (0,7,8,18,21,24,27,47,56,6):
    print('FIELDS client',tid,F.get(('client',tid)))
print('--- t6 (16B) 检查')
b=payload(c,'client',6); n=struct.unpack_from('<I',b,8)[0]
print('t6 payload',len(b),'count',n,'closure',14+n*16+8==len(b))
print('t6 first row bytes',b[14:30].hex(' '))
