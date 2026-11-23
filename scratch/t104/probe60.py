import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
ident=d['ident']; lens=d['lens']; n=len(ident); sel=[x[2] for x in ident]
starts=[14]+[ident[i][0]+13 for i in range(n-1)]
def body(i): return raw[starts[i]:starts[i]+lens[i]]
def name_start(b):
    """find start of a 2-name region at end: [u32 l1][s1][0?][u32 l2][s2][0?]"""
    for n2 in (0,1):
        e2=len(b)-n2
        if e2<6: continue
        l2=struct.unpack_from('<I',b,e2-4)[0]
        if l2>400 or e2-4-l2<0: continue
        s2=b[e2-l2:e2]
        if 0 in s2: continue
        try: s2.decode('utf-8')
        except: continue
        if n2 and b[e2]!=0: continue
        p2=e2-4-l2
        for n1 in (0,1):
            e1=p2-n1
            if e1<6: continue
            l1=struct.unpack_from('<I',b,e1-4)[0]
            if l1>400 or e1-4-l1<0: continue
            s1=b[e1-l1:e1]
            if 0 in s1: continue
            try: s1.decode('utf-8')
            except: continue
            if n1 and b[e1]!=0: continue
            return (e1-4-l1, l1, l2)
    return None
stat=collections.Counter(); bad=[]
for i in range(n):
    b=body(i); ns=name_start(b)
    if ns is None: stat[(sel[i],'noname')]+=1; continue
    be=ns[0]
    hit=None
    for pre in (0,49):
        if be<pre+35: continue
        c=struct.unpack_from('<H',b,pre+33)[0]
        if pre+35+4*c+10==be: hit=pre
    if hit is None: stat[(sel[i],'nofit')]+=1; bad.append(i)
    else: stat[(sel[i],hit)]+=1
print(stat)
print('bad rows',len(bad), bad[:10])
for i in (0,50,89,655,1162,3041,700):
    b=body(i); ns=name_start(b); be=ns[0]
    c0=struct.unpack_from('<H',b,33)[0]
    print('row',i,'sel',sel[i],'len',len(b),'c0',c0,'be',be,'pre0 fit',35+4*c0+10==be,'names',ns)
    print('   base33',b[:33].hex())
    print('   blk10 ',b[35+4*c0:35+4*c0+10].hex())
    print('   names ',b[be:].hex())
