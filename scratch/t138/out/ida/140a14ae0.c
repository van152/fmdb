__int64 __fastcall sub_140A14AE0(__int64 *a1, int a2)
{
  __int64 v4; // rdi
  __int64 v5; // rcx
  volatile signed __int32 *v6; // rsi
  __int64 v7; // rsi
  __int64 v8; // r15
  __int64 v9; // rbx
  __int64 v10; // r12
  __int64 v11; // rdi
  unsigned __int64 v12; // rcx
  __int64 v13; // r8
  __int64 v14; // r14
  bool v15; // al
  __int64 v16; // rsi
  int v17; // r13d
  __int64 v18; // r14
  __int64 v19; // rsi
  __int64 v20; // rsi
  __int64 v21; // rsi
  __int64 v22; // rbx
  __int64 v23; // r12
  __int64 v24; // rsi
  __int64 v25; // rdi
  __int64 v26; // rdi
  __int64 v27; // rsi
  __int64 v28; // rsi
  __int64 v29; // rsi
  unsigned __int64 *v30; // r12
  __int64 v31; // rdi
  unsigned __int64 v32; // rbx
  unsigned __int64 v33; // rax
  unsigned __int64 v34; // rcx
  unsigned __int64 v35; // rax
  __int64 v36; // rsi
  __int64 v37; // rbx
  __int64 v38; // rdx
  __int64 v39; // r12
  __int64 v40; // rbx
  unsigned __int64 v41; // rcx
  __int64 v42; // r8
  __int64 v43; // rcx
  __int64 v44; // rbx
  __int64 v45; // rcx
  bool v46; // al
  __int64 v47; // rbx
  __int64 v48; // rdi
  unsigned __int64 v49; // rcx
  __int64 v50; // rbx
  __int64 v51; // rbx
  __int64 v52; // rdi
  unsigned __int64 v53; // rcx
  __int64 v54; // rbx
  __int64 v55; // rbx
  __int64 v56; // rbx
  __int64 v57; // rbx
  __int64 v58; // rsi
  __int64 v59; // rsi
  __int64 v60; // rsi
  __int64 v61; // rsi
  int v62; // ebx
  __int64 v63; // rsi
  __int64 v64; // rsi
  __int64 *v65; // r12
  __int64 *v66; // r15
  __int64 v67; // rbx
  unsigned __int64 v68; // rax
  unsigned __int64 v69; // rsi
  unsigned __int64 v70; // rcx
  unsigned __int64 v71; // rsi
  __int64 v72; // rax
  __int64 *v73; // rdi
  __int64 v74; // r14
  __int64 v75; // rdi
  unsigned __int64 v76; // rcx
  __int64 v77; // rbx
  __int64 v78; // rbx
  bool v79; // al
  __int64 *v80; // rcx
  volatile signed __int32 *v81; // rsi
  volatile signed __int32 *v82; // rcx
  __int64 *v84; // r13
  __int64 v85; // r15
  __int64 v86; // rbx
  __int64 v87; // r12
  __int64 v88; // rdi
  unsigned __int64 v89; // rcx
  __int64 v90; // r8
  __int64 v91; // r14
  bool v92; // al
  int v93; // edi
  __int64 v94; // r12
  __int64 v95; // rbx
  void (__fastcall ***v96)(_QWORD, __int64); // rcx
  __int64 *v97; // r14
  __int64 v98; // r15
  unsigned __int64 v99; // rax
  unsigned __int64 v100; // rdi
  unsigned __int64 v101; // rcx
  unsigned __int64 v102; // rdi
  __int64 v103; // rbx
  __int64 *v104; // rsi
  unsigned __int64 v105; // rcx
  __int64 v106; // r8
  __int64 v107; // r14
  bool v108; // al
  void (__fastcall ***v109)(_QWORD, __int64); // rcx
  __int64 v110; // rbx
  unsigned __int64 v111; // rcx
  __int64 v112; // r8
  __int64 v113; // r14
  bool v114; // al
  unsigned __int64 v115; // rcx
  __int64 v116; // rbx
  __int64 v117; // rbx
  bool v118; // al
  __int64 **v119; // r14
  __int64 **v120; // r15
  __int64 **v121; // rbx
  __int64 *v122; // rdi
  __int64 v123; // rsi
  unsigned __int64 v124; // rcx
  __int64 v125; // r8
  __int64 v126; // r12
  bool v127; // al
  __int64 v128; // rsi
  unsigned __int64 v129; // rcx
  __int64 v130; // r8
  __int64 v131; // r12
  bool v132; // al
  __int64 v133; // rsi
  __int64 v134; // [rsp+48h] [rbp-38h] BYREF
  __int64 v135; // [rsp+50h] [rbp-30h]
  __int64 v136; // [rsp+58h] [rbp-28h]
  volatile signed __int32 *v137; // [rsp+60h] [rbp-20h] BYREF
  unsigned __int64 v138; // [rsp+68h] [rbp-18h]
  __int64 *v139; // [rsp+70h] [rbp-10h]
  unsigned int v140; // [rsp+78h] [rbp-8h] BYREF
  unsigned int v141; // [rsp+7Ch] [rbp-4h] BYREF
  unsigned __int64 v142; // [rsp+80h] [rbp+0h] BYREF
  _QWORD v143[9]; // [rsp+88h] [rbp+8h] BYREF

  v143[1] = -2;
  v134 = 0x80100004E554C4CLL;
  sub_14080D0E0(a1: &v142, a2: 0x1418E2C24LL);
  v4 = sub_1412EC810(a1: 264, a2: 10);
  *(_QWORD *)v4 = 0xA00000000LL;
  strcpy((char *)(v4 + 8), "comp_hosts");
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v143[0] = 0;
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v143[0] = v4 + 4;
  sub_1407D0F70(
    a1: (unsigned int)&v134,
    a2: (unsigned int)&v137,
    a3: a2,
    a4: (unsigned int)v143,
    a5: (__int64)&v142,
    a6: 0,
    a7: 0,
    0);
  v5 = v143[0];
  if ( v143[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v143[0] - 4LL)) == 0 )
    sub_1412EC9A0(a1: v5 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v4) == 0 )
    sub_1412EC9A0(a1: v4);
  v6 = v137;
  if ( v137 == nullptr )
  {
    LODWORD(v16) = 1;
    return (unsigned int)v16;
  }
  dword_141AAAAE0 = WORD2(v134);
  (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)v137 + 40LL))(
    a1: v137,
    a2: &v141,
    a3: 4);
  if ( *((_DWORD *)v6 + 4) == 0 )
  {
    v7 = v141;
    v8 = *a1;
    if ( (a1[2] - *a1) >> 3 < (unsigned __int64)v141 )
    {
      v9 = a1[1];
      v10 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v141);
      sub_141758A00(a1: v10, a2: *a1, a3: a1[1] - *a1);
      v11 = *a1;
      if ( *a1 != 0 )
      {
        v12 = a1[2] - v11;
        if ( v12 == -1 )
          v12 = *(unsigned int *)(v11 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v13 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v13) >> 3 > v12)
          && (v14 = *(_QWORD *)(v13 + 8 * v12)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v14 + 32, a2: v11 - *(unsigned int *)(v14 + 120));
          v15 = *(_BYTE *)(v14 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 + 64)) != 0;
          if ( !v15 && *(_BYTE *)(v14 + 97) != 0 )
            sub_1412D33C0(a1: v14);
        }
        else
        {
          MEMORY[0x141948990](a1: v11 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      *a1 = v10;
      a1[1] = v10 + v9 - v8;
      a1[2] = v10 + 8 * v7;
      LODWORD(v7) = v141;
    }
    v139 = a1;
    if ( (_DWORD)v7 != 0 )
    {
      v17 = 0;
      while ( 1 )
      {
        v18 = sub_141750CC0(a1: 96);
        if ( qword_141ABD470 == 0 )
        {
          if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(a1: &dword_141B59AA8);
            if ( dword_141B59AA8 == -1 )
            {
              sub_1407E3E70(a1: &unk_141B59A68);
              sub_141751048(a1: sub_1407E4B20);
              sub_141750EA0(a1: &dword_141B59AA8);
            }
          }
          qword_141ABD470 = (__int64)&unk_141B59A68;
        }
        *(_QWORD *)(v18 + 72) = 0;
        *(_QWORD *)(v18 + 64) = 0;
        *(_QWORD *)(v18 + 56) = 0;
        *(_QWORD *)(v18 + 48) = 0;
        *(_QWORD *)(v18 + 40) = 0;
        *(_QWORD *)(v18 + 32) = 0;
        *(_QWORD *)(v18 + 24) = 0;
        *(_QWORD *)(v18 + 16) = 0;
        *(_QWORD *)(v18 + 8) = 0;
        *(_QWORD *)v18 = 0;
        *(_DWORD *)(v18 + 80) = 124518400;
        *(_WORD *)(v18 + 84) = 1900;
        *(_DWORD *)(v18 + 86) = 0x1000000;
        *(_BYTE *)(v18 + 90) = 0;
        v143[0] = v137;
        if ( v137 != nullptr )
          _InterlockedIncrement(v137 + 2);
        if ( (unsigned __int8)sub_140F80B80(a1: v18 + 72, a2: v143, a3: (unsigned __int8)byte_141B5FC2C ^ 1u) == 0 )
          goto LABEL_67;
        v19 = v143[0];
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v143[0] + 40LL))(a1: v143[0], a2: v18 + 80, a3: 2);
        if ( *(_DWORD *)(v19 + 16) != 0 )
          goto LABEL_67;
        v20 = v143[0];
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v143[0] + 40LL))(a1: v143[0], a2: v18 + 86, a3: 1);
        if ( *(_DWORD *)(v20 + 16) != 0 )
          goto LABEL_67;
        v21 = v143[0];
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v143[0] + 40LL))(a1: v143[0], a2: v18 + 87, a3: 1);
        if ( *(_DWORD *)(v21 + 16) != 0 )
          goto LABEL_67;
        v140 = 0;
        (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)v143[0] + 40LL))(
          a1: v143[0],
          a2: &v140,
          a3: 4);
        v22 = v140;
        if ( qword_141AA7808 <= (unsigned __int64)v140 )
          goto LABEL_67;
        v23 = *(_QWORD *)(v18 + 48);
        if ( (*(_QWORD *)(v18 + 64) - v23) >> 3 < (unsigned __int64)v140 )
        {
          v24 = *(_QWORD *)(v18 + 56);
          v25 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v140);
          sub_141758A00(a1: v25, a2: *(_QWORD *)(v18 + 48), a3: *(_QWORD *)(v18 + 56) - *(_QWORD *)(v18 + 48));
          if ( *(_QWORD *)(v18 + 48) != 0 )
            sub_1407E4890(a1: qword_141ABD470);
          *(_QWORD *)(v18 + 48) = v25;
          *(_QWORD *)(v18 + 56) = v25 + v24 - v23;
          *(_QWORD *)(v18 + 64) = v25 + 8 * v22;
          LODWORD(v22) = v140;
        }
        if ( (_DWORD)v22 != 0 )
          break;
