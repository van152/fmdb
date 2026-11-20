import runpy, sys, json, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_c = core['load_payload']('client', 21)
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413

def mat(raw, S):
    a = np.frombuffer(raw, dtype=np.uint8, count=H + n*S, offset=0)[H:H+n*S]
    return a.reshape(n, S)

def prof(m, name):
    print('='*20, name, m.shape)
    S = m.shape[1]
    for off in range(S):
        col = m[:, off]
        u = np.unique(col)
        info = f"{off:4d} u8d={len(u):3d}"
        if len(u) == 1: info += f" CONST={u[0]:02x}"
        if off + 2 <= S:
            v2 = m[:, off:off+2].copy().view('<u2').ravel()
            info += f" u16[{v2.min()},{v2.max()}]"
        if off + 4 <= S:
            v4 = m[:, off:off+4].copy().view('<u4').ravel()
            vf = m[:, off:off+4].copy().view('<f4').ravel()
            fin = np.isfinite(vf)
            info += f" u32[{v4.min()},{v4.max()}] d={len(np.unique(v4))}"
            if fin.all() and np.abs(vf).max() < 1e9:
                info += f" F32[{vf.min():.3f},{vf.max():.4f}]"
            info += f" ff={int((v4==0xffffffff).sum())} z={int((v4==0).sum())}"
        print(info)
prof(mat(raw_c, 38), 'client21')
prof(mat(raw_s, 181)[:, 140:181], 'server21[140:181]')
