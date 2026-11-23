__int64 sub_143B5B340()
{
  if ( dword_141B5C9B0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(a1: &dword_141B5C9B0);
    if ( dword_141B5C9B0 == -1 )
    {
      sub_1407E53D0(a1: (unsigned int)&unk_141B5C960, a2: 1100123118, a3: 64, a4: 24, a5: 0, a6: 0, a7: 64, a8: 4096);
      sub_141751048(a1: sub_140DD51C0);
      sub_141750EA0(a1: &dword_141B5C9B0);
    }
  }
  return sub_1407E58C0(a1: &unk_141B5C960, a2: 24);
}
