__int64 __fastcall sub_143D5C1C0(__int64 a1, int *a2)
{
  __int64 *v3; // rax
  __int64 v4; // rcx
  __int64 v5; // rdi
  int v7; // ebp
  unsigned __int64 v8; // rdi
  int v9; // edi
  int v10; // esi
  __int64 v11; // rdx
  __int64 result; // rax
  int v13; // ebx
  __int64 v14; // rcx
  unsigned __int64 v15; // rdi
  int v16; // edi
  int v17; // esi
  __int64 v18; // rdx
  __int64 v19; // rbx
  unsigned int v20; // eax
  int v21; // r8d
  int v22; // ecx

  v3 = *(__int64 **)(a1 + 128);
  v4 = *v3;
  v5 = v3[1];
  if ( *v3 == v5 )
    return 0;
  v7 = *a2;
  if ( *a2 <= 0 )
    return 0;
  if ( (*(_BYTE *)(a1 + 92) & 1) != 0 )
  {
    if ( *(_BYTE *)(a1 + 160) != 0 )
    {
      sub_140054D70(
        *(_QWORD *)(a1 + 136),
        *(_QWORD *)(a1 + 144),
        (__int64)(*(_QWORD *)(a1 + 144) - *(_QWORD *)(a1 + 136)) >> 3,
        sub_1400115D0);
      *(_BYTE *)(a1 + 160) = 0;
    }
    v14 = *(_QWORD *)(a1 + 136);
    v15 = (unsigned __int64)(*(_QWORD *)(a1 + 144) - v14) >> 3;
    if ( (int)v15 > 0 )
    {
      v16 = v15 - 1;
      v17 = 0;
      do
      {
        while ( 1 )
        {
          v18 = (unsigned int)(v17 + v16) >> 1;
          result = *(_QWORD *)(v14 + 8 * v18);
          v13 = *(_DWORD *)(result + 12);
          if ( v13 <= v7 )
            break;
          v16 = v18 - 1;
          if ( v17 > (int)v18 - 1 )
            goto LABEL_20;
        }
        if ( v13 >= v7 )
          goto LABEL_24;
        v17 = v18 + 1;
      }
      while ( (int)v18 + 1 <= v16 );
    }
LABEL_20:
    v19 = 0;
    if ( a2[1] <= 0 )
      return v19;
    goto LABEL_21;
  }
  v8 = (unsigned __int64)(v5 - v4) >> 3;
  if ( (int)v8 <= 0 )
    goto LABEL_20;
  v9 = v8 - 1;
  v10 = 0;
  while ( 1 )
  {
    while ( 1 )
    {
      v11 = (unsigned int)(v10 + v9) >> 1;
      result = *(_QWORD *)(v4 + 8 * v11);
      v13 = *(_DWORD *)(result + 12);
      if ( v13 <= v7 )
        break;
      v9 = v11 - 1;
      if ( v10 > (int)v11 - 1 )
        goto LABEL_20;
    }
    if ( v13 >= v7 )
      break;
    v10 = v11 + 1;
    if ( (int)v11 + 1 > v9 )
      goto LABEL_20;
  }
LABEL_24:
  v21 = a2[1];
  v22 = *(_DWORD *)(result + 16);
  if ( v22 == 0 )
    v22 = v13;
  if ( v22 == v21 || v21 == 0 && v22 == v13 )
    return result;
  v19 = 0;
  if ( v21 == 0 )
    v19 = result;
  if ( v21 <= 0 )
    return v19;
LABEL_21:
  v20 = sub_140FFAA00(a1, (unsigned int)v7);
  if ( v20 == v7 )
    return v19;
  result = sub_140F45DB0(a1, v20);
  if ( result == 0 )
    return v19;
  return result;
}
