import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def parse(raw):
    """id u32, then repeated (len u32, bytes) fields, 0xff separator, 00 01 00 object tag."""
    cnt=struct.unpack_from('<I',raw,8)[0]
    pos=12; objs=[]; errs=[]
    while pos<cnt and len(raw)-pos>4:  # cnt == decoded size? placeholder
        break
    return cnt

raw=lib.load_member('lang_update','8_3.dat')
print('len',len(raw),'u32@8',struct.unpack_from('<I',raw,8)[0])
# manual walk: object = [id:u32] then fields
pos=12; objs=0; fields_total=0
while pos+4<=len(raw):
    oid=struct.unpack_from('<I',raw,pos)[0]
    if oid>10_000_000: break
    p=pos+4; nf=0
    while p+4<=len(raw):
        b=raw[p]
        if b==0xff:
            p+=1; continue
        L=struct.unpack_from('<I',raw,p)[0]
        if L>300 or p+4+L>len(raw):
            break
        try: raw[p+4:p+4+L].decode('utf-8')
        except Exception: break
        p+=4+L; nf+=1
        if nf>12: break
    # expect 00 01 00 tag then next object
    if raw[p:p+3]==b'\x00\x01\x00': p+=3
    elif raw[p:p+1]==b'\x00': p+=1
    objs+=1; fields_total+=nf
    if objs<=4 or objs>=3460:
        print('obj',objs,'id',oid,'fields',nf,'end',p)
    if p<=pos: print('stuck at',pos, raw[pos:pos+24].hex(' ')); break
    pos=p
print('objects',objs,'fields',fields_total,'end',pos,'len',len(raw))
