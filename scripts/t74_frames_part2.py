"""t74 builder part 2: 各表行语法模型 + identity-triple 分层 DP。

身份三元组(每表自证,不跨表照抄)[ordinal u32][UID u32][UID u32][尾字节]
  - ordinal == 行下标(rdui 语义)
  - 两处 UID 相等(duni 语义)
  - 尾字节:0=marker(绝大多数表);t24 为 selector(10/11/0)
"""
import numpy as np


def struct_u32(b, p):
    return int.from_bytes(b[p:p + 4], "little")


def lstr(b, p, e):
    """长度前缀 UTF-8 串;非法返回 None。"""
    if p + 4 > e:
        return None
    n = struct_u32(b, p)
    if n > 4096 or p + 4 + n > e:
        return None
    try:
        t = b[p + 4:p + 4 + n].decode("utf-8")
    except UnicodeDecodeError:
        return None
    return (p + 4 + n, n, t) if t and t.isprintable() else None

# (archive, table) -> (stride, header, footer)
FIXED = {
    ("client", 56): (13, 14, 8), ("server", 56): (13, 14, 8),
    ("client", 0): (77, 14, 8), ("server", 0): (77, 14, 8),
    ("client", 21): (38, 14, 8), ("server", 21): (181, 14, 8),
}


def _scan(b, tag, lo, hi, n, W=13, strict_uid=True, pair=True):
    """四对齐 × 相位向量扫描,返回 {ordinal: [(pos, uid)]}."""
    m, cand = len(b), {}
    for off in range(4):
        cnt = (m - off - 3) // 4
        if cnt <= 2:
            continue
        w = np.frombuffer(b, dtype="<u4", count=cnt, offset=off)
        o, u1, u2 = w[:cnt - 2], w[1:cnt - 1], w[2:cnt]
        mask = (o < n) & (u1 > 0)
        if pair:
            mask &= (u1 == u2)
        idx = np.nonzero(mask)[0]
        if not len(idx):
            continue
        pos = idx * 4 + off
        keep = (pos >= lo) & (pos + W <= hi)
        for p, oo, uu in zip(pos[keep].tolist(), o[idx][keep].tolist(), u1[idx][keep].tolist()):
            cand.setdefault(oo, []).append((p, uu))
    for k in cand:
        cand[k].sort()
    return cand


def _dp(b, tag, lo, hi, n, W=13, strict_uid=True, pair=True):
    """ordinal 递增 + UID 递增 + 不重叠的精确铺法计数,返回 (路径数, 行首, 层)。"""
    cand = _scan(b, tag, lo, hi, n, W, strict_uid, pair)
    if any(i not in cand for i in range(n)):
        return 0, None, None
    states = {(lo, 0): (1, None)}
    layers = [dict(states)]
    for i in range(n):
        nxt = {}
        for (q, pu), (c, _) in states.items():
            for p, u in cand[i]:
                if p < q or p + W > hi:
                    if p >= q:
                        break
                    continue
                if strict_uid and u <= pu:
                    continue
                key = (p + W, u)
                prev = nxt.get(key)
                nxt[key] = (c + (prev[0] if prev else 0), (q, pu))
        if not nxt:
            return 0, None, layers
        states = nxt
        layers.append(dict(states))
    fin = [k for k in states if k[0] == hi]
    if not fin:
        return 0, None, layers
    cnt = sum(states[k][0] for k in fin)
    cur, starts = fin[0], [0] * n
    for i in range(n, 0, -1):
        q, pu = layers[i][cur][1]
        starts[i - 1] = q
        cur = (q, pu)
    return cnt, starts, layers


# ------------------------------------------------------- 定长表
def fixed_rows(b, spec):
    stride, H, F = spec
    n = struct_u32(b, 8)
    if H + n * stride + F != len(b):
        return None
    rows = [(H + i * stride, H + (i + 1) * stride) for i in range(n)]
    bad = sum(1 for i, (s, e) in enumerate(rows)
              if not _ident_at(b, e - 13, i))
    return dict(rows=rows, closure=True, bad_identity=bad, rows_n=n)


def _ident_at(b, p, i):
    o = struct_u32(b, p)
    u1 = struct_u32(b, p + 4)
    u2 = struct_u32(b, p + 8)
    return o == i and u1 == u2 and u1 > 0


def _dp_rows(b, n, H, F, W=13):
    """DP 唯一铺法 -> 行首序列;行尾取下一行首。"""
    cnt, starts, _ = _dp(b, "row", H, len(b) - F, n, W)
    if cnt != 1 or not starts:
        return None
    hi = len(b) - F
    rows = list(zip(starts, starts[1:] + [hi]))
    bad = sum(1 for i, (s, e) in enumerate(rows) if not _ident_at(b, e - W, i))
    return dict(rows=rows, closure=True, bad_identity=bad, rows_n=n, paths=cnt)


# ------------------------------------------------------- 变长表
def seq_lang(b, n, H=14, F=8):
    """[u32 len][name][17B][13B identity];后缀 = 17+13 = 30B。"""
    e_all = len(b) - F
    p, rows = H, []
    while p < e_all:
        r = lstr(b, p, e_all)
        if not r:
            return None
        q = r[0] + 30
        if q > e_all:
            return None
        rows.append((p, q))
        p = q
    if p != e_all or len(rows) != n:
        return None
    bad = sum(1 for i, (s, e) in enumerate(rows) if not _ident_at(b, e - 13, i))
    return dict(rows=rows, closure=True, bad_identity=bad, rows_n=n)


def seq_weat(b, n, H=14, F=8):
    """[u32 len][name][95B][13B identity]。"""
    e_all = len(b) - F
    p, rows = H, []
    while p < e_all:
        L = struct_u32(b, p)
        if not (0 < L < 200):
            return None
        q = p + 4 + L + 95 + 13
        if q > e_all:
            return None
        rows.append((p, q))
        p = q
    if p != e_all or len(rows) != n:
        return None
    bad = sum(1 for i, (s, e) in enumerate(rows) if not _ident_at(b, e - 13, i))
    return dict(rows=rows, closure=True, bad_identity=bad, rows_n=n)


def seq_derby(b, n, const, H=14, F=8):
    """k 个 lstr 名(k=2 常见,4 少数)+ (const-4k) 数字段 + 13B identity。"""
    e_all = len(b) - F
    p, rows = H, []
    while p < e_all:
        q, tot, k = p, 0, 0
        while k < 8:
            r = lstr(b, q, e_all)
            if not r:
                break
            q, nl = r[0], r[1]
            tot, k = tot + nl, k + 1
        if k < 2 or (q - p) != tot + 4 * k:
            return None
        e = p + tot + const
        if e > e_all:
            return None
        rows.append((p, e))
        p = e
    if p != e_all or len(rows) != n:
        return None
    bad = sum(1 for i, (s, e) in enumerate(rows) if not _ident_at(b, e - 13, i))
    return dict(rows=rows, closure=True, bad_identity=bad, rows_n=n)


def seq_lcrg(b, n, H=14, F=8):
    """identity-triple DP(41+5k 变长由 DP 自证)。"""
    return _dp_rows(b, n, H, F)


def seq_media7(b, n, H=14, F=8):
    return _dp_rows(b, n, H, F)


def seq_team24(b, n, H=14, F=8):
    return _dp_rows(b, n, H, F)
