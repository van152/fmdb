#!/usr/bin/env python3
"""Offline, path-specialized client table_3 reader. Offsets in this source are PE file offsets."""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import struct
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch/t24/out'
EDITOR = Path(str(_cfg.EDITOR_EXE))
PROV = 'evidence/fm24/reports/qa/IDA_PROVENANCE.md'
MASTER = 'evidence/fm24/reports/editor_schema/master.json'
EXPECTED_SHA = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
LEGACY_FOOTER = 0x69c66a
STD = 'CLUB'
DER = 'LEAGUE_BODY_CLUB'
SEL = 0xf2ba0e
DERIVED = [(0x43bebef, 4, 0x170), (0x43bec0e, 1, 0x178)]
SCALARS = [(0xe5a81a, 4, 0xd8), (0xe5a843, 4, 0xe0), (0xe5a877, 4, 0xe8),
           (0xe5a8a0, 4, 0xf0), (0xe5a8cd, 4, 0xf8), (0xe5a92a, 6, 0x160)]
LEN, TEXT = 0x35b0828, 0x35b0883
TAIL_BYTE, TAIL_PAIR, IDENTITY = 0x3fc2050, 0x11d0f6f, 0x11d21df
BODY = {SEL: None, **{a: o for a, _, o in DERIVED + SCALARS}, LEN: None, TEXT: None,
        TAIL_BYTE: 0xba, TAIL_PAIR: 0xb8, IDENTITY: 8}
FOOT = [(0xffa602, 4), (0xf2baa2, 1), (0xf2bac2, 4)]
TRANSFER_PROOFS = {
    SEL: [0xf2ba02, 0xf2ba0b, 0xf2ba1b, 0xf2ba23],
    0x43bebef: [0x43bebdc, 0x43bebe6], 0x43bec0e: [0x43bebfb, 0x43bec05],
    0xe5a81a: [0xe5a7dc, 0xe5a811], 0xe5a843: [0xe5a807, 0xe5a837, 0xe5a840],
    0xe5a877: [0xe5a846, 0xe5a86e], 0xe5a8a0: [0xe5a864, 0xe5a894, 0xe5a89d],
    0xe5a8cd: [0xe5a8a3, 0xe5a8c4], 0xe5a92a: [0xe5a8d4, 0xe5a8f2, 0xe5a900, 0xe5a921],
    LEN: [0xe5a945, 0xe5a952, 0xe5a995, 0xe5a99f, 0x814110, 0x35b081e, 0x35b0822],
    TEXT: [0x35b0835, 0x35b083f, 0x35b0845, 0x35b0847, 0x35b0879],
    TAIL_BYTE: [0x11d0d6d, 0x11d0d75, 0x11d0d89, 0x12e66a0, 0x3fc2038, 0x11d0d99],
    TAIL_PAIR: [0x11d0f01, 0x11d0f24, 0x11d0f47, 0x11d0f59],
    IDENTITY: [0x11d0fa4, 0x11d21cc, 0x11d21d3, 0x11d2213],
    0xffa602: [0xf2ba7f, 0xffa5fc], 0xf2baa2: [0xf2ba92, 0xf2ba99],
    0xf2bac2: [0xf2bab2, 0xf2bab9],
}


class CheckError(Exception):
    pass


