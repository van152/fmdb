// THUNK ALIAS -> sub_143BFC6D0 (jmp:0x140e469c0->0x143bfc6d0)
__int64 __fastcall sub_143BFC6D0(_QWORD *a1)
{
  __int64 result; // rax
  __int64 v3; // rsi
  __int64 *v4; // rdi
  void (__fastcall *v5)(__int64); // r14
  void (__fastcall *v6)(__int64); // r15
  __int64 v7; // rcx

  result = (unsigned int)dword_141B5D8D0;
  if ( dword_141B5D8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    result = sub_141750E08(&dword_141B5D8D0);
    if ( dword_141B5D8D0 == -1 )
    {
      sub_1407E53D0((unsigned int)&unk_141B5D880, 1100152970, 1024, 16, 0, 0, 1024, 4096);
      sub_141751048(sub_140E469B0);
      result = sub_141750EA0(&dword_141B5D8D0);
    }
  }
  if ( a1 != nullptr )
  {
    result = qword_141B5D8A8;
    *a1 = qword_141B5D8A8;
    qword_141B5D8A8 = (__int64)a1;
    LODWORD(qword_141B5D8B0) = qword_141B5D8B0 + 1;
    if ( --HIDWORD(qword_141B5D8B0) == 0 && byte_141B5D8C9 != 0 )
    {
      v3 = qword_141B5D898;
      v4 = (__int64 *)qword_141B5D890;
      if ( qword_141B5D890 != qword_141B5D898 )
      {
        v5 = (void (__fastcall *)(__int64))MEMORY[0x141948960];
        v6 = (void (__fastcall *)(__int64))MEMORY[0x141948990];
        do
        {
          v7 = *v4;
          if ( (dword_141B5D888 & 0xFFF000u) < 0x2001 )
            v6(v7);
          else
            v5(v7);
          ++v4;
        }
        while ( v4 != (__int64 *)v3 );
        result = qword_141B5D890;
        if ( qword_141B5D890 != qword_141B5D898 )
          qword_141B5D898 = qword_141B5D890;
      }
      qword_141B5D8B0 = 0;
      qword_141B5D8A8 = 0;
    }
  }
  return result;
}
