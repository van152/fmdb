import json
m=json.load(open('scratch/t88/f4_to_rectype.json'))
master=json.load(open('evidence/fm24/reports/editor_schema/master.json'))
fields=master['entities']['club.xml'][0]['fields'][211:328]
hit=0; miss=[]
for i,f in enumerate(fields,211):
    c=f['field']
    if c in m: hit+=1; print(i,c,f['type'],'->',m[c])
    else: miss.append((i,c,f['type']))
print('\nhit',hit,'miss',len(miss))
print('miss codes:',[c for _,c,_ in miss])