LABEL_65:
        v47 = v143[0];
        if ( *(_DWORD *)(v143[0] + 16LL) != 0 )
          goto LABEL_68;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v143[0] + 40LL))(a1: v143[0], a2: v18 + 88, a3: 1);
        if ( *(_DWORD *)(v47 + 16) != 0 )
          goto LABEL_67;
        if ( dword_141AAAAE0 < 13 )
        {
          v57 = v143[0];
          (*(void (__fastcall **)(_QWORD, unsigned __int64 *, __int64))(*(_QWORD *)v143[0] + 40LL))(
            a1: v143[0],
            a2: &v142,
            a3: 1);
          if ( *(_DWORD *)(v57 + 16) != 0 )
            goto LABEL_67;
          *(_BYTE *)(v18 + 89) = (_BYTE)v142 != 0 ? -1 : 1;
        }
        else
        {
          v56 = v143[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v143[0] + 40LL))(
            a1: v143[0],
            a2: v18 + 89,
            a3: 1);
          if ( *(_DWORD *)(v56 + 16) != 0 )
            goto LABEL_67;
        }
        v58 = v143[0];
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v143[0] + 40LL))(a1: v143[0], a2: v18 + 90, a3: 1);
        if ( *(_DWORD *)(v58 + 16) != 0 )
          goto LABEL_67;
        v59 = v143[0];
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v143[0] + 40LL))(a1: v143[0], a2: v18 + 82, a3: 2);
        if ( *(_DWORD *)(v59 + 16) != 0 )
          goto LABEL_67;
        if ( dword_141AAAAE0 >= 12 )
        {
          v60 = v143[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v143[0] + 40LL))(
            a1: v143[0],
            a2: v18 + 84,
            a3: 2);
          if ( *(_DWORD *)(v60 + 16) != 0 )
            goto LABEL_67;
        }
        v61 = v143[0];
        (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)v143[0] + 40LL))(
          a1: v143[0],
          a2: &v140,
          a3: 4);
        if ( *(_DWORD *)(v61 + 16) != 0 )
          goto LABEL_67;
        if ( (int)v140 > 0 )
        {
          v62 = 0;
          while ( 1 )
          {
            v63 = sub_141750CC0(a1: 88);
            sub_1409FD8C0(a1: v63);
            v142 = v63;
            if ( (unsigned __int8)sub_1409FD9F0(a1: v63, a2: v143) == 0 )
              break;
            sub_14087F540(a1: v18, a2: &v142);
            if ( ++v62 >= (int)v140 )
              goto LABEL_113;
          }
          sub_1409FDF00(a1: v63);
          sub_141750CFC(a1: v63);
LABEL_67:
          v47 = v143[0];
          if ( v143[0] == 0 )
            goto LABEL_70;
LABEL_68:
          if ( _InterlockedDecrement((volatile signed __int32 *)(v47 + 8)) != 0 )
            goto LABEL_70;
LABEL_69:
          (**(void (__fastcall ***)(__int64, __int64))v47)(a1: v47, a2: 1);
          goto LABEL_70;
        }
