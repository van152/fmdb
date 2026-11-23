__int64 __fastcall sub_143B943A0(__int64 a1)
{
  __int64 v1; // rdi

  v1 = *(_QWORD *)(a1 - 32);
  if ( v1 == 0 )
  {
    if ( dword_141B5CD80 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B5CD80);
      if ( dword_141B5CD80 == -1 )
      {
        sub_1407E53D0(
          a1: (unsigned int)&unk_141B5CD30,
          a2: 1100131616,
          a3: 4096,
          a4: 80,
          a5: 0,
          a6: 0,
          a7: 1024,
          a8: 4096);
        sub_141751048(a1: sub_140DF2D20);
        sub_141750EA0(a1: &dword_141B5CD80);
      }
    }
    v1 = sub_1407E58C0(a1: &unk_141B5CD30, a2: 80);
    sub_1413FFFE0(a1: v1);
    *(_QWORD *)(a1 - 32) = v1;
  }
  return v1;
}
