__int64 __fastcall sub_143B58760(_QWORD *a1)
{
  __int64 result; // rax
  __int64 v3; // rsi
  __int64 *v4; // rdi
  void (__fastcall *v5)(__int64); // r14
  void (__fastcall *v6)(__int64); // r15
  __int64 v7; // rcx

  result = (unsigned int)dword_141B5CAB8;
  if ( dword_141B5CAB8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    result = sub_141750E08(&dword_141B5CAB8);
    if ( dword_141B5CAB8 == -1 )
    {
      sub_1407E53D0((unsigned int)&unk_141B5CA68, 1100123354, 256, 24, 0, 0, 256, 4096);
      sub_141751048(sub_140DD51A0);
      result = sub_141750EA0(&dword_141B5CAB8);
    }
  }
  if ( a1 != nullptr )
  {
    result = qword_141B5CA90;
    *a1 = qword_141B5CA90;
    qword_141B5CA90 = (__int64)a1;
    LODWORD(qword_141B5CA98) = qword_141B5CA98 + 1;
    if ( --HIDWORD(qword_141B5CA98) == 0 && byte_141B5CAB1 != 0 )
    {
      v3 = qword_141B5CA80;
      v4 = (__int64 *)qword_141B5CA78;
      if ( qword_141B5CA78 != qword_141B5CA80 )
      {
        v5 = (void (__fastcall *)(__int64))MEMORY[0x141948960];
        v6 = (void (__fastcall *)(__int64))MEMORY[0x141948990];
        do
        {
          v7 = *v4;
          if ( (dword_141B5CA70 & 0xFFF000u) < 0x2001 )
            v6(v7);
          else
            v5(v7);
          ++v4;
        }
        while ( v4 != (__int64 *)v3 );
        result = qword_141B5CA78;
        if ( qword_141B5CA78 != qword_141B5CA80 )
          qword_141B5CA80 = qword_141B5CA78;
      }
      qword_141B5CA98 = 0;
      qword_141B5CA90 = 0;
    }
  }
  return result;
}