LABEL_113:
        sub_1409FE0A0(a1: &v142, a2: v143, a3: v18 + 24);
        if ( (_DWORD)v142 != 0 )
          goto LABEL_67;
        v47 = v143[0];
        if ( *(_DWORD *)(v143[0] + 16LL) != 0 )
        {
          if ( _InterlockedDecrement((volatile signed __int32 *)(v143[0] + 8LL)) == 0 )
            goto LABEL_69;
        }
        else
        {
          v64 = *(_QWORD *)(v18 + 72);
          if ( _InterlockedDecrement((volatile signed __int32 *)(v143[0] + 8LL)) == 0 )
            (**(void (__fastcall ***)(__int64, __int64))v47)(a1: v47, a2: 1);
          if ( v64 != 0 )
          {
            v65 = (__int64 *)v139[1];
            if ( v65 == (__int64 *)v139[2] )
            {
              v66 = v139;
              v67 = (__int64)v65 - *v139;
              v68 = v67 >> 3;
              v69 = (unsigned __int64)(v67 >> 3) >> 1;
              v70 = 0x1FFFFFFFFFFFFFFFLL - v69;
              v71 = (v67 >> 3) + v69;
              v138 = (v67 >> 3) + 1;
              if ( v71 <= v138 )
                v71 = v68 + 1;
              if ( v68 > v70 )
                v71 = 0x1FFFFFFFFFFFFFFFLL;
              v72 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v71);
              *(_QWORD *)(v72 + v67) = v18;
              v73 = (__int64 *)v66[1];
              v74 = v72;
              sub_141758A00(a1: v72, a2: *v66, a3: (char *)v65 - *v66);
              if ( v73 != v65 )
                sub_141758A00(a1: v74 + v67 + 8, a2: v65, a3: v139[1] - (_QWORD)v65);
              v75 = *v139;
              if ( *v139 != 0 )
              {
                v76 = v139[2] - v75;
                if ( v76 == -1 )
                  v76 = *(unsigned int *)(v75 - *(unsigned int *)(qword_141ABD470 + 48));
                if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                  && (v77 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v77) >> 3 > v76)
                  && (v78 = *(_QWORD *)(v77 + 8 * v76)) != 0 )
                {
                  MEMORY[0x1419475D8](a1: v78 + 32, a2: v75 - *(unsigned int *)(v78 + 120));
                  v79 = *(_BYTE *)(v78 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v78 + 64)) != 0;
                  if ( !v79 && *(_BYTE *)(v78 + 97) != 0 )
                    sub_1412D33C0(a1: v78);
                }
                else
                {
                  MEMORY[0x141948990](a1: v75 - *(unsigned int *)(qword_141ABD470 + 48));
                }
              }
              v80 = v139;
              *v139 = v74;
              v80[1] = v74 + 8 * v138;
              v80[2] = v74 + 8 * v71;
            }
            else
            {
              *v65 = v18;
              v139[1] += 8;
            }
            goto LABEL_93;
          }
        }
