// THUNK ALIAS -> sub_144320A70 (jmp:0x1414196c0->0x144320a70)
__int64 __fastcall sub_144320A70(__int64 a1)
{
  *(_QWORD *)a1 = 0x76C0001076C0001LL;
  *(_QWORD *)(a1 + 8) = 0x76C0001076C0001LL;
  *(_QWORD *)(a1 + 16) = 0x76C0001076C0001LL;
  *(_QWORD *)(a1 + 24) = 0x76C0001076C0001LL;
  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(&unk_141B59A68);
        sub_141751048(sub_1407E4B20);
        sub_141750EA0(&dword_141B59AA8);
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  *(_QWORD *)(a1 + 56) = 0;
  *(_QWORD *)(a1 + 48) = 0;
  *(_QWORD *)(a1 + 40) = 0;
  *(_QWORD *)(a1 + 32) = 0;
  *(_QWORD *)(a1 + 72) = 0;
  *(_QWORD *)(a1 + 80) = 0;
  *(_QWORD *)(a1 + 88) = 0;
  *(_QWORD *)(a1 + 96) = 0;
  *(_QWORD *)(a1 + 104) = 0;
  *(_QWORD *)(a1 + 112) = 0;
  *(_QWORD *)(a1 + 120) = 0;
  *(_QWORD *)(a1 + 128) = 0;
  *(_QWORD *)(a1 + 136) = 0;
  *(_QWORD *)(a1 + 152) = 0;
  *(_QWORD *)(a1 + 160) = 0;
  *(_QWORD *)(a1 + 168) = 0;
  *(_QWORD *)(a1 + 176) = 0;
  *(_QWORD *)(a1 + 184) = 0;
  *(_QWORD *)(a1 + 192) = 0;
  *(_QWORD *)(a1 + 200) = 0;
  *(_QWORD *)(a1 + 208) = 0;
  *(_QWORD *)(a1 + 216) = 0;
  *(_QWORD *)(a1 + 224) = 0;
  *(_QWORD *)(a1 + 232) = 0;
  *(_QWORD *)(a1 + 240) = 0;
  *(_QWORD *)(a1 + 248) = 0;
  *(_DWORD *)(a1 + 255) = 0;
  sub_141758A10(a1 + 264, 0, 168);
  *(_QWORD *)(a1 + 464) = -1;
  *(_BYTE *)(a1 + 536) = 0;
  *(_DWORD *)(a1 + 520) = 0;
  sub_1414198F0(a1, 0);
  return a1;
}
