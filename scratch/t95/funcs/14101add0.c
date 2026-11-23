// THUNK ALIAS -> sub_143E8F250 (jmp:0x14101add0->0x143e8f250)
__int64 __fastcall sub_143E8F250(_QWORD *a1, char a2, __int64 a3, char a4)
{
  int v6; // r12d
  _QWORD *v7; // rax
  _QWORD *v8; // rcx
  __int64 v9; // rcx
  unsigned __int64 v10; // r15
  __int64 v11; // rax
  __int64 v12; // rcx
  __int64 v13; // rsi
  __int64 v14; // rax
  unsigned __int64 v15; // rbp
  __int64 v16; // rbx
  __int64 *v17; // rax
  unsigned __int64 v18; // rcx
  __int64 v19; // rdi
  unsigned __int64 v20; // rbp
  __int64 v21; // rax
  __int64 v22; // rcx
  __int64 v23; // rsi
  __int64 v24; // rax
  __int64 v25; // rcx
  unsigned __int64 v26; // r15
  __int64 *v27; // rax
  unsigned __int64 v28; // rcx
  __int64 v29; // rdi
  __int64 v31; // [rsp+20h] [rbp-48h]

  v6 = a2;
  switch ( a2 )
  {
    case 1:
      v7 = a1 + 69;
      v8 = a1 + 70;
      break;
    case 2:
      v7 = a1 + 72;
      v8 = a1 + 73;
      break;
    case 3:
      v7 = a1 + 66;
      v8 = a1 + 67;
      break;
    default:
      return 0;
  }
  v9 = *v8 - *v7;
  if ( v9 == 0 )
    return 0;
  v31 = v9 >> 3;
  if ( a4 == 0 )
  {
    v20 = 0;
    while ( 1 )
    {
      if ( v6 == 1 )
      {
        v21 = a1[69];
        v22 = a1[70];
      }
      else if ( v6 == 2 )
      {
        v21 = a1[72];
        v22 = a1[73];
      }
      else
      {
        v21 = a1[66];
        v22 = a1[67];
      }
      if ( (v22 - v21) >> 3 <= v20 )
      {
        v23 = 0;
        if ( MEMORY[0x24] == 3 )
        {
LABEL_43:
          v24 = *(_QWORD *)(v23 + 64);
          v25 = *(_QWORD *)(v23 + 72);
          if ( v25 != v24 )
          {
            v26 = 0;
            do
            {
              v16 = *(_QWORD *)(v24 + 8 * v26);
              if ( v16 != 0 )
              {
                v27 = *(__int64 **)(v16 + 176);
                v28 = *(_QWORD *)(v16 + 184) - (_QWORD)v27;
                if ( v28 == 0
                  || (v29 = 0, v28 <= 8)
                  && ((v29 = *v27, *v27 == 0)
                   || (*(unsigned int (__fastcall **)(__int64))(*(_QWORD *)v29 + 56LL))(v29) != 25) )
                {
                  v29 = 0;
                }
                if ( v29 == a3 )
                  return v16;
                v24 = *(_QWORD *)(v23 + 64);
                v25 = *(_QWORD *)(v23 + 72);
              }
              ++v26;
            }
            while ( v26 < (v25 - v24) >> 3 );
          }
        }
      }
      else
      {
        v23 = *(_QWORD *)(v21 + 8 * v20);
        if ( *(_BYTE *)(v23 + 36) == 3 )
          goto LABEL_43;
      }
      if ( ++v20 == v31 )
        return 0;
    }
  }
  v10 = 0;
  while ( 1 )
  {
    if ( v6 == 1 )
    {
      v11 = a1[69];
      v12 = a1[70];
    }
    else if ( v6 == 3 )
    {
      v11 = a1[66];
      v12 = a1[67];
    }
    else
    {
      v11 = a1[72];
      v12 = a1[73];
    }
    if ( (v12 - v11) >> 3 <= v10 )
      break;
    v13 = *(_QWORD *)(v11 + 8 * v10);
    if ( *(_BYTE *)(v13 + 36) == 3 )
      goto LABEL_20;
LABEL_10:
    if ( ++v10 == v31 )
      return 0;
  }
  v13 = 0;
  if ( MEMORY[0x24] != 3 )
    goto LABEL_10;
LABEL_20:
  v14 = *(_QWORD *)(v13 + 64);
  if ( *(_QWORD *)(v13 + 72) == v14 )
    goto LABEL_10;
  v15 = 0;
  while ( 1 )
  {
    v16 = *(_QWORD *)(v14 + 8 * v15);
    if ( v16 != 0 )
    {
      v17 = *(__int64 **)(v16 + 176);
      v18 = *(_QWORD *)(v16 + 184) - (_QWORD)v17;
      if ( v18 == 0
        || (v19 = 0, v18 <= 8)
        && ((v19 = *v17, *v17 == 0) || (*(unsigned int (__fastcall **)(__int64))(*(_QWORD *)v19 + 56LL))(v19) != 25) )
      {
        v19 = 0;
      }
      if ( v19 == a3 && *(_BYTE *)(v16 + 118) == 0 )
        return v16;
    }
    ++v15;
    v14 = *(_QWORD *)(v13 + 64);
    if ( v15 >= (*(_QWORD *)(v13 + 72) - v14) >> 3 )
      goto LABEL_10;
  }
}
