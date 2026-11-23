__int64 __fastcall sub_143BA8EE0(__int64 a1)
{
  __int64 v1; // rdi

  v1 = *(_QWORD *)(a1 + 256);
  if ( v1 == 0 )
  {
    if ( dword_141B5D188 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B5D188);
      if ( dword_141B5D188 == -1 )
      {
        sub_1407E53D0(
          a1: (unsigned int)&unk_141B5D138,
          a2: 1100160064,
          a3: 1024,
          a4: 256,
          a5: 0,
          a6: 0,
          a7: 1024,
          a8: 4096);
        sub_141751048(a1: sub_140E40430);
        sub_141750EA0(a1: &dword_141B5D188);
      }
    }
    v1 = sub_1407E58C0(a1: &unk_141B5D138, a2: 256);
    sub_141758A10(a1: v1, a2: 0, a3: 256);
    sub_14145CB30(a1: v1);
    *(_DWORD *)(v1 + 248) = 124518401;
    *(_QWORD *)(a1 + 256) = v1;
  }
  return v1;
}
