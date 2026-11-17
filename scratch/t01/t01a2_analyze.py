# t01-a2 follow-up v2: fix tuple bug, add windowed editor-code density profile.
import re, os, json

EXE = r'D:\tmp2b\fm24\input\fm.exe'
MASTER = r'D:\tmp2b\fm24-db\evidence\fm24\reports\editor_schema\master.json'
CHUNK = 32 * 1024 * 1024
C = rb'[A-Za-z0-9]'
PATS = [
    ('mov', re.compile(rb'\xc7\x45.(' + C + rb'{4})')),
    ('cmp81', re.compile(rb'\x81[\xf8-\xff](' + C + rb'{4})')),
    ('cmp3d', re.compile(rb'\x3d(' + C + rb'{4})')),
]

def scan():
    hits = []
    with open(EXE, 'rb') as f:
        chunk_start = 0
        prev_tail = b''
        while True:
            data = f.read(CHUNK)
            if not data:
                break
            buf = prev_tail + data
            b0 = chunk_start - len(prev_tail)
            for ki, (name, rx) in enumerate(PATS):
                for m in rx.finditer(buf):
                    s = b0 + m.start()
                    if s < chunk_start:
                        continue
                    hits.append((s, ki, m.group(1)))
            prev_tail = data[-8:]
            chunk_start += len(data)
    hits.sort()
    return hits

def clusters(hits, gap=4096, minh=3):
    out, cur = [], [hits[0]]
    for h in hits[1:]:
        if h[0] - cur[-1][0] < gap:
            cur.append(h)
        else:
            if len(cur) >= minh: out.append(cur)
            cur = [h]
    if len(cur) >= minh: out.append(cur)
    return out

def find_all_ci(needle):
    rx = re.compile(re.escape(needle), re.IGNORECASE)
    n = 0; first = None
    with open(EXE, 'rb') as f:
        chunk_start = 0; prev_tail = b''
        while True:
            data = f.read(CHUNK)
            if not data: break
            buf = prev_tail + data
            b0 = chunk_start - len(prev_tail)
            for m in rx.finditer(buf):
                a = b0 + m.start()
                if a >= chunk_start:
                    n += 1
                    if first is None: first = a
            prev_tail = data[-8:]
            chunk_start += len(data)
    return n, first

def hx(x): return f'0x{x:X}'

def main():
    master = json.load(open(MASTER, encoding='utf-8'))
    es = master['entity_summary']
    ed_codes = set()
    for ent, info in es.items():
        ed_codes.update(info['codes'])
    ed_rev = {c[::-1] for c in ed_codes}
    print(f'editor codes union={len(ed_codes)}')

    hits = scan()
    cls = clusters(hits)
    print(f'fm hits={len(hits)} clusters={len(cls)}')

    # distribution of editor-code matches per cluster
    per = []
    for cl in cls:
        codes = {}
        for off, ki, cb in cl:
            if cb not in codes: codes[cb] = (off, ki)
        inter = [cb for cb in codes if cb in ed_rev]
        per.append((len(inter), cl, codes, inter))
    per.sort(key=lambda t: -t[0])
    dist = {}
    for n_ed, *_ in per:
        dist[n_ed] = dist.get(n_ed, 0) + 1
    print('editor-matches-per-cluster histogram (n_matches: n_clusters):',
          dict(sorted(dist.items())))
    for n_ed, cl, codes, inter in per[:5]:
        if n_ed == 0: break
        kinds = [h[1] for h in cl]
        print(f'  off={hx(cl[0][0])}..{hx(cl[-1][0])} n={len(cl)} editor={n_ed}/{len(codes)} '
              f'mov={kinds.count(0)} cmp81={kinds.count(1)} cmp3d={kinds.count(2)}')
        for cb in inter[:8]:
            off, ki = codes[cb]
            print(f'    {cb[::-1].decode("ascii")} @ {hx(off)} kind={["mov","cmp81","cmp3d"][ki]}')

    # mov blocks with stride 0x30 x4+
    reg_blocks = []
    for cl in cls:
        movs = [(h[0], h[2]) for h in cl if h[1] == 0]
        if len(movs) < 4: continue
        offs = [o for o, _ in movs]
        ds = [b - a for a, b in zip(offs, offs[1:])]
        if ds.count(0x30) >= 4:
            codes_hit = sum(1 for _, cb in movs if cb in ed_rev)
            reg_blocks.append((codes_hit, len(movs), cl[0][0], cl[-1][0], [cb for _, cb in movs]))
    reg_blocks.sort(key=lambda t: (-t[0], -t[1]))
    print(f'\nfm mov-blocks with stride 0x30 x4+: {len(reg_blocks)}')
    for ch, nm, o0, o1, cbs in reg_blocks[:8]:
        names = [cb[::-1].decode('ascii') for cb in cbs]
        print(f'  off={hx(o0)}..{hx(o1)} n_mov={nm} editor_match={ch} codes: {names[:20]}')

    # windowed density profile of editor-code hits (rev reading), 1MB windows
    WIN = 1 << 20
    prof = {}
    for off, ki, cb in hits:
        if cb in ed_rev:
            prof.setdefault(off // WIN, []).append((off, ki, cb))
    top = sorted(prof.items(), key=lambda kv: -len(kv[1]))[:10]
    print('\n1MB windows with most editor-code hits:')
    for w, hs in top:
        kinds = [h[1] for h in hs]
        print(f'  win {hx(w * WIN)}..{hx((w + 1) * WIN)} n={len(hs)} '
              f'mov={kinds.count(0)} cmp81={kinds.count(1)} cmp3d={kinds.count(2)} '
              f'first_code={hs[0][2][::-1].decode("ascii")}')

    # Ssds anchor offset check
    print(f'\nSsds anchor file_off=0x49A06F2? = {hx(77200626)}; '
          f'sub_1449A06C0 RVA=0x49A06C0 -> delta={hx(77200626 - 0x49A06C0)}')

    # case-insensitive variants for missing anchors
    for code in ['cnsm', 'cl3n']:
        nb, fb = find_all_ci(code.encode())
        nr, fr = find_all_ci(code.encode()[::-1])
        print(f'{code}: ci-fwd={nb}@{fb and hx(fb)} ci-rev={nr}@{fr and hx(fr)}')

    # editor codes seen in fm by context
    hitmap = {}
    for off, ki, cb in hits:
        hitmap.setdefault(cb, set()).add(ki)
    any_hit = sum(1 for c in ed_rev if c in hitmap)
    any_mov = sum(1 for c in ed_rev if 0 in hitmap.get(c, set()))
    any_cmp = sum(1 for c in ed_rev if hitmap.get(c, set()) & {1, 2})
    print(f'\neditor codes in fm: any={any_hit}/{len(ed_rev)} '
          f'with-mov-context={any_mov} with-cmp-context={any_cmp}')

if __name__ == '__main__':
    main()
