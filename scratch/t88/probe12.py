import struct,json
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
starts=json.load(open('scratch/t88/rows.json'))['starts']
rows=list(zip(starts,starts[1:]+[L-8]))
for i in (0,1,2):
    s,e=rows[i]; r=b[s:e]
    print(f'row{i} len={e-s}')
    for o in range(0,len(r),8):
        print(' ',o, r[o:o+8].hex(' '))
