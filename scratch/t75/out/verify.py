"""Independent t75 verifier: member frames, frozen cursors, vector lanes and PE witnesses."""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
import runpy
import struct
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SIDES = ('client','server')
NUMBERS = (3,5,8,10,19,21,25,56)
LAYOUT = {'club':(3,57,63),'comp':(25,59,64),'nation':(10,55,65)}
MAGIC = bytes.fromhex('0201666d662e080000')
HEAD = bytes.fromhex('03017461642ef10d')
EXEH = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
BASE_WIDTHS = {2: (4,),3: (4,),11:(1,4,4,4,2,1,1,4,1,1),12:(4,4,4),13:(1,4,4,1,1,1,1,1),
               23:(4,1),24:(4,)*7,25:(4,)*7,26:(4,)*3}
COUNTS = {2:'h',3:'i',4:'h',11:'i',12:'I',13:'I',23:'b',24:'i',25:'i',26:'i'}
ITEM_TALLY = {2:0,3:0,4:7,11:1899,12:27178,13:58,23:492,24:214,25:63,26:162}
ABCD = {23:('Nlns',('lang','perc')),24:('Nefr',('nfrn','nfrc','fren','nfrr','nfra','stdt','endt')),
        25:('Nnfr',('nfrn','nfrc','fren','nfrr','nfra','stdt','endt')),26:('Nagr',('NGag','NGsd','NGed'))}
REF = {'language':8,'nation':10,'continent':5,'region':19,'agreement':56,'club':3}

class Check(Exception): pass


def ck(cond, detail):
    if not cond:raise Check(detail)


def read(path):return json.loads((ROOT/path).read_bytes())
def prev(t,name):return f'scratch/t{t}/out/{name}'
def digest(b):return sha256(b).hexdigest()
def u(b,p):return struct.unpack_from('<I',b,p)[0]
def hist(seq):return {str(x):n for x,n in Counter(map(int,seq)).items()}


def archives():
    db=Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data').resolve(); vendor=ROOT.parent/'fm24/tools/python'
    if any(p.resolve().drive.upper()=='Z:' for p in (db,vendor)):raise ValueError('Z: forbidden')
    sys.path.insert(0,str(vendor)); import zstandard as z
    def frame(buf):
        ck(buf[:4]==bytes.fromhex('28b52ffd'),'frame signature')
        d=z.ZstdDecompressor().decompressobj(); data=d.decompress(buf); consumed=len(buf)-len(d.unused_data)
        ck(d.eof and consumed>0,'frame end');return data,consumed
    out={}
    for side,expected in zip(SIDES,(31,77),strict=True):
        blob=(db/f'{side}_db.dat').read_bytes(); ck(blob[8:17]==MAGIC,'container magic')
        toc,base=(17+x for x in struct.unpack_from('<QQ',blob,17))
        ck(base==34 and base<toc<len(blob) and blob[toc:toc+9]==MAGIC,'archive bounds')
        raw,n=frame(blob[toc+9:]);ck(toc+9+n==len(blob),'directory frame EOF');pos=0;files={}
        def get(n):
            nonlocal pos
            ck(0<=n<=len(raw)-pos,'directory bounds');p=pos;pos+=n;return raw[p:pos]
        def integer():return int.from_bytes(get(4),'little')
        def text():return get(integer()).decode('utf8')
        def walk(parent,depth):
            ck(depth<40,'directory depth'); parent=parent/text()
            for _ in range(integer()):
                path=parent/(text()+text()); fields=struct.unpack('<QQQQQ',get(40)); ck(not path.is_absolute() and '..' not in path.parts and path not in files,'index path')
                files[path]=fields[:3]
            for _ in range(integer()): walk(parent,depth+1)
        walk(PurePosixPath(),0);ck(pos==len(raw) and len(files)==expected,'directory size/EOF')
        for tid in NUMBERS:
            lo,w,size=files[PurePosixPath(f'{side}_db/table_{tid}.dat')]; end=base+lo+w
            bound=min((base+a for a,_,_ in files.values() if a>lo),default=toc)
            p=base+lo; ck(base<=p<end<=bound,'member bound');matches=[]
            while p<end:
                payload,n=frame(blob[p:end]);p+=n
                if len(payload)==size:matches.append(payload)
            ck(p==end and len(matches)==1 and matches[0][:8]==HEAD,(side,tid,'unique sized member'))
            out[side,tid]=matches[0]
    return out


