#!/usr/bin/env python3
"""t113 people archive reconnaissance. Exit: 0 complete, 1 partial, 2 fatal/usage.
Uses only read-only input files; never opens or writes the source IDA database.
"""
from __future__ import annotations
import argparse, collections, hashlib, importlib.util, json, struct, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'scratch/t113/out'
DATA=ROOT/'scratch/data'
OLD=Path(r'D:\tmp2b\fm24\scripts\modding_read_dbdat.py')

def helper():
    spec=importlib.util.spec_from_file_location('t113_old_reader',OLD)
    if spec is None or spec.loader is None: raise RuntimeError(f'missing decoder: {OLD}')
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def digest(b): return hashlib.sha256(b).hexdigest()
def unpack(m,name):
    p=DATA/(name+'.dat'); blob=p.read_bytes()
    if blob[:8] != bytes.fromhex('03017461642ef10d') or blob[8:12] != bytes.fromhex('28b52ffd'):
        raise ValueError(f'{name}: unexpected tad/zstd framing')
    raw=m._stream_decompress(blob[8:],512*1024*1024)
    return p,blob,raw

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,default=OUT)
    ap.add_argument('--selftest',action='store_true')
    a=ap.parse_args()
    try:
        m=helper(); a.out.mkdir(parents=True,exist_ok=True); (a.out/'funcs').mkdir(exist_ok=True)
        inv={'status':'partial','source_model':'standalone tad. archives, not FMF directory entries','archives':{},'person_type_distribution':None,
             'distribution_note':'Not inferred: people_db.dat variable-record grammar/person_type offset is not closed in this workspace.'}
        raws={}
        for name in ('people_db','basic_people_db'):
            p,b,r=unpack(m,name); raws[name]=r
            inv['archives'][name]={'path':str(p),'file_bytes':len(b),'archive_sha256':digest(b),'header_13_bytes':b[:13].hex(),
                'zstd_offset':8,'decompressed_bytes':len(r),'payload_sha256':digest(r),'row_count_header_u32':struct.unpack_from('<I',r)[0] if name=='basic_people_db' else None,
                'payload_header_13_bytes':r[:13].hex(),'first_64_bytes':r[:64].hex(),'members':[{'name':name+'.dat','packed_bytes':len(b)-8,'unpacked_bytes':len(r),'member_count':1,'kind':'single zstd frame'}]}
        r=raws['basic_people_db']; n,flag=struct.unpack_from('<IB',r); lengths={1:83,2:83,3:83,4:34,5:22}; pos=5; hist=collections.Counter(); bad=0
        for i in range(n):
            if pos+2>len(r) or r[pos]!=0x11 or r[pos+1] not in lengths: bad+=1; break
            cls=r[pos+1]; hist[cls]+=1; pos+=lengths[cls]
        inv['archives']['basic_people_db'].update({'validated_row_count':sum(hist.values()),'row_type_histogram':dict(sorted(hist.items())),
            'row_chain_closed':bad==0 and pos+9==len(r),'row_chain_end':pos,'footer':r[pos:].hex()})
        inv['basic_people_layout']='header u32 count + u8 flag; row tag 0x11, class byte; widths {1:83,2:83,3:83,4:34,5:22}; 9-byte footer'
        (a.out/'people_archives_inventory.json').write_text(json.dumps(inv,indent=2,ensure_ascii=False),encoding='utf-8')
        # RTTI/vtable work is intentionally not mislabeled as complete: no class-name/vtable inventory was validated.
        vt={'status':'partial','classes':[],'note':'No verified RTTI scan / Hex-Rays class-slot pass was completed; do not treat empty classes as absence. Source i64 left untouched.'}
        (a.out/'people_vtables.json').write_text(json.dumps(vt,indent=2),encoding='utf-8')
        print(f"people_db={len(raws['people_db']):,} B basic_people_db={len(r):,} B; basic rows={n:,}; classes={dict(sorted(hist.items()))}; closed={inv['archives']['basic_people_db']['row_chain_closed']}")
        if a.selftest: return 0 if inv['archives']['basic_people_db']['row_chain_closed'] and flag==0 else 1
        return 1
    except Exception as e:
        print(f'ERROR: {e}',file=sys.stderr); return 2
if __name__=='__main__': sys.exit(main())
