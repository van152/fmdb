import pathlib,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
D=pathlib.Path('scratch/t106/out')
a=(D/'payload_server_table_for_old_save_25.bin').read_bytes()
import runpy
sys.path.insert(0,'scripts')
mf=runpy.run_path('scripts/t38_multiframe.py'); codec=mf['_codec']()
inf=mf['archive_info'](codec,'server')
e=codec['_resolve_table'](25,inf['tables'],'server_db.dat')
s=mf['inspect_entry'](codec,e,inf)['data']
print('old25',len(a),'server25',len(s))
# common prefix
i=0
while i<min(len(a),len(s)) and a[i]==s[i]: i+=1
print('common prefix',i)
j=0
while j<min(len(a),len(s)) and a[-1-j]==s[-1-j]: j+=1
print('common suffix',j)
# does s contain a as subsequence at some offset? check if a[12:] appears in s
print('a[12:] in s?', s.find(a[12:200]))
print('a tail in s?', s.find(a[-200:]))
