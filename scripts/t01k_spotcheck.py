"""Commander's independent spot-check of t01k claims (static + payload sample).
Run from fm24-db root: py -V:3.12 -I scripts/t01k_spotcheck.py
"""
from __future__ import annotations
import importlib.util
import struct
import sys

ED = r"D:\tmp2b\fm24\input\editor.exe"
fails = 0
data = open(ED, "rb").read()

def expect(label, off, hexstr):
    global fails
    e = bytes.fromhex(hexstr.replace(" ", ""))
    got = data[off:off + len(e)]
    good = got == e
    fails += not good
    print(f"{'PASS' if good else 'FAIL':4} {label:52} @{off:#x}: {got.hex()}" + ("" if good else f" exp={e.hex()}"))

# reader entry + control flow claims
expect("slot19 ptr -> 0x140e4fd70 @0x187b3c0", 0x187b3c0, "70 fd e4 40 01 00 00 00")
expect("slot2 getter ptr -> 0x140e502d0 @0x187b338", 0x187b338, "d0 0c e5 40 01 00 00 00")
expect("reader prologue @0xe4f370", 0xe4f370, "41 57 41 56 56 57 55 53 48 83 ec 48")
expect("dest object+0x65 @0xe4f38b", 0xe4f38b, "48 8d 71 65")
expect("first width 1 @0xe4f393", 0xe4f393, "41 b8 01 00 00 00")
expect("mask1 mov edx,0x90020 @0xe4f3c8", 0xe4f3c8, "ba 20 00 09 00")
expect("bt @0xe4f3cd", 0xe4f3cd, "0f a3 ca")
expect("jae @0xe4f3d0", 0xe4f3d0, "0f 83 ff 00 00 00")
expect("mask2 mov edx,0xd0170 @0xe4f3e7", 0xe4f3e7, "ba 70 01 0d 00")
expect("class4 cmp al,4 @0xe4f42e", 0xe4f42e, "3c 04")
expect("jne @0xe4f430", 0xe4f430, "75 4c")
expect("dest object+0x52 @0xe4f432", 0xe4f432, "48 8d 53 52")
expect("width 2 @0xe4f43c", 0xe4f43c, "41 b8 02 00 00 00")
expect("dest object+0x5a @0xe4f452", 0xe4f452, "48 8d 53 5a")
expect("width 2 @0xe4f468", 0xe4f468, "41 b8 02 00 00 00")
expect("selector1 @0xe4f4d5", 0xe4f4d5, "80 3d 77 04 d1 00 00")
expect("selector2 @0xe4f4ed", 0xe4f4ed, "80 3d 38 fd d0 00 00")
expect("dest object+0x30 @0xe4f4dc", 0xe4f4dc, "48 8d 53 30")
expect("width 8 arm @0xe4f4f6", 0xe4f4f6, "41 b8 08 00 00 00")
expect("width 4 arm @0xe4f4fe", 0xe4f4fe, "41 b8 04 00 00 00")
expect("branch je @0xe4f4eb", 0xe4f4eb, "74 11")
expect("branch jne @0xe4f4f4", 0xe4f4f4, "75 08")
expect("helper call @0xe4f5a3", 0xe4f5a3, "e8 f8 2b 16 00")
# getter chains: cmp edx,<4CC reversed> pattern
expect("Ptyp getter cmp edx,'Ptyp' @0xe50959", 0xe50959, "81 fa 70 79 74 50")
expect("Ptyp getter movsx byte [rdi+0x65] @0xe50965", 0xe50965, "0f be 7f 65")
expect("Pdob getter cmp edx,'Pdob' @0xe506a5", 0xe506a5, "81 fa 62 6f 64 50")
expect("Pdob getter movzx word [rdi+0x5a] @0xe51158", 0xe51158, "0f b7 7f 5a")

# payload sample: class-4 row @0x13b29
spec = importlib.util.spec_from_file_location("o", r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py")
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
zmod = old._zstd_module()
raw_file = open(r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm\basic_people_db.dat", "rb").read()
payload = old._stream_decompress(raw_file[8:], 256 * 1024 * 1024)
sample = payload[0x13b29:0x13b37].hex()
good = sample == "1104af0000002103000064006c07"
fails += not good
print(f"{'PASS' if good else 'FAIL':4} class-4 sample row @payload 0x13b29: {sample}")
# Ptyp (object+0x65) sourced from row+1: sample row+1 = 04 == class byte
good = payload[0x13b29 + 1] == 4
fails += not good
print(f"{'PASS' if good else 'FAIL':4} Ptyp@row+1 == 4 (class byte doubles as Ptyp value)")

print(f"\n{'ALL PASS' if fails == 0 else f'{fails} FAILURES'}")
sys.exit(1 if fails else 0)