def outer(b, name, t, side, fs):
    # Reuse the *prior independent verifiers*, not any builder replay or t75 output coordinates.
    mod=runpy.run_path(str(ROOT/prev(t,'verify.py'))); server=side=='server'
    if name=='club':
        c,uid,_,starts,ends,_,trace=mod['table3'](b,server)
        cols={s['key']:c[s['position']] for s in fs['slots']}
        ck(trace==fs['envelopes'][side]['row_trace_sha256'],(name,side,'whole row digest'))
    elif name=='comp':
        lines,cols,_=mod['replay'](b,server); starts,ends,uid=zip(*lines,strict=True)
        ck(digest(np.array(lines,dtype='<u4').tobytes())==fs['envelopes'][side]['row_trace_sha256'],(name,side,'whole row digest'))
    else:
        lines,_=mod['read_rows'](b,server); starts,ends,uid=[],[],[]; cols={}
        for r,(a,e,trip,book) in enumerate(lines):
            starts.append(a); ends.append(e); uid.append(trip[1]);
            for k,(p,w,_) in book.items():cols.setdefault(f'slot_{k}',[]).append((r,p,w))
        if server:
            lines=(ROOT/prev(46,'profiles/table_server_10.rows.jsonl')).read_bytes()
            anchor=read(prev(46,'profiles/table_server_10.profile.json'))
            ck(digest(lines)==anchor['full_rows_sha256'] and digest(b)==anchor['payload']['payload_sha256'],'t46 profile SHA')
            for a,e,v,line in zip(starts,ends,uid,lines.splitlines(),strict=True):
                o=json.loads(line);ck(o['offset']==a+1 and o['len']==e-a and o['identity']['row_id']==v and bytes.fromhex(o['raw_hex'])==b[a+1:e+1],('t46 witness',a))
    ck(starts[0]==13 and ends[-1]+9==len(b) and np.array_equal(starts[1:],ends[:-1]),(name,side,'envelope'))
    return cols, np.array(starts),np.array(ends)-12


def words(b, offsets, dtype):
    v=np.frombuffer(b,np.uint8); dt=np.dtype(dtype); ix=np.asarray(offsets,dtype=np.int64)
    ck(np.all((ix>=0)&(ix+dt.itemsize<=len(b))),'gather bounds')
    return v[ix[:,None]+np.arange(dt.itemsize)].copy().view(dt).ravel()


def target(b,tid,side, known=None):
    n=u(b,8); e=len(b)-9; starts=known
    if starts is None:
        if tid==8:
            # Independent of the builder's triple candidate filtering: the
            # length-prefixed UTF-8 name is followed by a 17 B tail prefix.
            v=[];p=13
            for _ in range(n):
                ck(b[p]==0,'t8 selector');s=p+5+u(b,p+1); b[p+5:s].decode('utf8')
                v.append(s+17);p=s+29
            ck(p==e,'t8 name cursor EOF');starts=v
        else:
            w={5:(34,48),19:(45,46),21:(38,181),56:(13,13)}[tid][side=='server']; starts=range(13+w-12,e-11,w)
    ends=np.array(starts,dtype=np.int64)
    v=np.stack([words(b,ends+i,'<u4') for i in (0,4,8)],axis=1).astype('<u4')
    ck(len(v)==n and ends[-1]+12==e and np.all(v[:,0]==np.arange(n)) and np.all(v[:,1]==v[:,2]) and
       np.all(v[:,1]!=0) and len(np.unique(v[:,1]))==n,(tid,side,'target raw triples'))
    return v[:,1], dict(count=n,identity_sha256=digest(v.tobytes()),payload_sha256=digest(b),last_identity=int(ends[-1]))


