"""t74 builder part 3: 敏感性网格(identity 宽度自证)+ fm24_dump 锚点回归。

锚点口径(与 fm24_dump 一致,勿混):
  rdui (Random ID) = 行序号,值 == 行下标
  duni (Unique ID) = 行 UID,值 == 该行 identity 的 UID(两处分相等)
纠正:任务简报把 media 归到 t7(rdui@3/duni@7),但 fm24_dump FIELDS 该条目实为
  ("client", 6) = {rdui:3, duni:7}(行 16B 定长,115 行)。t7 在 FIELDS 中无条目。
  lcrg 的 rdui@-13/duni@-9 来自 fm24_dump OVERRIDE("client",47),非 FIELDS。
"""
import struct
from t74_frames_part2 import _dp

# (archive, table) -> {slot: 行内偏移(负数相对行尾)}
ANCHORS = {
    ("client", 21): {"rdui": 25, "duni": 29, "Scti": 3, "Slat": 17, "Slon": 21},
    ("client", 0): {"rdui": 64, "duni": 68},
    ("client", 56): {"rdui": 0, "duni": 4},
    ("client", 47): {"rdui": -13, "duni": -9},
    ("client", 6): {"rdui": 3, "duni": 7},     # 对照表(不在本任务 9 表内)
}
# t8 的 rdui_suffix@17 是"30B 后缀内偏移 17",不是行内偏移
SUFFIX_ANCHORS = {("client", 8): {"rdui_suffix": 17}}


def sens_grid(b, n, lo, Ws=(12, 13, 14), foots=(7, 8, 9, 10, 12), pair=True):
    """{(W, footer): 路径数};每点独立重算 hi = len(b) - footer。"""
    out = {}
    for W in Ws:
        for fo in foots:
            hi = len(b) - fo
            if hi <= lo:
                out[(W, fo)] = -1
                continue
            paths, bounds, _ = _dp(b, "sens", lo, hi, n, W, strict_uid=True, pair=pair)
            out[(W, fo)] = paths
    return out


def anchor_report(b, rows, table_arch):
    """rdui 必须 == 行下标;duni 必须 == 该行 UID(与 rdui+4 处相等)。"""
    spec = ANCHORS.get(table_arch)
    if not spec or not rows:
        return None
    rep = {}
    for name, off in spec.items():
        if name not in ("rdui", "duni"):
            continue
        hit = tot = 0
        for i, (s, e) in enumerate(rows):
            p = e + off if off < 0 else s + off
            if p < 0 or p + 4 > len(b):
                continue
            tot += 1
            v = struct.unpack_from("<I", b, p)[0]
            if name == "rdui":
                if v == i:
                    hit += 1
            else:  # duni: 与 identity 内第二个 UID 副本相等
                u = struct.unpack_from("<I", b, p + 4)[0] if p + 8 <= len(b) else None
                if u is not None and v == u:
                    hit += 1
        rep[name] = {"offset": off, "hit": hit, "total": tot, "ok": (hit == tot and tot > 0)}
    return rep


def suffix_anchor_report(b, rows_with_suffix, table_arch):
    """t8: suffix 起点 + 17 处 == 行下标。rows_with_suffix = [(i, suffix_start)]."""
    spec = SUFFIX_ANCHORS.get(table_arch)
    if not spec:
        return None
    rep = {}
    for name, off in spec.items():
        hit = 0
        for i, sp in rows_with_suffix:
            if sp + off + 4 <= len(b) and struct.unpack_from("<I", b, sp + off)[0] == i:
                hit += 1
        rep[name] = {"suffix_offset": off, "hit": hit, "total": len(rows_with_suffix),
                     "ok": hit == len(rows_with_suffix) and len(rows_with_suffix) > 0}
    return rep


def geo_report(b, rows, table_arch):
    """stadium Scti/Slat/Slon:只报告字节位置与值域,不断言语义。"""
    if table_arch != ("client", 21):
        return None
    out = {}
    for name, off in (("Scti", 3), ("Slat", 17), ("Slon", 21)):
        vals = [struct.unpack_from("<I", b, s + off)[0] for s, e in rows[:2000]]
        out[name] = {"offset": off, "min": min(vals), "max": max(vals), "distinct": len(set(vals))}
    return out
