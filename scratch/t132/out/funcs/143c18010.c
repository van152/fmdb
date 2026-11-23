__int64 __fastcall sub_143C18010(_QWORD *a1)
{
  __int64 result; // rax
  __int64 v3; // rsi
  __int64 *v4; // rdi
  void (__fastcall *v5)(__int64); // r14
  void (__fastcall *v6)(__int64); // r15
  __int64 v7; // rcx

  result = (unsigned int)dword_141B5DAE8;
  if ( dword_141B5DAE8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    result = sub_141750E08(a1: &dword_141B5DAE8);
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
      result = sub_141750EA0(a1: &dword_141B5DAE8);
    }
  }
  if ( a1 != nullptr )
  {
    result = qword_141B5DAC0;
    *a1 = qword_141B5DAC0;
    qword_141B5DAC0 = (__int64)a1;
    LODWORD(qword_141B5DAC8) = qword_141B5DAC8 + 1;
    if ( --HIDWORD(qword_141B5DAC8) == 0 && byte_141B5DAE1 != 0 )
    {
      v3 = qword_141B5DAB0;
      v4 = (__int64 *)qword_141B5DAA8;
      if ( qword_141B5DAA8 != qword_141B5DAB0 )
      {
        v5 = (void (__fastcall *)(__int64))MEMORY[0x141948960];
        v6 = (void (__fastcall *)(__int64))MEMORY[0x141948990];
        do
        {
          v7 = *v4;
          if ( (dword_141B5DAA0 & 0xFFF000u) < 0x2001 )
            v6(a1: v7);
          else
            v5(a1: v7);
          ++v4;
        }
        while ( v4 != (__int64 *)v3 );
        result = qword_141B5DAA8;
        if ( qword_141B5DAA8 != qword_141B5DAB0 )
          qword_141B5DAB0 = qword_141B5DAA8;
      }
      qword_141B5DAC8 = 0;
      qword_141B5DAC0 = 0;
    }
  }
  return result;
}
