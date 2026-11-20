"""Census of inline COMP collections, using t59 frozen outer coordinates."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import runpy
import struct as S
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch/t66/out'
T59 = ROOT / 'scratch/t59/out'
SIDES = ('client', 'server')
TARGETS = (2, 3, 10, 21, 25)
# Wire order comes from t59 execution templates, not these dictionary keys.
SPEC = {
    'vec18': ('vec18', None, 'i32 N; N × (i8 tag + 4 + 2 + 1 + [1 if tag >= 2])'),
    '+0xe8': ('obj_e8', 'e8_present', 'u32 version + u32 N; N × (i16 tag + 4 + 1 + 1 + (2 if tag >= 2 else 1) + 1 + [1 if tag >= 3])'),
    '+0xc0': ('obj_c0', 'c0_present', 'u8 version + u32 N; N × (u8 tag + 1 + u32 M + M × (u8 tag + 1 + 1 + 1 + 4 + 4))'),
    '+0xc8': ('obj_c8', 'c8_present', 'u8 tag + exactly 4 × (u8 tag + 1 + 1 + 1 + 1 + 1); no serialized count'),
    '+0xd0': ('obj_d0', 'd0_present', 'one 4+4+1+1+4+1 B record; no serialized count or item tag'),
    '+0xd8': ('obj_d8', 'd8_present', 'one 4+4+1+1+4+1 B record; no serialized count or item tag'),
    '+0x100': ('vec100', None, 'i16 N; N × (1 + 2 + 2); no item tag'),
    'vec30': ('vec30', None, 'u32 N; N × 2 (static only for N > 0)'),
    '+0xa8': ('obj_a8', 'a8_present', 'static optional; no payload coordinate'),
    '+0xe0': ('obj_e0', 'e0_present', 'static optional; no payload coordinate'),
}
# Hand-selected PE ranges: source, destinations, transfer sizes and taken edges.
PE_RANGES = '''f2ba2d:f2ba54 ed0a40:ed0a45 3b3f0d0:3b3f10c eb7394:eb73ad eb7502:eb754a eb75bd:eb75d7 eb76ac:eb773c eb7776:eb77bd eb77f7:eb783e eb7853:eb786d eb7890:eb78b8 eb78e2:eb7927 eb7951:eb7a3a eb7dbe:eb7e42 eb7e50:eb7e55 3b1f030:3b1f111 9f7c30:9f7c35 37b8710:37b87c9 155b450:155b455 4387ab0:4387af7 4387b36:4387bb8 155c139:155c16b 155c2e3:155c427 155ce40:155ce45 438b680:438b6dc 155d03c:155d06b 155d22c:155d2a0 155d392:155d4d4 155de30:155de35 438e850:438e8c8 155dad0:155dad5 438bfd0:438c095 eb5580:eb5585 3b1e790:3b1e8c8 eb87a8:eb880e eb8866:eb88de f7e440:f7e445 3bf3460:3bf351d f7f440:f7f445 3bf70c0:3bf71c0 f73c50:f73c55 3be8bc0:3be8c26 9f9840:9f9845 37be3a0:37be410 9f9ab0:9f9ab5 37c18b0:37c191f 838b5a:838b79'''
PE_RANGES += ' fb19b:fb1a7 efee00:efee20 efee90:efeeaa f026c0:f026e5 f04056:f04076 f04184:f041b2 f042c3:f042ca 3ceb8e2:3ceb8e6 eb9171:eb91d6 9f7b50:9f7b55 37b81b0:37b8232 eb90e9:eb9108 eb9137:eb9156 eb5440:eb5445 3b1e480:3b1e524 3bf7194:3bf71a5'
PROBES = {'vec18': ('item.+1',), '+0xe8': ('item.+2',), '+0xc0': ('inner.+4', 'inner.+8'),
          '+0xd0': ('item.+0', 'item.+4'), '+0xd8': ('item.+0', 'item.+4')}


class Check(Exception):
    pass


def ck(ok, detail):
    if not ok:
        raise Check(detail)


def h(b):
    return sha256(b).hexdigest()


def read(p):
    return json.loads(p.read_bytes())


def hist(xs):
    return {str(k): v for k, v in sorted(Counter(xs).items())}


def bounds(spans):
    return [min(a for a, _ in spans), max(b for _, b in spans)] if spans else None


def decode(name, b, start, end, fields):
    """A bounded transfer cursor; records are [start,end,children]."""
    at = start
    items = []

    def v(label, w, signed=False):
        nonlocal at
        a = at
        at += w
        ck(at <= end, (name, a, 'short transfer', w, end))
        value = int.from_bytes(b[a:at], 'little', signed=signed)
        fields[label].append((a, w, value))
        return value

    def count(w, width, signed=False, label='count'):
        a = at
        n = v(label, w, signed)
        ck(0 <= n <= (end - at) // width, (name, a, 'invalid count', n, end))
        return n

    def lanes(prefix, widths):
        a = at
        for w in widths:
            v(f'{prefix}.+{at-a}', w)

    if name in ('+0xe8', '+0xc0', '+0xc8'):
        v('version' if name != '+0xc8' else 'tag', 4 if name == '+0xe8' else 1)
    n = {
        'vec18': lambda: count(4, 8, True), '+0xe8': lambda: count(4, 10), '+0xc0': lambda: count(4, 6),
        'vec30': lambda: count(4, 2), '+0x100': lambda: count(2, 5, True), '+0xc8': lambda: 4,
        '+0xd0': lambda: 1, '+0xd8': lambda: 1,
    }[name]()
    for _ in range(n):
        a = at
        children = []
        if name == 'vec18':
            tag = v('item.tag', 1, True)
            v('item.+1', 4); v('item.+5', 2); v('item.+7', 1)
            if tag >= 2:
                v('item.+8', 1)
        elif name == '+0xe8':
            tag = v('item.tag', 2, True)
            v('item.+2', 4); v('item.+6', 1); v('item.+7', 1)
            w = 2 if tag >= 2 else 1
            v('item.+8', w); v('item.tail0', 1)
            if tag >= 3:
                v('item.tail1', 1)
        elif name == '+0xc0':
            v('item.tag', 1); v('item.+1', 1)
            for _ in range(count(4, 12, label='inner_count')):
                c = at
                v('inner.tag', 1)
                for offset, w in ((1, 1), (2, 1), (3, 1), (4, 4), (8, 4)):
                    v(f'inner.+{offset}', w)
                children.append([c, at])
        else:
            widths = {'+0xc8': (1,)*6, '+0xd0': (4,4,1,1,4,1), '+0xd8': (4,4,1,1,4,1), '+0x100': (1,2,2), 'vec30': (2,)}[name]
            lanes('item', widths)
        items.append([a, at, children])
    ck(at == end, (name, start, 'collection endpoint', at, end))
    return n, items


def portrait(values):
    return dict(count=len(values), minimum=min(values), maximum=max(values), histogram=hist(values))


def join(b, points, ids):
    rev = {uid: i for i, uid in ids.items()}
    out = dict(live=0, all_ones=0, ordinal_hits=0, uid_hits=0, different_target=0, zero_live=0)
    for row, a, w, x in points:
        if x == 0xffffffff:
            out['all_ones'] += 1
            continue
        u, ordinal = ids.get(x), rev.get(x)
        out['live'] += 1; out['ordinal_hits'] += u is not None; out['uid_hits'] += ordinal is not None
        out['zero_live'] += x == 0
        clash = u is not None and ordinal is not None and ordinal != x
        out['different_target'] += clash
        point = dict(row=row, at=a, raw=b[a:a+w].hex(), value=x, ordinal_to_uid=u, uid_to_ordinal=ordinal)
        for k, yes in [('first_live', True), ('first_ordinal_miss', u is None), ('first_uid_miss', ordinal is None), ('first_different_target', clash)]:
            if yes:
                out.setdefault(k, point)
    return out


def evidence(frozen):
    import pefile
    import capstone as cs
    path = Path(frozen['source']['editor'])
    raw = path.read_bytes()
    digest = h(raw)
    ck(digest == frozen['source']['editor_sha256'], 'editor digest')
    p = pefile.PE(data=raw, fast_load=True)
    md = cs.Cs(cs.CS_ARCH_X86, cs.CS_MODE_64)
    md.detail = True
    base = p.OPTIONAL_HEADER.ImageBase
    ranges = []
    for pair in PE_RANGES.split():
        a, z = (int(v, 16) for v in pair.split(':'))
        va = base + p.get_rva_from_offset(a)
        code = []
        for i in md.disasm(raw[a:z], va):
            rec = [a + i.address-va, i.address, i.bytes.hex(), i.mnemonic, i.op_str]
            code.append(rec)
        ck(bool(code), (a, 'empty instruction range'))
        ranges.append(dict(range=[a,z], instructions=code))
    return dict(editor=path.as_posix(), sha256=digest, ranges=ranges)


def build():
    prev = runpy.run_path(str(ROOT/'scripts/t59_compmain_fields.py'))
    slots = read(T59/'field_slots.json')
    fmap = read(T59/'field_map.json')
    manifest={r['path']:r['sha256'] for r in read(ROOT/'evidence/MANIFEST.json')['files']}
    ck(all(h((ROOT/k).read_bytes())==v==manifest[k] for k,v in slots['frozen'].items()),'t59 frozen manifest')
    raw, arc = prev['archives']()
    ck(arc == slots['archives'], 't59 member evidence')
    runs = {s: prev['replay'](raw[s,25], slots['external_modes'][s]['mode']) for s in SIDES}
    keys, meta = prev['target_domains'](raw, {s: r[0] for s,r in runs.items()})
    ck(meta == slots['target_identity_domains'], 't59 target identity witnesses')
    # Full directory listing, no payload scan for unbound members.
    import os
    depot = Path(os.environ.get('FM24_DB_DIR', ROOT/'scratch/data'))
    entry_reader = runpy.run_path(str(ROOT.parent/'fm24/scripts/modding_read_dbdat.py'))['_entries']
    import zstandard as zstd
    directories = {}; extra = {}; extra_entries = {}
    for side in SIDES:
        _, archive, toc = entry_reader(depot/f'{side}_db.dat')
        ck(h(archive)==arc[side]['archive_sha256'], (side,'same archive'))
        entries = directories[side] = {e['path']: [34+e['offset'], e['packed_size'], e['size']] for e in toc['entries']}
        extra[side]={f'table_25.dat': raw[side,25]}; extra_entries[side]={}
        for name in ('table_23.dat',) + (('table_24.dat','table_extra_24.dat') if side=='server' else ()):
            full=f'{side}_db/{name}'; a,span,n=entries[full]; end=a+span
            bound=min((x for x,_,_ in entries.values() if x>a),default=toc['toc_offset'])
            ck(34<=a<end<=bound,(full,'range'))
            p=a; frames=[]; selected=[]
            while p<end:
                dz=zstd.ZstdDecompressor().decompressobj(); got=dz.decompress(archive[p:end]); q=end-len(dz.unused_data)
                ck(dz.eof and q>p,(full,'frame EOF')); frames.append([p,q,len(got)]); p=q
                if len(got)==n:
                    selected.append(got)
            ck(len(selected)==1,(full,'unique frame')); b,=selected
            extra[side][name]=b
            extra_entries[side][name]=dict(range=[a,end],bound=bound,frames=frames,payload_sha256=h(b),compressed_sha256=h(archive[a:end]))
    t39=runpy.run_path(str(ROOT/'scripts/t39_tchl_cursor.py'))
    domains,aux,_,_=t39['targets'](lambda n:(extra['server'][n],None),lambda n:(extra['client'][n],None))
    frozen_aux=read(ROOT/'scratch/t39/out/fields_tchl.json')['target_domains']
    ck(all(json.loads(json.dumps(domains[t]))==frozen_aux[str(t)] for t in (23,24)), 't39 target witnesses')
    for side in SIDES:
        keys[side,23]=aux[23]
    keys['server',24]=aux[24]
    static = evidence(slots)
    out = dict(status='partial', L4=0, scope='table_25.dat slot 19, inline physical grammar only',
               t59_input_sha256={name: h((T59/name).read_bytes()) for name in ('field_slots.json','field_map.json','REPORT.md')},
               t59_negatives=fmap['fixtures']['falsified_t01f'], mode_tests=slots['external_modes'],
               static=static, target_identity_domains={s:{str(t):meta[s][str(t)] for t in TARGETS} for s in SIDES},
               directory=directories, extra_identity_entries=extra_entries,
               extra_identity_domains={str(t):domains[t] for t in (23,24)},
               independent_member_binding=None, collections={})
    census = dict(format='t66/1', row_columns=['selector_at','identity_at','end_exclusive','UID'],
                  event_columns=['ordinal','presence_at_or_null','payload_at_or_null','end_exclusive_or_null','count_at_or_null','count_or_null','items'],
                  item_columns=['at','end_exclusive','child_spans'], axes='absolute uncompressed table_25.dat offsets; absent client event = mode skip',
                  identity_width=12, header_width=13, footer_width=9, envelopes=slots['envelopes'], sides={})
    for s, (rows, book, order) in runs.items():
        b = raw[s,25]
        e = slots['envelopes'][s]
        ck(h(b''.join(S.pack('<III', *x) for x in rows)) == e['row_trace_sha256'], (s,'row trace'))
        ck(dict(order) == {tuple(t['sequence']):t['rows'] for t in slots['execution_templates'][s]}, (s,'execution templates'))
        for d in slots['slots']:
            ck(json.loads(json.dumps(prev['describe'](b,book.get(d['key'],[]),rows))) == d['profiles'][s], (s,d['key'],'t59 coordinate/content digest'))
        try:
            prev['replay'](b, 1-slots['external_modes'][s]['mode'])
        except prev['Check'] as exc:
            ck(str(exc)==slots['external_modes'][s]['forced_opposite_first_failure'], (s,'opposite mode failure'))
        else:
            raise Check((s,'opposite mode closed'))
        census['sides'][s] = dict(rows=[[a,z-12,z,u] for a,z,u in rows], collections={})
    for name,(slot,flag,grammar) in SPEC.items():
        info=dict(slot=slot, presence_slot=flag, grammar=grammar, inline_member='table_25.dat',
                  grade=('held' if name in ('vec30','+0xa8','+0xe0') else 'L3'), grade_scope='physical item grammar only', sides={})
        out['collections'][name]=info
        for s, (rows,book,_) in runs.items():
            b=raw[s,25]
            spans={i:(a,a+w) for i,a,w in book.get(slot,[])}
            flags={i:a for i,a,w in book.get(flag,[])}
            events=[]; by_field=defaultdict(list)
            for i in sorted(spans.keys() | flags.keys()):
                a,z=spans.get(i,(None,None)); f=flags.get(i); n=None; items=[]; cnt_at=None
                if flag:
                    ck(f is not None and b[f] in (0,1) and bool(b[f])==(a is not None), (name,s,i,'presence'))
                    ck(a is None or a==f+1, (name,s,i,'presence/payload gap'))
                if a is not None:
                    fields=defaultdict(list)
                    ck(rows[i][0]<a<z<=rows[i][1]-12, (name,s,i,'crossed identity'))
                    n,items=decode(name,b,a,z,fields)
                    if 'count' in fields:
                        cnt_at=fields['count'][0][0]
                    for lane, vals in fields.items():
                        by_field[lane].extend((i,*x) for x in vals)
                events.append([i,f,a,z,cnt_at,n,items])
            census['sides'][s]['collections'][name]=events
            nonempty=[i for i,_,_,_,_,n,_ in events if n]
            items=[it for *_, arr in events for it in arr]
            children=[x for _,_,ch in items for x in ch]
            fields={k:portrait([p[3] for p in v]) for k,v in by_field.items()}
            # Real data domains constrain observed grammar revisions only; no business enum inferred.
            for k,v in fields.items():
                tag_expect={('vec18','item.tag'):2,('+0xe8','version'):2,('+0xe8','item.tag'):3,
                            ('+0xc0','version'):1,('+0xc0','item.tag'):1,('+0xc0','inner.tag'):1,
                            ('+0xc8','tag'):1,('+0xc8','item.+0'):1,('vec30','count'):0}.get((name,k))
                if tag_expect is not None:
                    for i,a,w,value in by_field[k]:
                        ck(value==tag_expect, (s,name,k,i,a,b[a:a+w].hex(),'unexpected observed revision/count'))
            ref_targets={'vec18':{'item.+1':24},'+0xd0':{'item.+0':23,'item.+4':23},'+0xd8':{'item.+0':23,'item.+4':23}}.get(name,{})
            probe={k:{str(t):join(b,by_field[k],keys[s,t]) for t in TARGETS} for k in PROBES.get(name,()) if k in by_field}
            for lane,t in ref_targets.items():
                if lane in by_field:
                    probe[lane][str(t)]=join(b,by_field[lane],keys[s,t])
            if s=='server':
                info['reference_lanes']={}
                for lane in probe:
                    if lane in ref_targets:
                        t=ref_targets[lane]; jn=probe[lane][str(t)]
                        grade='L3' if jn['live'] and jn['ordinal_hits']==jn['live'] else 'held'
                        a,w,x=by_field[lane][0][1:]
                        ev=jn.get('first_ordinal_miss',dict(row=by_field[lane][0][0],at=a,raw=b[a:a+w].hex(),value=x))
                        info['reference_lanes'][lane]=dict(target_table=t,encoding='ordinal; 0xffffffff null',grade=grade,
                            first_counterexample=None if grade=='L3' else ev)
                    else:
                        i,a,w,x=next((p for p in by_field[lane] if p[3]!=0xffffffff),by_field[lane][0])
                        info['reference_lanes'][lane]=dict(target_table=None,grade='held',
                            reason='all 0xffffffff; no live target witness' if name=='+0xe8' else 'overlapping ordinal domains, no resolved target',
                            first_counterexample=dict(row=i,at=a,raw=b[a:a+w].hex(),value=x))
            info['sides'][s]=dict(parent_rows=len(rows), mode_skipped_rows=len(rows) if not events else 0,
                events=len(events), payload_rows=len(spans), nonempty_ordinals=nonempty,
                presence_histogram=hist(b[a] for a in flags.values()), presence_bounds=bounds([(a,a+1) for a in flags.values()]),
                payload_bounds=bounds(list(spans.values())), item_bounds=bounds([(a,z) for a,z,_ in items]),
                count_histogram=hist(n for *_,n,_ in events if n is not None), item_width_histogram=hist(z-a for a,z,_ in items),
                items=len(items), inner_items=len(children), inner_bounds=bounds(children), fields=fields, ordinal_probes=probe)
        if info['grade']=='held':
            i,f,a,z,_,_,_=census['sides']['server']['collections'][name][0]
            a,z=(f,f+1) if f is not None else (a,z)
            info['first_counterexample']=dict(row=i, at=a, raw=raw['server',25][a:z].hex(), reason='no non-empty item observation')
    out['L3_grammars']=sum(x['grade']=='L3' for x in out['collections'].values())
    out['L3_reference_lanes']=sum(lane['grade']=='L3' for x in out['collections'].values() for lane in x['reference_lanes'].values())
    OUT.mkdir(parents=True,exist_ok=True)
    for name,obj in [('collections',out),('census',census)]:
        path=OUT/f'{name}.json'
        if name=='census':
            text=json.dumps(obj,ensure_ascii=False,separators=(',',':'))
            # Compact records but keep a line per row/event for tooling and diffs.
            text=text.replace('],[','],\n[')
        else:
            text=json.dumps(obj,ensure_ascii=False,indent=2)
        path.write_text(text+'\n',encoding='utf-8',newline='\n')
    print(f"PASS build: 2 x 7047 mother rows; {out['L3_grammars']} inline grammars; {out['L3_reference_lanes']} typed reference lanes; no independent member grade")


def selftest():
    for tag in (-1,1,2,3):
        for name in ('vec18','+0xe8'):
            if name=='vec18':
                b=S.pack('<ib',1,tag)+bytes(7+(tag>=2))
            else:
                b=S.pack('<IIh',2,1,tag)+bytes(8+(tag>=2)+(tag>=3))
            ck(decode(name,b,0,len(b),defaultdict(list))[0]==1,'tag branches')
            try:
                decode(name,b,0,len(b)-1,defaultdict(list))
            except Check:
                pass
            else:
                raise Check('truncated item accepted')
    print('PASS selftest: tag widths and short transfers')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    mode=ap.add_mutually_exclusive_group()
    mode.add_argument('--build',action='store_true',help='rebuild JSON (default)')
    mode.add_argument('--selftest',action='store_true',help='run synthetic bounded cursor checks')
    args=ap.parse_args()
    try:
        selftest() if args.selftest else build()
    except Check as exc:
        print(f'FAIL: {exc}',file=sys.stderr); return 1
    except Exception as exc:
        if exc.__class__.__name__=='Check':
            print(f'FAIL: {exc}',file=sys.stderr); return 1
        print(f'FATAL: {exc}',file=sys.stderr); return 2
    return 0


if __name__=='__main__':
    sys.exit(main())
