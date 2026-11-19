"""t61: read-only scoped enum sweep over accepted held records."""
import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch/t61/out'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
BASE = 'reports/club_nation_subtable_schema.json'
LEDGER = 'scratch/t01/LEDGER.json'
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
FROZEN = '7d57477e144d5359ccde64bb24b3ba7c640ef41738ed196eba8a38e792776eda'
SIDES = ('client', 'server')
MAIN = {'nation': (55, 10, 251, 't55_natmain_fields'), 'club': (57, 3, 84259, 't57_clubmain_fields'), 'comp': (59, 25, 7047, 't59_compmain_fields')}
LEDGER_GUARDS = {
    'E94': {'id':'E94','kind':'acceptance','level':'L3','claim_sha256':'358243779bba359656ecae6804cea9cea26b1739ffce5bf96a2599d735263c89'},
    'E97': {'id':'E97','kind':'acceptance','level':'L3','claim_sha256':'ba5a1079403dd970b30c9304a90c37d5a66f3d28163ee2cf2588fd355129ff32'},
    'E98': {'id':'E98','kind':'acceptance','level':'L3','claim_sha256':'57a2384c170c3effc159a98012b866ab174849da8849269abc118b8e7fe4f150'},
    'E99': {'id':'E99','kind':'acceptance','level':'L3','claim_sha256':'e13990af22d739ba1f6a61e9adc2211febb051821845a48358e30306d452b16b'},
}
T9_STRIDE = {'Nntp': 9, 'Nctp': 8, 'Nrtp': 8, 'Nfmp': 9, 'NCro': 9}


class Check(Exception):
    pass


def need(ok, detail):
    if not ok:
        raise Check(detail)


def h(b):
    return sha256(b).hexdigest()


