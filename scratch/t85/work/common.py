"""t85 shared helpers: payload loading (E80 rule) + identity census."""
from __future__ import annotations
import json, os, pathlib, runpy, struct

ROOT = pathlib.Path(__file__).resolve().parents[3] if False else pathlib.Path.cwd()
DB = pathlib.Path(os.environ.get('FM24_DB_DIR') or 'D:/tmp2b/fm24-db/scratch/data')
MAGIC = bytes.fromhex('28b52ffd')
_C = None

def codec():
    global _C
    if _C is None:
        k = runpy.run_path(str(ROOT / 'scratch/t01/inbox/t01k/verify.py'))
        _C = runpy.run_path(str(k['OLD_READER_PATH']))
    return _C

def entries(archive):
    c = codec(); fn = f'{archive}_db.dat'; p = DB / fn
    return c['list_tables'](p, fn), c['_archive_layout'](p.read_bytes())['data_base']

def payload(archive, path, size):
    """E80: member start = data_base(34) + entry.offset; pick frame whose out len == size."""
    c = codec(); fn = f'{archive}_db.dat'; p = DB / fn
    db = p.read_bytes()
    ents = c['list_tables'](p, fn)
    e = next(x for x in ents if x['path'] == path)
    base = int(c['_archive_layout'](db)['data_base'])
    s = base + int(e['offset']); end = s + int(e['packed_size'])
    z = c['_zstd_module'](); d = z.ZstdDecompressor(); pos = s
    while pos + 4 <= end and db[pos:pos+4] == MAGIC:
        obj = d.decompressobj(); out = obj.decompress(db[pos:end])
        if len(out) == size:
            return out
        used = (end - pos) - len(obj.unused_data)
        if not obj.eof or used <= 0:
            break
        pos += used
    raise RuntimeError(f'{fn} {path}: no frame with len {size}')

def jl(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8'))
