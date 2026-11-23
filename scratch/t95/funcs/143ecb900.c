char __fastcall sub_143ECB900(_QWORD *a1, __int64 a2, _QWORD *a3, char a4, unsigned __int8 a5)
{
  __int64 v8; // rdx
  int v9; // ebx
  unsigned __int64 v10; // rbp
  __int64 v11; // rdx
  unsigned __int64 v12; // rbp
  __int64 v13; // r8
  __int64 v14; // rax
  unsigned __int64 v15; // rbx
  __int64 v16; // rbp
  __int64 v17; // rax
  unsigned __int64 v18; // rbx
  __int64 v19; // rbp
  __int64 v20; // rdx
  __int64 v21; // rbx
  unsigned __int64 v22; // rbp

  sub_140F7F220(a3, a1 + 30, a5);
  sub_140F7FC40(a3, a1 + 31, a5);
  sub_140F7EC80((_DWORD)a3, (_DWORD)a1 + 232, a3[1], a5, 1, 0);
  sub_140F7F320(a3, a1 + 32, a5);
  v8 = a1[37];
  if ( a1[38] != v8 )
  {
    v9 = 0;
    v10 = 0;
    do
    {
      sub_140F7EC80((_DWORD)a3, v9 + v8, a3[5], a5, 1, 0);
      ++v10;
      v8 = a1[37];
      v9 += 8;
    }
    while ( v10 < (a1[38] - v8) >> 3 );
  }
  v11 = a1[9];
  if ( a1[10] != v11 )
  {
    v12 = 0;
    do
    {
      sub_140F7EC80((_DWORD)a3, 16 * v12 + v11, a3[10], a5, 1, 0);
      v11 = a1[9];
      v13 = a1[10];
      if ( *(_QWORD *)(v11 + 16 * v12) == 0 )
      {
        sub_141758A00(16 * v12 + v11, 16 * v12 + v11 + 16, v13 - (16 * v12 + v11 + 16));
        v11 = a1[9];
        v13 = a1[10] - 16LL;
        a1[10] = v13;
        --v12;
      }
      ++v12;
    }
    while ( v12 < (v13 - v11) >> 4 );
  }
  v14 = a1[21];
  if ( a1[22] != v14 )
  {
    v15 = 0;
    do
    {
      v16 = *(_QWORD *)(v14 + 8 * v15);
      sub_140F7EC80((_DWORD)a3, v16, a3[5], a5, 1, 0);
      sub_140F7F220(a3, v16 + 8, a5);
      sub_140F7EC80((_DWORD)a3, v16 + 16, a3[5], a5, 1, 0);
      sub_140F7FC40(a3, v16 + 24, a5);
      sub_140F80150(a3, v16 + 32, a5);
      ++v15;
      v14 = a1[21];
    }
    while ( v15 < (a1[22] - v14) >> 3 );
  }
  v17 = a1[18];
  if ( a1[19] != v17 )
  {
    v18 = 0;
    do
    {
      v19 = *(_QWORD *)(v17 + 8 * v18);
      sub_140F7EC80((_DWORD)a3, v19, a3[5], a5, 1, 0);
      sub_140F7F220(a3, v19 + 8, a5);
      sub_140F7EC80((_DWORD)a3, v19 + 16, a3[5], a5, 1, 0);
      sub_140F7FC40(a3, v19 + 24, a5);
      sub_140F80150(a3, v19 + 32, a5);
      ++v18;
      v17 = a1[18];
    }
    while ( v18 < (a1[19] - v17) >> 3 );
  }
  v20 = a1[24];
  if ( a1[25] != v20 )
  {
    v21 = 0;
    v22 = 0;
    do
    {
      sub_140F80150(a3, v21 + v20, a5);
      ++v22;
      v20 = a1[24];
      v21 += 16;
    }
    while ( v22 < (a1[25] - v20) >> 4 );
  }
  if ( a4 != 0 )
    sub_140F7FD40(a3, a1 + 35, a5);
  return 1;
}
