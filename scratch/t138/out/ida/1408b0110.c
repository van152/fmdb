__int64 __fastcall sub_1408B0110(
        __int64 a1,
        unsigned __int8 a2,
        unsigned int a3,
        volatile signed __int32 **a4,
        __int64 *a5,
        volatile signed __int32 **a6)
{
  __int64 *v8; // rax
  __int64 *v9; // rdx
  __int64 *v10; // rcx
  __int64 *v11; // rsi
  void (__fastcall ***v12)(_QWORD, __int64); // rcx
  __int64 v13; // rsi
  __int64 v14; // rdx
  __int64 v15; // rcx
  __int64 v16; // r14
  bool v17; // al
  __int64 v18; // rax
  __int64 v19; // rcx
  volatile signed __int32 *v20; // rax
  __int64 v21; // rcx
  volatile signed __int32 *v22; // rax
  __int64 v23; // rcx
  __int64 v24; // rax
  volatile signed __int32 *v25; // rcx
  __int64 v26; // rsi
  __int64 v27; // rdi
  __int64 v28; // r8
  volatile signed __int32 *v29; // rcx
  __int64 v30; // rcx
  int *v31; // rsi
  __int64 v32; // rsi
  __int64 v33; // rdi
  __int64 v34; // rcx
  __int64 v35; // r8
  __int64 v36; // rcx
  __int64 v37; // rcx
  __int64 v38; // rsi
  __int64 v39; // rdi
  __int64 v40; // rcx
  __int64 v41; // r8
  __int64 v42; // rcx
  __int64 v43; // rcx
  void (__fastcall ***v44)(_QWORD, __int64); // rcx
  __int64 v45; // rcx
  void (__fastcall ***v46)(_QWORD, __int64); // rcx
  __int64 v48; // rax
  __int64 v49; // rcx
  __int64 v50; // rbx
  __int64 v51; // rcx
  __int64 v52; // rsi
  __int64 v53; // rdi
  __int64 v54; // r8
  volatile signed __int32 *v55; // rcx
  __int64 v56; // rcx
  void (__fastcall ***v57)(_QWORD, __int64); // rcx
  void (__fastcall ***v58)(_QWORD, __int64); // rcx
  void (__fastcall ***v59)(_QWORD, __int64); // rcx
  __int64 *v61; // r14
  __int64 v62; // rbp
  __int64 v63; // r15
  __int64 v64; // r13
  __int64 v65; // r12
  __int64 *v66; // rdi
  unsigned __int64 v67; // rcx
  __int64 v68; // r8
  __int64 v69; // r14
  bool v70; // al
  unsigned __int64 v71; // rdi
  _DWORD *v72; // rbp
  __int64 v73; // rsi
  unsigned __int64 v74; // rax
  unsigned __int64 v75; // r12
  unsigned __int64 v76; // r13
  unsigned __int64 v77; // rcx
  unsigned __int64 v78; // r13
  __int64 v79; // r15
  __int64 v80; // rdx
  _DWORD *v81; // r14
  bool v82; // zf
  __int64 v83; // rsi
  unsigned __int64 v84; // rcx
  __int64 v85; // rbp
  __int64 v86; // rbp
  bool v87; // al
  void (__fastcall ***v88)(_QWORD, __int64); // rcx
  __int64 v89; // rcx
  __int64 v90; // [rsp+38h] [rbp-A0h]
  __int64 v91; // [rsp+40h] [rbp-98h] BYREF
  unsigned __int8 v92; // [rsp+4Fh] [rbp-89h]
  __int64 v93; // [rsp+50h] [rbp-88h] BYREF
  __int64 v94; // [rsp+58h] [rbp-80h] BYREF
  __int64 v95; // [rsp+60h] [rbp-78h] BYREF
  __int64 v96; // [rsp+68h] [rbp-70h] BYREF
  int v97; // [rsp+70h] [rbp-68h] BYREF
  __int64 v98; // [rsp+78h] [rbp-60h] BYREF
  __int64 v99; // [rsp+80h] [rbp-58h] BYREF
  __int64 v100; // [rsp+88h] [rbp-50h] BYREF
  __int64 v101; // [rsp+90h] [rbp-48h]

  v92 = a2;
  v101 = a1;
  v91 = 0;
  v8 = **(__int64 ***)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
  v9 = (__int64 *)v8[1];
  v10 = v8;
  if ( *((_BYTE *)v9 + 25) == 0 )
  {
    v10 = **(__int64 ***)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
    do
    {
      v11 = v9 + 2;
      if ( v9[4] >= (unsigned __int64)qword_141B5ACC0 )
      {
        v10 = v9;
        v11 = v9;
      }
      v9 = (__int64 *)*v11;
    }
    while ( *(_BYTE *)(*v11 + 25) == 0 );
  }
  if ( *((_BYTE *)v10 + 25) != 0 || qword_141B5ACC0 < (unsigned __int64)v10[4] || v10 == v8 )
  {
    v96 = 0;
  }
  else
  {
    v18 = v10[5];
    v96 = v18;
    if ( v18 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v18 + 8));
  }
  sub_1407C3450(a1: &v100, a2: &v96, a3: &v91);
  v12 = (void (__fastcall ***)(_QWORD, __int64))v96;
  if ( v96 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v96 + 8)) == 0 )
    (**v12)(a1: v12, a2: 1);
  v13 = v91;
  if ( v91 != 0 && _InterlockedDecrement((volatile signed __int32 *)v91) == 0 )
  {
    sub_1408B5D70(a1: *(_QWORD *)(*(_QWORD *)(v13 + 8) + 8LL));
    v14 = *(_QWORD *)(v13 + 8);
    if ( v14 != 0 )
    {
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v15 = *(_QWORD *)(qword_141ABD470 + 24), (unsigned __int64)(*(_QWORD *)(qword_141ABD470 + 32) - v15) >= 0x181)
        && (v16 = *(_QWORD *)(v15 + 384)) != 0 )
      {
        MEMORY[0x1419475D8](a1: v16 + 32, a2: v14 - *(unsigned int *)(v16 + 120));
        v17 = *(_BYTE *)(v16 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v16 + 64)) != 0;
        if ( !v17 && *(_BYTE *)(v16 + 97) != 0 )
          sub_1412D33C0(a1: v16);
      }
      else
      {
        MEMORY[0x141948990](a1: v14 - *(unsigned int *)(qword_141ABD470 + 48));
      }
    }
    sub_141750CFC(a1: v13);
  }
  v19 = v100;
  if ( v100 != 0 )
  {
    v91 = 0;
    if ( &v91 != (__int64 *)a6 )
    {
      v20 = *a6;
      if ( *a6 != nullptr )
        _InterlockedIncrement(v20 - 1);
      v91 = (__int64)v20;
    }
    (*(void (__fastcall **)(__int64, __int64 *, __int64 *, __int64 *))(*(_QWORD *)v19 + 208LL))(
      a1: v19,
      a2: &v96,
      a3: &v91,
      a4: &qword_141B59858);
    v21 = v91;
    if ( v91 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v91 - 4)) == 0 )
      sub_1412EC9A0(a1: v21 - 4);
    if ( v96 == 0 )
    {
      v32 = qword_141B5AD60;
      v95 = 0;
      v33 = sub_1412EC810(a1: 264, a2: 29);
      *(_QWORD *)v33 = 0x1D00000000LL;
      strcpy((char *)(v33 + 8), "Could not find db folder for ");
      if ( v95 != 0 )
      {
        v34 = v95 - 4;
        if ( _InterlockedDecrement((volatile signed __int32 *)(v95 - 4)) == 0 )
          sub_1412EC9A0(a1: v34);
      }
      v95 = 0;
      _InterlockedIncrement((volatile signed __int32 *)v33);
      v95 = v33 + 4;
      sub_140809550(a1: &v95, a2: &v91, a3: a6);
      LOBYTE(v35) = 1;
      (*(void (__fastcall **)(__int64, __int64 *, __int64, _QWORD))(*(_QWORD *)v32 + 120LL))(
        a1: v32,
        a2: &v91,
        a3: v35,
        a4: 0);
      v36 = v91;
      if ( v91 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v91 - 4)) == 0 )
        sub_1412EC9A0(a1: v36 - 4);
      v37 = v95;
      if ( v95 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v95 - 4)) == 0 )
        sub_1412EC9A0(a1: v37 - 4);
      LODWORD(v31) = 0;
      goto LABEL_108;
    }
    sub_14080D0E0(a1: &v94, a2: 0x1418E2C24LL);
    v93 = 0;
    if ( &v93 != (__int64 *)a4 )
    {
      v22 = *a4;
      if ( *a4 != nullptr )
        _InterlockedIncrement(v22 - 1);
      v93 = (__int64)v22;
    }
    v91 = 0x80100004E554C4CLL;
    sub_1407D0F70(
      a1: (unsigned int)&v91,
      a2: (unsigned int)&v95,
      a3: (unsigned int)&v96,
      a4: (unsigned int)&v93,
      a5: (__int64)&v94,
      a6: 1,
      a7: 0,
      0);
    v23 = v93;
    if ( v93 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v93 - 4)) == 0 )
      sub_1412EC9A0(a1: v23 - 4);
    v24 = v95;
    if ( v95 == 0 )
    {
      v38 = qword_141B5AD60;
      v94 = 0;
      v39 = sub_1412EC810(a1: 264, a2: 48);
      *(_QWORD *)v39 = 0x3000000000LL;
      strcpy((char *)(v39 + 8), "Could not load required record list for version ");
      if ( v94 != 0 )
      {
        v40 = v94 - 4;
        if ( _InterlockedDecrement((volatile signed __int32 *)(v94 - 4)) == 0 )
          sub_1412EC9A0(a1: v40);
      }
      v94 = 0;
      _InterlockedIncrement((volatile signed __int32 *)v39);
      v94 = v39 + 4;
      sub_140809550(a1: &v94, a2: &v91, a3: a6);
      LOBYTE(v41) = 1;
      (*(void (__fastcall **)(__int64, __int64 *, __int64, _QWORD))(*(_QWORD *)v38 + 120LL))(
        a1: v38,
        a2: &v91,
        a3: v41,
        a4: 0);
      v42 = v91;
      if ( v91 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v91 - 4)) == 0 )
        sub_1412EC9A0(a1: v42 - 4);
      v43 = v94;
      if ( v94 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v94 - 4)) == 0 )
        sub_1412EC9A0(a1: v43 - 4);
      LODWORD(v31) = 0;
      goto LABEL_105;
    }
    v91 = 0;
    if ( &v91 != (__int64 *)a4 )
    {
      v25 = *a4;
      if ( *a4 != nullptr )
      {
        _InterlockedIncrement(v25 - 1);
        v24 = v95;
        v91 = (__int64)v25;
        v93 = v95;
        if ( v95 == 0 )
          goto LABEL_76;
        goto LABEL_75;
      }
      v91 = 0;
    }
    v93 = v95;
