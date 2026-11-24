#!/usr/bin/env python3
"""t05 — 把 EDITOR_SCHEMA_FIELDS.md 解析成机读实体字段序列(对齐法的输入)。

产出 scratch/t05/schema_inventory.json:
  entities[<name>] = {
    code, declared_fields, top_level, scalars, lists,
    fields: [ {idx, code, name, type, optional, list, list_of, parent} ... ]   # 保序
  }
  type_width_candidates = 类型 -> 候选线宽 + 依据

用法:
  py -V:3.12 -I -B scripts/t05_schema.py
  py -V:3.12 -I -B scripts/t05_schema.py --entity club
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMA_MD = pathlib.Path(str(_cfg.EDITOR_SCHEMA_FIELDS_MD))
OUT = ROOT / "scratch/t05/schema_inventory.json"

DB_ENTITIES = {
    "agent", "agreement", "alternative names", "award", "city", "club b team",
    "club c team", "club d team", "club", "comp", "continent", "contract",
    "currency", "derby", "description", "injury", "journalist", "language",
    "local region", "media source", "nation", "non player", "official",
    "person name", "person", "player", "region", "stadium", "stage name",
    "team kit", "team", "weather",
}

# 类型 -> 候选线宽(1/2/4/8 字节)。依据:本项目 E20/E32/t02 已验的行内编码 + 常规二进制序列化。
# 注意:这是"候选",不是结论;对齐器需要用行宽与数据合法性来消歧。
TYPE_WIDTHS: dict[str, dict] = {
    "boolean":            {"candidates": [1, 0], "note": "常打包位域;共享字节时对单字段可视作 0 宽"},
    "enum":               {"candidates": [1, 2, 4], "note": "枚举基数<256 时多为 1B"},
    "multiple_enum":      {"candidates": [1, 2, 4], "note": "位掩码,常 1/2B"},
    "day_of_week":        {"candidates": [1], "note": "7 位掩码"},
    "integer":            {"candidates": [1, 2, 4], "note": "按取値范围消歧"},
    "date":               {"candidates": [2, 4], "note": "常见 2B 年+日;也可能是 4B 序列号"},
    "colour":             {"candidates": [3, 4], "note": "RGB 3B 或 ARGB 4B"},
    "real":               {"candidates": [4], "note": "float32"},
    "cash":               {"candidates": [4], "note": "int32"},
    "short_distance":     {"candidates": [1, 2], "note": "短整型"},
    "database_record_unique_id": {"candidates": [4], "note": "u32 引用;空值 0xFFFFFFFF"},
    "unique_id":          {"candidates": [8], "note": "u64 或两个相等 u32(本项目 duni 惯例)"},
    "string":             {"candidates": [4, 0], "note": "行内多为 u32 名称引用;0=名称在 lang 表"},
    "picture":            {"candidates": [4, 0], "note": "同 string"},
    "list":               {"candidates": [0], "note": "元素不内联:行内只有计数/段;元素布局单列"},
    "database_record_list": {"candidates": [0], "note": "同上"},
    "button":             {"candidates": [0], "note": "UI 专用,不参与序列化"},
    "label":              {"candidates": [0], "note": "UI 专用"},
    "min_and_max":        {"candidates": [2, 4], "note": "两字段"},
    "string_and_sort_order": {"candidates": [4, 0], "note": "字符串+序号"},
    "player_attribute":   {"candidates": [1], "note": "0-100 或 1-20 的单字节"},
    "large":              {"candidates": [4, 8], "note": "64 位整数"},
}


def parse() -> dict:
    text = SCHEMA_MD.read_text(encoding="utf-8")
    pat = re.compile(r"### (.+?)（记录标识 `([A-Za-z0-9]+)`，(\d+) 个字段）(.*?)(?=\n### )", re.S)
    out: dict[str, dict] = {}
    for m in pat.finditer(text):
        name, code, declared, body = m.group(1).strip(), m.group(2), int(m.group(3)), m.group(4)
        fields: list[dict] = []
        cur_list: str | None = None
        idx = 0
        for line in body.splitlines():
            if not line.startswith("|") or line.startswith("| 字段代码") or line.startswith("|---"):
                continue
            indented = "\u3000" in line[:8]
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 3:
                continue
            raw0 = cells[0]
            if "↳" in raw0:
                mm = re.search(r"（([A-Za-z0-9]+)）", raw0)
                cur_list = mm.group(1) if mm else None
                continue
            fc = raw0.strip("`").strip()
            if not fc:
                continue
            ty = cells[2]
            fields.append({
                "idx": idx,
                "code": fc,
                "name": cells[1],
                "type": ty,
                "optional": ("可选" in cells[3]) or ("可选" in cells[2]),
                "list": indented,
                "parent": cur_list if indented else None,
            })
            idx += 1
        top = [f for f in fields if not f["list"]]
        out[name] = {
            "code": code,
            "declared_fields": declared,
            "top_level": len(top),
            "scalars": len([f for f in top if "list" not in f["type"]]),
            "lists": len([f for f in top if "list" in f["type"]]),
            "sub_fields": len(fields) - len(top),
            "fields": fields,
        }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--entity")
    args = ap.parse_args()

    ents = parse()
    db = {k: v for k, v in ents.items() if k in DB_ENTITIES}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": str(SCHEMA_MD),
        "entities_all": len(ents),
        "entities_db": len(db),
        "type_width_candidates": TYPE_WIDTHS,
        "entities": db,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")

    if args.entity:
        e = db.get(args.entity)
        if not e:
            print("未找到实体:", args.entity, "可选:", ", ".join(db))
            return 1
        print(f"{args.entity} code={e['code']} 声明={e['declared_fields']} 顶层={e['top_level']} "
              f"标量={e['scalars']} 列表={e['lists']} 子字段={e['sub_fields']}")
        for f in e["fields"]:
            mark = "  └" if f["list"] else "   "
            print(f"{mark} {f['idx']:>3} {f['code']:<6} {f['type']:<28} {f['name'][:34]}"
                  + ("  (可选)" if f["optional"] else "")
                  + (f"  [list of {f['parent']}]" if f["parent"] else ""))
        return 0

    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"实体: 全文档 {len(ents)} / 数据库 {len(db)}")
    print(f"{'entity':<18}{'code':<6}{'声明':>5}{'顶层':>5}{'标量':>5}{'列表':>5}{'子字段':>6}")
    for k, v in sorted(db.items(), key=lambda x: -x[1]["declared_fields"]):
        print(f"{k:<18}{v['code']:<6}{v['declared_fields']:>5}{v['top_level']:>5}"
              f"{v['scalars']:>5}{v['lists']:>5}{v['sub_fields']:>6}")
    tot = sum(v["scalars"] for v in db.values())
    print(f"{'合计':<18}{'':<6}{sum(v['declared_fields'] for v in db.values()):>5}"
          f"{sum(v['top_level'] for v in db.values()):>5}{tot:>5}"
          f"{sum(v['lists'] for v in db.values()):>5}{sum(v['sub_fields'] for v in db.values()):>6}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