LABEL_70:
        v48 = *(_QWORD *)(v18 + 48);
        if ( v48 != 0 )
        {
          v49 = *(_QWORD *)(v18 + 64) - v48;
          if ( v49 == -1 )
            v49 = *(unsigned int *)(v48 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v50 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v50) >> 3 > v49)
            && (v51 = *(_QWORD *)(v50 + 8 * v49)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v51 + 32, a2: v48 - *(unsigned int *)(v51 + 120));
            if ( (*(_BYTE *)(v51 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v51 + 64)) == 0)
              && *(_BYTE *)(v51 + 97) != 0 )
            {
              sub_1412D33C0(a1: v51);
            }
          }
          else
          {
            MEMORY[0x141948990](a1: v48 - *(unsigned int *)(qword_141ABD470 + 48));
          }
          *(_QWORD *)(v18 + 64) = 0;
          *(_QWORD *)(v18 + 56) = 0;
          *(_QWORD *)(v18 + 48) = 0;
        }
        sub_1409B40B0(a1: v18 + 24);
        sub_140A16420(a1: v18);
        v52 = *(_QWORD *)v18;
        if ( *(_QWORD *)v18 == 0 )
          goto LABEL_92;
        v53 = *(_QWORD *)(v18 + 16) - v52;
        if ( v53 == -1 )
        {
          v53 = *(unsigned int *)(v52 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
            goto LABEL_91;
        }
        else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
          goto LABEL_91;
        }
        v54 = *(_QWORD *)(qword_141ABD470 + 24);
        if ( (*(_QWORD *)(qword_141ABD470 + 32) - v54) >> 3 > v53 )
        {
          v55 = *(_QWORD *)(v54 + 8 * v53);
          if ( v55 != 0 )
          {
            MEMORY[0x1419475D8](a1: v55 + 32, a2: v52 - *(unsigned int *)(v55 + 120));
            if ( (*(_BYTE *)(v55 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v55 + 64)) == 0)
              && *(_BYTE *)(v55 + 97) != 0 )
            {
              sub_1412D33C0(a1: v55);
            }
            goto LABEL_92;
          }
        }
