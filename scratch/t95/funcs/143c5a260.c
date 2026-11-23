__int64 __fastcall sub_143C5A260(__int64 a1, __int64 a2, unsigned int a3, __int64 a4)
{
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
  *(_QWORD *)(a1 + 16) = 0;
  *(_QWORD *)(a1 + 8) = 0;
  *(_QWORD *)a1 = 0;
  *(_BYTE *)(a1 + 24) = a3;
  *(_DWORD *)(a1 + 28) = 3;
  LOBYTE(a4) = 1;
  sub_1411E9300(a2, a3, a1, a4, 0);
  return a1;
}
