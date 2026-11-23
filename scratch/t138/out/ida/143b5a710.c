_QWORD *__fastcall sub_143B5A710(__int64 a1)
{
  _QWORD *v1; // rdi

  v1 = *(_QWORD **)(a1 + 176);
  if ( v1 == nullptr )
  {
    if ( dword_141B5CAB8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B5CAB8);
      if ( dword_141B5CAB8 == -1 )
      {
        sub_1407E53D0(
          a1: (unsigned int)&unk_141B5CA68,
          a2: 1100123354,
          a3: 256,
          a4: 24,
          a5: 0,
          a6: 0,
          a7: 256,
          a8: 4096);
        sub_141751048(a1: sub_140DD51A0);
        sub_141750EA0(a1: &dword_141B5CAB8);
      }
    }
    v1 = (_QWORD *)sub_1407E58C0(a1: &unk_141B5CA68, a2: 24);
    if ( qword_141ABD470 == 0 )
    {
      if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B59AA8);
        if ( dword_141B59AA8 == -1 )
        {
          sub_1407E3E70(a1: &unk_141B59A68);
          sub_141751048(a1: sub_1407E4B20);
          sub_141750EA0(a1: &dword_141B59AA8);
        }
      }
      qword_141ABD470 = (__int64)&unk_141B59A68;
    }
    v1[2] = 0;
    v1[1] = 0;
    *v1 = 0;
    *(_QWORD *)(a1 + 176) = v1;
  }
  return v1;
}
