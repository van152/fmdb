import sys,struct
sys.stdout.reconfigure(encoding='utf-8')
ed=open(r'D:\tmp2b\fm24\input\editor.exe','rb').read()
for off in (17048862,17048874,17048098,17050846,17048156,17047713,16660317):
    print(f'{off} 0x{off:x}', ed[off:off+24].hex(' '))
