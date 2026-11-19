#!/usr/bin/env python3
"""Offline t53: separate the t9 main and named auxiliary responsibility vectors."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import runpy
import struct as S
import sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'scratch/t53/out'
EXE=ROOT.parent/'fm24/input/editor.exe'
EXEH='b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTER='evidence/fm24/reports/editor_schema/master.json'
MH='7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda'
MEMBERS=('table_9.dat','table_extra_9.dat')
SIDES=('client','server')
HEAD=bytes.fromhex('03017461642ef10d')

def h(b): return sha256(b).hexdigest()
def j(p): return json.loads((ROOT/p).read_bytes())
def write(name,d): (OUT/name).write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8')
def hist(a): return {str(k):v for k,v in sorted(Counter(a).items())}
class Check(Exception): pass
def ck(x,msg):
    if not x: raise Check(msg)

class Span:
    def __init__(self,b,p,end,row): self.b=b; self.p=p; self.end=end; self.row=row
    def fail(self,at,site,kind,**kw):
        raise Check(dict(row=self.row,absolute=at,site=site,kind=kind,raw=self.b[at:at+8].hex(),**kw))
    def take(self,w,s):
        a=self.p
        if not 0<=w<=self.end-a: self.fail(a,s,'short transfer',width=w,limit=self.end)
        self.p+=w
        return self.b[a:self.p]
    def num(self,w,s,signed=False): return int.from_bytes(self.take(w,s),'little',signed=signed)
    def count(self,w,s,m,signed=False):
        a=self.p; v=self.num(w,s,signed)
        if not 0<=v<=(self.end-self.p)//m: self.fail(a,s,'invalid count',value=v,width=w,item_min=m)
        return v
    def string(self,s): return self.take(self.count(4,s,1),s)

def observed(c):
    ver_at=c.p; ver=c.num(4,0x4387ae0); count_at=c.p
    count=c.count(4,0x155c152,10)
    start=c.p; items=[]
    for i in range(count):
        a=c.p; tag=c.num(2,0x155c2f9,True)
        for w,s in ((4,0x155c31a),(1,0x155c33d),(1,0x155c360),(2 if tag>=2 else 1,0x155c38d if tag>=2 else 0x155c3b5),(1,0x155c3e0)):
            c.take(w,s)
        if tag>=3: c.take(1,0x155c40c)
        items.append(dict(item=i,absolute=a,end=c.p,tag=tag,raw=c.b[a:c.p].hex()))
    return dict(version_at=ver_at,version=ver,count_at=count_at,count=count,start=start,end=c.p,items=items)

def census(rows):
    blocks=[r['vector'] for r in rows if r['vector'] is not None]; scores=[r['presence'] for r in rows if r['presence'] is not None]
    return dict(presence=hist(scores),skipped=len(rows)-len(scores),counts=hist(b['count'] for b in blocks),
                version=hist(b['version'] for b in blocks),tags=hist(i['tag'] for b in blocks for i in b['items']),
                item_width=hist(i['end']-i['absolute'] for b in blocks for i in b['items']),items=sum(b['count'] for b in blocks))

def main_walk(b,side):
    t=j(f'scratch/t49/out/cursor_t9_{side}.json'); ck(h(b)==t['payload_sha256'],'accepted payload'); rr=[]; end=13
    for r in t['rows']:
        a=r['wire13']; z=r['end']; ordinal=r['row']; ck(a==end and h(b[a:z])==r['wire_sha256'],'accepted row')
        ck(r['identity_at']==z-12 and list(S.unpack_from('<III',b,z-12))==r['identity'] and r['identity'][0]==ordinal,'identity')
        event=r['trace']; gates=[(k,p) for k,(s,p,w,n) in enumerate(event) if s==0x105dd07]
        next_at=next(p for s,p,w,n in event if s==0x105dd87)
        ck(len(gates)==t['mode'],'mode/presence trace'); p=presence=vec=None
        if gates:
            k,p=gates[0]; c=Span(b,p,next_at,ordinal); presence=c.num(1,0x105dd07)
            ck(presence in (0,1),'presence domain')
            if presence: vec=observed(c)
            ck(c.p==next_at and a<=p<next_at<z,'next transfer boundary')
            # Comparing extent, not using t49's inner item spans as parse inputs.
            ck(event[k+1][1]==p+1,'trace adjacency')
        rr.append(dict(row=ordinal,start=a,end=z,identity_at=z-12,uid=r['identity'][1],row_sha256=r['wire_sha256'],
                       presence_at=p,presence=presence,next_site_at=next_at,vector=vec))
        end=z
    ck(b[end:].hex()==t['footer']['raw'] and len(b)==end+9 and len(rr)==251,'main EOF')
    return dict(member=MEMBERS[0],side=side,mode=t['mode'],rows=rr,header=13,end=end,footer=b[end:].hex(),payload_sha256=h(b),summary=census(rr))

def aux_walk(b,side,mode,name_path=True):
    ck(b[:8]==HEAD and S.unpack_from('<I',b,8)[0]==251,'extra header')
    c=Span(b,12,len(b),0); rr=[]
    for row in range(251):
        c.row=row; a=c.p; ordinal=c.num(4,0x3bb9748,True)
        if ordinal!=row: c.fail(a,0x3bb9748,'ordinal mismatch',value=ordinal,expected=row)
        name=c.string(0x11d34ab) if name_path else b''
        name_end=c.p
        c.take(2,0x11d358e); c.string(0x11d35c7)
        n=c.count(1,0x11d365d,27); c.take(27*n,0x11d38b3); c.take(8,0x11d3f72)
        base_end=c.p; p=presence=vec=None; selectors=[]
        if mode:
            c.take(20*c.count(2,0x11d41ca,20,True),0x11d4328)
            c.take(6*c.count(1,0x11d44a5,6,True),0x11d45ff)
            c.take(16,0x11d47de)
            for _ in range(c.count(2,0x11d4866,37)):
                at=c.p; tag=c.num(1,0x11d494d)
                if tag!=9: c.fail(at,0x11d4959,'unreduced typed selector',value=tag)
                c.take(20,0x42dba7a)
                for s in (0x42dbb34,0x42dbb4c,0x42dbb64,0x42dbb8a): c.string(s)
                selectors.append([at,tag,c.p])
            p=c.p; presence=c.num(1,0x11d4b5a)
            if presence not in (0,1): c.fail(p,0x11d4b5f,'presence outside observed domain',value=presence)
            if presence: vec=observed(c)
        rr.append(dict(row=row,start=a,end=c.p,name_hex=name.hex(),name_end=name_end,base_end=base_end,row_sha256=h(b[a:c.p]),
                       typed_records=selectors,presence_at=p,presence=presence,vector=vec))
    if c.p!=len(b): c.fail(c.p,0x3bb9803,'aux EOF',remaining=len(b)-c.p)
    return dict(member=MEMBERS[1],side=side,mode=mode,rows=rr,header=12,end=c.p,footer='',payload_sha256=h(b),summary=census(rr))

def trial(fn,*args):
    try: out=fn(*args)
    except Check as e: return dict(closed=False,first_failure=e.args[0])
    return dict(closed=True,first_failure=None,rows=len(out['rows']))

def people(root):
    import zstandard as z
    blob=(root/'basic_people_db.dat').read_bytes(); d=z.ZstdDecompressor().decompressobj(); b=d.decompress(blob[8:])
    ck(d.eof and not d.unused_data and b[:5]==bytes.fromhex('5b0a0a0000'),'person shell')
    x={}; u={}; p=5
    for index in range(658011):
        sel,k=b[p:p+2]; ck(sel==17 and 1<=k<=5,'person kind')
        p+=(83,83,83,34,22)[k-1]; a,v,w=S.unpack_from('<III',b,p-12)
        ck(a==index and v==w and v and v not in u,'person identity')
        x[a]=(v,k); u[v]=a
    ck(b[p:]==bytes.fromhex('00000000014cbd5477'),'person EOF')
    return x,u,dict(member='basic_people_db.dat',rows=len(x),end=p,footer=b[p:].hex(),payload_sha256=h(b),source_sha256=h(blob))

# code: (jumptable arm, object displacement, wire delta at tag 3, transfer site)
FIELD={'PUnI':(0x155a35c,4,6,0x155c33d),'PUnT':(0x155a4c1,5,7,0x155c360),
       'PUnP':(0x155a42a,0,2,0x155c31a),'PUnJ':(0x155a3c3,6,8,0x155c38d)}
def fields(cursors,master,ordinals,uids):
    parent=master['entities']['nation.xml'][0]['fields'][64]; ck(parent['field']=='TCrs','parent idx'); out={}
    dom={int(v['enum']) for v in master['enums']['ftjn']['values']}
    for k,(arm,disp,delta,sink) in FIELD.items():
        sf=[x for x in parent['list_item_fields'] if x['field']==k]; ck(len(sf)==1,k)
        groups={}
        for key,cur in cursors.items():
            evidence=[]; by=Counter(); misses={}; first={}
            for row in cur['rows']:
                if row['vector'] is None: continue
                for it in row['vector']['items']:
                    b=bytes.fromhex(it['raw']); ck(len(b)==12 and it['tag']==3,'observed tag/width')
                    width=4 if k=='PUnP' else 2 if k=='PUnJ' else 1
                    value=int.from_bytes(b[delta:delta+width],'little',signed=k in ('PUnP','PUnT'))
                    rec=dict(row=row['row'],item=it['item'],absolute=it['absolute']+delta,raw=b[delta:delta+width].hex(),value=value)
                    by[value]+=1
                    if k=='PUnP':
                        rec.update(state_byte=b[11],sentinel=value==-1,ordinal_target=ordinals.get(value),uid_target_ordinal=uids.get(value))
                        if value!=-1:
                            for x,hit in [('ordinal',value in ordinals),('UID_probe',value in uids)]:
                                label=x+('_hit' if hit else '_miss'); misses[label]=misses.get(label,0)+1; first.setdefault(label,rec)
                        else: first.setdefault('sentinel',rec)
                    elif k=='PUnJ':
                        rec['in_ftjn']=value in dom
                        label='ftjn_hit' if rec['in_ftjn'] else 'ftjn_miss'; misses[label]=misses.get(label,0)+1; first.setdefault(label,rec)
                    evidence.append(rec)
            groups[key]=dict(rows=evidence,histogram=hist(y['value'] for y in evidence),checks=misses,first_by_check=first,first_wire_example=next(iter(evidence),None),
                             no_live_person=k=='PUnP' and not any(not x['sentinel'] for x in evidence))
        reason={'PUnI':'no scoped enum_ref','PUnT':'no scoped enum_ref; 0xff is signed -1 and getter missing',
                'PUnP':'main all -1; auxiliary raw UID/id branch (state +9=0), ordinal test rejected; UID probe is contrast, not promotion',
                'PUnJ':'scoped ftjn exists but live raw values outside domain; zero is getter-missing, separately recorded'}[k]
        out[k]=dict(code=k,grade='held',slot_evidence='L3 static plus L1 span; field-level promotion held',
                    scope='nation.xml#nation[64].TCrs',schema=sf[0],gates=dict(scoped_schema_occurrences=1,dispatch_arm=arm,object_offset=disp,
                    reader_transfer=sink,item_offset_at_tag3=delta,tag_below_2_job_width=1 if k=='PUnJ' else None,domain_result=reason),archives=groups)
    return out

CFG=(0x105cb10,0x105fef0,0x1059a30,0x3ea1420,0x3bb9650,0x3b94b50,0x11d3200,0x4330ce0,0x3ea5150,0x14cf6d0,0x42dba50,
     0x4387ab0,0x155c120,0x11f3dc0,0x3ebb830,0x4387250,0x155a320,0x28150,0x907f0,0xb02980,0x83d5a0,0x83d080)
BR={0x105cbb1:(0x105cbae,'runtime-external','mode 0 bypasses the entire main presence site'),
    0x105dbc5:(0x105dbc0,'runtime-external','modern arm bypasses legacy linked-Nation transfer before the presence'),
    0x105dd19:(0x105dd14,'wire_data','main presence'),0x105dd6a:(0x105dd68,'IO-result','shared vector reader rejects'),
    0x11d3472:(0x11d346b,'context-lifecycle','t9 base ctor sets +0xba=1; without it the initial string is skipped'),
    0x11d4143:(0x11d413c,'runtime-external','aux mode 0 skips extension tail, not just TCrs presence'),
    0x11d4b66:(0x11d4b5f,'wire_data','aux presence'),0x155c378:(0x155c372,'wire_data','signed tag below 2 takes short +6 lane'),
    0x155c3f3:(0x155c3ed,'wire_data','signed tag below 3 omits +9 byte'),0x4387b6f:(0x4387b6a,'wire_data','version <=2 enables object +4 == 0xad cleanup'),
    0x155c300:(0x155c2fc,'IO-result','short item-tag transfer'),0x11d411f:(0x11d411d,'dead','xor eax,eax then test al,al cannot take JNE'),
    0x29c6c:(0x29c69,'context-lifecycle','type 24 cannot enter type 10 EDfx view'),0x90a2c:(0x90a29,'context-lifecycle','null day result takes fallback/UI gate')}

STATIC_SITES=(0xf2ba38,0xf2ba51,0xf51665,0xf51671,0xf55120,0xffa3b0,0x3cefc62,0x3cefca4,0x3cefcb2,0x3cefd4e,
              0xf4e131,0xf2dbd0,0xf2dbd3,0x155b450,0x155b390,0x11d01c0,0x150ec50,0x814110,0x11d52d0,
              0x14cf8bc,0x14cf8c4,0x14cf8cb,0x14d5ea0,0x103f9f0,0x3d5c091,0x3d5c098,0x2b4a2,0x41d34,0xa999d,0xa99e3,
              0x155a464,0x155a46e,0x155a476,0x155a4b8,0x155a55d,0x155a55f,0x155a593,0x155a599,0x155a5a9,0x155a5b1,
              0x155a5b8,0x155a5c4,0x155a60a,0x155a633,0x155a63b,0x155a650,0x155a658)

def static(old):
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64
    from capstone.x86 import X86_OP_IMM,X86_OP_MEM,X86_REG_RIP
    sys.path.insert(0,str(ROOT/'scripts'))
    from t05_pe import PE
    from t21b_control_flow import ReaderCFG
    p=PE(EXE); ck(h(p.raw)==EXEH,'editor input SHA'); p.pe.parse_data_directories(directories=[3]); m=Cs(CS_ARCH_X86,CS_MODE_64); m.detail=True
    ins={}; ext={}; branch=[]
    def rec(o,i=None):
        if o in ins: return ins[o]
        i=i or next(m.disasm(p.raw[o:o+15],p.f2va(o),count=1)); a=dict(file_offset=o,VA=p.f2va(o),bytes=i.bytes.hex(),instruction=(i.mnemonic+' '+i.op_str).rstrip())
        if i.operands and i.operands[0].type==X86_OP_IMM and (i.mnemonic.startswith('j') or i.mnemonic=='call'):
            a['direct_target']=p.va2f(i.operands[0].imm)
        rip=[i.address+i.size+x.mem.disp for x in i.operands if x.type==X86_OP_MEM and x.mem.base==X86_REG_RIP]
        if rip: a['rip_targets_VA']=rip
        ins[o]=a;return a
    for f in CFG:
        c=ReaderCFG(p,m,f); ext[str(f)]=dict(entry=f,end_exclusive=c.function_end_off,reachable=len(c.instructions),external_edges=c.external_edges)
        for va,i in c.instructions.items(): rec(p.va2f(va),i)
    for s in STATIC_SITES+tuple(FIELD[k][0] for k in FIELD): rec(s)
    for k in ('getter','setter','projection','read_chain','archive_candidate_context','main_table_context_comparison'):
        for s in old['parents']['TCrs']['new_evidence'][k]: rec(s)
    def cell(base,index,target):
        o=base+4*index; data=p.raw[o:o+4]; va=p.f2va(base)+S.unpack('<i',data)[0]; ck(p.va2f(va)==target,'rel32')
        return dict(base=base,index=index,offset=o,raw=data.hex(),target=target,target_VA=va)
    cells={k:cell(0x155a728,int.from_bytes(k.encode(),'big')-0x50556e49,x[0]) for k,x in FIELD.items()}
    cells['aux_type9']=cell(0x14d0184,9,0x14cf8bc)
    v=p.va2f(0x1418b9c08+16); data=p.raw[v:v+8]; ck(p.va2f(S.unpack('<Q',data)[0])==0x14d5ea0,'typed vslot')
    cells['aux_type9_slot2']=dict(offset=v,raw=data.hex(),target=0x14d5ea0)
    for s,(pred,kind,reason) in BR.items():
        x=ins[s]; branch.append(dict(site=s,classification=kind,predicate=pred,predicate_instruction=ins[pred]['instruction'],taken=x['direct_target'],fallthrough=s+len(bytes.fromhex(x['bytes'])),reason=reason))
    for a,dst in [(0x105dd63,0x155b450),(0x11d4bfe,0x155b450),(0x3bb97ec,0x11d3200),(0x29c80,0x907f0),(0x90a24,0xb02980),(0x90fd3,0x83d5a0)]:
        ck(ins[a]['direct_target']==dst,('call target',a,dst))
    # Scope this negative to two exact/mirrored forms and explicit encodings; not an exhaustive computed-key search.
    def hits(buf,key): return [x.start() for x in re.finditer(re.escape(key),buf)]
    rsrc=[x for x in p.pe.sections if x.Name.rstrip(b'\0')==b'.rsrc']
    section=[dict(start=int(x.PointerToRawData),size=int(x.SizeOfRawData),matches={k:hits(p.raw[x.PointerToRawData:x.PointerToRawData+x.SizeOfRawData],v) for k,v in {'ascii':b'EDsc','utf16le':'EDsc'.encode('utf-16le'),'label_utf16le':'Schedule'.encode('utf-16le')}.items()}) for x in rsrc]
    sc={k:hits(p.raw,v) for k,v in {'ascii':b'EDsc','reverse':b'csDE','utf16le':'EDsc'.encode('utf-16le'),'reverse_utf16le':'csDE'.encode('utf-16le')}.items()}
    ck(not any(sc.values()),'EDsc literal scans')
    cfg_id=0x28150
    c=ReaderCFG(p,m,cfg_id); target=int.from_bytes(b'EDsc','big'); deltas={}; intervals=[]
    for i in c.instructions.values():
        if i.mnemonic not in ('add','sub','lea','xor','cmp') or not i.operands: continue
        dest=i.reg_name(i.operands[0].reg) if i.operands[0].type==1 else ''
        if dest not in ('esi','edx','eax'): continue
        for op in i.operands[1:]:
            if op.type==X86_OP_IMM:
                v=op.imm&0xffffffff
                if abs(v-target)<=0x100: intervals.append([p.va2f(i.address),i.mnemonic,dest,v]);
                if v==target or v==(-target & 0xffffffff): deltas[str(p.va2f(i.address))]=v
    # Out-of-line dispatch arms/loaded keys remain out of scope of this bounded probe.
    return ext,ins,cells,branch,dict(literals=sc,pe_resource_sections=section,handler_entry=cfg_id,near_immediates=sorted(intervals),direct_or_signed_add=deltas,
                                  scope='PE literals and direct-reachable selected-register arithmetic/compares near the EDsc FourCC in the EDfx dispatcher; not a general symbolic dispatcher/resource loader')

BASEFILES=['docs/BASELINE.md','scratch/t37/out/REPORT.md','scratch/t37/out/nation_subtable_inventory.json',
 'scratch/t47/out/REPORT.md','scratch/t47/out/discovery_nation_unknown.json','scratch/t49/out/REPORT.md','scratch/t49/out/discovery_t9_wire.json',
 'scratch/t50/out/REPORT.md','scratch/t50/out/profile_t9.json','scratch/t51/out/REPORT.md','scratch/t51/out/discovery_unknown2.json']

def build():
    manifest={x['path']:x['sha256'] for x in j('evidence/MANIFEST.json')['files']}; ck(h((ROOT/MASTER).read_bytes())==manifest[MASTER]==MH,'schema SHA')
    master=j(MASTER); old=j('scratch/t51/out/discovery_unknown2.json'); t50=j('scratch/t50/out/profile_t9.json')
    t49=runpy.run_path(str(ROOT/'scripts/t49_nation_t9.py')); raw,meta=t49['archives']()
    cursors={}; trials={}; comparisons={}
    for side in SIDES:
        b=raw[side,MEMBERS[0]]; a=raw[side,MEMBERS[1]]; mode=int(side=='server')
        def slot19(blob,m):
            ok,err=t49['probe'](blob,m)
            return dict(closed=ok is not None,first_failure=err,rows=ok['row_count'] if ok else None)
        trials['main_'+side]={str(m):slot19(b,m) for m in (0,1)}
        trials['extra_as_slot19_'+side]={str(m):slot19(a,m) for m in (0,1)}
        trials['extra_named_'+side]={str(m):trial(aux_walk,a,side,m) for m in (0,1)}
        trials['extra_named_without_object_name_arm_'+side]=trial(aux_walk,a,side,mode,False)
        cm=main_walk(b,side); ca=aux_walk(a,side,mode); cursors.update({'main_'+side:cm,'extra_'+side:ca})
        profile=(ROOT/f'scratch/t50/out/profiles/table_{side}_extra_9.rows.jsonl').read_bytes(); rows=[json.loads(x) for x in profile.splitlines()]
        ck(len(rows)==len(ca['rows'])==251,'extra census')
        conflicts=[]
        for now,prev in zip(ca['rows'],rows):
            if [now['start'],now['end']]!=[prev['offset'],prev['offset']+prev['len']]:
                conflicts.append(dict(row=now['row'],t50=[prev['offset'],prev['offset']+prev['len']],replay=[now['start'],now['end']],
                    replay_ordinal_raw=a[now['start']:now['start']+4].hex(),t50_start_raw=a[prev['offset']:prev['offset']+8].hex(),
                    witness={'consumed_past_t50_end':a[prev['offset']+prev['len']:now['end']].hex()} if now['end']>prev['offset']+prev['len'] else
                    {'bytes_before_replay_start':a[prev['offset']:now['start']].hex()}))
            else: ck(now['name_hex']==prev['marker']['name_hex'],'t50 prefix')
        comparisons[side]=dict(profile_sha256=h(profile),prefix='u32 ordinal | u32 byte length | name; not an item',block0={'ordinal':0,'absolute':12,'raw':a[12:31].hex(),'name':bytes.fromhex(ca['rows'][0]['name_hex']).decode()},
            dual_list=conflicts,accepted_t50_not_changed=True,profile_anchors=t50['members'][f'{side}/table_extra_9.dat'] if f'{side}/table_extra_9.dat' in t50['members'] else None)
    ordinals,uids,pt=people(t49['dbroot']()); fl=fields(cursors,master,ordinals,uids)
    ext,ins,cells,branch,sc=static(old)
    mn=cursors['main_server']; ax=cursors['extra_server']; ck(mn['summary']['presence']=={'0':166,'1':85},'main gates'); ck(ax['summary']['items']==76,'extension items'); ck(mn['summary']['items']==2219,'main item census')
    # Truncated row-1 vector: retain original absolute coordinates, not slice-relative positions.
    sample=raw['server',MEMBERS[0]]; short_tag=bytearray(sample[:1736]); short_tag[1731:1735]=b'\1\0\0\0'
    # Capacity guard catches a true short buffer before entering the inner reader; the IO n=1 case below
    # models a failing tag transfer after the count and allocation have already succeeded.
    io_example=dict(real_vector_start=1727,short_stream_ends_at=1736,tag_read_at=1735,requested=2,
                    note='synthetic loss after count; guarded offline cursor rejects earlier at the count',
                    strict_guard=trial(lambda: {'rows':[observed(Span(short_tag,1727,len(short_tag),1))]}))
    examples={0x105cbb1:trials['main_client']['1'],0x105dbc5:'modern context >0xdc3; old extra transfer not replayed',
              0x105dd19:[mn['rows'][i]['presence_at'] for i in (0,1)],0x105dd6a:io_example,0x11d4143:trials['extra_named_client']['1'],
              0x11d3472:trials['extra_named_without_object_name_arm_client'],0x11d4b66:[ax['rows'][i]['presence_at'] for i in (0,6)],
              0x155c378:'synthetic tags 1/2 consume 10/11 B; all observed tags=3',0x155c3f3:'synthetic tags 2/3 consume 11/12 B',
              0x4387b6f:'all present vectors have version=2; a synthetic version=3 skips cleanup but reads the same wire length',
              0x155c300:io_example,0x11d411f:'taken edge contradicts preceding xor; not merely unobserved',
              0x29c6c:'static alternate: selected type=24 rejects even with exact EDfx key',
              0x90a2c:'static alternate: null day-vector result goes to 0x90e30, not to a record sink'}
    for item in branch: item['witness']=examples.get(item['site'])
    def flags(cur):
        xs=[(r,i,bytes.fromhex(i['raw'])) for r in cur['rows'] if r['vector'] for i in r['vector']['items']]; result={}
        for idx in (10,11):
            result[str(idx)]=dict(counts=hist(b[idx] for r,i,b in xs),bit_true_counts={hex(bit):sum(bool(b[idx]&bit) for r,i,b in xs) for bit in (1,2,4,8,16,32,64,128)},
              first_by_raw={str(v):next(dict(row=r['row'],item=i['item'],absolute=i['absolute']+idx,raw=f'{v:02x}') for r,i,b in xs if b[idx]==v) for v in set(b[idx] for r,i,b in xs)})
        return result
    efx=old['parents']['EDfx']; esc=old['parents']['EDsc']; edscope=master['entities']['nation.xml'][0]['fields']; rules=master['rule_groups']['advanced\\database test\\comp test.xml']; rule=next(x for z in rules if z['id']=='cpts' for x in z['fields'] if x['field']=='EDsc')
    discovery=dict(status='dual_wire_closed_fields_held_EDsc_partial',L3_fields=0,L4=0,
      source=dict(editor=str(EXE),editor_sha256=EXEH,master_path=MASTER,master_sha256=MH,unchanged={p:h((ROOT/p).read_bytes()) for p in BASEFILES},t51_source_verbatim=old['source']),
      TCrs=dict(scope='nation.xml#nation parent 64',getter_backing='table_extra_9.dat',main_wire='table_9.dat',distinct_slots=True,
        no_alias_claim='Separate constructor/allocated vector destinations and separate writers; no migration/alias in examined routes; universal absence not asserted',
        evidence_table={'getter_extension':dict(owner_path=[176,72],member=MEMBERS[1],client_mode=0,server_mode=1,allocation_sites=[0x11d4b71,0x3ebb864],vector_write=[0x11d3429,0x11d4bad,0x3ebb8c7],read_sites=[0x11f3e44,0x11f3e54,0x11f40a8],fill=[0x11d4bfe,0x155b450,0x4387b46,0x155c120],opener=[0xf51665,0xf51671,0xf55120,0x3bb9698,0x3bb96d6,0x3bb9708,0x3bb9748,0x3bb97ec]),
          'main':dict(owner_path=[392],member=MEMBERS[0],client_mode=0,server_mode=1,allocation_sites=[0x105dd20],vector_write=[0x1059d50,0x105dd56],read_sites=[0x10608bb,0x10608e9],writer=[0x10608dc,0x10608f8,0x155b390],fill=[0x105dd63,0x155b450,0x4387b46,0x155c120],context=[0xf2ba38,0xf2ba51,0x105cb2c,0x105cb49,0x105cbb1,0x105dbc0,0x105dbc5]),
          'shared':dict(item_width_in_memory=12,vector_header_allocation=24,item_allocation_site=0x155c2c5,pool_materialization=0x155c268,pool_VA=0x141b5e150,tag_wire_widths={'lt2':10,'eq2':11,'ge3':12})},
        t51_verbatim={k:v for k,v in old['parents']['TCrs'].items() if k!='new_evidence'}, t51_previous_chains=old['parents']['TCrs']['new_evidence'],
        no_comparison_rewrites=True,extra_profile=comparisons, item_state={'wire_offsets':[10,11],'object_offsets':[8,9],
          'interpretation':'+8 is an octet transfer, no schema code or named bits claimed; +9 uses a nonzero test (not an established bitmask field), switches reference resolution in two context arms',
          'sites':[0x155c3e0,0x155c40c,0x155a464,0x155a46e,0x155a55f],'profiles':{k:flags(c) for k,c in cursors.items()}}),
      trials=trials,archives={s:{**{k:v for k,v in meta[s].items() if k!='members'},'members':{k:meta[s]['members'][k] for k in MEMBERS}} for s in SIDES},
      summaries={k:c['summary'] for k,c in cursors.items()},people=pt,extents=ext,dispatch=cells,
      EDfx=dict(status='editor_only_generated_output_on_traced_route',persistence_scope='Output not sent to archive/record sink on this route. Upstream imported competition/rules/calendar inputs may themselves be persisted.',
               input_sites=[0x29c66,0x29c80,0x9082e,0x90880,0x908c3,0x909d9,0x3d5c091,0x90a24],
               day_temp_sites=[0x90a32,0x90ae0,0x90aa8,0x90e07,0x90e0c,0x90e1c],result_sink=[0x90fc3,0x90fc8,0x90fd3,0x83d5d2,0x83d5d6,0x90fdb,0x90fe3,0x29c85,0x29f68,0x29f7f],t51_verbatim=efx),
      EDsc=dict(status='negative_strengthened_no_verified_call_chain',scan=sc,schema=edscope[344],rule_schema=rule,rule_scope='advanced/database test/comp test.xml#cpts',
                limits='Read-only list plus other rule occurrence is not proof of no persistence; no verified resource selection or computed dispatch found in bounded search',t51_verbatim=esc))
    OUT.mkdir(parents=True,exist_ok=True)
    instructions=sorted(ins.values(),key=lambda x:x['file_offset'])
    for i in range(0,len(instructions),600): write(f'instructions.part{i//600+1:03}.json',instructions[i:i+600])
    write('branches.part001.json',branch); write('discovery_crs_wire.json',discovery)
    for k,c in cursors.items(): write(f'cursor_crs_{k}.json',c)
    for k,v in fl.items(): write(f'fields_{k}.json',v)
    print('t53 build OK: 4 x 251 rows; 2219 main + 76 auxiliary items; field promotions=0; L4=0')

def selftest():
    for tag,length in [(1,10),(2,11),(3,12),(-1,10)]:
        b=S.pack('<IIh',2,1,tag)+bytes(length-2); c=Span(b,0,len(b),0)
        ck(observed(c)['items'][0]['end']==8+length,'tag width')
        ck(not trial(lambda: {'rows':[observed(Span(b[:-1],0,len(b)-1,0))]})['closed'],'short read')
    print('t53 builder selftest: OK')

def main():
    ap=argparse.ArgumentParser(description=__doc__); g=ap.add_mutually_exclusive_group(); g.add_argument('--build',action='store_true'); g.add_argument('--selftest',action='store_true'); args=ap.parse_args()
    try: selftest() if args.selftest else build()
    except Check as e: print('FAIL:',e,file=sys.stderr); return 1
    except Exception as e: print('ERROR:',e,file=sys.stderr); return 2
    return 0

if __name__=='__main__': raise SystemExit(main())
