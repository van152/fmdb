#!/usr/bin/env python3
"""Pure-Python framing validator for the FM24 basic-people payload.

The framing/parser is Python; decompression uses the system libzstd through ctypes.
"""
import argparse, ctypes, ctypes.util, json, struct, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "scratch/data"
OUT = ROOT / "scratch/t114/out"
COUNT = 658011
WIDTH = {1: 83, 2: 83, 3: 83, 4: 34, 5: 22}
HIST_EXPECTED = {1: 166064, 2: 476158, 3: 4757, 4: 9839, 5: 1193}

def decompress(path, expected):
    raw = path.read_bytes()
    # The project's Tad wrapper has an 8-byte prefix followed by one zstd frame.
    frame = raw[8:]
    name = ctypes.util.find_library('libzstd') or ctypes.util.find_library('zstd')
    if not name:
        raise RuntimeError('libzstd unavailable')
    lib = ctypes.CDLL(name)
    fn = lib.ZSTD_decompress
    fn.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_size_t]
    fn.restype = ctypes.c_size_t
    iserr = lib.ZSTD_isError
    iserr.argtypes = [ctypes.c_size_t]
    iserr.restype = ctypes.c_uint
    src = ctypes.create_string_buffer(frame)
    dst = ctypes.create_string_buffer(expected)
    n = fn(dst, expected, src, len(frame))
    if iserr(n) or n != expected:
        raise RuntimeError(f'zstd decode failed/size mismatch: {n} expected {expected}')
    return dst.raw[:n]

def parse_basic(b):
    declared = struct.unpack_from('<I', b)[0]
    if declared < 0 or (declared == COUNT and len(b) != 54060043):
        raise ValueError('unexpected payload size or count header')
    p, end = 5, len(b)-9
    hist, samples = {}, []
    # Each row is marker 0x11, class, then the fixed-size class record.
    for i in range(declared):
        if p + 2 > end or b[p] != 0x11:
            raise ValueError(f'bad row marker at row {i}, offset {p}')
        typ = b[p+1]
        if typ not in WIDTH:
            raise ValueError(f'unknown class {typ} at row {i}, offset {p}')
        n = WIDTH[typ]
        if p+n > end:
            raise ValueError(f'truncated row {i}')
        hist[typ] = hist.get(typ, 0)+1
        if len(samples)<20:
            samples.append({'row':i,'offset':p,'class':typ,'record_hex':b[p:p+n].hex()})
        p += n
    if p != end:
        raise ValueError(f'row chain ended at {p}, expected footer at {end}')
    return {'row_count':declared,'row_chain_end':p,'footer_offset':end,'footer_hex':b[end:].hex(),'histogram':hist,'sample_rows':samples}

def selftest():
    # exercise all fixed class widths and reject malformed tags
    for t,n in WIDTH.items():
        b = struct.pack('<I',1)+b'\0'+bytes([0x11,t])+bytes(n-2)+bytes(9)
        b = b[:5] + bytes([0x11,t]) + bytes(n-2) + bytes(9)
        assert parse_basic(b)['histogram']=={t:1}
    try: parse_basic(struct.pack('<I',1)+b'\0'+b'\x10\x01'+bytes(81)+bytes(9))
    except ValueError: pass
    else: raise AssertionError('bad marker accepted')

def run():
    OUT.mkdir(parents=True, exist_ok=True)
    basic = decompress(DATA/'basic_people_db.dat', 54060043)
    r = parse_basic(basic)
    if r['histogram'] != HIST_EXPECTED: raise ValueError(f'histogram mismatch: {r["histogram"]}')
    inventory = json.loads((ROOT/'scratch/t113/out/people_archives_inventory.json').read_text(encoding='utf-8'))
    schema = {
      'status':'partial', 'reason':'Record framing is validated, but the available evidence does not establish a complete semantic wire-column map or UID anchors; do not claim L3 completion.',
      'basic_person_layout_evidence': {'reader_va':'0x140e4fd70','property_getter_va':'0x140e50cd0','record_marker':'0x11','class_byte_offset':1,'record_width_including_marker_and_class':WIDTH,'reader_observed_mem_offsets':[101,48,32,40,56,72,76,80,82,84,86,88,90,94,96,98,100,102,104]},
      'class_counts':HIST_EXPECTED, 'full_scan':r,
      'uid_anchors':[],
      'layout_caveat':'The reader establishes memory destinations and conditional reads but not their semantic 4CC mapping. Getter reports 20 fourCCs but code paths/widths still require complete branch-by-branch correlation.'}
    (OUT/'basic_people_schema.json').write_text(json.dumps(schema,indent=2),encoding='utf-8')
    people = decompress(DATA/'people_db.dat',400443970)
    probe={'status':'partial','size_bytes':len(people),'first_64_bytes':people[:64].hex(),'first_100_bytes':people[:100].hex(),'payload_sha256':inventory['archives']['people_db']['payload_sha256'],'analysis':'Container inflated and header bytes captured. No closed variable-record grammar: cannot safely assign each row a person_type or claim first-100-row parsing.','known_helper_gaps':inventory.get('person_type_distribution')}
    (OUT/'people_db_probe.json').write_text(json.dumps(probe,indent=2),encoding='utf-8')
    (OUT/'REPORT.md').write_text('# t114 partial results\n\n`basic_people_db.dat` was scanned as 658,011 fixed-width records; row chain closes exactly at `len-9`, with observed class histogram 166,064 / 476,158 / 4,757 / 9,839 / 1,193. The first byte of each row is 0x11 and the next byte is class.\n\nSemantic field names/4CCs and UID anchors are not asserted: the supplied reader includes conditional branches and the getter has multiple cases, which cannot be established from offsets alone. `people_db.dat` was decompressed and its header captured, but variable row boundaries and person_type dispatch remain unclosed. See JSON artifacts for evidence and caveats.\n',encoding='utf-8')
    (OUT/'DONE.md').write_text('DONE type=t114\n\nFraming scan: 658011 rows; footer boundary exact; histogram '+json.dumps(r['histogram'])+'. Semantic schema and UID anchors remain incomplete.\n',encoding='utf-8')
    print(json.dumps({'files':[str(x) for x in sorted(OUT.iterdir())],'rows':COUNT,'end':r['row_chain_end'],'footer_offset':r['footer_offset'],'histogram':r['histogram']},indent=2))

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--selftest',action='store_true'); ap.add_argument('--run',action='store_true'); a=ap.parse_args()
    try:
        if a.selftest: selftest(); print('selftest: OK'); return 0
        if a.run: run(); return 0
        ap.print_help(); return 0
    except Exception as e:
        print(f'ERROR: {e}',file=sys.stderr); return 1
if __name__=='__main__': raise SystemExit(main())
