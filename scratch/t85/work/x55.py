import sys,struct,zlib
sys.stdout.reconfigure(encoding='utf-8')
k=__import__('runpy').run_path('scratch/t01/inbox/t01k/verify.py')
codec=__import__('runpy').run_path(k['OLD_READER_PATH'])
z=codec['_zstd_module']()
raw=open('scratch/data/lang_update_db.dat','rb').read()
print('outer head',raw[:20].hex(' '))
# nested member at 47: 'fmf.' header -> use codec list_tables on it
import pathlib,tempfile
# try codec on the file directly
for f in ('lang_update_db.dat',):
    p=pathlib.Path('scratch/data')/f
    try:
        ents=codec['list_tables'](p,f)
        print(f,'entries',len(ents))
        for e in ents[:12]: print('  ',e['path'],e['offset'],e['packed_size'],e['size'])
    except Exception as ex: print(f,'ERR',ex)
