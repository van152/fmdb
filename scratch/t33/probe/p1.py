import os, sys, json, struct, ctypes
sys.path.insert(0, 'scripts')
ROOT='.'
import importlib.util
spec = importlib.util.spec_from_file_location("dump","scripts/fm24_dump.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
codec = m._reader()
os.environ.setdefault("FM24_DB_DIR","D:/tmp2b/fm24-db/scratch/data")
for tid in (73,58,39):
    raw = m.load_payload(codec,"server",tid)
    print("==",tid,len(raw), struct.unpack_from("<I",raw,8)[0], raw[:20].hex())
