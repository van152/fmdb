# t115 — basic people framing and anchor verification

**Status: partial, not L3 complete.** The exact requested semantic completion cannot be responsibly asserted: supplied C excerpts do not by themselves establish all serialized field mappings, and the on-disk type histogram includes type 5 although the supplied factory excerpt lists type 6.

Rows: 658,011; chain end: 54,060,034; expected `len(payload)-9`: 54,060,034; diff: 0.

## Frame counts

- type 1: 166,064
- type 2: 476,158
- type 3: 4,757
- type 4: 9,839
- type 5: 1,193

## Anchor checks

| UID | Name | CA candidate | PA candidate | Year candidate | Result |
|---:|---|---:|---:|---:|---|
| 28049320 | Harry Kane | 184 | 185 | 1993 | verified at supplied UID offset |
| 735216 | Cristiano Ronaldo | 160 | 200 | 1985 | verified at supplied UID offset |
| 7458500 | Lionel Messi | 200 | 200 | 1987 | verified at supplied UID offset |

## CA candidates

Candidate ordering uses the observed u16 at record+44 only; it is not presented as an authenticated FM24 Top 30. See JSON for the list.

## Source interpretation caveat

`140e4fd70.c` establishes conditional reads into in-memory offsets +32..+104 and invokes `sub_141084540`; `140e50cd0.c` is a property dispatcher, not a wire-schema declaration. Exact name/date/nation/club semantics and name-table join remain unresolved.