LABEL_75:
    _InterlockedIncrement((volatile signed __int32 *)(v24 + 8));
LABEL_76:
    sub_1407C5A20(a1: &v94, a2: &v93, a3: &v96, a4: &v91);
    v44 = (void (__fastcall ***)(_QWORD, __int64))v93;
    if ( v93 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v93 + 8)) == 0 )
      (**v44)(a1: v44, a2: 1);
    v45 = v91;
    if ( v91 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v91 - 4)) == 0 )
      sub_1412EC9A0(a1: v45 - 4);
    v46 = (void (__fastcall ***)(_QWORD, __int64))v94;
    if ( v94 == 0 )
    {
      v52 = qword_141B5AD60;
      v91 = 0;
      v53 = sub_1412EC810(a1: 264, a2: 43);
      *(_QWORD *)v53 = 0x2B00000000LL;
      strcpy((char *)(v53 + 8), "Could not load archive for required records");
      if ( v91 != 0 )
      {
        v55 = (volatile signed __int32 *)(v91 - 4);
        if ( _InterlockedDecrement((volatile signed __int32 *)(v91 - 4)) == 0 )
          sub_1412EC9A0(a1: v55);
      }
      v91 = 0;
      _InterlockedIncrement((volatile signed __int32 *)v53);
      v91 = v53 + 4;
      LOBYTE(v54) = 1;
      (*(void (__fastcall **)(__int64, __int64 *, __int64, _QWORD))(*(_QWORD *)v52 + 120LL))(
        a1: v52,
        a2: &v91,
        a3: v54,
        a4: 0);
      v56 = v91;
      if ( v91 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v91 - 4)) == 0 )
        sub_1412EC9A0(a1: v56 - 4);
