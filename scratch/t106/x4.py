import pathlib,sys,struct,collections
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
def get(n): return (D/f'payload_server_{n}.bin').read_bytes()
b=get('table_for_old_save_23')
print('len',len(b))
print('last 16:',b[-16:].hex())
print('12+278*14=',12+278*14,'15+278*14=',15+278*14)
# test hypothesis header 13 stride 14 footer 9
for s in (12,13,14,15):
    k=14; f=len(b)-s-278*k
    print('start',s,'footer',f,'footer bytes',b[s+278*k:].hex())
