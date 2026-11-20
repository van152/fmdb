"""Independently verify t61 scope, enum membership, all raw histograms, and grades."""
import argparse
from collections import Counter, defaultdict
from functools import cache
from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
import runpy
import struct
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
BASE = 'reports/club_nation_subtable_schema.json'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
FROZEN = '7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda'
MAIN = {'nation':(55,10,251), 'club':(57,3,84259), 'comp':(59,25,7047)}
SIDES = 'client','server'
LEDGER_GUARDS = {
    'E94': {'id':'E94','kind':'acceptance','level':'L3','claim_sha256':'358243779bba359656ecae6804cea9cea26b1739ffce5bf96a2599d735263c89'},
    'E97': {'id':'E97','kind':'acceptance','level':'L3','claim_sha256':'ba5a1079403dd970b30c9304a90c37d5a66f3d28163ee2cf2588fd355129ff32'},
    'E98': {'id':'E98','kind':'acceptance','level':'L3','claim_sha256':'57a2384c170c3effc159a98012b866ab174849da8849269abc118b8e7fe4f150'},
    'E99': {'id':'E99','kind':'acceptance','level':'L3','claim_sha256':'e13990af22d739ba1f6a61e9adc2211febb051821845a48358e30306d452b16b'},
}


class Fail(Exception):
    pass


def ck(ok, message):
    if not ok:
        raise Fail(message)


def digest(b):
    return sha256(b).hexdigest()


def canonical_sha(value):
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8'))


@cache
def read(p):
    return json.loads((ROOT/p).read_bytes())


def path(task, name):
    return f'scratch/t{task}/out/{name}'


def table(t):
    return f'table_{t}.dat'


@cache
def adapter(task):
    # Only accepted independent data-side replay functions are invoked, never
    # their PE checks / target joins / CLIs. No t61 or other builder import.
    return runpy.run_path(str(ROOT/path(task,'verify.py')))


def decode_archives(wanted, refs):
    depot = Path(os.environ.get('FM24_DB_DIR',ROOT/'scratch/data'))
    if depot.drive.upper()=='Z:' or depot.resolve().drive.upper()=='Z:':
        raise ValueError('Z: forbidden')
    sys.path.append(str(ROOT.parent/'fm24/tools/python'))
    import zstandard
    fm = bytes.fromhex('0201666d662e080000')

    def frame(data):
        ck(data.startswith(b'\x28\xb5\x2f\xfd'),'Zstd signature')
        z=zstandard.ZstdDecompressor().decompressobj(); out=z.decompress(data)
        ck(z.eof and len(z.unused_data)<len(data),'bounded EOF')
        return out,z.unused_data

    raw={}; meta={}
    for side,size in zip(SIDES,(31,77)):
        blob=(depot/f'{side}_db.dat').read_bytes(); checksum=digest(blob)
        ck(all(r==checksum for r in refs[side]),(side,'accepted archive SHA'))
        toc,base=(17+v for v in struct.unpack_from('<QQ',blob,17))
        ck(17<base<toc<len(blob) and blob[8:17]==blob[toc:toc+9]==fm,'FMF anchors')
        toc_bytes,rest=frame(blob[toc+9:]); ck(not rest,'TOC EOF')
        p=0; entries={}

        def get(n):
            nonlocal p
            ck(0<=n<=len(toc_bytes)-p,'TOC bounds'); p+=n
            return toc_bytes[p-n:p]

        def u():
            return int.from_bytes(get(4),'little')

        def text():
            return get(u()).decode('utf-8')

        def folder(parent,level):
            ck(level<40,'TOC depth'); current=parent/text()
            for _ in range(u()):
                f=current/(text()+text()); a,c,n,_,_=struct.unpack('<5Q',get(40))
                ck('..' not in f.parts and not f.is_absolute() and f.as_posix() not in entries,'TOC path')
                entries[f.as_posix()]=(base+a,c,n)
            for _ in range(u()):
                folder(current,level+1)

        folder(PurePosixPath(),0); ck(p==len(toc_bytes) and len(entries)==size,'TOC census')
        members={}
        for name in wanted:
            ent=entries.get(f'{side}_db/{name}')
            members[name]=None
            if ent is None:
                continue
            a,w,n=ent; b=a+w; next_at=min((v[0] for v in entries.values() if v[0]>a),default=toc)
            ck(base<=a<b<=next_at<=toc,('member limit',side,name))
            remainder=blob[a:b]; hits=[]
            while remainder:
                buf,remainder=frame(remainder)
                if len(buf)==n:
                    hits.append(buf)
            ck(len(hits)==1,('unique size-selected frame',side,name)); payload,=hits
            raw[side,name]=payload
            members[name]=dict(payload_sha256=digest(payload),bytes=n,header_rows=struct.unpack_from('<I',payload,8)[0])
        meta[side]=dict(archive_sha256=checksum,members=members)
    return raw,meta


