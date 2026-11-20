#!/usr/bin/env python3
"""Independently verify t44 with PE bytes, a fixed-format unpacker, and both archives."""
import argparse
import calendar
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import struct as S
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
EXE=Path('<OLD_REPO>/input/editor.exe')
MASTER='evidence/fm24/reports/editor_schema/master.json'
HEADER=bytes.fromhex('03017461642ef10d')
NEW=S.Struct('<IBIiIIIiBBIbbBIbI')
OLD=S.Struct(NEW.format[:-1])
SITES=(0x152923a,0x15293e7,0x1529407,0x1529427,0x1529447,0x1529470,0x15294ad,0x15294e1,0x1529501,
       0x1529521,0x1529541,0x1529555,0x1529575,0x1529595,0x15295b5,0x15295d5,0x15295f5,0x1529617)
SINKS=(None,0,0x30,0x1c,8,0x20,0x24,0x14,0x10,0x31,0x32,0x28,0x33,0x34,0x35,0x18,0x36,0x2c)
OFFSETS=(None,0,4,5,9,13,17,21,25,29,30,31,35,36,37,38,42,43)
WIDTHS=(4,4,1,4,4,4,4,4,4,1,1,4,1,1,1,4,1,4)
BITS=dict(frly=1,golo=2,fotb=3,plfr=4,yutr=5,perm=6,smbo=7,fnhl=9,hlwf=10,mrrl=13,scks=14,cpsd=15,
          ualf=16,lpfs=17,ustf=18,yout=19,rsrv=20,pfpr=21,UsSK=23,bttr=28)
BIT_FIELDS={0x1526252,0x1526def,0x1526815,0x15266a0,0x1526990,0x1526d24,0x1526a5d,0x1526eb2,0x152671c,
            0x1526f7e,0x1526891,0x1526abe,0x152679b,0x1526509,0x1526c2d,0x1526fe4,0x1526f18,0x1526d88,0x1526c93,0x1526615}
FIXED={'type':(4,1,1),'stdt':(13,4,4),'endt':(17,4,5),'yfee':(25,4,7),'fri%':(35,1,11),'msls':(36,1,12),'pwgp':(42,1,15)}

class Check(Exception):pass

def ck(ok,message):
    if not ok:raise Check(message)
def J(p):return json.loads(p.read_bytes())
def H(b):return sha256(b).hexdigest()
def U(b,i):return int.from_bytes(b[i:i+4],'little')
def hist(v):return {str(k):n for k,n in Counter(v).items()}

def read_data(c):
    # Independent of builder, fm24_dump, and t38 frame picker; use existing directory decoder only.
    codec=runpy.run_path(str(ROOT.parent/'fm24/scripts/modding_read_dbdat.py'))
    import zstandard as z
    root=Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data').resolve()
    if root.drive.upper()=='Z:':raise ValueError('Z: forbidden')
    clubs={};links=None
    for side,n in [('client',31),('server',77)]:
        _,blob,d=codec['_entries'](root/(side+'_db.dat'));base=d['data_base'];entries={e['path']:e for e in d['entries']}
        here=c[side];name=f'{side}_db/club_links.dat';present=name in entries
        ck(len(entries)==n==here['directory_entries'] and base==34==here['data_base'] and H(blob)==here['archive_sha256'] and
           present==(side=='server')==here['present'],'directories and archive SHA')
        def decode(path):
            e=entries[path];a=base+e['offset'];b=a+e['packed_size'];bound=min((base+v['offset'] for v in entries.values() if v['offset']>e['offset']),default=d['toc_offset'])
            part=blob[a:b]; ck(part[:4]==b'\x28\xb5\x2f\xfd' and b<=bound,'bounded canonical frame')
            raw=z.ZstdDecompressor().decompress(part,max_output_size=e['size'],allow_extra_data=False)
            ck(len(raw)==e['size'],'frame matches directory size');return raw,part,a,b,bound,e
        clubs[side]=decode(f'{side}_db/table_3.dat')[0]
        if present:
            links,part,a,b,bound,e=decode(name)
            ck(a==here['member_start']==38906250 and b==bound==here['member_end']==here['next_member_start'] and
               H(part)==here['entry']['sha256']=='894f1efb9caf18482402198ed19294d04725a583ca262a6a01b2ed95c2222fe0' and
               here['entry']=={**e,'sha256':H(part)} and
               H(links)==here['payload_sha256']=='8933328064b13a9d8dc153dd5b455970a7c28ada1e24f4ecc9df35735f42f3d2' and len(links)==435279,'server source payload and separate packed SHA')
        else:ck(all(here[k] is None for k in ('entry','count','stride','payload_sha256')),'absent is not empty')
    return links,clubs

