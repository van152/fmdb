// THUNK ALIAS -> sub_143DCC870 (jmp:0x140faf160->0x143dcc870)
__int64 __fastcall sub_143DCC870(_QWORD *a1)
{
  __int64 result; // rax
  __int64 v3; // rsi
  __int64 *v4; // rdi
  void (__fastcall *v5)(__int64); // r14
  void (__fastcall *v6)(__int64); // r15
  __int64 v7; // rcx

  result = (unsigned int)dword_141B5E968;
  if ( dword_141B5E968 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    result = sub_141750E08(&dword_141B5E968);
    if ( dword_141B5E968 == -1 )
    {
      sub_1407E53D0((unsigned int)&unk_141B5E918, 1100127567, 64, 56, 0, 0, 64, 4096);
      sub_141751048(sub_140FB3F20);
      result = sub_141750EA0(&dword_141B5E968);
    }
  }
  if ( a1 != nullptr )
  {
    result = qword_141B5E940;
    *a1 = qword_141B5E940;
    qword_141B5E940 = (__int64)a1;
    LODWORD(qword_141B5E948) = qword_141B5E948 + 1;
    if ( --HIDWORD(qword_141B5E948) == 0 && byte_141B5E961 != 0 )
    {
      v3 = qword_141B5E930;
      v4 = (__int64 *)qword_141B5E928;
      if ( qword_141B5E928 != qword_141B5E930 )
      {
        v5 = (void (__fastcall *)(__int64))MEMORY[0x141948960];
        v6 = (void (__fastcall *)(__int64))MEMORY[0x141948990];
        do
        {
          v7 = *v4;
          if ( (dword_141B5E920 & 0xFFF000u) < 0x2001 )
            v6(v7);
          else
            v5(v7);
          ++v4;
        }
        while ( v4 != (__int64 *)v3 );
        result = qword_141B5E928;
        if ( qword_141B5E928 != qword_141B5E930 )
          qword_141B5E930 = qword_141B5E928;
      }
      qword_141B5E948 = 0;
      qword_141B5E940 = 0;
    }
  }
  return result;
}
