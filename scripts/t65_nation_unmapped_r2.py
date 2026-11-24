#!/usr/bin/env python3
"""t65: bounded second-pass Nation table_10 main-row projection census."""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
from collections import Counter, deque
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch/t65/out'
T55 = ROOT / 'scratch/t55/out'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
EXEH = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
SIDES = ('client', 'server')
MAIN = 0x103fac0
CLAIMS = {
    # gate, actual source, path witness (not a claim to have followed callbacks)
    'Nnam': (0x1042222, 'name wrapper carrying this + lang selector long', [0x1042cde, 0x1042d62, 0x1042daf]),
    'Nsnm': (0x104225c, 'this+0x20 string pointer, not a t10 transfer', [0x1042fde, 0x1042ff8]),
    'N3ln': (0x10420a1, 'this+0x28 string pointer, not a t10 transfer', [0x10425a3, 0x10425bd]),
    'Nnty': (0x1041f9c, 'this+0x30 string pointer, not a t10 transfer', [0x1042627, 0x1042641]),
    'nhrl': (0x104251e, 'compares bounds at [this+0x108]+0x4a0/0x4a8; not a scalar bit load', [0x104252a, 0x1042532, 0x1042539, 0x1042545, 0x1042548]),
    'dbnm': (0xfe375d, 'virtual name provider and formatter; no proven t10 cursor', [0xfe3774, 0xfe3796]),
    'ttcl': (0xfe35bc, 'virtual lookup through Nation+0xf0 or fcol fallback; not a Nation colour sink', [0xfe35d4, 0x1041eb0, 0xfe35ea, 0xfe3600]),
    'tbcl': (0xfe3980, 'virtual lookup through Nation+0xf0 or bcol fallback; not a Nation colour sink', [0xfe3f37, 0x1041eb0, 0xfe3f4d, 0xfe3f63]),
    'rdui': (0xfe3862, 'base getter exposes this+0x10 only if distinct from this+0xc', [0xfe389d, 0xfe38a2, 0xfe38a7, 0xfe38b6]),
}
# Collection item activation is subordinate to the outer (mode) gate.
ITEM_GATES = {2:0x103fc63, 3:0x103ff2a, 4:0x1040144, 11:0x1040485, 12:0x10404e3, 13:0x3d74f70,
              23:0x104073b, 24:0x10407d6, 25:0x1040898, 26:0x1040980}


class Check(Exception): pass


def ck(ok, msg):
    if not ok: raise Check(msg)


