__int64 __fastcall sub_143BA80E0(__int64 a1)
{
  if ( dword_141B5D130 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(a1: &dword_141B5D130);
    if ( dword_141B5D130 == -1 )
    {
      sub_1407E53D0(a1: (unsigned int)&unk_141B5D0E0, a2: 1100159847, a3: 1024, a4: 56, a5: 0, a6: 0, a7: 1024, a8: 0);
      sub_141751048(a1: sub_140E3FDA0);
      sub_141750EA0(a1: &dword_141B5D130);
    }
  }
  return sub_1407E58C0(a1: &unk_141B5D0E0, a2: a1);
}
