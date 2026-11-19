#!/usr/bin/env python3
"""Verify t28 without loading its builder: archive, x64 evidence, schema and all rows."""
from __future__ import annotations

import argparse
from calendar import isleap
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import struct
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
EDITOR_HASH = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
PAYLOAD_HASH = '7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34'
FOOT = b'\x00\x00\x00\x00\x01\xec\x7a\xe4\x04'
# Independently recorded join witnesses, in wire order: field, item offset, width,
# item member displacement, native read, getter dispatch witness, member access.
LANG = [('lang',0,4,0,0x3d8771f,0x3da29ef,0x3da29f7),('perc',4,1,8,0x3d87742,0x3da29e7,0x3da2a0c)]
FOREIGN = [('nfrn',0,4,0,0x448faaf,0x448fd30,0x15cfa72),('nfrc',4,4,8,0x448facf,0x448fd60,0x15cfa4d),
           ('fren',8,4,16,0x448faeb,0x15cf988,0x15cf994),('nfrr',12,4,24,0x448fb07,0x448fdc0,0x15cfa96),
           ('nfra',16,4,32,0x448fb23,0x448fdf0,0x15cf950),('stdt',20,4,40,0x39dd7d4,0x15cf9a6,0x15cf9d7),
           ('endt',24,4,44,0x39dd7d4,0x15cf97c,0x15cfb22)]
AGREEMENTS = [('NGag',0,4,0,0x3d88320,0x3da09cb,0x3da09d7),('NGsd',4,4,8,0x3d88345,0x3da09b7,0x3da09f3),
              ('NGed',8,4,12,0x3d8838c,0x3da09bf,0x3da0a92)]
SPECS = {'A':('Nlns',0x48,5,0x1040717,0x104075b,0x1042216,LANG),
         'B':('Nefr',0xa8,28,0x10407b0,0x1040829,0x1042047,FOREIGN),
         'C':('Nnfr',0x90,28,0x104086c,0x10408eb,0x104222e,FOREIGN),
         'D':('Nagr',0xc0,12,0x1040927,0x10409a7,0x10426c4,AGREEMENTS)}
TARGETS = {'continent':(5,7),'language':(8,126),'nation':(10,251),'region':(19,28),'currency':(41,173),'agreement':(56,6)}
CT_EXPR = ('24','25+5*A','29+5*A+28*B','33+5*A+28*B+28*C')
IT_EXPR = ('25','29+5*A','33+5*A+28*B','37+5*A+28*B+28*C')


class Fail(Exception):
    pass


def demand(ok, what):
    if not ok:
        raise Fail(what)


