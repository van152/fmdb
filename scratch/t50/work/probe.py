import hashlib,json,os,pathlib,runpy,struct,sys
ROOT=pathlib.Path(r'D:\tmp2b\fm24-db'); sys.path.append(r'D:\tmp2b\fm24\tools\python')
import zstandard as z
codec=runpy.run_path(r'D:\tmp2b\fm24\scripts\modding_read_dbdat.py')
DB=pathlib.Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
def H(b): return hashlib.sha256(b).hexdigest()
out={}
for side,exp in [('client',31),('server',77)]:
    p=DB/f'{side}_db.dat'; db=p.read_bytes()
    lay=codec['_archive_layout'](db); base=lay['data_base']; es={(x['path'].split('/')[-1]):x for x in lay['entries']}
    print(side,'base',base,'entries',len(lay['entries']),'names~',list(es)[:3])
    for name in ('table_9.dat','table_extra_9.dat','table_10.dat','table_extra_10.dat'):
        e=es.get(name)
        if not e: print(' ',side,name,'ABSENT'); out[side,name]=None; continue
        lo=base+e['offset']; hi=lo+e['packed_size']; part=db[lo:hi]
        # frames
        i=0; frames=[]
        while i<len(part):
            assert part[i:i+4]==b'\x28\xb5\x2f\xfd',(name,i)
            s=z.ZstdDecompressor().decompressobj(); pl=s.decompress(part[i:]); w=len(part)-i-len(s.unused_data)
            frames.append((lo+i,w,len(pl))); 
            if len(pl)==e['size']: payload=pl
            i+=w
        print(' ',side,name,'off',e['offset'],'psz',e['packed_size'],'size',e['size'],'start',lo,'frames',frames,'packedSHA',H(part)[:16],'entrySHA',str(e.get('sha256'))[:16],'plSHA',H(payload)[:16],'len',len(payload))
        print('    head',payload[:24].hex())
        out[side,name]=dict(payload=payload,meta=dict(offset=e['offset'],packed_size=e['packed_size'],size=e['size'],start=lo,frames=frames,packed_sha=H(part),entry_sha=e.get('sha256'),payload_sha=H(payload),payload_len=len(payload),head=payload[:32].hex()))
json.dump({k:(None if v is None else v['meta']) for k,v in out.items()},open(ROOT/'scratch/t50/work/probe.json','w'),indent=1)
