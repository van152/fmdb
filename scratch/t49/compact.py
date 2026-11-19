import sys,subprocess,re
for p in sys.argv[1:]:
 s=subprocess.check_output([sys.executable,'-I','-B','scratch/t49/scan.py',p],text=True).splitlines(); print(p)
 for i,l in enumerate(s):
  if re.search(r' call +', l) and ('0x28]' in l or any(k in l for k in ('814110','837ca0','db7f80'))):
   print(' | '.join(s[max(0,i-5):i+1]))
  elif re.search(r' j(ae?|be?|e|ne|le|g|ge|l|s) +',l) and not re.search(r'(test|cmp) +.*(?:0x10\]|gs:|\[rip|qword ptr|, rax$)',s[i-1]): print(s[i-1],l)
