# t16 ledger

Status: `partial_golden_gate_failed`

| entity | total | named | unnamed | conflicts | evidence | result |
|---|---:|---:|---:|---:|---|---|
| city | 15 | 7 | 8 | 0 | L3_inherited_and_t16_walk_not_closed | partial_golden_gate_failed |
| comp | 255 | 18 | 237 | 0 | L3_inherited_E20_and_t16_walk_not_closed | partial_golden_gate_failed |
| weather | 94 | 0 | 94 | 0 | none_E27_reference_missing | partial_missing_E27_baseline |
| nation | 346 | 7 | 339 | 0 | L3_inherited_t01g_and_t16_walk_not_closed | partial_golden_gate_failed |
| debug_city | 15 | 1 | 14 | 0 | L3_static_candidate | partial_engine_candidates |
| debug_comp | 255 | 0 | 255 | 7 | L3_static_candidate | partial_engine_candidates |
| club | 433 | 0 | 433 | 6 | L3_static_candidate | partial_engine_candidates |
| debug_nati | 346 | 0 | 346 | 0 | L3_static_candidate | partial_engine_candidates |

Batch extraction remains gated by city/weather/comp goldens.
