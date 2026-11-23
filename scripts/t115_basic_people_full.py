#!/usr/bin/env python3
"""t115 basic people framing and anchor probe. Semantic columns are deliberately conservative."""
from __future__ import annotations
import argparse, ctypes, ctypes.util, json, struct, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'scratch/data/basic_people_db.dat'; OUT=ROOT/'scratch/t115/out'
COUNT=658011; END=54060034
WIDTH={1:83,2:83,3:83,4:34,5:22}
ANCHORS={28049320:{'label':'Harry Kane','ca':184,'pa':185,'year':1993},735216:{'label':'Cristiano Ronaldo','ca':160,'pa':200,'year':1985},7458500:{'label':'Lionel Messi','pa':200,'year':1987}}
def decompress(path=DATA):
 raw=path.read_bytes(); lib=ctypes.CDLL(ctypes.util.find_library('zstd') or ctypes.util.find_library('libzstd'))
 f=lib.ZSTD_decompress; f.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_size_t]; f.restype=ctypes.c_size_t
 err=lib.ZSTD_isError; err.argtypes=[ctypes.c_size_t]; err.restype=ctypes.c_uint
 src=ctypes.create_string_buffer(raw[8:]); dst=ctypes.create_string_buffer(54060043); n=f(dst,len(dst),src,len(raw)-8)
 if err(n) or n!=54060043: raise ValueError(f'zstd decode error/size {n}')
 return dst.raw[:n]
def scan(b):
 if struct.unpack_from('<I',b)[0]!=COUNT: raise ValueError('unexpected row count')
 p=5; rows=[]; hist={}
 for i in range(COUNT):
  if p>=len(b)-9 or b[p]!=0x11: raise ValueError(f'bad marker row {i} at {p}')
  t=b[p+1]
  if t not in WIDTH: raise ValueError(f'unknown type {t} row {i}')
  n=WIDTH[t]; r=b[p:p+n]; hist[t]=hist.get(t,0)+1
  # Type-2 observations: uid, CA/PA/year are independently checked against the supplied anchors.
  uid=struct.unpack_from('<I',r,75)[0] if n>=79 else None
  if t in (1,2,3):
   rows.append({'ordinal':i,'person_type':t,'uid':uid,'record_offset':p,'record_hex':r.hex()})
  p+=n
 if p!=len(b)-9: raise ValueError(f'closure mismatch {p} != {len(b)-9}')
 return rows,hist,p

def find_uid_record(rows,uid):
 return next((r for r in rows if r['uid']==uid),None)
def verify(b,rows):
 # Payload offsets named in the task identify the UID word, not the record start.
 expected={28049320:(13650120,184,185,1993),735216:(1594042,160,200,1985),7458500:(4317787,None,200,1987)}; checked=[]
 for uid,(uoff,ca,pa,year) in expected.items():
  r=find_uid_record(rows,uid)
  if not r: raise AssertionError(f'UID {uid} absent')
  if uoff != r['record_offset']+75: raise AssertionError(f'UID offset mismatch {uid}')
  q=r['record_offset']; raw=b[q:q+83]
  # Observed player core sequence: reputation, CA, PA, repeated/current ability, birth year.
  ca0,pa0,yr=struct.unpack_from('<HHH',raw,44) # year is not adjacent; replaced below
  yr=struct.unpack_from('<H',raw,52)[0]
  if ca is not None and ca0!=ca: raise AssertionError(f'CA {uid}: {ca0}')
  if pa0!=pa: raise AssertionError(f'PA {uid}: {pa0}')
  if yr!=year: raise AssertionError(f'year {uid}: {yr}')
  checked.append({'uid':uid,'label':ANCHORS[uid]['label'],'record_offset':q,'uid_offset':uoff,'ca':ca0,'pa':pa0,'birth_year':yr,'verified':True})
 return checked

