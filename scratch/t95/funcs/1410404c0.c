__int64 __fastcall sub_1410404C0(_QWORD *a1, _QWORD *a2, __int64 a3, __int64 a4, int a5, int a6, char a7, __int64 a8)
{
  _QWORD *v9; // r13
  _QWORD *v10; // r15
  __int64 v11; // rsi
  __int64 v12; // rsi
  __int64 v13; // rdx
  __int16 v14; // ax
  __int64 v15; // rbx
  __int64 v16; // r12
  unsigned __int64 v17; // rcx
  __int64 v18; // rdi
  __int64 v19; // r14
  __int64 v20; // rsi
  unsigned __int64 v21; // rcx
  __int64 v22; // r8
  __int64 v23; // rbp
  bool v24; // al
  int v25; // r14d
  __int64 v26; // rsi
  _QWORD *v27; // rdi
  __int64 v28; // rbp
  unsigned __int64 v29; // rax
  unsigned __int64 v30; // r12
  unsigned __int64 v31; // rcx
  unsigned __int64 v32; // r12
  __int64 v33; // rsi
  _QWORD *v34; // r13
  __int64 v35; // rdi
  unsigned __int64 v36; // rcx
  __int64 v37; // r8
  __int64 v38; // rbx
  bool v39; // al
  __int64 v40; // rsi
  __int64 v41; // rdx
  int v42; // eax
  __int64 v43; // rdi
  __int64 v44; // r14
  unsigned __int64 v45; // rcx
  __int64 v46; // rbx
  __int64 v47; // rsi
  __int64 v48; // rdx
  int v49; // r14d
  __int64 v50; // rsi
  _DWORD *v51; // rdi
  __int64 v52; // rsi
  unsigned __int64 v53; // rax
  unsigned __int64 v54; // r12
  unsigned __int64 v55; // rcx
  unsigned __int64 v56; // r12
  __int64 v57; // r13
  _DWORD *v58; // rbx
  __int64 v59; // rsi
  unsigned __int64 v60; // rcx
  __int64 v61; // rdi
  __int64 v62; // rdi
  bool v63; // al
  __int64 v64; // rsi
  int v65; // edi
  __int64 v66; // rbp
  __int64 *v67; // rsi
  __int64 *v68; // r14
  __int64 v69; // rdi
  unsigned __int64 v70; // rax
  unsigned __int64 v71; // r12
  unsigned __int64 v72; // rcx
  unsigned __int64 v73; // r12
  __int64 v74; // rbx
  __int64 *v75; // rbp
  __int64 v76; // rsi
  __int64 v77; // rsi
  __int64 v78; // rsi
  __int64 v79; // rsi
  __int64 v80; // rsi
  __int64 v81; // rsi
  _QWORD *v82; // r14
  __int64 v83; // rsi
  int v84; // ebx
  __int64 v85; // rsi
  _QWORD *v86; // rsi
  __int64 v87; // rbx
  __int64 v88; // r15
  __int64 v89; // rsi
  __int64 v90; // rsi
  __int64 v91; // rsi
  __int64 v92; // rsi
  __int64 v93; // rsi
  __int64 v94; // rsi
  __int64 v95; // rsi
  __int64 v96; // rsi
  __int64 v97; // rsi
  _QWORD *v98; // r14
  int v99; // r15d
  __int64 v100; // rsi
  char v101; // bl
  __int64 v102; // rax
  __int64 v103; // rsi
  int v104; // ebx
  _QWORD *v105; // rax
  __int64 v106; // rsi
  int v107; // ebx
  _QWORD *v108; // rax
  __int64 v109; // rsi
  __int64 i; // rdi
  __int64 v112; // rsi
  __int64 v113; // rsi
  __int64 v114; // rsi
  __int64 v115; // rsi
  __int64 v116; // rsi
  __int64 v117; // rsi
  __int64 v118; // rsi
  __int64 v119; // rsi
  __int64 v120; // rsi
  __int64 v121; // rsi
  __int64 v122; // rsi
  __int64 v123; // rsi
  int v124; // [rsp+30h] [rbp-B8h]
  int v125; // [rsp+44h] [rbp-A4h] BYREF
  int v126; // [rsp+48h] [rbp-A0h] BYREF
  __int16 v127; // [rsp+4Ch] [rbp-9Ch] BYREF
  __int16 v128; // [rsp+4Eh] [rbp-9Ah] BYREF
  __int128 v129; // [rsp+50h] [rbp-98h] BYREF
  __int16 v130; // [rsp+60h] [rbp-88h]
  int v131; // [rsp+62h] [rbp-86h]
  __int16 v132; // [rsp+66h] [rbp-82h]
  int v133; // [rsp+70h] [rbp-78h] BYREF
  __int64 v134; // [rsp+74h] [rbp-74h] BYREF
  unsigned int v135; // [rsp+7Ch] [rbp-6Ch] BYREF
  int v136; // [rsp+80h] [rbp-68h] BYREF
  unsigned __int64 v137; // [rsp+88h] [rbp-60h]
  _QWORD *v138; // [rsp+90h] [rbp-58h]
  int v139; // [rsp+9Ch] [rbp-4Ch]
  __int64 v140; // [rsp+A0h] [rbp-48h]

  v9 = a2;
  v10 = a1;
  if ( a7 != 0 )
  {
    a1[36] = 0;
    v11 = *a2;
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 35, 4);
    if ( *(_DWORD *)(v11 + 16) != 0 )
      return 0;
    v128 = 0;
    v12 = *v9;
    (*(void (__fastcall **)(_QWORD, __int16 *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, &v128, 2);
    if ( *(_DWORD *)(v12 + 16) != 0 )
      return 0;
    v140 = a4;
    v14 = v128;
    v15 = v128;
    v16 = v10[37];
    v17 = (v10[39] - v16) >> 3;
    if ( v17 < v128 )
    {
      if ( v128 < 0 )
        sub_1400526C0(v17, v13);
      v18 = v10[38];
      v19 = sub_1407E4490(qword_141ABD470, 8LL * v128);
      sub_141758A00(v19, v10[37], v10[38] - v10[37]);
      v20 = v10[37];
      if ( v20 != 0 )
      {
        v21 = v10[39] - v20;
        if ( v21 == -1 )
          v21 = *(unsigned int *)(v20 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v22 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v22) >> 3 > v21)
          && (v23 = *(_QWORD *)(v22 + 8 * v21)) != 0 )
        {
          MEMORY[0x1419475D8](v23 + 32, v20 - *(unsigned int *)(v23 + 120));
          v24 = *(_BYTE *)(v23 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v23 + 64)) != 0;
          if ( !v24 && *(_BYTE *)(v23 + 97) != 0 )
            sub_1412D33C0(v23);
        }
        else
        {
          MEMORY[0x141948990](v20 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      v10[37] = v19;
      v10[38] = v19 + v18 - v16;
      v10[39] = v19 + 8 * v15;
      v14 = v128;
    }
    if ( v14 > 0 )
    {
      v25 = 0;
      v138 = v9;
      while ( 1 )
      {
        *(_QWORD *)&v129 = 0;
        v26 = *v9;
        (*(void (__fastcall **)(_QWORD, __int128 *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, &v129, 4);
        if ( *(_DWORD *)(v26 + 16) != 0 )
          return 0;
        v27 = (_QWORD *)v10[38];
        if ( v27 == (_QWORD *)v10[39] )
          break;
        *v27 = v129;
        v10[38] += 8LL;
LABEL_19:
        if ( ++v25 >= v128 )
          goto LABEL_43;
      }
      v28 = (__int64)v27 - v10[37];
      v29 = v28 >> 3;
      v30 = (unsigned __int64)(v28 >> 3) >> 1;
      v31 = 0x1FFFFFFFFFFFFFFFLL - v30;
      v32 = (v28 >> 3) + v30;
      v137 = (v28 >> 3) + 1;
      if ( v32 <= v137 )
        v32 = v29 + 1;
      if ( v29 > v31 )
        v32 = 0x1FFFFFFFFFFFFFFFLL;
      v33 = sub_1407E4490(qword_141ABD470, 8 * v32);
      *(_QWORD *)(v33 + v28) = v129;
      v34 = (_QWORD *)v10[38];
      sub_141758A00(v33, v10[37], (char *)v27 - v10[37]);
      if ( v34 != v27 )
        sub_141758A00(v33 + v28 + 8, v27, v10[38] - (_QWORD)v27);
      v35 = v10[37];
      v9 = v138;
      if ( v35 == 0 )
      {
LABEL_38:
        v10[37] = v33;
        v10[38] = v33 + 8 * v137;
        v10[39] = v33 + 8 * v32;
        goto LABEL_19;
      }
      v36 = v10[39] - v35;
      if ( v36 == -1 )
      {
        v36 = *(unsigned int *)(v35 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
LABEL_37:
          MEMORY[0x141948990](v35 - *(unsigned int *)(qword_141ABD470 + 48));
          goto LABEL_38;
        }
      }
      else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
        goto LABEL_37;
      }
      v37 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v37) >> 3 > v36 )
      {
        v38 = *(_QWORD *)(v37 + 8 * v36);
        if ( v38 != 0 )
        {
          MEMORY[0x1419475D8](v38 + 32, v35 - *(unsigned int *)(v38 + 120));
          v39 = *(_BYTE *)(v38 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v38 + 64)) != 0;
          if ( !v39 && *(_BYTE *)(v38 + 97) != 0 )
            sub_1412D33C0(v38);
          goto LABEL_38;
        }
      }
      goto LABEL_37;
    }
LABEL_43:
    v126 = 0;
    v40 = *v9;
    (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, &v126, 4);
    if ( *(_DWORD *)(v40 + 16) != 0 )
      return 0;
    v42 = v126;
    v43 = v126;
    v44 = v10[43];
    v45 = (v10[45] - v44) >> 2;
    if ( v45 < v126 )
    {
      if ( v126 < 0 )
        sub_1400526C0(v45, v41);
      v46 = v10[44];
      v47 = sub_1407E4490(qword_141ABD470, 4LL * v126);
      sub_141758A00(v47, v10[43], v10[44] - v10[43]);
      v48 = v10[43];
      if ( v48 != 0 )
        sub_1407E4890(qword_141ABD470, v48, v10[45] - v48);
      v10[43] = v47;
      v10[44] = v47 + v46 - v44;
      v10[45] = v47 + 4 * v43;
      v42 = v126;
    }
    if ( v42 > 0 )
    {
      v49 = 0;
      v138 = v9;
      do
      {
        LODWORD(v129) = 0;
        v50 = *v9;
        (*(void (__fastcall **)(_QWORD, __int128 *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, &v129, 4);
        if ( *(_DWORD *)(v50 + 16) != 0 )
          return 0;
        v51 = (_DWORD *)v10[44];
        if ( v51 == (_DWORD *)v10[45] )
        {
          v52 = (__int64)v51 - v10[43];
          v53 = v52 >> 2;
          v54 = (unsigned __int64)(v52 >> 2) >> 1;
          v55 = 0x3FFFFFFFFFFFFFFFLL - v54;
          v56 = (v52 >> 2) + v54;
          v137 = (v52 >> 2) + 1;
          if ( v56 <= v137 )
            v56 = v53 + 1;
          if ( v53 > v55 )
            v56 = 0x3FFFFFFFFFFFFFFFLL;
          v57 = sub_1407E4490(qword_141ABD470, 4 * v56);
          *(_DWORD *)(v57 + v52) = v129;
          v58 = (_DWORD *)v10[44];
          sub_141758A00(v57, v10[43], (char *)v51 - v10[43]);
          if ( v58 != v51 )
            sub_141758A00(v57 + v52 + 4, v51, v10[44] - (_QWORD)v51);
          v59 = v10[43];
          if ( v59 != 0 )
          {
            v60 = v10[45] - v59;
            if ( v60 == -1 )
              v60 = *(unsigned int *)(v59 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v61 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v61) >> 3 > v60)
              && (v62 = *(_QWORD *)(v61 + 8 * v60)) != 0 )
            {
              MEMORY[0x1419475D8](v62 + 32, v59 - *(unsigned int *)(v62 + 120));
              v63 = *(_BYTE *)(v62 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v62 + 64)) != 0;
              if ( !v63 && *(_BYTE *)(v62 + 97) != 0 )
                sub_1412D33C0(v62);
            }
            else
            {
              MEMORY[0x141948990](v59 - *(unsigned int *)(qword_141ABD470 + 48));
            }
          }
          v10[43] = v57;
          v10[44] = v57 + 4 * v137;
          v10[45] = v57 + 4 * v56;
          v9 = v138;
        }
        else
        {
          *v51 = v129;
          v10[44] += 4LL;
        }
      }
      while ( ++v49 < v126 );
    }
    v127 = 0;
    v64 = *v9;
    (*(void (__fastcall **)(_QWORD, __int16 *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, &v127, 2);
    if ( *(_DWORD *)(v64 + 16) != 0 )
      return 0;
    sub_140893BE0(v10[46], v127);
    if ( v127 > 0 )
    {
      v65 = 0;
      do
      {
        if ( dword_141B5F208 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(&dword_141B5F208);
          if ( dword_141B5F208 == -1 )
          {
            sub_1407E53D0((unsigned int)&unk_141B5F1B8, 1100133160, 128, 56, 0, 1, 128, 4096);
            sub_141751048(sub_140FC6360);
            sub_141750EA0(&dword_141B5F208);
          }
        }
        v66 = sub_1407E58C0(&unk_141B5F1B8, 56);
        *(_QWORD *)v66 = 0;
        *(_QWORD *)(v66 + 8) = 0;
        *(_QWORD *)(v66 + 16) = 0;
        *(_QWORD *)(v66 + 24) = 0;
        *(_DWORD *)(v66 + 32) = 124518401;
        *(_QWORD *)(v66 + 36) = -1;
        *(_QWORD *)(v66 + 44) = -1;
        if ( (unsigned __int8)sub_1415CFD70(v66, v9) == 0 )
          return 0;
        v67 = (__int64 *)v10[46];
        v68 = (__int64 *)v67[1];
        if ( v68 == (__int64 *)v67[2] )
        {
          v139 = v65;
          v69 = (__int64)v68 - *v67;
          v70 = v69 >> 3;
          v71 = (unsigned __int64)(v69 >> 3) >> 1;
          v72 = 0x1FFFFFFFFFFFFFFFLL - v71;
          v73 = (v69 >> 3) + v71;
          v137 = (v69 >> 3) + 1;
          if ( v73 <= v137 )
            v73 = v70 + 1;
          if ( v70 > v72 )
            v73 = 0x1FFFFFFFFFFFFFFFLL;
          v74 = sub_1407E4490(qword_141ABD470, 8 * v73);
          *(_QWORD *)(v74 + v69) = v66;
          v75 = (__int64 *)v67[1];
          sub_141758A00(v74, *v67, (char *)v68 - *v67);
          if ( v75 != v68 )
            sub_141758A00(v74 + v69 + 8, v68, v67[1] - (_QWORD)v68);
          v65 = v139;
          if ( *v67 != 0 )
            sub_1407E4890(qword_141ABD470, *v67, v67[2] - *v67);
          *v67 = v74;
          v67[1] = v74 + 8 * v137;
          v67[2] = v74 + 8 * v73;
        }
        else
        {
          *v68 = v66;
          v67[1] += 8;
        }
      }
      while ( ++v65 < v127 );
    }
    v76 = *v9;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, (__int64)v10 + 388, 4);
    if ( *(_DWORD *)(v76 + 16) != 0 )
      return 0;
    v77 = *v9;
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, v10 + 49, 4);
    if ( *(_DWORD *)(v77 + 16) != 0 )
      return 0;
    v78 = *v9;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, (__int64)v10 + 396, 4);
    if ( *(_DWORD *)(v78 + 16) != 0 )
      return 0;
    v79 = *v9;
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, v10 + 50, 4);
    if ( *(_DWORD *)(v79 + 16) != 0 )
      return 0;
    v80 = *v9;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, (__int64)v10 + 404, 4);
    if ( *(_DWORD *)(v80 + 16) != 0 )
      return 0;
    v81 = *v9;
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, v10 + 51, 4);
    if ( *(_DWORD *)(v81 + 16) != 0 )
      return 0;
    v82 = v10;
    v129 = 0;
    v130 = 0;
    v131 = -65279;
    v132 = 1900;
    v125 = 0;
    v83 = *v9;
    (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, &v125, 4);
    if ( *(_DWORD *)(v83 + 16) != 0 )
      return 0;
    sub_1410416A0(v10 + 12, v125);
    if ( v125 > 0 )
    {
      v84 = 0;
      while ( (unsigned __int8)sub_14144C6A0(&v129, v9) != 0 )
      {
        sub_140BA1B40(v10 + 12, &v129);
        if ( ++v84 >= v125 )
          goto LABEL_105;
      }
      return 0;
    }
