#!/usr/bin/env python3
"""Club table_3 R2: bounded dispatch census and full-archive projection gates."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from decimal import Decimal
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import runpy
import struct as S
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'scratch/t63/out'
R1 = ROOT/'scratch/t57/out'
EXE = ROOT.parent/'fm24/input/editor.exe'
EXEH = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
BIG = 'evidence/fm24/reports/dbdat_decode/db_tables_big.json'
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
SCHEMA = 'reports/club_nation_subtable_schema.json'
INPUTS = ['scratch/t57/out/'+f for f in ('field_slots.json','field_map.json','REPORT.md')]+['scratch/t59/out/'+f for f in ('REPORT.md','field_map.json')]+[MASTER,BIG,PROV,SCHEMA]
SIDES = ('client','server')
N = 84259
# Getter roots only. 11f0690 is the inherited getter (registration scan, not a subtable parse).
GETTERS = (0xe89a00,0x151d9b0,0x151e500,0x147a290,0xe96a10,0xe96f20,0x11f0690,0xfe3520)
FIN = {
    # wire lane, codec, tag-0 member, getter use, chronological/bit evidence
    'Cesd':(8,'date',0x2c,0x147a433,[0x147a439,0x147a442,0x147a446,0x147a449,0x147a450]),
    'Ceed':(12,'date',0x30,0x147a77a,[0x147a780,0x147a789,0x147a78d,0x147a790,0x147a797]),
    'Cead':(16,'date',0x34,0x147a6df,[0x147a6e5,0x147a6ee,0x147a6f2,0x147a6f5,0x147a6fc]),
    'Cadm':(7,'bit1',0x3b,0x147a52c,[0x147a539,0x147a53b,0x147a53e]),
    'Chaf':(5,'gated_bool',0x39,0x147a5fc,[0x147a5f2,0x147a5f6,0x147a609,0x147a8b7]),
    'Chsd':(4,'enum_i8',0x3c,0x147a65b,[0x147a668]),
    'Cpfa':(7,'enum_i8',0x3b,0x147a7f0,[0x147a7fd]),
    'CteA':(20,'i8',0x38,0x147a4cd,[0x147a4da]),
    'Cmtp':(25,'f32',0x18,0x147a388,[0x147a396]),
    'Casp':(29,'f32',0x1c,0x147a590,[0x147a59e]),
    'Ccba':(0,'i32',0x14,0x55fc0,[0x147a2ed,0x147a2f3,0x147a2f5,0x147a2fb,0x147a306,0x55fc3]),
}
# Ordinal must never be inferred merely from a matching domain; these first
# departures from the putative direct lane are proof failures, not data guesses.
BLOCKED = {
    'Clri':(0xe8bb8f,'CLUB+0xf8 selects City; City+0x38, not a Club local-region lane'),
    'Cldi':(0xe8d152,'forwards Tldi to first-Team getter, not a CLUB ordinal'),
    'Cndi':(0xe8ab1e,'forwards Tndi to first-Team getter, not a CLUB ordinal'),
    'Codi':(0xe8e3fa,'forwards Todo to first-Team getter, not a CLUB ordinal'),
    'Csmn':(0xe96aad,'runtime list filters first Team before loading stadium at +0x28'),
    'Csna':(0xe96aad,'runtime list filters first Team before loading stadium at +0x48'),
    'Csjd':(0xe96aad,'runtime list filters first Team before loading date'),
    'Csld':(0xe96aad,'runtime list filters first Team before loading date'),
    'Cebd':(0xe96f7c,'CLUB+0x100 -> extra+0x78 election object; no main-row cursor'),
    'Cmls':(0x3ebf736,'first Team and its competition context; not a CLUB packed flag'),
    'Chdb':(0xe8e12f,'helper assembles result; no proven scalar transfer for its return'),
    'CssS':(0x3ebcd5c,'helper scans indirect +0xb0 polymorphic list (0x23), not proven for a t57 slot'),
    'CssE':(0x3ebcd5c,'helper scans indirect +0xb0 polymorphic list (0x23), not proven for a t57 slot'),
    'CssP':(0x3ebcd5c,'helper scans indirect +0xb0 polymorphic list (0x23), not proven for a t57 slot'),
    'CssT':(0x3ebcd5c,'helper scans indirect +0xb0 polymorphic list (0x23), not proven for a t57 slot'),
}

class Failed(Exception): pass

def ck(ok, why):
    if not ok: raise Failed(why)

def H(data): return sha256(data).hexdigest()
def J(path): return json.loads(Path(path).read_bytes())
def U(b,a=0): return S.unpack_from('<I',b,a)[0]
def hist(vals): return {str(k):n for k,n in sorted(Counter(vals).items())}
def four(code): return int.from_bytes(code.encode('ascii'),'big')

def provenance():
    m = J(ROOT/'evidence/MANIFEST.json')
    manifest = {r['path']:r['sha256'] for r in m['files']}
    h = {p:H((ROOT/p).read_bytes()) for p in INPUTS}
    ck(all(h[p]==manifest[p] for p in (MASTER,BIG,PROV)), 'snapshot SHA')
    ck(EXEH in (ROOT/PROV).read_text(encoding='utf-8'), 'editor snapshot provenance')
    return h


class PE:
    def __init__(self):
        import pefile
        from capstone import Cs,CS_ARCH_X86,CS_MODE_64
        self.raw=EXE.read_bytes(); ck(H(self.raw)==EXEH,'editor.exe SHA')
        self.p=pefile.PE(data=self.raw,fast_load=True)
        self.p.parse_data_directories(directories=[3]); self.image=self.p.OPTIONAL_HEADER.ImageBase
        self.ext={self.off(self.image+x.struct.BeginAddress):self.off(self.image+x.struct.EndAddress) for x in self.p.DIRECTORY_ENTRY_EXCEPTION}
        self.md=Cs(CS_ARCH_X86,CS_MODE_64); self.md.detail=True
        self.i={}
    def va(self, a): return self.image+self.p.get_rva_from_offset(a)
    def off(self, v): return self.p.get_offset_from_rva(v-self.image)
    def get(self,a):
        if a not in self.i: self.i[a]=next(self.md.disasm(self.raw[a:a+15],self.va(a),1))
        return self.i[a]
    def dst(self,i):
        from capstone import CS_OP_IMM
        return self.off(i.operands[0].imm) if i.operands and i.operands[0].type==CS_OP_IMM else None
    def rip(self,i): return self.off(i.address+i.size+i.operands[1].mem.disp)
    def record(self,a):
        i=self.get(a)
        return {'offset':a,'va':i.address,'bytes':bytes(i.bytes).hex(),'insn':(i.mnemonic+' '+i.op_str).strip()}
    def data(self,a,w): return {'offset':a,'va':self.va(a),'bytes':self.raw[a:a+w].hex()}
    def cell(self,base,index):
        a=base+4*index; rel=S.unpack_from('<i',self.raw,a)[0]
        return dict(self.data(a,4),table=base,index=index,rel32=rel,target=self.off(self.va(base)+rel))
    def edge(self,a):
        i=self.get(a); t=self.dst(i); ck(i.mnemonic in ('jmp','call') and t is not None and i.size==5,('direct rel32',hex(a)))
        return dict(self.record(a),target=t,encoding='next-IP rel32',rel32=S.unpack_from('<i',i.bytes,1)[0])


def scan(p, root, switches=True):
    """Walk bounded direct CFG, optionally resolving proven indexed rel32 dispatches."""
    from capstone import CS_OP_IMM, CS_OP_REG, CS_OP_MEM
    end=p.ext[root]; tables={}; bitg={}
    if switches:
        last=[]
        for q in p.md.disasm(p.raw[root:end],p.va(root)):
            a=p.off(q.address); p.i[a]=q
            if len(last)>=6:
                seq=last[-6:]; pattern=[x.mnemonic for x in seq]
                if q.mnemonic=='jmp' and q.operands[0].type==CS_OP_REG and pattern[1:]==['cmp','ja','lea','movsxd','add']:
                    tables[a]=seq
                if q.mnemonic=='bt' and pattern[2:5]==['lea','cmp','ja'] and last[-1].mnemonic in ('mov','movabs'):
                    bitg[a]=last[-4:]
            last.append(q)
        for a,norm,load in {0xe89a00:[(0xe8c092,0xe8b04e,0xe8c084),(0xe8b1ae,0xe8a236,0xe8b1a0)],
                          0x11f0690:[(0x11f1018,0x11f0da0,0x11f100a),(0x11f1038,0x11f0b85,0x11f102a),(0x11f1058,0x11f0ca7,0x11f104a)]}.get(root,[]):
            def three(start):
                out=[]
                for _ in range(3):
                    q=p.get(start);out.append(q);start+=q.size
                return out
            tables[a]=three(norm)+three(load)
            ck(p.dst(tables[a][2])==load and tables[a][2].mnemonic=='jbe',('split range gate',a))
    todo=[root]; seen={}; gates=defaultdict(list); unresolved=[]; shapes={}
    def add(cc,kind,ix,sites,target,**other):
        gates[cc].append(dict(root=root,kind=kind,index=ix,sites=[p.off(x.address) for x in sites],arm=target,**other))
    while todo:
        a=todo.pop()
        if not root<=a<end or a in seen: continue
        q=p.get(a); seen[a]=q; m=q.mnemonic; nxt=a+q.size
        if q.mnemonic=='cmp' and len(q.operands)==2 and q.operands[0].type==CS_OP_REG and q.operands[1].type==CS_OP_IMM:
            h=p.get(nxt)
            if h.mnemonic in ('je','jne'):
                add(q.operands[1].imm,'compare',None,[q,h],p.dst(h) if h.mnemonic=='je' else nxt+h.size)
        if a in bitg:
            sub,bound,br,load=bitg[a]; low=-sub.operands[1].mem.disp; n=bound.operands[1].imm+1; mask=load.operands[1].imm
            h=p.get(nxt); ck(h.mnemonic in ('jb','jae') and 0<n<=64,('bit gate',a))
            target=p.dst(h) if h.mnemonic=='jb' else nxt+h.size
            for idx in range(n):
                if (mask>>idx)&1: add(low+idx,'bt',idx,[sub,bound,br,load,q,h],target,low=low,mask=mask)
        if m.startswith('j'):
            t=p.dst(q)
            if t is not None: todo.append(t)
            if m!='jmp': todo.append(nxt)
            elif t is None:
                if a not in tables: unresolved.append(a); continue
                sub,bound,br,lea,rd,summ=tables[a]; base=p.rip(lea); n=bound.operands[1].imm+1
                ck(0<n<=128 and sub.mnemonic in ('lea','add') and rd.operands[1].mem.scale==4 and rd.operands[1].type==CS_OP_MEM,('table shape',a))
                low=(-(sub.operands[1].mem.disp if sub.mnemonic=='lea' else sub.operands[1].imm))&0xffffffff
                # Skip the padding/default cells, which may enter a different subtree.
                default=p.dst(br) if br.mnemonic=='ja' else Counter(p.cell(base,k)['target'] for k in range(n)).most_common(1)[0][0]
                shapes[a]={'base':base,'count':n,'first_code':low,'default':default}
                for idx in range(n):
                    cell=p.cell(base,idx); t=cell['target']; todo.append(t)
                    if t!=default: add(low+idx,'rel32_table',idx,[sub,bound,br,lea,rd,summ,q],t,cell=cell)
        elif m not in ('ret','retf','int3','ud2'): todo.append(nxt)
    return seen,gates,{'root':root,'end':end,'reachable':len(seen),'conditionals':sum(q.mnemonic.startswith('j') and q.mnemonic!='jmp' for q in seen.values()),'register_jumps_not_followed':sorted(unresolved),'rel32_tables':[dict(v,jump=a) for a,v in sorted(shapes.items())]}


def prefix(p,seen,entry,limit=22):
    """No type assumptions for generic arms. Follow local unconditional jumps only."""
    path=[]; a=entry
    while a in seen and a not in path and len(path)<limit:
        q=seen[a]; path.append(a)
        if q.mnemonic in ('ret','int3','ud2'): break
        if q.mnemonic=='jmp':
            a=p.dst(q)
            if a is None: break
        else:
            a+=q.size
            if q.mnemonic.startswith('j'): break
    return path


def static(slots, fs):
    from capstone import CS_OP_MEM
    p=PE(); vt=p.off(slots['source']['CLUB']['vtable'])
    ck([p.off(S.unpack_from('<Q',p.raw,vt+n*8)[0]) for n in (2,19,56)]==[0xe89a00,0xe5a7a0,0x11f4550],'CLUB getter/reader/base virtual roots')
    finvt=p.rip(p.get(0xe5ae12)); ck([p.off(S.unpack_from('<Q',p.raw,finvt+n*8)[0]) for n in (2,4)]==[0x147a290,0x1476470],'tag 0 same vptr selects getter + reader')
    readers={}; ins=set(); branch_book=[]
    for name,old in slots['source']['runtime_function_extents'].items():
        root=int(name); here,_,s=scan(p,root,False)
        ck((s['end'],s['reachable'],s['conditionals'])==(old['end_exclusive'],old['reachable'],old['conditional']),(hex(root),'t57 bounded CFG'))
        direct=[a for a,i in sorted(here.items()) if i.mnemonic=='call' and i.operands[0].type==CS_OP_MEM and i.operands[0].mem.disp==0x28]
        ck(direct==sorted(old['direct_stream_reads']),(hex(root),'t57 reader sites'))
        readers[root]=dict(s,transfers=direct)
    for part in sorted(R1.glob('branches.part*.json')):
        for b in J(part):
            root=b['function']; a=b['site']; q=p.get(a); pred=b['predicate']
            ck(readers[root]['root']<=a<readers[root]['end'] and p.dst(q)==b['taken'] and a+q.size==b['fallthrough'],('reader branch',a))
            ins.add(a)
            if pred is not None: ins.add(pred)
            branch_book.append({'root':root,'branch':a,'gate':pred,'taken':b['taken'],'fallthrough':b['fallthrough'],'classification':b['classification']})
    ck(len(branch_book)==sum(s['conditionals'] for s in readers.values()),'reader conditional census')
    roots={}
    by=defaultdict(list)
    codes={four(x['code']) for x in fs if len(x['code'])==4 and x['code'].isascii()}
    for root in GETTERS:
        seen,gs,s=scan(p,root); roots[root]=s
        for cc in codes & gs.keys():
            for t in gs[cc]:
                path=prefix(p,seen,t['arm']); t['local_path']=path
                t['direct_rel32']=[p.edge(a) for a in path if p.get(a).mnemonic in ('call','jmp') and p.dst(p.get(a)) is not None and p.get(a).size==5]
                ins.update(t['sites']+path); by[cc].append(t)
    balance_cell=finvt+0x190; ck(p.off(S.unpack_from('<Q',p.raw,balance_cell)[0])==0x55fc0,'tag0 balance getter slot +0x190')
    cap_at=p.rip(p.get(0x423ffa0)); ck(S.unpack_from('<f',p.raw,cap_at)[0]==150,'raw ticket clamp')
    ins.update([0x423ff9b,0x423ffa0,0x423ffa7,0x423ffa9])
    transfer=[]; cur=0
    for load,site,member,w in [(0x423ff0d,0x423ff1d,0x14,4),(0x423ff30,0x423ff44,0x3c,1),(0x423ff34,0x423ff5a,0x39,3),(0x423ff47,0x423ff70,0x2c,13),(0x423ff5d,0x423ff86,0x10,4),(0x423ff73,0x423ff98,0x18,20)]:
        ck(p.get(load).operands[1].mem.disp==member,'tag-0 member'); ins.update([load,site]); transfer.append(dict(site=site,destination=load,relative_to_tag0_object=member,width=w,wire_interval=[cur,cur+w])); cur+=w
    finance_path=[0xe5a9ba,0xe5ada9,0xe5adc4,0xe5adc8,0xe5adcb,0xe5add1,0xe5add3,0xe5ae12,0xe5ae19,0xe5aea6,0xe5aee1,0xe5aee8,0xe5aef1,0x1476470,0x423fefe,0xe8c605,0xe8c60d,0xe8c610,0xe8c612,0xe8c615,0xe8c619,0xe8c61b,0xe8eb85,0xe8eb9f,0x147a2ac]
    ins.update(finance_path)
    props=[]
    for f in fs:
        k=f['code']; er=f['schema'].get('enum_ref'); gs=sorted(by[four(k)],key=lambda x:(x['root'],x['sites'][0])) if k.isascii() and len(k)==4 else []
        top=[t for t in gs if t['root']==0xe89a00]; x=dict(id=f'E97/club.xml#club/{f["xml_index"]:03d}',code=k,dispatch=gs,projection=None)
        if er=='cnst':
            # A dispatch overlap can reach the B arm (Ccss), never use a same-code cell in the *other* helper.
            hits=[(t,h) for t in top for h in gs if h['root'] in (0x151d9b0,0x151e500) and any(r['target']==h['root'] for r in t['direct_rel32']) and h['local_path'] and p.get(h['arm']).mnemonic=='movsx']
            ck(len(hits)==1,(k,'one exact cnst byte arm',hits))
            t,h=hits[0]; site=h['arm']; member=p.get(site).operands[1].mem.disp; origin=0xe0 if h['root']==0x151d9b0 else 0xe7
            lift=0xe89bef if origin==0xe0 else 0xe89fe1; ck(lift in t['local_path'],'cnst indirection in equal arm')
            x['projection']=dict(family='cnst_extra',gate=t,helper=h,object_path=[0x100,origin+member],member_use=site,
                cursor=None,first_counterexample={'site':lift,'reason':'qword load of CLUB+0x100; byte is in a separate object not reached by t57 main cursor'})
        elif k in FIN:
            lane,codec,member,use,proof=FIN[k]; helper=[h for h in gs if h['root']==0x147a290]
            if k=='Cpfa': top_use=0xe8e787
            else: top_use=0xe8c605
            ck(len(helper)==1 and len(top)==1 and top[0]['arm']==top_use,(k,'financial gate chain'))
            ins.update([use]+proof)
            a=next(r for r in transfer if r['wire_interval'][0]<=lane<r['wire_interval'][1]); ck(a['relative_to_tag0_object']+lane-a['wire_interval'][0]==member,'wire lane arithmetic')
            ck(p.get(use).operands[1].mem.disp==member,('getter member',k))
            x['projection']=dict(family='tag0_finance',gate=top[0],helper=helper[0],object_path=[0x150,member],member_use=use,
                proof=proof,cursor=dict(r1_slot='obj150',tag=0,member_transfer=a['site'],lane=lane,codec=codec))
        elif k=='rdui':
            r=[t for t in gs if t['root']==0xfe3520 and t['sites'][0]==0xfe3862];ck(len(r)==1,'inherited rdui compare')
            route=[0xe8f4fe,0xe8f51d,0x11f2a95,0x11f2a98,0x11f2aba,0x11f4550,0xfe389d,0xfe38a2,0xfe38a7,0xe5bca7,0x43bec5b,0x11d21cc,0x11d21d3,0x11d21df]
            ins.update(route);x['projection']=dict(family='saved_rdui',gate=r[0],object_path=[0x10],cursor={'r1_slot':'identity','lane':8,'codec':'suppressed_uid'},proof=route)
        elif k in BLOCKED:
            a,reason=BLOCKED[k]; ins.add(a);x['projection']=dict(family='static_stop',gate=top[0] if len(top)==1 else None,cursor=None,first_counterexample={'site':a,'reason':reason})
        props.append(x)
    return dict(static_source={'source':EXE.as_posix(),'sha256':EXEH,'unit':'PE file offset; records include VA','club_vtable_slots':{str(n):p.data(vt+n*8,8) for n in (2,19,56)},'tag0_vtable_slots':{str(n):p.data(finvt+n*8,8) for n in (2,4)}},
        reader_extents=list(readers.values()),reader_branches=sorted(branch_book,key=lambda b:b['branch']),getter_extents=list(roots.values()),
        finance={'route':finance_path,'reader_rel32':p.edge(0x1476470),'balance_vtable_cell':p.data(balance_cell,8),'ticket_clamp_f32':p.data(cap_at,4),'transfer_spans':transfer},instructions=[p.record(a) for a in sorted(ins)],occurrences=props)


def load(slots, members):
    depot=Path(os.environ.get('FM24_DB_DIR',ROOT/'scratch/data'))
    if depot.drive.upper()=='Z:' or depot.resolve().drive.upper()=='Z:': raise ValueError('Z: forbidden')
    old=ROOT.parent/'fm24'; sys.path.append(str(old/'tools/python'))
    import zstandard as z
    entries=runpy.run_path(str(old/'scripts/modding_read_dbdat.py'))['_entries']; raw={}
    for side in SIDES:
        _,b,d=entries(depot/f'{side}_db.dat'); base=d['data_base']; frozen=slots['archives'][side]
        ck(H(b)==frozen['archive_sha256'] and base==frozen['data_base'],(side,'archive SHA / base'))
        for e in d['entries']:
            for s,t in members:
                if s!=side or e['path']!=f'{side}_db/table_{t}.dat':continue
                a=base+e['offset'];end=a+e['packed_size'];k=frozen['members'][str(t)]
                ck([a,end]==k['range'] and end<=k['bound'] and H(b[a:end])==k['compressed_sha256'],'member bounds')
                found=[]; frames=[]
                while a<end:
                    dec=z.ZstdDecompressor().decompressobj(); v=dec.decompress(b[a:end]); q=end-len(dec.unused_data)
                    ck(dec.eof and q>a,'frame closure');frames.append([a,q,len(v)]);a=q
                    if len(v)==e['size']:found.append(v)
                ck(len(found)==1 and frames==k['frames'] and H(found[0])==k['payload_sha256'],('payload',side,t))
                raw[side,t]=found[0]
    ck(set(raw)==members,'member selection');return raw


def point(b,i,a,w,v): return dict(row=i,absolute=a,raw=b[a:a+w].hex(),value=v)

def domain(b,cells,x,sch,allowed):
    codec=x['codec']; lane=x['lane']; live=Counter(); raw_h=Counter(); bad=0; first_bad=None; first=None; first_live=None; masked=0
    lo=Decimal(sch['min_value']) if 'min_value' in sch else None
    hi=Decimal(sch['max_value']) if 'max_value' in sch else None
    w=4 if codec in ('date','f32','i32','suppressed_uid') else 1
    for i,a,span in cells:
        ck(lane+w<=span,'projection crosses outer slot'); off=a+lane; v=None; reason=None
        if codec=='bit1': v=(b[off]>>1)&1; raw_h[b[off]]+=1
        elif codec=='gated_bool':
            r=b[off]; raw_h[r]+=1
            if b[a+4]==0:masked+=1
            else:v=r
            if r not in (0,1): reason='raw byte not boolean'
        elif codec in ('i8','enum_i8'):
            v=S.unpack_from('<b',b,off)[0]
            if codec=='enum_i8' and (not allowed or v not in allowed):reason='no scoped enum_ref' if not allowed else 'outside scoped enum'
        elif codec=='i32': v=S.unpack_from('<i',b,off)[0]
        elif codec=='f32':
            v=S.unpack_from('<f',b,off)[0]
            if not math.isfinite(v): reason='nonfinite'; v=str(v)
        elif codec=='date':
            low,y=S.unpack_from('<HH',b,off);day=low&511; flags=low>>9;v=(y,day,flags)
            leap=y%4==0 and (y%100!=0 or y%400==0)
            if flags or not (1<=y<=9999 and 1<=day<=365+leap): reason='not an unflagged Gregorian ordinal date'
        elif codec=='suppressed_uid':
            v=U(b,off)
            if v==U(b,off-4):masked+=1;reason='equal UID: getter suppresses saved rdui'
        else:raise Failed(('codec',codec))
        if isinstance(v,(float,int)) and ((lo is not None and v<lo) or (hi is not None and v>hi)):
            reason='outside frozen XML min/max in local getter units'
        if first is None: first=point(b,i,off,w,v)
        if v is not None:
            live[v]+=1
            if first_live is None:first_live=point(b,i,off,w,v)
        if reason:
            bad+=1
            if first_bad is None:first_bad=dict(point(b,i,off,w,v),reason=reason)
    keys=sorted(live) if all(isinstance(a,(tuple,float,int)) for a in live) else sorted(live,key=str)
    return dict(events=len(cells),bypassed=N-len(cells),suppressed=masked,values=sum(live.values()),minimum=keys[0] if keys else None,maximum=keys[-1] if keys else None,
        distinct=len(live),histogram={str(k):live[k] for k in keys} if len(live)<=128 else None,raw_byte_histogram=hist(raw_h) if raw_h else None,
        first=first,first_value=first_live,violations=bad,first_counterexample=first_bad)


def target10(b, meta, side):
    # Only raw keys at the accepted t47 coordinates; no Nation field reopening.
    doc=J(ROOT/'scratch/t47/out/cursor_nation_tax.json')[side]
    ck(H(b)==doc['payload_sha256'],'t47 key source')
    uids=[]; h=sha256()
    for i,r in enumerate(doc['rows']):
        a=r['identity_at']; j,u,v=S.unpack_from('<III',b,a);ck(j==i and u==v!=0,('nation raw triple',side,i));uids.append(u);h.update(b[a:a+12])
    ck(len(set(uids))==U(b,8)==meta['count']==251 and h.hexdigest()==meta['identity_sha256'],'nation ordinal set')
    return dict(enumerate(uids))


def ref_control(b, cells, target):
    ids=set(target.values()); live=miss=wrong=0; first_wrong=None; first_miss=None; first_live=None
    for i,a,w in cells:
        v=U(b,a)
        if v==0xffffffff:continue
        live+=1
        if v not in target:
            miss+=1
            if first_miss is None:first_miss=point(b,i,a,w,v)
        elif first_live is None:first_live=dict(point(b,i,a,w,v),target_uid=target[v])
        if v in ids:wrong+=1
        elif first_wrong is None:first_wrong=point(b,i,a,w,v)
    return dict(events=len(cells),considered_live=live,null=len(cells)-live,ordinal_hits=live-miss,ordinal_misses=miss,first_ordinal_miss=first_miss,
        wrong_uid_hits=wrong,first_wrong_uid_miss=first_wrong,first_live=first_live)


def chronology(b,cells):
    # The title of Cead suggests an editing constraint, not a wire representation.
    seen={'start_end_nondefault':0,'end_before_start':0,'appeal_and_start_nondefault':0,'appeal_not_before_start':0}; first=None
    for i,a,_ in cells:
        dates=[]
        for k in (8,12,16):
            lo,hi=S.unpack_from('<HH',b,a+k);dates.append((hi,lo&511))
        start,end,appeal=dates
        if start!=(1900,1) and end!=(1900,1):
            seen['start_end_nondefault']+=1;seen['end_before_start']+=end<start
        if start!=(1900,1) and appeal!=(1900,1):
            seen['appeal_and_start_nondefault']+=1
            if appeal>=start:
                seen['appeal_not_before_start']+=1
                if first is None:first=dict(point(b,i,a+8,12,dates),reason='XML title says before start; not a wire-validity constraint')
    return dict(events=len(cells),**seen,first_appeal_order_counterexample=first)


def fixtures(raw, books, old):
    c=raw['client',2]; s=raw['server',21]; x=raw['client','extra_3']; d=J(ROOT/BIG)['tables']; reg=old['regression']
    city={}; stad={}; years=[]; joins={}
    for f in d['2']['named_anchor_checks']:
        i=f['row_index']; a=14+43*i; j,uid,v=S.unpack_from('<III',c,a+30)
        row=[j,uid,list(S.unpack_from('<ff',c,a+1)),c[a+10]]
        ck(j==i and v==uid and row==reg['city'][f['city']],('city',f['city'])); city[f['city']]=row
    for f in d['21']['landmark_cross_checks']:
        i=f['row_index']; a=14+181*i; j,uid,v=S.unpack_from('<III',s,a+168); r=reg['stadium'][str(i)]
        ck(j==i and v==uid==r['uid'] and tuple(r['capacity_and_seats'])==S.unpack_from('<II',s,a) and r['city_ordinal']==U(s,a+146) and tuple(r['coordinates'])==S.unpack_from('<ff',s,a+160),('stadium',i)); stad[str(i)]=r
    for side in SIDES:
        b=raw[side,3]; book=books[side]; name=book['short_len'][460][1]; j,u,v=S.unpack_from('<III',b,book['identity'][460][1]); city_o=U(b,book['ref_f8'][460][1]); nation=U(b,book['ref_d8'][460][1]); short=b[name+4:name+4+U(b,name)].decode()
        ck((j,u,v,city_o,nation,short)==(460,676,676,1061,139,'Liverpool'),('Liverpool',side)); joins[side]=[j,u,city_o,nation,short]
    exp={e['candidate_order_index']:e for e in d['3']['field_validation']['Cyfn_named_year_checks']}
    for r in reg['founded_year_fixture_only']:
        a=r['absolute']; i=r['row']; j,y=S.unpack_from('<IH',x,a-4)
        ck(i==j and y==r['year']==exp[i]['client_extra_3_u16_at_row_plus_4'] and r['note']==exp[i]['note'],('year fixture',i));years.append(r)
    ck(len(years)==14 and any(r['row']==460 and r['year']==1892 for r in years) and stad['430']['capacity_and_seats']==[81044,81044],'anchors')
    return dict(liverpool=joins,city=city,stadium=stad,founded_year_fixture_only=years)


def build():
    # Reuse the only accepted Club outer cursor, not its field grades.
    sys.path.insert(0,str(ROOT/'scripts'))
    from t57_clubmain_fields import replay,Check as R1Failed
    prov=provenance(); frozen=J(ROOT/MASTER); orig=J(R1/'field_map.json'); slots=J(R1/'field_slots.json'); sc=J(ROOT/SCHEMA)
    xml=frozen['entities']['club.xml'][0]['fields']; all_f=orig['fields']; ck(len(xml)==len(all_f)==433 and all(f['schema']==xml[i] and f['xml_index']==i for i,f in enumerate(all_f)),'frozen XML occurrence identity')
    unm=[f for f in all_f if f['grade']=='unmapped']; ck(len(unm)==399 and orig['grade_counts']=={'L3':13,'held':11,'skipped_separate_member':10,'unmapped':399},'r1 disposition')
    ck(sc['club_main_row_fields']['acceptance_ledger_entry']=='E97' and len(slots['slots'])==34,'schema/r1 source')
    p=static(slots,unm); p['input_sha256']=prov
    members={(s,t) for s in SIDES for t in (3,10)}|{('client',2),('server',21),('client','extra_3')}
    raw=load(slots,members); rows={}; books={}; ctl={}; run={}
    for s in SIDES:
        b=raw[s,3]
        try: rr,book,_=replay(b,int(s=='server'))
        except R1Failed as e: raise Failed(str(e)) from e
        frozen_env=slots['envelopes'][s]
        ck(len(rr)==N and len(b)==frozen_env['payload'] and H(b''.join(S.pack('<IIIB',*r) for r in rr))==frozen_env['row_trace_sha256'],'R1 row trace')
        for slot in slots['slots']:
            key=slot['key']; cells=book[key]; pr=slot['profiles'][s]
            ck(len(cells)==pr['rows'] and (not cells or H(b''.join(S.pack('<III',*c) for c in cells))==pr['coordinate_sha256']),('R1 coordinate trace',s,key))
        rows[s]=rr;books[s]=book
        ids=target10(raw[s,10],slots['target_identity_domains'][s]['10'],s)
        ctl[s]=ref_control(b,book['ref_e0'],ids);ck(not ctl[s]['ordinal_misses'] and ctl[s]['wrong_uid_hits']<ctl[s]['considered_live'],('reference control',s))
        run[s]={'rows':N,'payload_bytes':len(b),'tag150':hist(b[a] for _,a,_ in book['obj150_tag']),'payload_sha256':H(b),'coordinates_revalidated':34}
    ck([r[2:] for r in rows['client']]==[r[2:] for r in rows['server']],'cross-archive triples')
    p['date_relationship_control']={s:chronology(raw[s,3],books[s]['obj150']) for s in SIDES}
    fmap=[]
    for base,pj in zip(unm,p['occurrences'],strict=True):
        x=pj['projection']; k=base['code']; sch=base['schema']; er=sch.get('enum_ref'); allowed=sorted(int(v['enum']) for v in frozen['enums'][er]['values']) if er else None
        grade='unmapped'; first=None; result=None; proof=None; reason='no bounded same-object byte cursor join'
        if sch['type']=='string':reason='string slots not inferred from proximity or type'
        if x:
            grade='held'; first=x.get('first_counterexample'); proof=x.get('cursor')
            if first: reason=first['reason']
            else:
                result={s:domain(raw[s,3],books[s][proof['r1_slot']],proof,sch,allowed) for s in SIDES}
                first=next((r['first_counterexample'] for r in result.values() if r['first_counterexample']),None)
                grade='held' if first else 'L3';reason=first['reason'] if first else 'exact getter member plus scoped full-archive projection domain'
                ck(all(r['events']+r['bypassed']==N for r in result.values()),'projection incidence')
                if k=='Cmtp': ck(result['server']['maximum']<=150,'unobserved ticket reader clamp')
        fmap.append(dict(id=pj['id'],r1_id={'ledger':'E97','path':'scratch/t57/out/field_map.json','xml_index':base['xml_index'],'grade':'unmapped'},code=k,xml_type=sch['type'],
            xml_domain={**{a:sch[a] for a in ('min_value','max_value','enum_ref','store_pence','dependencies') if a in sch},'allowed_enum':allowed},grade=grade,reason=reason,
            projection_family=x['family'] if x else None,wire=proof if grade=='L3' else None,domain_profiles=result,first_counterexample=first))
    count=hist(r['grade'] for r in fmap); p['r1_envelopes']=run
    p['reference_controls']={'ref_e0':{'target':'t10', 'getter_binding':None,'reader':0xe5a843,'fixup':0xe5c5b9,'sides':ctl,'note':'unnamed control, typed fixup shares Nation resolver; no XML assignment'}}
    pp=PE(); add=set([0xe5a807,0xe5a837,0xe5a840,0xe5a843,0xe5c59e,0xe5c5a5,0xe5c5b9,0xe5c5be,0xe5c5c5,0xe5c5d9]); current={i['offset']:i for i in p['instructions']}; current.update({a:pp.record(a) for a in add});p['instructions']=[current[i] for i in sorted(current)]
    m=dict(scope='club.xml#club r1 unmapped only',input_sha256=prov,schema_version=sc['schema_version'],r1_reference='E97',preserved_grades={'L3':13,'held':11,'skipped_separate_member':10},
        r1_held_indices=[f['xml_index'] for f in all_f if f['grade']=='held'],superseded_r1_negatives=[],L4=0,reviewed=len(fmap),grade_counts=count,new_L3=[x['code'] for x in fmap if x['grade']=='L3'],
        fixture_regression=fixtures(raw,books,orig),fields=fmap)
    OUT.mkdir(parents=True,exist_ok=True)
    for name,obj in [('projections.json',p),('field_map_r2.json',m)]:
        (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print('t63 build PASS:',count,'new L3:',', '.join(m['new_L3']))


def selftest():
    ck(four('Cadm')==0x4361646d!=four('cadm'),'case-sensitive')
    b=bytes([0,2,16]); z=domain(b,[(i,i,1) for i in range(3)],{'codec':'bit1','lane':0},{},None)
    ck(z['histogram']=={'0':2,'1':1} and z['violations']==0,'packed bit')
    b=S.pack('<4H',366,2024,366,2023); z=domain(b,[(0,0,4),(1,4,4)],{'codec':'date','lane':0},{},None)
    ck(z['violations']==1 and z['first_counterexample']['row']==1,'leap day counterexample')
    z=ref_control(S.pack('<3I',0,1,0xffffffff),[(i,4*i,4) for i in range(3)],{0:1,1:100})
    ck(z['ordinal_hits']==2 and z['wrong_uid_hits']==1 and z['null']==1,'ordinal vs UID')
    print('t63 builder selftest PASS')


def main():
    p=argparse.ArgumentParser(description=__doc__); g=p.add_mutually_exclusive_group();g.add_argument('--build',action='store_true');g.add_argument('--selftest',action='store_true');a=p.parse_args()
    try:
        if a.selftest:selftest()
        else:build()
    except Failed as e: print('check failed:',e,file=sys.stderr);return 1
    except Exception as e: print(f'fatal: {type(e).__name__}: {e}',file=sys.stderr);return 2
    return 0

if __name__=='__main__':raise SystemExit(main())
