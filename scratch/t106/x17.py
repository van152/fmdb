import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_simple_vars.bin').read_bytes()
print('len',len(b))
def trygrammar(name, hdr, fmt, use_len_bytes=True):
    p=hdr; n=0
    try:
        while p<len(b):
            if fmt=='HIL':
                key,ln=struct.unpack_from('<HI',b,p); p+=6
            elif fmt=='HIH':
                key,ln=struct.unpack_from('<HH',b,p); p+=4
            elif fmt=='HIB':
                key,ln=struct.unpack_from('<HB',b,p); p+=3
            elif fmt=='IIL':
                key,ln=struct.unpack_from('<II',b,p); p+=8
            elif fmt=='BB':
                key,ln=struct.unpack_from('<BB',b,p); p+=2
            if ln>len(b)-p: return (name,p,n,'len overflow')
            p+=ln; n+=1
            if n>200000: return (name,p,n,'too many')
    except struct.error:
        return (name,p,n,'struct err')
    return (name,p,n,'ok' if p==len(b) else 'left %d'%(len(b)-p))
for hdr in (12,14):
    for fmt in ('HIL','HIH','HIB','IIL','BB'):
        print(hdr,fmt,trygrammar('x',hdr,fmt))
