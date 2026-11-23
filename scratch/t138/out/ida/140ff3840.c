__int64 __fastcall sub_140FF3840(_QWORD *a1)
{
  __int64 *v2; // rax
  __int64 *v3; // rdx
  __int64 *v4; // rcx
  __int64 *v5; // rdi
  volatile signed __int32 *v6; // rsi
  __int64 v7; // rdi
  int v8; // r9d
  void (__fastcall ***v9)(_QWORD, __int64); // rcx
  __int64 v10; // rcx
  volatile signed __int32 *v11; // rbx
  int v12; // eax
  _QWORD *v13; // rdi
  _QWORD *v14; // rsi
  unsigned __int64 v15; // rdi
  _QWORD *v16; // rsi
  int v17; // eax
  __int64 v18; // r14
  __int64 v19; // rsi
  __int64 v20; // r14
  __int64 v21; // rdx
  __int64 v22; // rbx
  __int64 v23; // rdi
  __int64 v24; // rcx
  __int64 v25; // rcx
  __int64 v26; // r15
  unsigned __int64 v27; // rdi
  unsigned __int64 v28; // rdi
  unsigned __int64 v29; // rdi
  _DWORD *v30; // rax
  int v31; // eax
  unsigned __int64 v32; // rdi
  _DWORD *v33; // rax
  int v34; // eax
  unsigned __int64 v35; // rdi
  bool v36; // zf
  _QWORD *v38; // rsi
  int v39; // eax
  __int64 v40; // r14
  _QWORD *v41; // rsi
  int v42; // eax
  __int64 v43; // r14
  _QWORD *v44; // r12
  __int64 *v45; // rcx
  __int64 v46; // rax
  char v47; // bl
  __int64 *v48; // rcx
  unsigned __int64 v49; // rcx
  __int64 v50; // rdx
  __int64 v51; // rsi
  char v52; // al
  unsigned __int64 v53; // rbx
  unsigned __int64 v54; // rbx
  __int64 v55; // [rsp+30h] [rbp-40h] BYREF
  char v56[8]; // [rsp+38h] [rbp-38h] BYREF
  __int64 v57; // [rsp+40h] [rbp-30h]
  __int64 v58; // [rsp+48h] [rbp-28h] BYREF
  _QWORD *v59; // [rsp+50h] [rbp-20h]
  volatile signed __int32 *v60; // [rsp+58h] [rbp-18h]
  unsigned __int64 v61; // [rsp+60h] [rbp-10h] BYREF
  _QWORD v62[9]; // [rsp+68h] [rbp-8h] BYREF

  v62[1] = -2;
  v2 = **(__int64 ***)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
  v3 = (__int64 *)v2[1];
  v4 = v2;
  if ( *((_BYTE *)v3 + 25) == 0 )
  {
    v4 = **(__int64 ***)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
    do
    {
      v5 = v3 + 2;
      if ( v3[4] >= (unsigned __int64)qword_141B5EDF0 )
      {
        v4 = v3;
        v5 = v3;
      }
      v3 = (__int64 *)*v5;
    }
    while ( *(_BYTE *)(*v5 + 25) == 0 );
  }
  if ( *((_BYTE *)v4 + 25) != 0 )
  {
LABEL_7:
    v6 = nullptr;
    goto LABEL_8;
  }
  v6 = nullptr;
  if ( qword_141B5EDF0 >= (unsigned __int64)v4[4] && v4 != v2 )
  {
    v6 = (volatile signed __int32 *)v4[5];
    if ( v6 != nullptr )
    {
      _InterlockedIncrement(v6 + 2);
      goto LABEL_8;
    }
    goto LABEL_7;
  }
LABEL_8:
  sub_14080D0E0(a1: v56, a2: 0x1418E2C24LL);
  v7 = sub_1412EC810(a1: 264, a2: 7);
  *(_QWORD *)v7 = 0x700000000LL;
  strcpy((char *)(v7 + 8), "summary");
  _InterlockedIncrement((volatile signed __int32 *)v7);
  v58 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v7);
  v58 = v7 + 4;
  v55 = 0x80100004E554C4CLL;
  if ( v6 != nullptr
    && ((*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64 *, char *))(*(_QWORD *)v6 + 224LL))(
          a1: v6,
          a2: v62,
          a3: &v58,
          a4: v56),
        v62[0] != 0) )
  {
    LOWORD(v8) = 3569;
    sub_1407D1280(a1: (unsigned int)&v55, a2: (unsigned int)&v61, a3: (unsigned int)v62, a4: v8, a5: 0);
    v9 = (void (__fastcall ***)(_QWORD, __int64))v62[0];
    if ( v62[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v62[0] + 8LL)) == 0 )
      (**v9)(a1: v9, a2: 1);
  }
  else
  {
    v61 = 0;
  }
  v10 = v58;
  if ( v58 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v58 - 4)) == 0 )
    sub_1412EC9A0(a1: v10 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v7) == 0 )
    sub_1412EC9A0(a1: v7);
  if ( v61 != 0 )
  {
    v60 = v6;
    LODWORD(v62[0]) = (a1[2] - a1[1]) >> 3;
    (*(void (__fastcall **)(unsigned __int64, _QWORD *, __int64))(*(_QWORD *)v61 + 40LL))(a1: v61, a2: v62, a3: 4);
    v11 = (volatile signed __int32 *)v61;
    v12 = *(_DWORD *)(v61 + 16);
    v59 = a1;
    if ( v12 != 0 || (v13 = (_QWORD *)a1[1], v14 = (_QWORD *)a1[2], v13 == v14) )
    {
      if ( v12 == 0 )
      {
LABEL_32:
        v16 = v59;
        LODWORD(v62[0]) = (v59[5] - v59[4]) >> 3;
        (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v11 + 40LL))(
          a1: v11,
          a2: v62,
          a3: 4);
        v15 = v61;
        v17 = *(_DWORD *)(v61 + 16);
        if ( v17 != 0 || (v18 = v16[4], v19 = v16[5], v18 == v19) )
        {
LABEL_62:
          if ( v17 == 0 )
          {
            v38 = v59;
            LODWORD(v62[0]) = (v59[14] - v59[13]) >> 3;
            (*(void (__fastcall **)(unsigned __int64, _QWORD *, __int64))(*(_QWORD *)v15 + 40LL))(
              a1: v15,
              a2: v62,
              a3: 4);
            v11 = (volatile signed __int32 *)v61;
            v39 = *(_DWORD *)(v61 + 16);
            if ( v39 != 0 || (v15 = v38[13], v40 = v38[14], v15 == v40) )
            {
              if ( v39 == 0 )
              {
LABEL_77:
                v41 = v59;
                LODWORD(v62[0]) = (v59[17] - v59[16]) >> 3;
                (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v11 + 40LL))(
                  a1: v11,
                  a2: v62,
                  a3: 4);
                v11 = (volatile signed __int32 *)v61;
                v42 = *(_DWORD *)(v61 + 16);
                if ( v42 != 0 || (v15 = v41[16], v43 = v41[17], v15 == v43) )
                {
                  if ( v42 == 0 )
                  {
LABEL_86:
                    v44 = (_QWORD *)qword_141B5FDD8;
                    v45 = *(__int64 **)(qword_141B5FDD8 + 128);
                    v46 = *v45;
                    if ( v45[1] != *v45 )
                    {
                      v47 = word_141B60320;
                      v15 = 0;
                      do
                      {
                        v49 = v15 & 0x7FFFFFFF;
                        if ( v47 != 0 || (v50 = v44[12], (v44[13] - v50) >> 3 <= v49) )
                          v50 = v46;
                        v51 = *(_QWORD *)(v50 + 8 * v49);
                        v52 = sub_14157FD30(a1: *(unsigned int *)(v51 + 12));
                        if ( v52 != -1 )
                        {
                          v53 = v61;
                          LODWORD(v62[0]) = v52;
                          (*(void (__fastcall **)(unsigned __int64, _QWORD *, __int64))(*(_QWORD *)v61 + 40LL))(
                            a1: v61,
                            a2: v62,
                            a3: 4);
                          if ( *(_DWORD *)(v53 + 16) != 0 )
                            goto LABEL_63;
                          v54 = v61;
                          LODWORD(v62[0]) = *(_DWORD *)(v51 + 56);
                          (*(void (__fastcall **)(unsigned __int64, _QWORD *, __int64))(*(_QWORD *)v61 + 40LL))(
                            a1: v61,
                            a2: v62,
                            a3: 4);
                          if ( *(_DWORD *)(v54 + 16) != 0 )
                            goto LABEL_63;
                          v47 = word_141B60320;
                          v44 = (_QWORD *)qword_141B5FDD8;
                        }
                        ++v15;
                        v48 = (__int64 *)v44[16];
                        v46 = *v48;
                      }
                      while ( v15 < (v48[1] - *v48) >> 3 );
                      v11 = (volatile signed __int32 *)v61;
                    }
                    LODWORD(v62[0]) = -1;
                    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v11 + 40LL))(
                      a1: v11,
                      a2: v62,
                      a3: 4);
                    if ( *((_DWORD *)v11 + 4) == 0 )
                    {
                      v11 = (volatile signed __int32 *)v61;
                      LOBYTE(v15) = *(_DWORD *)(v61 + 16) == 0;
                      v6 = v60;
                      if ( _InterlockedDecrement((volatile signed __int32 *)(v61 + 8)) != 0 )
                        goto LABEL_66;
                      goto LABEL_65;
                    }
                  }
                }
                else
                {
                  while ( 1 )
                  {
                    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v11 + 40LL))(
                      a1: v11,
                      a2: *(_QWORD *)v15 + 8LL,
                      a3: 4);
                    if ( *((_DWORD *)v11 + 4) != 0 )
                      break;
                    v11 = (volatile signed __int32 *)v61;
                    if ( *(_DWORD *)(v61 + 16) != 0 )
                      goto LABEL_83;
                    v15 += 8LL;
                    if ( v15 == v43 )
                      goto LABEL_86;
                  }
                }
              }
            }
            else
            {
              while ( 1 )
              {
                (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v11 + 40LL))(
                  a1: v11,
                  a2: *(_QWORD *)v15 + 8LL,
                  a3: 4);
                if ( *((_DWORD *)v11 + 4) != 0 )
                  break;
                v11 = (volatile signed __int32 *)v61;
                if ( *(_DWORD *)(v61 + 16) != 0 )
                  goto LABEL_83;
                v15 += 8LL;
                if ( v15 == v40 )
                  goto LABEL_77;
              }
            }
          }
        }
        else
        {
          v20 = v18 + 8;
          v21 = 0x141886CC2LL;
          v57 = v19;
          while ( 1 )
          {
            v22 = *(_QWORD *)(v20 - 8);
            if ( *(_DWORD *)(v22 + 4) == 771 && *(int *)(v22 + 144) > 0 )
            {
              v62[0] = 0;
              v23 = sub_1412EC810(a1: 264, a2: 32);
              *(_QWORD *)v23 = 0x2000000000LL;
              strcpy((char *)(v23 + 8), "Germany should not be manageable");
              v24 = v62[0];
              if ( v62[0] != 0 )
              {
                v24 = v62[0] - 4LL;
                if ( _InterlockedDecrement((volatile signed __int32 *)(v62[0] - 4LL)) == 0 )
                  sub_1412EC9A0(a1: v24);
              }
              v62[0] = 0;
              _InterlockedIncrement((volatile signed __int32 *)v23);
              v62[0] = v23 + 4;
              LOBYTE(v24) = 1;
              sub_1407E0E00(a1: v24, a2: v62, a3: 0);
              v25 = v62[0];
              v19 = v57;
              if ( v62[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v62[0] - 4LL)) == 0 )
                sub_1412EC9A0(a1: v25 - 4);
              v15 = v61;
              v21 = 0x141886CC2LL;
            }
            v26 = v21;
            (*(void (__fastcall **)(unsigned __int64, __int64, __int64))(*(_QWORD *)v15 + 40LL))(
              a1: v15,
              a2: v21,
              a3: 1);
            if ( *(_DWORD *)(v15 + 16) != 0 )
              break;
            v27 = v61;
            (*(void (__fastcall **)(unsigned __int64, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
              a1: v61,
              a2: v22,
              a3: 4);
            if ( *(_DWORD *)(v27 + 16) != 0 )
              break;
            v28 = v61;
            (*(void (__fastcall **)(unsigned __int64, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
              a1: v61,
              a2: v22 + 4,
              a3: 4);
            if ( *(_DWORD *)(v28 + 16) != 0 )
              break;
            v29 = v61;
            (*(void (__fastcall **)(unsigned __int64, __int64, __int64))(*(_QWORD *)v61 + 40LL))(
              a1: v61,
              a2: v22 + 144,
              a3: 4);
            if ( *(_DWORD *)(v29 + 16) != 0 )
              break;
            v30 = *(_DWORD **)(v22 + 136);
            v31 = v30 != nullptr ? *v30 : -1;
            v32 = v61;
            LODWORD(v62[0]) = v31;
            (*(void (__fastcall **)(unsigned __int64, _QWORD *, __int64))(*(_QWORD *)v61 + 40LL))(
              a1: v61,
              a2: v62,
              a3: 4);
            if ( *(_DWORD *)(v32 + 16) != 0 )
              break;
            v33 = *(_DWORD **)(v22 + 128);
            v34 = v33 != nullptr ? *v33 : -1;
            v35 = v61;
            LODWORD(v62[0]) = v34;
            (*(void (__fastcall **)(unsigned __int64, _QWORD *, __int64))(*(_QWORD *)v61 + 40LL))(
              a1: v61,
              a2: v62,
              a3: 4);
            if ( *(_DWORD *)(v35 + 16) != 0 )
              break;
            sub_1407E3A70(a1: &v61, a2: v22 + 148);
            sub_1407E3A70(a1: &v61, a2: v22 + 152);
            sub_140FF4420(a1: v62, a2: &v61, a3: v22 + 80);
            if ( LODWORD(v62[0]) != 0 )
              break;
            sub_140FF4390(a1: v62, a2: &v61, a3: v22 + 32);
            if ( LODWORD(v62[0]) != 0 )
              break;
            sub_140FF4390(a1: v62, a2: &v61, a3: v22 + 56);
            if ( LODWORD(v62[0]) != 0 )
              break;
            sub_140FF47B0(a1: v62, a2: &v61, a3: v22 + 104);
            if ( LODWORD(v62[0]) != 0 )
              break;
            v15 = v61;
            v17 = *(_DWORD *)(v61 + 16);
            if ( v17 == 0 )
            {
              v36 = v20 == v19;
              v20 += 8;
              v21 = v26;
              if ( !v36 )
                continue;
            }
            goto LABEL_62;
          }
        }
      }
    }
    else
    {
      while ( 1 )
      {
        (*(void (__fastcall **)(volatile signed __int32 *, _QWORD, __int64))(*(_QWORD *)v11 + 40LL))(
          a1: v11,
          a2: *v13,
          a3: 4);
        if ( *((_DWORD *)v11 + 4) != 0 )
          break;
        v11 = (volatile signed __int32 *)v61;
        if ( *(_DWORD *)(v61 + 16) != 0 )
        {
LABEL_83:
          LODWORD(v15) = 0;
          v6 = v60;
          if ( _InterlockedDecrement(v11 + 2) != 0 )
            goto LABEL_66;
          goto LABEL_65;
        }
        if ( ++v13 == v14 )
          goto LABEL_32;
      }
    }
LABEL_63:
    v11 = (volatile signed __int32 *)v61;
    LODWORD(v15) = 0;
    v6 = v60;
    if ( v61 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v61 + 8)) == 0 )
LABEL_65:
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v11)(a1: v11, a2: 1);
  }
  else
  {
    LODWORD(v15) = 0;
  }
LABEL_66:
  if ( v6 != nullptr && _InterlockedDecrement(v6 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v6)(a1: v6, a2: 1);
  return (unsigned int)v15;
}
