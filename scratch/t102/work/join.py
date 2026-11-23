import json,re,os,struct,sys
idx=json.load(open('scratch/t95/vtable_index.json'))
fm=json.load(open('scratch/t97/out/fourcc_mem_map.json'))
T=[0,2,5,6,7,8,18,19,21,22,23,27,35,41,47,56]
CALL=re.compile(r'\(\*\(void \(__fastcall \*\*\)\([^)]*\)\)\(([^,]+),\s*(?:\(__int64\))?a1\s*\+\s*(\d+),\s*(\d+)\)')
HELP=re.compile(r'(sub_[0-9A-Fa-f]+)\(\s*(?:\(unsigned int\)|\(int\)|\(_DWORD\))?\s*(?:\*a2,\s*)?(?:\(int\))?a1\s*\+\s*(\d+)')
def mem4cc(tid):
    out={}
    for t in fm['tables']:
        if t['table_type']!=tid: continue
        for k,v in t['fourccs'].items():
            o=v.get('primary_off_int')
            if o is None: continue
            out.setdefault(o,[]).append((k,v.get('width'),v.get('c_type'),v.get('access_kind')))
    return out
def seq(path):
    src=open(path,encoding='utf-8',errors='replace').read()
    items=[]
    for m in CALL.finditer(src):
        ln=src[:m.start()].count('\n')+1
        items.append({'kind':'direct','mem':int(m.group(2)),'w':int(m.group(3)),'line':ln})
    for m in HELP.finditer(src):
        ln=src[:m.start()].count('\n')+1
        items.append({'kind':'helper','mem':int(m.group(2)),'fn':m.group(1),'line':ln})
    items.sort(key=lambda x:x['line'])
    return items
out={}
for t in idx['tables']:
    if t['table_type'] not in T: continue
    mm=mem4cc(t['table_type'])
    rec={'class':t['class'],'fourccs':len(mm)}
    for key,side in (('slot19_read_server','server'),('slot20_read_client','client')):
        e=t['core'].get(key) or {}
        f=e.get('file')
        if not f: rec[side]=None; continue
        p=os.path.join('scratch/t95/funcs',os.path.basename(f))
        it=seq(p)
        for x in it:
            x['fourccs_at_mem']=mm.get(x['mem'])
        rec[side]={'file':os.path.basename(p),'va':e.get('va'),'items':it}
    out[t['table_type']]=rec
json.dump(out,open('scratch/t102/work/join.json','w'),indent=1)
for tt in T:
    r=out[tt]
    print('='*10,tt,r['class'],'4cc_mem',r['fourccs'])
    for side in ('server','client'):
        v=r[side]
        if not v: print('  ',side,'NO-READER'); continue
        kn=sum(x['w'] for x in v['items'] if x['kind']=='direct')
        unk=[(x['mem'],x['fn']) for x in v['items'] if x['kind']=='helper']
        print(f'   {side}: n={len(v["items"])} known_w={kn} helpers={unk}')