def split_items(b, blocks, pos):
    # Fixed columns via repeat/cumulative sums, variant columns with a bounded sequential parser.
    cw=struct.calcsize(COUNTS[pos]); c=np.asarray(blocks,dtype=np.int64).reshape(-1,3)
    n=words(b,c[:,1],'<'+COUNTS[pos]).astype(np.int64)
    ck(np.all((n>=0)&(n<=c[:,2]-cw)),('count bound',pos))
    rows=np.repeat(c[:,0],n); per_item=np.arange(len(rows))-np.repeat(np.r_[0,np.cumsum(n)[:-1]][:len(n)],n)
    columns={}; records=[]
    if pos not in (4,11):
        widths=BASE_WIDTHS[pos];stride=sum(widths);a=np.repeat(c[:,1]+cw,n)+stride*per_item
        ck(np.array_equal(c[:,2],cw+n*stride),('closed fixed segments',pos))
        records=np.column_stack((rows,per_item,a,np.full(len(rows),stride,dtype=np.int64)))
        if len(rows):
            for off,w in zip(np.r_[0,np.cumsum(widths)[:-1]],widths,strict=True):
                columns[str(off)]=np.column_stack((rows,a+off,np.full(len(rows),w)))
    else:
        for (row,a,l),count in zip(c,n,strict=True):
            q=a+cw; end=a+l
            for i in range(count):
                if pos==4:
                    begin=q; parts={'tag':(q,1)}; q+=1
                    for k in range(4):
                        ck(q+4<=end,('string prefix bounds',row,q)); length=u(b,q); parts[f'len{k}']=(q,4)
                        q+=4;parts[f'str{k}']=(q,length); q+=length
                    for k,key in enumerate(('date','after0','after4','after8','after12')): parts[key]=(q+4*k,4)
                    q+=20
                else:
                    begin=q; ck(q<end,('tax tag bounds',row,q)); w=23+2*(b[q]>=2)
                    offsets=(0,1,5,9,13,15,16,17,21,22,23) if w==25 else (0,1,5,9,13,15,16,17,21,22)
                    parts={str(k):(q+k,j-k) for k,j in zip(offsets,(*offsets[1:],w),strict=True)};q+=w
                ck(q<=end,('variant item bounds',pos,row,q,end));records.append((row,i,begin,q-begin))
                for k,(p,w) in parts.items():columns.setdefault(k,[]).append((row,p,w))
            ck(q==end,('variant segment end',row,pos,q,end))
    return np.asarray(records,dtype='<u4').reshape(-1,4),columns,n


def witness(b, cell, row_starts=None):
    r,a,w=map(int,cell); result={'row':r,'absolute':a,'width':w,'raw':b[a:a+min(w,32)].hex()}
    if row_starts is not None:result['body_relative']=a-int(row_starts[r])-1
    return result


def profile(b,c,metadata,starts):
    a=np.asarray(c,dtype='<u4').reshape(-1,3); w=a[:,2]; coords=digest(a.tobytes())
    ck((metadata['rows'],metadata['bytes'],metadata['coordinates_sha256'],metadata['width_histogram'])==
       (len(w),int(w.sum()),coords,hist(w)),('coordinate profile',coords))
    if not len(w):return None
    ck(metadata['first']==witness(b,a[0],starts) and metadata['last']==witness(b,a[-1],starts),'profile witnesses')
    width=int(w.min()) if w.min()==w.max() else None;ck(metadata['fixed_width']==width,'fixed width')
    if width not in (1,2,4,8):return None
    v=words(b,a[:,1],f'<u{width}');limit=(1<<(8*width))-1
    ck((metadata['value_sha256'],metadata['distinct'],metadata['minimum'],metadata['maximum'],metadata['zero'],metadata['all_ones'])==
       (digest(v.tobytes()),len(np.unique(v)),int(v.min()),int(v.max()),int((v==0).sum()),int((v==limit).sum())),('value profile',coords))
    return v


