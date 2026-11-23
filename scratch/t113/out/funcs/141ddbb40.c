__int64 sub_141DDBB40()
{
  __int64 v0; // rsi

  v0 = qword_141ABF0A8;
  if ( qword_141ABF0A8 == 0 )
  {
    if ( dword_141ABF0A4 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141ABF0A4);
      if ( dword_141ABF0A4 == -1 )
      {
        sub_1400DAD40(&unk_141ABF0A2);
        sub_141751048(sub_1400DAD90);
        sub_141750EA0(&dword_141ABF0A4);
      }
    }
    v0 = qword_141ABF0A8;
    if ( qword_141ABF0A8 == 0 )
    {
      byte_141ABF0B0 = 1;
      v0 = sub_141750CC0(672);
      sub_141200420(v0);
      qword_141ABF0A8 = v0;
      byte_141ABF0B0 = 0;
    }
  }
  return v0;
}