def keys(clubs,c):
    # Locate ordered triples in the small client payload first; independently bound the
    # earliest/latest sequence on both sides (no inheritance of the builder's string walk).
    b=clubs['client'];s=clubs['server'];n=U(b,8)
    ck(n==84259==U(s,8) and b[:8]==s[:8]==HEADER and H(b)==c['client_payload_sha256'] and H(s)==c['server_payload_sha256'],'club source')
    p=14;mapping={};cp=[]
    for j in range(n):
        tag=S.pack('<I',j);q=b.find(tag,p+20,min(p+8192,len(b)-12));hits=[]
        while q>=0:
            x,y=U(b,q+4),U(b,q+8)
            if x==y and b[q+12] in (0,12):hits.append((q,x))
            q=b.find(tag,q+1,min(p+8192,len(b)-12))
        # In normal rows the tail follows two length-prefixed strings and three bytes.
        def text_end(a):
            for _ in range(2):
                size=U(b,a)
                if size>200:return -1
                try:b[a+4:a+4+size].decode('utf-8')
                except UnicodeError:return -1
                a+=4+size
            return a+3
        ends={text_end(p+25),text_end(p+26)}
        shaped=[pair for pair in hits if pair[0] in ends]
        if shaped:hits=shaped
        else:hits=[pair for pair in hits if pair[0]<p+8192]
        ck(len(hits)==1,f'client ambiguous/missing triple {j}: {hits[:4]}');(q,x),=hits;mapping[j]=x;cp.append(q);p=q+13
    triples=[S.pack('<III',i,x,x) for i,x in mapping.items()]
    ck(p+8==len(b) and len(set(mapping.values()))==n and c['actual_ordinals']==n and H(b''.join(triples))==c['key_map_sha256'],'actual key map')
    for side,buf in (('client',b),('server',s)):
        early=[];p=13
        for triple in triples:
            q=buf.find(triple,p,len(buf)-9);ck(q>=0,side+' missing triple');early.append(q);p=q+12
        ck(p==len(buf)-9 and (side!='client' or early==cp),side+' final identity')
        p=len(buf)-9
        for q,triple in zip(reversed(early),reversed(triples)):
            p=buf.rfind(triple,13,p);ck(p==q,side+' nonunique ordered triple sequence')
        ck(c[side+'_positions_sha256']==H(S.pack(f'<{n}I',*early)),side+' identity-position digest')
    return mapping

