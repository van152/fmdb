#!/usr/bin/env python3
"""Independently verify the t62 exact-key UI paths and bounded archive exclusions."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import struct
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EXE = Path('<OLD_REPO>/input/editor.exe')
PIN = 'b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'


class Mismatch(Exception):
    pass


def need(test, note):
    if not test:
        raise Mismatch(note)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def js(p):
    return json.loads(p.read_bytes())


def signed(n):
    return struct.unpack('<i', struct.pack('<I', n))[0]


def predicate(op, a, b):
    # near (0F 8x) and short (7x) jcc share the low nibble.
    return {4: a == b, 5: a != b, 6: a <= b, 7: a > b,
            0xe: signed(a) <= signed(b), 0xf: signed(a) > signed(b)}[op & 15]


def key_replay(raw, to_va, to_off, input_key):
    # Independent raw-opcode walk; no Capstone and no saved key route used here.
    a = 0x281cb; taken = []; esi = input_key; ecx = None; flags = None
    for _ in range(40):
        taken.append(a)
        if a in (0x29c43, 0x2a684):
            return {'input':input_key, 'trace':taken, 'entry':a}
        op = raw[a:a+2]
        if op == b'\x81\xfe':
            flags = esi, struct.unpack_from('<I',raw,a+2)[0]; a += 6
        elif op in (b'\x83\xfe', b'\x83\xf9'):
            lhs = esi if op[1] == 0xfe else ecx
            flags = lhs, struct.unpack_from('<b',raw,a+2)[0] & 0xffffffff; a += 3
        elif op == b'\x8d\x8e':
            ecx = (esi + struct.unpack_from('<i',raw,a+2)[0]) & 0xffffffff; a += 6
        elif op == b'\x81\xc6':
            esi = (esi + struct.unpack_from('<I',raw,a+2)[0]) & 0xffffffff; a += 6; flags = None
        elif op[0] == 0x0f and op[1] >> 4 == 8:
            rel = struct.unpack_from('<i',raw,a+2)[0]; a += 6
            if predicate(op[1], *flags): a = to_off(to_va(a) + rel)
        elif op[0] >> 4 == 7:
            rel = struct.unpack_from('<b',raw,a+1)[0]; a += 2
            if predicate(op[0], *flags): a = to_off(to_va(a) + rel)
        elif a == 0x282c8:
            need(raw[a:a+3] == b'\x48\x8d\x0d' and raw[a+7:a+15] == bytes.fromhex('486314b14801caff') and raw[a+15] == 0xe2,
                 'table addressing opcodes')
            taken += [a+7, a+11, a+14]
            va = to_va(a+7) + struct.unpack_from('<i',raw,a+3)[0]; table = to_off(va)
            n = raw[0x282c1] + 1
            need(0 <= esi < n == 68, 'computed index')
            ds = struct.unpack_from(f'<{n}i',raw,table); rel = ds[esi]; cell = table+4*esi
            return dict(input=input_key, trace=taken, entry=to_off(va+rel), table=table, table_va=va, entries=n,
                        index=esi, cell=cell, rel32=rel, cell_bytes=raw[cell:cell+4].hex(), same_target_indices=[i for i,k in enumerate(ds) if k == rel])
        else:
            raise Mismatch(f'unexpected opcode {a:#x} {op.hex()}')
    raise Mismatch('bounded key replay did not stop')


def verify_pe(x, c):
    import pefile
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_GRP_JUMP, CS_GRP_RET
    raw = EXE.read_bytes()
    need(sha(raw) == x['image']['sha256'] == c['image']['sha256'] == PIN, 'editor provenance')
    pe = pefile.PE(data=raw, fast_load=True)
    pe.parse_data_directories(directories=[3])
    base = pe.OPTIONAL_HEADER.ImageBase
    def va(o):
        for s in pe.sections:
            if s.PointerToRawData <= o < s.PointerToRawData+s.SizeOfRawData:
                return base+s.VirtualAddress+o-s.PointerToRawData
        return None
    def off(v):
        for s in pe.sections:
            d = v-base-s.VirtualAddress
            if 0 <= d < max(s.Misc_VirtualSize,s.SizeOfRawData): return s.PointerToRawData+d
        return None
    need(len(raw) == x['image']['size'] and c['image'] == x['image'], 'PE metadata')
    for key in ('EDfx','EDsc'):
        for codec in ('ascii','utf-16le','utf-16be'):
            for direction in ('forward','reverse'):
                s = (key if direction == 'forward' else key[::-1]).encode(codec)
                pos = raw.find(s); hits = []
                while pos >= 0:
                    hits.append(pos); pos = raw.find(s,pos+1)
                want = [0x29c39] if (key,codec,direction) == ('EDfx','ascii','reverse') else []
                rows = x['literal'][key][f'{codec}_{direction}']
                need(hits == want == [r['offset'] for r in rows], (key,codec,direction,hits))
                for row in rows:
                    need(row['kind'] == 'comparison' and row['bytes'] == s.hex() and row['instruction'] == 0x29c37 and row['va'] == va(row['offset']), 'literal location/classification')
    need(raw[0x29c37:0x29c3d] == bytes.fromhex('81fe78664445'), 'EDfx compare bytes')
    for key, target in {'EDfx':0x29c43,'EDsc':0x29389,'EDsb':0x2a684,'EDsd':0x293e9}.items():
        res = key_replay(raw,va,off,int.from_bytes(key.encode(),'big'))
        need(res == x['key_routes'][key] and res['entry'] == target, f'{key} route')
    need(x['key_routes']['EDsc']['cell'] == 0x2a8b8 and x['key_routes']['EDsc']['same_target_indices'] == [50], 'EDsc unique table cell')
    need(len(x['nonliteral'])==1 and x['nonliteral'][0]['jump_site']==0x282d6 and x['nonliteral'][0]['table_cell']==0x2a8b8 and x['nonliteral'][0]['arm']==0x29389,'computed xref row')
    cap = Cs(CS_ARCH_X86, CS_MODE_64); cap.detail = True; cache = {}
    def decode(a):
        if a not in cache:
            cache[a] = next(cap.disasm(raw[a:a+15],va(a),1))
        return cache[a]
    def imm(i): return i.operands and i.operands[0].type == 2
    ext = {off(base+e.struct.BeginAddress):off(base+e.struct.EndAddress) for e in pe.DIRECTORY_ENTRY_EXCEPTION}
    membership = {}
    for summary in c['cfg']:
        a,b = summary['entry'], summary['end_exclusive']
        need(ext[a] == b, f'bad RUNTIME_FUNCTION {a:#x}')
        extension = summary.get('extra_edge')
        need(extension is None or (a == 0x28150 and extension == [0x282d6, x['key_routes']['EDsc']['entry']]), 'unexpected resolved edge')
        pending = {a}; visited = set(); edges = []; outside = []; stops = []
        while pending:
            q = pending.pop(); visited.add(q)
            i = decode(q); following = q+i.size
            need(following <= b, f'instruction straddles extent {q:#x}')
            nexts = []
            if i.group(CS_GRP_JUMP):
                if imm(i):
                    nexts.append(off(i.operands[0].imm))
                    if raw[q:q+1] not in (b'\xe9',b'\xeb') and i.mnemonic != 'jmp': nexts.append(following)
                elif extension and q == extension[0]: nexts.append(extension[1])
                else: stops.append(q)
            elif not i.group(CS_GRP_RET) and i.mnemonic not in ('int3','ud2','iretq'):
                nexts.append(following)
            for r in nexts:
                if r is not None and a <= r < b:
                    edges.append([q,r]);
                    if r not in visited: pending.add(r)
                else: outside.append([q,r])
        need((len(visited),sorted(stops),sorted(outside),sha(json.dumps(sorted(visited)).encode()),sha(json.dumps(sorted(edges)).encode())) ==
             (summary['reachable'],summary['unknown_indirect_jmps'],summary['out_of_extent_edges'],summary['ip_sha256'],summary['edge_sha256']),
             f'CFG replay at {a:#x}')
        membership[a] = visited
        if a == 0x28150: need((0x29389 in visited) == bool(extension),'expected delta from recovered rel32 edge')
    sites = c['instructions']; need(set(sites) == {hex(a) for g in c['groups'].values() for a in g}, 'group coverage')
    for k,s in sites.items():
        a = int(k,16); i = decode(a)
        need(s['offset'] == a and s['va'] == va(a) and s['bytes'] == i.bytes.hex() and s['asm'] == (i.mnemonic+' '+i.op_str).strip(), f'instruction bytes {k}')
        if s.get('extent_entry') is not None:
            need(a in membership[s['extent_entry']], f'unreachable witness {k}')
        if i.mnemonic in ('call','jmp') and imm(i):
            need(s['target'] == off(i.operands[0].imm), f'direct target {k}')
        need(s['rip_targets'] == [i.address+i.size+o.mem.disp for o in i.operands if o.type==3 and i.reg_name(o.mem.base)=='rip'],f'RIP targets {k}')
    for track in c['hops'].values():
        need(all(hop['sites'] and all(hex(a) in sites for a in hop['sites']) for hop in track),'unbound hop witness')
    # Recheck the semantic hinge sites independently of instruction text in the ledgers.
    exact = {0x28163:'mov esi, r9d',0x2b47a:'mov r9d, dword ptr [rsp + 0x50]',
             0x29389:'test al, al',0x29396:'test r15, r15',0x2939f:'test bpl, bpl',0x293af:'cmp byte ptr [rax + 0x54c], 0',
             0x293c2:'call qword ptr [rax + 0x38]',0x293c5:'cmp eax, 0x19',0x293dc:'mov r9b, 1',0x2a23b:'cmp eax, 0xa',
             0x6be5f:'xor r9d, r9d',0x6c273:'mov ebx, r9d',0x6c2f3:'test bl, bl',
             0x29c69:'cmp eax, 0xa',0x9087b:'mov edx, 0x636f6d70',0x1b7a313:'mov edx, 0x666c6573',
             0x908e7:'lea r14, [rax + 0x1c0]',0x6288b0:'mov qword ptr [rcx + 0x38], rdx',
             0x909d7:'xor edx, edx',0x3d5c091:'mov rax, qword ptr [rcx + 0x108]',0x90a21:'mov r9, rax',
             0xb02af5:'add rcx, 0x38',0xb02bf0:'imul rax, rax, 0x2250',0xb02c03:'mov rbx, qword ptr [rax + rcx*8]',
             0x90fc8:'mov rcx, qword ptr [rsp + 0x80]',0x6c22f:'mov rcx, qword ptr [rsp + 0x28]',
             0x83d5d2:'mov qword ptr [rsi + 8], rcx',0x83d5d6:'mov qword ptr [rsi], rax',
             0x44d7c71:'mov rax, qword ptr [rax + 0x80]'}
    for a,s in exact.items():
        i = decode(a); need(i.mnemonic+' '+i.op_str == s,(hex(a),s))
    links = {0x2b4a2:0x28150,0x2938b:0x29f68,0x29399:0x29f6a,0x293a2:0x29f6a,0x293b6:0x29f6a,
             0x293c8:0x2a232,0x2a246:0x2a684,0x293df:0x6c120,0x2a252:0x6bb00,0x6be62:0x6c120,
             0x6c157:0x6c260,0x6c21a:0x6c770,0x6c237:0x83d5a0,0x6c0d0:0x83d5a0,0x29c80:0x907f0,
             0x90864:0x2ce20,0x2ce20:0x1b7a3c0,0x908c3:0xafe0f0,0xafe0f0:0x385d630,0x90906:0xaf8900,
             0x909d9:0x103f9f0,0x103f9f0:0x3d5c080,0x3d5c082:0x3d5c091,0x90a24:0xb02980,
             0x90fd3:0x83d5a0,0x29c85:0x29f68,0x15e9830:0x44d7bf0}
    for a,b in links.items():
        i=decode(a); need(imm(i) and off(i.operands[0].imm)==b, f'hop {a:#x} → {b:#x}')
    need(sites['0x44d7c6a']['rip_targets']==[0x141b60158], 'control collection global')
    return len(sites)


def verify_packages(d):
    sys.path.append('<OLD_REPO>/tools/python')
    import zstandard
    base_dir = Path(os.environ.get('FM24_DB_DIR',str(ROOT/'scratch/data')))
    need(base_dir.drive.upper() != 'Z:' and base_dir.resolve().drive.upper() != 'Z:', 'Z: forbidden')
    shell = b'\x02\x01fmf.\x08\x00\x00'
    def frame(b):
        need(b[:4] == b'\x28\xb5\x2f\xfd','Zstd magic')
        z = zstandard.ZstdDecompressor().decompressobj(); u = z.decompress(b)
        need(z.eof and z.unused_data == b'', 'bounded frame/EOF')
        return u
    for side, total in (('client',31),('server',77)):
        rec = d['archive'][side]; raw = (base_dir/f'{side}_db.dat').read_bytes()
        toc = 17 + int.from_bytes(raw[17:25],'little'); origin = 17 + int.from_bytes(raw[25:33],'little')
        need(raw[toc:toc+9] == shell and raw[8:17] == shell and origin == rec['data_base'] == 34 and toc == rec['toc_offset'],'archive framing')
        t = frame(raw[toc+9:]); index = {}; p = 0
        def u32():
            nonlocal p
            x = struct.unpack_from('<I',t,p)[0]; p += 4; return x
        def string():
            nonlocal p
            n = u32(); need(p+n<=len(t),'directory bounds'); s = t[p:p+n].decode('utf8'); p += n; return s
        def folder(path, depth):
            nonlocal p
            need(depth < 32, 'TOC depth')
            parent = path/string()
            for _ in range(u32()):
                member = (parent/(string()+string())).as_posix()
                need(member not in index and '..' not in PurePosixPath(member).parts, 'TOC unique path')
                o,w,n = struct.unpack_from('<QQQ',t,p); p += 40
                index[member] = (origin+o,w,n)
            for _ in range(u32()): folder(parent,depth+1)
        folder(PurePosixPath(),0)
        need(p==len(t) and len(index)==total and sorted(index)==rec['entries'] and sha(t)==rec['directory_sha256'] and sha(raw)==rec['archive_sha256'], f'{side}: directory ledger')
        names = [s for s in sorted(index) if 'edfx' in s.casefold() or 'edsc' in s.casefold()]
        need(rec['literal_names']==names==[], f'{side}: exact path control')
        need(len(rec['header_controls'])==2, 'bounded controls only')
        for tid,count in ((10,251),(25,7047)):
            member = f'{side}_db/table_{tid}.dat'; o,w,n = index[member]
            ceiling = min((v[0] for v in index.values() if v[0]>o),default=toc)
            need(origin <= o < o+w <= ceiling, f'{member}: member bounds')
            payload = frame(raw[o:o+w]); k = struct.unpack_from('<I',payload,8)[0]
            need(payload[2:6]==b'tad.' and k==count and len(payload)==n and rec['header_controls'][member]==
                 dict(start=o,packed=w,size=n,bound=ceiling,prefix13=payload[:13].hex(),count=k,sha256=sha(payload)),member)


def verify_sources(c, e):
    p = c['provenance']; ledger = js(ROOT/'reports/club_nation_subtable_schema.json')
    baseline = ledger['v3_baseline']; prev = js(ROOT/baseline['json_path']); man = ROOT/'evidence/MANIFEST.json'
    need(sha(man.read_bytes())==p['manifest_sha256'], 'manifest digest')
    for path,d in p['sources'].items(): need(sha((ROOT/path).read_bytes())==d, path)
    manifest = js(man); rows = manifest if isinstance(manifest,list) else next(lst for lst in manifest.values() if isinstance(lst,list) and lst and isinstance(lst[0],dict) and 'path' in lst[0])
    for path in ('evidence/fm24/reports/editor_schema/master.json','evidence/fm24/reports/qa/IDA_PROVENANCE.md'):
        need(next(x['sha256'] for x in rows if x['path']==path)==p['sources'][path],path)
    need(p['v3_baseline']==baseline and p['sources'][baseline['json_path']]==baseline['json_sha256'] and p['sources'][baseline['markdown_path']]==baseline['markdown_sha256'], 'v3 pins')
    need(p['v3_inventory_verbatim']==prev['inventory_reconciliation'], 'v3 original inventory')
    need(p['negative_regressions_verbatim']==prev['negative_regressions']==ledger['negative_regressions'], 'original regressions')
    old = next(f for f in js(ROOT/'scratch/t55/out/field_map.json')['fields'] if f['code']=='EDsc')
    need(p['t55_EDsc_verbatim']==old and old['grade']=='held' and old['slot'] is None, 't55 historical literal grade')
    need(p['t53_edsc_status']==js(ROOT/'scratch/t53/out/discovery_crs_wire.json')['EDsc']['status']=='negative_strengthened_no_verified_call_chain','t53 historical scope')
    master = js(ROOT/'evidence/fm24/reports/editor_schema/master.json')
    for scope, record in p['frozen_scopes'].items():
        kind, src, ord_string = scope.split(':'); path,tag = src.rsplit('#',1)
        family = 'entities' if kind == 'entity' else 'rule_groups'
        block = next(b for b in master[family][path] if b['id']==tag)
        need(block['fields'][int(ord_string)]==record, scope)
    need({s for s,r in p['frozen_scopes'].items() if r['field']=='EDsc'}==
         {'entity:nation.xml#nati:344','rule_group:advanced\\database test\\comp test.xml#cpts:22'},'EDsc scopes')
    need(c['L4']==e['L4']==0 and c['status']=='partial','claim bounds')
    for n,val in c['conclusions'].items(): need(all(val[k] is None for k in ('member','reader','writer')), f'unproven persistent source {n}')
    need(c['conclusions']['EDsc']['consumers']=={'10':0x6bb00,'25':0x6c120}, 'EDsc consumers')
    need({x['id'] for x in e['excludes']}=={f'E{i}' for i in range(1,8)} and all(x['scope'] and x['reopen'] and x['witness'] for x in e['excludes']), 'falsifier coverage')


def selftest():
    need(predicate(0x7f,0,0xffffffff) and not predicate(0x77,0,0xffffffff), 'signed/unsigned')
    need(predicate(0x86,0x43,0x43) and predicate(0x87,0x44,0x43) and not predicate(0x87,0x43,0x43), 'bounds')
    need(struct.unpack('<i', bytes.fromhex('99ebffff'))[0]+0x2a7f0==0x29389, 'negative rel32')
    print('t62 independent verifier selftest PASS')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--selftest',action='store_true',help='test signed branches and table cells without inputs')
    args = ap.parse_args()
    try:
        if args.selftest:
            selftest()
        else:
            x,c,e = (js(HERE/f'{name}.json') for name in ('xref','chain','exclusions'))
            n = verify_pe(x,c); verify_sources(c,e); verify_packages(e)
            print(f't62 verify PASS: {n} instruction witnesses; 4 key replays; 2 FMF directories; EDfx upstream unbound; L4=0')
    except Mismatch as e:
        print(f't62 mismatch: {e}',file=sys.stderr); return 1
    except Exception as e:
        print(f't62 fatal: {type(e).__name__}: {e}',file=sys.stderr); return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
