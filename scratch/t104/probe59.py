import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
ident=d['ident']; lens=d['lens']; n=len(ident); sel=[x[2] for x in ident]
starts=[14]+[ident[i][0]+13 for i in range(n-1)]
def body(i): return raw[starts[i]:starts[i]+lens[i]]
def names_tail(b):
    """2 names ending exactly at len(b), each [u32 l][bytes] with optional trailing NUL"""
    cands=[]
    for nul2 in (0,1):
        e2=len(b)-nul2
        if e2<5: continue
        l2=struct.unpack_from('<I',b,e2-4)[0]
        if l2>400 or e2-4-l2<0: continue
        s2=b[e2-l2:e2]
        if 0 in s2: continue
        try: t2=s2.decode('utf-8')
        except: continue
        if nul2 and b[e2]!=0: continue
        p2=e2-4-l2
        for nul1 in (0,1):
            e1=p2-nul1
            if e1<5: continue
            l1=struct.unpack_from('<I',b,e1-4)[0]
            if l1>400 or e1-4-l1<0: continue
            s1=b[e1-l1:e1]
            if 0 in s1: continue
            try: t1=s1.decode('utf-8')
            except: continue
            if nul1 and b[e1]!=0: continue
            p1=e1-4-l1
            cands.append((p1,l1,t1,l2,t2,nul1,nul2))
    return cands
res=collections.Counter(); good=[]
for i in range(n):
    b=body(i)
    for (ns,l1,t1,l2,t2,n1,n2) in names_tail(b):
        c=struct.unpack_from('<H',b,33)[0]
        if 35+4*c+12==ns:
            res[(sel[i],'ok',n1,n2)]+=1
            good.append(i); break
    else:
        res[(sel[i],'FAIL')]+=1
print(res)
print('ok rows', len(good))
for i in (0,50,89,655,1162,3041):
    b=body(i); cands=names_tail(b)
    c=struct.unpack_from('<H',b,33)[0]
    ns=35+4*c+12
    print(i,'sel',sel[i],'len',len(b),'c',c,'ns',ns,'names',[x[2:5] for x in cands][:2])
    print('   blk12', b[35+4*c:35+4*c+12].hex(), '| tail18@', b[35+4*c:35+4*c+18].hex())
