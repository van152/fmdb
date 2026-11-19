#!/usr/bin/env python3
"""Independently verify t53 from the archive directory, wire bytes, schema and PE."""
import argparse
from collections import Counter, deque
from hashlib import sha256
import json
import os
from pathlib import Path
import struct
import sys

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
MEM=('table_9.dat','table_extra_9.dat')
SIDES=('client','server')
HEAD=bytes.fromhex('03017461642ef10d')

class Reject(Exception): pass
def need(x,msg):
    if not x: raise Reject(msg)
def j(p): return json.loads(p.read_bytes())
def h(b): return sha256(b).hexdigest()
def hist(xs): return {str(k):v for k,v in Counter(xs).items()}
def integer(b,p,fmt): return struct.unpack_from('<'+fmt,b,p)[0]

def read_archives(root,d):
    import zstandard as z
    def frame(blob,more=False):
        dec=z.ZstdDecompressor().decompressobj(); b=dec.decompress(blob)
        need(dec.eof and (more or not dec.unused_data),'Zstd frame');return b,dec.unused_data
    result={}
    for side,total in zip(SIDES,(31,77)):
        blob=(root/f'{side}_db.dat').read_bytes(); fmf=bytes.fromhex('0201666d662e080000')
        need(blob[:8]==HEAD and blob[8:17]==fmf,'archive signature')
        toc,base=(17+x for x in struct.unpack_from('<QQ',blob,17)); need(base==34 and blob[toc:toc+9]==fmf,'TOC')
        zdir,_=frame(blob[toc+9:]); cursor=0; entries={}
        def string():
            nonlocal cursor
            n=integer(zdir,cursor,'I'); cursor+=4; s=zdir[cursor:cursor+n]; need(len(s)==n,'directory string'); cursor+=n;return s.decode('utf8')
        def folder(prefix,level=0):
            nonlocal cursor
            need(level<=40,'directory depth'); path=prefix+string()+'/'
            n=integer(zdir,cursor,'I'); cursor+=4; need(n<100000,'directory file count')
            for _ in range(n):
                key=(path+string()+string()).lstrip('/'); need(key not in entries,'unique entry')
                entries[key]=struct.unpack_from('<5Q',zdir,cursor);cursor+=40
            n=integer(zdir,cursor,'I');cursor+=4; need(n<100000,'directory folder count')
            for _ in range(n): folder(path,level+1)
        folder('');need(cursor==len(zdir) and len(entries)==total,'directory EOF')
        for name in MEM:
            off,packed,declared,*times=entries[f'{side}_db/{name}']; a=base+off; end=a+packed
            nxt=min((base+o[0] for o in entries.values() if o[0]>off),default=toc);need(a<end<=nxt,'member bound')
            rem=blob[a:end]; part=rem; pos=a; framed=[]; found=[]
            while rem:
                b,tail=frame(rem,True); used=len(rem)-len(tail);need(used>0,'frame progress')
                framed.append([pos,used,len(b)]);pos+=used;rem=tail
                if len(b)==declared: found.append(b)
            need(len(found)==1 and pos==end,'declared member frame'); b=found[0]
            expect=d['archives'][side]['members'][name]
            need(expect['bounds']==[a,end,nxt] and expect['frames']==framed and expect['entry']['sha256']==h(part)
                 and expect['payload_sha256']==h(b),'member evidence SHA')
            result[side,name]=b
    return result

class Bounded:
    def __init__(self,b,a,end): self.b=b; self.p=a; self.end=end
    def skip(self,n):
        a=self.p; self.p+=n; need(n>=0 and self.p<=self.end,('underflow/short transfer',a,n,self.end));return self.b[a:self.p]
    def read(self,f): return struct.unpack('<'+f,self.skip(struct.calcsize('<'+f)))[0]
    def string(self): return self.skip(self.read('I'))
    def vector(self,fmt,stride): return self.skip(self.read(fmt)*stride)

