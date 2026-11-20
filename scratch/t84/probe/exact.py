import sys, struct
sys.path.insert(0,'scratch/t84/probe'); sys.path.insert(0,'scripts')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
import t84_join as J
raw3=lib.load_member('client','table_3.dat')
recs,_,_=J.lang_records(lib.load_member('lang_update','8_3.dat'),6,3)
for r in recs[:4]:
    nb=r['fields'][0].encode('utf-8')
    i=raw3.find(struct.pack('<I',len(nb))+nb)
    print(f"uid={r['uid']} name@{i}")
    print('   ctx -40:', raw3[i-40:i+8].hex(' '))
    # locate exact uid offset
    off=raw3.rfind(struct.pack('<I',r['uid']), i-2048, i)
    print('   uid abs offset', off, 'distance', i-off)
