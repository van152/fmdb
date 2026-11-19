import os,sys,importlib.util,struct
spec=importlib.util.spec_from_file_location("d","scripts/fm24_dump.py");m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m._reader()
def get(t):
    p=f"scratch/t33/probe/t{t}.bin"
    if os.path.exists(p): return open(p,"rb").read()
    raw=m.load_payload(c,"server",t); open(p,"wb").write(raw); return raw
person=get(49); club=get(3)
print("person49 len",len(person),"club3 len",len(club))
vals={29001407,80864099,2131246847,124518401,16777216}
for v in vals:
    pat=struct.pack("<I",v)
    print(f"{v:>12} in person49:{person.count(pat)} in club3:{club.count(pat)}")