def unpack_items(r):
    v=r.p; ver=r.read('I'); at=r.p; n=r.read('I'); start=r.p; its=[]; need(n<=(r.end-start)//10,('invalid item count',at,n))
    for i in range(n):
        a=r.p; tag=r.read('h'); width=10+int(tag>=2)+int(tag>=3); r.skip(width-2)
        its.append(dict(item=i,absolute=a,end=r.p,tag=tag,raw=r.b[a:r.p].hex()))
    return dict(version_at=v,version=ver,count_at=at,count=n,start=start,end=r.p,items=its)

def aux(b,mode):
    need(b[:12]==HEAD+struct.pack('<I',251),'aux header'); r=Bounded(b,12,len(b)); out=[]
    for index in range(251):
        a=r.p; val=r.read('i'); need(val==index,('aux ordinal',a,index,val)); name=r.string(); name_end=r.p
        r.skip(2); r.string(); r.vector('B',27);r.skip(8); base=r.p; typed=[]; presence=gate=vec=None
        if mode:
            r.vector('h',20);r.vector('b',6);r.skip(16)
            n=r.read('H');need(n<=(r.end-r.p)//37,'typed count')
            for _ in range(n):
                q=r.p; sel=r.read('B'); need(sel==9,('typed selector',q,sel));r.skip(20)
                for _ in range(4):r.string()
                typed.append([q,sel,r.p])
            gate=r.p; presence=r.read('B');need(presence in (0,1),'aux presence')
            if presence: vec=unpack_items(r)
        out.append(dict(row=index,start=a,end=r.p,name_hex=name.hex(),name_end=name_end,base_end=base,row_sha256=h(b[a:r.p]),
             typed_records=typed,presence_at=gate,presence=presence,vector=vec))
    need(r.p==len(b),('aux EOF',r.p));return out

def main_member(b,side):
    prev=j(ROOT/f'scratch/t49/out/cursor_t9_{side}.json'); mode=(side=='server'); anchor=[]; p=13; seen=set()
    need(h(b)==prev['payload_sha256'] and b[:12]==HEAD+struct.pack('<I',251),'frozen main payload')
    for i,row in enumerate(prev['rows']):
        q=row['end']; uid=integer(b,q-8,'I');need(row['wire13']==p and b[p]==0 and uid and uid not in seen,'row and UID')
        need(tuple(row['identity'])==struct.unpack_from('<III',b,q-12)==(i,uid,uid),'identity lanes');seen.add(uid)
        need(h(b[p:q])==row['wire_sha256'],'main row digest')
        by_site={int(x[0]):x[1] for x in row['trace'] if x[0] in (0x105dd07,0x105dd87)}
        gate=by_site.get(0x105dd07); nxt=by_site[0x105dd87]; presence=vec=None
        if mode:
            need(p<gate<nxt<=q-12,'target within row'); reader=Bounded(b,gate,nxt); presence=reader.read('B');need(presence<=1,'main gate')
            if presence: vec=unpack_items(reader)
            need(reader.p==nxt,'main next transfer')
        else: need(gate is None and nxt==p+1,'client bypass')
        anchor.append(dict(row=i,start=p,end=q,identity_at=q-12,uid=uid,row_sha256=h(b[p:q]),presence_at=gate,presence=presence,next_site_at=nxt,vector=vec));p=q
    need(len(anchor)==251 and b[p:]==struct.pack('<IBI',0,1,max(seen)),'main footer and EOF');return anchor

def pe_verify(d):
    import pefile
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64
    from capstone.x86 import X86_OP_IMM
    ep=ROOT.parent/'fm24/input/editor.exe'; b=ep.read_bytes();need(h(b)==d['source']['editor_sha256'],'editor SHA')
    pe=pefile.PE(data=b,fast_load=True);pe.parse_data_directories(directories=[3]); base=pe.OPTIONAL_HEADER.ImageBase
    def va(o):return base+pe.get_rva_from_offset(o)
    def off(v):return pe.get_offset_from_rva(v-base)
    ext={x.struct.BeginAddress:x.struct.EndAddress for x in pe.DIRECTORY_ENTRY_EXCEPTION}; m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True
    ins={}
    for part in sorted(OUT.glob('instructions.part*.json')):
        for row in j(part):
            o=row['file_offset']; i=next(m.disasm(b[o:o+15],va(o),count=1));need(o not in ins and row['bytes']==i.bytes.hex() and row['VA']==i.address and row['instruction']==(i.mnemonic+' '+i.op_str).rstrip(),('PE instruction',o))
            if 'direct_target' in row: need(row['direct_target']==off(i.operands[0].imm),('direct target',o))
            ins[o]=i
    for x in d['extents'].values():
        start=x['entry']; stop=off(base+ext[va(start)-base]);need(stop==x['end_exclusive'],'PE extent')
        q=deque([start]); seen=set(); outside=set()
        while q:
            a=q.popleft()
            if a in seen: continue
            seen.add(a); i=ins[a]; n=i.mnemonic; nexts=[]
            if n.startswith('j') and i.operands[0].type==X86_OP_IMM: nexts.append(off(i.operands[0].imm))
            if n not in ('jmp','int3','ud2') and not n.startswith(('ret','iret')):nexts.append(a+i.size)
            for k in nexts:
                if start<=k<stop: q.append(k)
                else: outside.add((a,k))
        need(len(seen)==x['reachable'] and outside=={(int(z['from'],16),off(int(z['target_va'],16))) for z in x['external_edges']},('CFG worklist',start))
    for x in j(OUT/'branches.part001.json'):
        i=ins[x['site']]; need(x['taken']==off(i.operands[0].imm) and x['fallthrough']==x['site']+i.size,'branch witness edges')
    for k,x in d['dispatch'].items():
        a=x['offset']; raw=bytes.fromhex(x['raw']); need(b[a:a+len(raw)]==raw,('dispatch bytes',k))
        dst=va(x['base'])+int.from_bytes(raw,'little',signed=True) if len(raw)==4 else int.from_bytes(raw,'little')
        need(off(dst)==x['target'],('dispatch target',k))
    for a,k in [(0x105dd56,'0x188'),(0x11d4bad,'0x48'),(0x11f3e44,'0xb0'),(0x10608e9,'0x188'),(0x83d5d6,'[rsi]')]:
        need(k in ins[a].op_str,('object lane',a))
    for a,k in [(0x105dd63,0x155b450),(0x11d4bfe,0x155b450),(0x90fd3,0x83d5a0),(0x29c80,0x907f0),(0x3bb97ec,0x11d3200)]:
        need(off(ins[a].operands[0].imm)==k,'edge')
    for form in (b'EDsc',b'csDE','EDsc'.encode('utf-16le'),'csDE'.encode('utf-16le')): need(form not in b,'EDsc negative')
    need(d['EDsc']['scan']['pe_resource_sections']==[] and not any(x.Name.rstrip(b'\0')==b'.rsrc' for x in pe.sections),'PE section inventory')

def verify_fields(d,basic,decoded,master):
    import zstandard as z
    f=z.ZstdDecompressor().decompressobj(); p=f.decompress(basic[8:]); end=5; ordinal={}; uid={}
    need(f.eof and not f.unused_data and p[:5]==bytes.fromhex('5b0a0a0000'),'person frame')
    for index in range(integer(p,0,'I')):
        cls=p[end+1]; need(p[end]==17 and cls in (1,2,3,4,5),'person row class');end+=83 if cls<=3 else 34 if cls==4 else 22
        key,u,w=struct.unpack_from('<III',p,end-12);need(key==index and u==w and u and u not in uid,'person key');ordinal[key]=[u,cls];uid[u]=key
    need(len(uid)==658011 and p[end:]==bytes.fromhex('00000000014cbd5477') and d['people']['end']==end and d['people']['payload_sha256']==h(p),'person identity EOF')
    parent=master['entities']['nation.xml'][0]['fields'][64]; need(parent['field']=='TCrs','scoped parent'); enums={int(x['enum']) for x in master['enums']['ftjn']['values']}
    for k,lane,fmt in [('PUnP',2,'i'),('PUnI',6,'B'),('PUnT',7,'b'),('PUnJ',8,'H')]:
        ledger=j(OUT/f'fields_{k}.json');need(ledger['grade']=='held' and ledger['schema']==next(x for x in parent['list_item_fields'] if x['field']==k),'schema gate')
        for name,rs in decoded.items():
            x=ledger['archives'][name]; rows=[]; checks=Counter(); first={}
            for r in rs:
                for it in (r['vector'] or {}).get('items',[]):
                    a=it['absolute']+lane; b=bytes.fromhex(it['raw']); v=integer(b,lane,fmt); w=struct.calcsize(fmt)
                    need(it['tag']==3 and len(b)==12,'observed item tag/size')
                    rec=dict(row=r['row'],item=it['item'],absolute=a,raw=b[lane:lane+w].hex(),value=v)
                    labels=[]
                    if k=='PUnP':
                        rec.update(sentinel=v==-1,state_byte=b[11],ordinal_target=ordinal.get(v),uid_target_ordinal=uid.get(v))
                        if v!=-1: labels=['ordinal_'+('hit' if v in ordinal else 'miss'),'UID_probe_'+('hit' if v in uid else 'miss')]
                        else: first.setdefault('sentinel',rec)
                    if k=='PUnJ':
                        rec['in_ftjn']=v in enums;labels=['ftjn_hit' if rec['in_ftjn'] else 'ftjn_miss']
                    for label in labels:checks[label]+=1;first.setdefault(label,rec)
                    rows.append(rec)
            need(x['rows']==rows and x['histogram']==hist(r['value'] for r in rows) and x['checks']==checks and x['first_by_check']==first,('all item value gates',name,k))

def verify():
    root=Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
    need(root.drive.upper()!='Z:' and root.resolve().drive.upper()!='Z:','Z: forbidden')
    sys.path.append(str(ROOT.parent/'fm24/tools/python'))  # local read-only pinned zstandard wheel
    d=j(OUT/'discovery_crs_wire.json');need(d['L4']==0 and d['L3_fields']==0,'grades');m=ROOT/d['source']['master_path']
    manifest={x['path']:x['sha256'] for x in j(ROOT/'evidence/MANIFEST.json')['files']};need(h(m.read_bytes())==d['source']['master_sha256']==manifest[d['source']['master_path']],'manifest')
    for group in [d['source']['unchanged'],d['source']['t51_source_verbatim']['unchanged']]:
        for name,sum_ in group.items():need(h((ROOT/name).read_bytes())==sum_,('predecessor not changed',name))
    raw=read_archives(root,d); decoded={}
    for side in SIDES:
        mode=(side=='server'); a=raw[side,MEM[1]]; b=raw[side,MEM[0]]
        for k,rows,blob in [('main',main_member(b,side),b),('extra',aux(a,mode),a)]:
            key=k+'_'+side; decoded[key]=rows; c=j(OUT/f'cursor_crs_{key}.json')
            need(c['rows']==rows and c['mode']==mode and c['payload_sha256']==h(blob),('cursor replay',key))
            pres=[r['presence'] for r in rows if r['presence'] is not None]; vs=[r['vector'] for r in rows if r['vector'] is not None]; its=[i for v in vs for i in v['items']]
            summary=dict(presence=hist(pres),skipped=251-len(pres),counts=hist(v['count'] for v in vs),version=hist(v['version'] for v in vs),tags=hist(i['tag'] for i in its),item_width=hist(i['end']-i['absolute'] for i in its),items=len(its))
            need(c['summary']==d['summaries'][key]==summary,'summary')
            states=d['TCrs']['item_state']['profiles'][key]
            for o in (10,11):
                vals=[bytes.fromhex(i['raw'])[o] for i in its]; s=states[str(o)];need(s['counts']==hist(vals) and s['bit_true_counts']=={hex(i):sum(1 for v in vals if v&i) for i in (1,2,4,8,16,32,64,128)},'bit counts')
        try: aux(a,not mode)
        except Reject: pass
        else: raise Reject('wrong aux mode unexpectedly closed')
        f=(ROOT/f'scratch/t50/out/profiles/table_{side}_extra_9.rows.jsonl').read_bytes(); tp=[json.loads(x) for x in f.splitlines()]; diff=[]
        for r,v in zip(decoded['extra_'+side],tp):
            ar=[r['start'],r['end']]; old=[v['offset'],v['offset']+v['len']]
            if ar!=old:diff.append([r['row'],old,ar]);continue
            need(r['name_hex']==v['marker']['name_hex'],'name per profile')
        dd=d['TCrs']['extra_profile'][side];need(h(f)==dd['profile_sha256'] and diff==[[x['row'],x['t50'],x['replay']] for x in dd['dual_list']],'t50 dual-list')
    need(d['summaries']['main_server']['presence']=={'0':166,'1':85} and d['summaries']['extra_server']['items']==76,'key cardinalities')
    mr=decoded['main_server'][1];need(mr['presence_at']==1726 and mr['next_site_at']==2035,'row 1 witness')
    need(integer(raw['client',MEM[0]],28,'i')==1543569408 and struct.unpack_from('<III',raw['server',MEM[0]],59)==(0,0,0),'main incorrect-mode inputs')
    verify_fields(d,(root/'basic_people_db.dat').read_bytes(),decoded,j(m));pe_verify(d)
    print('t53 verify: 4 x 251 rows; 2219 main + 76 getter items; PE, joins, held and negatives OK; L4=0')

def selftest():
    r=Bounded(struct.pack('<IIh',2,1,2)+b'\0'*9,0,19)
    need(unpack_items(r)['items'][0]['end']==19,'tag-2 regression')
    try: unpack_items(Bounded(struct.pack('<II',2,1),0,8))
    except Reject: pass
    else: raise Reject('truncation regression')
    print('t53 independent selftest: OK')

def entry():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--selftest',action='store_true');args=ap.parse_args()
    try:selftest() if args.selftest else verify()
    except Reject as e: print('FAIL:',e,file=sys.stderr);return 1
    except Exception as e: print('ERROR:',e,file=sys.stderr);return 2
    return 0

if __name__=='__main__': raise SystemExit(entry())
