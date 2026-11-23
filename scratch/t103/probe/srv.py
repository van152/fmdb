import sys, struct
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
sys.path.insert(0, 'scripts')
import t38_multiframe as mf
codec = mf._codec()
for arch in ('server','client'):
    try:
        info = mf.archive_info(codec, arch)
    except Exception as e:
        print(arch,'fail',e); continue
    print('==',arch,'data_base',info['data_base'],'entries',len(info['entries']))
    for e in info['entries']:
        if e['path'].endswith(('table_14.dat','table_44.dat','table_1.dat')):
            print('  ',e['path'],e['offset'],e['packed_size'],e['size'])
            try:
                start,end = mf.member_bounds(e, info['data_base'])
                fr = mf.decode_frames_unbounded(info['data'], start)
                hit=[f for f in fr if f['length']==int(e['size'])]
                print('     frames',len(fr),'hits',len(hit))
                if hit:
                    d=hit[0]['data']
                    print('     payload',len(d),'hdr',d[:16].hex(' '))
                    if len(d)>12:
                        ver, cnt = struct.unpack_from('<H',d,6)[0], struct.unpack_from('<I',d,8)[0]
                        print('     ver',hex(ver),'count',cnt,'rowsize',(len(d)-13-9)/cnt if cnt else None)
            except Exception as ex:
                print('     err',ex)
