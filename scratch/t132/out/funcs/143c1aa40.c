__int64 sub_143C1AA40()
{
  if ( dword_141B5DAE8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(a1: &dword_141B5DAE8);
    if ( dword_141B5DAE8 == -1 )
    {
      sub_1407E53D0(
        a1: (unsigned int)&unk_141B5DA98,
        a2: 1100140274,
        a3: 1024,
        a4: 24,
        a5: 0,
        a6: 0,
        a7: 1024,
        a8: 4096);
      sub_141751048(a1: sub_140E9BAB0);
      sub_141750EA0(a1: &dword_141B5DAE8);
    }
  }
  return sub_1407E58C0(a1: &unk_141B5DA98, a2: 24);
}
