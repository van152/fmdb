_QWORD *sub_140E78A80()
{
  _QWORD *v0; // rsi
  __int64 v2; // rcx

  v0 = (_QWORD *)qword_141ABE010;
  if ( qword_141ABE010 == 0 )
  {
    if ( dword_141ABE00C > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141ABE00C);
      if ( dword_141ABE00C == -1 )
      {
        sub_140EA4BF0(v2);
        sub_141751048(sub_140EA4D00);
        sub_141750EA0(&dword_141ABE00C);
      }
    }
    v0 = (_QWORD *)qword_141ABE010;
    if ( qword_141ABE010 == 0 )
    {
      byte_141ABE018 = 1;
      v0 = (_QWORD *)sub_141750CC0(208);
      *v0 = 0x141886CB8LL;
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
      sub_141758A10(v0 + 1, 0, 193);
      qword_141ABE010 = (__int64)v0;
      byte_141ABE018 = 0;
    }
  }
  return v0;
}
