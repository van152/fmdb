__int64 __fastcall sub_141535610(__int64 a1, __int64 a2, unsigned __int8 a3)
{
  __int64 v6; // rcx
  unsigned __int64 v7; // rax
  __int64 v8; // rdx
  __int64 v10; // rdx
  __int64 v11; // rdx

  *(_QWORD *)a1 = a2;
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
  v6 = a1 + 8;
  *(_QWORD *)(a1 + 24) = 0;
  *(_QWORD *)(a1 + 16) = 0;
  *(_QWORD *)(a1 + 8) = 0;
  v7 = (a3 & 0xFEu) - 2;
  if ( (unsigned int)v7 <= 0x3E && (v8 = 0x4000000101100001LL, _bittest64(&v8, v7)) )
  {
    if ( *(_QWORD *)(a2 + 48) != 0 )
      sub_141533F50(v6);
  }
  else if ( a3 <= 0x33u && (v10 = 0xC000000003000LL, _bittest64(&v10, a3))
         || (a3 & 0xF6) == 0x26
         || a3 <= 0x31u && (v11 = 0x3030000000000LL, _bittest64(&v11, a3)) )
  {
    if ( *(_QWORD *)(a2 + 48) != 0 )
      sub_1415344F0(v6);
  }
  else if ( (a3 & 1) != 0 )
  {
    sub_141534910(v6, a2);
  }
  *(_BYTE *)(a1 + 32) = a3;
  return a1;
}
