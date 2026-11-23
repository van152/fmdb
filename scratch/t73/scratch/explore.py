import runpy, sys, json, struct, hashlib
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()
for arch in ('client','server'):
    for tid in (2,5,19,41):
        try:
            raw = dump['load_payload'](codec, arch, tid)
        except Exception as e:
            print(arch, tid, 'ERR', e); continue
        print(f"{arch} table_{tid}: len={len(raw)} sha={hashlib.sha256(raw).hexdigest()[:16]}")
        print("  head64:", raw[:64].hex())
        print("  tail64:", raw[-64:].hex())
