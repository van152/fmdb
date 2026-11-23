char __fastcall sub_1444E5A90(_QWORD *a1, __int64 a2, _QWORD *a3, char a4, unsigned __int8 a5)
{
  _QWORD *v7; // rbx
  _QWORD *v8; // rbp
  unsigned __int64 v9; // rsi
  __int64 v10; // rax
  __int64 v11; // rax
  __int64 v12; // rcx
  _QWORD *v13; // rax
  _QWORD *v14; // rbp
  __int64 v15; // r14
  __int64 v16; // rdx
  int v17; // esi
  unsigned __int64 v18; // rbx
  __int64 v19; // rdx
  __int64 v20; // rsi
  unsigned __int64 v21; // rbx
  __int64 v22; // rdx
  int v23; // esi
  unsigned __int64 v24; // rbx
  __int64 v25; // rdx
  __int64 v26; // rsi
  unsigned __int64 v27; // rbx
  __int64 v29[8]; // [rsp+38h] [rbp-40h] BYREF

  if ( a4 != 0 )
  {
    v7 = (_QWORD *)a1[28];
    v8 = v7;
    if ( v7 != (_QWORD *)a1[27] )
    {
      v8 = (_QWORD *)a1[27];
      v9 = 0;
      do
      {
        if ( (a5 & 8) != 0 )
        {
          v11 = v8[v9];
          v12 = v11 + 136;
          if ( v11 == 0 )
            v12 = 0;
          v29[0] = v12;
        }
        else
        {
          v29[0] = v8[v9];
        }
        if ( (unsigned __int8)sub_140F80250(a3, v29, a5, 0) != 0 )
        {
          if ( v29[0] != 0 )
            v10 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v29[0] + 1880LL))(v29[0]);
          else
            v10 = 0;
          v8[v9] = v10;
        }
        ++v9;
        v8 = (_QWORD *)a1[27];
        v7 = (_QWORD *)a1[28];
      }
      while ( v9 < v7 - v8 );
    }
    v13 = (_QWORD *)sub_141751B70(v8, v7, 0);
    v14 = v13;
    if ( v13 != v7 )
    {
      while ( ++v13 != v7 )
      {
        if ( *v13 != 0 )
          *v14++ = *v13;
      }
    }
    if ( v14 != v7 )
    {
      v15 = a1[28] - (_QWORD)v7;
      sub_141758A00(v14, v7, v15);
      a1[28] = (char *)v14 + v15;
    }
  }
  sub_140F7EC80((_DWORD)a3, (_DWORD)a1 + 192, a3[1], a5, 1, 0);
  v16 = a1[9];
  if ( a1[10] != v16 )
  {
    v17 = 0;
    v18 = 0;
    do
    {
      sub_140F7EC80((_DWORD)a3, v17 + v16, a3[3], a5, 1, 0);
      ++v18;
      v16 = a1[9];
      v17 += 8;
    }
    while ( v18 < (a1[10] - v16) >> 3 );
  }
  v19 = a1[15];
  if ( a1[16] != v19 )
  {
    v20 = 0;
    v21 = 0;
    do
    {
      sub_140F7F730(a3, v20 + v19, a5);
      ++v21;
      v19 = a1[15];
      v20 += 8;
    }
    while ( v21 < (a1[16] - v19) >> 3 );
  }
  v22 = a1[12];
  if ( a1[13] != v22 )
  {
    v23 = 0;
    v24 = 0;
    do
    {
      sub_140F7EC80((_DWORD)a3, v23 + v22, a3[5], a5, 1, 0);
      ++v24;
      v22 = a1[12];
      v23 += 8;
    }
    while ( v24 < (a1[13] - v22) >> 3 );
  }
  sub_140F7F220(a3, a1 + 25, a5);
  v25 = a1[18];
  if ( a1[19] != v25 )
  {
    v26 = 0;
    v27 = 0;
    do
    {
      sub_140F7F830(a3, v26 + v25, a5);
      ++v27;
      v25 = a1[18];
      v26 += 8;
    }
    while ( v27 < (a1[19] - v25) >> 3 );
  }
  return 1;
}
