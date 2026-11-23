import sys,struct
sys.stdout.reconfigure(encoding='utf-8')
raw=open('scratch/data/lang_update_db.dat','rb').read()
print('len',len(raw),'head',raw[:48].hex(' '))
print(repr(raw[:120]))
# find 'tad.' occurrences = nested members
p=0; hits=[]
while True:
    p=raw.find(b'tad.',p)
    if p<0: break
    hits.append(p); p+=1
print('tad. count',len(hits),'first 10',hits[:10])
print('fmf. count',raw.count(b'fmf.'))
print('zstd frames',raw.count(bytes.fromhex('28b52ffd')))
