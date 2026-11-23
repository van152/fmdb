import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def parse(raw):
    """u32 count@8 ; record = uid:u32, then fields: [0xFF] u32len bytes ;
       trailer = 0x00, then u16 flags (detected when the byte after 0x00 is non-zero)."""
    cnt=struct.unpack_from('<I',raw,8)[0]
    pos=12; recs=[]
    while len(recs)<cnt:
        if pos+4>len(raw): return recs,pos,f'eof_uid rec{len(recs)}'
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4
        flds=[]
        while True:
            if pos>=len(raw): return recs,pos,f'eof_body rec{len(recs)}'
            b=raw[pos]
            if b==0xFF: pos+=1; continue
            if b==0x00 and pos+1<len(raw) and raw[pos+1]!=0:
                pos+=3; break                      # trailer 00 <u16>
            if pos+4>len(raw): return recs,pos,'eof_len'
            L=struct.unpack_from('<I',raw,pos)[0]
            if pos+4+L>len(raw): return recs,pos,f'badlen {L} @{pos} rec{len(recs)}'
            flds.append(raw[pos+4:pos+4+L]); pos+=4+L
        recs.append((uid,flds))
    return recs,pos,'ok'

for lang in ('8','32','7','10','11','12','15','16','17','18','19','21','22','24','25','30','6','1000000','1000001','1000002','1000003','1000004'):
    tot=okc=bad=0
    det=[]
    for typ in ('0','2','3','5','6','7','9','18','19','21','23','25','35','47','56'):
        nm=f'{lang}_{typ}.dat'
        try: raw=lib.load_member('lang_update',nm)
        except Exception: continue
        cnt=struct.unpack_from('<I',raw,8)[0]
        recs,pos,st=parse(raw)
        tot+=1
        if st=='ok' and pos==len(raw)-8 and len(recs)==cnt: okc+=1
        else:
            bad+=1; det.append((nm,cnt,len(recs),pos,len(raw)-8,st[:28]))
    print(f'lang {lang:>8s}: {okc}/{tot} close'); [print('    ',d) for d in det[:2]]
