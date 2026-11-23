// THUNK ALIAS -> sub_143C410D0 (jmp:0x140e6cc80->0x143c410d0)
char __fastcall sub_143C410D0(__int64 a1)
{
  __int64 *v1; // rax
  __int64 v2; // r10
  unsigned __int64 v3; // rax
  unsigned __int16 v4; // r8
  __int64 v5; // rdx
  __int64 v6; // rcx
  int v7; // r11d
  char result; // al
  __int64 v9; // rsi
  unsigned int v10; // edi
  unsigned __int16 v11; // di

  v1 = *(__int64 **)(a1 + 304);
  if ( v1 == nullptr )
    return 0;
  v2 = *v1;
  v3 = (unsigned __int64)(v1[1] - *v1) >> 3;
  if ( (int)v3 <= 0 )
    return 0;
  v4 = dword_141AAE084 & 0x1FF;
  v5 = (unsigned int)v3;
  v6 = 0;
  v7 = 784;
  result = 0;
  do
  {
    v9 = *(_QWORD *)(v2 + 8 * v6);
    v10 = *(unsigned __int8 *)(v9 + 18);
    if ( v10 <= 9 )
    {
      if ( _bittest(&v7, v10) )
      {
        v11 = *(_WORD *)(v9 + 6);
        if ( v11 >= HIWORD(dword_141AAE084)
          && (v11 > HIWORD(dword_141AAE084) || (unsigned __int16)(*(_WORD *)(v9 + 4) & 0x1FF) >= v4)
          && *(_WORD *)(v9 + 2) <= HIWORD(dword_141AAE084)
          && (*(_WORD *)(v9 + 2) < HIWORD(dword_141AAE084) || (unsigned __int16)(*(_WORD *)v9 & 0x1FF) <= v4) )
        {
          ++result;
        }
      }
    }
    ++v6;
  }
  while ( v5 != v6 );
  return result;
}
