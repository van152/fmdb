import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
for arch in ('server','client'):
    try:
        raw=m['load_payload_mf'](codec,arch,9,cache)
    except Exception as e:
        print(arch,'ERR',e); continue
    print(arch,'len',len(raw),'head',raw[:24].hex())
    print('  count@8?',struct.unpack_from('<I',raw,8)[0] if len(raw)>=12 else None)
    print('  tail',raw[-16:].hex())
