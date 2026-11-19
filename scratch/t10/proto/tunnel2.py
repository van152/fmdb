import json, collections, importlib.util, re
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
pairs=json.loads(Path('scratch/t10/proto/tunnel.json').read_text())
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
clubs={f['code'] for f in si['entities']['club']['fields'] if f['parent'] is None}
# cross-check against cmp-chain resolved (A/B/S)
CH={'A':[(0xe82afc,0xe846ac)],'B':[(0xe89a34,0xe8cded)],'S':[(0xe57de0,0xe59000)]}
cmpres={'C4ty':(0x160,4),'CASt':(0x160,4),'CIns':(0x160,4),'CiCa':(0x160,4),'CnCV':(0x160,4),'Crep':(0xa8,2),'Crmb':(0x3c,1),'Csot':(0x160,4),'Cull':(0x160,4),'Cwwa':(0x160,4),'TCln':(0x164,1),'TCro':(0x164,1),'TCsn':(0x165,1),
 'CInr':(0x160,4),'CWsc':(0x24,1),'Cacb':(0x30,1),'Cadl':(0x30,1),'Cape':(0x30,1),'Capf':(0x30,1),'Cfis':(0x16b,1),'CiEC':(0x160,1),'CibC':(0x30,1),'Cprs':(0x16a,1),'Crpc':(0xa8,2),
 'CScP':(0x127,1),'Ctlv':(0x120,1),'Cyfn':(0xd8,2),'Cytv':(0x12c,1),'TCoi':(0xcc,4)}
tmap=collections.defaultdict(set)
for p in pairs: tmap[p['code']].add(p['off'])
agree=dis=miss=0
for c,(off,sz) in cmpres.items():
    got=tmap.get(c)
    if not got: miss+=1
    elif off in got: agree+=1
    else: dis+=1; print('  disagree',c,hex(off),'tunnel',[hex(x) for x in got])
print(f'tunnel vs cmp-chain: agree={agree} disagree={dis} tunnel-miss={miss} of {len(cmpres)}')
print('club codes with tunnel pair:', len(clubs&set(tmap)), '/', len(clubs))
offs=sorted({p['off'] for p in pairs if p['code'] in clubs})
print('distinct offsets for club codes:',len(offs))
print([hex(o) for o in offs[:40]])
