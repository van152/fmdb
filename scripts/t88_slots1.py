"""t88-fix6: static extraction.
 A) 4CC imm32 in cmp esi/edx (bytes big-endian ascii) -> (entry block dl=rec_type, r8d=tag)
 B) RECORD_GET @0x1543ca0: cmp edx,tag -> [rdi+off] load -> tag -> struct off/width
 usage: t88_slots1.py [--selftest]
"""
import sys,json,struct,capstone
EXE='D:/tmp2b/fm24/input/editor.exe'
BASE=0x140000000
def s4(v):
    b=v.to_bytes(4,'big')
    return b.decode('latin1') if all(32<=c<127 for c in b) else None
def blocks(d):
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
    lo,hi=0x11f0800,0x11f2d00
    out=[];dl=None;ent=None
    for i in md.disasm(d[lo:hi],BASE+lo):
        o=i.op_str
        if i.mnemonic=='mov' and o.startswith('dl, '):
            dl=int(o.split(', ')[1],16); ent=i.address-BASE
        elif i.mnemonic=='mov' and o.startswith('r8d, '):
            s=s4(int(o.split(', ')[1],16))
            if s and dl is not None: out.append({'entry':ent,'rec_type':dl,'tag':s})
    return out
def dispatch(d):
    res={}
    for pat,mn in ((b'\x81\xfe','esi'),(b'\x81\xfa','edx'),(b'\x41\x81\xfe','esi')):
        i=0
        while True:
            i=d.find(pat,i)
            if i<0: break
            fo=i+len(pat); v=struct.unpack_from('<I',d,fo)[0]; s=s4(v)
            if s:
                md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
                tgt=[]
                for k in md.disasm(d[fo+4:fo+4+14],BASE+fo+4):
                    if k.mnemonic in ('je','jne','jg','jle') and k.op_str.startswith('0x'):
                        tgt.append([k.mnemonic,int(k.op_str,16)-BASE])
                    else: break
                res.setdefault(s,[]).append([i,tgt])
            i+=1
    return res
def tag_struct_off(d):
    md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64)
    lo,hi=0x1543ca0,0x15446a0
    ins=list(md.disasm(d[lo:hi],BASE+lo))
    cur=None;res={}
    for idx,i in enumerate(ins):
        o=i.op_str
        if i.mnemonic=='cmp' and o.startswith('edx, 0x'):
            s=s4(int(o.split(', ')[1],16))
            cur=s if s else None
        elif cur and i.mnemonic in ('mov','movsx','movzx','movsxd') and '[rdi + 0x' in o:
            off=int(o.split('[rdi + ')[1].split(']')[0],16)
            w='?'
            if 'byte ptr' in o: w=1
            elif 'word ptr' in o: w=2
            elif 'dword ptr' in o: w=4
            elif 'qword ptr' in o: w=8
            res.setdefault(cur,[]).append([hex(off),w,o])
            if len(res[cur])>4: res[cur]=res[cur][:4]
    return res
if __name__=='__main__':
    if '--help' in sys.argv:
        print("usage: t88_slots1.py [--selftest]  writes out3/_blocks.json _dispatch2.json _tagstruct.json"); sys.exit(0)
    d=open(EXE,'rb').read()
    bl=blocks(d); dp=dispatch(d); ts=tag_struct_off(d)
    O='scratch/t88/out3/'
    json.dump(bl,open(O+'_blocks.json','w'),indent=0)
    json.dump({k:[[hex(a),[[m,hex(t)] for m,t in g]] for a,g in v] for k,v in dp.items()},open(O+'_dispatch2.json','w'),indent=0)
    json.dump(ts,open(O+'_tagstruct.json','w'),indent=0)
    print('blocks',len(bl),'tags',sorted(set(b['tag'] for b in bl)))
    print('dispatch codes',len(dp))
    print('tagstruct tags',len(ts))
    for k in ('stdb','gols','ogls','stdt','comp','stid','stnm','atte','gams','endt','fsgt','otht','cash','infn','stic'):
        print(' ',k,ts.get(k))
