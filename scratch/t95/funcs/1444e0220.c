char __fastcall sub_1444E0220(_QWORD *a1, __int64 a2, _QWORD *a3, __int64 a4, unsigned __int8 a5)
{
  __int64 v7; // rdx
  __int64 v8; // rbx
  unsigned __int64 v9; // rbp
  __int64 v10; // rdx
  __int64 v11; // rbx
  unsigned __int64 v12; // rbp
  __int64 v13; // rdx
  __int64 v14; // rbx
  unsigned __int64 v15; // rbp
  __int64 v16; // rdx
  __int64 v17; // rbx
  unsigned __int64 v18; // rbp
  __int64 *v19; // rbp
  __int64 *i; // r15
  __int64 v21; // rbx
  __int64 *v22; // rbp
  __int64 *j; // r15
  __int64 v24; // rbx
  _DWORD *v25; // rbx
  _DWORD *k; // rbp
  _DWORD *v27; // rbx
  _DWORD *m; // rdi
  _QWORD v30[7]; // [rsp+30h] [rbp-38h] BYREF

  v30[0] = a1[3];
  if ( (unsigned __int8)sub_140F7EE40((_DWORD)a3, (unsigned int)v30, a3[19], a5, 1, 0) != 0 )
    a1[3] = v30[0];
  v30[0] = a1[4];
  if ( (unsigned __int8)sub_140F7EE40((_DWORD)a3, (unsigned int)v30, a3[19], a5, 1, 0) != 0 )
    a1[4] = v30[0];
  v7 = a1[6];
  if ( a1[7] != v7 )
  {
    v8 = 0;
    v9 = 0;
    do
    {
      sub_140F80250(a3, v8 + v7, a5, 0);
      ++v9;
      v7 = a1[6];
      v8 += 8;
    }
    while ( v9 < (a1[7] - v7) >> 3 );
  }
  v10 = a1[12];
  if ( a1[13] != v10 )
  {
    v11 = 0;
    v12 = 0;
    do
    {
      sub_140F80250(a3, v11 + v10, a5, 0);
      ++v12;
      v10 = a1[12];
      v11 += 8;
    }
    while ( v12 < (a1[13] - v10) >> 3 );
  }
  v13 = a1[9];
  if ( a1[10] != v13 )
  {
    v14 = 0;
    v15 = 0;
    do
    {
      sub_140F80250(a3, v14 + v13, a5, 0);
      ++v15;
      v13 = a1[9];
      v14 += 8;
    }
    while ( v15 < (a1[10] - v13) >> 3 );
  }
  v16 = a1[15];
  if ( a1[16] != v16 )
  {
    v17 = 0;
    v18 = 0;
    do
    {
      sub_140F80250(a3, v17 + v16, a5, 0);
      ++v18;
      v16 = a1[15];
      v17 += 8;
    }
    while ( v18 < (a1[16] - v16) >> 3 );
  }
  v19 = (__int64 *)a1[18];
  for ( i = (__int64 *)a1[19]; v19 != i; ++v19 )
  {
    v21 = *v19;
    sub_140F7EE40((_DWORD)a3, *(_DWORD *)v19 + 8, a3[19], a5, 1, 0);
    sub_140F7EC80((_DWORD)a3, v21, a3[3], a5, 1, 0);
  }
  v22 = (__int64 *)a1[24];
  for ( j = (__int64 *)a1[25]; v22 != j; ++v22 )
  {
    v24 = *v22;
    sub_140F7EE40((_DWORD)a3, *(_DWORD *)v22 + 8, a3[19], a5, 1, 0);
    sub_140F7EC80((_DWORD)a3, v24, a3[3], a5, 1, 0);
  }
  v25 = (_DWORD *)a1[21];
  for ( k = (_DWORD *)a1[22]; v25 != k; v25 += 2 )
    sub_140F7EE40((_DWORD)a3, *v25 + 8, a3[2], a5, 1, 0);
  v27 = (_DWORD *)a1[27];
  for ( m = (_DWORD *)a1[28]; v27 != m; v27 += 2 )
    sub_140F7EE40((_DWORD)a3, *v27 + 8, a3[2], a5, 1, 0);
  return 1;
}
