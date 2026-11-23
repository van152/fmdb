import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_table_for_old_save_23.bin').read_bytes()
cnt=struct.unpack_from('<I',b,8)[0]
for start,stride,ftr in ((14,14,8),(15,14,7),(13,14,9)):
    ok=all(struct.unpack_from('<I',b,start+stride*k)[0]==k for k in range(cnt))
    end=start+stride*cnt
    print(f'start={start} stride={stride} footer={ftr} index_ok={ok} end={end} tail={b[end:].hex(" ")} close={end+ftr==len(b)}')
print()
# summary tail
s=(D/'payload_summary.bin').read_bytes()
T=1637014
print('tail len',len(s)-T)
print('tail head',s[T:T+32].hex(' '))
# scan for ascending u32 run
off=T; ids=[]
while off+4<=len(s):
    v=struct.unpack_from('<I',s,off)[0]
    if ids and v<=ids[-1]: break
    if v==0xffffffff: break
    ids.append(v); off+=4
print('ascending u32 run',len(ids),'ends at',off,'first',ids[:5],'last',ids[-3:])
print('after run',s[off:off+24].hex(' '))
rest=len(s)-off
print('rest',rest,'mod8',rest%8)
