#!/usr/bin/env python3
"""Rebuild t49: offline NATIONAL_TEAM_CONTAINER wire replay and evidence."""
import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'scratch/t49/out'
EXE = ROOT.parent/'fm24/input/editor.exe'
HEAD = bytes.fromhex('03017461642ef10d')
PARENTS = {'Nntp':(224,1,9,0x105e264,0x41ba910), 'Nctp':(225,1,8,0x105e2e9,0x41babb0),
           'Nrtp':(226,1,8,0x105e369,0x41babb0), 'NTRv':(228,1,4,0x105e9ec,0x105ea36),
           'NWGv':(229,1,4,0x105ea6b,0x105eab5), 'NSps':(230,1,4,0x105eaea,0x105eb34),
           'Nfmp':(233,2,9,0x105d99c,0x3d86430), 'NCro':(231,4,9,0x105f304,0x105f487)}
EXEH='b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
MASTER='evidence/fm24/reports/editor_schema/master.json'
T47='scratch/t47/out/discovery_nation_unknown.json'
BASE='scratch/t37/out/nation_subtable_inventory.json'
IDA='evidence/fm24/reports/qa/IDA_PROVENANCE.md'

class Check(Exception): pass

def need(cond,msg):
    if not cond: raise Check(msg)

def digest(x): return sha256(x).hexdigest()
def J(p): return json.loads((ROOT/p).read_bytes())
def put(name,obj): (OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def hist(xs): return dict(sorted(Counter(xs).items()))

class Cursor:
    def __init__(self,b): self.b=b; self.p=13; self.row=-1; self.events=[]
    def fail(self,at,site,kind,**info):
        raise Check(dict(row=self.row,absolute=at,site=site,kind=kind,raw=self.b[at:at+8].hex(),**info))
    def cut(self,w,s,n=1):
        at=self.p; end=at+w*n
        if not 0<=w*n<=len(self.b)-at: self.fail(at,s,'short transfer',width=w,repeat=n)
        self.p=end; self.events.append([s,at,w,n]); return self.b[at:end]
    def num(self,w,s,signed=False): return int.from_bytes(self.cut(w,s),'little',signed=signed)
    def count(self,w,s,itemmin,signed=True):
        at=self.p; v=self.num(w,s,signed)
        if not 0<=v<=(len(self.b)-self.p)//itemmin: self.fail(at,s,'invalid count',value=v,width=w,item_min=itemmin)
        return v
    def vec(self,w,s,stride,s2,signed=True):
        n=self.count(w,s,stride,signed)
        if n: self.cut(stride,s2,n)
    def string(self):
        n=self.count(4,0x35b0828,1,False)
        if n: self.cut(1,0x35b0883,n)

def collection(c,rows,key,tag=None,gate=None):
    _,w,stride,s,item=PARENTS[key]; at=c.p
    n=c.count(w,s,stride,key not in ('NTRv','NWGv','NSps'))
    start=c.p
    if n: c.cut(stride,item,n)
    rows[key]=dict(count_at=at,count=n,start=start,end=c.p,gate=gate,tag=tag)

def full_prefix(c,cols):
    for s,w in [(0x105cbcf,2),(0x105cbf4,4),(0x105cc19,4),(0x105cc6c,4)]: c.cut(w,s)
    for _ in range(c.count(4,0x105cc9d,8)):
        c.cut(4,0x105cd0d); c.cut(4,0x105cd2d)
    for s,w in [(0x105cd5a,4),(0x105cd81,2),(0x105cdb6,4),(0x105cdda,2),(0x105cdfe,2),(0x105ce56,1),(0x105ce7a,4),(0x105cfcc,1),(0x105cff0,2),(0x105d014,4),(0x105d038,2),(0x105d088,4)]: c.cut(w,s)
    for _ in range(c.count(4,0x360e3ce,6,False)):
        c.cut(4,0x360e43f); tag=c.num(1,0x837cd9)
        c.cut(tag,0x837cf2)
    c.vec(4,0x838b6b,1,0x838aff,False) # callback summary traced separately
    for _ in range(2): c.vec(4,0x3d81aff,2,0x3d81b7b,False)
    c.vec(1,0x105d128,4,0x105d170)
    c.vec(2,0x105d1a9,4,0x105d1ef)
    for groups in range(5):
        for s,t in [(0x105d2d8,0x105d339),(0x105d375,0x105d3c1),(0x105d3fd,0x105d449),(0x105d485,0x105d4d1)]: c.vec(1,s,4,t)
    c.vec(2,0x105d52d,4,0x105d573)
    # 0x105d644 / 0x105d6ce: summarized below after the shared helper is reduced.
    c.vec(2,0x105d644,1,0x1570e83)
    c.vec(2,0x105d6ce,1,0x1570e83)
    at=c.p; present=c.num(1,0x105d8c6)
    if present:
        tag=c.num(1,0x105f2e7)
        collection(c,cols,'NCro',tag,[at,present])
    else: cols['NCro']=dict(count_at=None,count=None,start=None,end=None,gate=[at,present],tag=None)
    collection(c,cols,'Nfmp')
    for _ in range(2): c.vec(4,0x10733c2,1,0x443aed0)
    for _ in range(c.count(2,0x105db62,13)):
        for s,w in [(0x3d8762f,4),(0x3d8764b,4),(0x3d87667,4),(0x3d87683,1)]: c.cut(w,s)
    c.vec(4,0x1073732,1,0x39b9d60)
    c.cut(1,0x105dc2b); c.cut(4,0x105dcd5)
    if c.num(1,0x105dd07):
        n=c.count(4,0x4387ae0,1); c.cut(1,0x155c120,n)

def full_base_tail(c):
    # Same-width transfers grouped, with the vcall site order retained.
    for s in range(0x105e7e9,0x105e8c2,0x24): c.cut(4,s)
    for s,w in [(0x105e8e5,1),(0x105e95e,4),(0x105e982,1),(0x105e9a6,2),(0x105e9ca,1)]: c.cut(w,s)

def common(c,mode,cols):
    c.cut(4,0x105dd87)
    for s in (0x105dddf,0x105de03,0x105de23,0x105de43,0x105de63,0x105def3,0x105df21): c.cut(1,s)
    c.cut(4,0x105df58)
    for s in (*range(0x105df7c,0x105e109,0x24),0x105e15c,0x105e180,0x105e1a4,0x105e1c8): c.cut(1,s)
    for k in ('Nntp','Nctp','Nrtp'): collection(c,cols,k)
    for s in (0x105e619,0x105e63d,0x105e661,0x105e685): c.cut(2,s)
    if mode:
        full_base_tail(c)
        for k in ('NTRv','NWGv','NSps'): collection(c,cols,k)
        for s in range(0x105ec47,0x105edf8,0x24): c.cut(1,s)
        for s,w in [(0x105ee1b,4),(0x105ee3f,4),(0x105ee63,2),(0x105ee87,1),(0x105eeab,1),(0x105eecf,2)]: c.cut(w,s)

def team_tail(c,mode):
    c.cut(1,0x3fc2050)
    c.cut(2,0x11d0f6f)
    if mode:
        raise Check(dict(row=c.row,absolute=c.p,site=0x11d0fa4,kind='mode 1 team helper not reduced'))
    return c.p,struct.unpack('<III',c.cut(12,0x11d21df))

def walk(b,mode,limit=None):
    need(len(b)>=13 and b[:8]==HEAD,'header'); n=struct.unpack_from('<I',b,8)[0]
    c=Cursor(b); rows=[]; ids=set(); first={}
    for j in range(n if limit is None else limit):
        c.row=j; c.events=[]; a=c.p; cols={}
        selector=c.num(1,0xf2ba0e)
        if selector!=0: c.fail(a,0xf2ba0e,'selector outside confirmed domain',value=selector)
        if mode: full_prefix(c,cols)
        common(c,mode,cols)
        at,ident=team_tail(c,mode)
        if ident[0]!=j or ident[1]!=ident[2] or not ident[1] or ident[1] in ids:
            c.fail(at,0x11d21df,'identity after reader',value=ident)
        ids.add(ident[1]); end=c.p
        for s,p,w,nrep in c.events: first.setdefault(s,dict(row=j,absolute=p,width=w,repeat=nrep))
        rows.append(dict(row=j,selector=selector,wire13=a,legacy14=a+1,end=end,length=end-a,identity_at=at,identity=ident,
            wire_sha256=digest(b[a:end]),legacy_sha256=digest(b[a+1:end+1]),collections=cols,trace=c.events))
    footer=None
    if limit is None:
        if len(b)-c.p!=9: c.fail(c.p,0xf2ba99,'footer/EOF',remaining=len(b)-c.p)
        count,flag,maxid=struct.unpack_from('<IBI',b,c.p)
        if (count,flag,maxid)!=(0,1,max(ids,default=0)): c.fail(c.p,0xf2ba99,'footer disagreement',value=(count,flag,maxid))
        footer=dict(absolute=c.p,count=count,flag=flag,last_u32=maxid,equals_observed_max_identity=True,raw=b[c.p:].hex())
    return dict(mode=mode,payload_len=len(b),payload_sha256=digest(b),rows=rows,row_count=len(rows),row_sum=sum(r['length'] for r in rows),
        wire_header=13,wire_footer=9,legacy_header=14,legacy_footer=8,footer=footer,first_site=first,
        selector_hist=hist(r['selector'] for r in rows),row_len_hist=hist(r['length'] for r in rows))

if __name__=='__main__':
    from t47_nation_unknown import read_archives
    _,raw=read_archives()
    for key,b in raw.items():
        if '9.' not in key[1]: continue
        for mode in (0,1):
            try:
                r=walk(b,mode); print(key,mode,r['row_count'],r['row_sum'],r['footer'])
            except Check as e: print(key,mode,e)