LABEL_101:
      LODWORD(v31) = 0;
LABEL_102:
      v46 = (void (__fastcall ***)(_QWORD, __int64))v94;
      if ( v94 == 0 || _InterlockedDecrement((volatile signed __int32 *)(v94 + 8)) != 0 )
      {
LABEL_105:
        v57 = (void (__fastcall ***)(_QWORD, __int64))v95;
        if ( v95 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v95 + 8)) == 0 )
          (**v57)(a1: v57, a2: 1);
LABEL_108:
        v58 = (void (__fastcall ***)(_QWORD, __int64))v96;
        if ( v96 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v96 + 8)) == 0 )
          (**v58)(a1: v58, a2: 1);
        goto LABEL_111;
      }
LABEL_104:
      (**v46)(a1: v46, a2: 1);
      goto LABEL_105;
    }
    if ( (a3 & 0x80u) != 0 )
    {
      LODWORD(v31) = 0;
      if ( _InterlockedDecrement((volatile signed __int32 *)(v94 + 8)) != 0 )
        goto LABEL_105;
      goto LABEL_104;
    }
    LODWORD(v31) = 1099836452;
    while ( 1 )
    {
      sub_1408B0DB0(a1: &v93, a2: *(_QWORD *)(v101 + 24), a3: v92, a4: a3);
      sub_14080D0E0(a1: &v97, a2: 0x1418E2C24LL);
      v98 = 0;
      v48 = v93;
      if ( v93 != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(v93 - 4));
      v98 = v48;
      LOBYTE(v90) = 0;
      sub_1407D0F70(
        a1: (unsigned int)&v91,
        a2: (unsigned int)&v99,
        a3: (unsigned int)&v94,
        a4: (unsigned int)&v98,
        a5: (__int64)&v97,
        a6: 1,
        a7: 0,
        v90,
        0x80100004E554C4CLL);
      v49 = v98;
      if ( v98 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v98 - 4)) == 0 )
        sub_1412EC9A0(a1: v49 - 4);
      v50 = v99;
      if ( v99 != 0 )
        break;
      v51 = v93;
      if ( v93 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v93 - 4)) == 0 )
        sub_1412EC9A0(a1: v51 - 4);
      if ( (char)a3-- <= 0 )
        goto LABEL_101;
    }
    _InterlockedIncrement((volatile signed __int32 *)(v99 + 8));
    v61 = a5;
    if ( a5[1] == *a5 )
    {
      LODWORD(v91) = 0;
      (*(void (__fastcall **)(__int64, __int64 *, __int64))(*(_QWORD *)v50 + 40LL))(a1: v50, a2: &v91, a3: 4);
      if ( qword_141AA7808 > (unsigned __int64)(unsigned int)v91 )
      {
        sub_1408B6B10(a1: a5);
        if ( (a5[1] - *a5) >> 2 >= (unsigned __int64)(unsigned int)v91 )
        {
          (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v50 + 40LL))(
            a1: v50,
            a2: *a5,
            a3: 4LL * (unsigned int)v91);
LABEL_164:
          LOBYTE(v31) = *(_DWORD *)(v50 + 16) == 0;
          goto LABEL_165;
        }
      }
    }
    else
    {
      LODWORD(v91) = 0;
      (*(void (__fastcall **)(__int64, __int64 *, __int64))(*(_QWORD *)v50 + 40LL))(a1: v50, a2: &v91, a3: 4);
      v62 = (unsigned int)v91;
      if ( qword_141AA7808 > (unsigned __int64)(unsigned int)v91 )
      {
        v63 = *a5;
        if ( (a5[2] - *a5) >> 2 < (unsigned __int64)(unsigned int)v91 )
        {
          v64 = a5[1];
          v65 = sub_1407E4490(a1: qword_141ABD470, a2: 4LL * (unsigned int)v91);
          sub_141758A00(a1: v65, a2: *a5, a3: a5[1] - *a5);
          v31 = (int *)*a5;
          v66 = a5;
          if ( *a5 != 0 )
          {
            v67 = a5[2] - (_QWORD)v31;
            if ( v67 == -1 )
              v67 = *(unsigned int *)((char *)v31 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v68 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v68) >> 3 > v67)
              && (v69 = *(_QWORD *)(v68 + 8 * v67)) != 0 )
            {
              v31 = (int *)((char *)v31 - *(unsigned int *)(v69 + 120));
              MEMORY[0x1419475D8](a1: v69 + 32, a2: v31);
              v70 = *(_BYTE *)(v69 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v69 + 64)) != 0;
              v66 = a5;
              if ( !v70 && *(_BYTE *)(v69 + 97) != 0 )
                sub_1412D33C0(a1: v69);
            }
            else
            {
              v31 = (int *)((char *)v31 - *(unsigned int *)(qword_141ABD470 + 48));
              MEMORY[0x141948990](a1: v31);
              v66 = a5;
            }
          }
          *v66 = v65;
          v66[1] = v65 + v64 - v63;
          v66[2] = v65 + 4 * v62;
          LODWORD(v62) = v91;
          v61 = v66;
        }
        if ( (_DWORD)v62 != 0 )
        {
          v71 = 0;
          v31 = &v97;
          do
          {
            v97 = 0;
            (*(void (__fastcall **)(__int64, int *, __int64))(*(_QWORD *)v50 + 40LL))(a1: v50, a2: &v97, a3: 4);
            if ( *(_DWORD *)(v50 + 16) != 0 )
              break;
            v72 = (_DWORD *)v61[1];
            if ( v72 == (_DWORD *)v61[2] )
            {
              v73 = (__int64)v72 - *v61;
              v74 = v73 >> 2;
              v75 = (v73 >> 2) + 1;
              v76 = (unsigned __int64)(v73 >> 2) >> 1;
              v77 = 0x3FFFFFFFFFFFFFFFLL - v76;
              v78 = (v73 >> 2) + v76;
              if ( v78 <= v75 )
                v78 = v74 + 1;
              if ( v74 > v77 )
                v78 = 0x3FFFFFFFFFFFFFFFLL;
              v79 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v78);
              *(_DWORD *)(v79 + v73) = v97;
              v80 = *v61;
              v81 = (_DWORD *)a5[1];
              sub_141758A00(a1: v79, a2: v80, a3: (char *)v72 - v80);
              v82 = v81 == v72;
              v61 = a5;
              if ( !v82 )
                sub_141758A00(a1: v79 + v73 + 4, a2: v72, a3: a5[1] - (_QWORD)v72);
              v83 = *a5;
              if ( *a5 != 0 )
              {
                v84 = a5[2] - v83;
                if ( v84 == -1 )
                  v84 = *(unsigned int *)(v83 - *(unsigned int *)(qword_141ABD470 + 48));
                if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                  && (v85 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v85) >> 3 > v84)
                  && (v86 = *(_QWORD *)(v85 + 8 * v84)) != 0 )
                {
                  MEMORY[0x1419475D8](a1: v86 + 32, a2: v83 - *(unsigned int *)(v86 + 120));
                  v87 = *(_BYTE *)(v86 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v86 + 64)) != 0;
                  if ( !v87 && *(_BYTE *)(v86 + 97) != 0 )
                    sub_1412D33C0(a1: v86);
                }
                else
                {
                  MEMORY[0x141948990](a1: v83 - *(unsigned int *)(qword_141ABD470 + 48));
                }
              }
              *a5 = v79;
              a5[1] = v79 + 4 * v75;
              a5[2] = v79 + 4 * v78;
              v31 = &v97;
            }
            else
            {
              *v72 = v97;
              v61[1] += 4;
            }
            ++v71;
          }
          while ( v71 < (unsigned int)v91 );
        }
        goto LABEL_164;
      }
    }
    LODWORD(v31) = 0;
