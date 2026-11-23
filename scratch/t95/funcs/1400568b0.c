__int64 __fastcall sub_1400568B0(__int64 a1, int a2)
{
  __int64 *v3; // rax
  __int64 v4; // rcx
  __int64 v5; // rsi
  unsigned __int64 v7; // rsi
  int v8; // esi
  int v9; // edi
  __int64 v10; // rdx
  __int64 result; // rax
  __int64 v12; // rcx
  unsigned __int64 v13; // rsi
  int v14; // esi
  int v15; // edi
  __int64 v16; // rdx

  v3 = *(__int64 **)(a1 + 128);
  v4 = *v3;
  v5 = v3[1];
  if ( *v3 == v5 )
    return 0;
  if ( (*(_BYTE *)(a1 + 92) & 1) == 0 )
  {
    v7 = (unsigned __int64)(v5 - v4) >> 3;
    if ( (int)v7 > 0 )
    {
      v8 = v7 - 1;
      v9 = 0;
      while ( 1 )
      {
        while ( 1 )
        {
          v10 = (unsigned int)(v9 + v8) >> 1;
          result = *(_QWORD *)(v4 + 8 * v10);
          if ( *(_DWORD *)(result + 12) <= a2 )
            break;
          v8 = v10 - 1;
          if ( v9 > (int)v10 - 1 )
            return 0;
        }
        if ( *(_DWORD *)(result + 12) >= a2 )
          break;
        v9 = v10 + 1;
        if ( (int)v10 + 1 > v8 )
          return 0;
      }
      return result;
    }
    return 0;
  }
  if ( *(_BYTE *)(a1 + 160) != 0 )
  {
    sub_140054D70(
      *(_QWORD *)(a1 + 136),
      *(_QWORD *)(a1 + 144),
      (__int64)(*(_QWORD *)(a1 + 144) - *(_QWORD *)(a1 + 136)) >> 3,
      sub_1400115D0);
    *(_BYTE *)(a1 + 160) = 0;
  }
  v12 = *(_QWORD *)(a1 + 136);
  v13 = (unsigned __int64)(*(_QWORD *)(a1 + 144) - v12) >> 3;
  if ( (int)v13 <= 0 )
    return 0;
  v14 = v13 - 1;
  v15 = 0;
  while ( 1 )
  {
    while ( 1 )
    {
      v16 = (unsigned int)(v15 + v14) >> 1;
      result = *(_QWORD *)(v12 + 8 * v16);
      if ( *(_DWORD *)(result + 12) <= a2 )
        break;
      v14 = v16 - 1;
      if ( v15 > (int)v16 - 1 )
        return 0;
    }
    if ( *(_DWORD *)(result + 12) >= a2 )
      break;
    v15 = v16 + 1;
    if ( (int)v16 + 1 > v14 )
      return 0;
  }
  return result;
}
