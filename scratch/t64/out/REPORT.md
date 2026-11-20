# t64 COMP unmapped round 2

## Scope

This is an evidence increment over the frozen t59 `comp` `table_25` main-row map. It surveys all 196 t59 `unmapped` occurrences and the static `COMP+0xa8` / `COMP+0xe0` payload entries. It does not reopen t59's 49 L3 fields, 10 held fields, or 818 inversion records, and it does not decode derived collections owned by t66.

Coordinates in the machine-readable files are PE file offsets unless a record includes an explicit `va`. The binary is `editor.exe` SHA-256 `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`.

## Result

- Reviewed occurrences: **196/196**.
- New L3 closures: **0**. The t59 L3/held map and 818 inversions remain byte-for-byte frozen as inputs.
- Candidate only: `WpBn`, whose getter computes a Band projection using the already-read `+0xf4` state; it is not promoted to a wire binding.
- Bounded COMP getter literal-code hits: **47** unmapped occurrences; the slot-5 root separately contains `VARv`/`VARm`/`VARs`/`VARd`. Derived collection roots were not scanned. The remaining occurrences are only negative within the two bounded getter roots, not a whole-binary absence claim.

Exclusion category counts are: `{"advanced_rules_or_debug": 4, "bounded_getter_without_wire_closure": 38, "derived_count": 2, "derived_list_or_shared_handler": 5, "derived_parent_or_global_state": 1, "no_bounded_comp_getter_case": 141, "projection_candidate": 1, "rules_context_sibling": 4}`. Per-occurrence reasons and falsification conditions are in `exclusions.json`; the full field ledger is in `field_map_r2.json`.

## Main-reader ledger

The main reader extent is `0xeb7000..0xeb7e42`. The bounded CFG and the frozen t59 instruction records enumerate 55 direct `stream+0x28` calls: 52 outer slots plus three tag-4 alternate calls at `0xeb7218`, `0xeb72f8`, and `0xeb7332`. The t59 report states 54/51; the additional outer marker is `wbcl_present` at `0xeb7c8f`, already recorded in t59 `field_slots.json`. This is a call-accounting correction only: no t59 field status, L3 closure, or inversion record changes. The alternate calls reuse `m58/m60/m68`, whose existing XML consumers are `ccti/cnti/cpcm`. The non-stream helper ledger contains 43 reachable direct calls, listed site by site in `helpers.json`.

The tag-4 arm is gated at `0xeb71b9` and uses name readers at `COMP+0x48` and `COMP+0x40`; the local `[rsp+0xf8]` flag remains source-unresolved. Outside that arm, COMP getter equal paths add `r12+0x40` for `cnam`, `r12+0x48` for `csnm`, and `r12+0x50` for `c3ln`. These are getter-member candidates only: the main-row stream does not prove their wire transfer, tag-4 is absent in both archives, and the t59 held statuses are unchanged.

`VARt` loads `COMP+0xd0` and `HKEt` loads `COMP+0xd8`, then each compare block tests the field code and object pointer. The matching-code/non-null branch reaches file offset `0xec1830`, where the code reads and compares context-object `+0xc0/+0xc8`, calls helper VA `0x140eba600`, and continues through shared context checks. The `0xec0e30 -> 0xeb56c0` nested-rules dispatch is recorded separately and is not asserted as the direct successor of those compare blocks. No same-COMP scalar wire transfer is proved; both t59 fields remain held. The first counterchain and falsification checklist are in `helpers.json`.

## Static payloads

`+0xa8` is entered only when the presence byte read at `0xeb7532` is nonzero; `cmp` at `0xeb753f` followed by `je` at `0xeb7544` skips on zero, while nonzero reaches the allocator at `0xeb754a` and reader at `0xeb75ca`. `+0xe0` is entered only when the presence byte read at `0xeb76c0` is nonzero; `cmp` at `0xeb76cd` followed by `je` at `0xeb76d2` skips on zero, while nonzero reaches allocation/construction at `0xeb76d9/0xeb76e4` and reader at `0xeb76fb`. Exact branch targets and instruction bytes are recorded in `helpers.json`.

The independent row replay found:

- client: no `a8_present` or `e0_present` event because client mode has no extension block;
- server: 7,047 presence events for each, all zero; `obj_a8` and `obj_e0` events are 0/0;
- server sibling rules objects are separate: `+0xd0` presence is 121 and `+0xd8` presence is 51.

The helper scan also separates `+0xd0/+0xd8` nested rules objects from the requested pair. Generic reader calls at `0xeb718b/0xeb71a2` target `+0x138/+0x13c` and have no XML consumer; the same helper at `0xeb7cc4/0xeb7cdb` maps existing slots `+0x140/+0x144` to `wbst/wben` (XML 25/26).

The zero result is a data counterexample to entry, not proof that the static payloads do not exist.

## Verification

`verify.py` reopens the raw client/server `table_25` payloads and independently parses the native row envelope. The expected command environment is `py -V:3.12 -I -B` with `FM24_DB_DIR=<WORKSPACE>/scratch/data`.

Post-build checks completed: generated `verify.py` passed, and `scripts/t01_anchors.py` passed all 7/7 checks.
