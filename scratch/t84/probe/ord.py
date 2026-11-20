import sys, struct
sys.path.insert(0,'scratch/t84/probe'); sys.path.insert(0,'scripts')
import lib
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
import t84_join as J
raw3=lib.load_member('client','table_3.dat')
recs,_,_=J.lang_records(lib.load_member('lang_update','8_3.dat'),6,3)
# row0 body starts at 14; head was 7e 00 00 00 (db_id 126), ffffffff, 7e,7e
rows=list(lib.K['walk_club_block'](lib.K['load_payload'](lib.CODEC,'client','3')))
print('club row0 body', rows[0][2][:20].hex(' '))
print('row0 db_id', struct.unpack_from('<I',rows[0][2],0)[0])
print('row1 db_id', struct.unpack_from('<I',rows[1][2],0)[0])
print('row16 db_id', struct.unpack_from('<I',rows[16][2],0)[0])
print('row39 db_id', struct.unpack_from('<I',rows[39][2],0)[0])
# So lang uid 74 -> which row has ordinal 74?
for r in recs[:4]:
    nb=r['fields'][0].encode('utf-8')
    i=raw3.find(struct.pack('<I',len(nb))+nb)
    # find enclosing row
    row=[x for x in rows if x[1]<=i<x[1]+len(x[2])]
    print(f"lang uid {r['uid']} name {r['fields'][0][:24]!r} -> club ordinal {row[0][0] if row else None} db_id {struct.unpack_from('<I',row[0][2],0)[0] if row else None}")
