import capstone,struct,re
b=open('D:/tmp2b/fm24/input/editor.exe','rb').read()
# find stores/loads with disp 0x4c and 0x5e in modrm disp8 form
pat4c=re.compile(rb'[\x89\x8b\xc7\x8d\x3b\x8a\x88][\x40-\x7f]\x4c')
pat5e=re.compile(rb'[\x89\x8b\xc7\x8d\x3b\x8a\x88][\x40-\x7f]\x5e')
for name,pat in (('disp4c',pat4c),('disp5e',pat5e)):
    hits=[m.start() for m in pat.finditer(b)]
    print(name,len(hits))
