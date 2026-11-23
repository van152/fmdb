char __fastcall sub_140928730(_QWORD *a1, __int64 a2, char **a3, int a4, char a5)
{
  char **v6; // r12
  __int64 v9; // rax
  __int64 v10; // r13
  unsigned __int64 v11; // r13
  char result; // al
  unsigned __int64 v13; // rbp
  __int64 v14; // rdx
  __int64 v15; // rcx
  __int64 v16; // rax
  __int64 v17; // rcx
  __int64 v18; // r15
  char **v19; // rsi
  __int64 v20; // r12
  char *v21; // rdi
  __int64 v22; // r9
  int v23; // r15d
  __int64 v24; // rsi
  char v25; // bl
  bool v26; // zf
  __int64 v27; // rax
  __int64 v28; // r15
  __int64 v29; // rdx
  bool v30; // r8
  bool v31; // dl
  char v32; // r15
  __int64 v33; // rsi
  __int64 v34; // rax
  __int64 v35; // rax
  __int64 v36; // rax
  __int64 v37; // rax
  char v38; // [rsp+2Eh] [rbp-5Ah]
  unsigned __int8 v39; // [rsp+2Fh] [rbp-59h]
  unsigned __int8 v40; // [rsp+2Fh] [rbp-59h]
  char *v41; // [rsp+30h] [rbp-58h]
  __int64 v42; // [rsp+38h] [rbp-50h]
  bool v43; // [rsp+40h] [rbp-48h]

  v6 = a3;
  v9 = a1[56];
  v10 = a1[57];
  if ( a3 != nullptr )
    *a3 = nullptr;
  if ( v10 != v9 )
  {
    v11 = (v10 - v9) >> 3;
    result = -1;
    v13 = 0;
    v41 = nullptr;
    v43 = false;
    while ( 1 )
    {
      if ( (v13 & 0x80u) != 0LL )
        goto LABEL_6;
      v14 = a1[56];
      if ( (a1[57] - v14) >> 3 <= v13 )
        goto LABEL_6;
      v15 = *(_QWORD *)(v14 + 8 * v13);
      if ( v15 == 0 )
        goto LABEL_6;
      v38 = result;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v15 + 656LL))(v15) == 6 )
        goto LABEL_5;
      v16 = a1[56];
      v17 = *(_QWORD *)(v16 + 8 * v13);
      if ( v17 == 0 )
        goto LABEL_5;
      if ( (a1[57] - v16) >> 3 > v13
        && (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v17 + 656LL))(v17) != 6
        && (v18 = *(_QWORD *)(a1[56] + 8 * v13)) != 0
        && (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v18 + 632LL))(v18) != 0
        && (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v18 + 632LL))(v18) != 0 )
      {
        if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v18 + 784LL))(v18) != 0 )
        {
          v39 = a4;
          v19 = v6;
          v20 = 0;
          while ( 1 )
          {
            v21 = (char *)(*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)v18 + 792LL))(v18, v20);
            LOBYTE(v22) = 1;
            if ( (*(unsigned __int8 (__fastcall **)(char *, __int64, _QWORD, __int64))(*(_QWORD *)v21 + 536LL))(
                   v21,
                   a2,
                   0,
                   v22) != 0 )
              break;
            v20 = (unsigned __int8)(v20 + 1);
            if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v18 + 784LL))(v18) <= (unsigned __int64)(unsigned __int8)v20 )
            {
              v21 = nullptr;
              break;
            }
          }
          v6 = v19;
          a4 = v39;
        }
        else
        {
          v21 = nullptr;
        }
        v37 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v18 + 824LL))(v18);
        if ( v37 != 0 )
        {
          v26 = *(_BYTE *)(v37 + 149) == 3;
          result = v38;
          if ( v26 )
            goto LABEL_6;
          goto LABEL_25;
        }
      }
      else
      {
        v21 = (char *)sub_1408FA960((__int64)a1, v13, 0xFFu, 0);
      }
      result = v38;