LABEL_91:
        MEMORY[0x141948990](a1: v52 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_92:
        sub_141750CFC(a1: v18);
LABEL_93:
        if ( ++v17 >= v141 )
          goto LABEL_145;
      }
      v26 = 0;
      while ( 1 )
      {
        v142 = 0xFFFFFFFF00000000uLL;
        v27 = v143[0];
        (*(void (__fastcall **)(_QWORD, unsigned __int64 *, __int64))(*(_QWORD *)v143[0] + 40LL))(
          a1: v143[0],
          a2: &v142,
          a3: 2);
        if ( *(_DWORD *)(v27 + 16) != 0 )
          goto LABEL_67;
        v28 = v143[0];
        (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)v143[0] + 40LL))(
          a1: v143[0],
          a2: (char *)&v142 + 2,
          a3: 2);
        if ( *(_DWORD *)(v28 + 16) != 0 )
          goto LABEL_67;
        v29 = v143[0];
        (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)v143[0] + 40LL))(
          a1: v143[0],
          a2: (char *)&v142 + 4,
          a3: 4);
        if ( *(_DWORD *)(v29 + 16) != 0 || *(_DWORD *)(v143[0] + 16LL) != 0 )
          goto LABEL_67;
        v30 = *(unsigned __int64 **)(v18 + 56);
        if ( v30 == *(unsigned __int64 **)(v18 + 64) )
        {
          v135 = v26;
          v31 = (__int64)v30 - *(_QWORD *)(v18 + 48);
          v32 = v31 >> 3;
          v33 = (unsigned __int64)(v31 >> 3) >> 1;
          v34 = 0x1FFFFFFFFFFFFFFFLL - v33;
          v35 = (v31 >> 3) + v33;
          v138 = (v31 >> 3) + 1;
          if ( v35 <= v138 )
            v35 = v32 + 1;
          v36 = v35;
          if ( v32 > v34 )
            v36 = 0x1FFFFFFFFFFFFFFFLL;
          v37 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v36);
          *(_QWORD *)(v37 + v31) = v142;
          v38 = *(_QWORD *)(v18 + 48);
          v136 = *(_QWORD *)(v18 + 56);
          sub_141758A00(a1: v37, a2: v38, a3: (char *)v30 - v38);
          if ( (unsigned __int64 *)v136 != v30 )
            sub_141758A00(a1: v37 + v31 + 8, a2: v30, a3: *(_QWORD *)(v18 + 56) - (_QWORD)v30);
          v39 = v37;
          v40 = *(_QWORD *)(v18 + 48);
          v26 = v135;
          if ( v40 != 0 )
          {
            v41 = *(_QWORD *)(v18 + 64) - v40;
            if ( v41 == -1 )
              v41 = *(unsigned int *)(v40 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v42 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v42) >> 3 > v41)
              && (v43 = *(_QWORD *)(v42 + 8 * v41)) != 0 )
            {
              v44 = v40 - *(unsigned int *)(v43 + 120);
              v136 = v43;
              MEMORY[0x1419475D8](a1: v43 + 32, a2: v44);
              v45 = v136;
              v46 = *(_BYTE *)(v136 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v136 + 64)) != 0;
              if ( !v46 && *(_BYTE *)(v45 + 97) != 0 )
                sub_1412D33C0(a1: v45);
            }
            else
            {
              MEMORY[0x141948990](a1: v40 - *(unsigned int *)(qword_141ABD470 + 48));
            }
          }
          *(_QWORD *)(v18 + 48) = v39;
          *(_QWORD *)(v18 + 56) = v39 + 8 * v138;
          *(_QWORD *)(v18 + 64) = v39 + 8 * v36;
        }
        else
        {
          *v30 = v142;
          *(_QWORD *)(v18 + 56) += 8LL;
        }
        if ( ++v26 >= (unsigned __int64)v140 )
          goto LABEL_65;
      }
    }