def definitions(root, maps):
    """Start from accepted membership, not from the t61 occurrence list."""
    defs={}
    for e,(t,_,_) in MAIN.items():
        p=path(t,'field_map.json')
        for i,f in enumerate(maps[e]['fields']):
            grade=f.get('grade',f.get('status'))
            if grade in {'held','linked_parent_held'}:
                layer='main_other' if e=='nation' and grade!='held' or e=='nation' and f['slot'] is None else 'main'
                defs[p,f'/fields/{i}']=(e,layer,f,None)
    defs[path(55,'field_map.json'),'/supplemental/Npop']=('nation','main_other',maps['nation']['supplemental']['Npop'],None)
    for ti,tab in enumerate(root['tables']):
        for i,f in enumerate(tab['held_fields']):
            shared=tab['parent_code']=='Tchl'
            defs[BASE,f'/tables/{ti}/held_fields/{i}']=('club','shared_subtable' if shared else 'subtable',f,tab['parent_code'])
    for ti,aux in enumerate(root['club_auxiliary_sources']):
        for vi,view in enumerate(aux['views']):
            for i,f in enumerate(view['occurrences']):
                if f['grade'].startswith('held'):
                    defs[BASE,f'/club_auxiliary_sources/{ti}/views/{vi}/occurrences/{i}']=('club','auxiliary',f,view['view'])
    for i,f in enumerate(root['nation_static_side']['Ntxr']['fields']):
        if f['grade']=='held':
            defs[BASE,f'/nation_static_side/Ntxr/fields/{i}']=('nation','subtable',f,'Ntxr')
    t9=root['nation_t9_wire']
    for par,d in t9['table_9']['parents'].items():
        for i,f in enumerate(d['fields']):
            if f['grade']=='held':
                defs[BASE,f'/nation_t9_wire/table_9/parents/{par}/fields/{i}']=('nation','subtable',f,par)
    for par,d in root['nation_static_side']['t51_followup']['field_ledgers'].items():
        for code,f in d['fields'].items():
            if f['status']=='held':
                defs[BASE,f'/nation_static_side/t51_followup/field_ledgers/{par}/fields/{code}']=('nation','subtable',dict(f,code=code),par)
    for code,d in t9['t53_crs_adjudication']['field_dispositions'].items():
        ck(d['grade']=='held','TCrs ledger grade')
        defs[BASE,f'/nation_t9_wire/t53_crs_adjudication/field_dispositions/{code}']=('nation','subtable',dict(d,code=code,schema=d['source_record_verbatim']['schema']),'TCrs')
    return defs


def enum_table(master, schema):
    key=schema.get('enum_ref'); doc=master['enums'].get(key)
    if not doc or not doc['values']:
        return key,None,None
    source=dict(master=MASTER,key=key,file=doc['file'])
    values=[{'value':int(v['enum']) if v['enum'].lstrip('+-').isdecimal() else v['enum'],
             'label':v['name'],'enum_id':v.get('enum_id')} for v in doc['values']]
    return key,source,values


def xml_loc(master,e,par,source):
    fields=master['entities'][e+'.xml'][0]['fields']
    code=source.get('code','Npop'); schema=source.get('schema')
    if schema is None:
        ck(code=='Npop' and not any(f['field']==code for f in fields),'out-of-schema exception')
        return [None,None],None,None,None
    clean={k:v for k,v in schema.items() if k!='idx'}
    if par is None:
        i=source['xml_index']; j=None
        ck(fields[i]==clean and clean['field']==code,('main occurrence',e,i,code))
        label=f'{e}.xml#{e}/fields[{i}]/{code}'
    else:
        [(i,parent)]=[(i,p) for i,p in enumerate(fields) if p['field']==par]
        [j]=[j for j,v in enumerate(parent['list_item_fields']) if v==clean and v['field']==code]
        label=f'{e}.xml#{e}/fields[{i}]/{par}/list_item_fields[{j}]/{code}'
    alias=None
    if par=='Tchl':
        s={'schema':clean,'code':code}; _,alias,_,_=xml_loc_single_nation(master,s)
    return [i,j],label,alias,clean


