__int64 sub_140036ED0()
{
  __int64 v0; // rsi

  v0 = qword_141ABE010;
  if ( qword_141ABE010 == 0 )
  {
    if ( dword_141ABE00C > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141ABE00C);
      if ( dword_141ABE00C == -1 )
      {
        sub_1400569D0(&unk_141ABE008);
        sub_141751048(sub_140056A20);
        sub_141750EA0(&dword_141ABE00C);
      }
    }
    v0 = qword_141ABE010;
    if ( qword_141ABE010 == 0 )
    {
      byte_141ABE018 = 1;
      v0 = sub_141750CC0(208);
      sub_140FEC270(v0);
      qword_141ABE010 = v0;
      byte_141ABE018 = 0;
    }
  }
  return v0;
}
