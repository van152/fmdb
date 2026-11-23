__int64 __fastcall sub_140945390(_QWORD *a1, unsigned int a2, __int64 a3)
{
  __int64 v6; // rax
  __int64 v7; // rax
  unsigned __int64 v8; // rbp
  __int64 v9; // rbx
  __int64 v10; // rdx
  __int64 v11; // rax
  unsigned __int64 v12; // rax
  __int64 v13; // rcx
  __int64 v14; // rdi
  __int64 v15; // rbp
  __int64 result; // rax
  unsigned __int64 v17; // rbp
  unsigned __int64 v18; // rcx
  bool v19; // cf
  __int64 v20; // rbx
  __int64 v21; // rax
  __int64 v22; // rcx
  unsigned __int64 i; // rbp
  __int64 *v24; // rbx
  char v25; // al
  __int64 v26; // rdx
  __int64 v27; // rax
  __int64 v28; // rdx
  __int64 v29; // rbp
  __int64 v30; // rbx
  unsigned __int64 v31; // rbx
  unsigned __int64 v32; // rdi
  __int64 v33; // rcx

  v6 = a1[115];
  if ( v6 != 0 )
  {
    if ( *(_BYTE *)(v6 + 143) != 0 )
    {
LABEL_25:
      v21 = a1[56];
      v22 = a1[57];
      if ( v22 != v21 )
      {
        for ( i = 0; i < (v22 - v21) >> 3; ++i )
        {
          v24 = *(__int64 **)(v21 + 8 * i);
          if ( v24 != nullptr )
          {
            v25 = (*(__int64 (__fastcall **)(__int64 *))(*v24 + 624))(v24);
            v26 = *v24;
            if ( v25 != 0 )
              return (*(__int64 (__fastcall **)(__int64 *, _QWORD, __int64))(v26 + 1008))(v24, a2, a3);
            if ( (*(unsigned __int8 (__fastcall **)(__int64 *))(v26 + 632))(v24) != 0 )
              return (*(__int64 (__fastcall **)(__int64 *, _QWORD, __int64))(*v24 + 840))(v24, a2, a3);
            v21 = a1[56];
            v22 = a1[57];
          }
        }
      }
      v27 = a1[115];
      if ( v27 != 0 && ((_BYTE)a2 == 0 || *(_BYTE *)(v27 + 142) != 0) )
      {
        v28 = *(unsigned int *)(v27 + 116);
        if ( (_DWORD)v28 != -1 )
          return sub_140F45DB0(qword_141B5FDC0, v28);
      }
      return 0;
    }
  }
  else
  {
    v7 = a1[56];
    if ( a1[57] != v7 )
    {
      v8 = 0;
      do
      {
        v9 = *(_QWORD *)(v7 + 8 * v8);
        if ( v9 != 0
          && (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v9 + 368LL))(v9) != 0
          && (*(_BYTE *)((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v9 + 368LL))(v9) + 57) & 1) != 0 )
        {
          goto LABEL_25;
        }
        ++v8;
        v7 = a1[56];
      }
      while ( v8 < (a1[57] - v7) >> 3 );
    }
  }
  v10 = a1[24];
  v11 = a1[25];
  if ( v10 == v11 )
    goto LABEL_25;
  v12 = (v11 - v10) >> 3;
  v13 = 2;
  if ( v12 < 2 )
    v13 = v12;
  if ( v13 == 0 )
    return 0;
  if ( a3 != 0 )
  {
    v14 = 0;
    v15 = 0;
    do
    {
      v20 = *(_QWORD *)(v10 + 8 * v15);
      if ( (unsigned __int8)sub_1409D4AC0(v20, a3, 0) != 0 )
      {
        result = sub_140945390(v20, a2, a3);
        if ( v14 != 0 && v14 != result )
          return 0;
      }
      else
      {
        result = v14;
      }
      v17 = v15 + 1;
      v10 = a1[24];
      v18 = (a1[25] - v10) >> 3;
      if ( v18 >= 2 )
        v18 = 2;
      v14 = result;
      v19 = v17 < v18;
      v15 = 1;
    }
    while ( v19 );
  }
  else
  {
    v29 = 0;
    v30 = 0;
    do
    {
      v33 = sub_140945390(*(_QWORD *)(v10 + 8 * v30), a2, 0);
      if ( v29 != 0 )
      {
        result = 0;
        if ( v29 != v33 )
          break;
      }
      v31 = v30 + 1;
      v10 = a1[24];
      v32 = (a1[25] - v10) >> 3;
      if ( v32 >= 2 )
        v32 = 2;
      v29 = v33;
      result = v33;
      v19 = v31 < v32;
      v30 = 1;
    }
    while ( v19 );
  }
  return result;
}
