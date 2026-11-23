char *__fastcall sub_143671D70(__int64 a1, unsigned __int64 a2)
{
  int v2; // esi
  __int64 v3; // rax
  __int64 v4; // rbx
  __int64 v5; // r14
  __int64 v6; // rax
  _DWORD *v7; // rdi
  __int64 v8; // rbx
  _DWORD *v9; // rax

  v2 = a2;
  if ( *(_BYTE *)(a1 + 52) != 0
    && (v3 = *(_QWORD *)(a1 + 24), (*(_QWORD *)(a1 + 32) - v3) >> 3 > a2)
    && (v4 = *(_QWORD *)(v3 + 8 * a2)) != 0 )
  {
    v5 = *(unsigned int *)(v4 + 120);
    v6 = MEMORY[0x1419475D0](a1: v4 + 32);
    v7 = (_DWORD *)v6;
    if ( v6 != 0 && *(_BYTE *)(v4 + 72) != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v4 + 64));
    if ( v6 == 0 )
      v7 = (_DWORD *)sub_1412D31C0(
                       a1: v4,
                       a2: *(unsigned int *)(v4 + 80),
                       a3: *(unsigned int *)(v4 + 4LL * (*(_DWORD *)(v4 + 56) != 0) + 84));
    if ( v7 != nullptr && *(_BYTE *)(v4 + 96) != 0 )
      sub_141758A10(a1: v7, a2: 0, a3: *(unsigned int *)(v4 + 80));
    if ( v5 != 0 )
    {
      *v7 = v2;
      return (char *)v7 + v5;
    }
  }
  else
  {
    v8 = *(unsigned int *)(a1 + 48);
    v9 = (_DWORD *)sub_141601260(a1: (unsigned int)(v8 + a2), a2: 4096);
    v7 = v9;
    if ( v8 != 0 )
    {
      *v9 = v2;
      return (char *)v9 + v8;
    }
  }
  return (char *)v7;
}
