__int64 __fastcall sub_140CD4430(unsigned __int64 a1, _QWORD *a2)
{
  __int64 v4; // r14
  __int64 v5; // rbx
  int v6; // r9d
  void (__fastcall ***v7)(_QWORD, __int64); // rcx
  __int64 v8; // rcx
  unsigned __int64 v9; // rsi
  __int64 v10; // rbx
  __int64 v11; // rsi
  __int64 v13; // rax
  __int64 v14; // rcx
  __int64 *v15; // r12
  __int64 v16; // rdx
  _QWORD *v17; // rbx
  _QWORD *v18; // rdx
  _QWORD *v19; // r13
  __int64 v20; // rsi
  __int64 v21; // rsi
  __int64 v22; // rsi
  __int64 v23; // rsi
  __int64 v24; // rsi
  int v25; // eax
  _QWORD *v26; // rcx
  _QWORD *v27; // rdi
  __int64 v28; // rbx
  __int64 v29; // rsi
  __int64 v30; // rsi
  __int64 v31; // rsi
  __int64 v32; // rsi
  __int64 v33; // rsi
  __int64 v34; // rsi
  __int64 v35; // rsi
  __int64 v36; // rsi
  __int64 v37; // rsi
  __int64 v38; // rsi
  __int64 v39; // rsi
  __int64 v40; // rsi
  __int64 v41; // rsi
  __int64 v42; // rsi
  __int64 v43; // rsi
  __int64 v44; // rsi
  __int64 v45; // rsi
  __int64 v46; // rsi
  __int64 v47; // rsi
  __int64 v48; // rsi
  __int64 v49; // rsi
  __int64 v50; // rsi
  __int64 v51; // rsi
  __int64 v52; // rsi
  __int64 v53; // rsi
  __int64 v54; // rsi
  __int64 v55; // rsi
  __int64 v56; // rsi
  __int64 v57; // rsi
  __int64 v58; // rsi
  __int64 v59; // rsi
  __int64 v60; // rsi
  __int64 v61; // rsi
  __int64 v62; // rsi
  __int64 v63; // rsi
  __int64 v64; // rsi
  __int64 v65; // rsi
  __int64 v66; // rsi
  __int64 v67; // rsi
  __int64 v68; // rsi
  __int64 v69; // rsi
  __int64 v70; // rsi
  __int64 v71; // rsi
  __int64 v72; // rsi
  _QWORD *v73; // rdi
  unsigned __int64 v74; // rbx
  __int64 v75; // rsi
  __int64 v76; // rbx
  _QWORD *v77; // rdi
  __int64 v78; // rax
  __int64 v79; // rsi
  __int64 v80; // rsi
  __int64 *v81; // r15
  __int64 v82; // rax
  unsigned __int64 v83; // r13
  __int64 *v84; // r12
  __int64 v85; // rsi
  __int64 v86; // rax
  unsigned __int64 v87; // r14
  __int64 v88; // rax
  int v89; // eax
  __int64 v90; // rsi
  __int64 v91; // rax
  __int64 v92; // rsi
  __int64 v93; // rsi
  void (__fastcall ***v94)(_QWORD, __int64); // rcx
  __int64 v95; // rax
  __int64 v96; // rcx
  unsigned __int64 v97; // rsi
  __int64 v98; // rdx
  _QWORD *v99; // rbx
  _QWORD *v100; // rdx
  __int64 v101; // r12
  __int64 v102; // rax
  __int64 v103; // rcx
  __int64 v104; // rbx
  __int64 *v105; // r14
  __int64 v106; // rdx
  unsigned __int64 v107; // r13
  __int64 v108; // rcx
  __int64 v109; // [rsp+30h] [rbp-50h] BYREF
  char v110[8]; // [rsp+38h] [rbp-48h] BYREF
  _QWORD *v111; // [rsp+40h] [rbp-40h]
  _QWORD *v112; // [rsp+48h] [rbp-38h]
  _QWORD *v113; // [rsp+50h] [rbp-30h]
  _QWORD *v114; // [rsp+58h] [rbp-28h]
  __int64 v115; // [rsp+60h] [rbp-20h] BYREF
  _QWORD *v116; // [rsp+68h] [rbp-18h]
  __int64 v117; // [rsp+70h] [rbp-10h]
  _QWORD *v118; // [rsp+78h] [rbp-8h]
  __int64 v119; // [rsp+80h] [rbp+0h] BYREF
  _QWORD v120[9]; // [rsp+88h] [rbp+8h] BYREF

  v120[1] = -2;
  v4 = qword_141B5AD60;
  sub_14080D0E0(a1: v110, a2: 0x1418E2C24LL);
  v5 = sub_1412EC810(a1: 264, a2: 8);
  *(_QWORD *)v5 = 0x800000000LL;
  strcpy((char *)(v5 + 8), "reserves");
  _InterlockedIncrement((volatile signed __int32 *)v5);
  v115 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v5);
  v115 = v5 + 4;
  v109 = 0x80100004E554C4CLL;
  if ( *a2 != 0
    && ((*(void (__fastcall **)(_QWORD, __int64 *, __int64 *, char *))(*(_QWORD *)*a2 + 224LL))(
          a1: *a2,
          a2: &v119,
          a3: &v115,
          a4: v110),
        v119 != 0) )
  {
    LOWORD(v6) = 3;
    sub_1407D1280(a1: (unsigned int)&v109, a2: (unsigned int)v120, a3: (unsigned int)&v119, a4: v6, a5: 0);
    v7 = (void (__fastcall ***)(_QWORD, __int64))v119;
    if ( v119 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v119 + 8)) == 0 )
      (**v7)(a1: v7, a2: 1);
  }
  else
  {
    v120[0] = 0;
  }
  v8 = v115;
  if ( v115 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v115 - 4)) == 0 )
    sub_1412EC9A0(a1: v8 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v5) == 0 )
    sub_1412EC9A0(a1: v5);
  if ( v120[0] == 0 )
  {
    LODWORD(a1) = 0;
    return (unsigned int)a1;
  }
  v9 = *(_QWORD *)(a1 + 8) - *(_QWORD *)a1;
  LODWORD(v119) = v9 >> 2;
  (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v120[0] + 40LL))(a1: v120[0], a2: &v119, a3: 4);
  v10 = v120[0];
  (*(void (__fastcall **)(_QWORD, _QWORD, unsigned __int64))(*(_QWORD *)v120[0] + 40LL))(
    a1: v120[0],
    a2: *(_QWORD *)a1,
    a3: v9);
  if ( *(_DWORD *)(v10 + 16) != 0 )
  {
LABEL_14:
    LODWORD(a1) = 0;
LABEL_15:
    v11 = v120[0];
    if ( v120[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v120[0] + 8LL)) == 0 )
      goto LABEL_17;
    return (unsigned int)a1;
  }
  v13 = *(_QWORD *)(v4 + 16);
  v14 = *(_QWORD *)(v4 + 24);
  if ( v14 == v13 )
  {
LABEL_120:
    v94 = (void (__fastcall ***)(_QWORD, __int64))v120[0];
    if ( v120[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v120[0] + 8LL)) == 0 )
      (**v94)(a1: v94, a2: 1);
    v120[0] = 0;
    v95 = *(_QWORD *)(v4 + 16);
    v96 = *(_QWORD *)(v4 + 24);
    if ( v96 == v95 )
    {
      LOBYTE(a1) = 1;
      return (unsigned int)a1;
    }
    v97 = 0;
    do
    {
      v98 = *(_QWORD *)(v95 + 8 * v97);
      if ( *(_QWORD *)(v98 + 24) != 0 && *(_BYTE *)(v98 + 68) != 0 )
      {
        v99 = *(_QWORD **)(v98 + 632);
        v100 = *(_QWORD **)(v98 + 640);
        if ( v99 != v100 )
        {
          v116 = v100;
          v117 = v4;
          while ( 2 )
          {
            v118 = v99;
            v101 = *(_QWORD *)(*(_QWORD *)(*v99 + 440LL) + 56LL);
            a1 = 0;
            do
            {
              if ( *(_QWORD *)(v101 + 8 * a1) != 0 )
              {
                v102 = *(_QWORD *)(v101 + 128);
                v103 = *(_QWORD *)(v101 + 136);
                if ( v103 != v102 )
                {
                  v104 = 0;
                  while ( 1 )
                  {
                    v105 = *(__int64 **)(v102 + 8 * v104);
                    if ( a1 == *((unsigned __int8 *)v105 + 228) )
                    {
                      v106 = *v105;
                      if ( v105[1] != *v105 )
                        break;
                    }
LABEL_134:
                    if ( ++v104 >= (unsigned __int64)((v103 - v102) >> 3) )
                      goto LABEL_141;
                  }
                  v107 = 0;
                  while ( (unsigned __int8)sub_14096EA70(a1: *(_QWORD *)(v106 + 8 * v107), a2) != 0 )
                  {
                    ++v107;
                    v106 = *v105;
                    if ( v107 >= (v105[1] - *v105) >> 3 )
                    {
                      v102 = *(_QWORD *)(v101 + 128);
                      v103 = *(_QWORD *)(v101 + 136);
                      goto LABEL_134;
                    }
                  }
                  goto LABEL_14;
                }
              }
LABEL_141:
              v108 = *(_QWORD *)(v101 + 8 * a1 + 64);
              if ( v108 != 0 && (unsigned __int8)sub_14096EA70(a1: v108, a2) == 0 )
                goto LABEL_14;
              ++a1;
            }
            while ( a1 != 8 );
            v99 = v118 + 1;
            if ( v118 + 1 != v116 )
              continue;
            break;
          }
          v4 = v117;
          v95 = *(_QWORD *)(v117 + 16);
          v96 = *(_QWORD *)(v117 + 24);
        }
      }
      ++v97;
      LOBYTE(a1) = 1;
    }
    while ( v97 < (v96 - v95) >> 3 );
    goto LABEL_15;
  }
  a1 = 0;
  v15 = &v119;
  while ( 1 )
  {
    v16 = *(_QWORD *)(v13 + 8 * a1);
    if ( *(_QWORD *)(v16 + 24) != 0 && *(_BYTE *)(v16 + 68) != 0 )
    {
      v17 = *(_QWORD **)(v16 + 632);
      v18 = *(_QWORD **)(v16 + 640);
      if ( v17 != v18 )
        break;
    }
LABEL_22:
    if ( ++a1 >= (v14 - v13) >> 3 )
      goto LABEL_120;
  }
  v111 = (_QWORD *)a1;
  v116 = v18;
  while ( 2 )
  {
    v19 = *(_QWORD **)(*(_QWORD *)(*v17 + 440LL) + 56LL);
    v20 = v120[0];
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
      a1: v120[0],
      a2: (__int64)v19 + 228,
      a3: 2);
    if ( *(_DWORD *)(v20 + 16) != 0 )
      goto LABEL_14;
    v21 = v120[0];
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
      a1: v120[0],
      a2: (__int64)v19 + 239,
      a3: 1);
    if ( *(_DWORD *)(v21 + 16) != 0 )
      goto LABEL_14;
    v22 = v120[0];
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)v120[0] + 40LL))(a1: v120[0], a2: v19 + 30, a3: 1);
    if ( *(_DWORD *)(v22 + 16) != 0 )
      goto LABEL_14;
    v23 = v120[0];
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)v120[0] + 40LL))(a1: v120[0], a2: v19 + 28, a3: 2);
    if ( *(_DWORD *)(v23 + 16) != 0 )
      goto LABEL_14;
    v24 = v120[0];
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
      a1: v120[0],
      a2: (__int64)v19 + 226,
      a3: 2);
    if ( *(_DWORD *)(v24 + 16) != 0 )
      goto LABEL_14;
    v113 = v17;
    LODWORD(v119) = (v19[17] - v19[16]) >> 3;
    (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v120[0] + 40LL))(a1: v120[0], a2: v15, a3: 4);
    v11 = v120[0];
    v25 = *(_DWORD *)(v120[0] + 16LL);
    v118 = v19;
    if ( v25 == 0 )
    {
      v26 = (_QWORD *)v19[16];
      if ( v26 != (_QWORD *)v19[17] )
      {
        v114 = (_QWORD *)v19[17];
        while ( 1 )
        {
          v27 = v26;
          v28 = *v26;
          (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v11 + 40LL))(a1: v11, a2: *v26 + 184LL, a3: 1);
          if ( *(_DWORD *)(v11 + 16) != 0 )
            goto LABEL_14;
          v29 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 185,
            a3: 1);
          if ( *(_DWORD *)(v29 + 16) != 0 )
            goto LABEL_14;
          v30 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 186,
            a3: 1);
          if ( *(_DWORD *)(v30 + 16) != 0 )
            goto LABEL_14;
          v31 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 187,
            a3: 1);
          if ( *(_DWORD *)(v31 + 16) != 0 )
            goto LABEL_14;
          v32 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 188,
            a3: 1);
          if ( *(_DWORD *)(v32 + 16) != 0 )
            goto LABEL_14;
          v33 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 189,
            a3: 1);
          if ( *(_DWORD *)(v33 + 16) != 0 )
            goto LABEL_14;
          v34 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 190,
            a3: 2);
          if ( *(_DWORD *)(v34 + 16) != 0 )
            goto LABEL_14;
          v35 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 196,
            a3: 1);
          if ( *(_DWORD *)(v35 + 16) != 0 )
            goto LABEL_14;
          v36 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 197,
            a3: 1);
          if ( *(_DWORD *)(v36 + 16) != 0 )
            goto LABEL_14;
          v37 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 198,
            a3: 1);
          if ( *(_DWORD *)(v37 + 16) != 0 )
            goto LABEL_14;
          v38 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 199,
            a3: 1);
          if ( *(_DWORD *)(v38 + 16) != 0 )
            goto LABEL_14;
          v39 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 200,
            a3: 1);
          if ( *(_DWORD *)(v39 + 16) != 0 )
            goto LABEL_14;
          v40 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 228,
            a3: 1);
          if ( *(_DWORD *)(v40 + 16) != 0 )
            goto LABEL_14;
          v41 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 229,
            a3: 1);
          if ( *(_DWORD *)(v41 + 16) != 0 )
            goto LABEL_14;
          v42 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 230,
            a3: 1);
          if ( *(_DWORD *)(v42 + 16) != 0 )
            goto LABEL_14;
          v43 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 220,
            a3: 4);
          if ( *(_DWORD *)(v43 + 16) != 0 )
            goto LABEL_14;
          v44 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 224,
            a3: 4);
          if ( *(_DWORD *)(v44 + 16) != 0 )
            goto LABEL_14;
          v45 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 231,
            a3: 1);
          if ( *(_DWORD *)(v45 + 16) != 0 )
            goto LABEL_14;
          v46 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 232,
            a3: 1);
          if ( *(_DWORD *)(v46 + 16) != 0 )
            goto LABEL_14;
          v47 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 233,
            a3: 1);
          if ( *(_DWORD *)(v47 + 16) != 0 )
            goto LABEL_14;
          v48 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 234,
            a3: 1);
          if ( *(_DWORD *)(v48 + 16) != 0 )
            goto LABEL_14;
          v49 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 235,
            a3: 1);
          if ( *(_DWORD *)(v49 + 16) != 0 )
            goto LABEL_14;
          v50 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 236,
            a3: 2);
          if ( *(_DWORD *)(v50 + 16) != 0 )
            goto LABEL_14;
          v51 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 238,
            a3: 1);
          if ( *(_DWORD *)(v51 + 16) != 0 )
            goto LABEL_14;
          v52 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 239,
            a3: 1);
          if ( *(_DWORD *)(v52 + 16) != 0 )
            goto LABEL_14;
          v53 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 240,
            a3: 1);
          if ( *(_DWORD *)(v53 + 16) != 0 )
            goto LABEL_14;
          v54 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 241,
            a3: 1);
          if ( *(_DWORD *)(v54 + 16) != 0 )
            goto LABEL_14;
          v55 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 242,
            a3: 1);
          if ( *(_DWORD *)(v55 + 16) != 0 )
            goto LABEL_14;
          v56 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 244,
            a3: 1);
          if ( *(_DWORD *)(v56 + 16) != 0 )
            goto LABEL_14;
          v57 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 246,
            a3: 2);
          if ( *(_DWORD *)(v57 + 16) != 0 )
            goto LABEL_14;
          v58 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 248,
            a3: 2);
          if ( *(_DWORD *)(v58 + 16) != 0 )
            goto LABEL_14;
          v59 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 250,
            a3: 1);
          if ( *(_DWORD *)(v59 + 16) != 0 )
            goto LABEL_14;
          v60 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 251,
            a3: 1);
          if ( *(_DWORD *)(v60 + 16) != 0 )
            goto LABEL_14;
          v61 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 245,
            a3: 1);
          if ( *(_DWORD *)(v61 + 16) != 0 )
            goto LABEL_14;
          sub_1409C6F60(a1: v15, a2: v120, a3: v28 + 144);
          if ( (_DWORD)v119 != 0 )
            goto LABEL_14;
          sub_140CD5EC0(a1: v15, a2: v120, a3: v28 + 24);
          if ( (_DWORD)v119 != 0 )
            goto LABEL_14;
          sub_1409701F0(a1: v15, a2: v120, a3: v28 + 48);
          if ( (_DWORD)v119 != 0 )
            goto LABEL_14;
          sub_1409701F0(a1: v15, a2: v120, a3: v28 + 72);
          if ( (_DWORD)v119 != 0 )
            goto LABEL_14;
          sub_1409701F0(a1: v15, a2: v120, a3: v28 + 96);
          if ( (_DWORD)v119 != 0 )
            goto LABEL_14;
          v62 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 252,
            a3: 1);
          if ( *(_DWORD *)(v62 + 16) != 0 )
            goto LABEL_14;
          v63 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 243,
            a3: 1);
          if ( *(_DWORD *)(v63 + 16) != 0 )
            goto LABEL_14;
          v64 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 254,
            a3: 1);
          if ( *(_DWORD *)(v64 + 16) != 0 )
            goto LABEL_14;
          v65 = v120[0];
          LOBYTE(v119) = *(_BYTE *)(v28 + 255);
          (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v120[0] + 40LL))(a1: v120[0], a2: v15, a3: 1);
          if ( *(_DWORD *)(v65 + 16) != 0 )
            goto LABEL_14;
          v66 = v120[0];
          LOBYTE(v119) = *(_BYTE *)(v28 + 201);
          (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v120[0] + 40LL))(a1: v120[0], a2: v15, a3: 1);
          if ( *(_DWORD *)(v66 + 16) != 0 )
            goto LABEL_14;
          v67 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 202,
            a3: 1);
          if ( *(_DWORD *)(v67 + 16) != 0 )
            goto LABEL_14;
          v68 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 253,
            a3: 1);
          if ( *(_DWORD *)(v68 + 16) != 0 )
            goto LABEL_14;
          if ( (unsigned __int8)sub_140F80810(
                                  a1: *(_QWORD *)(v28 + 168),
                                  a2: v120,
                                  a3: (unsigned __int8)byte_141B5FC2C ^ 1u) == 0 )
            goto LABEL_14;
          if ( (unsigned __int8)sub_140F80810(
                                  a1: *(_QWORD *)(v28 + 176),
                                  a2: v120,
                                  a3: (unsigned __int8)byte_141B5FC2C ^ 1u) == 0 )
            goto LABEL_14;
          v69 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 204,
            a3: 4);
          if ( *(_DWORD *)(v69 + 16) != 0 )
            goto LABEL_14;
          v70 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 208,
            a3: 4);
          if ( *(_DWORD *)(v70 + 16) != 0 )
            goto LABEL_14;
          v71 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 212,
            a3: 4);
          if ( *(_DWORD *)(v71 + 16) != 0 )
            goto LABEL_14;
          v72 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v28 + 216,
            a3: 4);
          if ( *(_DWORD *)(v72 + 16) != 0 )
            goto LABEL_14;
          v11 = v120[0];
          if ( *(_DWORD *)(v120[0] + 16LL) != 0 )
            goto LABEL_147;
          v26 = v27 + 1;
          if ( v27 + 1 == v114 )
            goto LABEL_91;
        }
      }
    }
    if ( v25 != 0 )
      goto LABEL_14;
