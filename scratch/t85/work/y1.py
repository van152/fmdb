import sys
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
ents,base=C.entries('client')
print('base',base,'n',len(ents))
print(sorted(ents[0].keys()))
for e in ents[:3]: print(e)
import collections
print(collections.Counter(e.get('entry_type') for e in ents).most_common())
