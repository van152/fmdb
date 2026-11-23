import runpy, sys, struct, collections
import numpy as np
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()
def load(arch,tid,n,S):
    raw=dump['load_payload'](codec,arch,tid); H=len(raw)-n*S-8
    return raw, np.frombuffer(raw,dtype=np.uint8,count=n*S,offset=H).reshape(n,S)

# continent side-by-side business areas
rc,Mc=load('client',5,7,34); rs,Ms=load('server',5,7,48)
print('cont client business 21B vs server 35B')
for i in range(7):
    print(i,'C',Mc[i,:21].tobytes().hex(),'S',Ms[i,:35].tobytes().hex(),'Sextra',Ms[i,21:35].tobytes().hex())
print('client extra-equal?', all(Mc[i,:21].tobytes()==Ms[i,:21].tobytes() for i in range(7)))
print('server extra cols distinct:',[ (o, len(np.unique(Ms[:,o]))) for o in range(21,35)])
print('client cols distinct:',[(o,int(Mc[:,o].min()),int(Mc[:,o].max()),len(np.unique(Mc[:,o]))) for o in range(21)])
# city detail
raw,M=load('client',2,56293,43)
print('\ncity u16@18:', collections.Counter(M[:,18:20].copy().view('<u2').ravel().tolist()).most_common(5))
print('city u16@18 min/max', int(M[:,18:20].copy().view('<u2').min()), int(M[:,18:20].copy().view('<u2').max()))
print('city byte20 hist', collections.Counter(M[:,20].tolist()).most_common(8))
print('city byte29 hist', collections.Counter(M[:,29].tolist()).most_common(5))
print('city byte0/9 hist', collections.Counter(M[:,0].tolist()).most_common(3), collections.Counter(M[:,9].tolist()).most_common(3))
print('city u32@10 sentinel count', int((M[:,10:14].copy().view('<u4')==0xffffffff).sum()), 'max', int(M[:,10:14].copy().view('<u4').max()))
print('city u32@14 sentinel', int((M[:,14:18].copy().view('<u4')==0xffffffff).sum()), 'max', int(M[:,14:18].copy().view('<u4').max()))
print('city u32@21 sentinel', int((M[:,21:25].copy().view('<u4')==0xffffffff).sum()), 'max', int(M[:,21:25].copy().view('<u4').max()))
print('city u32@25 sentinel', int((M[:,25:29].copy().view('<u4')==0xffffffff).sum()), 'max', int(M[:,25:29].copy().view('<u4').max()))
print('city lat range', float(np.frombuffer(M[:,1:5].tobytes(),dtype='<f4').min()), float(np.frombuffer(M[:,1:5].tobytes(),dtype='<f4').max()))
print('city lon range', float(np.frombuffer(M[:,5:9].tobytes(),dtype='<f4').min()), float(np.frombuffer(M[:,5:9].tobytes(),dtype='<f4').max()))