LABEL_91:
    v73 = v118;
    v74 = v118[20] - v118[19];
    LODWORD(v119) = v74 >> 2;
    (*(void (__fastcall **)(__int64, __int64 *, __int64))(*(_QWORD *)v11 + 40LL))(a1: v11, a2: v15, a3: 4);
    v75 = v120[0];
    (*(void (__fastcall **)(_QWORD, _QWORD, unsigned __int64))(*(_QWORD *)v120[0] + 40LL))(
      a1: v120[0],
      a2: v73[19],
      a3: v74);
    if ( *(_DWORD *)(v75 + 16) != 0 )
      goto LABEL_14;
    sub_1409701F0(a1: v15, a2: v120, a3: v73 + 22);
    if ( (_DWORD)v119 != 0 )
      goto LABEL_14;
    v11 = v120[0];
    if ( *(_DWORD *)(v120[0] + 16LL) == 0 )
    {
      v76 = 0;
      v117 = v4;
      v112 = a2;
      do
      {
        v77 = v118;
        v78 = v118[v76];
        v79 = v120[0];
        if ( v78 != 0 )
        {
          LODWORD(v119) = *(_DWORD *)(*(_QWORD *)(v78 + 288) + 8LL);
          (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v120[0] + 40LL))(a1: v120[0], a2: v15, a3: 4);
          if ( *(_DWORD *)(v79 + 16) != 0 )
            goto LABEL_14;
          v80 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v77[v76] + 1640LL,
            a3: 1);
          if ( *(_DWORD *)(v80 + 16) != 0 )
            goto LABEL_14;
          v81 = v15;
          v82 = v77[16];
          if ( v77[17] != v82 )
          {
            v83 = 0;
            while ( 1 )
            {
              v84 = *(__int64 **)(v82 + 8 * v83);
              if ( v76 == *((unsigned __int8 *)v84 + 228) )
              {
                v85 = v120[0];
                LODWORD(v119) = (unsigned __int64)(v84[1] - *v84) >> 3;
                (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v120[0] + 40LL))(
                  a1: v120[0],
                  a2: v81,
                  a3: 4);
                if ( *(_DWORD *)(v85 + 16) != 0 )
                  goto LABEL_14;
                v86 = *v84;
                if ( v84[1] != *v84 )
                  break;
              }
LABEL_100:
              ++v83;
              v82 = v118[16];
              if ( v83 >= (v118[17] - v82) >> 3 )
                goto LABEL_112;
            }
            v87 = 0;
            while ( 1 )
            {
              v88 = *(_QWORD *)(*(_QWORD *)(v86 + 8 * v87) + 288LL);
              v89 = v88 != 0 ? *(_DWORD *)(v88 + 12) : -1;
              v90 = v120[0];
              LODWORD(v119) = v89;
              (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v120[0] + 40LL))(
                a1: v120[0],
                a2: v81,
                a3: 4);
              if ( *(_DWORD *)(v90 + 16) != 0 )
                goto LABEL_14;
              ++v87;
              v86 = *v84;
              if ( v87 >= (v84[1] - *v84) >> 3 )
                goto LABEL_100;
            }
          }
        }
        else
        {
          LODWORD(v119) = -1;
          v81 = v15;
          (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v120[0] + 40LL))(a1: v120[0], a2: v15, a3: 4);
          if ( *(_DWORD *)(v79 + 16) != 0 )
            goto LABEL_14;
        }
