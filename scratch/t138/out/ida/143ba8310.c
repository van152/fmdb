__int64 *__fastcall sub_143BA8310(__int64 *a1)
{
  __int64 v2; // rdi

  if ( dword_141B5D608 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(a1: &dword_141B5D608);
    if ( dword_141B5D608 == -1 )
    {
      sub_1407E53D0(
        a1: (unsigned int)&unk_141B5D5B8,
        a2: 1100159870,
        a3: 2048,
        a4: 168,
        a5: 0,
        a6: 0,
        a7: 1024,
        a8: 4096);
      sub_141751048(a1: sub_140E40B30);
      sub_141750EA0(a1: &dword_141B5D608);
    }
  }
  v2 = sub_1407E58C0(a1: &unk_141B5D5B8, a2: 168);
  *(_QWORD *)(v2 + 8) = -1;
  *(_QWORD *)(v2 + 16) = 0x76C0001076C0001LL;
  *(_DWORD *)(v2 + 24) = 124518401;
  *(_BYTE *)(v2 + 28) = 0;
  *(_QWORD *)v2 = 0x14187B0D8LL;
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
  *(_QWORD *)(v2 + 80) = 0;
  *(_QWORD *)(v2 + 72) = 0;
  *(_QWORD *)(v2 + 64) = 0;
  *(_QWORD *)(v2 + 56) = 0;
  *(_QWORD *)(v2 + 48) = 0;
  *(_QWORD *)(v2 + 40) = 0;
  *(_QWORD *)(v2 + 32) = 0;
  *(_QWORD *)(v2 + 88) = 0x76C0001076C0001LL;
  *(_QWORD *)(v2 + 96) = 0;
  *(_QWORD *)(v2 + 120) = 0x76C0001076C0001LL;
  *(_QWORD *)(v2 + 128) = 0;
  *(_DWORD *)(v2 + 136) = 0;
  *(_QWORD *)(v2 + 140) = 0x76C0001076C0001LL;
  *(_DWORD *)(v2 + 148) = 124518401;
  *(_BYTE *)(v2 + 167) = 0;
  *(_DWORD *)(v2 + 160) = 0;
  *(_BYTE *)(v2 + 164) = 0;
  *(_WORD *)(v2 + 165) = 10;
  *(_QWORD *)(v2 + 112) = 0;
  *(_QWORD *)(v2 + 152) = -4170448895LL;
  *(_QWORD *)(v2 + 104) = 0;
  *a1 = v2;
  return a1;
}