def xml_loc_single_nation(master,source):
    fs=master['entities']['nation.xml'][0]['fields']
    [(i,p)]=[(i,p) for i,p in enumerate(fs) if p['field']=='Tchl']
    [j]=[j for j,f in enumerate(p['list_item_fields']) if f==source['schema']]
    return [i,j],f'nation.xml#nation/fields[{i}]/Tchl/list_item_fields[{j}]/{source["code"]}',None,source['schema']


class Replay:
    def __init__(self, raw, meta, base, slots):
        self.raw=raw; self.meta=meta; self.base=base; self.slots=slots

    @cache
    def main_columns(self,e,side):
        t,tid,n=MAIN[e]; b=self.raw[side,table(tid)]; mode=side=='server'; mod=adapter(t)
        saved=self.slots[e].get('archives',self.slots[e].get('archive'))[side]['members'][str(tid)]
        ck(digest(b)==saved['payload_sha256'] and struct.unpack_from('<I',b,8)[0]==n,('main identity',e,side))
        try:
            if e=='nation':
                rr,_=mod['read_rows'](b,mode); cols=defaultdict(list)
                for i,(_,_,_,row) in enumerate(rr):
                    for k,(at,w,cnt) in row.items():
                        cols[k].append((i,at,w,cnt))
            elif e=='club':
                vals,rr,*_=mod['table3'](b,mode); cols=dict(enumerate(vals))
            else:
                rr,cols,_=mod['replay'](b,mode)
        except mod.get('Check',mod.get('Failed')) as err:
            raise Fail(err) from err
        ck(len(rr)==n,('coverage',e,side)); return cols

    @cache
    def cursor(self, side, name, p):
        doc=read(p); b=self.raw[side,name]; rows=doc['rows']; at=13
        ck(doc['payload_sha256']==digest(b) and len(rows)==251,'accepted cursor SHA/count')
        for i,r in enumerate(rows):
            end=r['end']; ck(r['row']==i and r['wire13']==at and b[at]==0 and end>at+12,'accepted native row')
            ck(digest(b[at:end])==r['wire_sha256'] and list(struct.unpack_from('<III',b,end-12))==r['identity'] and r['identity'][0]==i,'accepted row hash/identity')
            at=end
        ck(at+9==len(b) and b[at:at+5]==b'\0\0\0\0\1','accepted cursor EOF')
        return rows

    @cache
    def tc_rows(self, side, name):
        b=self.raw[side,name]; mod=adapter(53)
        return mod['main_member'](b,side) if name==table(9) else mod['aux'](b,side=='server')

    def make(self, side, e, layer, f, parent):
        """Yield independent groups and cell spans without consuming t61 coordinates."""
        code=f.get('code','Npop'); fmt=None; names=[]; status='not_bound'; cells=(); n=None
        if layer.startswith('main'):
            _,tid,n=MAIN[e]; names=[table(tid)]
            pos=f.get('candidate_position',f.get('slot',f.get('position')))
            if pos is not None:
                fmt=({'Necf':'i8','Nygn':'i8','Ngct':'i8','Nsod':'i8','Nftb':'i16','Npop':'i32'} if e=='nation' else
                     {'Cnam':'utf8_length','Csnm':'utf8_length','PLgn':'i8','Cprs':'i8'} if e=='club' else
                     {'dbty':'i8','rdui':'u32','CTty':'u8','PLgn':'u8','CpRp':'u8'}).get(code)
                if fmt:
                    book=self.main_columns(e,side); src=book.get(pos,[]); b=self.raw[side,names[0]]; lane=f.get('lane') or 0
                    if fmt=='utf8_length':
                        cells=[(r,None,a+4,struct.unpack_from('<I',b,a)[0]) for r,a,_ in book[pos-1]]
                        ck([(r,a,w) for r,_,a,w in cells if w]==src,'text and length columns')
                    else:
                        w=int(fmt[1:])//8; ck(all(s>=w+lane for _,_,s,*_ in src),'field fits span')
                        cells=[(r,None,a+lane,w) for r,a,_,*_ in src]
                    ck(len(cells) in (0,n),'full main coverage')
                    status='scanned' if cells else 'mode_bypass'
        elif e=='club':
            if layer=='auxiliary':
                names=['club_links.dat']; doc=self.base['club_auxiliary_sources'][0]['server_payload']
                coord=f['candidate_coordinate']; off=coord['wire_offset']; w=coord['width_bytes']; start=12; stride=47; footer=0
                fmt=f'i{w*8}'
            else:
                tab=next(x for x in self.base['tables'] if x['parent_code']==parent); names=[table(tab['table_type'])]
                doc=tab['server_payload' if side=='server' else 'client_observation']; start=13; footer=9; stride=doc.get('stride_bytes')
                if f['coordinates']:
                    c,=f['coordinates']; off=c['wire_offset']; w=c['width_bytes']; fmt=('u' if parent in ('Tchl','CNtp') else 'i')+str(w*8)
            b=self.raw.get((side,names[0])); status='member_absent' if b is None else status
            if b is not None:
                ck(digest(b)==doc['payload_sha256'],'accepted subtable payload'); n=doc['row_count']
                if side=='client':
                    status='mode_bypass'; ck(start+stride*n+footer==len(b),'client identity only')
                elif parent=='Csme':
                    fmt='pair_i32'; p=13; cells=[]; status='scanned'
                    for i in range(n):
                        num=struct.unpack_from('<I',b,p+6)[0]; content=p+10; ip=content+10*num
                        ck(struct.unpack_from('<III',b,ip)[0]==i,'Csme identity')
                        cells.extend((i,j,content+10*j+1,8) for j in range(num)); p=ip+12
                    ck(p+9==len(b),'Csme EOF')
                elif fmt:
                    ck(start+n*stride+footer==len(b) and off+w<=stride,'fixed rows')
                    cells=[(i,None,a+off,w) for i,a in enumerate(range(start,len(b)-footer,stride))]; status='scanned'
            else:
                fmt=None
                if layer!='auxiliary':
                    ck(not doc['present'],'directory absence')
        elif parent=='TCrs':
            for name in (table(9),table('extra_9')):
                if code=='PUnP':
                    yield name,'person_boundary',251,None,()
                    continue
                width,fmt={'PUnI':(1,'u8'),'PUnT':(1,'i8'),'PUnJ':(2,'u16')}[code]
                delta=f['source_record_verbatim']['gates']['item_offset_at_tag3']; rows=self.tc_rows(side,name)
                ck(len(rows)==251,'TCrs rows'); cells=[]
                for r in rows:
                    if v:=r['vector']:
                        for item in v['items']:
                            ck(item['tag']==3 and item['end']-item['absolute']==12 and delta+width<=12,'TCrs observed branch'); cells.append((r['row'],item['item'],item['absolute']+delta,width))
                yield name,'scanned' if side=='server' else 'mode_bypass',251,fmt,cells
            return
        elif parent=='Ntxr':
            names=[table(10)]; n=251; fmt='i8'; b=self.raw[side,names[0]]; off=f['source_record']['static_item_offset']
            d=read(path(47,'cursor_nation_tax.json'))[side]; cells=[]
            for item in d['tax_items']:
                a=item['absolute']; ck(b[a:a+25].hex()==item['hex'] and b[a]==2 and item['length']==25,'tax source coordinates')
                cells.append((item['row'],item['item'],a+off,1))
            ck(len(cells)==(1899 if side=='server' else 0),'tax census'); status='scanned' if cells else 'mode_bypass'
        elif parent=='Nftb':
            names=[table(10)]; n=251
            if code!='NbPi':
                c={'NbPn':12,'NbFt':8}[code]; rows=self.cursor(side,names[0],path(51,f'cursor_table_10_{side}.json'))
                fmt='i32'; cells=[(r['row'],i,item['end']-c,4) for r in rows if r['Nftb'] for i,item in enumerate(r['Nftb']['items'])]
                ck(len(cells)==(7 if side=='server' else 0),'Nftb count'); status='scanned' if cells else 'mode_bypass'
        else:
            names=[table(9)]; n=251; b=self.raw[side,names[0]]; cells=[]
            if parent=='Calt':
                rows=self.cursor(side,names[0],path(51,f'cursor_table_9_{side}.json'))
                ck(all(r['Calt'] is None if side=='client' else struct.unpack_from('<h',b,r['Calt']['count_at'])[0]==0 for r in rows),'Calt empty')
                status='no_items' if side=='server' else 'mode_bypass'
            elif f['static_item_offset'] is not None:
                offsets=self.cursor(side,names[0],path(49,f'cursor_t9_{side}.json'))
                enc=f['encoding']; w=f['width_bytes']; fmt=('u' if enc=='B' else 'i')+str(w*8); off=f['static_item_offset']
                step={'Nntp':9,'Nctp':8,'Nrtp':8,'Nfmp':9,'NCro':9}[parent]
                for r in offsets:
                    if (c:=r['collections'].get(parent)) is None:
                        continue
                    if c.get('gate') and c['count'] is None:
                        ck(b[c['gate'][0]]==c['gate'][1]==0,'NCro presence gate'); continue
                    a=c['start']; ck(c['end']-a==step*c['count'] and int.from_bytes(b[c['count_at']:a],'little')==c['count'],'t9 count/stride')
                    cells.extend((r['row'],j,a+j*step+off,w) for j in range(c['count']))
                status='scanned' if cells else 'mode_bypass' if side=='client' and parent in ('Nfmp','NCro') else 'no_items'
        name,=names
        if f.get('schema',{}).get('database_table_type')=='person':
            status='person_boundary'
        if n is None:
            d=self.meta[side]['members'].get(name); n=0 if d is None else d['header_rows']
        yield name,status,n,fmt,cells

    def check_profile(self, side, independent, result, schema, allowed):
        member,status,rows,fmt,cells=independent
        ck((member,status,rows,fmt)==tuple(result[k] for k in ('member','status','rows','encoding')),(side,member,'profile metadata',independent[:4]))
        fmt_map={'u8':'B','i8':'b','u16':'H','i16':'h','u32':'I','i32':'i','pair_i32':'ii'}
        payload=self.raw.get((side,member)); counts=Counter(); firsts={}; first=None
        for r,j,a,w in cells:
            raw=payload[a:a+w]; ck(len(raw)==w,'short lane')
            if fmt=='utf8_length':
                val=len(raw.decode())
            else:
                vals=struct.unpack('<'+fmt_map[fmt],raw)
                val=f'{vals[0]},{vals[1]}' if len(vals)==2 else vals[0]
            if val not in counts:
                wit=dict(row=r,item=j,absolute=a,raw=raw.hex(),value=val)
                firsts[val]=wit
                if first is None:
                    first=wit
            counts[val]+=1
        misses=Counter({k:v for k,v in counts.items() if allowed is not None and k not in allowed})
        bad=[k for k in counts if isinstance(k,int) and (
            ('min_value' in schema and k<int(schema['min_value'])) or ('max_value' in schema and k>int(schema['max_value'])) or
            (fmt=='utf8_length' and 'max_length' in schema and k>int(schema['max_length'])))]
        hist=lambda c: {str(k):v for k,v in c.items()}
        expected=dict(tested=len(cells),histogram=hist(counts),first_value=first,out_of_enum=hist(misses),
                      enum_misses=None if allowed is None or status=='not_bound' else misses.total(),
                      first_enum_counterexample=firsts[next(iter(misses))] if misses else None,
                      frozen_bound_violations=sum(counts[k] for k in bad),first_frozen_bound_counterexample=firsts[bad[0]] if bad else None)
        ck(all(result[k]==v for k,v in expected.items()),(side,member,'histogram/domain/witness'))


