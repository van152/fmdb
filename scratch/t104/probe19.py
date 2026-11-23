import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
for side,tid in [('server',24)]:
    raw=m['load_payload_mf'](codec,side,tid,cache)
print('ok',len(raw))
# extras
for side, name in [('server','table_extra_24.dat'),('server','table_extra_9.dat'),('server','table_extra_3.dat'),('client','table_extra_9.dat'),('client','table_extra_3.dat')]:
    info=m['archive_info'](codec,side,cache)
    ent=next(e for e in info['tables'] if e['path'].endswith(name))
    r=m['inspect_entry'](codec,ent,info)
    pl=r['data']
    n=struct.unpack_from('<I',pl,8)[0] if len(pl)>=12 else None
    print(side,name,'len',len(pl),'declared',ent['size'],'head',pl[:16].hex(),'count@8',n)
    print('   ver@6',struct.unpack_from('<H',pl,6)[0] if len(pl)>=8 else None, 'tail',pl[-16:].hex())
