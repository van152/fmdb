import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def get(n): return (D/(('payload_summary.bin') if n=='summary' else f'payload_server_{n}.bin')).read_bytes()

b=get('table_for_old_save_23')
print('len',len(b),'hdr count',struct.unpack_from('<I',b,8)[0])
for o in range(12,12+70):
    pass
print('bytes 12..12+84:')
print(' '.join('%02x'%x for x in b[12:12+84]))
# try 14-byte rows starting at 12
for s in (12,13,14,15,16):
    n=(len(b)-s)//14
    print('start',s,'rows',n,'rem',(len(b)-s)-n*14)
    for i in range(3):
        r=b[s+i*14:s+i*14+14]; print('   ',i,' '.join('%02x'%x for x in r),struct.unpack('<3I',r[:12]))
