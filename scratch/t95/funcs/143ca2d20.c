__int64 sub_143CA2D20()
{
  __int64 v0; // rax
  __int64 v1; // rsi

  if ( dword_141ABD750 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141ABD750);
    if ( dword_141ABD750 == -1 )
    {
      sub_1407E4EA0((unsigned int)&unk_141ABD6E0, 1100151682, 0x4000, 16, 0, 0, 4096, 4096);
      sub_141751048(sub_140003AA0);
      sub_141750EA0(&dword_141ABD750);
    }
  }
  v0 = MEMORY[0x1419475D0](&unk_141ABD700);
  v1 = v0;
  if ( v0 != 0 && byte_141ABD728 != 0 )
    _InterlockedIncrement(&dword_141ABD720);
  if ( v0 == 0 )
    v1 = sub_1412D31C0(
           &unk_141ABD6E0,
           (unsigned int)dword_141ABD730,
           *((unsigned int *)&unk_141ABD6E0 + (dword_141ABD718 != 0) + 21));
  if ( v1 != 0 && byte_141ABD740 != 0 )
    sub_141758A10(v1, 0, (unsigned int)dword_141ABD730);
  return v1;
}
