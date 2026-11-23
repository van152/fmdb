import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
for arch in ('server','client'):
    raw=m['load_payload_mf'](codec,arch,9,cache)
    print('==',arch,len(raw),raw[:40].hex())
    # find positions of u32 == k for k in 0..5
    for k in range(6):
        pos=[i for i in range(12,min(len(raw),4000)) if struct.unpack_from('<I',raw,i)[0]==k]
        print('  u32==%d at'%k, pos[:6])
