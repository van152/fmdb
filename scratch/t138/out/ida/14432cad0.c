__int64 __fastcall sub_14432CAD0(__int64 a1)
{
  *(_DWORD *)a1 = 0;
  *(_QWORD *)(a1 + 8) = 0;
  *(_QWORD *)(a1 + 16) = 0;
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
  *(_DWORD *)(a1 + 72) = 0;
  *(_QWORD *)(a1 + 64) = 0;
  *(_QWORD *)(a1 + 56) = 0;
  *(_QWORD *)(a1 + 48) = 0;
  *(_QWORD *)(a1 + 40) = 0;
  *(_QWORD *)(a1 + 32) = 0;
  *(_QWORD *)(a1 + 24) = 0;
  *(_QWORD *)(a1 + 80) = 0;
  *(_QWORD *)(a1 + 88) = 0;
  *(_QWORD *)(a1 + 96) = 0;
  *(_QWORD *)(a1 + 104) = 0;
  *(_QWORD *)(a1 + 112) = 0;
  *(_QWORD *)(a1 + 120) = 0;
  *(_QWORD *)(a1 + 128) = 0;
  *(_QWORD *)(a1 + 136) = 0;
  *(_DWORD *)(a1 + 144) = 0;
  *(_QWORD *)(a1 + 152) = 0;
  *(_QWORD *)(a1 + 160) = 0;
  *(_QWORD *)(a1 + 168) = 0;
  *(_QWORD *)(a1 + 176) = 0xFF676981FFFFFFFFuLL;
  *(_QWORD *)(a1 + 184) = 0;
  *(_QWORD *)(a1 + 192) = 0x10000076C0001LL;
  *(_BYTE *)(a1 + 200) = 0;
  return a1;
}
