import sys,struct
sys.path.insert(0,'scripts')
import numpy as np, t74_frames_part2 as P
b=open('scratch/t88/t45.bin','rb').read(); L=len(b); n=84477
for (lo,hi,W) in ((12,L-8,13),(14,L-8,13),(12,L-8,12)):
    paths,starts,layers=P._dp(b,'t45',lo,hi,n,W,strict_uid=True,pair=True)
    print('lo',lo,'W',W,'paths',paths)
    if paths:
        lens=sorted(set(starts[i+1]-starts[i] for i in range(n-1)))
        print('  distinct lens',len(lens),lens[:6],lens[-4:],'first',starts[:3])
