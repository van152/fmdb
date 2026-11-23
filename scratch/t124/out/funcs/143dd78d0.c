__int64 __fastcall sub_143DD78D0(_QWORD *a1)
{
  __int64 result; // rax
  __int64 v3; // rsi
  __int64 *v4; // rdi
  void (__fastcall *v5)(__int64); // r14
  void (__fastcall *v6)(__int64); // r15
  __int64 v7; // rcx

  result = (unsigned int)dword_141B5FBD0;
  if ( dword_141B5FBD0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    result = sub_141750E08(&dword_141B5FBD0);
    if ( dword_141B5FBD0 == -1 )
    {
      sub_1407E53D0((unsigned int)&unk_141B5FB80, 1100122305, 5000, 80, 0, 1, 5000, 4096);
      sub_141751048(sub_140FB4420);
      result = sub_141750EA0(&dword_141B5FBD0);
    }
  }
  if ( a1 != nullptr )
  {
    result = qword_141B5FBA8;
    *a1 = qword_141B5FBA8;
    qword_141B5FBA8 = (__int64)a1;
    LODWORD(qword_141B5FBB0) = qword_141B5FBB0 + 1;
    if ( --HIDWORD(qword_141B5FBB0) == 0 && byte_141B5FBC9 != 0 )
    {
      v3 = qword_141B5FB98;
      v4 = (__int64 *)qword_141B5FB90;
      if ( qword_141B5FB90 != qword_141B5FB98 )
      {
        v5 = (void (__fastcall *)(__int64))MEMORY[0x141948960];
        v6 = (void (__fastcall *)(__int64))MEMORY[0x141948990];
        do
        {
          v7 = *v4;
          if ( (dword_141B5FB88 & 0xFFF000u) < 0x2001 )
            v6(v7);
          else
            v5(v7);
          ++v4;
        }
        while ( v4 != (__int64 *)v3 );
        result = qword_141B5FB90;
        if ( qword_141B5FB90 != qword_141B5FB98 )
          qword_141B5FB98 = qword_141B5FB90;
      }
      qword_141B5FBB0 = 0;
      qword_141B5FBA8 = 0;
    }
  }
  return result;
}