def build():
 b=decompress(); rows,hist,end=scan(b); anchors=verify(b,rows)
 # Stable top list by observed CA word; semantic player designation and club/nation join are not asserted.
 ranked=[]
 for r in rows:
  if r['person_type'] not in (2,3): continue
  raw=bytes.fromhex(r['record_hex']); ranked.append({'uid':r['uid'],'person_type':r['person_type'],'CA_observed_u16_at_record_plus_44':struct.unpack_from('<H',raw,44)[0],'PA_observed_u16_at_record_plus_46':struct.unpack_from('<H',raw,46)[0],'record_offset':r['record_offset']})
 ranked.sort(key=lambda x:(-x['CA_observed_u16_at_record_plus_44'],x['uid'] or 0)); top=ranked[:30]
 schema={'status':'partial','reason':'Framing/closure and three UID anchors are validated. A complete semantic wire map, name-table join, nation/club identifiers, and independently verified all-player ranking are not established by the supplied evidence; no L3 completion is claimed.','source_files':['scratch/t95/funcs/140e4fd70.c','scratch/t95/funcs/140e50cd0.c','scratch/t113/out/funcs/1410992c0.c'],'framing':{'count':COUNT,'row_chain_end':end,'expected_end':len(b)-9,'diff':end-(len(b)-9),'histogram':hist,'width_including_marker_and_type':WIDTH},'anchor_checks':anchors,'top30_observed_CA_candidates':top,'field_evidence':[{'field':'record marker','offset':'row+0','type':'u8','evidence':'t114 validated framing'}, {'field':'person_type','offset':'row+1','type':'u8','evidence':'factory mapping 1/2/3/4/6 conflicts with observed on-disk type 5; mapping unresolved'}, {'field':'uid','offset':'row+75','type':'u32','evidence':'three supplied UID anchors locate exact words'}, {'field':'CA/PA candidate','offset':'row+44 / row+46','type':'u16','evidence':'Kane/Ronaldo/Messi anchor values match'}, {'field':'birth-year candidate','offset':'row+52','type':'u16','evidence':'three supplied anchor years match; semantic layout still requires full C correlation'}]}
 OUT.mkdir(parents=True,exist_ok=True); (OUT/'basic_people_l3_schema.json').write_text(json.dumps(schema,indent=2),encoding='utf-8')
 report=['# t115 — basic people framing and anchor verification','','**Status: partial, not L3 complete.** The exact requested semantic completion cannot be responsibly asserted: supplied C excerpts do not by themselves establish all serialized field mappings, and the on-disk type histogram includes type 5 although the supplied factory excerpt lists type 6.','',f"Rows: {COUNT:,}; chain end: {end:,}; expected `len(payload)-9`: {len(b)-9:,}; diff: {end-(len(b)-9)}.",'','## Frame counts','']+[f'- type {k}: {v:,}' for k,v in sorted(hist.items())]+['','## Anchor checks','','| UID | Name | CA candidate | PA candidate | Year candidate | Result |','|---:|---|---:|---:|---:|---|']+[f"| {a['uid']} | {a['label']} | {a['ca']} | {a['pa']} | {a['birth_year']} | verified at supplied UID offset |" for a in anchors]+['','## CA candidates','', 'Candidate ordering uses the observed u16 at record+44 only; it is not presented as an authenticated FM24 Top 30. See JSON for the list.','', '## Source interpretation caveat','', '`140e4fd70.c` establishes conditional reads into in-memory offsets +32..+104 and invokes `sub_141084540`; `140e50cd0.c` is a property dispatcher, not a wire-schema declaration. Exact name/date/nation/club semantics and name-table join remain unresolved.']
 (OUT/'REPORT.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
 (OUT/'DONE.md').write_text(f"DONE type=t115\n\nValidated framing and anchor probe (partial semantic status): {COUNT:,} rows; exact closure diff={end-(len(b)-9)}; type histogram {json.dumps(hist,sort_keys=True)}; verified anchors={len(anchors)}.\n",encoding='utf-8')
 print(json.dumps({'files':[str(OUT/x) for x in ('basic_people_l3_schema.json','REPORT.md','DONE.md')],'rows':COUNT,'end':end,'diff':end-(len(b)-9),'histogram':hist,'anchors':anchors},indent=2))
def main():
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--selftest',action='store_true'); ap.add_argument('--uid',type=int); ap.add_argument('--top',type=int); a=ap.parse_args()
 try:
  b=decompress(); rows,hist,end=scan(b)
  if a.selftest:
   checks=verify(b,rows); assert len(rows)>0 and end==len(b)-9 and hist=={1:166064,2:476158,3:4757,4:9839,5:1193}; print('selftest: framing and anchor checks OK; semantic L3 incomplete'); return 0
  if a.uid is not None:
   r=find_uid_record(rows,a.uid); print(json.dumps(r,indent=2) if r else 'UID not found'); return 0 if r else 1
  if a.top is not None:
   candidates=[]
   for r in rows:
    if r['person_type'] in (2,3):
     x=bytes.fromhex(r['record_hex']); candidates.append((struct.unpack_from('<H',x,44)[0],r['uid'],r['person_type']))
   candidates.sort(reverse=True); print(json.dumps([{'CA_observed':x,'uid':u,'person_type':t} for x,u,t in candidates[:a.top]],indent=2)); return 0
  build(); return 0
 except Exception as e: print(f'ERROR: {e}',file=sys.stderr); return 1
if __name__=='__main__': raise SystemExit(main())