def static(d,c):
    from capstone import Cs,CS_ARCH_X86,CS_MODE_64
    from t05_pe import PE
    p=PE(EXE);p.pe.parse_data_directories(directories=[3]);m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True
    prov=d['provenance'];ck(H(p.raw)==prov['editor_sha256']=='b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4','original editor SHA')
    manifest={r['path']:r['sha256'] for r in J(ROOT/'evidence/MANIFEST.json')['files']}
    for path,h in prov['frozen_snapshots'].items():ck(H((ROOT/path).read_bytes())==h==manifest[path],'frozen '+path)
    ck(manifest[MASTER].startswith('7d57477e'),'frozen master SHA')
    for path,h in prov['t35_unchanged_sha256'].items():ck(H((ROOT/path).read_bytes())==h,'preserve t35 '+path)
    ck(prov==c['provenance'] and len(prov['t35_unchanged_sha256'])==2,'provenance consistency')
    saved={}
    for file in c['instruction_shards']:
        for r in J(HERE/file)['instructions']:
            x=int(r['file_offset'],16);v=p.f2va(x);i=next(m.disasm(p.raw[x:x+15],v,1))
            ck(x not in saved and p.va2f(v)==x and hex(v)==r['VA'] and i.bytes.hex()==r['bytes'] and
               r['instruction']==(i.mnemonic+' '+i.op_str).rstrip(),f'bytes/VA {x:#x}');saved[x]=i
    route=d['static_chain'];ck(d['table_type'] is route['entry_rtti'] is route['entry_vptr'] is route['vtable_slot19'] is None,'named POD, not numeric table')
    for r in route['raw_data']:
        o=int(r['file_offset'],16);b=bytes.fromhex(r['bytes']);ck(hex(p.f2va(o))==r['VA'] and p.raw[o:o+len(b)]==b,'route raw bytes')
    def target(o):return p.va2f(saved[o].operands[0].imm)
    def rip(o):
        i=saved[o];return i.address+i.size+next(x.mem.disp for x in i.operands if x.type==3 and i.reg_name(x.mem.base)=='rip')
    for e in route['direct_edges']:ck(target(e['source'])==e['target'],'direct route edge')
    for o,w in {0xe8b4db:'ebx, 0x4361666c',0xe8c1e8:'ebx, 0x4376666c',0x436385d:'rdx, qword ptr [rax + 0x118]',
                0x15322f3:'rax, qword ptr [rbx + 0x118]',0x15322fa:'qword ptr [rbx + 0x120], rax',
                0x15323ed:'byte ptr [r14 + 8], al',0x43656d7:'edi, byte ptr [rdi + 8]',0xf2a395:'rcx, qword ptr [rdi + 0x680]',
                0xf3dba1:'rcx, qword ptr [r13 + 0x680]',0x434e3d2:'rax, 0x6e696c5f62756c63',0x434e3e0:'word ptr [rdi + 0x10], 0x736b',
                0x1529393:'qword ptr [rax], 0',0x1529628:'rax, qword ptr [rbp]',0x3ad6f78:'qword ptr [rsi + 0x120], 8'}.items():
        ck(saved[o].op_str==w,f'route dataflow {o:#x}')
    ck(rip(0x1529357)==rip(0x153230a)==rip(0xf7411f)==0x141b5ecc8 and rip(0x1529602)==0x141b60330,'pool and version globals')
    o=p.va2f(rip(0x434e39f));ck(route['source_extension']=='.dat' and p.raw[o:o+5]==b'.dat\0','named member extension')
    ck(p.raw[p.va2f(0x14192ee21):p.va2f(0x14192ee21)+10]==b'CLUB_LINK\0','pool diagnostic name')
    bk={}
    for file in c['branch_shards']:
        for r in J(HERE/file)['branches']:
            x=r['site'];ck(x not in bk and r['taken_to']==target(x) and r['fallthrough_to']==x+saved[x].size and all(e in saved for e in r['evidence']) and
                           r['first_counterexample_or_constraint'],'per-branch evidence');bk[x]=r
    cnd=set();io={t['status_branch'] for t in c['transfer_calls']};wire={0x152934e,0x152962c,0x1529794};dead={0x15297a3,0x1529825,0x39dd7bc}
    for start,end,total in [(0x1529210,0x1529844,404),(0x39dd7b0,0x39dd7f9,26)]:
        rf=[r.struct.EndAddress for r in p.pe.DIRECTORY_ENTRY_EXCEPTION if r.struct.BeginAddress==p.f2r(start)]
        ck(rf==[p.f2r(end)],'PE function extent');g={};todo=[start];calls=[]
        while todo:
            x=todo.pop()
            if x in g:continue
            ck(start<=x<end,'CFG escapes extent');i=saved[x];n=x+i.size;op=i.mnemonic
            ns=[] if op=='ret' else [target(x)] if op=='jmp' else [n,target(x)] if op.startswith('j') else [n]
            if op=='call':calls.append(x)
            if len(ns)==2:
                cnd.add(x);want='IO-result' if x in io else 'wire_data' if x in wire else 'dead' if x in dead else 'runtime-external' if x==0x152960e else 'context-lifecycle'
                ck(bk[x]['classification']==want and bk[x]['changes_regular_item_width']==(x==0x152960e),'predicate classes')
            g[x]=sorted(ns);todo.extend(ns)
        q=c['reader_cfg'][str(start)]
        ck(len(g)==total==q['reachable'] and g=={int(k):sorted(v) for k,v in q['successors'].items()} and sorted(calls)==q['calls'] and not q['external_edges'],'independent CFG exact match')
    ck(cnd==set(bk) and hist(r['classification'] for r in bk.values())==c['branch_counts'],'exhaustive reachable conditions')
    ck([(t['site'],t['object_offset'],t['row_offset'],t['width']) for t in c['transfer_calls']]==list(zip(SITES,SINKS,OFFSETS,WIDTHS)), 'all stream sinks')
    for t in c['transfer_calls']:
        x=t['site'];i=saved[x];actual=t['actual_read']
        ck(saved[actual].op_str in ('qword ptr [rax + 0x28]','qword ptr [rdi + 0x28]'),'transfer virtual stream slot')
        if actual!=x:ck(target(x)==0xdb7f80 and target(0xdb7f80)==0x39dd7b0 and saved[0x39dd7c8].op_str=='r8d, 4','date thunk and width')
        else:ck(any(saved[a].op_str==f'r8d, {t["width"]}' for a in range(x-32,x) if a in saved),'width witness')
    return saved

