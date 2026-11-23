DONE type=t90 status=complete
task=t90 schema v11.2 candidate assembly + denominator re-bucket
date=2026-11-21
mode=mechanical assembly only; no source re-adjudicated; L4=0

# deliverables (scratch/t90/out/)
schema_v112.json        30,291,049 B  37 -> 40 root keys (3 new sections)
denominator_v2.json        349,292 B  1,034 rows, before/after per occurrence
verify.py                    9,372 B  independent verifier (no builder imports)
diff_inventory.json          1,215 B  machine-readable diff + trace map
REPORT.md                    8,705 B  full report
DONE.md                            this file

# builders (repo scripts, new files)
scripts/t90_schema_v112.py   --selftest 8/8   --verify 36/36
scripts/t90_denominator.py   --selftest 5/5   --verify 18/18

# verification
scratch/t90/out/verify.py --verify     35/35 PASS, 0 failure
scripts/t01_anchors.py                  7/7 PASS

# schema diff v11.1 -> v11.2-candidate
added   fk_index_e125 / five_tables_l3_e126 / table9_closure_e127
changed schema_version / generated_by / coverage / incremental_provenance
        + scan_tables (weather t76c/27 slots VALUES only: 25 in / 25 out,
          offset set identical, E118 rationale preserved under why_before_E118)
untouched 32 non-mutable roots byte-identical (per-section SHA-256 guarded)

# grades attached
fk_index_e125        L2 (E125)   37 targets closed, city 4 lanes mapped-ordinal
five_tables_l3_e126  L3 (E126)   188 xml fields, 152 L3, 17 held, 0 byte gap
table9_closure_e127  L2 (E127)   t9 31,956/307,564 B strict closure, grammar held

# denominator re-bucket (E116 -> v2 candidate)
occurrences 1,034 -> 1,034 (conserved)
unresolved_wire_slot 277 -> 160 (-117, all club.xml[211..327])
new bucket re_routed_table_45 = 117 @ L2_candidate (t88-fix2 lane in flight)
carried 110 -> 110 (physical coverage 10.6% gross; 110/917 = 12.0% if the
        table_45 family is carved out of the club extra_3 denominator)
moved rows total 117; held / no_wire_evidence / ui_or_derived: 0 moved

# conflicts raised (not adjudicated, escalate=true)
C1 the 117-item family is club.xml[211..327], not literally "CBW*/CBD*"
   (only 10 of 117 codes are CB*)
C2 rule (2) structurally empty: the t83 five tables are not in the 1,034
   denominator; nation duni is a different field (held E94/E108) -> 0 moved
C3 rule (3) structurally empty: city(2) has no occurrence in the 1,034;
   the Cnti rows that do exist (club/016, comp/015) were already mapped_l3

# read-only guarantees
reports/club_nation_subtable_schema.json  f811a216... 29,893,769 B unchanged
reports/xml_denominator_coverage.json     e3a6d56e...    297,905 B unchanged
scratch/t01/LEDGER.json                   794bad55...    282,003 B unchanged
scripts/t87_v11_patch.py                  c303310e...     34,473 B unchanged
no file written outside scratch/t90/out/ and scripts/t90_*.py

# open for commander acceptance
1 merge into reports/ (deliberately not done here)
2 adopt or reject the net-denominator reading (110/917 = 12.0%)
3 rule on C1/C2/C3
4 decide 11.2-candidate -> 11.2
