import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
from importlib import import_module
sys.path.insert(0,'scripts')
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
import t84_join as J
recs,end,st=J.lang_records(lib.load_member('lang_update','8_3.dat'),6,3)
uids=[r['uid'] for r in recs]
print('n',len(uids),'sorted?',uids==sorted(uids),'min',min(uids),'max',max(uids))
print('first 20',uids[:20])
# gaps
print('dups', len(uids)-len(set(uids)))
raw3=lib.load_member('client','table_3.dat')
# for a few records, find the name and its row ordinal by counting rows is expensive;
# instead check whether uid appears anywhere within +/-2KB of the name
for r in recs[:6]:
    nb=r['fields'][0].encode('utf-8')
    i=raw3.find(struct.pack('<I',len(nb))+nb)
    win=raw3[max(0,i-2048):i+len(nb)+64]
    near=struct.pack('<I',r['uid']) in win
    print(r['uid'], repr(r['fields'][0][:28]), 'name@',i,'uid within 2KB:',near)