def check_coordinates(obj, base, e, layer, f, par, slots):
    decl=obj['coordinate']; slot=obj['slot']; code=obj['code']
    if layer.startswith('main'):
        pos=f.get('candidate_position',f.get('slot',f.get('position')))
        if pos is None:
            ck(decl is None and slot is None,'unbound main declaration'); return
        t,_,_=MAIN[e]
        s=(next(s for s in slots[e]['slots'] if s['key']==pos) if e=='comp' else slots[e]['slots'][pos])
        lane=f.get('lane') or 0
        ck(slot==dict(slot=pos,lane=lane,reader_site=s['site'],slot_ledger=path(t,'field_slots.json')),'main reader slot reference')
        enc=next((p['encoding'] for group in obj['archives'].values() for p in group if p['encoding']),None)
        expected=None if enc is None else ['main',s.get('key',s['site']),lane,enc]
    elif e=='club' and layer!='auxiliary':
        d=next(t for t in base['tables'] if t['parent_code']==par)
        ck(slot==dict(table_type=d['table_type'],source_task=d['source_task']),'club subtable source')
        if f['coordinates']:
            c,=f['coordinates']; enc=('u' if par in ('CNtp','Tchl') else 'i')+str(c['width_bytes']*8)
            expected=['fixed',d['table_type'],c['wire_offset'],enc]
        else:
            expected=['media_pair'] if par=='Csme' else None
    else:
        ck(slot is None,'not a main-row slot')
        if layer=='auxiliary':
            c=f['candidate_coordinate']; expected=['club_link',c['wire_offset'],'i'+str(c['width_bytes']*8)]
        elif par=='Ntxr':
            expected=['tax',f['source_record']['static_item_offset'],'i8']
        elif par=='Calt':
            expected=['calt']
        elif par=='Nftb':
            expected={'NbPn':['ftb',1],'NbFt':['ftb',2]}.get(code)
        elif par=='TCrs':
            enc={'PUnI':'u8','PUnT':'i8','PUnJ':'u16'}.get(code)
            expected=['crs',f['source_record_verbatim']['gates']['item_offset_at_tag3'],enc] if enc else None
        else:
            off=f['static_item_offset']
            expected=None if off is None else ['t9',par,off,('u' if f['encoding']=='B' else 'i')+str(f['width_bytes']*8)]
    ck(decl==expected,('declared coordinate does not match source',obj['xml_path']))


