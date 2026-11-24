"""t88-fix6: jump-table code -> stub (rec_type,tag).
stub shapes at target t:
  A) 48 89 f9 (mov rcx,rdi) ; b2 N ; 41 b8 tag32 ; e9
  B) b2 N ; 41 b8 tag32 ; e9            (rcx already rdi)
  C) 48 89 f9 ; b2 N ; jmp  -> tag inherited from shared tail (resolve via 0x11f2a5a)
usage: t88_jt2.py
"""
import sys,json,struct
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg
EXE=str(_cfg.EDITOR_EXE)
def s4(v):
    b=v.to_bytes(4,'big')
    return b.decode('latin1') if all(32<=c<127 for c in b) else None
def main():
    d=open(EXE,'rb').read()
    tabs=json.load(open('scratch/t88/out3/_jt.json'))
    m=json.load(open('evidence/fm24/reports/editor_schema/master.json'))
    codes=[f['field'] for f in m['entities']['club.xml'][0]['fields'][211:328]]
    SHARED={0x11f2a5a:'otht'}
    def stub(t):
        p=t
        if d[p:p+3]==b'\x48\x89\xf9': p+=3
        if d[p:p+1]!=b'\xb2': return None
        dl=d[p+1]; p+=2
        if d[p:p+2]==b'\x41\xb8':
            tg=s4(struct.unpack_from('<I',d,p+2)[0])
            if tg: return dl,tg,t
        if d[p:p+1]==b'\xe9':
            off=struct.unpack_from('<i',d,p+1)[0]; tgt=p+5+off
            if tgt in SHARED: return dl,SHARED[tgt],t
        return None
    res={}
    for t in tabs:
        for e in t['entries']:
            if not e['code']: continue
            st=stub(e['tgt'])
            res.setdefault(e['code'],[]).append({'rt':st[0] if st else None,'tag':st[1] if st else None,
                'jt':hex(t['lea_fo']),'tgt':hex(e['tgt'])})
    json.dump(res,open('scratch/t88/out3/_jtmap.json','w'),indent=0)
    hit=[c for c in codes if c in res and res[c][0]['rt'] is not None]
    print('codes in tables',len([c for c in codes if c in res]),'with stub',len(hit))
    miss=[c for c in codes if c in res and res[c][0]['rt'] is None]
    print('unresolved in-table',len(miss),miss)
    for c in codes:
        if c in res and res[c][0]['rt'] is not None: print('  %s rt=%d tag=%s'%(c,res[c][0]['rt'],res[c][0]['tag']))
if __name__=='__main__':
    if '--help' in sys.argv: print(__doc__); sys.exit(0)
    main()
