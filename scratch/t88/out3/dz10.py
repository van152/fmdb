import json
d=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
m=json.load(open('evidence/fm24/reports/editor_schema/master.json'))
codes=[f['field'] for f in m['entities']['club.xml'][0]['fields'][211:328]]
import collections
cnt=collections.Counter()
for c in codes:
    b=c.encode()
    n=d.count(b); cnt[n]+=1
print(cnt)
for c in ('CHSo','CYPp','CBWo','CHRf','CGMg'):
    i=0; locs=[]
    while True:
        i=d.find(c.encode(),i)
        if i<0: break
        locs.append(hex(i)); i+=1
    print(c, locs[:10], len(locs))