LABEL_165:
    if ( _InterlockedDecrement((volatile signed __int32 *)(v50 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v50)(a1: v50, a2: 1);
    v88 = (void (__fastcall ***)(_QWORD, __int64))v99;
    if ( v99 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v99 + 8)) == 0 )
      (**v88)(a1: v88, a2: 1);
    v89 = v93;
    if ( v93 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v93 - 4)) == 0 )
      sub_1412EC9A0(a1: v89 - 4);
    goto LABEL_102;
  }
  v26 = qword_141B5AD60;
  v91 = 0;
  v27 = sub_1412EC810(a1: 264, a2: 27);
  *(_QWORD *)v27 = 0x1B00000000LL;
  strcpy((char *)(v27 + 8), "Could not find comps folder");
  if ( v91 != 0 )
  {
    v29 = (volatile signed __int32 *)(v91 - 4);
    if ( _InterlockedDecrement((volatile signed __int32 *)(v91 - 4)) == 0 )
      sub_1412EC9A0(a1: v29);
  }
  v91 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v27);
  v91 = v27 + 4;
  LOBYTE(v28) = 1;
  (*(void (__fastcall **)(__int64, __int64 *, __int64, _QWORD))(*(_QWORD *)v26 + 120LL))(
    a1: v26,
    a2: &v91,
    a3: v28,
    a4: 0);
  v30 = v91;
  if ( v91 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v91 - 4)) == 0 )
    sub_1412EC9A0(a1: v30 - 4);
  LODWORD(v31) = 0;
LABEL_111:
  v59 = (void (__fastcall ***)(_QWORD, __int64))v100;
  if ( v100 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v100 + 8)) == 0 )
    (**v59)(a1: v59, a2: 1);
  return (unsigned int)v31;
}
