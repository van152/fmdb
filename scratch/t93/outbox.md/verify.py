"""t93 step 7 -- independent verification of the outbox.

Nine checks, each of which fails loudly. This file never imports, runs or shells out to
anything in scratch/ext; the only executables it can reach are its own read/hash routines.

    py -V:3.12 -I -B scratch/t93/outbox.md/verify.py
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "scratch" / "t93" / "outbox.md"

REPOS = {
    "fmsave": "755fe9c566bb0497d4ad6ef6e1ac1fd2fde7351b",
    "fm-editor": "ba605f4b64137dfc18940a69ecb2f523007f3ea8",
    "FMLibreEditor": "fb76023fc28c53ddc851ad1afdaf9879d3534d5c",
}

BASELINE_SHA = {
    "scratch/t92/out/schema_v113.json":
        "e4175578d587e201b7d0b14bd15c69c967679049d4a0d236cd4f9e861944254e",
    "scratch/t88/out3/slots.json":
        "f1050953d19da7ea30902f3cc11ee4eb0cf1e55b1f4ca8be408f7f2026663420",
    "reports/stage2_table_identity.json":
        "f2533a06de4e79c19b26d93c4f51471da7c0552d45a0c20b54ccc31c4f5b14c7",
}

DELIVERABLES = [
    "README.md",
    "save_grammar.json",
    "field_dictionary.json",
    "fm24_memory_layout.json",
    "fm27_recon_digest.json",
    "crosswalk.json",
    "verify.py",
    "REPORT.md",
    "DONE.md",
]

# Intermediate output of scripts/t93_fm24.py kept from an earlier pass: the same 270 fields
# and 15 sub-records as fm24_memory_layout.json but without the curated facts. It is not a
# deliverable; it is listed so the outbox listing check can tell it from a stray file.
INTERMEDIATE = ["fm24_fields.json"]

FORBIDDEN = (
    r"^\s*import\s+fmsave\b",
    r"^\s*from\s+fm(?:save|\.)\S*\s+import\b",
    r"\bpip\s+install\b",
    r"\bsubprocess\b",
    r"\bos\.system\b",
    r"\bcargo\s+(build|run)\b",
    r"\bpython\s+-m\s+fmsave\b",
)

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load(name: str) -> dict:
    with (OUT / name).open(encoding="utf-8") as fh:
        return json.load(fh)


def lines_of(rel: str) -> list[str] | None:
    path = ROOT / "scratch" / "ext" / rel
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def check_provenance() -> None:
    bad = []
    for repo, want in REPOS.items():
        head = ROOT / "scratch" / "ext" / repo / ".git" / "HEAD"
        if not head.is_file():
            bad.append(f"{repo}: no .git/HEAD")
            continue
        ref = head.read_text(encoding="utf-8").strip()
        if ref.startswith("ref:"):
            target = ROOT / "scratch" / "ext" / repo / ".git" / ref.split(" ", 1)[1].strip()
            ref = target.read_text(encoding="utf-8").strip() if target.is_file() else ""
        if ref != want:
            bad.append(f"{repo}: {ref[:12]} != {want[:12]}")
    check("1 three repos at the frozen commits", not bad, "; ".join(bad))

    declared = {
        "save_grammar.json": "ext/fmsave@",
        "fm24_memory_layout.json": "ext/fm-editor@",
        "fm27_recon_digest.json": "ext/FMLibreEditor@",
    }
    bad = []
    for name, prefix in declared.items():
        prov = json.dumps(load(name).get("provenance"), ensure_ascii=False)
        hit = [p for p in re.findall(r"ext/[A-Za-z-]+@[0-9a-f]{40}", prov)]
        if not hit or not all(h.startswith(prefix) for h in hit):
            bad.append(f"{name}: {prov[:60]}")
        for h in hit:
            repo = h.split("@")[0].split("/", 1)[1]
            if REPOS.get(repo) != h.split("@")[1]:
                bad.append(f"{name}: {h} mismatch")
    check("2 provenance strings name the frozen commits", not bad, "; ".join(bad))


def check_baseline() -> None:
    bad = []
    for rel, want in BASELINE_SHA.items():
        path = ROOT / rel
        if not path.is_file():
            bad.append(f"{rel}: missing")
        elif sha256(path) != want:
            bad.append(f"{rel}: sha256 drift")
    check("3 internal baseline artifacts unchanged (read-only respected)", not bad, "; ".join(bad))


def check_grammar_lines() -> None:
    grammar = load("save_grammar.json")["grammar"]
    bad, checked = [], 0
    for entry in grammar:
        ev = entry.get("evidence") or []
        if not ev:
            bad.append(f"{entry['id']}: no evidence")
            continue
        for e in ev:
            checked += 1
            lines = lines_of("fmsave/" + e["file"])
            if lines is None:
                bad.append(f"{entry['id']}: {e['file']} missing")
            elif not (1 <= e["line"] <= len(lines)):
                bad.append(f"{entry['id']}: {e['file']}:{e['line']} out of range")
            elif not lines[e["line"] - 1].strip():
                bad.append(f"{entry['id']}: {e['file']}:{e['line']} blank")
    check(
        f"4 save_grammar evidence lines exist ({len(grammar)} entries, {checked} anchors)",
        not bad,
        "; ".join(bad[:6]),
    )


def check_memory_lines() -> None:
    doc = load("fm24_memory_layout.json")
    bad, checked = [], 0
    for f in doc["fields"]:
        checked += 1
        lines = lines_of("fm-editor/" + f["file"])
        if lines is None:
            bad.append(f"{f['key']}: {f['file']} missing")
        elif not (1 <= f["line"] <= len(lines)):
            bad.append(f"{f['key']}: {f['file']}:{f['line']} out of range")
    for c in doc["curated_facts"]:
        checked += 1
        lines = lines_of("fm-editor/" + c["file"])
        if lines is None:
            bad.append(f"{c['id']}: {c['file']} missing")
        elif not (1 <= c["line"] <= len(lines)):
            bad.append(f"{c['id']}: {c['file']}:{c['line']} out of range")
        elif not lines[c["line"] - 1].strip():
            bad.append(f"{c['id']}: {c['file']}:{c['line']} blank")
    note = json.dumps(
        {
            "domain": doc.get("domain"),
            "domain_note": doc.get("domain_note"),
            "flag": doc.get("memory_layout_is_not_wire"),
        },
        ensure_ascii=False,
    ).lower()
    ok_note = "not the save-file wire format" in note and doc.get("memory_layout_is_not_wire") is True
    check(
        f"5 fm24_memory_layout lines exist ({checked} anchors) and declares memory!=wire",
        not bad and ok_note,
        "; ".join(bad[:6]) or ("" if ok_note else "domain note missing"),
    )


def check_recon_lines() -> None:
    doc = load("fm27_recon_digest.json")
    bad, checked = [], 0
    for d in doc["docs"]:
        lines = lines_of("FMLibreEditor/" + d["file"]) if d.get("file") else lines_of(
            "FMLibreEditor/docs/recon/" + d["doc"]
        )
        if lines is None:
            bad.append(f"{d['doc']}: missing")
            continue
        if d["line_count"] != len(lines):
            bad.append(f"{d['doc']}: line_count {d['line_count']} != {len(lines)}")
        first = next((x.strip() for x in lines if x.strip()), "")
        if d["title"] and d["title"] not in first:
            bad.append(f"{d['doc']}: title not on first non-blank line")
        pts = d["key_points"]
        if not 3 <= len(pts) <= 8:
            bad.append(f"{d['doc']}: {len(pts)} points (want 3..8)")
        for p in pts:
            checked += 1
            if not (1 <= p["line"] <= len(lines)):
                bad.append(f"{d['doc']}:{p['line']} out of range")
            elif not lines[p["line"] - 1].strip():
                bad.append(f"{d['doc']}:{p['line']} blank")
    check(
        f"6 recon digest: {len(doc['docs'])} docs, {checked} line-anchored points",
        not bad,
        "; ".join(bad[:6]),
    )


def check_field_dictionary() -> None:
    doc = load("field_dictionary.json")
    ents = doc["entities"]
    total = sum(len(e["fields"]) for e in ents)
    bad = []
    if doc["entity_count"] != len(ents):
        bad.append(f"entity_count {doc['entity_count']} != {len(ents)}")
    if doc["field_total"] != total:
        bad.append(f"field_total {doc['field_total']} != {total}")
    names = {e["entity"] for e in ents}
    for want in ("Player", "Staff", "Club", "Nation", "Contract"):
        if want not in names:
            bad.append(f"missing entity {want}")
    for e in ents:
        if not e["fields"]:
            bad.append(f"{e['entity']}: no fields")
        if e.get("verified_count", 0) + e.get("unconfirmed_count", 0) > len(e["fields"]):
            bad.append(f"{e['entity']}: status counts exceed fields")
        if not lines_of("fmsave/" + e["file"]):
            bad.append(f"{e['entity']}: source {e['file']} missing")
    vocab = json.dumps(doc["ext_status_vocabulary"], ensure_ascii=False).lower()
    if "not" not in vocab or "l1" not in vocab:
        bad.append("ext_status_vocabulary does not disclaim L1-L4 weight")
    check(
        f"7 field_dictionary self-consistent ({len(ents)} entities, {total} fields)",
        not bad,
        "; ".join(bad[:6]),
    )


def check_crosswalk() -> None:
    doc = load("crosswalk.json")
    bad = []
    grades = {"L1", "L2", "L3", "held", "n/a"}
    for x in doc["entries"]:
        if x["verdict"] != "held":
            bad.append(f"{x['id']}: verdict {x['verdict']}")
        g = x["our_side"]["grade"]
        if not any(g.startswith(t) for t in grades):
            bad.append(f"{x['id']}: grade {g!r} is not one of ours")
        if re.search(r"verified|unconfirmed|ext_status", g, re.I):
            bad.append(f"{x['id']}: grade borrows an external label")
        for e in x["external_side"]:
            if "@" not in e["provenance"]:
                bad.append(f"{x['id']}: unversioned provenance {e['provenance']}")
    if doc["summary"]["grade_moves"] != 0:
        bad.append("summary claims grade moves")
    if doc["summary"]["held_count"] != len(doc["entries"]):
        bad.append("held_count != entry count")
    verdicts = {x["verdict"] for x in doc["entries"]}
    if verdicts != {"held"}:
        bad.append(f"verdict vocabulary {sorted(verdicts)}")
    check(
        f"8 crosswalk fully held ({len(doc['entries'])} entries, 0 grade moves)",
        not bad,
        "; ".join(bad[:6]),
    )


def check_no_execution() -> None:
    bad = []
    scripts = sorted((ROOT / "scripts").glob("t93_*.py"))
    if len(scripts) < 4:
        bad.append(f"only {len(scripts)} t93 scripts found")
    for path in scripts + [OUT / "verify.py"]:
        text = path.read_text(encoding="utf-8")
        for pat in FORBIDDEN:
            for m in re.finditer(pat, text, re.M):
                line = text[: m.start()].count("\n") + 1
                bad.append(f"{path.name}:{line}: matches {pat}")
        # any path literal into scratch/ext must be a plain read of a file
        for m in re.finditer(r"scratch/ext[^\"']*", text):
            if path == OUT / "verify.py":
                continue
            if "read_text" not in text and "open(" not in text:
                bad.append(f"{path.name}: touches scratch/ext without a plain read")
    for path in OUT.iterdir():
        if path.name not in DELIVERABLES and path.name not in INTERMEDIATE:
            bad.append(f"unexpected file in outbox: {path.name}")
    missing = [n for n in DELIVERABLES if not (OUT / n).is_file()]
    if missing:
        bad.append("missing deliverables: " + ", ".join(missing))
    check(
        f"9 no external execution; {len(scripts)} t93 scripts + outbox contents",
        not bad,
        "; ".join(bad[:6]),
    )


def main() -> int:
    check_provenance()
    check_baseline()
    check_grammar_lines()
    check_memory_lines()
    check_recon_lines()
    check_field_dictionary()
    check_crosswalk()
    check_no_execution()

    width = max(len(n) for n, _, _ in RESULTS)
    failed = 0
    for name, ok, detail in RESULTS:
        mark = "PASS" if ok else "FAIL"
        print(f"{mark}  {name.ljust(width)}  {detail if not ok else ''}".rstrip())
        failed += 0 if ok else 1
    print(f"\n{len(RESULTS) - failed}/{len(RESULTS)} checks passed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
