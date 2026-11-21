import json,collections
p=json.load(open('scratch/t88/tcget_pairs.json'))
g=collections.defaultdict(list)
for a,tag,rt,b in p: g[rt].append((tag,hex(a)))
for rt in sorted(g):
    print(rt, [t for t,_ in g[rt]])
