#!/usr/bin/env python3
"""Commander independent spot-check of t28 nation client tail. Does NOT import t28 builder/verifier."""
import json, os, sys, hashlib, struct
from pathlib import Path
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(r'D:/tmp2b/fm24-db')
OUT = ROOT/'scratch/t28/out'
sys.path.insert(0, str(ROOT/'scripts'))
os.environ['FM24_DB_DIR'] = 'D:/tmp2b/fm24-db/scratch/data'
import fm24_dump as db
from t05_pe import PE

checks = []
def ck(name, cond, extra=''):
    checks.append((name, bool(cond), extra))
    print(('PASS' if cond else 'FAIL'), name, extra)

codec = db._reader()
raw = db.load_payload(codec, 'client', 10)
ck('payload_len_24732', len(raw) == 24732, f'len={len(raw)}')
# header: magic 8B + count u32 @8 + flag byte @12
n = struct.unpack_from('<I', raw, 8)[0]
ck('header_count_251', n == 251, f'n={n}')
ck('header_magic', raw[:8] == bytes.fromhex('03017461642ef10d'), raw[:8].hex())

def s8(b, o): return struct.unpack_from('<b', b, o)[0]
def u32(b, o): return struct.unpack_from('<I', b, o)[0]

pos = 13
tot = {'A':0,'B':0,'C':0,'D':0}
perc_vals = []
lang_vals = []
bc_dates = []   # (stdt, endt) raw u32 for B and C items
d_nged = []
ident_ok = 0
spans_sum = 0
row55 = None
for i in range(n):
    sel = raw[pos]
    bs = pos + 1
    A = s8(raw, bs+24)
    B = u32(raw, bs+25+5*A)
    C = u32(raw, bs+29+5*A+28*B)
    D = u32(raw, bs+33+5*A+28*B+28*C)
    a_start = bs+25
    b_start = bs+29+5*A
    c_start = bs+33+5*A+28*B
    d_start = bs+37+5*A+28*B+28*C
    id_off = d_start + 12*D
    ident = struct.unpack_from('<III', raw, id_off)
    if ident[0] == i and ident[1] == ident[2]:
        ident_ok += 1
    if i == 55:
        row55 = (id_off, ident)
    span = 50 + 5*A + 28*B + 28*C + 12*D
    spans_sum += span
    tot['A']+=A; tot['B']+=B; tot['C']+=C; tot['D']+=D
    for j in range(A):
        it = a_start + 5*j
        lang_vals.append(u32(raw, it))
        perc_vals.append(raw[it+4])
    for (cnt, st) in ((B, b_start), (C, c_start)):
        for j in range(cnt):
            it = st + 28*j
            bc_dates.append((u32(raw, it+20), u32(raw, it+24)))
    for j in range(D):
        it = d_start + 12*j
        d_nged.append(u32(raw, it+8))
    pos += span

ck('all_identity_relation', ident_ok == 251, f'{ident_ok}/251')
ck('spans_sum_24710', spans_sum == 24710, f'sum={spans_sum}')
ck('physical_closure_13_24710_9', pos == 24723 and len(raw) - pos == 9, f'pos={pos} footer={len(raw)-pos}')
ck('footer_9B', raw[pos:pos+9] == bytes.fromhex('0000000001ec7ae404'), raw[pos:pos+9].hex())
ck('collection_totals', tot == {'A':492,'B':214,'C':63,'D':162}, str(tot))
ck('items_931', sum(tot.values()) == 931, str(sum(tot.values())))
ck('row55_identity', row55 and row55[1] == (55,110,110), str(row55))
ck('perc_1_100', all(1 <= v <= 100 for v in perc_vals) and len(perc_vals)==492,
   f'min={min(perc_vals)} max={max(perc_vals)} n={len(perc_vals)}')
# date bit-split: year=high16, day=low9, mid7 bits zero
def split_date(v):
    return (v >> 16, v & 0x1ff, (v >> 9) & 0x7f)
bad_mid = [v for pair in bc_dates for v in pair if split_date(v)[2] != 0]
ck('bc_date_mid7_zero', not bad_mid, f'bad={len(bad_mid)} of {2*len(bc_dates)}')
years = [split_date(v)[0] for pair in bc_dates for v in pair]
days = [split_date(v)[1] for pair in bc_dates for v in pair]
ck('bc_date_year_range', all(1850 <= y <= 2100 or y==1900 for y in years), f'year min={min(years)} max={max(years)}')
ck('bc_date_day_range', all(0 <= d <= 366 for d in days), f'day min={min(days)} max={max(days)}')
# NGed default 1900-001 => year1900 day1 => (1900<<16)|1
nged_default = (1900<<16)|1
ck('NGed_all_default', all(v == nged_default for v in d_nged) and len(d_nged)==162,
   f'n={len(d_nged)} distinct={len(set(d_nged))}')

# fields grade tally
f = json.load(open(OUT/'fields_nation_client.json', encoding='utf-8'))
fields = f.get('fields') or f.get('client_fields') or []
if isinstance(f, dict) and 'fields' not in f and 'client_fields' not in f:
    print('fields keys:', list(f.keys()))
grades = {}
for x in fields:
    g = x.get('grade','?')
    grades[g] = grades.get(g,0)+1
l3 = sum(v for k,v in grades.items() if str(k).startswith('L3'))
ck('L3_total_25', l3 == 25, f'grades={grades}')

# static re-read: sample instruction records (decimal file_offset/VA per REPORT)
pe = PE(Path(r'D:/tmp2b/fm24/input/editor.exe'))
ck('pe_sha', hashlib.sha256(pe.raw).hexdigest() == 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4')
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)
recs = []
for p in sorted(OUT.glob('instructions.part*.json')):
    d = json.load(open(p, encoding='utf-8'))
    recs.extend(d if isinstance(d, list) else d.get('instructions', []))
ck('instruction_count_1912', len(recs) == 1912, f'n={len(recs)}')
import random
random.seed(28)
sample = random.sample(recs, min(40, len(recs)))
ok = 0
for r in sample:
    fo = int(r['file_offset']); va = int(r['VA']); wb = bytes.fromhex(r['bytes']) if isinstance(r['bytes'],str) else bytes(r['bytes'])
    if pe.va2f(va) == fo and pe.raw[fo:fo+len(wb)] == wb:
        di = list(md.disasm(pe.raw[fo:fo+15], va, count=1))
        if di and di[0].bytes == wb:
            ok += 1
ck('static_sample_40', ok == len(sample), f'{ok}/{len(sample)}')

print('---')
fails = [c for c in checks if not c[1]]
print(f't28 spot: {len(checks)-len(fails)}/{len(checks)} PASS', ('FAILS: '+str([c[0] for c in fails])) if fails else 'ALL GREEN')
sys.exit(1 if fails else 0)