LABEL_105:
    v135 = 0;
    v85 = *v9;
    (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, &v135, 4);
    if ( *(_DWORD *)(v85 + 16) != 0 )
      return 0;
    if ( v135 != 0 )
    {
      v86 = v10 + 27;
      v87 = 0;
      do
      {
        v133 = 0;
        v134 = 0x76C0001076C0001LL;
        v88 = *v9;
        (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, &v133, 4);
        if ( *(_DWORD *)(v88 + 16) != 0
          || (unsigned __int8)sub_140DB8980(&v134, v9) == 0
          || (unsigned __int8)sub_140DB8980((char *)&v134 + 4, v9) == 0 )
        {
          return 0;
        }
        sub_141041800(v82 + 27, &v136, *v86, &v133);
      }
      while ( ++v87 < (unsigned __int64)v135 );
    }
    sub_14104F0B0(&v133, v9, v82 + 15, &v136);
    if ( v133 != 0 )
      return 0;
    LODWORD(a4) = v140;
    v10 = v82;
  }
  v89 = *v9;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, (__int64)v10 + 459, 1);
  if ( *(_DWORD *)(v89 + 16) != 0 )
    return 0;
  v90 = *v9;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, v10 + 30, 4);
  if ( *(_DWORD *)(v90 + 16) != 0 )
    return 0;
  v91 = *v9;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, v10 + 31, 4);
  if ( *(_DWORD *)(v91 + 16) != 0 )
    return 0;
  v92 = *v9;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, v10 + 29, 4);
  if ( *(_DWORD *)(v92 + 16) != 0 )
    return 0;
  v93 = *v9;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, v10 + 32, 4);
  if ( *(_DWORD *)(v93 + 16) != 0 )
    return 0;
  v94 = *v9;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, (__int64)v10 + 460, 1);
  if ( *(_DWORD *)(v94 + 16) != 0 )
    return 0;
  v95 = *v9;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, v10 + 58, 1);
  if ( *(_DWORD *)(v95 + 16) != 0 )
    return 0;
  v96 = *v9;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, (__int64)v10 + 436, 4);
  if ( *(_DWORD *)(v96 + 16) != 0 )
    return 0;
  v97 = *v9;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, (__int64)v10 + 461, 1);
  if ( *(_DWORD *)(v97 + 16) != 0 )
    return 0;
  v98 = v10;
  v99 = a4;
  LOBYTE(v125) = 0;
  v100 = *v9;
  (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, &v125, 1);
  if ( *(_DWORD *)(v100 + 16) != 0 )
    return 0;
  sub_1410418B0(v98 + 9, (char)v125);
  if ( (char)v125 > 0 )
  {
    v101 = 0;
    do
    {
      *(_QWORD *)&v129 = 0;
      BYTE8(v129) = 100;
      if ( (unsigned __int8)sub_141060550(&v129, v9) == 0 )
        return 0;
      sub_1408C9770(v98 + 9, &v129);
    }
    while ( ++v101 < (char)v125 );
  }
  v102 = v98[9];
  if ( v98[10] - v102 == 16 )
    *(_BYTE *)(v102 + 8) = 100;
  v133 = 0;
  v103 = *v9;
  (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, &v133, 4);
  if ( *(_DWORD *)(v103 + 16) != 0 )
    return 0;
  sub_140893BE0(v98 + 21, v133);
  if ( v133 > 0 )
  {
    v104 = 0;
    do
    {
      v105 = (_QWORD *)sub_141750CC0(48);
      *v105 = 0;
      v105[1] = 0;
      v105[2] = 0;
      v105[3] = 0;
      v105[4] = 0;
      v105[5] = 0x76C0001076C0001LL;
      *(_QWORD *)&v129 = v105;
      if ( (unsigned __int8)sub_1415CFEA0(v105, v9) == 0 )
        return 0;
      sub_14087F540(v98 + 21, &v129);
    }
    while ( ++v104 < v133 );
  }
  v136 = 0;
  v106 = *v9;
  (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, &v136, 4);
  if ( *(_DWORD *)(v106 + 16) != 0 )
    return 0;
  sub_140893BE0(v98 + 18, v136);
  if ( v136 > 0 )
  {
    v107 = 0;
    do
    {
      v108 = (_QWORD *)sub_141750CC0(48);
      *v108 = 0;
      v108[1] = 0;
      v108[2] = 0;
      v108[3] = 0;
      v108[4] = 0;
      v108[5] = 0x76C0001076C0001LL;
      *(_QWORD *)&v129 = v108;
      if ( (unsigned __int8)sub_1415CFEA0(v108, v9) == 0 )
        return 0;
      sub_14087F540(v98 + 18, &v129);
    }
    while ( ++v107 < v136 );
  }
  v126 = 0;
  v109 = *v9;
  (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, &v126, 4);
  if ( *(_DWORD *)(v109 + 16) != 0 )
    return 0;
  sub_1410418B0(v98 + 24, v126);
  if ( v126 > 0 )
  {
    for ( i = 0; i < v126; sub_1410419F0(v98 + 24, &v129, i++) )
    {
      *(_QWORD *)&v129 = 0;
      *((_QWORD *)&v129 + 1) = 0x76C0001076C0001LL;
      if ( (unsigned __int8)sub_1410605B0(&v129, v9) == 0 )
        return 0;
    }
  }
  if ( a7 != 0 )
  {
    v112 = *v9;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, (__int64)v98 + 420, 4);
    if ( *(_DWORD *)(v112 + 16) != 0 )
      return 0;
    v113 = *v9;
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, v98 + 53, 4);
    if ( *(_DWORD *)(v113 + 16) != 0 )
      return 0;
    v114 = *v9;
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, v98 + 54, 4);
    if ( *(_DWORD *)(v114 + 16) != 0 )
      return 0;
    v115 = *v9;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, (__int64)v98 + 428, 4);
    if ( *(_DWORD *)(v115 + 16) != 0 )
      return 0;
    v116 = *v9;
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, v98 + 55, 4);
    if ( *(_DWORD *)(v116 + 16) != 0 )
      return 0;
    v117 = *v9;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, (__int64)v98 + 444, 4);
    if ( *(_DWORD *)(v117 + 16) != 0 )
      return 0;
    v118 = *v9;
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, v98 + 56, 4);
    if ( *(_DWORD *)(v118 + 16) != 0 )
      return 0;
    v119 = *v9;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, (__int64)v98 + 452, 4);
    if ( *(_DWORD *)(v119 + 16) != 0 )
      return 0;
    v120 = *v9;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, (__int64)v98 + 380, 4);
    if ( *(_DWORD *)(v120 + 16) != 0 )
      return 0;
    v121 = *v9;
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, v98 + 48, 4);
    if ( *(_DWORD *)(v121 + 16) != 0 )
      return 0;
    v122 = *v9;
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, v98 + 57, 2);
    if ( *(_DWORD *)(v122 + 16) != 0 )
      return 0;
    v123 = *v9;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v9 + 40LL))(*v9, (__int64)v98 + 458, 1);
    if ( *(_DWORD *)(v123 + 16) != 0 )
      return 0;
  }
  sub_141041A50(v98);
  LOBYTE(v124) = a7;
  return sub_140FAED40((_DWORD)v98, (_DWORD)v9, 0, v99, a5, a6, v124, a8);
}