def gate(pairs, allowed, chain):
    if allowed is None:
        return 'held','no_enum_source'
    if sum((p['enum_misses'] or 0) for p in pairs):
        return 'held','enum_domain_conflict'
    if not any(p['tested'] for p in pairs) or any(p['status']=='not_bound' for p in pairs):
        return 'held','no_persisted_enum_samples'
    return ('L3','scoped_enum_and_existing_L3_chain') if chain else ('held','getter_chain_not_sufficient')


def verify():
    doc=read(OUT/'enum_inventory.json'); promo=read(OUT/'promoted.json'); prov=doc['provenance']; base=read(BASE); master=read(MASTER)
    accepted={x['path']:x for x in read('evidence/MANIFEST.json')['files']}
    ck(accepted[MASTER]['sha256']==FROZEN and len((ROOT/MASTER).read_bytes())==accepted[MASTER]['bytes'],'frozen MANIFEST')
    ck(prov['schema_version']==base['schema_version'] in {8,9} and prov['baseline']==BASE,'schema baseline')
    ck((prov['editor_sha256'],prov['image_base'])==(base['binary_provenance']['sha256'],base['binary_provenance']['image_base']),'binary provenance')
    pins=prov['protected_artifact_sha256']; mandatory={MASTER,PROV,'evidence/MANIFEST.json'} | {path(t,f) for t,_,_ in MAIN.values() for f in ('field_map.json','field_slots.json','REPORT.md')}
    ck(mandatory<=pins.keys() and pins[MASTER]==FROZEN and pins[PROV]==accepted[PROV]['sha256'],'artifact pins')
    for p,d in pins.items():
        # Legacy t61 output may retain a schema SHA; it is historical only.
        if p == BASE:
            continue
        pp=Path(p); ck(not pp.drive and not pp.is_absolute() and '..' not in pp.parts,'pin path is repository relative')
        ck(digest((ROOT/pp).read_bytes())==d,('protected source changed',p))
    ledger=read('scratch/t01/LEDGER.json')
    live={}
    for item in ledger['entries']:
        x=item.get('id')
        if x in LEDGER_GUARDS:
            ck(x not in live,('duplicate ledger entry',x))
            live[x]=item
    ck(set(live)==set(LEDGER_GUARDS),'ledger guard coverage')
    for x,want in LEDGER_GUARDS.items():
        got={'id':x,'kind':live[x].get('kind'),'level':live[x].get('level'),'claim_sha256':canonical_sha(live[x].get('claim'))}
        ck(got==want,('ledger entry guard',x))
    if 'ledger_entry_guards' in prov:
        ck(prov['ledger_entry_guards']==list(LEDGER_GUARDS.values()),'output ledger guard snapshot')
    ck(all(live[x]['level']=='L3' and live[x]['kind']=='acceptance' for x in LEDGER_GUARDS),'accepted main linkage')
    if base['schema_version']==8:
        ck(any(x.startswith(BASE+'#') for x in live['E98'].get('evidence',[])),'E98 baseline reference')
    else:
        ck('comp_main_row_fields' in base,'v9 comp fold')
    maps={e:read(path(t,'field_map.json')) for e,(t,_,_) in MAIN.items()}; slots={e:read(path(t,'field_slots.json')) for e,(t,_,_) in MAIN.items()}
    if base['schema_version']==9:
        fold=base['comp_main_row_fields']; held={f['xml_index']:f for f in fold['held_records']}
        ck(fold['acceptance_ledger_entry']=='E99' and len(held)==len(fold['held_records']) and
           held=={i:f for i,f in enumerate(maps['comp']['fields']) if f['status']=='held'},'v9 held crosswalk to E99')
    want={table(3),table(9),table(10),table(25),table('extra_9'),'club_links.dat'}|{table(tab['table_type']) for tab in base['tables'] if tab['held_fields']}
    refs={s:[v.get('archive',v.get('archives'))[s]['archive_sha256'] for v in slots.values()] for s in SIDES}
    payloads,meta=decode_archives(want,refs); ck(meta==prov['archive_manifest'],'archive manifest')
    replay=Replay(payloads,meta,base,slots); plan=definitions(base,maps); promotion=[]; counts={e:{} for e in MAIN}; n_scoped=0
    for obj in doc['occurrences']:
        origin=obj['source']; key=origin['path'],origin['pointer']; ck(key in plan,('duplicate/unknown origin',key)); e,layer,source,par=plan.pop(key)
        ii,xml,alias,schema=xml_loc(master,e,par,source); code=source.get('code','Npop')
        ck((obj['entity'],obj['layer'],obj['code'],obj['xml_indices'],obj['xml_path'],obj['xml_alias'],obj['schema'],origin['grade'])==(e,layer,code,ii,xml,alias,schema,source.get('grade',source.get('status'))),('XML/grade provenance',key))
        ref,defsrc,values=enum_table(master,schema or {})
        ck((obj['enum_ref'],obj['enum_ref_source'],obj['enum_values'])==(ref,defsrc,values),('scoped enum',xml))
        n_scoped+=values is not None; allowed=None if values is None else {v['value'] for v in values}
        ck(set(obj['archives'])==set(SIDES),'dual archive profile')
        all_profiles=[]
        for s in SIDES:
            results=obj['archives'][s]; independent=list(replay.make(s,e,layer,source,par)); ck(len(results)==len(independent),'profile group count')
            for actual,wanted in zip(results,independent):
                replay.check_profile(s,wanted,actual,schema or {},allowed)
            all_profiles.extend(results)
        check_coordinates(obj,base,e,layer,source,par,slots)
        chain=(e=='nation' and layer=='main') or (e=='comp' and code in ('CTty','dbty','PLgn')) or par=='Ntxr' or code=='PUnJ'
        ck(obj['existing_l3_chain']==chain,('chain scope',xml))
        if chain:
            if layer=='main' and e=='nation':
                static=slots[e]['slots'][source['slot']]['getter']
            elif layer=='main':
                static=source['static']
            elif par=='Ntxr':
                static={k:source['source_record'][k] for k in ('compare','getter_load','reader_site','object_offset')}
            else:
                static=source['source_record_verbatim']['gates']
            ck(obj['existing_static']==static,('getter citation',xml))
        grade,reason=gate(all_profiles,allowed,chain)
        ck((obj['grade'],obj['decision'])==(grade,reason),('gate',xml))
        ck(obj['members']==list(dict.fromkeys(p['member'] for p in all_profiles)),('physical members',xml))
        ck(obj['value_scope']==('accepted_scoped_enum' if grade=='L3' else 'held_coordinate_diagnostic_only'),('display scope',xml))
        # Preserve source counterexamples byte-for-byte (including non-wire controls).
        old=source.get('first_counterexample')
        if par=='TCrs':
            old={k:v['first_by_check'].get('ftjn_miss',v.get('first_wire_example')) for k,v in source['source_record_verbatim']['archives'].items()}
        elif par=='Ntxr':
            old=source['source_record']['first_counterexample']
        elif par in base['nation_t9_wire']['table_9']['parents']:
            old=source['source_record'].get('first_open_witness')
        elif par=='Nftb':
            old=source.get('join',{}).get('first_ordinal_miss')
        elif e=='club' and layer in ('subtable','shared_subtable'):
            p=source['profile'] if isinstance(source['profile'],dict) else {}
            old=next((v for v in (p.get('first_violation'),*(p.get('first_violations') or [])[:1],*(p.get('mismatch_samples') or [])[:1],p.get('first_domain_conflict'),p.get('first_not_a_live_ordinal')) if v),None)
        ck(obj['prior_first_counterexample']==old,('prior negative/witness',xml))
        updated=old
        for field,kind in [('first_enum_counterexample','enum'),('first_frozen_bound_counterexample','frozen_bound_diagnostic')]:
            hit=next(((s,p) for s in SIDES for p in obj['archives'][s] if p[field]),None)
            if hit:
                s,p=hit; updated={**p[field],'side':s,'member':p['member'],'kind':kind}; break
        ck(obj['first_counterexample']==updated,('selected first counterexample',xml))
        if grade=='L3':
            promotion.append({k: obj[k] for k in ('entity','layer','code','xml_path','source','slot','existing_static','enum_ref')})
        summary=counts[e].setdefault(layer,dict(occurrences=0,L3=0,held=0,decisions={}))
        summary['occurrences']+=1; summary[grade]+=1; summary['decisions'][reason]=summary['decisions'].get(reason,0)+1
    ck(not plan,'held occurrence omitted')
    for e,expected in {'nation':{'main':4,'main_other':3,'subtable':24},'club':{'main':11,'subtable':14,'shared_subtable':2,'auxiliary':5},'comp':{'main':10}}.items():
        ck({l:v['occurrences'] for l,v in counts[e].items()}==expected,('scope totals',e))
    ck(n_scoped==6 and doc['counts']==counts and doc['task']=='t61' and doc['L4']==0,'scope totals/L4')
    for p,x in zip(('EDfx','EDsc'),doc['scope_exclusions'],strict=True):
        fields=master['entities']['nation.xml'][0]['fields']; [(i,par)]=[(i,f) for i,f in enumerate(fields) if f['field']==p]
        [(j,f)]=[(j,f) for j,f in enumerate(par['list_item_fields']) if f['field']=='stadium_rules']; k,s,vals=enum_table(master,f)
        ck(x==dict(xml_path=f'nation.xml#nation/fields[{i}]/{p}/list_item_fields[{j}]/stadium_rules',enum_ref=k,enum_file=s['file'],enum_values=vals,
                   reason='not a source-ledger held item occurrence; no archive lane attributed'),'unbound child scope')
    ck(promo==dict(task='t61',counts=counts,promoted=promotion,L4=0),'promotion file')
    print(f't61 VERIFY PASS: {len(doc["occurrences"])} held inputs; {n_scoped} resolved enum_ref; {len(promotion)} promotions; L4=0')


