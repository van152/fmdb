import struct,json
dt=open('scratch/t127/out/_dt.bin','rb').read()
def dec(off):
    b=dt[off:off+44]; g=lambda o,n:int.from_bytes(b[o:o+n],'little')
    return dict(y0=g(0,2),y1=g(2,2),f4=g(4,1),apps=g(5,1),goals=g(6,1),p7=g(7,4),
      club=g(11,4),comp=g(19,4),f27=g(27,1),s1=(g(28,2),g(30,2)),s2=(g(32,2),g(34,2)),
      s3=(g(36,2),g(38,2)),nxt=g(40,4))
idat=open('scratch/data/pl_hist_id.dat','rb').read()
n=(len(idat)-8)//8
bb=struct.unpack('<%dI'%(n*2),idat[8:8+n*8]); s=bb[0::2]; e=bb[1::2]
ip=open('scratch/data/pl_hist_index.dat','rb').read()
import sys
sys.path.insert(0,r'D:\tmp2b\fm24\tools\python')
import zstandard as z
pay=z.ZstdDecompressor().decompress(ip[8:],max_output_size=1<<26)
nn=struct.unpack('<I',pay[:4])[0]
keys=struct.unpack('<%dI'%(nn*2),pay[4:4+nn*8])[0::2]
import bisect
res={}
for name,uid in (('kane',28049320),('ronaldo',735216),('messi',7458500)):
    o=bisect.bisect_left(keys,uid)
    rows=[]; k=s[o]
    while k<e[o]:
        d=dec(k); d.pop('nxt'); rows.append(d); k+=44
    res[name]=dict(uid=uid,ordinal=o,nrows=len(rows),rows=rows)
open('scratch/t127/out/_stars.json','w',encoding='utf-8').write(json.dumps(res,indent=1))
for nm in res:
    print('==',nm,res[nm]['ordinal'],res[nm]['nrows'])
    for r in res[nm]['rows']:
        print('  %d-%d c%-5d p%-4d apps=%3d goals=%3d f4=%d f27=%d'%(r['y0'],r['y1'],r['club'],r['comp'],r['apps'],r['goals'],r['f4'],r['f27']))
