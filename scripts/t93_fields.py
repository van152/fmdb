"""t93: build field_dictionary.json from fmsave model/reader sources by READING them.

Never imports fmsave. Parses `class X:` bodies for `    name: type` dataclass fields and
collects the register_field_statuses() verdicts, plus the reader module's docstring/region.

Usage:
  py -V:3.12 -I -B scripts/t93_fields.py --help
  py -V:3.12 -I -B scripts/t93_fields.py --selftest
  py -V:3.12 -I -B scripts/t93_fields.py --out scratch/t93/outbox.md/field_dictionary.json
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXT = REPO / "scratch" / "ext" / "fmsave"
PROVENANCE = "ext/fmsave@755fe9c566bb0497d4ad6ef6e1ac1fd2fde7351b"

PRIORITY = ("Player", "Staff", "Club", "Nation", "Contract", "Competition", "Stadium", "Team")


def rel(path: Path) -> str:
    return path.relative_to(EXT).as_posix()


def parse_model(path: Path) -> dict[str, dict]:
    """Return {class: {fields: [(name, type, line)], verified: [...], unconfirmed: [...]}}."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    out: dict[str, dict] = {}
    cls = None
    for i, line in enumerate(lines, 1):
        m = re.match(r"^class (\w+)", line)
        if m:
            cls = m.group(1)
            out[cls] = {"fields": [], "verified": [], "unconfirmed": [], "doc": []}
            continue
        if cls is None:
            continue
        f = re.match(r"^    (\w+) *: *(.+?)(?: *=.*)?$", line)
        if f and not line.startswith("     "):
            out[cls]["fields"].append([f.group(1), f.group(2).strip(), i])
        d = re.match(r"^        (\w+): (\S.*)$", line)
        if d:
            out[cls]["doc"].append([d.group(1), d.group(2)])
    # statuses: balanced-paren scan from each register_field_statuses( call
    for m in re.finditer(r"register_field_statuses\(", text):
        start = m.end() - 1
        depth = 0
        end = start
        while end < len(text):
            ch = text[end]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    break
            end += 1
        call = text[start + 1 : end]
        name = re.match(r"\s*(\w+)", call)
        if name is None or name.group(1) not in out:
            continue
        name = name.group(1)
        for key in ("verified", "unconfirmed"):
            sub = re.search(key + r"=\((.*?)\)", call, re.S)
            if sub:
                out[name][key] = re.findall(r'"(\w+)"', sub.group(1))
    return out


def reader_regions() -> dict[str, str]:
    """{reader module: section region} from readers/_common.py constants + module docstring."""
    common = (EXT / "src/fmsave/readers/_common.py").read_text(encoding="utf-8")
    consts = dict(re.findall(r'^(\w+_SECTION) = "([^"]+)"', common, re.M))
    out: dict[str, str] = {}
    for path in sorted((EXT / "src/fmsave/readers").glob("*.py")):
        if path.name.startswith("_"):
            continue
        head = path.read_text(encoding="utf-8").splitlines()[:1]
        doc = head[0].strip().strip('"') if head else ""
        region = "game_db"
        for key, val in consts.items():
            if key.split("_")[0].lower() in path.stem:
                region = val
        out[path.stem] = {"region": region, "doc": doc}
    return out


def build() -> dict:
    models = {}
    for path in sorted((EXT / "src/fmsave/models").glob("*.py")):
        if path.name == "__init__.py":
            continue
        for cls, data in parse_model(path).items():
            if not data["fields"]:
                continue
            data["file"] = rel(path)
            models[cls] = data
    readers = reader_regions()
    entities = []
    for cls in PRIORITY + tuple(sorted(set(models) - set(PRIORITY))):
        data = models.get(cls)
        if data is None:
            continue
        semantics: dict[str, str] = {}
        for k, v in data["doc"]:
            semantics.setdefault(k, " ".join(v.split()))
        fields = []
        for name, typ, line in data["fields"]:
            grade = "unstated"
            if name in data["verified"]:
                grade = "verified"
            elif name in data["unconfirmed"]:
                grade = "unconfirmed"
            fields.append(
                {
                    "name": name,
                    "type": typ,
                    "file": data["file"],
                    "line": line,
                    "ext_status": grade,
                    "semantics": semantics.get(name),
                }
            )
        entities.append(
            {
                "entity": cls,
                "priority": cls in PRIORITY,
                "file": data["file"],
                "field_count": len(fields),
                "verified_count": len(data["verified"]),
                "unconfirmed_count": len(data["unconfirmed"]),
                "fields": fields,
            }
        )
    return {
        "schema": "t93/field_dictionary/v1",
        "provenance": PROVENANCE,
        "method": "read-only parse of scratch/ext/fmsave/src/fmsave/{models,readers}; no import",
        "ext_status_vocabulary": {
            "verified": "fmsave's own register_field_statuses(verified=...) list",
            "unconfirmed": "fmsave's own register_field_statuses(unconfirmed=...) list",
            "unstated": "field has no entry in either list",
        },
        "grade_policy": "ext_status is fmsave's internal claim; it is NOT our L1-L4 grade",
        "entity_count": len(entities),
        "field_total": sum(e["field_count"] for e in entities),
        "entities": entities,
        "readers": readers,
    }


def selftest() -> int:
    data = build()
    assert data["entity_count"] >= 30, data["entity_count"]
    assert data["field_total"] >= 300, data["field_total"]
    by = {e["entity"]: e for e in data["entities"]}
    for key in ("Player", "Staff", "Club", "Nation"):
        assert key in by, key
        assert by[key]["field_count"] > 0, key
    assert by["Player"]["verified_count"] >= 10
    for e in data["entities"]:
        for f in e["fields"]:
            assert (EXT / f["file"]).is_file(), f["file"]
    print("selftest OK:", data["entity_count"], "entities,", data["field_total"], "fields")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    data = build()
    if args.out:
        Path(args.out).write_text(
            json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
        )
        print("wrote", args.out, data["entity_count"], "entities", data["field_total"], "fields")
    else:
        print(json.dumps({e["entity"]: e["field_count"] for e in data["entities"]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
