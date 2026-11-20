#!/usr/bin/env python3
"""Independently check t24 against the decoded member and read-only editor.exe."""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import struct
import sys

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
EXE = Path('<OLD_REPO>/input/editor.exe')


class Failure(Exception):
    pass


def require(ok, why):
    if not ok:
        raise Failure(why)


def load(name):
    return json.loads((OUT / name).read_text(encoding='utf-8'))


def unpack(fmt, data, off):
    return struct.unpack_from('<'+fmt, data, off)


def grammar(data):
    kind, rev, signature, ver, nrows, meta = unpack('BB4sHIB', data, 0)
    require((kind, rev, signature) == (3,1,b'tad.') and ver >= 0xdc4, 'header grammar')
    start = 13
    for ordinal in range(nrows):
        selector = data[start]
        require(selector in (0,12), f'{ordinal}: selector domain')
        prefix = 5 * (selector == 12)
        body = start+1
        if prefix:
            require(unpack('IB', data, body) == (0xffffffff,0), f'{ordinal}: derived compact prefix')
        lengths = body+prefix+26
        n, = unpack('I', data, lengths)
        name = lengths+4
        short_len = name+n
        m, = unpack('I', data, short_len)
        short = short_len+4
        tail = short+m
        v, b8, b9, ident, uid, duplicate = unpack('BBBIII', data, tail)
        require((v,b8,b9)==(0,0,0) and ident==ordinal and uid==duplicate, f'{ordinal}: base-object suffix')
        data[name:short_len].decode('utf-8')
        data[short:tail].decode('utf-8')
        stop = tail+15
        require(stop-start==50+prefix+n+m, f'{ordinal}: row_length')
        yield [ordinal,body,selector,stop,n,m,uid]
        start = stop
    fcount, fflag, word = unpack('IBI', data, start)
    require(start+9==len(data) and (fcount,fflag)==(0,1), 'footer grammar')


def selftest():
    row = struct.pack('<B5I6BI1sI3sBBBIII',0,0,1,2,3,4,*([0]*6),1,b'a',3,b'bbb',0,0,0,0,101,101)
    raw = struct.pack('<BB4sHIB',3,1,b'tad.',0xdf1,1,0) + row + struct.pack('<IBI',0,1,101)
    require(list(grammar(raw))==[[0,14,0,67,1,3,101]], 'fixture coordinates')
    # Put a derived row first to defeat any ordinal-based discriminator.
    raw2 = raw[:13] + b'\x0c' + b'\xff'*4 + b'\0' + raw[14:]
    require(list(grammar(raw2))==[[0,14,12,72,1,3,101]], 'derived-first fixture')
    for bad in [raw[:13]+b'\xff'+raw[14:],raw[:-1],raw[:62]+b'\x05'+raw[63:]]:
        try:
            list(grammar(bad))
        except (Failure, struct.error, UnicodeError):
            continue
        raise Failure('invalid fixture accepted')
    print('t24 independent verifier selftest: OK')


def instructions(pe, manifest):
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    def dis(raw_record):
        off = int(raw_record['file_offset'],16)
        va = int(raw_record['VA'],16)
        data = bytes.fromhex(raw_record['bytes'])
        require(pe.va2f(va)==off and pe.f2va(off)==va, f'{off:#x}: PE mapping')
        require(pe.raw[off:off+len(data)]==data, f'{off:#x}: editor.exe bytes')
        return next(md.disasm(data,va,count=1),None)
    inst = {}
    for p in manifest['instruction_shards']:
        for x in load(p)['instructions']:
            i = dis(x)
            require(i is not None and f'{i.mnemonic} {i.op_str}'.rstrip()==x['instruction'], f'{x["file_offset"]}: decode')
            require(x['file_offset'] not in inst, 'duplicate instruction evidence')
            inst[x['file_offset']]=i
    for site, x in manifest['transfer_sites'].items():
        i = dis(x)
        require(i.mnemonic=='call' and i.operands[0].type==3 and i.operands[0].mem.disp==0x28,
                f'{site}: not stream slot +0x28')
        require(all(p in inst for p in x['setup']), f'{site}: missing transfer proof')
    classproof = manifest['class_selector']
    require(all(x in inst for x in classproof['instruction_sites']), 'selector references')
    require(inst['0xf2ba02'].op_str=='r8d, 1' and inst['0xf2ba1b'].op_str=='edx, byte ptr [rsp + 0x43]' and
            inst['0xf48daf'].op_str=='bl, 0xc', 'factory selector chain')
    jt = classproof['jump_table_3']
    off = int(jt['file_offset'],16)
    rel, = unpack('i',pe.raw,off)
    require(pe.f2va(off)==int(jt['VA'],16) and pe.raw[off:off+4].hex(' ')==jt['bytes'] and
            pe.va2f(pe.f2va(off-3*4)+rel)==0xf48daf, 'factory case 3 jump table')
    branch_rows = [r for name in manifest['branches']['shards'] for r in load(name)['branches']]
    require(Counter(r['class'] for r in branch_rows)=={'CLUB':167,'LEAGUE_BODY_CLUB':3}, 'CFG coverage')
    require(all(r['file_offset'] in inst for r in branch_rows), 'CFG evidence references')
    return inst