def check(ok, message):
    if not ok:
        raise CheckError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read_json(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8'))


def dump(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')


def parts(stem, data, key='rows', size=200):
    names = []
    for i in range(0, len(data), size):
        name = f'{stem}.part{len(names)+1:03d}.json'
        # One record per line; no unbounded diagnostic output.
        body = ',\n'.join(json.dumps(x, ensure_ascii=False, separators=(',', ':')) for x in data[i:i+size])
        (OUT / name).write_text('{"' + key + '":[\n' + body + '\n]}\n', encoding='utf-8')
        names.append(name)
    return names


def inputs():
    import fm24_dump as db
    from t05_pe import PE
    os.environ.setdefault('FM24_DB_DIR', str(_cfg.DATA_DIR))
    return db.load_payload(db._reader(), 'client', 3), PE(EDITOR)


def sources(pe):
    manifest = {x['path']:x['sha256'] for x in read_json('evidence/MANIFEST.json')['files']}
    for asset in PROV, MASTER:
        check(sha((ROOT / asset).read_bytes()) == manifest[asset], f'manifest mismatch: {asset}')
    check(EXPECTED_SHA in (ROOT / PROV).read_text(encoding='utf-8'), 'provenance missing expected SHA')
    check(sha(pe.raw) == EXPECTED_SHA, 'wrong editor.exe')
    return {a:manifest[a] for a in (PROV, MASTER)}


def from_int(b):
    return int.from_bytes(b, 'little')


def read_row(raw, p, i, limit, *, version):
    """Read selector first, then execute the observed successful modern-client path.

    Keep the previous coordinate origin at the first body byte. Identity's ordinal
    is a postcondition only. No ordinal, search for identity, or row lengths drive reads.
    Trace events are [file_offset:int, body_relative_offset, width].
    """
    trace = []
    beginning = p + 1

    def read(site, n):
        nonlocal p
        check(n >= 0 and p + n <= limit, f'row {i}: out-of-bounds read {site:#x} at {p:#x} width {n}')
        trace.append([site, p-beginning, n])
        data = raw[p:p+n]
        p += n
        return data

    kind = from_int(read(SEL, 1))
    check(kind in (0, 12), f'row {i}: selector {kind:#x} outside witnessed domain')
    if kind == 12:
        for site, width, _ in DERIVED:
            read(site, width)
    check(version >= 0xdc4, 'unsupported legacy reader path')
    for site, width, _ in SCALARS:
        read(site, width)
    lengths = []
    for _ in range(2):
        n = from_int(read(LEN, 4))
        lengths.append(n)
        if n:  # length test at 0x35b0847; no 0-byte transfer
            read(TEXT, n).decode('utf-8')
    tmp = read(TAIL_BYTE, 1)
    tail = read(TAIL_PAIR, 2)
    check(tmp == b'\0' and tail == b'\0\0', f'row {i}: outside witnessed base-helper domain')
    ordinal, uid, uid_copy = struct.unpack('<3I', read(IDENTITY, 12))
    check(ordinal == i and uid == uid_copy, f'row {i}: identity postcondition failed')
    check(sum(t[2] for t in trace) == p-(beginning-1), f'row {i}: transfer sum')
    return {'ordinal':i, 'body_start':beginning, 'selector':kind, 'end':p,
            'N':lengths[0], 'M':lengths[1], 'uid':uid, 'trace':trace}


def walk(raw):
    check(raw[:6] == b'\x03\x01tad.', 'wrong member type/context')
    version, count = struct.unpack_from('<HI', raw, 6)
    p = 13
    for i in range(count):
        row = read_row(raw, p, i, len(raw), version=version)
        yield row
        p = row['end']
    # The legacy framing borrowed the first byte of the terminal count as the last row's marker.
    check(len(raw)-p == 9 and from_int(raw[p:p+4]) == 0,
          f'footer requires 4B zero count + 1B flag + 4B word at {p:#x}')


def fixture(kind, full, short, i=0):
    return (bytes([kind]) + (b'\xff'*4+b'\0' if kind == 12 else b'') + b'\xff'*20 + b'\0'*6
            + struct.pack('<I',len(full)) + full + struct.pack('<I',len(short)) + short
            + b'\0'*3 + struct.pack('<3I', i, 123, 123))


def selftest():
    a, b = fixture(12,b'',b'',0), fixture(0,'é'.encode(),b'F',1)
    payload = b'\x03\x01tad.' + struct.pack('<HI', 0xdf1, 2) + b'\0' + a + b + b'\0'*9
    rows = list(walk(payload))
    check([x['selector'] for x in rows] == [12,0], 'selftest selector order')
    check([len(x['trace']) for x in rows] == [14,14], 'selftest zero-string transfer suppression')
    check(rows[0]['end'] == 68 and rows[1]['N'] == 2, 'selftest offsets')
    for bad in [payload[:13]+b'\x01'+payload[14:], payload[:-1], payload[:45]+b'\xff'+payload[46:]]:
        try:
            list(walk(bad))
        except CheckError:
            continue
        raise CheckError('malformed fixture accepted')
    print('t24 builder selftest: OK')


class Evidence:
    def __init__(self, pe):
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        self.pe = pe
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True
        self.records = {}

    def instruction(self, off):
        va = self.pe.f2va(off)
        check(va is not None and self.pe.va2f(va) == off, f'bad PE mapping {off:#x}')
        return next(self.md.disasm(self.pe.raw[off:off+15], va, count=1))

    def add(self, *offs):
        keys = []
        for off in offs:
            k = hex(off)
            if k not in self.records:
                i = self.instruction(off)
                self.records[k] = {'file_offset':k,'VA':hex(i.address),'bytes':i.bytes.hex(' '),
                                   'instruction':f'{i.mnemonic} {i.op_str}'.rstrip()}
            keys.append(k)
        return keys


def refl(row, site, idx=0):
    return [t for t in row['trace'] if t[0] == site][idx]


def transfer_index(ev):
    out = {}
    for site, proofs in TRANSFER_PROOFS.items():
        k = ev.add(site)[0]
        rec = ev.records[k].copy()
        check(rec['instruction'].startswith('call qword ptr [') and rec['bytes'].endswith('28'), f'bad transfer {k}')
        out[k] = {**rec,'object_off':BODY.get(site),'setup':ev.add(*proofs)}
    return out


# Site, offset within the transfer, width, object slot, (dispatch/getter evidence).
# A 4-byte wire reference is resolved to an in-memory pointer on slot-20 fix-up.
FIELDS = {
    'Cnti': (0xe5a81a,0,4,0xd8,[0xe8af47,0xe8af4d,0xe8af53,0xe8af5b,0xe5c57e,0xe5c599]),
    'Cbni': (0xe5a877,0,4,0xe8,[0xe8b7a7,0xe8b7ad,0xe8e3d3,0xe8e3db,0xe8e3e0,0xe5c5be,0xe5c5d9]),
    'Cccn': (0xe5a8a0,0,4,0xf0,[0xe8b7bf,0xe8b7c5,0xe8b7cb,0xe8b7d3,0xe5c5de,0xe5c5f9]),
    'Ccty': (0xe5a8cd,0,4,0xf8,[0xe8c22c,0xe8c232,0xe8e566,0xe8e571,0xe5c5fe,0xe5c619]),
    'Csot': (0xe5a92a,0,1,0x160,[0xe8b1cc,0xe8b1d2,0xe8b1d8,0xe8b1e9,0xe8b1eb]),
    'CASt': (0xe5a92a,1,1,0x161,[0xe8c9a8,0xe8c9ae,0xe8c9b4,0xe8c9c5]),
    'CnCV': (0xe5a92a,3,1,0x163,[0xe8cded,0xe8cdf3,0xe8cdf9,0xe8ce0a]),
    'Csnm': (TEXT,0,None,0xc8,[0xe8a451,0xe8a457,0xe8a460,0xe8a465,0xe8f51d,0x11f0f20,0x11f0f26,
                              0x11f1bdb,0xe9ab10]),
    'PLgn': (TAIL_PAIR,1,1,0xb9,[0xe8f51d,0x11f06fe,0x11f0704,0x11f0756]),
    'duni': (IDENTITY,4,4,0x0c,[0xe8f51d,0x11f2a98,0x11f2aba,0x11f4550,0xfe3912,0xfe3918,0xfe3bff]),
}
FORMS = {'Csnm': ('34+N','39+N'), 'PLgn': ('36+N+M','41+N+M'), 'duni': ('41+N+M','46+N+M')}
MASKS = {'Csot':2,'CASt':1,'CnCV':1}

# Observed successful paths within the frozen member. Branches off these paths
# are not claimed dead globally. The table is expanded with instruction bytes.
# (taken in CLUB, taken when called from derived, evidence source)
PATH = {
    0xe5a7d6:(False,False,'external_nonnull_stream'), 0xe5a801:(False,False,'external_nonnull_stream'),
    0xe5a900:(False,False,'data_member_version'), 0xe5a91c:(False,False,'external_nonnull_stream'),
    0xe5a95b:(False,False,'external_stream_status'), 0xe5a964:(True,True,'computed_pending_width_zero'),
    0xe5a9a8:(True,True,'external_stream_status'), 0xe5a9ba:(True,True,'external_mode_inferred_zero'),
    0xe5bc3c:(False,True,'selector_via_call_argument_r8b'), 0xe5bc59:(True,None,'computed_pending_width_zero'),
    0xe5bcae:(False,None,'external_base_helper_success'), 0xe5bcba:(True,True,'computed_pending_width_zero'),
    0xe5bcee:(False,False,'external_nonnull_stream'), 0xe5bcf4:(True,True,'external_refcount'),
}
DER_PATH = {0x43bebf6:(None,False,'external_stream_status'), 0x43bec15:(None,False,'external_stream_status'),
            0x43bec3d:(None,False,'external_base_reader_success')}
# Extra (interprocedural) conditions executed in the current member.
HELPER_BRANCHES = {
    0xf48db2:'data_selector_not_0x0c', 0xf2b9fa:'data_table_row_count_vs_iteration',
    0x35b0835:'data_string_length_vs_external_max', 0x35b083f:'external_stream_status',
    0x35b0847:'data_string_length_zero', 0x3fc203f:'computed_pending_width_nonzero',
    0x11d0dac:'data_member_version', 0x11d0e1c:'computed_pending_end_pointer',
    0x11d0f0f:'computed_pending_width_zero', 0x11d0f47:'data_member_version',
    0x11d0f66:'external_nonnull_stream', 0x11d0f8f:'data_object_plus_0xb9_zero',
    0x11d0fa4:'external_mode_inferred_zero', 0x11d2190:'computed_pending_width_zero',
    0x11d221a:'data_identity_first_word_lt_0x989681', 0x11d2256:'computed_pending_width_zero',
}


def cfg_evidence(ev, frozen):
    from t21b_control_flow import ReaderCFG
    ev.pe.pe.parse_data_directories(directories=[3])
    out = []
    active_transfers = set()
    for cls, path in zip(frozen['classes'], (PATH, DER_PATH), strict=True):
        base = cls['cfg']
        cfg = ReaderCFG(ev.pe, ev.md, int(base['entry_file_offset'],16))
        raw_branches = {int(x['file_offset'],16):x for x in base['branches'] if x['conditional']}
        check(set(path) <= raw_branches.keys(), 'missing chosen branch in t21b')
        for branch, x in raw_branches.items():
            cur = ev.pe.f2va(branch)
            local = [s for s, tos in cfg.successors.items() if cur in tos]
            # Skip straight-line instructions not writing flags. Stop at a merge,
            # call, or noncontiguous edge instead of inventing flag provenance.
            producer = None
            while len(local) == 1:
                addr = local[0]
                ins = cfg.instructions[addr]
                if ins.mnemonic == 'call' or addr + ins.size != cur:
                    break
                if any(ev.md.reg_name(r) in ('rflags','eflags') for r in ins.regs_access()[1]):
                    producer = ins
                    break
                cur = addr
                local = [s for s, tos in cfg.successors.items() if cur in tos]
            k = ev.add(branch)[0]
            check(ev.records[k]['VA'] == x['va'], f't21b VA mismatch {k}')
            reason = path.get(branch, (None,None,None))[2]
            if reason:
                status = 'selected_client_path_' + ('data' if reason.startswith(('data_','selector_')) else
                                                   'external' if reason.startswith('external_') else 'computed')
            elif producer is not None and ('rip +' in producer.op_str or 'rip -' in producer.op_str
                                           or 'gs:' in producer.op_str or '0x588]' in producer.op_str):
                status = 'off_path_context_or_global_predicate'
            elif producer is not None and any(z in producer.op_str for z in ('[rbp + 0x2f]', '[rbp + 0xa0]', '[rbp + 0xa8]')):
                status = 'off_path_count_or_argument_predicate_unresolved'
            else:
                status = 'off_path_unresolved_not_proven_dead'
            out.append({**ev.records[k],'class':cls['class'],'classification':status,'predicate':reason,
                        'taken_in_direct':path.get(branch,(None,None,None))[0],
                        'taken_in_derived':path.get(branch,(None,None,None))[1],
                        'flags_producer':None if producer is None else ev.add(ev.pe.va2f(producer.address))[0],
                        'target_file_offset':x['target_file_offset'],'backedge_t21b':x['backedge']})
        transfers = {int(x['file_offset'],16) for x in base['stream_transfers']}
        for mode in (0,1) if cls['class'] == STD else (1,):
            addr = cfg.start_va
            seen = set()
            this = []
            while addr in cfg.instructions:
                check(addr not in seen,'selected reader loop is not modeled')
                seen.add(addr)
                off = ev.pe.va2f(addr)
                if off in transfers:
                    this.append(off)
                ins = cfg.instructions[addr]
                succs = cfg.successors[addr]
                if off in raw_branches:
                    check(off in path and path[off][mode] is not None, f'unmodeled executed branch {off:#x}')
                    addr = ins.operands[0].imm if path[off][mode] else addr+ins.size
                    check(addr in succs, f'invalid branch choice {off:#x}')
                elif len(succs) == 1:
                    addr = succs[0]
                else:
                    check(ins.mnemonic=='ret' or off==0x43bec5b, f'unexpected path end {off:#x}')
                    break
            want = [a for a,_,_ in (SCALARS if cls['class']==STD else DERIVED)]
            check(this == want, f'path transfers differ: {this} vs {want}')
            active_transfers.update(this)
    return out, active_transfers


def field_ledger(raw, rows, ev, transfers):
    schema = read_json('scratch/t05/schema_inventory.json')['entities']['club']['fields']
    top = [x for x in schema if x['parent'] is None]
    check(len(top)==433 and len(schema)==672, 'unexpected schema counts')
    # t12's shaped global matches are not by themselves table_3 field evidence.
    # Preserve subtable coordinates separately from the main ledger.
    t12 = read_json('reports/t12_field_names.json')['slots']
    sub = defaultdict(list)
    for slot in t12:
        if slot['type_id']==3 or slot['schema_entity']!='club' or not slot.get('codes'):
            continue
        for code in slot['codes']:
            sub[code].append({k:slot.get(k) for k in ('type_id','archive','idx','row_off','width','object_off','confidence')})
    t20 = read_json('scratch/t20/out/fields_t22.json')
    t22_indices = defaultdict(list)
    for hit in t20['fields']:
        for cand in hit.get('schema_candidates',[]):
            t22_indices[cand['schema_index']].append({'type_id':22,'source':'E56/t20',
                'slot':hit['slot'],'object_off':hit['object_off'],'width':hit['width'],
                'row_offset':None,'row_offset_candidate':hit.get('row_offset_candidate'),
                'status':'partial_t22_slot_candidate_only'})
    table_identity = {x['table_type']:x for x in read_json('reports/stage2_table_identity.json')['rows']}
    t18 = read_json('scratch/t18/out/fields_club.json')
    for name in t18['shards']:
        page = read_json('scratch/t18/out/'+name)
        for rec in page['fields']:
            for hit in (rec.get('evidence',{}).get('matches',[]) + rec.get('evidence',{}).get('baseline',[])):
                t = hit.get('table_type')
                if t not in (None,3):
                    sub[rec['field']].append({'type_id':t,'source':'t18 '+name,
                                               'row_offset_candidate':hit.get('offset'), 'width':hit.get('width'),
                                               'object_off':hit.get('object_off')})
    for refs in sub.values():
        for r in refs:
            prior = table_identity.get(r['type_id'],{})
            r['table_identity_status'] = prior.get('status','unadjudicated')
            r['adjudicated_entity'] = prior.get('entity')
            r['coordinate_scope'] = 'prior per-table candidate only; never table_3'
    nested = []
    for rec in schema:
        if rec['parent'] is not None:
            refs = t22_indices.get(rec['idx'],[]) if rec['parent']=='Cstc' else []
            if rec['parent']=='Cstc' and not refs:
                refs = [{'type_id':22,'source':'E56/t20 family only; child slot not resolved'}]
            nested.append({**rec,'scope':'nested_schema_not_main_coordinate', 'references':refs})
    fields = []
    for s in top:
        code = s['code']
        field = {k:s[k] for k in ('idx','code','name','type')}
        if code not in FIELDS:
            notes = {}
            if code == 'Cstc':
                notes = {'subtable_family':{'type_id':22,'source':'E56/t20; see nested_shards',
                                            'parent_reference_slot':'t22 slot 0 / object+0x18; candidate, not t3 coordinate'}}
            elif code == 'Cnam':
                notes = {'candidate':{'status':'partial_Cnam_getter_proxy_unresolved','object_off':0xc0,
                    'note':'Cnam setter delegates to TCln; setter writes +0xc0; getter uses a localization proxy, not established as this direct string slot',
                    'sites':ev.add(0xe84072,0xe8409e,0xe840a6,0xe83806,0xe8380c,0xe84b97,0xe84ba4,
                                   0xe8bc91,0xe8bc97,0xe8e8f2,0x11f0849,0x11f0862)}}
            elif code == 'Clri':
                notes = {'candidate':{'status':'negative_not_separate_main_slot',
                    'note':'Getter follows the +0xf8 City reference, then city+0x38.',
                    'sites':ev.add(0xe8bb72,0xe8bb7e,0xe8bb8f)}}
            fields.append({**field,'grade':'unnamed','row_offset':None,'width':None,'object_off':None,
                           'VA':None,'bytes':None,'subtable_references':sub.get(code,[]),**notes})
            continue
        site, delta, width, obj, proof = FIELDS[code]
        check(int.from_bytes(code.encode(),'big') in [int(o.imm) for o in ev.instruction(proof[0] if code not in ('PLgn','duni')
              else (0x11f06fe if code=='PLgn' else 0xfe3912)).operands if o.type==2], f'4CC changed: {code}')
        # Both string transfers live in a shared helper; width=0 is legal and skips its payload call.
        stat = {STD:Counter(), DER:Counter()}
        samples = {}
        for r in rows:
            kind = DER if r['selector']==12 else STD
            if code=='Csnm':
                pos = refl(r,LEN,1)[1]+4
                w = r['M']
            else:
                pos = refl(r,site)[1]+delta
                w = width
            absolute = r['body_start']+pos
            b = raw[absolute:absolute+w]
            stat[kind][b] += 1
            key = (kind, bool(w))
            if key not in samples:
                samples[key] = {'ordinal':r['ordinal'],'member_offset':absolute,'row_offset':pos,'width':w,'data_bytes':b.hex(' ')}
        if code in FORMS:
            offset = dict(zip((STD,DER),FORMS[code],strict=True))
        else:
            off = refl(rows[0],site)[1]+delta
            offset = {STD:off,DER:off+5}
        stats = {k:{'rows':sum(v.values()),'distinct_wire_values':len(v),'most_common_hex':
                    [[b.hex(' '),n] for b,n in v.most_common(3)]} for k,v in stat.items()}
        extra = {'bit_mask':MASKS[code]} if code in MASKS else {}
        if code in ('Cnti','Cbni','Cccn','Ccty'):
            extra['wire_value'] = '4-byte reference index before slot-20 fix-up; not the referenced UID'
        if code=='Cbni':
            extra['fallback'] = 'getter falls back to Cnti when the resolved +0xe8 pointer is null'
        if code=='Csnm':
            extra['width_prefix'] = {STD:'30+N',DER:'35+N'}
            extra['vtable_slots'] = [vslot(ev,0x187c308,47),vslot(ev,0x18bf1f8,47)]
        if code=='duni':
            extra['vtable_slots'] = [vslot(ev,0x187c308,56),vslot(ev,0x18bf1f8,56)]
        tf = transfers[hex(site)]
        fields.append({**field,'row_offset':offset,'width':'M' if width is None else width,'object_off':obj,
                       'VA':tf['VA'],'file_offset':tf['file_offset'],'bytes':tf['bytes'],'grade':'L3_row_instruction',
                       'getter_sites':ev.add(*proof),'transfer_slice': {'delta':delta,'occurrence':'short_name' if width is None else 0},
                       'validation':stats,'samples':list(samples.values()),**extra})
    ledger = {'status':'partial_10_main_L3_of_433_schema_fields','entity':'club','schema_entries':len(top),
              'main_L3':len(FIELDS),'schema_source':'scratch/t05/schema_inventory.json (frozen master schema)',
              'offset_space':'t21 body-relative; selector at -1','subtable_sources':[
                  'reports/t12_field_names.json (prior bridge candidates only)',
                  'scratch/t18/out/fields_club*.json (retained per-table scope, no re-promotion)',
                  'scratch/t20/out/fields_t22.json (Cstc evidence, row offsets still unresolved)'],
              'nested_schema_count':len(nested),'t22_prior_status':t20.get('status'),
              'shards':parts('fields_club',fields,'fields',80), 'nested_shards':parts('subtables',nested,'nested_fields',80)}
    return ledger


def vslot(ev, table, slot):
    off = table+slot*8
    word = ev.pe.raw[off:off+8]
    return {'slot':slot,'file_offset':hex(off),'VA':hex(ev.pe.f2va(off)), 'bytes':word.hex(' '),
            'target':ev.add(ev.pe.va2f(from_int(word)))[0]}


def build():
    raw, pe = inputs()
    manifest = sources(pe)
    frozen = read_json('scratch/t21/out/control_flow.json')
    baseline = read_json('scratch/t21/out/audit.json')
    check(sha(raw)==baseline['data_sha256'], 'payload differs from t21 input')
    ev = Evidence(pe)
    transfers = transfer_index(ev)
    branches, active_transfers = cfg_evidence(ev,frozen)
    rows = list(walk(raw))
    check(len(rows)==84259 and rows[-1]['end']==LEGACY_FOOTER-1, 'unexpected row count or true footer')
    kinds = Counter(r['selector'] for r in rows)
    compact = [r for r in rows if r['selector']==12]
    check(kinds=={0:84256,12:3},'unexpected full-table selector counts')
    for r in rows:
        old_len = (r['end']+1)-r['body_start']
        check(old_len == r['N']+r['M']+50+(5 if r['selector']==12 else 0), f'width accounting row {r["ordinal"]}')
    check([r['ordinal'] for r in compact]==[69706,69707,69708] and
          all((r['N'],r['M'])==(0,0) for r in compact), 'compact overlap differs from the baseline')
    # Same transfer geometry is shared by all rows with the same kind and zero/nonzero strings.
    # Store a lossless trace tuple rather than repeating 14 triples across the corpus.
    packed = [[r[k] for k in ('ordinal','body_start','selector','end','N','M','uid')] for r in rows]
    OUT.mkdir(parents=True,exist_ok=True)
    branches_path = parts('branches',branches,'branches')
    ledger = field_ledger(raw,rows,ev,transfers)
    dump('fields_club.json',ledger)
    selectors = ev.add(0xf2b691,0xf2b6b1,0xf2ba0e,0xf2ba1b,0xf2ba20,0xf2ba23,0xf2ba51,
                       0xf48b41,0xf48b4c,0xf48b53,0xf48daf,0xf48db2,0xf48dc3,0xf48dc8,0xf48dcf,
                       0xf49c3f,0x3aad0fd,0x157cff0,0x43bec30,0x43bec36,0x43bec5b,
                       0xf28bf9,0xf28c16,0xf2b8b1,0xf2b8b5)
    helper_branches = [{**ev.records[ev.add(o)[0]],'predicate':rule} for o,rule in HELPER_BRANCHES.items()]
    route = ev.add(0xe5a92d,0xe5a935,0xe5a93d,0xe5a979,0xe5a981,0xe5a989,0xe5a9b1,0xe5a9ba,
                   0xe5a9f1,0xe5aa73,0xe5aaa2,0xe5aada,0xe5ab0a,0xe5bc39,0xe5bca7,
                   0xf2b670,0xf2ba38,0xf2ba4b,0x11d0f9d,0xf2b9f3,0xf2b9fa)
    structure = {
        'status':'complete_observed_client_row_cursor_partial_off_path_CFG', 'table':3,'archive':'client',
        'provenance':{'exe':str(EDITOR),'exe_sha256':EXPECTED_SHA,'snapshot_manifest_matches':manifest,
                      'payload_sha256':sha(raw),'t21_baseline':'scratch/t21/out/audit.json',
                      't21b_CFG':'scratch/t21/out/control_flow.json'},
        'old_row_origin':'first body byte; old trailer is next selector except on last row',
        'wire_row_origin':'selector at prior row-relative -1; wire end is exclusive and after identity',
        'old_footer':hex(LEGACY_FOOTER),'wire_footer':hex(rows[-1]['end']),
        'footer_raw':raw[rows[-1]['end']:].hex(' '),
        'footer_transfers':[[hex(site),width] for site,width in FOOT], 'row_count':len(rows),
        'rows':{'columns':['ordinal','body_start','selector','end','N','M','uid'],
                'trace_reconstruction':'read_row or trace_template; this is a lossless geometric summary',
                'shards':parts('cursor',packed,size=1000)},
        'trace_template':{'event_columns':['file_offset','body_relative_offset','width'],
                           'sequence':[hex(SEL),'if 12: '+', '.join(hex(x[0]) for x in DERIVED),
                                       *[hex(x[0]) for x in SCALARS],
                                       hex(LEN),'if N: '+hex(TEXT),hex(LEN),'if M: '+hex(TEXT),
                                       hex(TAIL_BYTE),hex(TAIL_PAIR),hex(IDENTITY)],
                           'constant_widths':{hex(a):n for a,n in [(SEL,1),*((a,n) for a,n,_ in DERIVED+SCALARS),
                                              (LEN,4),(TAIL_BYTE,1),(TAIL_PAIR,2),(IDENTITY,12)]}},
        'compact':[dict(r,body_hex=raw[r['body_start']:r['end']].hex(' ')) for r in compact],
        'class_selector':{'status':'complete_selector_byte_for_client_table3', 'origin':'row prefix; -1 in t21 coordinates',
                          'counts':{STD:kinds[0],DER:kinds[12]}, 'predicate':'factory case 3: BL==0x0c selects derived',
                          'ordinal_used_to_select':False, 'instruction_sites':selectors,
                          'jump_table_3':{'file_offset':'0xf49d44','VA':hex(pe.f2va(0xf49d44)),
                                          'bytes':pe.raw[0xf49d44:0xf49d48].hex(' ')},
                          'reader_slots':[vslot(ev,0x187c308,19), vslot(ev,0x18bf1f8,19)],
                          't21b_original_negative':frozen['row_class_discriminator']},
        'client_specialization':{'member_version':from_int(raw[6:8]),'external_mode':'inferred zero from transfer budgets; not a selector',
                                 'positive_mode_negative':'nonzero at e5a9ba enters path consuming at least 1+2+4+1 bytes before base footer, not the observed 3',
                                 'sites':route},
        'branches':{'shards':branches_path,'counts':dict(Counter(r['classification'] for r in branches)),
                    'interprocedural':helper_branches,
                    'unresolved_scope':'Branches only reachable on other modes, failures or allocation paths are not executed by this client walker; local flag producers are hints, not necessarily transitive origins.'},
        'transfer_sites':transfers, 'active_t21b_transfers':sorted(hex(x) for x in active_transfers),
        'controls':{'legacy_Cccn_plus8':'negative_E60; never promoted','derived_Cccn_row_offset':17,'direct_Cccn_row_offset':12,
                    'E60_original':next(e['claim'] for e in read_json('scratch/t01/LEDGER.json')['entries'] if e['id']=='E60'),
                    't21b_derived_backedge_correction':'0x43bec5b is an interprocedural tail-jump to lower VA 0x1411d1730, not a local loop',
                    'footer_prefix_reassignment':'legacy reported +1 to body and -1 to footer; file bytes unchanged'},
        'instruction_shards':parts('instructions',list(ev.records.values()),'instructions',200),
    }
    dump('cursor.json',structure)
    print(f't24: {len(rows)} rows; classes={dict(kinds)}; true wire footer {rows[-1]["end"]:#x}; {len(FIELDS)} main L3 fields')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()
    try:
        if args.selftest:
            selftest()
        else:
            build()
        return 0
    except (CheckError, UnicodeError, struct.error) as exc:
        print(f't24 check failed: {exc}', file=sys.stderr)
        return 1
    except (OSError, ImportError, KeyError, ValueError) as exc:
        print(f't24 fatal: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
