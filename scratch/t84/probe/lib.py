import runpy, os, struct
os.environ.setdefault('FM24_DB_DIR','D:/tmp2b/fm24-db/scratch/data')
K=runpy.run_path('scripts/fm24_dump.py')
CODEC=K['_reader']()
DB=K['DB_DIR']
MAGIC=b'\x28\xb5\x2f\xfd'

def load_member(archive, member):
    fn=f"{archive}_db.dat"
    p=DB/fn
    ents=CODEC["list_tables"](p,fn)
    e=[x for x in ents if x['path'].split('/')[-1]==member][0]
    db=p.read_bytes()
    base=int(CODEC["_archive_layout"](db)["data_base"])
    start=base+int(e['offset']); end=start+int(e['packed_size']); size=int(e['size'])
    zstd=CODEC['_zstd_module']()
    d=next((d for d in range(min(64,end-start)) if db[start+d:start+d+4]==MAGIC),None)
    assert d is not None, (fn,member)
    dctx=zstd.ZstdDecompressor()
    obj=dctx.decompressobj()
    out=obj.decompress(db[start+d:end])
    assert len(out)==size, (len(out),size)
    return out
