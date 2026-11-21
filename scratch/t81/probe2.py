"""Generic ordinal-chain identity scan: no grammar needed."""
import runpy, struct, time
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]

def chain(raw, n, start=0, require_marker_zero=True):
    pos = start; found = []
    for j in range(n):
        hit = None
        p = pos
        L = len(raw)
        while p + 12 <= L:
            if u32(raw,p) == j:
                a,b = u32(raw,p+4), u32(raw,p+8)
                if a == b != 0 and (not require_marker_zero or p+12 >= L or raw[p+12] == 0):
                    hit = p; break
            p += 1
        if hit is None: return found, 'lost at row %d' % j
        found.append(hit); pos = hit + 12
    return found, None

for a,t in [('client',10),('client',8),('client',27),('client',47),('server',24),('client',6),('server',6),('client',23),('client',35)]:
    t0=time.time(); raw = m['load_payload'](a,t); n = u32(raw,8)
    f, why = chain(raw, n)
    gaps = [f[i+1]-f[i] for i in range(len(f)-1)]
    print(a,t,'n',n,'found',len(f),'why',why,'first',f[:2],'last',f[-1] if f else None,
          'end_tail', len(raw)-f[-1]-12 if f else None, 'medgap', sorted(gaps)[len(gaps)//2] if gaps else None,
          '%.1fs'%(time.time()-t0))
    if f:
        print('   gap_ok_end:', f[-1]+12, 'payload', len(raw), 'gapdiff', f[-1]+12-len(raw))
