__int64 __fastcall sub_143C56700(__int64 a1, __int64 a2, unsigned int a3, __int64 a4)
{
  *(_QWORD *)a1 = a2;
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
  *(_QWORD *)(a1 + 24) = 0;
  *(_QWORD *)(a1 + 16) = 0;
  *(_QWORD *)(a1 + 8) = 0;
  *(_BYTE *)(a1 + 32) = a3;
  *(_DWORD *)(a1 + 36) = 3;
  LOBYTE(a4) = 1;
  sub_1411E9300(a1: a2, a2: a3, a3: a1 + 8, a4, a5: 0);
  *(_BYTE *)(a1 + 40) = a3;
  return a1;
}
