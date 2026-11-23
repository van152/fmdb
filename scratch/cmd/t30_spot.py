#!/usr/bin/env python3
"""Commander independent full-table spot-check of t30 Clhs/table37. Does NOT import t30 builder/verifier."""
import json, os, sys, hashlib, struct
from pathlib import Path
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(r'D:/tmp2b/fm24-db'); OUT = ROOT/'scratch/t30/out'
sys.path.insert(0, str(ROOT/'scripts'))
os.environ['FM24_DB_DIR'] = 'D:/tmp2b/fm24-db/scratch/data'
import fm24_dump as db
from t05_pe import PE
checks=[]
def ck(n,c,x=''):
    checks.append((n,bool(c),x)); print(('PASS' if c else 'FAIL'),n,x)

codec=db._reader()
# client must NOT have table37
cent=[e for e in codec['list_tables'](db.DB_DIR/'client_db.dat','client_db.dat') if e['table_id']==37]
ck('client_no_table37', len(cent)==0, f'client entries={len(cent)}')
raw=db.load_payload(codec,'server',37)
ck('payload_18628502', len(raw)==18628502, f'len={len(raw)}')
ck('payload_sha', hashlib.sha256(raw).hexdigest()=='46d9c5a7750a1d0fd2279b5f92b88936e98c143bfa4a0bd5faded5d710ef4f30')
n=struct.unpack_from('<I',raw,8)[0]
ck('count_465712', n==465712, f'n={n}')
ck('closure_13_n40_9', 13+n*40+9==len(raw))

def u8(b,o): return b[o]
def i8(b,o): return struct.unpack_from('<b',b,o)[0]
def u16(b,o): return struct.unpack_from('<H',b,o)[0]
def i16(b,o): return struct.unpack_from('<h',b,o)[0]
def u32(b,o): return struct.unpack_from('<I',b,o)[0]

# claimed legacy body offsets
OFF={'divi':(0,4),'play':(15,1),'wins':(16,1),'draw':(17,1),'lost':(18,1),
     'gfor':(19,2),'gaga':(21,2),'orde':(25,1),'year':(12,2),'posi':(14,1),
     'mxtm':(26,1),'poin':(23,2)}
uids=set(); ident_ok=0; sel_nonzero=0
divi_max=0; divi_min=1<<30
orde_zero=0; year_zero=0; posi_oob=0; mxtm_oob=0; poin_oob=0
play_sum=wins_sum=draw_sum=lost_sum=0
gfor_max=gaga_max=0
for i in range(n):
    sel=raw[13+40*i]
    if sel!=0: sel_nonzero+=1
    b=14+40*i
    lane0,l1,l2=struct.unpack_from('<III',raw,b+27)
    if lane0==i and l1==l2 and l1!=0: ident_ok+=1
    uids.add(l1)
    d=u32(raw,b+0); divi_max=max(divi_max,d); divi_min=min(divi_min,d)
    if u8(raw,b+25)==0: orde_zero+=1
    if u16(raw,b+12)==0: year_zero+=1
    pv=i8(raw,b+14)
    if pv!=-1 and (pv<0 or pv>50): posi_oob+=1
    if u8(raw,b+26)>50: mxtm_oob+=1
    p=i16(raw,b+23)
    if p<-1 or p>1000: poin_oob+=1
    play_sum+=u8(raw,b+15); wins_sum+=u8(raw,b+16); draw_sum+=u8(raw,b+17); lost_sum+=u8(raw,b+18)
    gfor_max=max(gfor_max,u16(raw,b+19)); gaga_max=max(gaga_max,u16(raw,b+21))

ck('all_selector_zero', sel_nonzero==0, f'nonzero={sel_nonzero}')
ck('all_identity', ident_ok==n, f'{ident_ok}/{n}')
ck('uids_distinct_nonzero', len(uids)==n, f'distinct={len(uids)}')
ck('divi_domain_0_7044', divi_min>=0 and divi_max<=7044, f'min={divi_min} max={divi_max}')
ck('orde_zero_sentinel_present', orde_zero>0, f'orde_zero={orde_zero}')
ck('year_87_zeros', year_zero==87, f'year_zero={year_zero}')
ck('posi_691_oob', posi_oob==691, f'posi_oob={posi_oob}')
ck('mxtm_2626_oob', mxtm_oob==2626, f'mxtm_oob={mxtm_oob}')
ck('poin_187_oob', poin_oob==187, f'poin_oob={poin_oob}')
ck('gfor_gaga_u16_sane', gfor_max<65536 and gaga_max<65536, f'gfor_max={gfor_max} gaga_max={gaga_max}')
# informational: my own football invariant (NOT a t30 claim). play scope may differ from W/D/L.
bad=0; checked=0; badrows=[]
for i in range(2000):
    b=14+40*i
    pl,wi,dr,lo=i8(raw,b+15),i8(raw,b+16),i8(raw,b+17),i8(raw,b+18)
    if -1 in (pl,wi,dr,lo): continue
    checked+=1
    if wi+dr+lo > pl: bad+=1; badrows.append((i,pl,wi,dr,lo))
print(f'NOTE play-vs-W/D/L scope: {bad}/{checked} rows sum>play (e.g. {badrows[:3]}); fields individually L3-proven, invariant is commander hypothesis not t30 claim')
foot=raw[13+n*40:]
ck('footer_9B_pattern', foot==bytes.fromhex('00000000018881da05'), foot.hex())
ck('footer_last_u32_maxUID', struct.unpack_from('<I',foot,5)[0]==max(uids), f'last={struct.unpack_from("<I",foot,5)[0]} maxUID={max(uids)}')

# fields grade
f=json.load(open(OUT/'fields_clhs.json',encoding='utf-8'))['fields']
l3=[x for x in f if str(x.get('grade','')).startswith('L3')]
held=[x for x in f if 'held' in str(x.get('grade',''))]
ck('8_L3_4_held', len(l3)==8 and len(held)==4, f'L3={len(l3)} held={len(held)}')
ck('L3_codes', {x['code'] for x in l3}=={'orde','divi','play','wins','draw','lost','gfor','gaga'}, str({x['code'] for x in l3}))

# static re-read sample
pe=PE(Path(r'D:/tmp2b/fm24/input/editor.exe'))
ck('pe_sha', hashlib.sha256(pe.raw).hexdigest()=='b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4')
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
md=Cs(CS_ARCH_X86,CS_MODE_64)
recs=[]
for p in sorted(OUT.glob('instructions.part*.json')):
    d=json.load(open(p,encoding='utf-8')); recs.extend(d if isinstance(d,list) else d.get('instructions',[]))
import random; random.seed(30)
sample=random.sample(recs,min(40,len(recs))); ok=0
def toint(v):
    if isinstance(v,int): return v
    s=str(v); return int(s,16) if s.lower().startswith('0x') else int(s)
for r in sample:
    fo=toint(r['file_offset']); va=toint(r['VA']); wb=bytes.fromhex(r['bytes']) if isinstance(r['bytes'],str) else bytes(r['bytes'])
    if pe.va2f(va)==fo and pe.raw[fo:fo+len(wb)]==wb:
        di=list(md.disasm(pe.raw[fo:fo+15],va,count=1))
        if di and di[0].bytes==wb: ok+=1
ck('static_sample_40', ok==len(sample), f'{ok}/{len(sample)} instr_total={len(recs)}')
print('---')
fails=[c for c in checks if not c[1]]
print(f't30 spot: {len(checks)-len(fails)}/{len(checks)} PASS', ('FAILS:'+str([c[0] for c in fails])) if fails else 'ALL GREEN')
sys.exit(1 if fails else 0)