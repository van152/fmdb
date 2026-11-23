__int64 __fastcall sub_141585E80(__int64 a1, _QWORD *a2, char a3, unsigned int a4)
{
  __int64 v4; // rbp
  __int64 v8; // rsi
  _DWORD *v9; // rbp
  __int64 v10; // rbx
  __int64 v11; // rbx
  _DWORD *v12; // rdi
  __int64 v13; // rdx
  __int64 v14; // rax
  int v15; // eax
  __int64 v16; // rcx
  _DWORD *v17; // rbp
  __int64 v18; // rax
  _QWORD *v19; // rdx
  __int64 v20; // r8
  _DWORD *v21; // rbp
  __int64 v22; // rbp
  __int64 v23; // rbp
  __int64 v24; // rbp
  __int64 v25; // rbp
  __int64 v26; // rbp
  __int64 v27; // rbp
  __int64 v28; // rbp
  __int64 v29; // rbp
  __int64 v30; // rbp
  __int64 v31; // rbp
  __int64 v32; // rbp
  _DWORD *v33; // rbp
  __int64 v34; // r13
  _DWORD *v35; // rbp
  __int64 v36; // r15
  unsigned __int64 v37; // rcx
  unsigned __int64 v38; // rax
  _QWORD *v39; // r14
  __int64 v40; // rbp
  __int64 v41; // rbp
  __int64 v42; // rbp
  __int64 v43; // rbp
  __int64 v44; // rbp
  __int64 v45; // rbp
  __int64 v46; // rbp
  __int64 v47; // rbp
  __int64 v48; // rbp
  __int64 v49; // rbp
  int v50; // eax
  _DWORD *v51; // rbp
  __int64 v52; // rax
  int v53; // eax
  _DWORD *v54; // rbp
  unsigned __int64 v56; // r14
  __int64 v57; // rbp
  unsigned __int64 v58; // r14
  __int64 v59; // rbp
  __int64 v60; // rbp
  __int64 v61; // rbp
  __int64 v62; // [rsp+20h] [rbp-58h] BYREF
  int v63; // [rsp+2Ch] [rbp-4Ch] BYREF
  __int64 v64; // [rsp+30h] [rbp-48h]

  v8 = a1 + -*(_DWORD *)(a1 - 4);
  if ( a3 == 0 )
  {
    LOBYTE(v4) = 1;
    if ( (_BYTE)a4 == 0 )
      return (unsigned int)v4;
    goto LABEL_11;
  }
  v9 = (_DWORD *)*a2;
  LOBYTE(v62) = 4;
  (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v9 + 40LL))(a1: v9, a2: &v62, a3: 1);
  if ( v9[4] != 0 )
    goto LABEL_60;
  if ( (_BYTE)a4 != 0 )
  {
LABEL_11:
    v14 = *(_QWORD *)(v8 - 200);
    if ( v14 != 0 )
    {
      v15 = *(_DWORD *)(v14 + 8);
      v16 = v15;
    }
    else
    {
      v15 = -1;
      v16 = -1;
    }
    v62 = v16;
    v17 = (_DWORD *)*a2;
    if ( BYTE5(qword_141B6034C) == 0 || byte_141B5FC2C != 0 )
    {
      v63 = v15;
      v18 = *(_QWORD *)v17;
      v19 = &v63;
      v20 = 4;
    }
    else
    {
      v18 = *(_QWORD *)v17;
      v19 = &v62;
      v20 = 8;
    }
    (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(v18 + 40))(a1: v17, a2: v19, a3: v20);
    if ( v17[4] == 0 )
    {
      v21 = (_DWORD *)*a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v8 - 28, a3: 2);
      if ( v21[4] == 0 )
      {
        v22 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v8 - 26, a3: 2);
        if ( *(_DWORD *)(v22 + 16) == 0 )
        {
          v23 = *a2;
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v8 - 24, a3: 2);
          if ( *(_DWORD *)(v23 + 16) == 0 )
          {
            v24 = *a2;
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v8 - 22, a3: 1);
            if ( *(_DWORD *)(v24 + 16) == 0 )
            {
              v25 = *a2;
              (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v8 - 21, a3: 1);
              if ( *(_DWORD *)(v25 + 16) == 0 )
              {
                v26 = *a2;
                (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v8 - 20, a3: 1);
                if ( *(_DWORD *)(v26 + 16) == 0 )
                {
                  v27 = *a2;
                  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                    a1: *a2,
                    a2: v8 - 19,
                    a3: 1);
                  if ( *(_DWORD *)(v27 + 16) == 0 )
                  {
                    v28 = *a2;
                    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                      a1: *a2,
                      a2: v8 - 18,
                      a3: 1);
                    if ( *(_DWORD *)(v28 + 16) == 0 )
                    {
                      v29 = *a2;
                      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                        a1: *a2,
                        a2: v8 - 17,
                        a3: 1);
                      if ( *(_DWORD *)(v29 + 16) == 0 )
                      {
                        v30 = *a2;
                        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                          a1: *a2,
                          a2: v8 - 16,
                          a3: 1);
                        if ( *(_DWORD *)(v30 + 16) == 0 )
                        {
                          v31 = *a2;
                          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                            a1: *a2,
                            a2: v8 - 15,
                            a3: 1);
                          if ( *(_DWORD *)(v31 + 16) == 0 )
                          {
                            v32 = *a2;
                            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                              a1: *a2,
                              a2: v8 - 14,
                              a3: 1);
                            if ( *(_DWORD *)(v32 + 16) == 0 )
                            {
                              v33 = (_DWORD *)*a2;
                              LOBYTE(v62) = *(_BYTE *)(v8 - 128);
                              (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v33 + 40LL))(
                                a1: v33,
                                a2: &v62,
                                a3: 1);
                              if ( v33[4] == 0 )
                              {
                                v34 = v8 - 128;
                                v64 = *(unsigned __int8 *)(v8 - 128);
                                if ( v64 != 0 )
                                {
                                  v35 = (_DWORD *)*a2;
                                  v36 = 0;
                                  while ( 1 )
                                  {
                                    v37 = v36 + *(unsigned __int8 *)(v34 + 88);
                                    v38 = v37 - 10;
                                    if ( v37 < 0xA )
                                      v38 = v36 + *(unsigned __int8 *)(v34 + 88);
                                    v39 = *(_QWORD **)(v34 + 8 * v38 + 8);
                                    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v35 + 40LL))(
                                      a1: v35,
                                      a2: 0x1418C0DE8LL,
                                      a3: 1);
                                    if ( v35[4] != 0 )
                                      break;
                                    v40 = *a2;
                                    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(
                                      a1: *a2,
                                      a2: v39 + 3,
                                      a3: 1);
                                    if ( *(_DWORD *)(v40 + 16) != 0 )
                                      break;
                                    v41 = *a2;
                                    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                                      a1: *a2,
                                      a2: (__int64)v39 + 25,
                                      a3: 1);
                                    if ( *(_DWORD *)(v41 + 16) != 0 )
                                      break;
                                    v42 = *a2;
                                    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                                      a1: *a2,
                                      a2: (__int64)v39 + 26,
                                      a3: 1);
                                    if ( *(_DWORD *)(v42 + 16) != 0 )
                                      break;
                                    v43 = *a2;
                                    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                                      a1: *a2,
                                      a2: (__int64)v39 + 20,
                                      a3: 2);
                                    if ( *(_DWORD *)(v43 + 16) != 0 )
                                      break;
                                    v44 = *a2;
                                    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                                      a1: *a2,
                                      a2: (__int64)v39 + 22,
                                      a3: 2);
                                    if ( *(_DWORD *)(v44 + 16) != 0 )
                                      break;
                                    v45 = *a2;
                                    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                                      a1: *a2,
                                      a2: (__int64)v39 + 27,
                                      a3: 1);
                                    if ( *(_DWORD *)(v45 + 16) != 0 )
                                      break;
                                    v46 = *a2;
                                    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                                      a1: *a2,
                                      a2: (__int64)v39 + 28,
                                      a3: 1);
                                    if ( *(_DWORD *)(v46 + 16) != 0 )
                                      break;
                                    v47 = *a2;
                                    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(
                                      a1: *a2,
                                      a2: v39 + 2,
                                      a3: 4);
                                    if ( *(_DWORD *)(v47 + 16) != 0 )
                                      break;
                                    v48 = *a2;
                                    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                                      a1: *a2,
                                      a2: (__int64)v39 + 29,
                                      a3: 1);
                                    if ( *(_DWORD *)(v48 + 16) != 0 )
                                      break;
                                    v49 = *a2;
                                    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                                      a1: *a2,
                                      a2: (__int64)v39 + 30,
                                      a3: 1);
                                    if ( *(_DWORD *)(v49 + 16) != 0 )
                                      break;
                                    v50 = *v39 != 0 ? *(_DWORD *)(*v39 + 8LL) : -1;
                                    v51 = (_DWORD *)*a2;
                                    LODWORD(v62) = v50;
                                    (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v51 + 40LL))(
                                      a1: v51,
                                      a2: &v62,
                                      a3: 4);
                                    if ( v51[4] != 0 )
                                      break;
                                    v52 = v39[1];
                                    v53 = v52 != 0 ? *(_DWORD *)(v52 + 8) : -1;
                                    v54 = (_DWORD *)*a2;
                                    LODWORD(v62) = v53;
                                    (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v54 + 40LL))(
                                      a1: v54,
                                      a2: &v62,
                                      a3: 4);
                                    if ( v54[4] != 0 )
                                      break;
                                    v35 = (_DWORD *)*a2;
                                    if ( *(_DWORD *)(*a2 + 16LL) != 0 )
                                      break;
                                    if ( v64 == ++v36 )
                                      goto LABEL_64;
                                  }
                                }
                                else
                                {
                                  v35 = (_DWORD *)*a2;
LABEL_64:
                                  v56 = *(_QWORD *)(v8 - 168) - *(_QWORD *)(v8 - 176);
                                  LODWORD(v62) = v56 >> 2;
                                  (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v35 + 40LL))(
                                    a1: v35,
                                    a2: &v62,
                                    a3: 4);
                                  v57 = *a2;
                                  (*(void (__fastcall **)(_QWORD, _QWORD, unsigned __int64))(*(_QWORD *)*a2 + 40LL))(
                                    a1: *a2,
                                    a2: *(_QWORD *)(v8 - 176),
                                    a3: v56);
                                  if ( *(_DWORD *)(v57 + 16) == 0 )
                                  {
                                    v58 = *(_QWORD *)(v8 - 144) - *(_QWORD *)(v8 - 152);
                                    LODWORD(v62) = v58 >> 2;
                                    (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*a2 + 40LL))(
                                      a1: *a2,
                                      a2: &v62,
                                      a3: 4);
                                    v59 = *a2;
                                    (*(void (__fastcall **)(_QWORD, _QWORD, unsigned __int64))(*(_QWORD *)*a2 + 40LL))(
                                      a1: *a2,
                                      a2: *(_QWORD *)(v8 - 152),
                                      a3: v58);
                                    if ( *(_DWORD *)(v59 + 16) == 0 )
                                    {
                                      v60 = *a2;
                                      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                                        a1: *a2,
                                        a2: v8 - 32,
                                        a3: 2);
                                      if ( *(_DWORD *)(v60 + 16) == 0 )
                                      {
                                        v61 = *a2;
                                        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                                          a1: *a2,
                                          a2: v8 - 32 + 2,
                                          a3: 2);
                                        if ( *(_DWORD *)(v61 + 16) == 0 )
                                        {
                                          v4 = *a2;
                                          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
                                            a1: *a2,
                                            a2: v8 - 13,
                                            a3: 1);
                                          LOBYTE(v4) = *(_DWORD *)(v4 + 16) == 0;
                                          if ( !(_BYTE)v4 || a3 == 0 )
                                            return (unsigned int)v4;
                                          goto LABEL_4;
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
LABEL_60:
    LODWORD(v4) = 0;
    return (unsigned int)v4;
  }
LABEL_4:
  LODWORD(v4) = 0;
  if ( (unsigned __int8)sub_140DFC460(a1: v8 - 192, a2, a3: 0, a4) != 0 )
  {
    v10 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v8 + 24, a3: 8);
    if ( *(_DWORD *)(v10 + 16) == 0 )
    {
      v11 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v8 + 8, a3: 4);
      if ( *(_DWORD *)(v11 + 16) == 0 )
      {
        v4 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v8 + 12, a3: 4);
        if ( *(_DWORD *)(v4 + 16) == 0 )
        {
          v12 = (_DWORD *)*a2;
          v13 = *(_DWORD *)(v8 + 16) != 0 ? v8 + 16 : v8 + 12;
          (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v12 + 40LL))(a1: v12, a2: v13, a3: 4);
          if ( v12[4] == 0 )
          {
            LOBYTE(v4) = 1;
            return (unsigned int)v4;
          }
        }
      }
    }
    goto LABEL_60;
  }
  return (unsigned int)v4;
}
