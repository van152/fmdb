#!/usr/bin/env python3
"""Commander independent full-table spot-check of t31 CSrs/table62. Does NOT import t31 builder/verifier."""
import json, os, sys, hashlib, struct
from pathlib import Path
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(r'D:/tmp2b/fm24-db'); OUT=ROOT/'scratch/t31/out'
sys.path.insert(0,str(ROOT/'scripts'))
os.environ['FM24_DB_DIR']='D:/tmp2b/fm24-db/scratch/data'
import fm24_dump as db
from t05_pe import PE
checks=[]
def ck(n,c,x=''):
    checks.append((n,bool(c),x)); print(('PASS' if c else 'FAIL'),n,x)
codec=db._reader()
cent=[e for e in codec['list_tables'](db.DB_DIR/'client_db.dat','client_db.dat') if e['table_id']==62]
ck('client_no_table62', len(cent)==0, f'{len(cent)}')
raw=db.load_payload(codec,'server',62)
ck('payload_1563010', len(raw)==1563010, f'len={len(raw)}')
ck('payload_sha', hashlib.sha256(raw).hexdigest()=='978066bc07e96f2e75ee8909635052d778322219abc0f266a9a9aa01f0a0a485')
n=struct.unpack_from('<I',raw,8)[0]
ck('count_37214', n==37214, f'n={n}')
ck('closure_13_n42_9', 13+n*42+9==len(raw))

def i8(o): return struct.unpack_from('<b',raw,o)[0]
def u32(o): return struct.unpack_from('<I',raw,o)[0]
def i32(o): return struct.unpack_from('<i',raw,o)[0]

fields=json.load(open(OUT/'fields_csrs.json',encoding='utf-8'))['fields']
# independent per-field domain validation across ALL rows
viol={x['code']:0 for x in fields}
sent={x['code']:0 for x in fields}
true_cnt={x['code']:0 for x in fields}
live={x['code']:set() for x in fields}
uids=set(); ident_ok=0; sel_nonzero=0
for i in range(n):
    if raw[13+42*i]!=0: sel_nonzero+=1
    b=14+42*i
    l0,l1,l2=struct.unpack_from('<III',raw,b+29)
    if l0==i and l1==l2 and l1!=0: ident_ok+=1
    uids.add(l1)
    for x in fields:
        c=x['code']; off=b+x['row_offset']; interp=x['interpretation']; dom=x.get('domain',{})
        if interp=='i8':
            v=i8(off); s=dom.get('sentinel', -1 if 'frozen_enum' in dom else 0)
            if 'frozen_enum' in dom:
                if v==-1: sent[c]+=1
                elif v not in dom['values']: viol[c]+=1
                else: live[c].add(v)
            else:
                lv=dom.get('live_values',[])
                if v==0: sent[c]+=1
                elif v not in lv: viol[c]+=1
                else: live[c].add(v)
        elif interp=='ordinal':
            v=u32(off); lo,hi=dom['bounds']
            if v==0xffffffff: sent[c]+=1
            elif not(lo<=v<=hi): viol[c]+=1
            else: live[c].add(v)
        elif interp=='bool':
            bit=(raw[off] & x['bit_mask'])!=0
            true_cnt[c]+= bit
        elif interp=='i32':
            v=i32(off); lo,hi=dom['xml_bounds']
            if v==-1: sent[c]+=1
            elif not(lo<=v<=hi): viol[c]+=1
            else: live[c].add(v)
ck('all_selector_zero', sel_nonzero==0, f'{sel_nonzero}')
ck('all_identity', ident_ok==n, f'{ident_ok}/{n}')
ck('uids_distinct', len(uids)==n, f'{len(uids)}')
ck('zero_domain_violations_all_fields', all(v==0 for v in viol.values()), str(viol))
ck('Ttyp_9_live_codes', len(live['Ttyp'])==9, f"live={sorted(live['Ttyp'])}")
ck('Tdvi_sentinel_29922', sent['Tdvi']==29922, f"{sent['Tdvi']}")
ck('Tsti_sentinel_30311', sent['Tsti']==30311, f"{sent['Tsti']}")
ck('tmno_true_23792', true_cnt['tmno']==23792, f"{true_cnt['tmno']}")
ck('tmnv_true_451', true_cnt['tmnv']==451, f"{true_cnt['tmnv']}")
ck('Twhm_sentinel_33197', sent['Twhm']==33197, f"{sent['Twhm']}")
ck('Twhm_Tmhm_live_1_7', live['Twhm']==set(range(1,8)) and live['Tmhm']==set(range(1,8)), f"Twhm={sorted(live['Twhm'])} Tmhm={sorted(live['Tmhm'])}")
foot=raw[13+n*42:]
ck('footer_9B', foot==bytes.fromhex('00000000015e910000'), foot.hex())
ck('10_L3_0_held', sum(str(x['grade']).startswith('L3') for x in fields)==10 and len(fields)==10)
# static
pe=PE(Path(r'D:/tmp2b/fm24/input/editor.exe'))
ck('pe_sha', hashlib.sha256(pe.raw).hexdigest()=='b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4')
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
md=Cs(CS_ARCH_X86,CS_MODE_64)
recs=[]
for p in sorted(OUT.glob('instructions.part*.json')):
    d=json.load(open(p,encoding='utf-8')); recs.extend(d if isinstance(d,list) else d.get('instructions',[]))
def toint(v):
    if isinstance(v,int): return v
    s=str(v); return int(s,16) if s.lower().startswith('0x') else int(s)
import random; random.seed(31)
sample=random.sample(recs,min(40,len(recs))); ok=0
for r in sample:
    fo=toint(r['file_offset']); va=toint(r['VA']); wb=bytes.fromhex(r['bytes']) if isinstance(r['bytes'],str) else bytes(r['bytes'])
    if pe.va2f(va)==fo and pe.raw[fo:fo+len(wb)]==wb:
        di=list(md.disasm(pe.raw[fo:fo+15],va,count=1))
        if di and di[0].bytes==wb: ok+=1
ck('static_sample_40', ok==len(sample), f'{ok}/{len(sample)} total={len(recs)}')
print('---')
fails=[c for c in checks if not c[1]]
print(f't31 spot: {len(checks)-len(fails)}/{len(checks)} PASS', ('FAILS:'+str([c[0] for c in fails])) if fails else 'ALL GREEN')
sys.exit(1 if fails else 0)