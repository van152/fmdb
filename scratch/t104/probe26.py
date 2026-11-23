import sys, struct, runpy, collections
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
def load(side,name):
    info=m['archive_info'](codec,side,cache)
    ent=next(e for e in info['tables'] if e['path'].endswith(name))
    return m['inspect_entry'](codec,ent,info)['data']
for side in ('server','client'):
    pl=load(side,'table_extra_9.dat'); n=struct.unpack_from('<I',pl,8)[0]
    p=12; lens=[]; okord=0; names=[]
    for i in range(n):
        o=struct.unpack_from('<I',pl,p)[0]
        if o==i: okord+=1
        l=pl[p+4]
        names.append(pl[p+5:p+5+l].decode('utf-8','replace'))
        lens.append(5+l); p+=5+l
    print(side,'extra_9 n',n,'ord ok',okord,'p==len',p==len(pl),'left',len(pl)-p,'len range',min(lens),max(lens))
    print('   first5',[(lens[i],names[i]) for i in range(5)])
    print('   last row',lens[-1],repr(names[-1]))