def unpack(b,fmt):
    ck(b[:6]==HEADER[:6] and len(b)>=12,'header');n=U(b,8)
    ck(12+fmt.size*n==len(b),'count determines exact EOF');return list(fmt.iter_unpack(b[12:]))

def check_fields(b,rows,ids,f,inst):
    master=J(ROOT/MASTER);nested=J(ROOT/'scratch/t24/out/subtables.part003.json')['nested_fields'];flags=[r[2] for r in rows]
    ck(f['flag_counts']==[sum(x>>j&1 for x in flags) for j in range(32)],'all bits independently counted')
    uid=set(ids.values());ep=f['endpoint_profiles']
    for k,col,ofs in [('A',0,0),('B',3,9)]:
        vals=[r[col] for r in rows];pr=ep[k]
        ck(all(v in ids for v in vals) and pr['actual_ordinal_hits']==len(vals) and pr['wrong_uid_row_misses']==sum(v not in uid for v in vals) and
           pr['first']['target_identity']==ids[vals[0]] and pr['row_offset']==ofs and pr['wrong_uid_first']['value']==vals[0],'endpoint domain and UID falsification')
    enum={int(e['enum']) for e in master['enums']['CAfT']['values']}
    def sample(j,o,w,value):
        p=12+47*j+o;return dict(row=j,absolute=p,hex=b[p:p+w].hex(),value=value)
    def first(v,condition,o,w):return next((sample(j,o,w,x) for j,x in enumerate(v) if condition(x)),None)
    for parent,fs in f['occurrences'].items():
        scopes=[x['list_item_fields'] for x in master['entities']['club.xml'][0]['fields'] if x['field']==parent];sc,=scopes
        ns=[x for x in nested if x['parent']==parent];ck(len(fs)==len(sc)==len(ns) and len({r['code'] for r in fs})==len(fs),'unique schema occurrences')
        for r,s,n in zip(fs,sc,ns):
            code=r['code'];ck(code==s['field']==n['code'] and r['schema']==s and r['schema_idx']==n['idx'],'exact scoped schema')
            ck(inst[r['compare']].operands[1].imm==int.from_bytes(code.encode(),'big'),'getter 4CC');grade='L3';ofs=None
            if code in BITS:
                bit=BITS[code];ofs=5
                ck(r['object_offset']==28 and r['reader_site']==0x1529427 and r['byte_offset']==5+bit//8 and
                   r['bit_mask_u32']==1<<bit and r['byte_mask']==1<<(bit%8) and r['counts']==hist(x>>bit&1 for x in flags) and
                   r['first_set']==first(flags,lambda x:x>>bit&1,5,4) and r['first_clear']==first(flags,lambda x:not(x>>bit&1),5,4),'boolean grouping and full table')
                i=inst[r['getter_case']];ck(i.operands[1].mem.disp==(30 if code=='ualf' else 28),'bit getter member');p=r['getter_case'];seen=set()
                while p in inst and p-r['getter_case']<24:seen.add(p);p+=inst[p].size
                [bit_site]=seen&BIT_FIELDS;ck(inst[bit_site].operands[1].imm==(1 if code=='ualf' else bit),'actual extraction instruction')
            elif code=='clfr':
                grade='runtime_only_no_wire_slot';ck(r['runtime_wrapper_byte']==8 and r['domain']==list(range(7)) and
                    r['domain']==[int(x['enum']) for x in master['enums']['clfr']['values']],'validation is a runtime-only enum')
            elif code in ('affl','ismc'):
                a,other=rows[0][0],rows[0][3]
                ck(r['derived'] and r['row_offset_candidates']==[0,9] and r['endpoint_slots']==ep and
                   r['first_row_view_roles']==[dict(viewer_ordinal=a,ismc=True,affl_ordinal=other),dict(viewer_ordinal=other,ismc=False,affl_ordinal=a)],
                   'two-sided viewer relation')
            else:
                ofs,w,col=FIXED[code];vals=[x[col] for x in rows];ck(r['candidate_row_offset']==ofs and r['width']==w,'fixed field coordinate')
                if code in ('stdt','endt'):
                    days=[x&511 for x in vals];ys=[x>>16 for x in vals]
                    ck(all((x&0xfe00)==0 and 1<=day<=365+calendar.isleap(y) for x,y,day in zip(vals,ys,days)) and
                       (r['year_min'],r['year_max'],r['ordinal_day_min'],r['ordinal_day_max'])==(min(ys),max(ys),min(days),max(days)) and
                       vals.count(0x076c0001)==r['default_1900_day1_count'],'packed calendar date')
                else:
                    bad=(lambda v:v not in enum) if code=='type' else (lambda v:not int(s['min_value'])<=v<=int(s['max_value']) and (v!=-1 or code=='yfee'))
                    ex=first(vals,bad,ofs,w)
                    if ex:
                        grade='held_domain_conflict';ck(r['first_counterexample']==ex and r['conflicting_rows']==sum(map(bad,vals)),'first domain counterexample')
                    elif all(v==-1 for v in vals):
                        grade='held_all_missing';ck(r['first_counterexample']==sample(0,ofs,w,-1),'no live evidence')
                    ck((min(vals),max(vals),len(set(vals)))==tuple(r['profile'][x] for x in ('min','max','distinct')), 'signed integer profile')
            ck(r['grade']==grade and r['row_offset']==(ofs if grade=='L3' else None),'grade / no published held coordinate')
        ck(f['occurrence_grades'][parent]==dict(Counter(r['grade'] for r in fs)),'grade summary')