LABEL_112:
        v91 = v118[v76 + 8];
        v92 = v120[0];
        if ( v91 != 0 )
        {
          LODWORD(v119) = *(_DWORD *)(*(_QWORD *)(v91 + 288) + 8LL);
          v15 = v81;
          (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v120[0] + 40LL))(a1: v120[0], a2: v81, a3: 4);
          v4 = v117;
          if ( *(_DWORD *)(v92 + 16) != 0 )
            goto LABEL_14;
          v93 = v120[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v120[0] + 40LL))(
            a1: v120[0],
            a2: v118[v76 + 8] + 1640LL,
            a3: 1);
          if ( *(_DWORD *)(v93 + 16) != 0 )
            goto LABEL_14;
        }
        else
        {
          LODWORD(v119) = -1;
          v15 = v81;
          (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v120[0] + 40LL))(a1: v120[0], a2: v81, a3: 4);
          v4 = v117;
          if ( *(_DWORD *)(v92 + 16) != 0 )
            goto LABEL_14;
        }
        ++v76;
        a2 = v112;
      }
      while ( v76 != 8 );
      v17 = v113 + 1;
      if ( v113 + 1 != v116 )
        continue;
      v13 = *(_QWORD *)(v4 + 16);
      v14 = *(_QWORD *)(v4 + 24);
      a1 = (unsigned __int64)v111;
      goto LABEL_22;
    }
    break;
  }
LABEL_147:
  LODWORD(a1) = 0;
  if ( _InterlockedDecrement((volatile signed __int32 *)(v11 + 8)) != 0 )
    return (unsigned int)a1;
LABEL_17:
  (**(void (__fastcall ***)(__int64, __int64))v11)(a1: v11, a2: 1);
  return (unsigned int)a1;
}
