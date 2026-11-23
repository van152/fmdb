import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_table_for_old_save_25.bin').read_bytes()
for o in range(0,300,16):
    print('%5d'%o,' '.join('%02x'%x for x in b[o:o+16]),'|',''.join(chr(x) if 32<=x<127 else '.' for x in b[o:o+16]))
