import sys,struct as s
sys.argv=[sys.argv[0]]
exec(open('scratch/t55/probe.py',encoding='utf8').read())
vt=0x1418c0048;o=p.va2f(vt); print(hex(o));
for n in [19,20,21]:print(n,hex(p.va2f(s.unpack_from('<Q',p.raw,o+8*n)[0])))
