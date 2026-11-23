__int64 __fastcall sub_143EC3830(__int64 a1)
{
  *(_QWORD *)(a1 + 21) = 0;
  *(_QWORD *)(a1 + 16) = 0;
  *(_QWORD *)(a1 + 8) = 0;
  *(_QWORD *)(a1 + 30) = 0;
  *(_QWORD *)(a1 + 38) = 0;
  *(_QWORD *)(a1 + 44) = 0;
  *(_QWORD *)(a1 + 52) = -1;
  *(_QWORD *)(a1 + 60) = 0x76C0001076C0001LL;
  *(_QWORD *)(a1 + 68) = 0x76C0001076C0001LL;
  *(_DWORD *)(a1 + 76) = 0;
  *(_WORD *)(a1 + 80) = 0;
  *(_QWORD *)(a1 + 82) = 4279500900LL;
  *(_BYTE *)(a1 + 90) = 0;
  *(_QWORD *)a1 = 0x141889138LL;
  *(_QWORD *)(a1 + 96) = 0;
  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(a1: &unk_141B59A68);
        sub_141751048(a1: sub_1407E4B20);
        sub_141750EA0(a1: &dword_141B59AA8);
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  *(_QWORD *)(a1 + 120) = 0;
  *(_QWORD *)(a1 + 112) = 0;
  *(_QWORD *)(a1 + 104) = 0;
  *(_DWORD *)(a1 + 128) = 91084;
  *(_WORD *)(a1 + 132) = 1900;
  *(_QWORD *)(a1 + 136) = -1;
  *(_QWORD *)(a1 + 141) = -1;
  *(_QWORD *)(a1 + 152) = 3;
  *(_QWORD *)(a1 + 160) = 0;
  *(_QWORD *)(a1 + 168) = -1;
  *(_QWORD *)(a1 + 176) = 0xFFFFFFFFLL;
  *(_QWORD *)(a1 + 184) = -1;
  *(_QWORD *)(a1 + 192) = -1;
  *(_DWORD *)(a1 + 200) = -1;
  *(_QWORD *)(a1 + 204) = 0x400000000LL;
  *(_WORD *)(a1 + 212) = 0;
  *(_BYTE *)(a1 + 214) = -1;
  *(_WORD *)(a1 + 219) = 0;
  *(_DWORD *)(a1 + 215) = 0;
  *(_BYTE *)(a1 + 221) = -2;
  *(_DWORD *)(a1 + 222) = 0;
  *(_WORD *)(a1 + 226) = -1;
  return a1;
}
