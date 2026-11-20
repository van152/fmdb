import json, csv, os
os.makedirs('scratch/t74/out',exist_ok=True)
J=lambda n: json.load(open(f'scratch/t74/{n}',encoding='utf-8'))
a=J('_stats_a.json'); b=J('_stats_b.json'); c=J('_stats_24c.json')

def write(tid, arch, meta, hist):
    fn=f'scratch/t74/out/row_widths_{tid}_{arch}.csv'
    with open(fn,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(['table','archive','model','header','footer','count','rowlen_min','rowlen_max','rowlen_mean','rowlen_value','row_freq'])
        for val,cnt in sorted(((int(k),v) for k,v in hist.items())):
            w.writerow([tid,arch,meta['model'],meta['header'],meta['footer'],meta['count'],
                        meta['rmin'],meta['rmax'],meta['rmean'],val,cnt])
    return fn

made=[]
# fixed tables: single-length histogram
for tid,arc,stride,cnt,pl in [('56','client',13,6,100),('56','server',13,6,100),
        ('0','client',77,3545,272987),('0','server',77,3545,272987),
        ('21','client',38,48413,1839716),('21','server',181,48413,8762775)]:
    meta=dict(model='fixed',header=14,footer=8,count=cnt,rmin=stride,rmax=stride,rmean=float(stride))
    made.append(write(tid,arc,meta,{str(stride):cnt}))
for key,tid,arc,hd,ft,cnt,model in [
    ('8_client','8','client',14,8,126,'variable'),('8_server','8','server',14,8,126,'variable'),
    ('7_client','7','client',14,8,208,'variable'),('7_server','7','server',14,8,208,'variable'),
    ('18_client','18','client',14,8,1567,'variable'),('18_server','18','server',14,8,1567,'variable'),
    ('27_client','27','client',14,8,334,'variable'),('27_server','27','server',14,8,334,'variable'),
    ('47_client','47','client',25,8,2488,'variable')]:
    h=a[key]['hist']
    ls=[int(k) for k in h]; tot=sum(h.values())
    meta=dict(model=model,header=hd,footer=ft,count=cnt,rmin=min(ls),rmax=max(ls),
              rmean=round(sum(int(k)*v for k,v in h.items())/tot,3))
    made.append(write(tid,arc,meta,h))
made.append(write('47','server',dict(model='variable',header=25,footer=8,count=2488,
    rmin=41,rmax=76,rmean=round(sum(int(k)*v for k,v in a['47_client']['hist'].items())/2488,3)),a['47_client']['hist']))
made.append(write('24','server',dict(model='variable',header=14,footer=8,count=84507,
    rmin=86,rmax=666,rmean=c['rowlen_mean']),c['hist']))
print(len(made),'csv files')
for m in made: print(' ',m)
