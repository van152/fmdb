import sys, struct, runpy, collections
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
def load(side,name):
    info=m['archive_info'](codec,side,cache)
    ent=next(e for e in info['tables'] if e['path'].endswith(name))
    return m['inspect_entry'](codec,ent,info)['data']
pl=load('server','table_extra_3.dat')
print('len',len(pl),'n',struct.unpack_from('<I',pl,8)[0])
print('first 200B:'); 
for k in range(0,200,16): print(k, pl[k:k+16].hex())
print('last 160B:')
for k in range(len(pl)-160,len(pl),16): print(k, pl[k:k+16].hex())
# look for triple positions in first 400
for p in range(12,400):
    a,b,c=struct.unpack_from('<III',pl,p)
    if b==c and b!=0 and a<90000: print('ident cand',p,a,b)