def reference(b,cells,values,targets,stats):
    live=values!=0xffffffff; r=values[live]; is_ord=(r<len(targets)); UID=np.sort(targets)
    p=np.searchsorted(UID,r); is_uid=UID[np.minimum(p,len(UID)-1)]==r
    good=is_ord & is_uid; diff=int(np.sum(targets[r[good]]!=r[good])); hit=int(is_ord.sum()); uid_hit=int(is_uid.sum())
    ck([stats[k] for k in ('live','all_ones','ordinal_hit','ordinal_miss','uid_hit','uid_wrong_target','legal_zero')]==
       [len(r),len(values)-len(r),hit,len(r)-hit,uid_hit,diff,int((r==0).sum())],'actual target join vs UID control')
    idx=np.flatnonzero(live)
    masks={'first_live':np.ones(len(r),bool),'first_ordinal_miss':~is_ord,'first_uid_miss':~is_uid,'first_wrong_target':np.zeros(len(r),bool)}
    masks['first_wrong_target'][good]=targets[r[good]]!=r[good]
    for k,m in masks.items():
        arr=np.flatnonzero(m); wanted=None
        if len(arr):
            i=idx[arr[0]];v=int(values[i]);hits=np.flatnonzero(targets==v)
            wanted=dict(witness(b,cells[i]),value=v,ordinal_target_uid=int(targets[v]) if v<len(targets) else None,
                        uid_target_ordinal=int(hits[0]) if len(hits) else None)
        ck(stats[k]==wanted,('control witness',k))


def datecheck(values, stats):
    words16=values.view('<u2').reshape(-1,2); yr=words16[:,1]; d=words16[:,0]%512; carry=words16[:,0]//512
    cap=365+((yr%4==0)&((yr%100!=0)|(yr%400==0)))
    invalid=np.count_nonzero((d<1)|(d>cap)|(yr==0))
    ck(stats==dict(year=[int(yr.min()),int(yr.max())],day=[int(d.min()),int(d.max())],flags=hist(carry),invalid=invalid,
                   default_1900_001=int(((yr==1900)&(d==1)).sum())),'packed date range')


