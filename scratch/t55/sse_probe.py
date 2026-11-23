exec(open('scratch/t55/probe.py').read().split('for x in sys.argv')[0].replace('Path(__file__).resolve().parents[2]','Path.cwd()'))
import re
for i in (0x1a4,0x1a8,0x1ac,0x1b0,0x1b4,0x184,0x1b8):
 print(f'{i:x}'); token=i.to_bytes(4,'little'); matches={}
 for v in re.finditer(re.escape(token),p.raw):
  end=v.end()
  for a in range(v.start()-5,v.start()-1):
   if p.raw[a] not in (0xf3,0xf2,0x0f,0x66):continue
   z=D(a)
   if not z or a+z.size!=end:continue
   if z.mnemonic in ('movss','mulss','addss','subss','comiss','ucomiss','cvtss2sd','cvttss2si','cvtsi2ss','minss','maxss','divss') and any(o.type==3 and o.mem.disp==i for o in z.operands):
    matches[a]=z.mnemonic+' '+z.op_str
 for a,x in sorted(matches.items()):print(f'{a:x}',x)
