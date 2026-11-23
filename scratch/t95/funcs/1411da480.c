__int64 __fastcall sub_1411DA480(_QWORD *a1, char a2)
{
  char v4; // al
  __int64 v5; // r14
  __int64 v6; // rax
  __int64 i; // rcx
  __int64 v8; // rdi
  unsigned __int64 v9; // rbp
  __int64 v10; // rax
  unsigned __int64 v11; // rdi
  unsigned __int64 v12; // rsi
  __int64 *v13; // rax
  __int64 v14; // rdi
  char v15; // al
  __int64 v16; // r8
  __int64 v17; // rdx
  __int64 v18; // rdx
  unsigned __int64 v19; // rdx
  __int64 j; // rax
  __int64 v21; // rcx
  unsigned __int64 v22; // r12
  __int64 v23; // rax
  unsigned __int64 v24; // rdi
  unsigned __int64 v25; // rbp
  __int64 *v26; // rax
  char v27; // al
  __int64 v28; // rcx
  __int64 v29; // rdx
  __int64 v30; // rdx
  unsigned __int64 v31; // rdx
  __int64 v32; // rax
  _QWORD *v33; // r15
  _QWORD *v34; // rbx
  __int64 *k; // rax
  __int64 v36; // rdx
  unsigned int v37; // ebp
  int v38; // ebx
  char v40; // [rsp+27h] [rbp-41h]

  v4 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 32LL))(qword_141B5AD60);
  v5 = (__int64)(a1[4] - a1[3]) >> 3;
  if ( v4 == 0 )
  {
    v5 += (__int64)(a1[7] - a1[6]) >> 3;
    if ( v5 == 0 )
      goto LABEL_30;
    goto LABEL_9;
  }
  v6 = a1[6];
  for ( i = a1[7]; v6 != i; v6 += 8 )
  {
    v8 = 368;
    if ( *(_BYTE *)(*(_QWORD *)v6 + 47LL) == 0 )
      v8 = 216;
    v5 -= (*(_QWORD *)(*(_QWORD *)(*(_QWORD *)v6 + 48LL) + v8) == 0) - 1LL;
  }
  if ( v5 != 0 )
  {
LABEL_9:
    v9 = 0;
    while ( 1 )
    {
      v10 = a1[3];
      v11 = (a1[4] - v10) >> 3;
      v12 = v9 - v11;
      if ( v9 < v11 )
        break;
      v15 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 32LL))(qword_141B5AD60);
      v16 = a1[6];
      v17 = a1[7];
      if ( v15 != 0 )
      {
        v18 = v17 - v16;
        if ( v18 != 0 )
        {
          v19 = v18 >> 3;
          if ( v19 < 2 )
            v19 = 1;
          for ( j = 0; v19 != j; ++j )
          {
            v14 = *(_QWORD *)(v16 + 8 * j);
            v21 = 368;
            if ( *(_BYTE *)(v14 + 47) == 0 )
              v21 = 216;
            if ( *(_QWORD *)(*(_QWORD *)(v14 + 48) + v21) != 0 )
            {
              if ( v12 == 0 )
                goto LABEL_10;
              --v12;
            }
          }
        }
      }
      else if ( v11 + ((v17 - v16) >> 3) > v9 )
      {
        v13 = (__int64 *)(v16 + 8 * v12);
LABEL_14:
        v14 = *v13;
        if ( *v13 != 0 )
        {
LABEL_10:
          if ( *(_BYTE *)(v14 + 40) == a2 )
            return v14;
        }
      }
      if ( ++v9 == v5 )
        goto LABEL_30;
    }
    v13 = (__int64 *)(v10 + 8 * v9);
    goto LABEL_14;
  }
LABEL_30:
  if ( (a2 == 13 || a2 == 3) && v5 != 0 )
  {
    v40 = a2;
    v22 = 0;
    while ( 1 )
    {
      v23 = a1[3];
      v24 = (a1[4] - v23) >> 3;
      v25 = v22 - v24;
      if ( v22 < v24 )
        break;
      v27 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 32LL))(qword_141B5AD60);
      v28 = a1[6];
      v29 = a1[7];
      if ( v27 != 0 )
      {
        v30 = v29 - v28;
        if ( v30 != 0 )
        {
          v31 = v30 >> 3;
          if ( v31 < 2 )
            v31 = 1;
          v32 = 0;
          while ( 1 )
          {
            v14 = *(_QWORD *)(v28 + 8 * v32);
            v33 = *(_QWORD **)(v14 + 48);
            v34 = v33 + 46;
            if ( *(_BYTE *)(v14 + 47) == 0 )
              v34 = v33 + 27;
            if ( *v34 != 0 )
            {
              if ( v25 == 0 )
                goto LABEL_53;
              --v25;
            }
            if ( v31 == ++v32 )
              goto LABEL_35;
          }
        }
        goto LABEL_35;
      }
      if ( v24 + ((v29 - v28) >> 3) > v22 )
      {
        v26 = (__int64 *)(v28 + 8 * v25);
LABEL_51:
        v14 = *v26;
        if ( *v26 != 0 )
        {
          v33 = *(_QWORD **)(v14 + 48);
LABEL_53:
          if ( v33 != a1 && *(_BYTE *)(v14 + 47) == 0 && v33 != nullptr )
          {
            for ( k = (__int64 *)v33[35]; k != (__int64 *)v33[36]; ++k )
            {
              v36 = *k;
              if ( *(_QWORD **)(*k + 8) == v33 )
              {
                v37 = *(unsigned __int8 *)(v36 + 48);
                if ( v37 <= 0x14 )
                {
                  v38 = 1049072;
                  if ( _bittest(&v38, v37) )
                  {
                    if ( *(_QWORD *)v36 == 0 )
                      break;
                    if ( (_QWORD *)sub_140E68C40(*(_QWORD *)v36) == v33 )
                    {
                      if ( v40 == 3 )
                        return v14;
                      break;
                    }
                    if ( v40 != 13 )
                      break;
                    return v14;
                  }
                }
              }
            }
          }
        }
      }
LABEL_35:
      if ( ++v22 == v5 )
        return 0;
    }
    v26 = (__int64 *)(v23 + 8 * v22);
    goto LABEL_51;
  }
  return 0;
}
