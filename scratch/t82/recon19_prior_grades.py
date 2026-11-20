"""Cross-reference all t82 candidate club.xml fields against t57, t63, t71 prior grades & IDs,
plus check kit comp_uid / year domain and exact TC_GET2/CLUB_GET 100 STARTING_RECORD 4CC list."""
import json, struct, sys
from collections import Counter
from pathlib import Path

ROOT = Path(r'D:\tmp2b\fm24-db')
master = json.loads((ROOT / 'evidence/fm24/reports/editor_schema/master.json').read_bytes())
club_fields = master['entities']['club.xml'][0]['fields']
t57 = json.loads((ROOT / 'scratch/t57/out/field_map.json').read_bytes())
t63 = json.loads((ROOT / 'scratch/t63/out/field_map_r2.json').read_bytes())
t71 = json.loads((ROOT / 'scratch/t71/out/field_map_r3.json').read_bytes())

print('t57 keys:', list(t57.keys()))
print('t63 keys:', list(t63.keys()))
print('t71 keys:', list(t71.keys()))

t57_by_idx = {}
for e in (t57.get('fields') or t57.get('entries') or []):
    idx = e.get('xml_index')
    if idx is not None: t57_by_idx[idx] = e

t63_by_idx = {}
for e in (t63.get('fields') or t63.get('entries') or t63.get('records') or []):
    idx = (e.get('r1_id') or {}).get('xml_index')
    if idx is None:
        id_s = e.get('id', '')
        if '#' in id_s and '/' in id_s:
            idx = int(id_s.rsplit('/', 1)[1])
    if idx is not None: t63_by_idx[idx] = e

t71_by_idx = {}
for e in (t71.get('fields') or []):
    id_s = e.get('id', '')
    if '/' in id_s:
        t71_by_idx[int(id_s.rsplit('/', 1)[1])] = e

print(f'Loaded priors: t57={len(t57_by_idx)}, t63={len(t63_by_idx)}, t71={len(t71_by_idx)}')
print('t71 L3 indices:', sorted(t71_by_idx.keys()))
print('t71 L3 codes:', [t71_by_idx[k]['code'] for k in sorted(t71_by_idx.keys())])

watch = {
    'Ctlv','Cmle','Cyim','Cyfb','Cytv','Crcb','Csth','CScP','Cown','Chti',
    'Cetl','Cmtm','Cect','Cemn','Cemx','Cepr','Csly','Csps','Cspt','Csaf','Cste','Cspe',
    'Cuf1','Cuf2','Cuf3','Cuf4','Cuf5','Cuf6','Cuf7','Cuf8','Cuf9','Cf10',
    'TCht','TCnn','ttcl','tbcl','Catd','Cmna','Cmxa','Cpfr','C2pf','Cdfo','Cafo',
    'Cscm','CPsL','Cspb','Cren','TCrs','Tko1','Tkg1','Tko2','Tkg2','Tko3','Tkg3',
    'Csoc','Camc','Cbbl','pcpt','CssT','CssP','CssS','CssE',
    '1scl','1sbc','2scl','2sbc','3scl','3sbc','2tcl','2tbc','3tcl','3tbc',
    'CBWa','CBWc','CBWd','CBWf','CBWo','CBDa','CBDc','CBDd','CBDf','CBDo',
    'Crkt','Csxn','Cl3n','Ca3n','C1sq','Cmls','Cdbt','Cffp','Clhs','CAmb','Cmti','Cwcl','Coin','Calt'
}
print('\n=== PRIOR STATUS FOR ALL WATCHED CLUB.XML OCCURRENCES ===')
for idx, f in enumerate(club_fields):
    c = f['field']
    if c in watch:
        g57 = t57_by_idx.get(idx, {}).get('grade', '-')
        g63 = t63_by_idx.get(idx, {}).get('grade', '-')
        r63 = str(t63_by_idx.get(idx, {}).get('reason') or t63_by_idx.get(idx, {}).get('first_counterexample') or '')[:70]
        g71 = t71_by_idx.get(idx, {}).get('grade', '-')
        print(f'  [{idx:3d}] {c:5s} type={f["type"]:24s} t57={g57:10s} t63={g63:10s} t71={g71:4s} r63={r63}')

# Check if ANY t63 held/L3 exists in our watch list!
print('\n=== ALL t63 HELD FIELDS (41 total) ===')
for idx in sorted(t63_by_idx):
    e = t63_by_idx[idx]
    if e.get('grade') == 'held':
        print(f"  [{idx:3d}] {e.get('code') or e.get('field'):5s} reason={str(e.get('reason') or e.get('first_counterexample',''))[:95]}")
