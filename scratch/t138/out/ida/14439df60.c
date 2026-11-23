__int64 sub_14439DF60()
{
  if ( dword_141B5D500 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(a1: &dword_141B5D500);
    if ( dword_141B5D500 == -1 )
    {
      sub_1407E53D0(a1: (unsigned int)&unk_141B5D4B0, a2: 1100160087, a3: 1024, a4: 44, a5: 0, a6: 0, a7: 1024, a8: 0);
      sub_141751048(a1: sub_140E41FD0);
      sub_141750EA0(a1: &dword_141B5D500);
    }
  }
  return sub_1407E58C0(a1: &unk_141B5D4B0, a2: 44);
}
