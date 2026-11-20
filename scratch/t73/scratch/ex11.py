import runpy, sys, struct, collections
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()
# cont server extra zero region check
s=dump['load_payload'](codec,'server',5); c=dump['load_payload'](codec,'client',5)
for i in range(7):
    rb=s[13+i*48:13+(i+1)*48]; cb=c[13+i*34:13+(i+1)*34]
    extra=rb[22:36]
    print('cont srv row',i,'extra22..36',extra.hex(),'client biz==server biz[:21]?',cb[1:22]==rb[1:22])
# region server extra byte
rs=dump['load_payload'](codec,'server',19); rc=dump['load_payload'](codec,'client',19)
xs=set(); pre=0
for i in range(28):
    rb=rs[13+i*46:13+(i+1)*46]; cb=rc[13+i*45:13+(i+1)*45]
    xs.add(rb[33]); pre += (cb[1:33]==rb[1:33])
print('regi srv byte33 set',xs,'client biz32==server biz[:32]:',pre,'/28')
print('regi client biz u32s row0',[hex(x) for x in struct.unpack_from('<8I',rc,14)])
# currency walk
raw=dump['load_payload'](codec,'client',41)
n=struct.unpack_from('<I',raw,8)[0]; p=14
items=collections.Counter(); yrs=[]; kinds=collections.Counter(); ok=0
for i in range(n):
    sel=raw[p-1] if p>14 else raw[13]
    for k in range(4):
        ln=struct.unpack_from('<I',raw,p)[0]; p+=4+ln
    rate=struct.unpack_from('<f',raw,p)[0]; p+=4
    cnt=struct.unpack_from('<I',raw,p)[0]; p+=4
    for j in range(cnt):
        kind=raw[p]; yr=struct.unpack_from('<H',raw,p+1)[0]; val=struct.unpack_from('<f',raw,p+3)[0]
        kinds[kind]+=1; yrs.append(yr); items[(yr)]+=1; p+=7
    j,u,v=struct.unpack_from('<III',raw,p)
    mark=raw[p+12]
    if j==i and u==v and mark==0: ok+=1
    p+=13
print('curr rows',n,'identity ok',ok,'end',p,'len',len(raw),'left',len(raw)-p, 'footer',raw[p:].hex())
print('item kinds',kinds,'year range',min(yrs),max(yrs))
