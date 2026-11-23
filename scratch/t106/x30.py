import sys,runpy,struct
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0,'scripts')
mf=runpy.run_path('scripts/t38_multiframe.py'); codec=mf['_codec']()
inf=mf['archive_info'](codec,'server')
e=codec['_resolve_table'](25,inf['tables'],'server_db.dat')
d=mf['inspect_entry'](codec,e,inf)['data']
print('t25 len',len(d),'count',struct.unpack_from('<I',d,8)[0])
print('tail 20',d[-20:].hex())
print('hl markers',d.count(b'\x64\xff\xff\xff'))
# check each 127 row ends with 64 ff ff ff
st=127; pos=12; bad=0
for i in range(7047):
    r=d[pos:pos+st]
    if r[-4:]!=b'\x64\xff\xff\xff': bad+=1
    pos+=st
print('rows not ending with 64ffffff:',bad,'end pos',pos,'len',len(d))
