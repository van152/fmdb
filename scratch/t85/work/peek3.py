import json,sys
sys.stdout.reconfigure(encoding='utf-8')
def L(p): return json.loads(open(p,encoding='utf-8').read())
inv=L('scratch/t72/out/inventory.json')
n=inv['tables']['nation']['slots']
print('%-4s %-8s %-18s %-4s %-5s %-14s %s'%('pos','kind','slot_type','w','disp','cov','claims'))
for s in n:
    print('%-4d %-8s %-18s %-4s %-5s %-14s %s'%(s['position'],s['kind'],s['slot_type'],s['nominal_width'],s['object_displacement'],s['coverage'],s['claims']))
