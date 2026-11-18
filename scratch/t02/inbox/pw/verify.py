"""Build/check t02-p from read-only editor.exe, schema snapshot, and basic_people_db.dat."""
import argparse
import hashlib
import json
from pathlib import Path
import runpy
import struct
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUTPUT = HERE/'output.json'


def build(s, stats, scan):
    raw, va, off, md, dec = (s[k] for k in ('E','va','off','MD','get'))
    editor_sha = hashlib.sha256(raw).hexdigest()
    assert editor_sha=='b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4'
    schema_rel='evidence/fm24/reports/editor_schema/master.json'
    schema=(ROOT/schema_rel).read_bytes(); schema_sha=hashlib.sha256(schema).hexdigest()
    manifest=json.loads((ROOT/'evidence/MANIFEST.json').read_text(encoding='utf-8'))
    def walk(o):
        if isinstance(o, list):
            for v in o: yield from walk(v)
        if isinstance(o, dict):
            if 'path' in o: yield o
            for v in o.values(): yield from walk(v)
    assert any(x['path']==schema_rel and x['sha256']==schema_sha for x in walk(manifest))
    entities=json.loads(schema)['entities']
    pers=next(t for t in entities['person.xml'] if t['id']=='pers')
    play=next(t for t in entities['player.xml'] if any(x['field']=='PCRP' for x in t['fields']))
    ps={x['field']:x for x in pers['fields']}; pl={x['field']:x for x in play['fields']}
    assert len(ps)==271

    def ev(o,n):
        return {'file_offset':hex(o),'va':hex(va(o)),'bytes':raw[o:o+n].hex(' ')}
    def check(o,expected):
        b=bytes.fromhex(expected); assert raw[o:o+len(b)]==b,(hex(o),expected)
        return ev(o,len(b))
    def body(a,b):
        ins=list(md.disasm(raw[a:b],va(a))); assert sum(i.size for i in ins)==b-a,(hex(a),hex(b))
        return [{**ev(off(i.address),i.size),'instruction':i.mnemonic+' '+i.op_str} for i in ins]
    def ref(o,target,length,index):
        i=next(md.disasm(raw[o:o+15],va(o),count=1)); assert i.size==length
        m=i.operands[index].mem
        assert i.address+i.size+m.disp==target
        return {**dec(o),'target_va':hex(target),'target_file_offset':off(target)}
    def rel(o,target):
        assert raw[o] in (0xe8,0xe9) and va(o)+5+struct.unpack_from('<i',raw,o+1)[0]==va(target)
        return {**dec(o),'target_file_offset':hex(target),'target_va':hex(va(target))}
    def vptr(o,target):
        assert struct.unpack_from('<Q',raw,o)[0]==va(target)
        return {**ev(o,8),'target_file_offset':hex(target),'target_va':hex(va(target))}
    def get_chain(code,c,b,m):
        assert raw[c:c+6]==b'\x81\xfa'+code.encode('ascii')[::-1]
        assert c+6==b
        i=next(md.disasm(raw[b:b+15],va(b),count=1)); assert i.mnemonic in ('je','jne')
        assert (i.operands[0].imm if i.mnemonic=='je' else i.address+i.size)==va(m)
        return {'compare':dec(c),'branch':dec(b),'member_access':dec(m)}
    getter_old=runpy.run_path(str(ROOT/'scratch/t01/inbox/t01k/verify.py'))['GETTER_EVIDENCE']
    getters={k:get_chain(k,v[0],v[2],v[4]) for k,v in getter_old.items()}
    getters.update({k:get_chain(k,c,b,m) for k,c,b,m in (
        ('PCRP',0xe507c8,0xe507ce,0xe507d4),('PCAB',0xe503fd,0xe50403,0xe50409),
        ('PPAB',0xe509c4,0xe509ca,0xe516b0),('PHRP',0xe5031f,0xe50325,0xe50bc0),
        ('PWRP',0xe50528,0xe5052e,0xe50ed4),('Pdva',0xe506b1,0xe506b7,0xe506bd),
        ('Pcww',0xe50540,0xe50546,0xe5054c),('PLag',0xe5032b,0xe50331,0xe50c2f))})
    for k,(c,cb,b,bb,m,mb) in getter_old.items():
        check(c,cb); check(b,bb); check(m,mb)
    def slot(at,n,m,d,c):
        assert raw[m:m+6]==bytes([0x41,0xb8,n,0,0,0]); assert raw[c:c+2]==b'\xff\x50' or raw[c:c+2]==b'\xff\xd0'
        return {'row_offset':at,'width':n,'object_offset':hex(d),'width_instruction':dec(m),'stream_call':dec(c)}
    tag={'row_offset':0,'width':1,'role':'record tag before slot 19','writer':check(0xe4fe98,'c6 44 24 2b 11'),
         'writer_width':dec(0xe4fea6),'table_read_call':check(0xf2af2f,'ff 50 28')}
    cl=slot(1,1,0xe4f393,0x65,0xe4f39f); cl['destination']=check(0xe4f38b,'48 8d 71 65')
    def attach_dest(z,o):
        d=int(z['object_offset'],16); assert raw[o:o+4]==bytes([0x48,0x8d,0x53,d]); z['destination']=dec(o); return z
    n1=attach_dest(slot(2,8,0xe4f4f6,0x30,0xe4f507),0xe4f4dc)
    long=[tag,cl,n1,attach_dest(slot(10,8,0xe4f542,0x20,0xe4f553),0xe4f529),
          attach_dest(slot(18,8,0xe4f57f,0x28,0xe4f590),0xe4f566),
          attach_dest(slot(26,8,0x3c6e121,0x38,0x3c6e132),0xe4f59c)]
    for o,at,n,d in [(0xe4f5ba,34,4,0x48),(0xe4f5da,38,4,0x4c)]+[
            (0xe4f5fa+j*0x20,42+2*j,2,d) for j,d in enumerate((0x50,0x52,0x54,0x56,0x58,0x5a,0x5e,0x60,0x62))]+[
            (0xe4f71a,60,1,0x64),(0xe4f73a,61,1,0x66),(0xe4f75a,62,1,0x68)]:
        long.append(attach_dest(slot(at,n,o,d,o+9 if o!=0xe4f75a else 0xe4f471),o-7))
    short=[tag,cl,n1,attach_dest(slot(10,2,0xe4f43c,0x52,0xe4f445),0xe4f432),
           attach_dest(slot(12,2,0xe4f468,0x5a,0xe4f471),0xe4f452)]
    short[3]['class4_copy_members']=[check(0xe4f456,'0f b7 43 52'),check(0xe4f45a,'66 89 43 54'),check(0xe4f45e,'66 89 43 50')]
    def base_fields(o):
        q=slot(o,8,0x3dc0241,0x18,0x3dc024a); q['destination']=check(0x3dc023a,'48 8d 51 18')
        q['role']='base prefix (schema meaning open)'
        block=slot(o+8,12,0x3dc027b,0x08,0x3dc0287); block['destination']=check(0x3dc0274,'48 8d 7e 08')
        block['subslots']=[{'row_offset':o+8+4*j,'width':4,'object_offset':hex(d),'role':role}
            for j,(d,role) in enumerate(((8,'wire ordinal, replaced by caller ordinal'),(12,'duni'),(16,'second ID word; copied from first if writer obj+0x10 is zero')))];
        return [q,block]
    groups={'1/2/3':long+base_fields(63),'4':short+base_fields(14),'5':[tag,cl]+base_fields(2)}
    for k,size in zip(groups,(83,34,22)):
        cursor=0
        for r in groups[k]:
            assert r['row_offset']==cursor; cursor+=r['width']
        assert cursor==size
    data=stats['uniform_width_experiment']
    assert all(data[c][8]['all_three_match']==n for c,n in stats['class_counts'].items())
    assert all(data[c][4]['all_three_match']==0 for c in (1,2,3,4))
    assert [r['second_u16_as_Pdob_year']['in_1800_through_2024'] for r in stats['class4_span_inventory']]==[0,0,9839]

    fields=[]
    for code,object_at in {'Ptyp':0x65,'Pnti':0x30,'Pcti':0x20,'Pnai':0x28,'Pdob':0x5a,
                           'PCJO':0x5e,'PSJO':0x60,'PNJO':0x62,'Piap':0x64,'duni':0x0c,
                           'PWRP':0x50,'PCRP':0x52,'PHRP':0x54,'PCAB':0x56,'PPAB':0x58}.items():
        schema_name, schema_id, props=('person.xml',pers['id'],ps) if code in ps else ('player.xml',play['id'],pl)
        assert code in props
        group_offsets={}
        for k, rr in groups.items():
            if schema_name=='player.xml' and k!='1/2/3': continue
            for r in rr:
                h=hex(object_at)
                if r.get('object_offset')==h:
                    group_offsets[k]={'row_offset':r['row_offset'],'wire_width':r['width'],'read_width':r['width_instruction']}; break
                z=next((q for q in r.get('subslots',[]) if q['object_offset']==h),None)
                if z:
                    group_offsets[k]={'row_offset':z['row_offset'],'wire_width':z['width'],'read_width':r['width_instruction'],
                        'writer_destination':dec(0xe4ffb1),'writer_width':dec(0xe4ffb9)}; break
        row={'code':code,'name':props[code]['name'],'schema':f'{schema_name}#{schema_id}',
             'object_offset':hex(object_at),'classification':'identity' if code=='duni' else 'business',
             'evidence_level':'L3 static member+cursor, L1 file-mode closure' if code!='Ptyp' else 'L3 mode-independent',
             'offsets_by_class':group_offsets,'getter':getters[code]}
        if code=='Pdob': row['wire_note']='BASIC_PERSON stores u16 year; getter constructs date-like value (year << 17) | 0x100; not a serialized full DOB day/month.'
        if code in ('PCRP','PHRP','PWRP'): row['wire_note']='raw signed-16 score; getter scales to display score; do not equate the raw u16 with display units.'
        fields.append(row)
    assert len(fields)==15 and sum(f['schema']=='person.xml#pers' for f in fields)==10
    assert next(f for f in fields if f['code']=='Pdob')['offsets_by_class']['4']['row_offset']==12
    assert sum(1 for r in scan['A']['potential_writer_or_address_sites'] if r['access']=='write')==1
    assert len(scan['B']['potential_writer_or_address_sites'])==13
    assert next(r for r in scan['B']['potential_writer_or_address_sites'] if r['file_offset']=='0x3c28b4e')['bytes']=='c6 05 d7 ba dc fd 01'
    for value in scan.values():
        value['absolute_literal_candidates']=[ev(int(o,16),8) for o in value['absolute_literal_hits']['VA_qword']]
    # Resolve the actual CRT dispatch of the initializer, not just a matching pointer.
    pe=s['PE']; pe.parse_data_directories(directories=[1]); crt_start, crt_end = 0x1943438, 0x1944c10
    a_slot=0x19441a0
    crt_dll=next(d for d in pe.DIRECTORY_ENTRY_IMPORT if d.dll==b'api-ms-win-crt-runtime-l1-1-0.dll')
    initterm=next(i for i in crt_dll.imports if i.name==b'_initterm')
    assert initterm.address==va(0x1947ed0) and off(s['BASE']+initterm.hint_name_table_rva)==0x194c18c
    assert va(crt_start)<=va(a_slot)<va(crt_end) and (a_slot-crt_start)%8==0
    assert next(md.disasm(raw[0x3c28a46:0x3c28a4c],va(0x3c28a46))).operands[0].imm==va(0x3c28b45)
    assert va(0x431a347)+6+struct.unpack_from('<i',raw,0x431a349)[0]==s['FLAGS']['A']-7
    outcome={
        'state':'file_W8_closed; executable_runtime_invariant_not_proven',
        'static_unconditional_value':None,'PE_zero_fill_width':4,'known_global_initializer_width':4,
        'file_width':8,'file_classes_using_selector':[1,2,3,4],
        'formula':'A != 0 && B == 0 ? 8 : 4; re-read at each use',
        'scan_scope':'Every mapped raw PE section byte position: ModRM RIP disp32 candidates, overlapping direct memory operands up to 64 bytes, FS/GS excluded; exact whole-file RVA/VA literals. Byte-position candidate census, not a proof about register-indirect stores, encoded addresses, bulk copies, or whole-program reachability.',
        'scan':scan,
        'reader_branch':body(0xe4f4d5,0xe4f509),
        'A_init':{'start':dec(0xfc5c70),'initializer_pointer':vptr(0x19441a0,0xfc5c70),
            'unwind_range_entry':ev(0x46f09cc,12),'nearby_legacy_date_default':dec(0xfc644d),
            'zero_extending_write_and_store':body(0xfc6468,0xfc6474),
            'stored_qword':'0x00000000ffffffff','A_byte_index_in_store':7,'A_value_written':0,
            'startup_crt':{'bounds':[ref(0x467c380,va(crt_start),7,1),ref(0x467c379,va(crt_end),7,1)],
                'call':rel(0x467c387,0x17581c0),'import_thunk':ref(0x17581c0,initterm.address,6,0),
                'iat_slot':check(0x1947ed0,'8c cb 94 01 00 00 00 00'),
                'import_hint_name':check(0x194c18c,'36 00 5f 69 6e 69 74 74 65 72 6d 00'),
                'lower_bound_inclusive':hex(crt_start),'upper_bound_exclusive':hex(crt_end),
                'initializer_pointer_index_zero_based':(a_slot-crt_start)//8},
            'adjacent_dword_negative_control':{'store':ref(0x431a347,0x141b6034c,6,0),
                'bytes_written':4,'last_modified_va':'0x141b6034f','reaches_A':False}},
        'B_changes':{'setter':body(0x3c28b45,0x3c28b62),'setter_range_entry':ev(0x4749598,12),
            'setter_condition_and_direct_path':body(0x3c28a39,0x3c28a4c),
            'conditional_warning_construction':body(0x3c28a7f,0x3c28aeb),
            'caller_save_token_example':rel(0x422fe12,0xf9eaa0),
            'setter_thunk':rel(0xf9eaa0,0x3c28a30),'caller_token_address':check(0x422fe0d,'48 8d 4c 24 20'),
            'first_stream_io_after_set':check(0x422fe37,'ff 50 28'),
            'conditional_clear_example':body(0x4230056,0x4230066),
            'success_restore_edge':[check(0x4230085,'80 7c 24 20 00'),check(0x423008a,'75 da'),check(0x423008c,'eb d1')],
            'caller_scope_summary':'0x422fe00 passes a stack byte for the old B, sets B=1 before stream I/O, and clears B on exit iff the old byte was zero. This is not a proven BASIC_PERSON load path.',
            'absolute_literal_caveat':'Two literal VA hits are not recognized executable store instructions by this analysis; no dataflow attribution.'},
        'writer_crosscheck':{'slot21':vptr(0x187b3d0,0xe4fe80),'class4_sources_and_writes':body(0xe4ff1d,0xe4ff5b),
            'W_select':body(0xe5001d,0xe5005a),'writer_A':ref(0xe5001d,0x141b60351,7,0),
            'W_select_caveat':'writer A != reader A; related alternate format, not proof of reader runtime flags.'},
        'pdb':{'debug_directory_entry':ev(0x194337c,28),'codeview_rsds':ev(0x46c46d8,0x3e),'name':'editor.pdb',
               'local_symbols_found':False},
        'why_file_W8':'All successful paths using the exact 20B base read match the full frame, ordinals, and repeated-ID dwords only with all reference sites taking W=8. Pdob year independently rules out W=4 for class 4. Class 5 has no W.'}
    return {'type_id':1,'entity':'pers','status':'complete_file_layout_runtime_selector_open',
            'selector_resolution':outcome,'row_offset_map':fields,
            'unclosed':[
                {'subject':'A=1 assignment and reader invocation order','reason':'No decoded direct nonzero writer or exact VA/RVA literal for A. The only decoded overlapping store sets A=0. Indirect/encoded stores and a complete startup-to-table-load chronology were not closed. The file determines W=8, not an invariant for arbitrary editor sessions.'},
                {'subject':'outside current input or arg3=0','reason':'The byte map is limited to the framed current basic_people payload; the reader can skip the 20B base suffix or choose W=4 under other flags.'},
                {'subject':'unnamed wire fields / identity semantics','reason':'obj+0x38, +0x18, +0x66 not mapped to a person schema property. Internal Pdva/Pcww/PLag and secondary ID word are not counted as pers fields; rdui is not dispatched by this BASIC_PERSON getter. Do not name the ordinal rdui.'},
                {'subject':'reference encoding and non-BASIC fields','reason':'8B physical spans and getter member provenance are fixed, but neither the meaning of each dword nor the 271-property schema in its entirety is closed.'}],
            'counts':{'fixed_person_schema_total':10,'fixed_person_business':9,'fixed_person_identity':1,
                'additional_player_schema_business':5,'fixed_all_named_distinct_codes':15,
                'mode_independent_named_fields':1,'L4':0},
            'sources':{'editor_path':str(s['EXE']),'editor_size':len(raw),'editor_sha256':editor_sha,
                'schema_snapshot':schema_rel,'schema_sha256':schema_sha,'schema_person_code_count':271},
            'static_anchors':{'type_dispatch':check(0xf49d3c,'da ef ff ff'),
                'rtti':check(0x1aac700,'2e 3f 41 56 42 41 53 49 43 5f 50 45 52 53 4f 4e 40 64 62 40 40 00'),
                'allocation':check(0x3bcd6fc,'ba 70 00 00 00'),
                'type_slot7':vptr(0x187b360,0x866e0),'type_value':check(0x866e0,'b8 01 00 00 00 c3'),
                'slot19':vptr(0x187b3c0,0xe4f370),'slot2':vptr(0x187b338,0xe502d0),
                'table_reader_loop':body(0xf2af3c,0xf2af78),
                'class_masks':[body(0xe4f3bf,0xe4f3f5),body(0xe4f42e,0xe4f432),body(0xe4f513,0xe4f522)],
                'post_body_base_call':{'dispatch':body(0xe4f47e,0xe4f4cd),
                    'chain':[rel(0xe4f4c0,0x1083b40),rel(0x1083b40,0x3dc0220)],
                    'callee':body(0x3dc0220,0x3dc0360),'writer_suffix':body(0xe4ff65,0xe4fffb),
                    'writer_duplicate_id_arm':body(0xe50275,0xe50295)},
                'object_0x38_helper':{'chain':[rel(0xe4f5a3,0xfb21a0),rel(0xfb21a0,0x3c6e100)],
                    'callee':body(0x3c6e100,0x3c6e146),'successful_reads':1,'W4_bytes':4,'W8_bytes':8,
                    'classes':[1,2,3],'note':'same RIP selectors as the reader, not 4+8. No helper invocation for class 4/5.'},
                'date_getter_year_transform':body(0xe51181,0xe5118a),
                'internal_code_links_not_counted':{k:getters[k] for k in ('Pdva','Pcww','PLag')}},
            'wire_layout_by_class':groups,'data_statistics':stats}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True); g.add_argument('--selftest',action='store_true'); g.add_argument('--write',action='store_true')
    args=p.parse_args()
    try:
        assert sys.version_info[:2]==(3,12) and sys.flags.isolated and sys.dont_write_bytecode
        s=runpy.run_path(str(HERE/'selector_scan.py')); d=runpy.run_path(str(HERE/'data_stats.py'))
        result=build(s,d['run'](),s['sweep']())
        text=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
        if args.write: OUTPUT.write_text(text,encoding='utf-8')
        else: assert json.loads(OUTPUT.read_text(encoding='utf-8'))==json.loads(text),'output.json differs from rebuilt checks'
        print('W=8 (current file); no editor-wide static invariant; person=10 (9 business+1 ID); player supplemental=5; 658011 rows; L4=0')
        return 0
    except AssertionError as e:
        print(f'Check failed: {e}'); return 1
    except Exception as e:
        print(f'Fatal: {e}'); return 2


if __name__=='__main__': raise SystemExit(main())