def check_vslots(pe, slots, expected=None):
    for v in slots:
        off = int(v['file_offset'],16)
        data=bytes.fromhex(v['bytes'])
        require(pe.f2va(off)==int(v['VA'],16) and pe.raw[off:off+len(data)]==data, 'vtable slot')
        dst = pe.va2f(int.from_bytes(data,'little'))
        require(dst==int(v['target'],16) and (expected is None or dst in expected), 'vtable target')


def sample_fields(raw, rows, pe, inst, summary):
    ledger = load('fields_club.json')
    entries = [x for name in ledger['shards'] for x in load(name)['fields']]
    require(len(entries)==433, 'schema inventory size')
    fields = [x for x in entries if x['grade']=='L3_row_instruction']
    require(len(fields)==ledger['main_L3']==len({x['code'] for x in fields}), 'field promotion cardinality')
    # Explicit independent wire coordinates for promoted fields.
    expected = {'Cnti':(0,4,0xd8), 'Cbni':(8,4,0xe8), 'Cccn':(12,4,0xf0),
                'Ccty':(16,4,0xf8), 'Csot':(20,1,0x160), 'CASt':(21,1,0x161), 'CnCV':(23,1,0x163),
                'Csnm':(34,'M',0xc8), 'PLgn':(36,1,0xb9), 'duni':(41,4,0xc)}
    require({f['code'] for f in fields}==expected.keys(), 'unexpected set of promoted fields')
    def coords(row, code):
        ordinal, body, selector, stop, n, m, uid = row
        initial, width, obj = expected[code]
        off = initial + (5 if selector==12 else 0) + (n if code in ('Csnm','PLgn','duni') else 0) + (m if code in ('PLgn','duni') else 0)
        return off, m if width=='M' else width, obj
    for fld in fields:
        code = fld['code']
        require(all(o in inst for o in fld['getter_sites']), f'{code}: getter not documented')
        imm = int.from_bytes(code.encode(),'big')
        require(any(i.mnemonic=='cmp' and any(o.type==2 and o.imm==imm for o in i.operands)
                    for i in (inst[o] for o in fld['getter_sites'])), f'{code}: no code comparator')
        check_vslots(pe, fld.get('vtable_slots',[]))
        site = summary['transfer_sites'][fld['file_offset']]
        require(fld['VA']==site['VA'] and fld['bytes']==site['bytes'], f'{code}: transfer mismatch')
        for sample in fld['samples']:
            row = rows[sample['ordinal']]
            off, w, obj = coords(row, code)
            abs_off = row[1]+off
            require((w,off,abs_off,obj)==(sample['width'],sample['row_offset'],sample['member_offset'],fld['object_off']) and
                    raw[abs_off:abs_off+w]==bytes.fromhex(sample['data_bytes']), f'{code}: field byte replay')
        counts = {'CLUB':Counter(),'LEAGUE_BODY_CLUB':Counter()}
        for row in rows:
            off,w,_ = coords(row,code)
            counts['CLUB' if row[2]==0 else 'LEAGUE_BODY_CLUB'][raw[row[1]+off:row[1]+off+w]]+=1
        for cls, col in counts.items():
            want = fld['validation'][cls]
            require(len(col)==want['distinct_wire_values'] and col.total()==want['rows'] and
                    all(col[bytes.fromhex(b)]==n for b,n in want['most_common_hex']), f'{code}: column validation')
    return len(fields)


def verify():
    from fm24_dump import _reader, load_payload
    from t05_pe import PE
    os.environ.setdefault('FM24_DB_DIR','<WORKSPACE>/scratch/data')
    manifest = load('cursor.json')
    raw = load_payload(_reader(),'client',3)
    pe = PE(EXE)
    require(sha256(raw).hexdigest()==manifest['provenance']['payload_sha256'], 'member digest')
    reg = ROOT / 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
    require((digest:=sha256(pe.raw).hexdigest())==manifest['provenance']['exe_sha256'] and
            digest in reg.read_text(encoding='utf-8'), 'exe digest')
    verified = list(grammar(raw))
    serialized = [r for part in manifest['rows']['shards'] for r in load(part)['rows']]
    require(verified==serialized and len(verified)==84259, 'all row-coordinate trace tuples')
    # Independently reconstruct the legacy footer offset after the wire count's first byte.
    require(verified[-1][3]==0x69c669 and int(manifest['wire_footer'],16)==0x69c669 and
            int(manifest['old_footer'],16)==0x69c66a and manifest['footer_raw']==raw[-9:].hex(' '), 'footer offsets')
    compact = [r[0] for r in verified if r[2]==12]
    require(compact==[69706,69707,69708], 'compact rows')
    inst = instructions(pe, manifest)
    check_vslots(pe, manifest['class_selector']['reader_slots'], {0xe5a7a0,0x157cff0})
    num = sample_fields(raw, verified, pe, inst, manifest)
    print(f't24 verification PASS: {len(verified)} rows; wire footer {verified[-1][3]:#x}; compact {compact}; {num} fields; {len(inst)} instruction records')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--selftest', action='store_true')
    a = p.parse_args()
    try:
        selftest() if a.selftest else verify()
        return 0
    except (Failure, UnicodeError, struct.error, StopIteration) as e:
        print(f't24 verification FAILED: {e}',file=sys.stderr)
        return 1
    except (OSError, ImportError, KeyError, ValueError, IndexError) as e:
        print(f't24 verification fatal: {e}',file=sys.stderr)
        return 2


if __name__=='__main__':
    sys.exit(main())
