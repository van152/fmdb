import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_table_for_old_save_23.bin').read_bytes()
for o in range(3895,len(b)):
    print(o, f'{b[o]:02x}')
