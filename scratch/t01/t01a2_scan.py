# t01-a2: pure-Python byte sweep for 4CC registration/comparison patterns.
# No IDA, no pip, stdlib only. Run: py -V:3.12 -I t01a2_scan.py
import re, os, sys, json, time

EXES = {
    'fm': r'D:\tmp2b\fm24\input\fm.exe',
    'editor': r'D:\tmp2b\fm24\input\editor.exe',
}
C = rb'[A-Za-z0-9]'
PATS = [
    ('mov', re.compile(rb'\xc7\x45.(' + C + rb'{4})')),        # mov [rbp+disp8], imm32
    ('cmp81', re.compile(rb'\x81[\xf8-\xff](' + C + rb'{4})')), # cmp r32, imm32 (incl esp/ebp)
    ('cmp3d', re.compile(rb'\x3d(' + C + rb'{4})')),            # cmp eax, imm32
]
CHUNK = 32 * 1024 * 1024
TAIL = 8  # max pattern len is 6; 8 is safe

def scan(path):
    size = os.path.getsize(path)
    hits = []  # (off, kind_idx, regbyte, code4bytes)
    t0 = time.time()
    with open(path, 'rb') as f:
        chunk_start = 0
        prev_tail = b''
        while True:
            data = f.read(CHUNK)
            if not data:
                break
            buf = prev_tail + data
            buf_abs0 = chunk_start - len(prev_tail)
            for ki, (name, rx) in enumerate(PATS):
                for m in rx.finditer(buf):
                    s = buf_abs0 + m.start()
                    if s < chunk_start:
                        continue  # already covered by previous chunk window
                    code = m.group(1)
                    reg = buf[m.start() + 1] if name == 'cmp81' else 0
                    hits.append((s, ki, reg, code))
            prev_tail = data[-TAIL:]
            chunk_start += len(data)
    hits.sort()
    dt = time.time() - t0
    return size, hits, dt

def count_raw(path, needle):
    n = 0
    first = None
    with open(path, 'rb') as f:
        chunk_start = 0
        prev_tail = b''
        while True:
            data = f.read(CHUNK)
            if not data:
                break
            buf = prev_tail + data
            base = chunk_start - len(prev_tail)
            i = buf.find(needle)
            while i != -1:
                aoff = base + i
                if aoff >= chunk_start:
                    n += 1
                    if first is None:
                        first = aoff
                i = buf.find(needle, i + 1)
            prev_tail = data[-TAIL:]
            chunk_start += len(data)
    return n, first

def count_raw32(path, needle):
    n, first = count_raw(path, needle)
    return n, first

def build_clusters(hits, gap=4096, min_hits=3):
    clusters = []
    cur = [hits[0]]
    for h in hits[1:]:
        if h[0] - cur[-1][0] < gap:
            cur.append(h)
        else:
            if len(cur) >= min_hits:
                clusters.append(cur)
            cur = [h]
    if len(cur) >= min_hits:
        clusters.append(cur)
    return clusters

def cluster_summary(cl, cap=64):
    kinds = [h[1] for h in cl]
    n_mov = kinds.count(0)
    n_cmp81 = kinds.count(1)
    n_cmp3d = kinds.count(2)
    codes = {}
    for h in cl:
        cb = h[3]
        if cb not in codes:
            codes[cb] = h[0]
    mov_offsets = [h[0] for h in cl if h[1] == 0]
    strides = {}
    for a, b in zip(mov_offsets, mov_offsets[1:]):
        d = b - a
        strides[d] = strides.get(d, 0) + 1
    top_strides = sorted(strides.items(), key=lambda kv: -kv[1])[:6]
    items = sorted(codes.items(), key=lambda kv: kv[1])
    out_codes = [{'off': off, 'fwd': cb.decode('ascii'), 'rev': cb[::-1].decode('ascii')}
                 for cb, off in items[:cap]]
    return {
        'off_start': cl[0][0], 'off_end': cl[-1][0],
        'n_hits': len(cl), 'n_mov': n_mov, 'n_cmp81': n_cmp81, 'n_cmp3d': n_cmp3d,
        'n_distinct': len(codes),
        'mov_stride_top': top_strides,
        'codes_cap': cap, 'n_codes_listed': len(out_codes),
        'codes': out_codes,
    }

def jaccard(a, b):
    a, b = set(a), set(b)
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)

MASTER = r'D:\tmp2b\fm24-db\evidence\fm24\reports\editor_schema\master.json'

