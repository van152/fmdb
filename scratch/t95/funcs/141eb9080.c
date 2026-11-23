_OWORD *sub_141EB9080()
{
  _OWORD *v0; // rsi

  v0 = (_OWORD *)qword_141ABFFE0;
  if ( qword_141ABFFE0 == 0 )
  {
    if ( dword_141ABFFD8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141ABFFD8);
      if ( dword_141ABFFD8 == -1 )
      {
        sub_14011C7F0(&unk_141ABFFD4);
        sub_141751048(sub_14011C860);
        sub_141750EA0(&dword_141ABFFD8);
      }
    }
    v0 = (_OWORD *)qword_141ABFFE0;
    if ( qword_141ABFFE0 == 0 )
    {
      byte_141ABFFE8 = 1;
      v0 = (_OWORD *)sub_141750CC0(48);
      *v0 = 0;
      v0[1] = 0;
      v0[2] = 0;
      sub_14080D3A0((char *)v0 + 8, 0);
      *(_QWORD *)v0 = 0x14176D168LL;
      qword_141ABFFE0 = (__int64)v0;
      byte_141ABFFE8 = 0;
    }
  }
  return v0;
}
