char *__fastcall sub_144140BB0(__int64 a1, int a2)
{
  unsigned __int64 v4; // rbx
  __int64 v5; // rdi
  __int64 v6; // r14
  __int64 v7; // rax
  _DWORD *v8; // rsi
  __int64 v9; // rdi
  _DWORD *v10; // rax

  if ( dword_141B627C8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B627C8);
    if ( dword_141B627C8 == -1 )
    {
      sub_1412ECB10(&unk_141B62788);
      sub_141751048(sub_1412ECD20);
      sub_141750EA0(&dword_141B627C8);
    }
  }
  v4 = a2 + a1 - 255;
  if ( byte_141B627BC != 0
    && (qword_141B627A8 - qword_141B627A0) >> 3 > v4
    && (v5 = *(_QWORD *)(qword_141B627A0 + 8 * v4)) != 0 )
  {
    v6 = *(unsigned int *)(v5 + 120);
    v7 = MEMORY[0x1419475D0](v5 + 32);
    v8 = (_DWORD *)v7;
    if ( v7 != 0 && *(_BYTE *)(v5 + 72) != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v5 + 64));
    if ( v7 == 0 )
      v8 = (_DWORD *)sub_1412D31C0(
                       v5,
                       *(unsigned int *)(v5 + 80),
                       *(unsigned int *)(v5 + 4LL * (*(_DWORD *)(v5 + 56) != 0) + 84));
    if ( v8 != nullptr && *(_BYTE *)(v5 + 96) != 0 )
      sub_141758A10(v8, 0, *(unsigned int *)(v5 + 80));
    if ( (_DWORD)v6 != 0 )
    {
      *v8 = v4;
      return (char *)v8 + v6;
    }
  }
  else
  {
    v9 = (unsigned int)dword_141B627B8;
    v10 = (_DWORD *)sub_141601260((unsigned int)(dword_141B627B8 + v4), 4096);
    v8 = v10;
    if ( v9 != 0 )
    {
      *v10 = v4;
      return (char *)v10 + v9;
    }
  }
  return (char *)v8;
}
