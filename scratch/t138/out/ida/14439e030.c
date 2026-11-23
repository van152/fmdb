__int64 sub_14439E030()
{
  if ( dword_141B5D558 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(a1: &dword_141B5D558);
    if ( dword_141B5D558 == -1 )
    {
      sub_1407E53D0(a1: (unsigned int)&unk_141B5D508, a2: 1100160168, a3: 256, a4: 64, a5: 0, a6: 0, a7: 256, a8: 4096);
      sub_141751048(a1: sub_140E42150);
      sub_141750EA0(a1: &dword_141B5D558);
    }
  }
  return sub_1407E58C0(a1: &unk_141B5D508, a2: 64);
}
