import sys, json
sys.path.insert(0,'scratch/t02/inbox/a')
from _dis import data, pe, opt, base, secs, va, off, md
import capstone.x86_const as x86

def q(o): return int.from_bytes(data[o:o+8],'little')

census={x['type_id']:x for x in json.load(open('scratch/t01/inbox/t01h/output.json'))['census']}
MASTER=json.load(open('evidence/fm24/reports/editor_schema/master.json'))
ent2fields={}
for k,v in MASTER['entities'].items():
    for e in v: ent2fields[e['id']]=[f['field'] for f in e['fields']]

for tid in (19,41,23,8,2,18,24,6):
    c=census[tid]
    cc=c['constructor_classes'][0]
    vptr=int(cc['rtti']['vptr_file_offset'],16)
    ent=cc['entity']['matched'][0] if cc['entity']['matched'] else None
    print('='*70)
    print(f"type {tid} entity={ent} vptr={vptr:#x} fields={ent2fields.get(ent)}")
    slots=[]
    for i in range(0,12):
        p=q(vptr+i*8)
        slots.append(off(p))
    print('  vtable slots ->', [hex(s) if s is not None else None for s in slots])
