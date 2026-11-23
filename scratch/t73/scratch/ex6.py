import runpy, sys, struct
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()
raw=dump['load_payload'](codec,'client',2)
n=struct.unpack_from('<I',raw,8)[0]
print('count',n,'len',len(raw),'hdr13',raw[:13].hex(),'hdr14',raw[:14].hex())
for h in (13,14):
    S=(len(raw)-h-9)//n if h==13 else (len(raw)-h-8)//n
    print('h',h,'S',S,'close',h+n*S+(9 if h==13 else 8)==len(raw))
    ok=0; ok13=0
    for i in range(n):
        b=h+i*S
        r=raw[b:b+S]
        rdui,dn,dn2=struct.unpack_from('<III',r,S-13) if False else (0,0,0)
        # try 12B at S-12 and 13B at S-13
        a1=struct.unpack_from('<III',r,S-12)
        a2=struct.unpack_from('<III',r,S-13)
        if a1[0]==i and a1[1]==a1[2]: ok+=1
        if a2[0]==i and a2[1]==a2[2]: ok13+=1
    print('  identity 12B at S-12 ok',ok,'of',n,'; 13B at S-13 ok',ok13)
    for i in range(2):
        b=h+i*S
        print('  row',i,' '.join(f'{i:02d}:{x:02x}' for i,x in enumerate(raw[b:b+S])))
    print('  tail from',len(raw)-12, raw[-12:].hex())