LABEL_25:
      if ( v21 == nullptr )
        goto LABEL_6;
      if ( (*(unsigned __int8 (__fastcall **)(char *))(*(_QWORD *)v21 + 400LL))(v21) == 0
        && *(char *)((*(__int64 (__fastcall **)(char *))(*(_QWORD *)v21 + 888LL))(v21) + 98) >= 0 )
      {
        v42 = a2;
        if ( v21[216] <= 0 )
          goto LABEL_62;
        v23 = a4;
        v24 = 0;
        v25 = 0;
        do
          v25 += _bittest(
                   (const signed __int32 *)((*(__int64 (__fastcall **)(char *, __int64))(*(_QWORD *)v21 + 840LL))(
                                              v21,
                                              v24++)
                                          + 200),
                   6u);
        while ( v24 < v21[216] );
        v26 = v25 == 0;
        a4 = v23;
        a2 = v42;
        if ( v26 || (_BYTE)v23 != 0 )
        {
LABEL_62:
          v27 = (*(__int64 (__fastcall **)(char *, __int64))(*(_QWORD *)v21 + 824LL))(v21, a2);
          if ( v27 != 0 )
          {
            v28 = v27;
            if ( (*(__int64 (__fastcall **)(char *))(*(_QWORD *)v21 + 296LL))(v21) != a1[36]
              || v41 == nullptr
              || v43
              || (*(__int64 (__fastcall **)(char *))(*(_QWORD *)v41 + 296LL))(v41) == a1[36] )
            {
              v30 = !v43;
              result = v38;
              v31 = v38 != -1;
              if ( v30 && v31 && *(_BYTE *)(v28 + 14) == 0 )
              {
                a2 = v42;
              }
              else
              {
                a2 = v42;
                if ( !v31 || !v30 || v41 == nullptr )
                {
                  v32 = *(_BYTE *)(v28 + 225);
                  if ( a5 != 0 )
                    v32 += *(_BYTE *)((*(__int64 (__fastcall **)(char *))(*(_QWORD *)v21 + 888LL))(v21) + 349);
                  v43 = false;
                  LOBYTE(v29) = 1;
                  if ( (*(unsigned __int8 (__fastcall **)(char *, __int64, _QWORD, _QWORD, _QWORD))(*(_QWORD *)v21 + 48LL))(
                         v21,
                         v29,
                         0,
                         0,
                         0) != 0
                    && (v43 = true, (*(__int64 (__fastcall **)(char *))(*(_QWORD *)v21 + 296LL))(v21) != a1[36])
                    && (*(__int64 (__fastcall **)(char *))(*(_QWORD *)v21 + 888LL))(v21) != 0 )
                  {
                    v40 = a4;
                    v33 = (*(__int64 (__fastcall **)(char *))(*(_QWORD *)v21 + 528LL))(v21);
                    v34 = (*(__int64 (__fastcall **)(char *))(*(_QWORD *)v21 + 888LL))(v21);
                    v35 = sub_140928C90(v33, v42, *(unsigned __int8 *)(v34 + 60), 0);
                    if ( v35 != 0 )
                    {
                      v36 = sub_140A45290(v35, v42);
                      if ( v36 != 0 )
                        v43 = *(_BYTE *)(v36 + 39) == *(_BYTE *)(v36 + 40);
                      v41 = v21;
                      a4 = v40;
                      a2 = v42;
                    }
                    else
                    {
                      v41 = v21;
                      a4 = v40;
                    }
                  }
                  else
                  {
                    v41 = v21;
                  }
                  result = v32;
                }
              }
              goto LABEL_6;
            }
          }
        }
      }
LABEL_5:
      result = v38;
LABEL_6:
      v13 = (unsigned __int8)(v13 + 1);
      if ( v11 <= v13 )
        goto LABEL_58;
    }
  }
  result = -1;
  v41 = nullptr;
LABEL_58:
  if ( v6 != nullptr )
    *v6 = v41;
  return result;
}
