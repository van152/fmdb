_QWORD *__fastcall sub_141533DD0(_QWORD *a1, __int64 a2, unsigned __int8 a3)
{
  unsigned __int64 v6; // rax
  __int64 v7; // rcx
  __int64 v9; // rcx
  __int64 v10; // rcx

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
  a1[2] = 0;
  a1[1] = 0;
  *a1 = 0;
  v6 = (a3 & 0xFEu) - 2;
  if ( (unsigned int)v6 <= 0x3E && (v7 = 0x4000000101100001LL, _bittest64(&v7, v6)) )
  {
    if ( *(_QWORD *)(a2 + 48) != 0 )
      sub_141533F50(a1);
  }
  else if ( a3 <= 0x33u && (v9 = 0xC000000003000LL, _bittest64(&v9, a3))
         || (a3 & 0xF6) == 0x26
         || a3 <= 0x31u && (v10 = 0x3030000000000LL, _bittest64(&v10, a3)) )
  {
    if ( *(_QWORD *)(a2 + 48) != 0 )
      sub_1415344F0(a1);
  }
  else if ( (a3 & 1) != 0 )
  {
    sub_141534910(a1, a2);
  }
  return a1;
}