LABEL_145:
    v81 = v137;
    (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)v137 + 40LL))(
      a1: v137,
      a2: &v141,
      a3: 4);
    if ( *((_DWORD *)v81 + 4) == 0 )
    {
      v16 = v141;
      v84 = v139;
      v85 = v139[3];
      if ( (v139[5] - v85) >> 3 < (unsigned __int64)v141 )
      {
        v86 = v139[4];
        v87 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v141);
        sub_141758A00(a1: v87, a2: v84[3], a3: v84[4] - v84[3]);
        v88 = v84[3];
        if ( v88 != 0 )
        {
          v89 = v84[5] - v88;
          if ( v89 == -1 )
            v89 = *(unsigned int *)(v88 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v90 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v90) >> 3 > v89)
            && (v91 = *(_QWORD *)(v90 + 8 * v89)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v91 + 32, a2: v88 - *(unsigned int *)(v91 + 120));
            v92 = *(_BYTE *)(v91 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v91 + 64)) != 0;
            if ( !v92 && *(_BYTE *)(v91 + 97) != 0 )
              sub_1412D33C0(a1: v91);
          }
          else
          {
            MEMORY[0x141948990](a1: v88 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        v84[3] = v87;
        v84[4] = v87 + v86 - v85;
        v84[5] = v87 + 8 * v16;
        LODWORD(v16) = v141;
      }
      if ( (_DWORD)v16 == 0 )
        goto LABEL_257;
      v93 = 0;
      while ( 1 )
      {
        v94 = sub_141750CC0(a1: 72);
        if ( qword_141ABD470 == 0 )
        {
          if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(a1: &dword_141B59AA8);
            if ( dword_141B59AA8 == -1 )
            {
              sub_1407E3E70(a1: &unk_141B59A68);
              sub_141751048(a1: sub_1407E4B20);
              sub_141750EA0(a1: &dword_141B59AA8);
              v84 = v139;
            }
          }
          qword_141ABD470 = (__int64)&unk_141B59A68;
        }
        *(_QWORD *)(v94 + 16) = 0;
        *(_QWORD *)(v94 + 8) = 0;
        *(_QWORD *)v94 = 0;
        *(_WORD *)(v94 + 24) = 257;
        *(_QWORD *)(v94 + 32) = 0;
        *(_QWORD *)(v94 + 40) = 0;
        *(_QWORD *)(v94 + 48) = 0;
        *(_QWORD *)(v94 + 56) = 0;
        *(_DWORD *)(v94 + 63) = 0;
        *(_BYTE *)(v94 + 67) = -1;
        v142 = (unsigned __int64)v137;
        if ( v137 != nullptr )
          _InterlockedIncrement(v137 + 2);
        if ( (unsigned __int8)sub_1409FFF20(a1: v94, a2: &v142) == 0 )
          break;
        v16 = *(_QWORD *)v94;
        v95 = *(_QWORD *)(v94 + 8);
        v96 = (void (__fastcall ***)(_QWORD, __int64))v142;
        if ( v142 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v142 + 8)) == 0 )
          (**v96)(a1: v96, a2: 1);
        if ( v95 == v16 )
          goto LABEL_203;
        v97 = (__int64 *)v84[4];
        if ( v97 == (__int64 *)v84[5] )
        {
          LODWORD(v135) = v93;
          v98 = (__int64)v97 - v84[3];
          v99 = v98 >> 3;
          v100 = (unsigned __int64)(v98 >> 3) >> 1;
          v101 = 0x1FFFFFFFFFFFFFFFLL - v100;
          v102 = (v98 >> 3) + v100;
          v138 = (v98 >> 3) + 1;
          if ( v102 <= v138 )
            v102 = v99 + 1;
          if ( v99 > v101 )
            v102 = 0x1FFFFFFFFFFFFFFFLL;
          v103 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v102);
          *(_QWORD *)(v103 + v98) = v94;
          v104 = (__int64 *)v84[4];
          sub_141758A00(a1: v103, a2: v84[3], a3: (char *)v97 - v84[3]);
          if ( v104 != v97 )
            sub_141758A00(a1: v103 + v98 + 8, a2: v97, a3: v84[4] - (_QWORD)v97);
          v16 = v84[3];
          if ( v16 != 0 )
          {
            v105 = v84[5] - v16;
            if ( v105 == -1 )
            {
              v105 = *(unsigned int *)(v16 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
                goto LABEL_192;
            }
            else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
            {
              goto LABEL_192;
            }
            v106 = *(_QWORD *)(qword_141ABD470 + 24);
            if ( (*(_QWORD *)(qword_141ABD470 + 32) - v106) >> 3 > v105 && (v107 = *(_QWORD *)(v106 + 8 * v105)) != 0 )
            {
              v16 -= *(unsigned int *)(v107 + 120);
              MEMORY[0x1419475D8](a1: v107 + 32, a2: v16);
              v108 = *(_BYTE *)(v107 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v107 + 64)) != 0;
              v84 = v139;
              if ( !v108 && *(_BYTE *)(v107 + 97) != 0 )
                sub_1412D33C0(a1: v107);
            }
            else
            {
LABEL_192:
              v16 -= *(unsigned int *)(qword_141ABD470 + 48);
              MEMORY[0x141948990](a1: v16);
              v84 = v139;
            }
          }
          v84[3] = v103;
          v84[4] = v103 + 8 * v138;
          v84[5] = v103 + 8 * v102;
          v93 = v135;
          goto LABEL_165;
        }
        *v97 = v94;
        v84[4] += 8;
