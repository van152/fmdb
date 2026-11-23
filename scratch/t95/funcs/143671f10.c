void *sub_143671F10()
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
  return &unk_141B59A68;
}
