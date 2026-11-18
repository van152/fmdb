"""Read-only byte-position RIP reference sweep for t02-p (no target execution)."""
import argparse
import struct
import hashlib
from pathlib import Path
import numpy as np
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_AC_WRITE
from capstone.x86 import X86_OP_MEM, X86_REG_RIP, X86_REG_FS, X86_REG_GS

HERE=Path(__file__).resolve().parent
EXE=Path(r'D:\tmp2b\fm24\input\editor.exe')
E=EXE.read_bytes()
PE=pefile.PE(data=E,fast_load=True)
BASE=PE.OPTIONAL_HEADER.ImageBase
MD=Cs(CS_ARCH_X86,CS_MODE_64); MD.detail=True
FLAGS={'A':0x141b60353,'B':0x141b5fc2c}


def sectva(va):
    return next(s for s in PE.sections if s.VirtualAddress <= va-BASE < s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData))


def va(off):
    s=next(s for s in PE.sections if s.PointerToRawData<=off<s.PointerToRawData+s.SizeOfRawData)
    return BASE+s.VirtualAddress+off-s.PointerToRawData


def off(va):
    s=sectva(va); d=va-BASE-s.VirtualAddress
    return s.PointerToRawData+d if d<s.SizeOfRawData else None


def get(o,n=None):
    i=next(MD.disasm(E[o:o+15],va(o),count=1))
    return {'file_offset':hex(o),'va':hex(i.address),'bytes':E[o:o+n].hex(' ') if n is not None else i.bytes.hex(' '),'instruction':i.mnemonic+' '+i.op_str}


def sweep():
    result={}
    for name,target in FLAGS.items():
        refs={}; abs_hits={}
        for n in (4,8):
            v=target if n==8 else target-BASE
            needle=v.to_bytes(n,'little'); pos=E.find(needle); hits=[]
            while pos>=0:
                hits.append(hex(pos)); pos=E.find(needle,pos+1)
            abs_hits['VA_qword' if n==8 else 'RVA_dword']=hits
        for s in PE.sections:
            start=s.PointerToRawData; end=start+s.SizeOfRawData
            if end-start<16: continue
            sec=s.Name.decode().rstrip('\0'); delta=BASE+s.VirtualAddress-start
            # Every byte as disp32, independently of alignment/instruction boundaries.
            # Adjacent starts up to 63 bytes below capture overlapping operands <=64B.
            for beg in range(start+1,end-3,1<<20):
                stop=min(beg+(1<<20),end-3)
                n=stop-beg
                rel=np.ndarray(n,dtype='<i4',buffer=E,offset=beg,strides=(1,))
                t=rel+np.arange(beg,stop,dtype='i4')
                t-=target-delta-4
                mod=np.frombuffer(E,dtype='u1',count=n,offset=beg-1)
                idx=np.flatnonzero((mod&0xc7==5)&(t<=0)&(t>=-71))
                for ix in idx:
                    d=beg+int(ix)
                    for o in range(max(start,d-11),d-1):
                        # Instructions are bounded to a section and 15 bytes.
                        i=next(MD.disasm(E[o:min(end,o+15)],o+delta,count=1),None)
                        if not i or i.disp_size!=4 or o+i.disp_offset!=d: continue
                        for m in i.operands:
                            if m.type!=X86_OP_MEM or m.mem.base!=X86_REG_RIP or m.mem.segment in (X86_REG_FS,X86_REG_GS): continue
                            addr=i.address+i.size+m.mem.disp
                            if (i.mnemonic=='lea' and addr!=target) or not addr<=target<addr+max(1,m.size): continue
                            op='address' if i.mnemonic=='lea' else ('write' if m.access&CS_AC_WRITE or (i.mnemonic=='setne' and i.operands[0].type==X86_OP_MEM) else 'read')
                            refs.setdefault((d,o+i.size),[]).append((o,sec,addr,i,op))
        canon=[]
        for group in refs.values():
            o,sec,addr,i,op=min(group,key=lambda g:g[0])
            canon.append({**get(o),'section':sec,'referent':hex(addr),'access':op,
                **({'suffix_decodings':[hex(g[0]) for g in group[1:]]} if len(group)>1 else {})})
        canon.sort(key=lambda x:int(x['file_offset'],16))
        s=sectva(target)
        result[name]={'va':hex(target),'rva':hex(target-BASE),'file_offset':off(target),
                      'pe_section':s.Name.decode().rstrip('\0'),'section_header_file_offset':hex(s.get_file_offset()),
                      'section_header_bytes':E[s.get_file_offset():s.get_file_offset()+40].hex(' '),
                      'section_offset':hex(target-BASE-s.VirtualAddress),'loaded_default':0,
                      'absolute_literal_hits':abs_hits,'direct_RIP_reference_count':len(canon),
                      'potential_writer_or_address_sites':[r for r in canon if r['access']!='read'],
                      'direct_RIP_refs':canon}
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--selftest',action='store_true',required=True); p.parse_args()
    try:
        assert hashlib.sha256(E).hexdigest()=='b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
        for o,target in zip((0xe4f4d5,0xe4f4ed),FLAGS.values()):
            assert va(o)+7+struct.unpack_from('<i',E,o+2)[0]==target and off(target) is None
        r=sweep()
        for k,v in r.items():
            found={x['file_offset'] for x in v['direct_RIP_refs']}
            assert {'A':{'0xe4f4d5','0x3c6e105'},'B':{'0xe4f4ed','0x3c6e118'}}[k]<=found
            print(k,{x:y for x,y in v.items() if x not in ('direct_RIP_refs','potential_writer_or_address_sites','absolute_literal_hits')}, {m: len(n) for m,n in v['absolute_literal_hits'].items()})
            for s in v['potential_writer_or_address_sites']: print(s)
        return 0
    except AssertionError as ex:
        print('check failed',ex); return 1
    except Exception as ex:
        print('fatal',ex); return 2


if __name__=='__main__': raise SystemExit(main())
