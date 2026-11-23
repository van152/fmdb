"""Offline evidence recovery only; not imported by the reader."""
from pathlib import Path
import shutil
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
WORK = OUT / 'probe.i64'
sys.path.insert(0, r'C:\Program Files\IDA Professional 9.4\idalib\python')
import idapro
import ida_bytes
import ida_funcs
import ida_hexrays
import ida_lines
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

TARGETS = [0x1411C2780, 0x141053A80, 0x14150F650, 0x14151DCE0, 0x14151E110,
           0x1409FA4B0, 0x140839480, 0x140839290, 0x1409F8630, 0x14155BE50,
           0x14155D840, 0x14155E830, 0x140EB5F80, 0x1409FA240,
           0x141571860, 0x1415CFD70, 0x1415CFEA0, 0x141072F60,
           0x1412E6FF0, 0x140814B10, 0x143D904B0, 0x140F49530,
           0x14155CB20, 0x14155DA10, 0x14155E4D0, 0x141572E80, 0x140EB8850,
           0x14150F650, 0x141476BB0]

if __name__ == '__main__':
    shutil.copyfile(ROOT / 'scratch/t95/editor_work.i64', WORK)
    try:
        idapro.open_database(str(WORK), run_auto_analysis=False)
        md = Cs(CS_ARCH_X86, CS_MODE_64)
        ida_hexrays.init_hexrays_plugin()
        # CLUB +0x150 alternate subtype read slots.
        vtables = [0x1418B7E08]
        slots = [ida_bytes.get_qword(v + 32) for v in vtables]
        print('vtable slot +32:', [hex(v) for v in slots], flush=True)
        vas = (int(x, 16) for x in sys.argv[1:]) if len(sys.argv) > 1 else TARGETS + slots
        directory = OUT / 'static'
        directory.mkdir(exist_ok=True)
        for va in vas:
            if not 0x140000000 <= va < 0x146000000:
                continue
            real = va
            for _ in range(5):
                ins = next(md.disasm(ida_bytes.get_bytes(real, 16) or b'', real), None)
                if ins is None or ins.mnemonic != 'jmp' or not ins.op_str.startswith('0x'):
                    break
                real = int(ins.op_str, 16)
            if ida_funcs.get_func(real) is None:
                ida_funcs.add_func(real)
            try:
                c = ida_hexrays.decompile(real)
                if c:
                    (directory / f'{va:x}.c').write_text('\n'.join(ida_lines.tag_remove(x.line) for x in c.get_pseudocode()) + '\n', encoding='utf-8')
                print(f'{va:#x} -> {real:#x}: {bool(c)}', flush=True)
            except Exception as exc:
                print(f'{va:#x}: {exc}', flush=True)
    finally:
        idapro.close_database(False)
        WORK.unlink(missing_ok=True)
