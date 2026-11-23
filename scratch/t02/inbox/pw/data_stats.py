"""Rebuild BASIC_PERSON row statistics from the original Zstd frame (read-only by default)."""
import argparse
import hashlib
import runpy
import struct
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
K=runpy.run_path(str(HERE.parents[2]/'t01/inbox/t01k/verify.py'))


def ev(raw, o, n):
    return {'payload_offset':hex(o),'bytes':raw[o:o+n].hex(' ')}


def summarize(cnt):
    return {'distinct':len(cnt),'min':min(cnt),'max':max(cnt),'zero':cnt[0],
            'top_8':cnt.most_common(8)}


def run():
    basic=K['BASIC_PATH'].read_bytes()
    assert hashlib.sha256(basic).hexdigest()==K['BASIC_SHA256'] and basic[8:12]==bytes.fromhex('28 b5 2f fd')
    codec=runpy.run_path(str(K['OLD_READER_PATH']))
    raw=codec['_stream_decompress'](basic[8:],256*1024*1024)
    assert len(raw)==54_060_043 and hashlib.sha256(raw).hexdigest()==K['RAW_SHA256']
    count,=struct.unpack_from('<I',raw)
    assert count==658011
    pos=5; by_class={}; lengths=K['CLASS_LENGTHS']
    ctr4_a={o:Counter() for o in (2,6,10)}
    ctr4_b={(o,d):Counter() for o in (2,6,10) for d in (0,2)}
    date_c123=Counter(); examples={}; date_neg={}; all_first8={}
    # Simulate only the successful class paths and the two observed base read sizes.
    # Check exact boundary, ordinal, and duplicate u32 for both width hypotheses.
    closure={c:{w:[0,0,0,0] for w in (4,8)} for c in lengths}
    # Check all independent W=4/8 choices too (future proof if flags change between reads).
    from itertools import product
    full={c:{ww:[0,0] for ww in product((4,8),repeat=4 if c in (1,2,3) else 1 if c==4 else 0)} for c in lengths}
    for ordinal in range(count):
        tag,c=raw[pos:pos+2]; assert tag==0x11
        length=lengths[c]; end=pos+length
        assert end<=len(raw)
        stored,a,b=struct.unpack_from('<III',raw,end-12)
        assert stored==ordinal and a==b
        if c not in by_class:
            by_class[c]=0
            examples[c]={'ordinal':ordinal,'row':ev(raw,pos,length),
                'ordinal_plus_two_ids':ev(raw,end-12,12),'W8_base_start':ev(raw,end-20,8)}
            all_first8[c]=Counter()
        by_class[c]+=1
        all_first8[c][int.from_bytes(raw[end-16:end-12],'little')]+=1
        for w in (4,8):
            start=2+4*w+8+18+3 if c in (1,2,3) else 2+w+4 if c==4 else 2
            # Reject a candidate that crosses the verified row boundary.
            x,y,z=struct.unpack_from('<III',raw,pos+start+8)
            m=closure[c][w]; boundary=start+20==length
            m[0]+=boundary; m[1]+=x==ordinal; m[2]+=y==z; m[3]+=boundary and x==ordinal and y==z
        # Boundary math depends on sum(ww) only. Count analytically below, no second row walk.
        if c==4:
            for o in ctr4_a:
                x,y=struct.unpack_from('<HH',raw,pos+o)
                ctr4_a[o][x+(y<<16)]+=1
                ctr4_b[o,0][x]+=1; ctr4_b[o,2][y]+=1
                if not 1800<=y<=2024 and o not in date_neg:
                    date_neg[o]={'ordinal':ordinal,**ev(raw,pos+o,4),'second_u16':y}
        elif c in (1,2,3):
            date_c123[struct.unpack_from('<H',raw,pos+52)[0]]+=1
        pos=end
    assert by_class=={1:166064,2:476158,3:4757,4:9839,5:1193}
    assert raw[pos:]==bytes.fromhex('00 00 00 00 01 4c bd 54 77')
    for c,poss in full.items():
        for ww in poss:
            start=2+sum(ww)+(8+18+3 if c<4 else 4 if c==4 else 0)
            poss[ww]=[start,start+20]
        good=[ww for ww,(_,end) in poss.items() if end==lengths[c]]
        assert good==[(8,)*len(next(iter(poss)))]
        assert closure[c][8]==[by_class[c]]*4
    date=lambda ct:{**summarize(ct),'in_1800_through_2024':sum(ct[y] for y in range(1800,2025)),
        'in_1900_through_2024':sum(ct[y] for y in range(1900,2025)), 'year_1900':ct[1900]}
    return {'source':str(K['BASIC_PATH']),'file_sha256':K['BASIC_SHA256'],'payload_sha256':K['RAW_SHA256'],
        'file_prefix_bytes':basic[:12].hex(' '),'file_prefix_offset':'0x0','payload_size':len(raw),
        'row_count':count,'class_counts':by_class,'trailer':ev(raw,pos,9),'sample_rows':examples,
        'class4_span_inventory':[{'row_offset_start':o,'row_offset_end_inclusive':o+3,'u32_le':summarize(ctr4_a[o]),
            'first_u16_le':summarize(ctr4_b[o,0]),'second_u16_as_Pdob_year':date(ctr4_b[o,2]),
            'first_second_u16_year_negative_control':date_neg.get(o)} for o in ctr4_a],
        'Pdob_year_class123_row_52':date(date_c123),
        'base_first_8_upper_dword_at_row_end_minus_16_by_class':{c:summarize(m) for c,m in all_first8.items()},
        'uniform_width_experiment':{c:{w:dict(zip(('boundary_matches','ordinal_matches','repeated_dwords_match','all_three_match'),m)) for w,m in d.items()} for c,d in closure.items()},
        'independent_width_choices':{c:[{'widths':ww,'base_cursor_row_offset':v[0],'end_cursor_row_offset':v[1],
            'matches_framed_length':v[1]==lengths[c]} for ww,v in d.items()] for c,d in full.items()}}


def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--selftest',action='store_true',required=True); p.parse_args()
    try:
        stats=run(); print('rows',stats['row_count']); print(*stats['class4_span_inventory'],sep='\n'); print(stats['uniform_width_experiment']); print(stats['Pdob_year_class123_row_52'])
        return 0
    except AssertionError as ex:
        print('check failed',ex); return 1
    except Exception as ex:
        print('fatal',ex); return 2


if __name__=='__main__': raise SystemExit(main())