def static(x):
    import pefile
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64,CS_OP_IMM
    exe=ROOT.parent/'fm24/input/editor.exe'
    if exe.resolve().drive.upper()=='Z:':raise ValueError('Z: forbidden')
    raw=exe.read_bytes(); ck(digest(raw)==x['editor']['sha256']==EXEH,'editor image SHA')
    pe=pefile.PE(data=raw,fast_load=True); pe.parse_data_directories(directories=[3]); cap=Cs(CS_ARCH_X86,CS_MODE_64);cap.detail=True
    image=pe.OPTIONAL_HEADER.ImageBase; va=lambda a:image+pe.get_rva_from_offset(a); off=lambda v:pe.get_offset_from_rva(v-image)
    instr={}
    for r in x['instructions']:
        a=r['offset']; q=next(cap.disasm(raw[a:a+15],va(a),1)); ck(a not in instr and r['va']==q.address and r['bytes']==q.bytes.hex() and r['insn']==(q.mnemonic+' '+q.op_str).strip(),('PE witness',a)); instr[a]=q
    def dst(q):return off(q.operands[0].imm) if q.operands and q.operands[0].type==CS_OP_IMM else None
    for name,s in x['vtable'].items():
        for _,r in s.items():
            a=r['offset']; ck(r['va']==va(a) and r['bytes']==raw[a:a+8].hex() and r['target']==off(struct.unpack_from('<Q',raw,a)[0]),('vtable ptr',name,a))
    for name,start,end in (('nation',0x103fac0,0x1040be4),('club',0xe5a7a0,0xe5bfca),('comp',0xeb7000,0xeb7e42)):
        extent=[off(image+p.struct.EndAddress) for p in pe.DIRECTORY_ENTRY_EXCEPTION if image+p.struct.BeginAddress==va(start)]
        ck(extent==[end] and (x['bounded_scan'][name]['reader']['root'],x['bounded_scan'][name]['reader']['end'])==(start,end),('PE exception extent',name))
    expected={0x104075b:0x105fb50,0x1040829:0x15cf4a0,0x10408eb:0x15cf4a0,0x10409a7:0x105fbb0,0x1040494:0x144bca0,
              0x10401dd:0x15cf370,0x104053f:0xdb7f80,0x1040554:0xdb7f80,0x1040592:0x104e6b0,0x104e6b0:0x3d74e30,
              0x3d74f9c:0x1072560,0x1072560:0x3daa110,0xe5c5b9:0xf7e280}
    expected.update({0x104056d:0x1040e00,0x1040e00:0x3d5df50,0x3d5df6b:0x104e4c0,0x104e4c0:0x3d745c0})
    for a,t in expected.items():ck(dst(instr[a])==t,('helper rel32',a))
    ed=x['edsc_control']; cell=ed['rel32_cell']; a=cell['offset']; q=instr[0x282b9]
    ck(ed['code']=='EDsc' and ed['prior_id']=='E105' and all(s in instr for s in ed['dispatch']) and
       q.mnemonic=='add' and ((int.from_bytes(b'EDsc','big')+q.operands[1].imm)&0xffffffff)==0x32 and a==0x2a8b8 and
       cell['bytes']==raw[a:a+4].hex() and off(va(0x2a7f0)+struct.unpack_from('<i',raw,a)[0])==cell['target']==0x29389,'nonliteral EDsc control')
    ck(ed['conclusion_verbatim']==read(prev(62,'chain.json'))['conclusions']['EDsc'],'EDsc scope unchanged')
    for r in x['slots']:
        a=r['reader_site']; ck(a is None or a in instr,('slot site',a)); ck(all(y in instr for y in r['selected_chain']),('selected path',r['slot']))
        for hit in r['displacement_xrefs_untyped']:
            for g in hit['keyed_prefix']:
                gate=g['gate']; sites=gate['sites']; k=int.from_bytes(g['code'].encode('ascii'),'big')
                if gate['kind']=='compare':
                    c,b=(instr[y] for y in sites); ck(c.mnemonic=='cmp' and c.operands[-1].imm==k and c.address+c.size==b.address and
                        gate['arm']==(dst(b) if b.mnemonic=='je' else off(b.address+b.size)),('case-sensitive gate',sites))
                elif gate['kind']=='rel32_table':
                    z=gate['cell']; a=z['offset'];ck(z['bytes']==raw[a:a+4].hex() and gate['arm']==off(va(z['table'])+struct.unpack_from('<i',raw,a)[0]),('rel32 cell',a))
                elif gate['kind']=='bt':ck(k==gate['low']+gate['index'] and (gate['mask']>>gate['index'])&1,('bit gate',sites))
                else:raise Check(('gate kind',gate['kind']))
    return instr


def negative_blocks(doc):
    todo=[('',doc)]; expected={}
    while todo:
        path,obj=todo.pop()
        if isinstance(obj,dict):
            for k,v in obj.items():
                key=path+'/'+k.replace('~','~0').replace('/','~1')
                if any(s in k.lower() for s in ('negativ','falsif','reject')):expected[key]=v
                elif k!='fields':todo.append((key,v))
    return expected