LABEL_165:
        if ( ++v93 >= v141 )
          goto LABEL_257;
      }
      v109 = (void (__fastcall ***)(_QWORD, __int64))v142;
      if ( v142 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v142 + 8)) == 0 )
        (**v109)(a1: v109, a2: 1);
LABEL_203:
      v110 = *(_QWORD *)(v94 + 32);
      if ( v110 != 0 )
      {
        v111 = *(_QWORD *)(v94 + 48) - v110;
        if ( v111 == -1 )
          v111 = *(unsigned int *)(v110 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v112 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v112) >> 3 > v111)
          && (v113 = *(_QWORD *)(v112 + 8 * v111)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v113 + 32, a2: v110 - *(unsigned int *)(v113 + 120));
          v114 = *(_BYTE *)(v113 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v113 + 64)) != 0;
          if ( !v114 && *(_BYTE *)(v113 + 97) != 0 )
            sub_1412D33C0(a1: v113);
        }
        else
        {
          MEMORY[0x141948990](a1: v110 - *(unsigned int *)(qword_141ABD470 + 48));
        }
        *(_QWORD *)(v94 + 48) = 0;
        *(_QWORD *)(v94 + 40) = 0;
        *(_QWORD *)(v94 + 32) = 0;
      }
      v16 = *(_QWORD *)v94;
      if ( *(_QWORD *)v94 != 0 )
      {
        v115 = *(_QWORD *)(v94 + 16) - v16;
        if ( v115 == -1 )
          v115 = *(unsigned int *)(v16 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v116 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v116) >> 3 > v115)
          && (v117 = *(_QWORD *)(v116 + 8 * v115)) != 0 )
        {
          v16 -= *(unsigned int *)(v117 + 120);
          MEMORY[0x1419475D8](a1: v117 + 32, a2: v16);
          v118 = *(_BYTE *)(v117 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v117 + 64)) != 0;
          if ( !v118 && *(_BYTE *)(v117 + 97) != 0 )
            sub_1412D33C0(a1: v117);
        }
        else
        {
          v16 -= *(unsigned int *)(qword_141ABD470 + 48);
          MEMORY[0x141948990](a1: v16);
        }
        *(_QWORD *)(v94 + 16) = 0;
        *(_QWORD *)(v94 + 8) = 0;
        *(_QWORD *)v94 = 0;
      }
      sub_141750CFC(a1: v94);
      v119 = (__int64 **)v84[3];
      v120 = (__int64 **)v84[4];
      if ( v119 != v120 )
      {
        v121 = (__int64 **)v84[3];
        do
        {
          v122 = *v121;
          if ( *v121 != nullptr )
          {
            v123 = v122[4];
            if ( v123 != 0 )
            {
              v124 = v122[6] - v123;
              if ( v124 == -1 )
                v124 = *(unsigned int *)(v123 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v125 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v125) >> 3 > v124)
                && (v126 = *(_QWORD *)(v125 + 8 * v124)) != 0 )
              {
                MEMORY[0x1419475D8](a1: v126 + 32, a2: v123 - *(unsigned int *)(v126 + 120));
                v127 = *(_BYTE *)(v126 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v126 + 64)) != 0;
                if ( !v127 && *(_BYTE *)(v126 + 97) != 0 )
                  sub_1412D33C0(a1: v126);
              }
              else
              {
                MEMORY[0x141948990](a1: v123 - *(unsigned int *)(qword_141ABD470 + 48));
              }
              v122[6] = 0;
              v122[5] = 0;
              v122[4] = 0;
              v84 = v139;
            }
            v128 = *v122;
            if ( *v122 != 0 )
            {
              v129 = v122[2] - v128;
              if ( v129 == -1 )
                v129 = *(unsigned int *)(v128 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v130 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v130) >> 3 > v129)
                && (v131 = *(_QWORD *)(v130 + 8 * v129)) != 0 )
              {
                MEMORY[0x1419475D8](a1: v131 + 32, a2: v128 - *(unsigned int *)(v131 + 120));
                v132 = *(_BYTE *)(v131 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v131 + 64)) != 0;
                if ( !v132 && *(_BYTE *)(v131 + 97) != 0 )
                  sub_1412D33C0(a1: v131);
              }
              else
              {
                MEMORY[0x141948990](a1: v128 - *(unsigned int *)(qword_141ABD470 + 48));
              }
            }
            sub_141750CFC(a1: v122);
          }
          ++v121;
        }
        while ( v121 != v120 );
        v133 = v84[4] - (_QWORD)v120;
        sub_141758A00(a1: v119, a2: v120, a3: v133);
        v16 = (__int64)v119 + v133;
        v84[4] = v16;
      }
      sub_140A011F0(a1: v84);
LABEL_257:
      dword_141AAAAE0 = 13;
      LOBYTE(v16) = 1;
LABEL_147:
      v82 = v137;
      if ( v137 != nullptr && _InterlockedDecrement(v137 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v82)(a1: v82, a2: 1);
      return (unsigned int)v16;
    }
  }
  LODWORD(v16) = 0;
  goto LABEL_147;
}
