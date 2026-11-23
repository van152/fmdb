__int64 __fastcall sub_143B5FEF0(__int64 a1)
{
  if ( dword_141B5CAB8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B5CAB8);
    if ( dword_141B5CAB8 == -1 )
    {
      sub_1407E53D0((unsigned int)&unk_141B5CA68, 1100123354, 256, 24, 0, 0, 256, 4096);
      sub_141751048(sub_140DD51A0);
      sub_141750EA0(&dword_141B5CAB8);
    }
  }
  return sub_1407E58C0(&unk_141B5CA68, a1);
}
