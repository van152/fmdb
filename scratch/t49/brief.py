import sys,re
from pathlib import Path
sys.path.insert(0,str(Path('scripts').resolve()))
from t47_nation_unknown import read_archives
if 'data' in sys.argv:
 a,b=read_archives()
 for (s,k),x in b.items():
  if '9.' in k: print(s,k,len(x), x[:125].hex(' '),x[-30:].hex(' '))
else:
 ls=Path('scratch/t49/reader.txt').read_text().splitlines()
 for n,l in enumerate(ls):
  if 'call' in l and '0x28]' in l:
   w=next((x.split(', ')[-1] for x in ls[n-1:n-11:-1] if 'mov      r8d,' in x),'?')
   print(l[:8],w, next((x[x.find('['):] for x in ls[n-1:n-10:-1] if ('lea      rdx' in x or 'lea      rbp' in x) and '[' in x),''))
  elif re.search(' (?:ja[e]?|jb|jle|jl|jg|jge|je|jne) +',l) and not l.endswith(('105de6c','105de7e')):print('branch',ls[n-1].strip(),l.strip())
  elif 'call' in l and '=>' in l:print(l.strip())
