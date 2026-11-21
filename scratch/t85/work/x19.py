import sys
sys.stdout.reconfigure(encoding='utf-8')
for f in ('lang_update_db.dat','summary.dat','client_db.dat','server_db.dat'):
    raw=open(f'scratch/data/{f}','rb').read()
    for n in (b'Algeria',b'Les Fennecs',b'England'):
        print(f,n.decode(),raw.count(n))