def H(buf): return sha256(buf).hexdigest()
def J(path): return json.loads((ROOT / path).read_bytes())
def U(buf, at=0): return struct.unpack_from('<I', buf, at)[0]
def hist(seq): return {str(k): v for k, v in sorted(Counter(seq).items())}
def canon(v): return json.dumps(v, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()


def inputs():
    names = ['field_slots.json', 'field_map.json', 'REPORT.md', 'branches.part001.json']
    names += sorted(p.name for p in T55.glob('instructions.part*.json'))
    files = [f'scratch/t55/out/{n}' for n in names] + ['scratch/t59/out/REPORT.md', 'scratch/t53/out/REPORT.md', 'scratch/t61/out/REPORT.md', MASTER, PROV]
    hashes = {s:H((ROOT/s).read_bytes()) for s in files}
    manifest = {x['path']:x['sha256'] for x in J('evidence/MANIFEST.json')['files']}
    ck(all(hashes[p]==manifest[p] for p in (MASTER, PROV)), 'evidence MANIFEST')
    ck(EXEH in (ROOT/PROV).read_text(encoding='utf-8'), 'binary provenance')
    fm, sl = J(T55/'field_map.json'), J(T55/'field_slots.json')
    pub = J('reports/club_nation_subtable_schema.json'); sec = pub['nation_main_row_fields']
    ck(sec['acceptance_ledger_entry']=='E94' and sec['source_records']['field_slots']==sl and sec['source_records']['field_map']==fm, 'public E94 conflict')
    mast = J(MASTER); fs = mast['entities']['nation.xml'][0]['fields']
    ck(len(fs)==346 and fs==[x['schema'] for x in fm['fields']] and hashes[MASTER]==fm['frozen_sha256'], 'schema freeze')
    ck(sum(x['grade']=='unmapped' for x in fm['fields'])==327, 'unmapped denominator')
    return sl, fm, mast['enums'], dict(files=hashes, public_schema_version=pub['schema_version'],
                                     public_nation_main_row_fields_sha256=H(canon(sec)))


def archives(sl):
    depot = Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
    old = ROOT.parent/'fm24'
    for p in (depot, old):
        if p.drive.upper()=='Z:' or p.resolve().drive.upper()=='Z:': raise ValueError('Z: forbidden')
    sys.path.append(str(old/'tools/python'))
    import zstandard
    entries = runpy.run_path(str(old/'scripts/modding_read_dbdat.py'))['_entries']
    b = {}
    for side in SIDES:
        _, blob, idx = entries(depot/f'{side}_db.dat')
        md = sl['archive'][side]; base = idx['data_base']; index = {x['path']:x for x in idx['entries']}
        ck((base,len(index),H(blob))==(md['data_base'],md['entries'],md['archive_sha256']), (side,'archive'))
        for t in ((10,21) if side=='server' else (10,)):
            e = index[f'{side}_db/table_{t}.dat']; a = base+e['offset']; end = a+e['packed_size']; p = a
            bound = min((base+x['offset'] for x in index.values() if x['offset']>e['offset']),default=idx['toc_offset'])
            saved = md['members'][str(t)]; found = []; frames = []
            ck(base<=a<end<=bound and (a,end,bound)==(saved['start'],saved['end'],saved['neighbor_bound']), (side,t,'frame boundaries'))
            while p < end:
                ck(blob[p:p+4]==b'\x28\xb5\x2f\xfd',(side,t,p,'zstd magic'))
                dec=zstandard.ZstdDecompressor().decompressobj(); raw=dec.decompress(blob[p:end]); q=end-len(dec.unused_data)
                ck(dec.eof and q>p,(side,t,p,'zstd EOF')); f=[p,q,len(raw)]; frames.append(f); p=q
                if len(raw)==e['size']: found.append((raw,f))
            ck(len(found)==1 and frames==saved['frames'], (side,t,'declared-size frame'))
            raw,f=found[0]
            ck(f==saved['selected'] and H(raw)==saved['payload_sha256'], (side,t,'payload hash'))
            b[side,t]=raw
    return b


def emit(name, value):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def pnt(row, at, raw, value): return {'row':row,'absolute':at,'raw':raw.hex(),'value':value}


def replay(raw, slots, side, mode):
    ck(raw[:8]==bytes.fromhex('03017461642ef10d') and U(raw,8)==251, (side,'header'))
    p=13; ids=[]; picks={s['position']:[] for s in slots}; end=len(raw)-9
    formats={'i8':'<b','i16':'<h','i32':'<i','u32':'<I'}
    order=[s for s in slots if mode in s['modes']]
    for row in range(251):
        for s in order:
            i=s['position']; w=s['width']; a=p; p+=w; count=None
            ck(p<=end,(side,row,a,'short'))
            if s['type']=='collection':
                count=struct.unpack_from(formats[s['count_type']],raw,a)[0]
                ck(count>=0,(side,row,a,'negative count',count))
                stride=s['collection']['stride']
                if stride is None:
                    # Closed Nftb/Ntxr: consume the accepted opaque span, never inspect items.
                    coords=s['coordinates'][side]
                    ck(len(coords)==251 and coords[row][0]==a,(side,row,a,'opaque t55 start'))
                    p=a+coords[row][1]
                else:
                    ck(count<=(end-p)//stride,(side,row,a,'count overrun',count)); p+=count*stride
            ck(p<=end,(side,row,a,'span'))
            picks[i].append((a,raw[a:p],count))
            if i==0: ck(raw[a]==0,(side,row,a,'selector'))
            if i==39:
                j,u,v=struct.unpack_from('<III',raw,a)
                ck(j==row and u==v!=0,(side,row,a,'identity',(j,u,v))); ids.append(u)
    ck(raw[p:]==bytes.fromhex('0000000001ec7ae404') and len(set(ids))==251,(side,'EOF/UID'))
    ck(all([[a,len(b)] for a,b,_ in picks[s['position']]]==s['coordinates'][side] for s in slots),(side,'t55 all coordinates'))
    return picks, ids


def slot_stats(cells, s):
    if not cells: return {'rows':0,'condition':'external mode != 0; t55 client replay uses mode 0'}
    c=s['type']=='collection'; values=[n if c else int.from_bytes(b,'little') for _,b,n in cells]
    a,b,_=cells[0]; first=pnt(0,a,b[:s['width']],values[0]); i=next((i for i,v in enumerate(values) if v),None)
    q=dict(rows=len(cells),bytes=sum(len(b) for _,b,_ in cells),sha256=H(b''.join(b for _,b,_ in cells)),
           first=first, distinct=len(set(values)), min=min(values),max=max(values))
    if c:
        q.update(items=sum(values),empty_rows=values.count(0),count_hist=hist(values),
                 first_nonempty=None if i is None else pnt(i,cells[i][0],cells[i][1][:s['width']],values[i]),
                 span_range=[min(len(b) for _,b,_ in cells),max(len(b) for _,b,_ in cells)])
    return q


def join(samples, ordinal_uid, sentinel=0xffffffff):
    inverse={u:o for o,u in ordinal_uid.items()}
    def first(cond): return next((p for p in samples if cond(p['value'])),None)
    v=[p['value'] for p in samples]; live=[x for x in v if x!=sentinel]
    collision=first(lambda x:x!=sentinel and x in ordinal_uid and x in inverse and ordinal_uid[x]!=x)
    if collision:
        x=collision['value']; collision={**collision,'ordinal_to_UID':ordinal_uid[x],'UID_to_ordinal':inverse[x]}
    return dict(rows=len(v),ordinal_hit=sum(x in ordinal_uid for x in live),ordinal_miss=sum(x not in ordinal_uid for x in live),
                null=len(v)-len(live),wrong_UID_hit=sum(x in inverse for x in live),wrong_UID_miss=sum(x not in inverse for x in live),
                first_ordinal_miss=first(lambda x:x!=sentinel and x not in ordinal_uid),first_wrong_UID_miss=first(lambda x:x!=sentinel and x not in inverse),
                first_collision_distinct_owner=collision)


def stadium(raw, side, d):
    n=U(raw,8); width=181 if side=='server' else 38; end=13+n*width
    ck(end+9==len(raw) and raw[end:end+5]==bytes.fromhex('0000000001'), (side,'t21 EOF'))
    pos=[13+(i+1)*width-12 for i in range(n)]
    triples=[struct.unpack_from('<III',raw,p) for p in pos]
    ck(all((i==j and a==b!=0 and raw[p+12]==0) for i,(p,(j,a,b)) in enumerate(zip(pos,triples))), (side,'t21 keys'))
    v={j:a for j,a,_ in triples}
    ck(len(set(v.values()))==n==d['count'] and H(b''.join(raw[p:p+12] for p in pos))==d['identity_sha256'],(side,'t21 key hash'))
    return v


def data(sl, raw):
    slots=sl['slots']; cells={}; ids={}; envelopes={}; controls={}; vals={}
    for side in SIDES:
        b=raw[side,10]; cells[side],ids[side]=replay(b,slots,side,int(side=='server'))
        envelopes[side]=dict(rows=251,bytes=len(b),first_selector=13,identity_bytes=12,footer_at=len(b)-9,
                             selector_hist=hist(x[1][0] for x in cells[side][0]),mode=int(side=='server'),
                             execution_positions=[s['position'] for s in slots if s['coordinates'][side]])
        vs=[]; suppressed=0
        for row,(a,p,_) in enumerate(cells[side][39]):
            uid,random=struct.unpack_from('<II',p,4); suppressed+=(uid==random); vs.append(pnt(row,a+8,p[8:12],random))
        vals[side]=dict(status='held_getter_suppressed',rows=251,suppressed=suppressed,exposed=251-suppressed,
                        raw_unsigned_range=[min(x['value'] for x in vs),max(x['value'] for x in vs)],
                        raw_values_sha256=H(b''.join(bytes.fromhex(x['raw']) for x in vs)),xml_min=None,xml_max=None,xml_enum_ref=None,
                        first_unexposed=vs[0])
        ck(suppressed==251,(side,'rdui suppression'))
        refs={i:u for i,u in enumerate(ids[side])}
        t21=stadium(raw[side,21],side,sl['targets'][side]['21']) if side=='server' else None
        def samples(i):return [pnt(row,a,w,int.from_bytes(w,'little')) for row,(a,w,_) in enumerate(cells[side][i])]
        controls[side]=dict(rdui_identity_NOT_reference=join(vs,refs),t10_target_count=len(refs),
                            raw_t10_hypotheses={str(i):join(samples(i),refs) for i in (5,6,7,21,35,36) if cells[side][i]},
                            Nnsi_prior_control=(join(samples(1),t21) if t21 else {'status':'bypassed_mode'}))
    ck(ids['client']==ids['server'],'cross-archive keys')
    common=[s['position'] for s in slots if s['coordinates']['client']]
    ck(len(common)==15 and len(slots)==40,'mode cardinality')
    ck(all(c[1]==d[1] for i in common for c,d in zip(cells['client'][i],cells['server'][i],strict=True)), 'common bytes')
    only=[]
    for s in slots:
        i=s['position']
        if i in common:continue
        only.append(dict(position=i,site=s['site'],object_displacement=s['object_displacement'],wire_type=s['type'],
                         t55_code=s['candidate_4cc'],gate=0x103fae6 if i<14 else 0x10409d3,
                         item_gate=ITEM_GATES.get(i),transfer=s['transfer'],collection=s.get('collection'),
                         client=slot_stats([],s),server=slot_stats(cells['server'][i],s)))
        only[-1]['classification'] = ({1:'prior_reference',4:'frozen_parent',11:'frozen_parent',34:'out_of_frozen_schema',37:'prior_word_bit'}
                                      .get(i,'opaque_collection' if 'collection' in s else 'unnamed_fixed_transfer'))
    tag78=[pnt(r,a+k,b[k:k+1],b[k]) for r,(a,b,n) in enumerate(cells['server'][13]) for k in range(4,4+14*n,14)]
    opaque78=dict(items=len(tag78),header_byte_hist=hist(x['value'] for x in tag78),first=tag78[0],
                  item_wire_width=14,header_semantics='unlabelled; one byte read to stack, not a keyed getter field')
    for side in SIDES:
        env=envelopes[side]; env['payload_sha256']=H(raw[side,10]); env['body_bytes']=env['footer_at']-13
    replay_rejections={}
    for side,at,w,label,value in (('client',7188,4,'extra_158 count',1507845),('server',38,1,'A count',-90)):
        bb=raw[side,10][at:at+w]
        ck(int.from_bytes(bb,'little',signed=True)==value,(side,'t55 wrong-mode witness'))
        replay_rejections[side]={**pnt(0,at,bb,value),'label':label,'forced_mode':int(side=='client'),'source':'t55 first bad transfer; raw bytes rechecked'}
    return dict(envelopes=envelopes,common_byte_equal_rows={str(i):251 for i in common},server_only=only,
                opaque_78_item_header=opaque78,reference_controls=controls,wrong_mode_witnesses=replay_rejections), vals


# Only main-row related regions. Calls/edges crossing this frontier are not explored.
REGIONS = {'local_get':0x1041f40,'base_get':0xfe3520,'helper_78':0x3d74e30,
           'item_78':0x3daa110,'packed_date':0x39dd7b0,'identity':0x3c600f0}


def reachable(graph, start, stop=()):
    seen=set(); todo=deque([start])
    while todo:
        k=todo.popleft()
        if k in seen or k in stop:continue
        seen.add(k); todo.extend(graph.get(k,()))
    return seen


def static(sl, fm):
    import pefile
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_IMM, CS_OP_MEM
    path=ROOT.parent/'fm24/input/editor.exe'
    if path.drive.upper()=='Z:' or path.resolve().drive.upper()=='Z:': raise ValueError('Z: forbidden')
    raw=path.read_bytes(); ck(H(raw)==EXEH==sl['source']['editor_SHA256'],'editor binary SHA')
    pe=pefile.PE(data=raw,fast_load=True); pe.parse_data_directories(directories=[3]); base=pe.OPTIONAL_HEADER.ImageBase
    va=lambda f:base+pe.get_rva_from_offset(f)
    off=lambda a:pe.get_offset_from_rva(a-base)
    runtime={x.struct.BeginAddress:x.struct.EndAddress for x in pe.DIRECTORY_ENTRY_EXCEPTION}
    cap=Cs(CS_ARCH_X86,CS_MODE_64);cap.detail=True
    def dec(o):return next(cap.disasm(raw[o:o+15],va(o),1))
    def direct(i):
        return off(i.operands[0].imm) if i.operands and i.operands[0].type==CS_OP_IMM else None
    def blob(o,n):return dict(file_offset=o,VA=va(o),bytes=raw[o:o+n].hex())
    def rec(o):
        i=dec(o); d={**blob(o,i.size),'instruction':(i.mnemonic+' '+i.op_str).strip()}
        if i.mnemonic.startswith('j') or i.mnemonic=='call':d['direct_target']=direct(i)
        return d
    records=[r for f in sorted(T55.glob('instructions.part*.json')) for r in J(f)]
    main={r['file_offset']:r for r in records if r.get('function')==MAIN}
    graph={o:r['successors'] for o,r in main.items()}
    ck(len(main)==992 and reachable(graph,MAIN)==set(main),'t55 main CFG')
    for o,r in main.items(): ck(all(r[k]==v for k,v in rec(o).items()),('t55 static fragment',o))
    branches={x['site']:x for x in J(T55/'branches.part001.json')}
    region={}; ops={'main':{o:dec(o) for o in sorted(main)}}
    for name,e in REGIONS.items():
        end=off(base+runtime[va(e)-base]); todo=[e]; ins={}; exits=[]
        while todo:
            o=todo.pop()
            if o in ins:continue
            i=dec(o); ins[o]=i; q=o+i.size
            if i.mnemonic in ('ret','retf','int3','ud2'): nx=()
            elif i.mnemonic=='jmp': nx=(direct(i),)
            elif i.mnemonic.startswith('j'): nx=(direct(i),q)
            else:nx=(q,)
            for y in nx:
                if y is not None and e<=y<end:todo.append(y)
                else:exits.append([o,y])
        ops[name]=dict(sorted(ins.items()))
        region[name]=dict(entry=e,end_exclusive=end,reachable=len(ins),external_edges=sorted(exits),
                          addresses_sha256=H(canon(sorted(ins))))
    vt=off(sl['source']['nation_vtable_VA'])
    vslots={str(n):{**blob(vt+8*n,8),'target':off(struct.unpack_from('<Q',raw,vt+8*n)[0])} for n in (2,10,19,25)}
    ck(vslots['2']['target']==0x1041f30 and direct(dec(0x1041f33))==REGIONS['local_get'] and vslots['19']['target']==MAIN,'Nation vtable linkage')
    code_to_fields={int.from_bytes(x['code'].encode(),'big'):x for x in fm['fields']}
    gates=[]
    for name in ('local_get','base_get'):
        for o,i in ops[name].items():
            if i.mnemonic!='cmp' or i.operands[-1].type!=CS_OP_IMM:continue
            f=code_to_fields.get(i.operands[-1].imm); nxt=o+i.size; j=ops[name].get(nxt)
            if f is None or j is None or j.mnemonic not in ('je','jne'):continue
            eq=direct(j) if j.mnemonic=='je' else nxt+j.size
            gates.append(dict(region=name,code=f['code'],xml_index=f['xml_index'],baseline_grade=f['grade'],gate=o,branch=nxt,equal_edge=eq))
    ck({(g['code'],g['gate']) for g in gates if g['baseline_grade']=='unmapped'}=={(k,v[0]) for k,v in CLAIMS.items()}, 'unmapped gate census changed')
    bitops=[]
    for name, ii in ops.items():
        for o,i in ii.items():
            if i.mnemonic not in ('shr','sar','shl','and','bt','bts','btr','btc'):continue
            if o in (0x1043605,0x1043608):role='t55 Nndn existing word projection'
            elif o in (0x10427a9,0x10427c6,0x10427db,0x1042853):role='packed date comparison on +0xc0 item or context, not a new top-level boolean'
            elif 0x10428ba<=o<=0x1042bb1:role='referenced object handle packaging, not a row-field bit'
            elif o in (0x10439e8,0x1043a4e):role='getter context/availability test, not a row-field bit'
            else:role='shift/scale in vector arithmetic, not a keyed boolean'
            bitops.append(dict(region=name,role=role,**rec(o)))
    ck(dec(0x1043605).op_str=='esi, 9' and dec(0x1043608).op_str=='sil, 1','t55 bit control')
    transfers={}
    for name in ('helper_78','item_78','packed_date','identity'):
        transfers[name]=[o for o,i in ops[name].items() if i.mnemonic=='call' and i.operands[0].type==CS_OP_MEM and i.operands[0].mem.disp==0x28]
    ck(transfers=={'helper_78':[0x3d74e62], 'item_78':[0x3daa131,0x3daa150,0x3daa170,0x3daa18c,0x3daa1a8,0x3daa1c4,0x3daa1e0,0x3daa209],
                   'packed_date':[0x39dd7d4], 'identity':[0x3c60119]}, 'helper transfer census')
    ck([dec(x).operands[1].imm for x in (0x3daa128,0x3daa144,0x3daa167,0x3daa183,0x3daa19f,0x3daa1bb,0x3daa1d7,0x3daa1fd)]==[1,4,4,1,1,1,1,1], 'helper 78 item widths')
    # Both mode gates use the same caller byte. Compute client reachability by pruning only these two fallthroughs.
    mode_edges={g:branches[g] for g in (0x103fae6,0x10409d3)}
    mode0=reachable({**graph,**{g:[b['taken']] for g,b in mode_edges.items()}},MAIN)
    outer=[]; tri=[]
    for s in sl['slots']:
        i=s['position']; pc=s['site']
        if i in (0,39):continue
        rep=0x1040592 if i==13 else pc
        mode_gate=0x103fae6 if i<14 else 0x10409d3 if i>=27 else None
        ck((rep in mode0)==(0 in s['modes']),('mode 0 reachability',i))
        if mode_gate is not None:
            ck(rep not in reachable(graph,MAIN,(mode_gate,)) and rep in reachable(graph,mode_edges[mode_gate]['fallthrough']),('mode dominance',i))
            outer.append(dict(position=i,outer_gate=mode_gate,main_site=rep,cursor=pc,client_reachable=False))
        if 'collection' in s:
            call=s['collection']['item']; target=direct(dec(call))
            chain=[call] if target is None else [call,target]
            if i==12:chain.extend([0x104053f,0x1040554,0xdb7f80,0x39dd7b0,0x39dd7d4])
            if i==13:chain=[0x1040592,0x104e6b0,0x3d74e30,call,0x1072560,0x3daa110,*transfers['item_78']]
            item_gate=ITEM_GATES[i]; br=dec(item_gate)
            ck(br.mnemonic in ('je','jle'),('empty collection edge',i))
            tri.append(dict(position=i,code=s['candidate_4cc'],mode_gate=mode_gate,count_cursor=pc,item_gate=item_gate,
                            item_activation='count != 0' if br.mnemonic=='je' else 'count > 0',
                            empty_edge=direct(br),item_path=chain,wire_stride=s['collection']['stride'],member=s['object_displacement'],
                            scope='prior parent span only' if s['candidate_4cc'] else 'opaque, no exact top-level getter binding'))
    claims=[]
    for k,(g,why,ins) in CLAIMS.items():
        row=next(x for x in gates if x['gate']==g)
        claims.append(dict(**row,member_route=why,helper_route=ins,
            cursor=0x3c60119 if k=='rdui' else None,wire_lane=[8,4] if k=='rdui' else None))
    claims.sort(key=lambda x:x['xml_index'])
    aux={0xf2ba38,0xf2ba51,0x103fadc,0x103fae4,0x10409cb,0x1041f30,0x1041f33,0x1043306,0x1043309,0x104330f,
         0x104331a,0x1043322,0x104332b,0x1043331,0x1043334,0x104334d,0x1040bcf,0xfae340,0x3c60106,0x3c6010d,
         0x3c60119,0x3c60138,0x3c60149,0x3d74e5c,0x3d74e62,0x3d74f6e,0x10426ab,0x10426b2,0x10426d0,0x10426d6,0x10435f3,0x1043605,0x1043608}
    aux.update(y for x in claims for y in x['helper_route']); aux.update(y for x in gates for y in (x['gate'],x['branch']))
    aux.update((0xfe354b,0xfe3560,0xfe3562,0xfe4b47,0xfe4b71,0x1041eb0,0x1042790,0x10427a4,0x10427bf,0x10427d6,0x104284c))
    aux.update(y for x in tri for y in (*x['item_path'],x['item_gate'],x['count_cursor']))
    aux.update((0x39dd7c8,0x3daa128,0x3daa144,0x3daa167,0x3daa183,0x3daa19f,0x3daa1bb,0x3daa1d7,0x3daa1fd))
    return dict(editor=dict(path=str(_cfg.EDITOR_EXE),sha256=EXEH),main_cfg='t55/E94: 992 instructions, 109 conditional branches',
                regions=region,vslots=vslots,exact_frozen_gates=gates,unmapped_gate_trials=claims,shift_mask_inventory=bitops,
                helper_transfer_sites=transfers,collection_gate_helper_cursor=tri,server_only_static=outer,
                mode_edges=list(mode_edges.values()),base_fallback_boundary={'linked_pointer_call':0x1043322,'followed':False,'base_tail':0x104334d,
                    'registry_compare':0xfe3560,'virtual_forward':0xfe4b47,'Nation_virtual_50':0x1041eb0,'virtual_50_member':0xf0},
                instructions=[rec(o) for o in sorted(aux)])


def fieldmap(fm,enums,proj,rdui):
    candidates={x['code']:x for x in proj['static']['unmapped_gate_trials']}
    summary=Counter(); rows=[]
    for f in fm['fields']:
        code=f['code']; schema=f['schema']; grade=f['grade']; trial=candidates.get(code)
        d=dict(xml_index=f['xml_index'],code=code,t55_grade=grade,grade=grade)
        if grade!='unmapped': d['status']='unchanged_e94'; rows.append(d);continue
        d['schema_domain']={k:schema[k] for k in ('type','min_value','max_value','max_length','enum_ref','database_table_type','is_optional') if k in schema}
        ref=schema.get('enum_ref')
        if ref:
            d['schema_domain']['enum_definition_rows']=len(enums.get(ref,{}).get('values',[]))
        if trial is None:
            d.update(status='no_bounded_exact_getter_gate',domain_status='not_evaluable_without_wire_binding')
        elif code=='rdui':
            ck(schema['type']=='integer' and not any(k in schema for k in ('min_value','max_value','enum_ref')),'rdui frozen domain')
            d.update(grade='held',status='same_member_wire_but_getter_suppressed',slot=39,wire_lane=[8,4],
                     domain_status='no_exposed_samples',archives=rdui,first_counterexample=rdui['client']['first_unexposed'])
        else:
            d.update(grade='held',status='getter_proven_but_no_main_row_sink',domain_status='no_bound_samples',slot=None,
                     first_counterexample={'kind':'static_member_or_helper_mismatch','gate':trial['gate'],'source':trial['member_route'],
                                           'first_evidence':trial['helper_route'][0],'absolute':None})
        if trial: d['projection_gate']=trial['gate']
        summary[d['grade']]+=1; rows.append(d)
    return dict(scope='frozen nation.xml#nation top-level occurrences only; delta, not a replacement for E94',
                before=fm['grade_counts'],round2_of_327=dict(summary),new_L3=summary['L3'],L4=0,
                public_schema_changed=False,fields=rows)


def build():
    sl,fm,enums,prov=inputs(); raw=archives(sl)
    profiles,rdui=data(sl,raw); st=static(sl,fm)
    proj=dict(scope='t10 main row only',coordinates='absolute offsets in decompressed member; ordinal zero-based; static offsets are PE file offsets',
              provenance=prov,static=st,**profiles)
    f=fieldmap(fm,enums,proj,rdui)
    emit('projections.json',proj); emit('field_map_r2.json',f)
    print(f't65: 251+251 rows; server-only {len(profiles["server_only"])}; {f["round2_of_327"]}; L3 +{f["new_L3"]}')


def selftest():
    o={0:5,1:7,2:1}; s=[pnt(i,8+4*i,v.to_bytes(4,'little'),v) for i,v in enumerate((0,1,9,0xffffffff))]
    j=join(s,o);ck((j['ordinal_hit'],j['wrong_UID_hit'],j['ordinal_miss'],j['null'])==(2,1,1,1),'ordinal/UID/null test')
    ck(j['first_collision_distinct_owner']['UID_to_ordinal']==2,'collision control')
    ck(reachable({1:[2,3],2:[4],3:[4]},1,(2,))=={1,3,4},'gate pruning')
    print('t65 builder selftest: OK')


def main():
    p=argparse.ArgumentParser(description=__doc__); g=p.add_mutually_exclusive_group()
    g.add_argument('--build',action='store_true',help='generate both JSON artifacts (default)');g.add_argument('--selftest',action='store_true')
    args=p.parse_args()
    try:
        selftest() if args.selftest else build();return 0
    except Check as e:print(f't65 check failed: {e}',file=sys.stderr);return 1
    except Exception as e:print(f't65 fatal: {type(e).__name__}: {e}',file=sys.stderr);return 2


if __name__=='__main__':sys.exit(main())
PY