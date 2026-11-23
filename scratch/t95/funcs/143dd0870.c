__int64 __fastcall sub_143DD0870(_QWORD *a1)
{
  __int64 result; // rax
  __int64 v3; // rsi
  __int64 *v4; // rdi
  void (__fastcall *v5)(__int64); // r14
  void (__fastcall *v6)(__int64); // r15
  __int64 v7; // rcx

  result = (unsigned int)dword_141B5FA18;
  if ( dword_141B5FA18 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    result = sub_141750E08(&dword_141B5FA18);
    if ( dword_141B5FA18 == -1 )
    {
      sub_1407E53D0((unsigned int)&unk_141B5F9C8, 1100134596, 500, 136, 0, 1, 500, 4096);
      sub_141751048(sub_140FB4680);
      result = sub_141750EA0(&dword_141B5FA18);
    }
  }
  if ( a1 != nullptr )
  {
    result = qword_141B5F9F0;
    *a1 = qword_141B5F9F0;
    qword_141B5F9F0 = (__int64)a1;
    LODWORD(qword_141B5F9F8) = qword_141B5F9F8 + 1;
    if ( --HIDWORD(qword_141B5F9F8) == 0 && byte_141B5FA11 != 0 )
    {
      v3 = qword_141B5F9E0;
      v4 = (__int64 *)qword_141B5F9D8;
      if ( qword_141B5F9D8 != qword_141B5F9E0 )
      {
        v5 = (void (__fastcall *)(__int64))MEMORY[0x141948960];
        v6 = (void (__fastcall *)(__int64))MEMORY[0x141948990];
        do
        {
          v7 = *v4;
          if ( (dword_141B5F9D0 & 0xFFF000u) < 0x2001 )
            v6(v7);
          else
            v5(v7);
          ++v4;
        }
        while ( v4 != (__int64 *)v3 );
        result = qword_141B5F9D8;
        if ( qword_141B5F9D8 != qword_141B5F9E0 )
          qword_141B5F9E0 = qword_141B5F9D8;
      }
      qword_141B5F9F8 = 0;
      qword_141B5F9F0 = 0;
    }
  }
  return result;
}
