#!/usr/bin/env python3
"""Build a compact t96b deliverable from the existing t96 Unicorn run.

This deliberately preserves incomplete measurements as incomplete; it does not
infer successful closure from requested targets or from unexecuted rows.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scratch/t96/out/wire_traces.json"
OUT = ROOT / "scratch/t96b/out"


def build() -> dict:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Required existing run not found: {SOURCE}")
    old = json.loads(SOURCE.read_text(encoding="utf-8"))
    by_key = {(x["archive"], int(x["table_id"])): x for x in old.get("tables", [])}
    tables = []
    # Preserve exactly the combinations in the source inventory.
    for x in old.get("tables", []):
        tables.append({k: v for k, v in x.items() if k not in ("reads", "row0_reads")})
        nrows = int(x.get("total_rows_header") or 0)
        is_closed = nrows > 0 and int(x.get("rows_tested") or 0) >= nrows and bool(x.get("all_rows_closed_to_footer"))
        tables[-1]["status"] = "closed" if is_closed else "partial"
    closed = sum(row.get("status") == "closed" for row in tables)
    return {"status": "partial", "source": str(SOURCE.relative_to(ROOT)),
            "source_status": old.get("status", "unknown"), "table_pairs_expected": len(tables),
            "table_pairs_present": len(by_key), "closed_pairs": closed,
            "tables": tables}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--outdir", type=Path, default=OUT)
    ap.add_argument("--selftest", action="store_true", help="Validate deliverable schema/compactness")
    ap.add_argument("--help-extra", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args()
    try:
        data = build()
        if args.selftest:
            assert data["status"] == "partial"
            assert len(data["tables"]) == 79
            assert all("reads" not in row for row in data["tables"])
            print("selftest: schema/compactness checks passed; no closure claim made")
            return 0
        out = args.outdir
        out.mkdir(parents=True, exist_ok=True)
        (out / "wire_traces_v2.json").write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
        old9 = json.loads((ROOT / "scratch/t96/out/table9_251_closure.json").read_text(encoding="utf-8"))
        # Prior run tried only a few rows and did not close; retain it verbatim as prior evidence.
        closure9 = {"status": "partial", "source": "scratch/t96/out/table9_251_closure.json",
                    "server": old9.get("tables", {}).get("server", {}),
                    "client": old9.get("tables", {}).get("client", {}),
                    "note": "This is the prior t96 measurement; no t96b 251-row rerun was completed."}
        (out / "table9_251_closure.json").write_text(json.dumps(closure9, indent=2), encoding="utf-8")
        t10 = {"status": "not_measured", "server": {"rows_header": 251, "rows_tested": 1, "closed": False},
               "client": {"rows_header": 251, "rows_tested": 1, "closed": False},
               "note": "Prior t96 run reached only row 0 for each archive; no 251-row closure evidence."}
        (out / "table10_251_closure.json").write_text(json.dumps(t10, indent=2), encoding="utf-8")
        report = ("# t96b Unicorn closure — partial\n\n"
                  "No new full-table Unicorn pass was completed in this run. The existing t96 artifact is the sole measurement source; its failures are not promoted to successes.\n\n"
                  f"- Expected archive/table pairs: 79 inventoried archive/table combinations.\n- Pairs present in source artifact: {data['table_pairs_present']}.\n- Pairs marked closed in source: {data['closed_pairs']}.\n"
                  "- `table_9`: prior artifact reports server 5 successful rows (then unmapped read) and client failure at row 0; neither closed.\n"
                  "- `table_10`: prior artifact reports only row 0 attempted and unsuccessful for both archives.\n"
                  "- No verified findings on polymorphic prefix flags or constructors; these remain unresolved.\n"
                  "- The required four-table diff=0 selftest and 251-row table9/table10 closures were not achieved.\n\n"
                  "Failure diagnostics and field aggregates are carried over only when present in the prior source. No row-level raw reads are stored.\n")
        (out / "REPORT.md").write_text(report, encoding="utf-8")
        (out / "DONE.md").write_text(
            f"DONE type=t96b\n\nStatus: partial. Pairs present={data['table_pairs_present']}/79; source-verified closed={data['closed_pairs']}.\n"
            "table9 and table10 server/client 251-row closures: not achieved. See REPORT.md.\n", encoding="utf-8")
        print("Deliverables:")
        for name in ("wire_traces_v2.json", "table9_251_closure.json", "table10_251_closure.json", "REPORT.md", "DONE.md"):
            print(f"  {out / name}")
        print(f"status=partial pairs={data['table_pairs_present']}/79 source_closed={data['closed_pairs']}")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
