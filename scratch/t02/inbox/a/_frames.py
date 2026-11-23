import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _lib import *

def try_stride(raw, count, hs=14, fs=8):
    body=len(raw)-hs-fs
    if body % count: return None
    return body//count

if __name__=='__main__':
    mod=load_old_decoder()
    for arch,tids in (('client_db.dat',(19,41,23,8,2,18,6)),('server_db.dat',(24,2,6,18))):
        for t in tids:
            try: s=member(mod,arch,t)
            except SystemExit: print(f'{arch} t{t} ABSENT'); continue
            st=try_stride(s['_raw'],s['count'])
            print(f"{arch:14s} t{t:<3d} payload={s['payload_bytes']:>9d} count={s['count']:>6d} stride={st}")
