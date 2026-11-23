import sys, runpy, json, struct
from hashlib import sha256
sys.path.append(r'D:\tmp2b\fm24\tools\python')
M=runpy.run_path('scripts/fm24_dump.py',run_name='x')
codec=M['_reader']()
raw={}
for side,tabs in (('client',(2,3,5,10,21,23,25)),('server',(2,3,5,10,21,23,24,25))):
    for t in tabs:
        raw[side,t]=M['load_payload'](codec,side,t)
        print(side,t,len(raw[side,t]),raw[side,t][:14].hex())
import pickle
pickle.dump(raw,open('scratch/t72/work/raw.pkl','wb'))