def digest(b):
    return sha256(b).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def framed(raw):
    """Independent cursor arithmetic on raw member, not based on emitted rows."""
    demand(len(raw)>=22 and raw[:8]==bytes.fromhex('03017461642ef10d') and raw[12]==0,'header')
    n, = struct.unpack_from('<I',raw,8)
    p = 13
    body_limit = len(raw)-len(FOOT)
    seen = set()
    rows = []
    for i in range(n):
        sel = p
        demand(p<body_limit and raw[p]==0,f'row {i} selector')
        p += 1
        start = p
        p += 24
        ns, count_pos, item_pos = {}, {}, {}
        for key, width, stride in (('A',1,5),('B',4,28),('C',4,28),('D',4,12)):
            demand(p+width<=body_limit,f'row {i}/{key} short count')
            count_pos[key] = p
            num = int.from_bytes(raw[p:p+width],'little',signed=True)
            p += width
            demand(0<=num<=(body_limit-p)//stride,f'row {i}/{key} count out of bounds')
            item_pos[key], ns[key] = p, num
            p += num*stride
        demand(p+12<=body_limit,f'row {i} identity short')
        ordinal, duni, duplicate = struct.unpack_from('<3I',raw,p)
        demand(ordinal==i and duni==duplicate and duni not in seen,f'row {i} identity mismatch')
        seen.add(duni)
        rows.append({'row':i,'selector_at':sel,'body_start':start,'end_before_next_selector':p+12,
                     'counts':ns,'count_at':count_pos,'items_at':item_pos,'identity_at':p,
                     'identity':[ordinal,duni,duplicate],'body_sha256':digest(raw[start:p+12]),
                     'transfer_count':14+2*ns['A']+7*(ns['B']+ns['C'])+3*ns['D']})
        p += 12
    demand(p==body_limit and raw[p:]==FOOT,'footer / EOF')
    return rows


def check_profile(p, records, schema):
    values = [int.from_bytes(x[3],'little') for x in records]
    h = Counter(values)
    demand((p['n'],p['distinct'],p['min'],p['max'])==(len(values),len(h),min(h),max(h)),f'{schema["field"]} profile bounds')
    demand(p['histogram']==[[v,n] for v,n in sorted(h.items())],f'{schema["field"]} histogram')
    wanted = [list(records[i][:3])+[records[i][3].hex()] for i in sorted({0,len(records)//2,len(records)-1})]
    demand(p['samples']==wanted,f'{schema["field"]} held-out coordinates / bytes')
    kind = schema['type']
    if kind=='database_record_unique_id':
        target = schema['database_table_type']
        tid,n = TARGETS[target]
        live = [v for v in values if v!=0xffffffff]
        demand(all(0<=v<n for v in live),'ordinal range')
        demand(schema.get('is_optional')=='true' or len(live)==len(values),'required ref null')
        demand((p['target'],p['target_table_id'],p['ordinal_domain'],p['null_count'],p['live_bounds'])==
               (target,tid,[0,n-1],len(values)-len(live),[min(live),max(live)] if live else None),'typed ref profile')
    elif kind=='integer':
        bound = [int(schema[x]) for x in ('min_value','max_value')]
        demand(p['schema_bounds']==bound and all(bound[0]<=v<=bound[1] for v in values),'integer profile')
    elif kind=='date':
        parts = [(v//65536, v%512, (v//512)%128) for v in values]
        demand(all(1<=y<=9999 and 1<=d<=365+isleap(y) for y,d,_ in parts),'packed date domain')
        demand(p['years']==[list(x) for x in sorted(Counter(y for y,_,_ in parts).items())] and
               p['day_range']==[min(d for _,d,_ in parts),max(d for _,d,_ in parts)] and
               p['intraday_codes']==sorted({t for _,_,t in parts}) and p['default_1900_001']==h[124518401],'date profile')
    else:
        raise Fail('unexpected promoted type')
    demand(p['matches']==len(records) and p['violations']==[],'profile did not pass')


def check_static(c, out, editor, fields, rows):
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from t05_pe import PE
    from t21b_control_flow import ReaderCFG
    pe = PE(editor)
    demand(digest(pe.raw)==c['provenance']['editor_sha256']==EDITOR_HASH,'editor hash')
    md = Cs(CS_ARCH_X86,CS_MODE_64)
    md.detail = True
    pe.pe.parse_data_directories(directories=[3])
    assembled = {}
    for key in ('instruction','branch'):
        by_site = {}
        for part in c[key+'_shards']:
            path = out/part['file']
            demand(digest(path.read_bytes())==part['sha256'],f'shard hash {path.name}')
            objs = read_json(path)
            demand(len(objs)==part['records'],f'shard records {path.name}')
            for x in objs:
                off = x['file_offset' if key=='instruction' else 'site']
                demand(off not in by_site,'duplicate evidence site')
                by_site[off] = x
        assembled[key] = by_site
    ins = {}
    for off,x in assembled['instruction'].items():
        va = pe.f2va(off)
        demand(x['VA']==va and pe.va2f(va)==off,f'PE displacement {off:#x}')
        i = next(md.disasm(pe.raw[off:off+15],va,count=1))
        demand(i.bytes.hex()==x['bytes'] and (i.mnemonic+' '+i.op_str).rstrip()==x['instruction'],f'bytes/disassembly {off:#x}')
        ins[off] = i
    vm = pe.va2f(0x1418893b8)
    for slot,file in [(2,0x1041f30),(19,0x103fac0)]:
        demand(pe.va2f(struct.unpack_from('<Q',pe.raw,vm+8*slot)[0])==file,'NATION vtable')
    local = {}
    for fn in c['cfg']:
        entry = fn['file_offset']
        g = ReaderCFG(pe,md,entry)
        demand(fn['va']==g.start_va and fn['end_exclusive']==g.function_end_off and fn['external_edges']==g.external_edges,'function extent')
        pcs = set()
        for bb in fn['blocks']:
            mids = bb['instructions']
            demand(mids[0]==bb['start'] and not pcs.intersection(mids),'basic block overlap')
            pcs.update(mids)
            for a,b in zip(mids,mids[1:]):
                demand(g.successors[pe.f2va(a)]==[pe.f2va(b)],f'intra-block edge {a:#x}')
            demand(bb['successors']==[pe.va2f(x) for x in g.successors[pe.f2va(mids[-1])]],'CFG exit edge')
        demand(pcs=={pe.va2f(k) for k in g.instructions} and pcs<=ins.keys(),'incomplete CFG')
        local.update({pc:entry for pc in pcs})
    br = assembled['branch']
    demand(set(br)=={pc for pc in local if ins[pc].mnemonic.startswith('j') and ins[pc].mnemonic!='jmp'},'branch census')
    for pc,b in br.items():
        i = ins[pc]
        demand(b['function']==local[pc] and b['taken']==pe.va2f(i.operands[0].imm) and b['not_taken']==pc+i.size,
               f'predicate successors {pc:#x}')
        demand(b['class'] in ('dead','wire_data','runtime_external','unresolved'),'branch classification')
        if b['class'] in ('dead','unresolved'):
            demand(b['observed_taken']==0 and (b['class']=='dead' or b['observed_not_taken']==0),'nonmodeled edge executed')
        if b['predicate'] is not None:
            demand(ins[b['predicate']].eflags and local[b['predicate']]==local[pc],'flag producer not local')
    for pc, jump in [(0x103fae6,True),(0x10409d3,True),(0x3c60131,True),(0x104092e,True)]:
        demand((br[pc]['observed_taken'],br[pc]['observed_not_taken'])==((251,0) if jump else (0,251)),'mode/identity profile')
    demand(br[0x103fae6]['class']==br[0x10409d3]['class']=='runtime_external' and
           '[rsp + 0x120]' in ins[br[0x10409d3]['predicate']].op_str,'external mode not a wire selector')
    for pc in (0x39dd7bc,0x3d8832f,0x3d88373):
        demand(br[pc]['class']=='dead' and '+ 0x10]' in ins[br[pc]['taken']].op_str,'null-stream invalid edge')
    actual_calls = [a for a in sorted(local) if local[a]==0x103fac0 and ins[a].mnemonic=='call' and ins[a].op_str.endswith('+ 0x28]')]
    demand(len(actual_calls)==40 and [t['site'] for t in c['calls_24_39']]==actual_calls[23:], '40-call census')
    demand([x['width'] for x in c['calls_24_39'][5:]]==[4]*10+[2,1] and
           all(x['ordinary_row_offset'] is None for x in c['calls_24_39'][5:]), 'excluded post-D 43B')
    for t in c['transfer_table']:
        demand(ins[t['native_site']].op_str.endswith(' + 0x28]'),'read slot mismatch')
        demand(any(ins[a].mnemonic=='mov' and ins[a].op_str.startswith('r8d, ')
                   and ins[a].operands[1].type==2 and ins[a].operands[1].imm==t['width']
                   for a in t['setup']), 'missing width setup')
    for t in c['getter_jump_table_cells']:
        off = t['file_offset']
        d, = struct.unpack_from('<i',pe.raw,off)
        demand(off==0x15cfca8+4*(int.from_bytes(t['code'].encode(),'big')-0x6e667261) and pe.f2va(off)==t['VA'] and
               pe.raw[off:off+4].hex()==t['bytes'] and pe.va2f(pe.f2va(0x15cfca8)+d)==t['target'],'child jump table')
    for k,(parent, obj, stride, count, item, cmp, evidence) in SPECS.items():
        x = c['collections'][k]
        y = fields[None,parent]
        demand((x['parent'],x['object_off'],x['wire_stride'],x['count']['site'],x['item_call'])==(parent,obj,stride,count,item),'collection join')
        demand(ins[cmp].op_str.endswith(hex(int.from_bytes(parent.encode(),'big'))) and cmp in y['getter_chain'],'parent 4CC')
        for site,target in [(item,x['item_thunk']),(x['item_thunk'],x['item_body'])]:
            demand(pe.va2f(ins[site].operands[0].imm)==target,'item call/thunk target')
        total = sum(r['counts'][k] for r in rows)
        nonempty = sum(r['counts'][k]>0 for r in rows)
        for site, takes, falls in [(x['gate'],len(rows)-nonempty,nonempty),(x['loop_backedge'],total-nonempty,nonempty)]:
            demand((br[site]['class'],br[site]['observed_taken'],br[site]['observed_not_taken'])==('wire_data',takes,falls),'count control replay')
        demand(len(x['item_transfers'])==len(evidence),'item transfer census')
        for transfer,(code,off,width,mem,ns,tag,access) in zip(x['item_transfers'],evidence,strict=True):
            f = fields[parent,code]
            demand((transfer['scoped_field'],transfer['item_offset'],transfer['width'],transfer['object_off'],transfer['native_site'])==
                   (f'{parent}/{code}',off,width,mem,ns),'child transfer coordinates')
            demand((f['item_offset'],f['width'],f['object_off'])==(off,width,mem) and ns in f['reader_sites'],'ledger coordinates')
            demand(ins[tag].op_str.endswith(hex(int.from_bytes(code.encode(),'big'))) and {tag,access}<=set(f['getter_chain']),'scoped child 4CC arm')
            demand(ins[access].operands[1].mem.disp==mem,'getter object offset')
    demand(ins[0x3d75dc7].op_str=='ecx, 0x90' and ins[0x3d75d99].op_str=='r14d, 0xa8' and
           ins[0x3d75dcc].op_str=='rcx, r14' and ins[0x3d75dcc].mnemonic=='cmove' and
           ins[0x1042057].op_str=='byte ptr [rbp + 0x20], 0' and
           ins[0x104223e].op_str=='byte ptr [rbp + 0x20], 1','same-type B/C disambiguation')
    count_a_one = sum(r['counts']['A']==1 for r in rows)
    norm = br[0x104078d]
    demand((norm['observed_not_taken'],norm['observed_taken'])==(count_a_one,251-count_a_one)
           and ins[0x104078f].op_str=='byte ptr [rax + 8], 0x64','A single-item postprocessing')
    for site,reg,off in [(0x1040724,'r14',0x48),(0x10407bd,'r14',0xa8),(0x1040879,'r14',0x90),
                         (0x1040967,'r14',0xc0),(0x104349d,'r12',0x48),(0x3d765a3,'rax',0xc0)]:
        op = ins[site].operands[1]
        demand(op.type==3 and md.reg_name(op.mem.base)==reg and op.mem.disp==off,'parent reader/getter object bridge')
    for site in (0x448fb33,0x448fb4d):
        demand(pe.va2f(ins[site].operands[0].imm)==0xdb7f80 and pe.va2f(ins[0xdb7f80].operands[0].imm)==0x39dd7b0,
               'both date-helper sites reach native date reader')
    for t in fields.values():
        demand(all(x in ins for x in t['getter_chain']+t.get('reader_sites',[])),'ledger evidence reference')
    return len(ins),len(br)


def replay(out, editor, data):
    sys.path.insert(0,str(ROOT/'scripts'))
    os.environ['FM24_DB_DIR'] = str(data)
    import fm24_dump as dat
    packed = (data/'client_db.dat').read_bytes()
    codec = dat._reader()
    index = {e['table_id']:e for e in codec['list_tables'](data/'client_db.dat','client_db.dat') if e['entry_type']=='table'}
    c = read_json(out/'cursor_nation_tail.json')
    f = read_json(out/'fields_nation_client.json')
    demand(digest(packed)==c['provenance']['archive_sha256'],'archive revision')
    for label,(tid,n) in TARGETS.items():
        block = dat.load_payload(codec,'client',tid)
        meta = c['provenance']['referenced_members'][label]
        demand((index[tid]['record_count_header'],struct.unpack_from('<I',block,8)[0],meta['count'])==(n,n,n),'referent header')
        demand(meta['sha256']==digest(block) and meta['bytes']==index[tid]['size']==len(block),'member digest/size')
        if tid==10:
            raw = block
    demand(digest(raw)==PAYLOAD_HASH,'nation member revision')
    rows = framed(raw)
    demand(len(rows)==251 and rows==c['rows'],'all row coordinates and hashes')
    demand(rows[55]['identity_at']==0x1042 and rows[55]['identity']==[55,110,110],'row 55 holdout')
    demand(rows[-1]['end_before_next_selector']==24723 and len(raw)==24732 and c['closure']['physical_footer_hex']==FOOT.hex(),'closure')
    demand(struct.unpack_from('<3I',raw,rows[0]['identity_at']+43)!=(0,5,5),'forced mode tail counterexample')
    master = read_json(ROOT/MASTER)['entities']['nation.xml'][0]['fields']
    manifest = {x['path']:x['sha256'] for x in read_json(ROOT/'evidence/MANIFEST.json')['files']}
    for file in MASTER,PROV:
        demand(digest((ROOT/file).read_bytes())==manifest[file]==c['provenance']['snapshot_manifest'][file],'frozen snapshot hash')
    demand(f['schema_sha256']==manifest[MASTER] and EDITOR_HASH in (ROOT/PROV).read_text(encoding='utf-8'),'schema and editor provenance')
    direct = {x['field']:x for x in master if x.get('is_client_field')=='true'}
    schema = {(None,code):x for code,x in direct.items()} | {(code,y['field']):y for code,x in direct.items() for y in x.get('list_item_fields',[])}
    fields = {(x['parent'],x['code']):x for x in f['fields']}
    demand(len(f['fields'])==len(fields)==len(schema)==49 and len(direct)==21 and set(fields)==set(schema),'49-field inventory')
    demand(all(x['name']==schema[k]['name'] and x['type']==schema[k]['type'] for k,x in fields.items()),'schema ledger columns')
    need_l3 = {(None,p) for p in ('Ncti','Ncur',*(s[0] for s in SPECS.values()))}
    for i,(k,(parent,obj,stride,_,_,_,items)) in enumerate(SPECS.items()):
        counts = Counter(r['counts'][k] for r in rows)
        total = sum(v*n for v,n in counts.items())
        demand(total==[492,214,63,162][i] and max(counts)==[7,40,21,2][i],'collection cardinality')
        px = fields[None,parent]
        cp = {'rows':251,'min':min(counts),'max':max(counts),'total':total,'histogram':[[v,n] for v,n in sorted(counts.items())]}
        demand(px['profile']==c['collections'][k]['count']['profile']==cp and px['row_offset']==CT_EXPR[i], 'count coordinates/profile')
        for code,off,width,*_ in items:
            need_l3.add((parent,code))
            x = fields[parent,code]
            demand(x['row_offset']==f'{IT_EXPR[i]}+{stride}*j+{off}','symbolic child row coordinate')
            records = [(r['row'],j,p,raw[p:p+width]) for r in rows for j in range(r['counts'][k])
                       for p in [r['items_at'][k]+stride*j+off]]
            check_profile(x['profile'],records,schema[parent,code])
        if k in 'BC':
            demand(all(sum(s!=0xffffffff for s in struct.unpack_from('<5I',raw,r['items_at'][k]+28*j))==1
                       for r in rows for j in range(r['counts'][k])),'reference-field dependency')
    normal = fields['Nlns','perc']['post_read_normalization']
    single = Counter(raw[r['items_at']['A']+4] for r in rows if r['counts']['A']==1)
    demand(normal=={'branch':0x104078d,'store':0x104078f,'wire_histogram_for_single_item_rows':[[v,n] for v,n in sorted(single.items())],
                    'rows_with_single_item':91,'rows_with_changed_object_value':17,'stored_object_value':100}
           and sum(single.values())==91 and single[100]==74,'single-language raw/object difference')
    for code,offset,member in [('Ncti',1,0xf0),('Ncur',13,0x100)]:
        x = fields[None,code]
        demand((x['row_offset'],x['width'],x['object_off'])==(offset,4,member),'inherited coordinates')
        records = [(r['row'],None,p,raw[p:p+4]) for r in rows for p in [r['body_start']+offset]]
        check_profile(x['profile'],records,schema[None,code])
    demand({k for k,x in fields.items() if x['grade']=='L3'}==need_l3,'promotion set')
    demand(f['summary']=={'direct':{'L3':6,'candidate':6,'unresolved':9},'nested':{'L3':19,'unresolved':9},'new_L3':23,'L4':0},'grade summary')
    demand(all(x['grade']=='L3' or x['row_offset'] is None for x in fields.values()),'unproven coordinate')
    neg = f['t01g_negative_unchanged']
    src = ROOT/'scratch/t01/inbox/t01g/output.json'
    original = read_json(src)
    demand(digest(src.read_bytes())==neg['sha256'] and all(neg[k]==original[k] for k in ('negative_result','falsified_or_rejected')),'t01g negative control')
    ni,nb = check_static(c,out,editor,fields,rows)
    print(f't28 verify: PASS — 251 rows / 931 items / 25 L3 (23 new), {ni} instructions, {nb} branches')


def selftest():
    header = bytes.fromhex('03017461642ef10d0100000000')
    a_count = b'\x01'
    a_item = struct.pack('<IB',7,95)
    raw = header+b'\0'*25+a_count+a_item+b'\0'*12+struct.pack('<III',0,5,5)+FOOT
    r, = framed(raw)
    demand((r['items_at']['A'],r['identity_at'],r['end_before_next_selector'])==(39,56,68),'synthetic row')
    for bad in [raw[:-1],raw[:13]+b'\x01'+raw[14:],raw[:38]+b'\xff'+raw[39:],raw[:64]+b'\xff'+raw[65:]]:
        try:
            framed(bad)
        except Fail:
            continue
        raise Fail('malformed fixture accepted')
    print('t28 verifier selftest: OK')


def main():
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument('--selftest',action='store_true')
    a.add_argument('--out-dir',type=Path,default=HERE)
    a.add_argument('--editor',type=Path,default=ROOT.parent/'fm24/input/editor.exe')
    a.add_argument('--data-dir',type=Path,default=Path('D:/tmp2b/fm24-db/scratch/data'))
    x = a.parse_args()
    try:
        selftest() if x.selftest else replay(x.out_dir,x.editor,x.data_dir)
        return 0
    except Fail as exc:
        print(f'FAIL: {exc}',file=sys.stderr)
        return 1
    except Exception as exc:
        print(f'ERROR: {type(exc).__name__}: {exc}',file=sys.stderr)
        return 2


if __name__=='__main__':
    sys.exit(main())
