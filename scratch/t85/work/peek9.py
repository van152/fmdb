import json,sys,runpy
sys.stdout.reconfigure(encoding='utf-8')
k=runpy.run_path('scratch/t01/inbox/t01k/verify.py')
codec=runpy.run_path(k['OLD_READER_PATH'])
print([x for x in codec if not x.startswith('_')][:30])
print([x for x in codec if x.startswith('_')][:30])
