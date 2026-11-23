import json, csv
hist=json.load(open('scratch/t74/_hists.json',encoding='utf-8'))
c24=json.load(open('scratch/t74/_stats_24c.json',encoding='utf-8'))
frame=json.load(open('scratch/t74/out/frames.json',encoding='utf-8'))

made=[]
def emit(tid,arch,meta,h):
    fn=f'scratch/t74/out/row_widths_{tid}_{arch}.csv'
    with open(fn,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(['table','archive','model','header','footer','count','rowlen_min','rowlen_max','rowlen_mean','rowlen_value','row_freq'])
        items=sorted((int(k),int(v)) for k,v in h.items())
        tot=sum(v for _,v in items)
        mean=round(sum(k*v for k,v in items)/tot,3)
        for val,cnt in items:
            w.writerow([tid,arch,meta['model'],meta['header'],meta['footer'],meta['count'],
                        items[0][0],items[-1][0],mean,val,cnt])
    made.append(fn)

for tid,arch,stride,cnt in [('56','client',13,6),('56','server',13,6),('0','client',77,3545),
        ('0','server',77,3545),('21','client',38,48413),('21','server',181,48413)]:
    emit(tid,arch,dict(model='fixed',header=14,footer=8,count=cnt),{str(stride):cnt})

spec=[('8','client',14,8,126),('8','server',14,8,126),('7','client',14,8,208),('7','server',14,8,208),
      ('18','client',14,8,1567),('18','server',14,8,1567),('27','client',14,8,334),('27','server',14,8,334),
      ('47','client',14,8,2488),('47','server',14,8,2488)]
for tid,arch,hd,ft,cnt in spec:
    emit(tid,arch,dict(model='variable',header=hd,footer=ft,count=cnt),hist[f'{tid}_{arch}'])
emit('24','server',dict(model='variable',header=14,footer=8,count=84507),c24['hist'])
print(len(made),'files')
for f in made: print(' ',f)
