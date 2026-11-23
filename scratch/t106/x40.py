import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
b=(D/'payload_server_simple_vars.bin').read_bytes()
H=34
def u(off,w):
    return int.from_bytes(b[off:off+w],'little')
for iw in (1,2):
  for lw in (1,2):
    for unit in (1,2,4):
      for base in (H,):
        off=base; ids=[]; ok=True
        while off+iw+lw<=len(b):
            i=u(off,iw); L=u(off+iw,lw)
            nxt=off+iw+lw+L*unit
            if nxt>len(b): ok=False; break
            ids.append(i); off=nxt
        if ok and off==len(b) and len(ids)>5:
            inc=sum(1 for a,c in zip(ids,ids[1:]) if c>a)
            print(f'iw={iw} lw={lw} unit={unit} recs={len(ids)} uniq={len(set(ids))} increasing_pairs={inc}/{len(ids)-1} first={ids[:8]} maxid={max(ids)}')
