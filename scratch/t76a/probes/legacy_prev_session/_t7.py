import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
dump = runpy.run_path('scripts/fm24_dump.py', run_name='t76a_dump')
codec = dump['_reader']()
t3 = dump['load_payload'](codec, 'client', 3)
rows = list(dump['walk_club_block'](t3))
for j in (0,1,2):
    b = rows[j][2]
    print(j, len(b), b[:24].hex(' '), '...', b[-20:].hex(' '))
    print('   tail u32s', [struct.unpack_from('<I', b, len(b)-4*k)[0] for k in range(1,5)])
