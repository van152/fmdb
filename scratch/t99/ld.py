import sys,struct,runpy
sys.path.insert(0,r'D:\tmp2b\fm24\tools\python')
K=runpy.run_path(r'scripts/t38_multiframe.py')
_c=K['_codec'](); _cache={}
_info=K['archive_info'](_c,'lang_update',_cache)
def load(m):
    e=[x for x in _info['entries'] if x['path'].split('/')[-1]==m][0]
    return K['inspect_entry'](_c,e,_info)['data']
def names():
    return sorted(x['path'].split('/')[-1] for x in _info['entries'])
def dump(raw,off=0,n=200):
    s=raw[off:off+n]
    for i in range(0,len(s),16):
        ch=s[i:i+16]
        print(f"  {off+i:6d} {ch.hex(' '):<48} {''.join(chr(c) if 32<=c<127 else '.' for c in ch)}")
