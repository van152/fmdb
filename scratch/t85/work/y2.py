import sys
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
for arch in ('client','server'):
    ents,_=C.entries(arch)
    print('=====',arch)
    for e in ents:
        rc=e.get('record_count_header')
        if rc in (251,7047,753):
            print(f'  {e["path"]:38s} rc={rc:6d} size={e["size"]}')
    print('  all rc:',{e["path"].split("/")[-1]:e.get("record_count_header") for e in ents if e.get('record_count_header')})
