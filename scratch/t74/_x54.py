import json
d=json.load(open('evidence/fm24/reports/editor_schema/master.json'))
e=d['entities']['media source.xml']
print(len(e))
for x in e[:25]: print(x)
