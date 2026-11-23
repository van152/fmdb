import sys,struct; sys.path.insert(0,'scripts')
import importlib.util, json, io
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
d=json.load(io.open('scratch/t81/out/fk_index.json',encoding='utf-8'))
# frozen FIELDS: (client,6) rdui@3 duni@7 ; (client,23) rdui@1 duni@5 ; (client,35) rdui@2 duni@6
for tid,ro,uo,S in [(6,3,7,16),(23,1,5,14),(35,2,6,15)]:
    raw=m.load_payload('client',tid); n=m.u32(raw,8)
    ok_o=all(m.u32(raw,14+j*S+ro)==j for j in range(n))
    ok_u=all(m.u32(raw,14+j*S+uo)==m.u32(raw,14+j*S+uo+4)!=0 for j in range(n))
    print(f't{tid} frozen rdui@{ro} ok={ok_o} duni@{uo} ok={ok_u} n={n}')
    # index-derived
    vals=d['targets'][f'{tid}/client']['uid_set'].get('values')
    frozen_uids=[m.u32(raw,14+j*S+uo) for j in range(n)]
    print('   index uid_set == frozen duni column:', vals==frozen_uids if vals else 'digest-only')
    print('   index rows',d['targets'][f'{tid}/client']['row_count'])