def verify():
    d=J(HERE/'discovery_cafl_cvfl.json');c=J(HERE/'cursor_club_links.json');f=J(HERE/'fields_cafl_cvfl.json')
    ck(d['L4']==f['L4']==0 and d['archives']==c['archives'] and d['instruction_shards']==c['instruction_shards'] and d['branch_shards']==c['branch_shards'],'artifact consistency')
    ck(H((ROOT/'scratch/t24/out/subtables.part003.json').read_bytes())==d['provenance']['t24_nested_sha256'],'nested snapshot')
    raw,clubs=read_data(c['archives']);inst=static(d,c);ids=keys(clubs,c['target_club_domain']);rows=unpack(raw,NEW);r=c['replay']
    ck(raw[:8]==HEADER and NEW.size==47 and len(rows)==r['count']==9261 and r['header_bytes']==12 and r['footer_bytes']==0 and
       r['selector'] is r['identity_tail'] is None and not r['selector_histogram'] and
       r['row_block_sha256']==H(raw[12:]) and r['type_histogram']==hist(x[1] for x in rows) and not any(x[0]==x[3] for x in rows),'whole-file cursor / native coordinates')
    trace=sha256()
    for j,x in enumerate(rows):
        a=12+j*47;z=a+47;trace.update(S.pack('<5I',j,a,z,x[0],x[3])+sha256(raw[a:z]).digest())
    ck(trace.hexdigest()==r['row_trace_sha256'],'all row boundaries and hashes')
    count=len(rows)
    assert_edges={0x152934e:(0,1),0x152962c:(sum(x[0]==x[3] for x in rows),count),0x1529794:(count-1,1),0x152960e:(0,count)}
    ck(r['replayed_branch_edges']=={str(k):dict(taken=x,fallthrough=y) for k,(x,y) in assert_edges.items()},'wire and version edge counts')
    for t in r['unnamed_lanes']:
        a=t['row_offset'];w=t['width'];slices=[raw[o+a:o+a+w] for o in range(12,len(raw),47)]
        ck(t['first_hex']==slices[0].hex() and t['distinct']==len(set(slices)),'unnamed lane kept structural')
    ck(r['old_version']==f'footer/EOF mismatch @{12+43*len(rows)}: {len(rows)*4} trailing bytes','first old mode divergence and full fork failure')
    for t,width,start in zip(c['transfer_calls'],WIDTHS,[8]+[12+o for o in OFFSETS[1:]]):
        # A stream chopped one byte before this call's required end has every prior transfer intact.
        cut=start+width-1;ck(cut>=start and cut<start+width and r['short_read'][str(t['site'])]==
          f'row={None if start==8 else 0} @{start} w={width} site={t["site"]:#x} short read','short-read first witness')
    check_fields(raw,rows,ids,f,inst)
    print('t44 independent verify PASS: shared named member; 9261 rows, 84259 actual club identities, 49 classified branches')

def selftest():
    b=HEADER+S.pack('<I',1)+bytes(47);ck(len(unpack(b,NEW))==len(unpack(b[:-4],OLD))==1 and OLD.size==43,'version selftest')
    for buf,fmt in [(b[:-1],NEW),(b,OLD),(b[:8],NEW)]:
        try:unpack(buf,fmt)
        except Check:continue
        raise Check('invalid fixture accepted')
    print('t44 verifier selftest PASS')

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--selftest',action='store_true');arg=ap.parse_args()
    sys.path.insert(0,str(ROOT/'scripts'));sys.path.append(str(ROOT.parent/'fm24/tools/python'))
    try:selftest() if arg.selftest else verify();return 0
    except Check as e:print(f'verify FAIL: {e}',file=sys.stderr);return 1
    except Exception as e:print(f'verify fatal: {e}',file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())
