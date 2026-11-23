# t114 partial results

`basic_people_db.dat` was scanned as 658,011 fixed-width records; row chain closes exactly at `len-9`, with observed class histogram 166,064 / 476,158 / 4,757 / 9,839 / 1,193. The first byte of each row is 0x11 and the next byte is class.

Semantic field names/4CCs and UID anchors are not asserted: the supplied reader includes conditional branches and the getter has multiple cases, which cannot be established from offsets alone. `people_db.dat` was decompressed and its header captured, but variable row boundaries and person_type dispatch remain unclosed. See JSON artifacts for evidence and caveats.