def selftest():
    ck(tuple(LEDGER_GUARDS)==('E94','E97','E98','E99') and
       all(x['kind']=='acceptance' and x['level']=='L3' and len(x['claim_sha256'])==64 for x in LEDGER_GUARDS.values()),
       'entry-level ledger guard scope')
    x={'enums':{'Lo':{'file':'e.xml','values':[{'enum':'-1','enum_id':'3','name':'test'}]}}}
    ck(enum_table(x,{'field':'Lo'})[2] is None and enum_table(x,{'enum_ref':'LO'})[2] is None,'strict scope')
    ck(enum_table(x,{'enum_ref':'Lo'})[2][0]==dict(value=-1,label='test',enum_id='3'),'numeric code, not UI ID')
    live=dict(tested=1,enum_misses=0,status='scanned')
    ck(gate([live],{-1},True)[0]=='L3' and gate([live],{-1},False)[0]=='held','static gate')
    ck(gate([dict(live,enum_misses=1)],{-1},True)[1]=='enum_domain_conflict','counterexample wins')
    ck(gate([dict(live,tested=0)],{-1},True)[0]=='held','empty domain is not a pass')
    print('t61 verifier selftest PASS')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    g=ap.add_mutually_exclusive_group(); g.add_argument('--selftest',action='store_true'); g.add_argument('--check',action='store_true')
    args=ap.parse_args()
    try:
        (selftest if args.selftest else verify)(); return 0
    except Fail as error:
        print(f'FAIL: {error}',file=sys.stderr); return 1
    except Exception as error:
        print(f'ERROR: {type(error).__name__}: {error}',file=sys.stderr); return 2


if __name__=='__main__':
    sys.exit(main())
