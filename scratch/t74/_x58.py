import numpy as np, collections, pickle
P=np.load('scratch/t74/_p24.npy'); O=np.load('scratch/t74/_o24.npy')
byord=collections.defaultdict(list)
for p,o in zip(P.tolist(),O.tolist()): byord[o].append(p)
for o in list(range(0,25)):
    print(o, byord.get(o))
