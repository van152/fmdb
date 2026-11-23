import sys, json
sys.path.insert(0,'scratch/t02/inbox/a')
from _dis import data, va, off, md, base, secs
import capstone.x86_const as x86
regs={0xF8:'eax',0xF9:'ecx',0xFA:'edx',0xFB:'ebx',0xFC:'esp',0xFD:'ebp',0xFE:'esi',0xFF:'edi'}
# also REX + 81 (44 81 f8 etc.)
def scan(start,end):
    hits=[]
    pos=start
    while pos<end:
        b=data[pos]
        # 81 /r id
        if b==0x81 and pos+6<=end and data[pos+1] in regs:
            imm=int.from_bytes(data[pos+2:pos+6],'little')
            ascii_be=imm.to_bytes(4,'big')
            if all(32<=c<127 for c in ascii_be):
                hits.append((pos,'81',regs[data[pos+1]],imm,ascii_be.decode()))
        elif b==0x3D and pos+5<=end:
            imm=int.from_bytes(data[pos+1:pos+5],'little')
            ab=imm.to_bytes(4,'big')
            if all(32<=c<127 for c in ab):
                hits.append((pos,'3d','eax',imm,ab.decode()))
        elif b==0x41 and pos+7<=end and data[pos+1]==0x81 and data[pos+2] in regs:
            imm=int.from_bytes(data[pos+3:pos+7],'little')
            ab=imm.to_bytes(4,'big')
            if all(32<=c<127 for c in ab):
                hits.append((pos,'41 81',regs[data[pos+2]],imm,ab.decode()))
        pos+=1
    return hits
if __name__=='__main__':
    s=int(sys.argv[1],16); e=int(sys.argv[2],16)
    for p,f,r,imm,a in scan(s,e):
        print(f"{p:#x} {f:6s} {r:4s} {imm:#010x} {a}")
