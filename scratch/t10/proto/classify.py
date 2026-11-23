import json, collections, importlib.util, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
spec2 = importlib.util.spec_from_file_location("_b","scratch/t07/out/build.py")
b = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(b)
hits, md = b.decode_cmp_hits(pe); hits.sort()
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
clubs={f['code'] for f in si['entities']['club']['fields'] if f['parent'] is None}
ACCESSOR={0x140833eb0,0x140835380,0x140e834a0}
ROUTER={0x140e587e0}
def is4cc(v):
    if not (0x20202020<=v<=0x7e7e7e7e): return False
    return True
def classify(sub,label):
    cnt=collections.Counter(); hdr=0; body=0; samples={}
    for off,code,va,_ in sub:
        ins=list(md.disasm(raw[off:off+0x18],va))
        br=next((x for x in ins[1:4] if x.mnemonic in ('je','jz','jne','jnz')),None)
        if br is None:
            cnt['no_branch']+=1; continue
        if br.mnemonic in ('jne','jnz'):
            # fall-through is the match path
            start=br.address+br.size; tf=pe.va2f(start)
        else:
            start=int(br.op_str,0); tf=pe.va2f(start)
        if tf is None: cnt['bad_target']+=1; continue
        blk=list(md.disasm(raw[tf:tf+0x80],start))[:24]
        kind=None
        for y in blk:
            o=y.op_str.lower()
            if y.mnemonic=='mov' and o.startswith('edx,') and 'ptr' not in o:
                try: v=int(o.split(',')[1].strip(),0)
                except Exception: v=None
                if v is not None and is4cc(v): kind='name_keyed'; break
            if y.mnemonic=='call':
                try: t=int(o,0)
                except Exception: t=None
                if t in ACCESSOR: kind='name_keyed_accessor'; break
                if 'qword ptr' in o: kind='vcall'; break
            if y.mnemonic=='jmp':
                try: t=int(o,0)
                except Exception: t=None
                if t in ROUTER: kind='router2'; break
                kind='tail_jmp'; break
            m=re.search(r"\[(rdi|rsi|rbx|r12|r13|r14|r15)\s*\+\s*(0x[0-9a-f]+)\]", y.op_str)
            if m and y.mnemonic in ('mov','movzx','movsx','cmp','test'):
                d=int(m.group(2),16)
                if 0x20<=d<=0x400:
                    if 'qword ptr' in y.op_str and y.mnemonic in ('mov','cmp'):
                        hdr+=1; kind='header_ptr'; samples.setdefault('header_ptr',(code,hex(y.address),y.mnemonic,y.op_str))
                    else:
                        body+=1; kind='inline_field'; samples.setdefault('inline_field',(code,hex(y.address),y.mnemonic,y.op_str))
                    break
            if y.mnemonic=='ret': break
        cnt[kind or 'no_access']+=1
    print(f'[{label}] n={len(sub)}')
    for k,v in cnt.most_common(): print(f'    {k:<22}{v:>5}  {v/len(sub):>6.1%}')
    print('    samples',samples)
    return cnt
A=[h for h in hits if 0xe82afc<=h[0]<0xe846ac]
B=[h for h in hits if 0xe89a34<=h[0]<0xe8cded]
S=[h for h in hits if 0xe57de0<=h[0]<0xe59000]
ca=classify(A,'A'); cb=classify(B,'B'); cs=classify(S,'S')
