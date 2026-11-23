char __fastcall sub_143EF3BF0(__int64 a1, __int64 a2, _QWORD *a3, char a4, unsigned __int8 a5)
{
  __int64 v8; // rax
  __int64 v9; // rax
  __int64 v10; // rbp
  __int64 i; // rbp
  __int64 j; // rbp
  __int64 k; // rbp
  __int64 m; // rbp
  __int64 v15; // rax
  unsigned __int64 v16; // rbp
  __int64 *v17; // rax
  __int64 v18; // rbp
  __int64 v19; // r15

  if ( (unsigned __int8)sub_140F7EC80((_DWORD)a3, (int)a1 + 368, a3[5], a5, 1, 0) != 0 )
  {
    v8 = *(_QWORD *)(a1 + 368);
    if ( v8 != 0 )
      *(_QWORD *)(v8 + 8LL * *(unsigned __int8 *)(a1 + 185) + 264) = a1;
  }
  if ( (a5 & 1) == 0 )
  {
    if ( *(_DWORD *)(a1 + 360) == -2 )
    {
      if ( *(_DWORD *)(a1 + 12) == -2000000002
        || (v9 = sub_140F45DB0(qword_141B5FDB8)) == 0
        || (v10 = v9, (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v9 + 352LL))(v9) == 0) )
      {
        v10 = 0;
      }
      *(_QWORD *)(a1 + 360) = v10;
    }
    else
    {
      sub_140F7EE40((_DWORD)a3, a1 + 360, a3[2], a5, 1, 0);
    }
  }
  for ( i = *(_QWORD *)(a1 + 192); i != *(_QWORD *)(a1 + 200); i += 32 )
  {
    sub_140F7EC80((_DWORD)a3, i, a3[5], a5, 1, 0);
    sub_140F7F730(a3, i + 8, a5);
    sub_140F7EC80((_DWORD)a3, i + 16, a3[3], a5, 1, 0);
  }
  for ( j = *(_QWORD *)(a1 + 240); j != *(_QWORD *)(a1 + 248); j += 16 )
    sub_140F7F930(a3, j + 8, a5);
  for ( k = *(_QWORD *)(a1 + 288); k != *(_QWORD *)(a1 + 296); k += 16 )
    sub_140F7FC40(a3, k + 8, a5);
  for ( m = *(_QWORD *)(a1 + 264); m != *(_QWORD *)(a1 + 272); m += 16 )
    sub_140F7F220(a3, m + 8, a5);
  if ( a4 != 0 )
  {
    v15 = *(_QWORD *)(a1 + 1760);
    if ( *(_QWORD *)(a1 + 1768) != v15 )
    {
      v16 = 0;
      do
      {
        sub_140F80250(a3, *(_QWORD *)(v15 + 8 * v16++), a5, 0);
        v15 = *(_QWORD *)(a1 + 1760);
      }
      while ( v16 < (*(_QWORD *)(a1 + 1768) - v15) >> 3 );
    }
    v17 = *(__int64 **)(a1 + 1272);
    if ( v17 != nullptr )
    {
      v18 = *v17;
      v19 = v17[1];
      if ( *v17 != v19 )
      {
        do
        {
          sub_140F7EC80((_DWORD)a3, v18, a3[3], a5, 1, 0);
          v18 += 16;
        }
        while ( v18 != v19 );
      }
    }
  }
  sub_1411D2F80(a1, 0, (__int64)a3, a4, a5);
  return 1;
}
