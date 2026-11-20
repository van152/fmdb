"""t01 anchor regression: re-verify the byte-level facts accepted into the ledger.

Checks (all cheap, read-only):
  A1  editor.exe comp registration block bytes @0xebf150 (ccti) match E2/E14
  A2  fm.exe comp block @36605107 == editor.exe @15462499 (E12 identity)
  A3  editor.exe vtable @0x187d2b0 slot6 == 0x140ebfa40 (E11)
  A4  t01b_switch_cases.json: comp-matched cases >= 60 and contains ccti/cnti/cpcm (E10)
  A5  t01a_editor_sweep.json: anchor cluster containment >= 0.9 for comp (E9)
  A6  fm_sweep.json anchor_check: cnam/csnm/c3ln/cnti/ccti/cpcm/crep/cext/PLgn/dbty present (E12)
  A7  ledger E2 erratum: sequence uses csnm/c3ln (not cnsm/cl3n)

Exit 0 = all pass; 1 = any check failed (prints which).
Run: py -V:3.12 -I scripts/t01_anchors.py [--json]
"""
from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDITOR = Path(r"<OLD_REPO>\input\editor.exe")
FM = Path(r"<OLD_REPO>\input\fm.exe")


def main() -> int:
    ap = argparse.ArgumentParser(description="Re-verify t01 ledger anchor facts.")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    results: list[dict] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        results.append({"check": name, "ok": bool(ok), "detail": detail})

    ed = EDITOR.read_bytes()
    # A1
    blk = ed[0xEBF150:0xEBF15B]
    check("A1_comp_ccti_block", blk.hex() == "c745f069746363488945e8", blk.hex())
    # A2
    fm = FM.read_bytes()
    check("A2_fm_editor_block_identical", fm[36605107:36605107 + 16] == ed[15462499:15462499 + 16])
    # A3
    vt = struct.unpack_from("<Q", ed, 0x187D2B0 + 6 * 8)[0]
    check("A3_vtable_slot6_comp", vt == 0x140EBFA40, f"slot6={vt:#x}")
    # A4
    sc = json.loads((ROOT / "scratch/t01/t01b_switch_cases.json").read_text(encoding="utf-8"))
    codes = {c["code"] for c in sc["comp_matched"]}
    check("A4_switch_comp_cases", len(codes) >= 60 and {"ccti", "cnti", "cpcm"} <= codes,
          f"n={len(codes)}")
    # A5
    sw = json.loads((ROOT / "scratch/t01/t01a_editor_sweep.json").read_text(encoding="utf-8"))
    anchor_ok = False
    try:
        clusters = sw["clusters"]
        for c in clusters:
            if int(c.get("start_off", "0"), 16) == 0xEBF060:
                anchor_ok = c.get("entity_top3", [{}])[0].get("containment", 0) >= 0.9
                break
    except Exception as e:  # noqa: BLE001
        check("A5_sweep_anchor_cluster", False, f"parse error: {e}")
    else:
        check("A5_sweep_anchor_cluster", anchor_ok)
    # A6
    fmjson = json.loads((ROOT / "scratch/t01/inbox/t01a2/fm_sweep.json").read_text(encoding="utf-8"))
    ac = fmjson.get("anchor_check", {})
    ac2 = fmjson.get("anchor_check_corrected", ac)
    codes_fm = set(ac2) | set(ac)
    need = {"cnam", "csnm", "c3ln", "cnti", "ccti", "cpcm", "crep", "cext", "PLgn", "dbty"}
    check("A6_fm_anchor_codes", need <= codes_fm, f"missing={sorted(need - codes_fm)}")
    # A7
    led = json.loads((ROOT / "scratch/t01/LEDGER.json").read_text(encoding="utf-8"))
    e2 = next(e for e in led["entries"] if e["id"] == "E2")
    seq = e2["evidence"]["4cc_sequence"]
    check("A7_ledger_erratum_applied", "csnm" in seq and "c3ln" in seq and "cnsm" not in seq, str(seq))

    failed = [r for r in results if not r["ok"]]
    if args.json:
        print(json.dumps({"passed": len(results) - len(failed), "failed": len(failed), "results": results}, indent=1, ensure_ascii=False))
    else:
        for r in results:
            print(("PASS " if r["ok"] else "FAIL ") + r["check"] + ("  " + r["detail"] if r["detail"] else ""))
        print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