def main():
    master = json.load(open(MASTER, encoding='utf-8'))
    es = master['entity_summary']
    editor_all_codes = set()
    for ent, info in es.items():
        editor_all_codes.update(info['codes'])

    results = {}
    for tag, path in EXES.items():
        size, hits, dt = scan(path)
        by_kind = {}
        for h in hits:
            by_kind.setdefault(h[1], []).append(h)
        distinct = {}
        for h in hits:
            distinct.setdefault(h[3], h[0])
        fwd_set = {cb.decode('ascii') for cb in distinct}
        rev_set = {cb[::-1].decode('ascii') for cb in distinct}
        results[tag] = {
            'path': path, 'size': size, 'scan_sec': round(dt, 1),
            'n_hits': len(hits),
            'n_hits_mov': len(by_kind.get(0, [])),
            'n_hits_cmp81': len(by_kind.get(1, [])),
            'n_hits_cmp3d': len(by_kind.get(2, [])),
            'n_distinct': len(distinct),
            'hits': hits,
            'fwd_set': fwd_set, 'rev_set': rev_set,
        }
        print(f"[{tag}] size={size} scan={dt:.1f}s hits={len(hits)} "
              f"(mov={results[tag]['n_hits_mov']} cmp81={results[tag]['n_hits_cmp81']} "
              f"cmp3d={results[tag]['n_hits_cmp3d']}) distinct4CC={len(distinct)}")
        print(f"[{tag}] jaccard(editor_codes, fwd_set)={jaccard(editor_all_codes, fwd_set):.4f} "
              f"jaccard(editor_codes, rev_set)={jaccard(editor_all_codes, rev_set):.4f}")

    # --- editor-side sanity: reproduce known anchor (0x30 stride mov blocks) ---
    ed = results['editor']
    ed_clusters = build_clusters(ed['hits'])
    print(f"[editor] clusters(>=3 hits, gap<4096): {len(ed_clusters)}")
    best_stride = {}
    ed_hit_codes = {h[3] for h in ed['hits']}
    anchor_found = 0
    for cl in ed_clusters[:400]:
        movs = [h[0] for h in cl if h[1] == 0]
        ds = [b - a for a, b in zip(movs, movs[1:])]
        if ds.count(0x30) >= 5:
            anchor_found += 1
            for h in cl:
                if h[1] == 0 and h[3] not in best_stride:
                    best_stride[h[3]] = h[0]
    print(f"[editor] clusters with mov stride 0x30 x5+: {anchor_found}")
    known = ['cnam', 'cnsm', 'cl3n', 'cnti', 'ccti', 'cpcm', 'crep', 'cext', 'PLgn']
    for k in known:
        kb = k.encode('ascii')
        kb_r = kb[::-1]
        in_ed = kb in ed_hit_codes or kb_r in ed_hit_codes
        print(f"[editor] known code {k}: present-as-hit={in_ed}")

    # --- fm clusters ---
    fm = results['fm']
    fm_clusters = build_clusters(fm['hits'])
    print(f"[fm] clusters(>=3 hits, gap<4096): {len(fm_clusters)}")
    cl_summaries = [cluster_summary(cl) for cl in fm_clusters]
    cl_summaries.sort(key=lambda c: -c['n_hits'])
    n0x30 = sum(1 for c in cl_summaries
                for d, cnt in c['mov_stride_top'] if d == 0x30 and cnt >= 5)
    print(f"[fm] clusters with mov stride 0x30 x5+: {n0x30}")

    # --- comp anchor check on fm.exe ---
    comp_anchor = {}
    for k in known:
        kb = k.encode('ascii')
        kb_r = kb[::-1]
        nf, ff = count_raw(fm['path'], kb)
        nr, fr = count_raw(fm['path'], kb_r)
        ctx = [h for h in fm['hits'] if h[3] == kb or h[3] == kb_r]
        ctx_small = [{'off': h[0], 'kind': ['mov', 'cmp81', 'cmp3d'][h[1]],
                      'reg': hex(h[2]), 'fwd': h[3].decode('ascii'),
                      'rev': h[3][::-1].decode('ascii')} for h in ctx[:12]]
        comp_anchor[k] = {
            'raw_fwd_bytes': nf, 'raw_fwd_first_off': ff,
            'raw_rev_bytes': nr, 'raw_rev_first_off': fr,
            'n_ctx_hits': len(ctx),
            'n_ctx_mov': sum(1 for h in ctx if h[1] == 0),
            'n_ctx_cmp81': sum(1 for h in ctx if h[1] == 1),
            'n_ctx_cmp3d': sum(1 for h in ctx if h[1] == 2),
            'ctx_examples': ctx_small,
        }
        print(f"[fm] anchor {k}: raw(fwd)={nf}@{ff} raw(rev)={nr}@{fr} "
              f"ctx={len(ctx)} (mov={comp_anchor[k]['n_ctx_mov']} "
              f"cmp81={comp_anchor[k]['n_ctx_cmp81']} cmp3d={comp_anchor[k]['n_ctx_cmp3d']})")

    # --- Ssds regression anchor: 81 fa 63 70 61 63 ---
    ssds = b'\x81\xfa\x63\x70\x61\x63'
    ns, fs = count_raw(fm['path'], ssds)
    print(f"[fm] Ssds anchor '81 fa 63 70 61 63': count={ns} first_off={fs}")

    # --- add rax, 0x38 / 0x30 stepper counts ---
    n38, f38 = count_raw(fm['path'], b'\x48\x83\xc0\x38')
    n30, f30 = count_raw(fm['path'], b'\x48\x83\xc0\x30')
    print(f"[fm] '48 83 c0 38' (add rax,0x38): {n38} first={f38}; "
          f"'48 83 c0 30' (add rax,0x30): {n30} first={f30}")

    # --- jaccard per entity, best direction ---
    fm_fwd = fm['fwd_set']; fm_rev = fm['rev_set']
    ent_scores = []
    for ent, info in es.items():
        codes = info['codes']
        jf = jaccard(codes, fm_fwd)
        jr = jaccard(codes, fm_rev)
        best = max(jf, jr)
        ent_scores.append((best, jf, jr, ent, len(codes)))
    ent_scores.sort(reverse=True)
    print("[fm] entity jaccard top5 (best|fwd|rev, entity, n_codes):")
    for best, jf, jr, ent, nc in ent_scores[:5]:
        print(f"  {best:.4f} (fwd={jf:.4f} rev={jr:.4f}) {ent} n={nc}")
    print(f"[fm] union editor codes={len(editor_all_codes)}; "
          f"intersect fwd={len(editor_all_codes & fm_fwd)} rev={len(editor_all_codes & fm_rev)}")

    # --- dump fm JSON deliverable ---
    meta = {
        'exe': fm['path'], 'size': fm['size'], 'scan_sec': fm['scan_sec'],
        'patterns': {
            'mov_imm': 'c7 45 disp8 + 4 bytes; reversed-or-fwd must be [A-Za-z0-9]{4}',
            'cmp81': '81 f8..ff + 4 bytes (cmp r32, imm32; f8=eax..ff=edi)',
            'cmp3d': '3d + 4 bytes (cmp eax, imm32)',
            'cluster': 'gap<4096, keep clusters with >=3 hits',
            'readings': 'fwd = file-order ASCII; rev = byte-reversed (IDA big-endian display)',
        },
        'editor_reference': {
            'exe': ed['path'], 'size': ed['size'],
            'n_hits': ed['n_hits'], 'n_distinct': ed['n_distinct'],
            'clusters_0x30_x5': anchor_found,
            'jaccard_editor_codes_vs_editor_fwd': round(jaccard(editor_all_codes, ed['fwd_set']), 4),
            'jaccard_editor_codes_vs_editor_rev': round(jaccard(editor_all_codes, ed['rev_set']), 4),
        },
        'totals': {
            'n_hits': fm['n_hits'], 'n_mov': fm['n_hits_mov'],
            'n_cmp81': fm['n_hits_cmp81'], 'n_cmp3d': fm['n_hits_cmp3d'],
            'n_distinct4CC': fm['n_distinct'],
            'n_clusters': len(fm_clusters),
            'clusters_kept_top': min(200, len(cl_summaries)),
        },
        'ssds_regression': {'bytes': '81 fa 63 70 61 63', 'count': ns, 'first_off': fs},
        'steppers': {
            'add_rax_0x38': {'count': n38, 'first_off': f38},
            'add_rax_0x30': {'count': n30, 'first_off': f30},
        },
        'overlap': {
            'editor_codes_union': len(editor_all_codes),
            'fm_fwd_intersect': len(editor_all_codes & fm_fwd),
            'fm_rev_intersect': len(editor_all_codes & fm_rev),
            'jaccard_fwd': round(jaccard(editor_all_codes, fm_fwd), 4),
            'jaccard_rev': round(jaccard(editor_all_codes, fm_rev), 4),
        },
        'entity_jaccard_top5': [
            {'entity': ent, 'n_codes': nc, 'best': round(best, 4),
             'fwd': round(jf, 4), 'rev': round(jr, 4)}
            for best, jf, jr, ent, nc in ent_scores[:5]
        ],
    }
    out = {
        'meta': meta,
        'clusters': cl_summaries[:200],
        'comp_anchor_check': comp_anchor,
    }
    outpath = r'D:\tmp2b\fm24-db\scratch\t01\t01a2_fm_sweep.json'
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"[out] wrote {outpath} ({os.path.getsize(outpath)} bytes)")

if __name__ == '__main__':
    main()