def canonical_sha(value):
    return h(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8'))


def table(t):
    return f'table_{t}.dat'


def prior(t, name):
    return f'scratch/t{t}/out/{name}'


def json_at(path):
    return json.loads((ROOT / path).read_bytes())


def ref_data(master, field):
    ref = field.get('enum_ref')
    definition = master['enums'].get(ref)
    if not definition or not definition['values']:
        return ref, None, None
    def decode(token):
        try:
            return int(token)
        except ValueError:
            return token
    return ref, definition['file'], [dict(value=decode(x['enum']), label=x['name'], enum_id=x.get('enum_id')) for x in definition['values']]


def decision(values, profiles, same_member):
    active = [p for p in profiles if p['status'] != 'mode_bypass' and p['status'] != 'member_absent']
    if values is None:
        return 'held', 'no_enum_source'
    if any(p['enum_misses'] for p in active):
        return 'held', 'enum_domain_conflict'
    if not active or not any(p['tested'] for p in active) or any(p['status'] == 'not_bound' for p in active):
        return 'held', 'no_persisted_enum_samples'
    if not same_member:
        return 'held', 'getter_chain_not_sufficient'
    return 'L3', 'scoped_enum_and_existing_L3_chain'


class Sweep:
    def __init__(self):
        self.protected = {}
        self.master = self.load(MASTER)
        self.baseline = self.load(BASE, pin=False)
        m = {x['path']: x for x in self.load('evidence/MANIFEST.json')['files']}
        self.track(PROV)
        need(FROZEN == self.protected[MASTER] == m[MASTER]['sha256'], 'frozen master SHA')
        need(self.protected[PROV] == m[PROV]['sha256'], 'IDA provenance SHA')
        self.version = self.baseline['schema_version']
        need(self.version in (8, 9), 'baseline v8/v9 only')
        ledger = self.load(LEDGER, pin=False)
        entries = {}
        for item in (ledger['entries'] if isinstance(ledger, dict) else ledger):
            key = item.get('id')
            if key in LEDGER_GUARDS:
                need(key not in entries, f'duplicate ledger entry {key}')
                entries[key] = item
        need(set(entries) == set(LEDGER_GUARDS), 'ledger entry guard set incomplete')
        self.ledger_guards = []
        for key, expected in LEDGER_GUARDS.items():
            item = entries[key]
            actual = dict(id=key, kind=item.get('kind'), level=item.get('level'), claim_sha256=canonical_sha(item.get('claim')))
            need(actual == expected, f'{key} entry guard')
            self.ledger_guards.append(actual)
        for k in ('E94', 'E97', 'E98', 'E99'):
            need(entries[k]['kind'] == 'acceptance' and entries[k]['level'] == 'L3', k)
        if self.version==8:
            need(any(x.startswith(BASE+'#') for x in entries['E98'].get('evidence',[])), 'E98 v8 baseline reference')
        else:
            need('comp_main_row_fields' in self.baseline,'v9 comp fold')
        self.fields = {e: self.master['entities'][e + '.xml'][0]['fields'] for e in MAIN}
        self.maps = {e: self.load(prior(t, 'field_map.json')) for e, (t, *_) in MAIN.items()}
        if self.version==9:
            fold=self.baseline['comp_main_row_fields']
            need(fold['acceptance_ledger_entry']=='E99' and fold['held_records']==[r for r in self.maps['comp']['fields'] if r['status']=='held'],
                 'v9/E99 held occurrences match t59 verbatim')
        self.slots = {e: self.load(prior(t, 'field_slots.json')) for e, (t, *_) in MAIN.items()}
        self.raw = {}
        self.books = {}
        self.rows = {}
        self.todo = []
        for t, *_ in MAIN.values():
            self.track(prior(t, 'REPORT.md'))

    def track(self, p):
        b = (ROOT / p).read_bytes()
        self.protected.setdefault(p, h(b))
        return b

    def load(self, p, pin=True):
        return json.loads(self.track(p) if pin else (ROOT / p).read_bytes())

    def xml(self, entity, parent, code=None, schema=None):
        out = []
        for i, f in enumerate(self.fields[entity]):
            if f['field'] != parent:
                continue
            if code is None:
                out.append((i, None, f))
            else:
                out += [(i, j, x) for j, x in enumerate(f.get('list_item_fields', [])) if x['field'] == code and (schema is None or x == schema)]
        need(len(out) == 1, (entity, parent, code, 'nonunique XML occurrence'))
        return out[0]

    def add(self, e, layer, code, coord, src, record, indexes, *, slot=None, static=None, alias=None, chain=False, reason=None):
        i, j, field = indexes
        source_grade = record.get('grade', record.get('status'))
        first = record.get('first_counterexample')
        ref, enum_file, values = ref_data(self.master, field or {})
        location = None if i is None else f'{e}.xml#{e}/fields[{i}]/{self.fields[e][i]["field"]}'
        if j is not None:
            location += f'/list_item_fields[{j}]/{code}'
        self.todo.append(dict(entity=e, layer=layer, code=code, xml_path=location, xml_indices=[i, j],
                              schema=field, xml_alias=alias, enum_ref=ref, enum_ref_source=None if values is None else dict(master=MASTER, key=ref, file=enum_file),
                              enum_values=values, source=dict(path=src[0], pointer=src[1], grade=source_grade),
                              value_scope='held_coordinate_diagnostic_only',
                              prior_reason=reason or record.get('reason') or record.get('hold_reason') or record.get('held_reason') or record.get('coordinate_note'),
                              prior_first_counterexample=first, coordinate=coord, slot=slot, existing_static=static, existing_l3_chain=chain))

    def catalog(self):
        for e, (t, tid, _, _) in MAIN.items():
            for i, f in enumerate(self.maps[e]['fields']):
                grade = f.get('grade', f.get('status'))
                if grade not in ('held', 'linked_parent_held'):
                    continue
                code = f['code']; field = self.fields[e][i]
                need(f['xml_index'] == i and f['schema'] == field, (e, i, 'XML drift'))
                pos = f.get('candidate_position', f.get('slot'))
                static = f.get('static'); coord = None; slot = None; fmt = None
                if pos is not None:
                    entry = (next(x for x in self.slots[e]['slots'] if x['key'] == pos) if e == 'comp' else self.slots[e]['slots'][pos])
                    key = entry.get('key', entry['site']); lane = f.get('lane') or 0
                    fmt = {'nation': 'i8', 'club': {'Cnam':'utf8_length','Csnm':'utf8_length','PLgn':'i8','Cprs':'i8'}.get(code),
                           'comp': 'u32' if code == 'rdui' else 'i8' if code == 'dbty' else 'u8'}[e]
                    if e == 'nation':
                        static = entry['getter']
                        if code == 'Nftb':
                            fmt = 'i16'
                    if fmt:
                        coord = ['main', key, lane, fmt]
                    slot = dict(slot=pos, lane=lane, reader_site=entry['site'], slot_ledger=prior(t, 'field_slots.json'))
                elif e == 'club' and code in ('CLat','CLon','Cyfn','Crep','Csti','Cdvi'):
                    static = {'source': prior(t, 'REPORT.md'), 'binding': 'no accepted same-object main-row lane'}
                self.add(e, 'main' if grade == 'held' and not (e == 'nation' and pos is None) else 'main_other', code, coord,
                         (prior(t, 'field_map.json'), f'/fields/{i}'), f, (i, None, field), slot=slot, static=static,
                         chain=bool(static and (e == 'nation' and fmt == 'i8' or e == 'comp' and code in ('CTty','dbty','PLgn'))))
        f = self.maps['nation']['supplemental']['Npop']
        s = self.slots['nation']['slots'][f['position']]
        self.add('nation', 'main_other', 'Npop', ['main',s['site'],0,'i32'], (prior(55,'field_map.json'),'/supplemental/Npop'),
                 f, (None,None,None), slot=dict(slot=f['position'],lane=0,reader_site=s['site'],slot_ledger=prior(55,'field_slots.json')),
                 static=s['getter'], reason='not in active frozen XML')
        self.catalog_subtables()

    def catalog_subtables(self):
        for i, t in enumerate(self.baseline['tables']):
            tid, p = t['table_type'], t['parent_code']
            for j, f in enumerate(t['held_fields']):
                code = f['code']; sch = {k:v for k,v in f['schema'].items() if k != 'idx'}
                ix = self.xml('club', p, code, sch)
                alias = None
                if p == 'Tchl':
                    ai, aj, _ = self.xml('nation', p, code, sch)
                    alias = f'nation.xml#nation/fields[{ai}]/{p}/list_item_fields[{aj}]/{code}'
                c = f['coordinates']; coord = None
                if c:
                    width = c[0]['width_bytes']; fmt = ('u' if p in ('CNtp','Tchl') else 'i') + str(width * 8)
                    coord = ['fixed', tid, c[0]['wire_offset'], fmt]
                elif p == 'Csme':
                    coord = ['media_pair']
                prof = f['profile'] if isinstance(f['profile'], dict) else {}
                first = (prof.get('first_violation') or next(iter(prof.get('first_violations', [])), None)
                         or next(iter(prof.get('mismatch_samples', [])), None)
                         or prof.get('first_domain_conflict') or prof.get('first_not_a_live_ordinal'))
                entry = dict(f, first_counterexample=first)
                self.add('club','shared_subtable' if alias else 'subtable', code, coord, (BASE,f'/tables/{i}/held_fields/{j}'),
                         entry, ix, reason=f.get('held_reason'), slot=dict(table_type=tid,source_task=t['source_task']), alias=alias)
        for i, aux in enumerate(self.baseline['club_auxiliary_sources']):
            for j, view in enumerate(aux['views']):
                for k, f in enumerate(view['occurrences']):
                    if not f['grade'].startswith('held'):
                        continue
                    q = f['candidate_coordinate']; code=f['code']
                    self.add('club','auxiliary',code,['club_link',q['wire_offset'],'i'+str(q['width_bytes']*8)],
                             (BASE,f'/club_auxiliary_sources/{i}/views/{j}/occurrences/{k}'),f,self.xml('club',view['view'],code,f['schema']))
        nat = self.baseline['nation_static_side']; tax = nat['Ntxr']
        for i,f in enumerate(tax['fields']):
            if f['grade'] != 'held':
                continue
            code=f['code']; rec=f['source_record']
            self.add('nation','subtable',code,['tax',rec['static_item_offset'],'i8'],(BASE,f'/nation_static_side/Ntxr/fields/{i}'),
                     dict(f,first_counterexample=rec['first_counterexample']),self.xml('nation','Ntxr',code,f['schema']),
                     static={k:rec[k] for k in ('compare','getter_load','reader_site','object_offset')},chain=True)
        for p,v in self.baseline['nation_t9_wire']['table_9']['parents'].items():
            for i,f in enumerate(v['fields']):
                if f['grade'] != 'held':
                    continue
                code=f['code']; rec=f['source_record']; off=f['static_item_offset']; w=f['width_bytes']
                coord=None if off is None else ['t9',p,off,('u' if f['encoding']=='B' else 'i')+str(w*8)]
                self.add('nation','subtable',code,coord,(BASE,f'/nation_t9_wire/table_9/parents/{p}/fields/{i}'),
                         dict(f,first_counterexample=rec.get('first_open_witness')),self.xml('nation',p,code,f['schema']))
        for p,v in nat['t51_followup']['field_ledgers'].items():
            for code,f in v['fields'].items():
                if f['status'] != 'held':
                    continue
                coord = ['calt'] if p == 'Calt' else ['ftb', {'NbPn':1,'NbFt':2}[code]] if code != 'NbPi' else None
                first=f.get('first_counterexample') or f.get('join',{}).get('first_ordinal_miss')
                self.add('nation','subtable',code,coord,(BASE,f'/nation_static_side/t51_followup/field_ledgers/{p}/fields/{code}'),
                         dict(f,first_counterexample=first),self.xml('nation',p,code,f['schema']))
        for code,f in self.baseline['nation_t9_wire']['t53_crs_adjudication']['field_dispositions'].items():
            rec=f['source_record_verbatim']; gates=rec['gates']; coord=None
            if code != 'PUnP':
                coord=['crs',gates['item_offset_at_tag3'],{'PUnI':'u8','PUnT':'i8','PUnJ':'u16'}[code]]
            first={k:v['first_by_check'].get('ftjn_miss',v.get('first_wire_example')) for k,v in rec['archives'].items()}
            self.add('nation','subtable',code,coord,(BASE,f'/nation_t9_wire/t53_crs_adjudication/field_dispositions/{code}'),
                     dict(f,first_counterexample=first),self.xml('nation','TCrs',code,rec['schema']),static=gates,
                     reason=f['domain_result'],chain=code=='PUnJ')

    def archives(self):
        depot=Path(os.environ.get('FM24_DB_DIR',ROOT/'scratch/data'))
        if depot.drive.upper()=='Z:' or depot.resolve().drive.upper()=='Z:':
            raise ValueError('Z: forbidden')
        sys.path.append(str(ROOT.parent/'fm24/tools/python'))
        import zstandard
        read_dir=runpy.run_path(str(ROOT.parent/'fm24/scripts/modding_read_dbdat.py'))['_entries']
        members={table(tid) for _,tid,*_ in MAIN.values()} | {table(t['table_type']) for t in self.baseline['tables'] if t['held_fields']} | {table(9),table('extra_9'),'club_links.dat'}
        self.archive_meta={}
        for side in SIDES:
            _, raw, d=read_dir(depot/f'{side}_db.dat'); base=d['data_base']
            archive_hash=h(raw)
            refs=[v.get('archives',v.get('archive'))[side]['archive_sha256'] for v in self.slots.values()]
            need(refs==[archive_hash]*3,(side,'accepted archive digest'))
            by_name={e['path']:e for e in d['entries']}; need(len(by_name)==len(d['entries']), 'unique TOC names')
            result={}
            for name in sorted(members):
                entry=by_name.get(f'{side}_db/{name}')
                if entry is None:
                    result[name]=None
                    continue
                lo=base+entry['offset']; hi=lo+entry['packed_size']
                bound=min((base+x['offset'] for x in by_name.values() if x['offset']>entry['offset']),default=d['toc_offset'])
                need(base<=lo<hi<=bound<=d['toc_offset'], (side,name,'member bounds'))
                p=lo; hits=[]
                while p<hi:
                    need(raw[p:p+4]==bytes.fromhex('28b52ffd'),'frame magic')
                    dec=zstandard.ZstdDecompressor().decompressobj(); b=dec.decompress(raw[p:hi]); q=hi-len(dec.unused_data)
                    need(dec.eof and q>p,(name,'frame EOF'))
                    if len(b)==entry['size']:
                        hits.append(b)
                    p=q
                need(len(hits)==1,(name,'bounded size select'))
                b,=hits; self.raw[side,name]=b
                result[name]=dict(payload_sha256=h(b),bytes=len(b),header_rows=struct.unpack_from('<I',b,8)[0])
            self.archive_meta[side]=dict(archive_sha256=archive_hash,members=result)

    def main_book(self, e, side):
        k=e,side
        if k not in self.books:
            t,tid,n,worker=MAIN[e]; b=self.raw[side,table(tid)]
            a=self.slots[e].get('archives',self.slots[e].get('archive'))[side]['members'][str(tid)]
            need(h(b)==a['payload_sha256'],(e, side, 'accepted payload digest'))
            fn=runpy.run_path(str(ROOT / f'scripts/{worker}.py'))
            try:
                rows, book, *_=fn['replay'](b, int(side=='server'))
            except fn.get('Check',fn.get('Failed')) as exc:
                raise Check(exc) from exc
            need(len(rows)==n, (e,side,'row census'))
            self.rows[k]=rows; self.books[k]=book
        return self.books[k]

    def accepted_rows(self, side, member, p):
        k=(side,p)
        if k not in self.rows:
            doc=self.load(p); b=self.raw[side,member]; end=doc.get('header',13)
            need(doc['payload_sha256']==h(b),p)
            for i,r in enumerate(doc['rows']):
                a=r.get('start',r.get('wire13')); z=r['end']
                need(r['row']==i and end==a<z and h(b[a:z])==r.get('row_sha256',r.get('wire_sha256')), (p,i,'row span'))
                end=z
            foot=doc.get('footer_hex',doc['footer']); foot=foot['raw'] if isinstance(foot,dict) else foot
            need(len(doc['rows'])==251 and b[end:].hex()==foot,p)
            self.rows[k]=doc['rows']
        return self.rows[k]

    def unbound(self, f, side, member):
        path = f['xml_path'] or ''
        if '/TCrs/' in path:
            members = [table(9), table('extra_9')]
        elif '/Nftb/' in path:
            members = [table(10)]
        elif '/repu' in path:
            members = [table(9)]
        else:
            members = [member]
        excluded = f['schema'].get('database_table_type') == 'person'
        out = []
        for name in members:
            d = self.archive_meta[side]['members'].get(name)
            status = 'person_boundary' if excluded else 'not_bound' if d else 'member_absent'
            out.append((name,status,d['header_rows'] if d else 0,None,()))
        return out

    def gather(self, f, side):
        """Return (member, status, row count, encoding, ordered raw cells)."""
        e=f['entity']; coord=f['coordinate']
        inferred=table(MAIN[e][1]) if f['layer'].startswith('main') else (table(f['slot']['table_type']) if f['slot'] and 'table_type' in f['slot'] else None)
        if coord is None:
            return self.unbound(f,side,inferred)
        kind,*args=coord; n=None; cells=[]; fmt=None; member=inferred
        if kind=='main':
            key,lane,fmt=args; n=MAIN[e][2]; b=self.raw[side,member]; book=self.main_book(e, side)
            src=book.get(key,[])
            s=self.slots[e]['slots'][f['slot']['slot']] if e!='comp' else next(x for x in self.slots[e]['slots'] if x['key']==key)
            if e=='nation':
                need([[a,w] for _,a,w,_ in src]==s['coordinates'][side],(e,key,side,'coordinate ref'))
            else:
                summary=s['profiles'][side]
                if src or summary.get('coordinate_sha256'):
                    need(h(b''.join(struct.pack('<III',*x) for x in src))==summary.get('coordinate_sha256'),(e,key,side,'coordinate SHA'))
            if fmt=='utf8_length':
                prefix=book[key.replace('_bytes','_len')]; need(len(prefix)==n,'all text lengths'); offsets={r:(a,w) for r,a,w in src}
                for r,a,w in prefix:
                    p,z=offsets.get(r,(a+w,0)); need(p==a+w and z==struct.unpack_from('<I',b,a)[0], 'text span')
                    cells.append((r,None,p,z))
            else:
                width=int(fmt[1:])//8
                for row,a,w,*_ in src:
                    need(lane+width<=w,(e,key,row,'lane width')); cells.append((row,None,a+lane,width))
            need(len(cells) in (0,n),(f['code'],side,'all main rows'))
            return [(member,'scanned' if cells else 'mode_bypass',n,fmt,cells)]
        if kind in ('fixed','club_link','media_pair'):
            aux=kind=='club_link'; tid=59 if kind=='media_pair' else args[0] if kind=='fixed' else None
            member='club_links.dat' if aux else table(tid); b=self.raw.get((side,member))
            if b is None:
                return [(member,'member_absent',0,None,())]
            if aux:
                off,fmt=args; doc=self.baseline['club_auxiliary_sources'][0]['server_payload']; start=12; stride=47
            else:
                d=next(x for x in self.baseline['tables'] if x['table_type']==tid); doc=d['server_payload' if side=='server' else 'client_observation']; start=13; stride=doc.get('stride_bytes')
                if kind=='fixed':
                    _,off,fmt=args
            n=doc['row_count']; need(h(b)==doc['payload_sha256'] and n==struct.unpack_from('<I',b,8)[0],(member,side,'payload provenance'))
            if side=='client':
                need(stride==13 and start+n*stride+9==len(b),'client identity-only'); return [(member,'mode_bypass',n,fmt,())]
            if kind=='media_pair':
                fmt='pair_i32'; p=start
                for r in range(n):
                    cnt=struct.unpack_from('<I',b,p+6)[0]; q=p+10+cnt*10
                    need(q+12<=len(b)-9 and struct.unpack_from('<I',b,q)[0]==r,('Csme',r))
                    cells.extend((r,j,p+11+10*j,8) for j in range(cnt)); p=q+12
                need(p+9==len(b),'Csme EOF')
            else:
                width=int(fmt[1:])//8; need(off+width<=stride and start+n*stride+(0 if aux else 9)==len(b), (member,'fixed closure'))
                cells=[(r,None,start+stride*r+off,width) for r in range(n)]
            return [(member,'scanned',n,fmt,cells)]
        if kind=='tax':
            off,fmt=args; member=table(10); b=self.raw[side,member]; n=251
            book=self.main_book('nation',side); site=self.slots['nation']['slots'][11]['site']
            for r,a,w,count in book.get(site,[]):
                p=a+4
                for j in range(count):
                    need(b[p]==2,('Ntxr',r,j,'tag')); cells.append((r,j,p+off,1)); p+=25
                need(p==a+w,('Ntxr',r,'span'))
            return [(member,'scanned' if side=='server' else 'mode_bypass',n,fmt,cells)]
        if kind=='ftb':
            index,=args; member=table(10); fmt='i32'; n=251
            rows=self.accepted_rows(side,member,prior(51,f'cursor_table_10_{side}.json')); b=self.raw[side,member]
            for r in rows:
                d=r['Nftb']
                if d is None:
                    continue
                for x in d['items']:
                    a=x['lanes'][index][0]; need(a==x['end']-16+4*index and b[x['absolute']:x['end']].hex()==x['raw'],'Nftb lane')
                    cells.append((r['row'],x['item'],a,4))
            return [(member,'scanned' if side=='server' else 'mode_bypass',n,fmt,cells)]
        if kind in ('t9','calt'):
            member=table(9); b=self.raw[side,member]; n=251
            rows=self.accepted_rows(side,member,prior(51,f'cursor_table_9_{side}.json') if kind=='calt' else prior(49,f'cursor_t9_{side}.json'))
            for r in rows:
                if kind=='calt':
                    d=r['Calt']; need(d is None if side=='client' else b[d['count_at']:d['start']]==b'\0\0' and d['count']==0,'Calt zero count')
                    continue
                p,off,fmt=args; width=int(fmt[1:])//8; stride=T9_STRIDE[p]; d=r['collections'].get(p)
                if not d:
                    continue
                if d['count'] is None:
                    a,v=d['gate']; need(b[a]==v==0,'NCro gate'); continue
                a=d['start']; q=d['end']; cnt=d['count']; c=d['count_at']
                need(int.from_bytes(b[c:a],'little',signed=True)==cnt and a+stride*cnt==q<=r['identity_at'] and off+width<=stride,('t9 collection',p,r['row']))
                cells.extend((r['row'],j,a+j*stride+off,width) for j in range(cnt))
            parent=args[0] if kind=='t9' else 'Calt'
            bypass=side=='client' and parent in ('Nfmp','Calt','NCro')
            return [(member,'mode_bypass' if bypass else 'scanned' if cells else 'no_items',n,fmt,cells)]
        need(kind=='crs',kind)
        off,fmt=args; width=int(fmt[1:])//8; groups=[]
        for label,member in [('main',table(9)),('extra',table('extra_9'))]:
            b=self.raw[side,member]; cells=[]
            rows=self.accepted_rows(side,member,prior(53,f'cursor_crs_{label}_{side}.json'))
            for r in rows:
                if (v:=r['vector']) is None:
                    continue
                need(v['count']==len(v['items']) and struct.unpack_from('<I',b,v['count_at'])[0]==v['count'],'TCrs count')
                for x in v['items']:
                    a=x['absolute']; z=x['end']; need(z-a==12 and b[a:z].hex()==x['raw'] and x['tag']==3,'TCrs observed item')
                    cells.append((r['row'],x['item'],a+off,width))
            groups.append((member,'scanned' if side=='server' else 'mode_bypass',251,fmt,cells))
        return groups

    def profile(self, side, member, status, n, fmt, cells, field, enum):
        b=self.raw.get((side,member)); count=Counter(); misses=Counter(); bounds=0; first=bad=bound_bad=None
        lo=field.get('min_value'); hi=field.get('max_value'); maxlen=field.get('max_length')
        domains={x['value'] for x in enum} if enum is not None else None
        for row,item,at,w in cells:
            need(0<=at<=at+w<=len(b), 'raw sample range')
            chunk=b[at:at+w]
            if fmt=='utf8_length':
                value=len(chunk.decode('utf-8'))
            elif fmt=='pair_i32':
                value=','.join(map(str,struct.unpack('<ii',chunk)))
            else:
                value=int.from_bytes(chunk,'little',signed=fmt[0]=='i')
            def witness():
                return dict(row=row,item=item,absolute=at,raw=chunk.hex(),value=value)
            if first is None:
                first=witness()
            count[value]+=1
            if domains is not None and value not in domains:
                misses[value]+=1
                if bad is None:
                    bad=witness()
            if isinstance(value,int) and ((lo is not None and value<int(lo)) or (hi is not None and value>int(hi)) or (fmt=='utf8_length' and maxlen is not None and value>int(maxlen))):
                bounds+=1
                if bound_bad is None:
                    bound_bad=witness()
        return dict(member=member,status=status,rows=n,encoding=fmt,tested=sum(count.values()),histogram={str(k):v for k,v in sorted(count.items())},
                    enum_misses=None if enum is None or status=='not_bound' else sum(misses.values()),
                    out_of_enum={str(k):v for k,v in sorted(misses.items())},first_value=first,first_enum_counterexample=bad,
                    frozen_bound_violations=bounds,first_frozen_bound_counterexample=bound_bad)

    def run(self):
        self.catalog()
        self.archives()
        rows=[]; promoted=[]
        for f in sorted(self.todo,key=lambda x:x['enum_values'] is None):
            f['archives']={side:[self.profile(side,*args,f['schema'] or {}, f['enum_values']) for args in self.gather(f,side)] for side in SIDES}
            profiles=[p for side in SIDES for p in f['archives'][side]]
            f['members']=list(dict.fromkeys(p['member'] for p in profiles))
            f['grade'],f['decision']=decision(f['enum_values'],profiles,f['existing_l3_chain'])
            if f['grade']=='L3':
                f['value_scope']='accepted_scoped_enum'
            f['first_counterexample']=next((dict(p['first_enum_counterexample'],side=side,member=p['member'],kind='enum') for side in SIDES for p in f['archives'][side] if p['first_enum_counterexample']),None)
            if f['first_counterexample'] is None:
                f['first_counterexample']=next((dict(p['first_frozen_bound_counterexample'],side=side,member=p['member'],kind='frozen_bound_diagnostic') for side in SIDES for p in f['archives'][side] if p['first_frozen_bound_counterexample']),f['prior_first_counterexample'])
            if f['grade']=='L3':
                promoted.append({k:f[k] for k in ('entity','layer','code','xml_path','source','slot','existing_static','enum_ref')})
            rows.append(f)
        totals={}
        for e in MAIN:
            totals[e]={}
            for layer in dict.fromkeys(f['layer'] for f in rows if f['entity']==e):
                r=[f for f in rows if f['entity']==e and f['layer']==layer]
                totals[e][layer]=dict(occurrences=len(r),L3=sum(f['grade']=='L3' for f in r),held=sum(f['grade']=='held' for f in r),decisions=dict(Counter(f['decision'] for f in r)))
        protected={k:v for k,v in sorted(self.protected.items())}
        for p,want in protected.items():
            need(h((ROOT/p).read_bytes())==want,(p,'source drift during sweep'))
        meta=dict(schema_version=self.version,baseline=BASE,editor_sha256=self.baseline['binary_provenance']['sha256'],image_base=self.baseline['binary_provenance']['image_base'],
                  ledger_entry_guards=self.ledger_guards,protected_artifact_sha256=protected,archive_manifest=self.archive_meta)
        excluded = []
        for p in ('EDfx','EDsc'):
            i,j,field = self.xml('nation',p,'stadium_rules')
            ref,enum_file,values = ref_data(self.master,field)
            excluded.append(dict(xml_path=f'nation.xml#nation/fields[{i}]/{p}/list_item_fields[{j}]/stadium_rules',enum_ref=ref,
                                 enum_file=enum_file,enum_values=values,reason='not a source-ledger held item occurrence; no archive lane attributed'))
        return dict(task='t61',provenance=meta,counts=totals,occurrences=rows,scope_exclusions=excluded,L4=0),dict(task='t61',counts=totals,promoted=promoted,L4=0)


def selftest():
    need(tuple(LEDGER_GUARDS)==('E94','E97','E98','E99') and
         all(x['kind']=='acceptance' and x['level']=='L3' and len(x['claim_sha256'])==64 for x in LEDGER_GUARDS.values()),
         'entry-level ledger guard scope')
    fake={'enums':{'X':{'file':'enums.xml','values':[{'enum':'-1','enum_id':'3','name':'label'}]}}}
    need(ref_data(fake,{'enum_ref':'X'})[2] == [dict(value=-1,label='label',enum_id='3')],'enum is not enum_id')
    need(ref_data(fake,{'field':'X'})[2] is None and ref_data(fake,{'enum_ref':'x'})[2] is None,'only explicit case-sensitive references')
    p=dict(status='scanned',tested=1,enum_misses=0); v=[{'value':1}]
    need(decision(v,[p],True)[0]=='L3' and decision(v,[p],False)[0]=='held','static gate')
    need(decision(v,[dict(p,enum_misses=1)],True)[1]=='enum_domain_conflict','single miss')
    need(decision(v,[dict(p,status='mode_bypass',tested=0)],True)[0]=='held','no vacuous promotion')
    print('t61 builder selftest PASS')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    g=ap.add_mutually_exclusive_group(); g.add_argument('--build',action='store_true'); g.add_argument('--selftest',action='store_true')
    a=ap.parse_args()
    try:
        if a.selftest:
            selftest(); return 0
        inv,pro=Sweep().run(); OUT.mkdir(parents=True,exist_ok=True)
        for name,doc in [('enum_inventory.json',inv),('promoted.json',pro)]:
            (OUT/name).write_text(json.dumps(doc,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
        print(f't61 build PASS: {len(inv["occurrences"])} occurrences; {len(pro["promoted"])} L3; L4=0')
        return 0
    except Check as exc:
        print(f'FAIL: {exc}',file=sys.stderr); return 1
    except Exception as exc:
        print(f'ERROR: {type(exc).__name__}: {exc}',file=sys.stderr); return 2


if __name__=='__main__':
    sys.exit(main())