def check():
    x=read('scratch/t75/out/xref_reverse.json'); delta=read('scratch/t75/out/field_map_r3.json')
    for p,sha in x['inputs_sha256'].items():ck(digest((ROOT/p).read_bytes())==sha,('pinned input',p))
    mpath='evidence/fm24/reports/editor_schema/master.json'; master=read(mpath); manifest={r['path']:r['sha256'] for r in read('evidence/MANIFEST.json')['files']}
    ck(len(master['field_codes'])==3009 and digest((ROOT/mpath).read_bytes())==manifest[mpath],'frozen field_codes')
    inv=read(prev(72,'inventory.json')); fp=read(prev(72,'fingerprints.json'));ck(x['t72_negative_notes_verbatim']==inv['negative_notes'],'t72 negatives')
    sk={(r['table'],r['slot']):r for r in x['slots']}; expected={(name,r['key']) for name,t in inv['tables'].items() for r in t['slots'] if r['kind'] in ('held','unnamed')}
    ck(set(sk)==expected and len(sk)==len(x['slots'])==99,'target scope/no t66/L3 rows')
    excluded=[{'id':r['id'],'code':r['code']} for r in read(prev(71,'field_map_r3.json'))['fields'] if r['grade']=='L3']
    ck(x['excluded_t71_4cc']==excluded and len(excluded)==24 and not ({r['code'] for r in excluded}&
       {f['code'] for r in x['slots'] if r['table']=='club' for f in r['codes']}),'t71 untouched')
    ck(x['L4']==delta['L4']==delta['new_named_L3']==0,'no unsupported promotion')
    ck(x['negative_evidence']['comp']['t64_exclusions_verbatim']==read(prev(64,'exclusions.json')) and
       x['negative_evidence']['nation']['edsc_exclusions_verbatim']==read(prev(62,'exclusions.json'))['excludes'],'prior exclusions verbatim')
    for name in LAYOUT:
        ck(delta[name]==[dict(id=f't75/{name}/{r["slot"]}',slot=r['slot'],grade='held',reason=r['blocker'],
                              first_counterexample=r['first_counterexample'],prior_ids=r['prior_ids'])
                         for r in x['slots'] if r['table']==name],('incremental held map',name))
    ck(delta['nation_physical_grammar']==[dict(slot=g['escalation']['slot'],grade=g['grade'],prior_ids=g['prior_ids'])
        for g in x['nation_escalations']],'physical grades only')
    code=static(x); dat=archives(); coords,origin,ids={}, {},{}
    for side in SIDES:
        for name,(tid,t,r2) in LAYOUT.items():
            fs=read(prev(t,'field_slots.json')); b=dat[side,tid]; cols,starts,ends=outer(b,name,t,side,fs)
            coords[side,name]=cols;origin[side,name]=starts;ids[side,tid],diag=target(b,tid,side,ends)
            ck(diag==x['target_and_payload_identity'][f'{side}/{tid}'],'replayed source identity')
            ck(diag['identity_sha256']==inv['targets'][str(tid)]['identity_sha256'][side],'frozen source identity')
            originals=read(prev(t,'field_map.json')); prior=read(prev(r2,'field_map_r2.json')); ng=x['negative_evidence'][name]
            def held(r):return r.get('grade')=='held' or r.get('status')=='held' or r.get('r2_status') in ('held','candidate')
            ck(ng['r1_held_verbatim']==[r for r in originals['fields'] if held(r)] and ng['r2_held_verbatim']==[r for r in prior['fields'] if held(r)],(name,'prior held verbatim'))
            ck(ng['r1_negative_keys_verbatim']==negative_blocks(originals) and ng['r2_negative_keys_verbatim']==negative_blocks(prior),
               (name,'prior negative blocks'))
            fpmap={r['key']:r for r in fp['tables'][name]['slots']}
            for z,s in zip(inv['tables'][name]['slots'],fs['slots'],strict=True):
                k=z['key']; c=cols.get(k,[]); a=np.asarray(c,dtype='<u4').reshape(-1,3)
                ck(len(a)==z['coverage'][side],'all outer slot coverage')
                if name=='nation':ck(a[:,1:].tolist()==s['coordinates'][side],('outer nation slot',k))
                elif len(a):ck(digest(a.tobytes())==s['profiles'][side]['coordinate_sha256'],('outer slot',name,k))
                if (name,k) not in sk:continue
                r=sk[name,k]; meta=r['archives'][side]
                ck(r['grade']=='held' and r['first_counterexample'] and r['reader_site']==z['site'] and r['object_displacement']==z['object_displacement'] and r['execution_index']==z['execution_index'],('reverse trial',name,k))
                for match in r['codes']:
                    ck(match['master_locations']==master['field_codes'].get(match['code'],{}).get('locations',[]),'case-sensitive locations')
                ck(meta['t72']==fpmap[k][side],'t72 input exact'); v=profile(b,c,meta,starts)
                if 'date_probe' in meta:datecheck(v,meta['date_probe'])
        for tid in (5,8,19,21,56):
            ids[side,tid],diag=target(dat[side,tid],tid,side)
            ck(diag==x['target_and_payload_identity'][f'{side}/{tid}'],(side,tid,'external target'))
    for tid in NUMBERS:ck(np.array_equal(ids['client',tid],ids['server',tid]),('paired target',tid))
    for (name,k),r in sk.items():
        b=LAYOUT[name][0]
        for side,a in r['archives'].items():
            if 'reference_probe' in a:
                c=coords[side,name][k]; p=a['reference_probe'];v=words(dat[side,b],[t[1] for t in c],f'<u{a["fixed_width"]}')
                reference(dat[side,b],c,v,ids[side,p['table_id']],p)
    held_ftb=read(prev(51,'fields_Nftb.json'))['fields'];held_tax=read(prev(47,'fields_nation_tax.json'))['fields']
    t28=read(prev(28,'fields_nation_client.json'))['fields']; t46=read(prev(46,'grammar_diff_client_server.json'))['segments']
    server_ids=set(); groups=x['nation_escalations']; ck([g['escalation'] for g in groups]==inv['escalations'],'ten escalation records verbatim')
    for g in groups:
        k=g['escalation']['slot']; pos=int(k[5:]); ck(g['count_format']=='<'+COUNTS[pos] and g['grade']==('held_no_items' if pos<4 else 'L3_physical_only'),'grammar grading')
        ck(g['reader_site'] in code and all(s in code for s in g['gate_helper_cursor']),'grammar static sites')
        if pos in ABCD:
            parent,names=ABCD[pos]; ck([f['code'] for f in g['fields']]==list(names) and g['t46_positional_reject_unchanged']==t46[g['escalation']['collection']],('ABCD earlier semantics',k))
        elif pos==4:parent='Nftb'
        elif pos==11:parent='Ntxr'
        else:parent=None
        replay=[]
        for side in SIDES:
            b=dat[side,10];c=coords[side,'nation'].get(k,[]); a=g['archives'][side]; profile(b,c,a,origin[side,'nation']); pts,columns,n=split_items(b,c,pos)
            ck(len(pts)==(ITEM_TALLY[pos] if side=='server' or pos>=23 else 0),(k,side,'all item tally'))
            ck((a['items'],a['nonempty'],a['count_histogram'],a['item_width_histogram'],a['item_coordinates_sha256'])==
               (len(pts),int((n!=0).sum()),hist(n),hist(pts[:,3]),digest(pts.tobytes())),(k,side,'item closure'))
            for label,at in (('first_item',0),('last_item',-1)):
                wanted=dict(witness(b,pts[at,[0,2,3]]),item=int(pts[at,1])) if len(pts) else None; ck(a[label]==wanted,('item witness',label,k,side))
            ck(set(columns)==({q['lane'] for q in g['fields']} if len(pts) else set()),(k,side,'physical lane cover'))
            replay.append([b[p:p+w] for _,p,w in c])
            if pos==23:
                v=words(b,[p+5 for _,p,w in c if w==6],'<u1'); ck(g['single_item_percent_rewrite'][side]==
                    dict(single_item_rows=len(v),wire_values_not_100=int((v!=100).sum()),wire_histogram=hist(v)),'A percent rewrite control')
            if pos in (24,25) and len(pts):
                sel=np.stack([words(b,np.asarray(columns[str(p)])[:,1],'<u4') for p in (0,4,8,12,16)])
                ck(np.all(np.sum(sel!=0xffffffff,axis=0)==1),'exclusive selector witness')
            for f in g['fields']:
                lk=f['lane']; child=f['code']; scope=f['scoped_occurrence']; a=f['archives'][side]; cells=columns.get(lk,[])
                v=profile(b,cells,a,origin[side,'nation'])
                if child:
                    fs=next(r for r in master['entities']['nation.xml'][0]['fields'] if r['field']==parent)['list_item_fields']
                    one=[r for r in fs if r['field']==child]; ck(one==[scope['schema']] and fs[scope['index']]==one[0] and scope['field_codes_locations']==master['field_codes'][child]['locations'],'scoped child')
                    if pos in ABCD:
                        p=next(q for q in t28 if q.get('parent')==parent and q['code']==child)
                        ck(p['grade']=='L3' and (f['getter_chain'],f['reader_sites'],f['item_object_displacement'],int(lk))==(p['getter_chain'],p['reader_sites'],p['object_off'],p['item_offset']),('prior lane',k,child))
                        server_ids.add((f't75/nation/{parent}/{child}',f['prior_id']))
                    elif f['grade']=='held':
                        ck(f['prior_negative_verbatim']==(held_ftb if pos==4 else held_tax)[child] and f['first_counterexample'],'prior child held')
                    ck(all(t in code for t in f['getter_chain']+f['reader_sites']),'static child sites')
                if 'date' in a:datecheck(v,a['date']);ck(a['date']['invalid']==0,'calendar pass')
                if 'untyped_join_probes' in a:
                    for tid,q in a['untyped_join_probes'].items():reference(b,cells,v,ids[side,int(tid)],q)
                if 'reference' in a:
                    ref=a['reference']; tid=REF[scope['schema']['database_table_type']];ck(ref['table_id']==tid,'typed target');reference(b,cells,v,ids[side,tid],ref)
                    if pos in ABCD:ck(ref['ordinal_miss']==0,('existing ordinal lane failed',k,child))
                if 'scalar_domain' in a:
                    if pos==11: v=v.view('<'+held_tax[child]['format'])
                    live=v[v>0] if child=='fram' else v[v>=0] if child=='leve' else v; s=scope['schema']
                    ck(np.all(np.isfinite(live)) and np.all(live>=float(s.get('min_value','-inf'))) and np.all(live<=float(s.get('max_value','inf'))),'scalar range')
                    ck(a['scalar_domain']==dict(live=len(live),suppressed=len(v)-len(live),minimum=float(live.min()),maximum=float(live.max())),'scalar report')
                if 'utf8_codepoint_lengths' in a:
                    ck(a['utf8_codepoint_lengths']==hist([len(b[p:p+w].decode('utf8')) for _,p,w in cells]),'string lengths')
        if pos in ABCD:ck(len(replay[0])==g['cross_archive_equal_segments']==251 and replay[0]==replay[1],'full byte parity')
    r=delta['nation_existing_named_server_domain_reverified']; ck(len(r)==len(server_ids)==19 and {(f['id'],f['prior_id']) for f in r}==server_ids,'delta count')
    for f in r:
        g=next(t for t in groups if int(t['escalation']['slot'][5:])==f['slot']);o=next(p for p in g['fields'] if p['prior_id']==f['prior_id'])
        ck(f['server_domain']==o['archives']['server'] and f['grade']==o['grade']=='L3_reverified_server','delta exact link')
    print('t75 verify OK: 6 main members, 99 held trials, 10 escalation records, 19 prior lanes with server domains')


def selftest():
    b=bytes.fromhex('02000100000002000000'); pts,cols,n=split_items(b,[(3,0,10)],2)
    ck(pts.tolist()==[[3,0,2,4],[3,1,6,4]] and cols['0'].tolist()==[[3,2,4],[3,6,4]],'fixed segments')
    try:split_items(b,[(3,0,9)],2)
    except Check: pass
    else:raise Check('short frame accepted')
    pts,_,_=split_items((1).to_bytes(4,'little')+bytes(23),[(0,0,27)],11); ck(pts.tolist()==[[0,0,4,23]],'legacy short variant')
    print('t75 verify selftest OK')


def main():
    p=argparse.ArgumentParser(description=__doc__);m=p.add_mutually_exclusive_group();m.add_argument('--check',action='store_true');m.add_argument('--selftest',action='store_true');a=p.parse_args()
    try:
        if a.selftest:selftest()
        else:check()
        return 0
    except Check as e:print(f't75 VERIFY FAILED: {e}',file=sys.stderr);return 1
    except Exception as e:print(f't75 verify fatal: {type(e).__name__}: {e}',file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
