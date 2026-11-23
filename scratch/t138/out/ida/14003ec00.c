__int64 __fastcall sub_14003EC00(
        __int64 a1,
        char a2,
        __int64 a3,
        int *a4,
        _BYTE *a5,
        __int64 a6,
        _DWORD *a7,
        char a8,
        char a9,
        __int64 a10,
        __int64 a11)
{
  __int64 v14; // rdx
  int v15; // eax
  __int64 v16; // rbp
  __int64 v17; // rdx
  __int64 v18; // rsi
  volatile signed __int32 *v19; // rsi
  char v20; // bl
  char v21; // al
  __int64 v22; // r8
  __int64 v23; // rdx
  char v24; // al
  __int64 v25; // r15
  __int64 v26; // rsi
  char v27; // bl
  volatile signed __int32 *v28; // rsi
  __int128 *v29; // r14
  __int64 v30; // rdi
  volatile signed __int32 *v31; // rsi
  volatile signed __int32 *v32; // rsi
  char v33; // al
  __int64 v34; // r8
  __int64 v35; // rbp
  volatile signed __int32 *v36; // rsi
  __int64 v37; // rax
  char v38; // al
  __int64 v39; // r14
  int v40; // edi
  int v41; // r8d
  unsigned __int16 v42; // ax
  __int16 v43; // r8
  unsigned __int16 v44; // ax
  int v45; // edx
  int v46; // ebp
  unsigned __int64 v47; // rdx
  int v48; // eax
  unsigned __int64 v49; // r12
  bool v50; // cf
  char v51; // bl
  _QWORD *v52; // rax
  __int64 v53; // rsi
  __int64 v54; // rdi
  volatile signed __int32 *v55; // r13
  int v56; // ecx
  char v57; // al
  unsigned __int8 v58; // r14
  __int64 v59; // rax
  __int64 v60; // rsi
  void (__fastcall ***v61)(_QWORD, __int64); // rcx
  void (__fastcall ***v62)(_QWORD, __int64); // rcx
  _QWORD *v63; // rax
  _QWORD *v64; // rax
  __int64 v65; // rsi
  __int64 v66; // r13
  __int64 v67; // rbp
  unsigned __int64 v68; // rsi
  unsigned __int64 v69; // rbx
  unsigned __int64 v70; // rdi
  __int64 v71; // rbx
  unsigned __int64 v72; // rsi
  unsigned __int64 v73; // rdi
  unsigned __int64 v74; // rbx
  __int64 v75; // rsi
  __int64 v76; // rsi
  __int64 v77; // rsi
  __int64 v78; // rdi
  __int64 v79; // r8
  _QWORD *v80; // rax
  _QWORD *v81; // rax
  _QWORD *v82; // rax
  char v83; // al
  __int64 v84; // rdi
  __int64 v85; // r8
  char v86; // al
  _QWORD *v87; // rax
  __int64 v88; // rsi
  __int64 v89; // rbx
  int v90; // edi
  int v91; // edi
  int v92; // esi
  bool v93; // al
  _QWORD *v94; // rax
  _QWORD *v95; // rax
  __int64 v96; // rsi
  _QWORD *v97; // rax
  __int64 v98; // rsi
  __int64 v99; // rsi
  __int64 v100; // rsi
  _QWORD *v101; // rax
  __int64 v102; // rdi
  int *v103; // rdx
  __int64 v104; // rsi
  __int64 v105; // rbx
  int v106; // edi
  int v107; // edi
  int v108; // esi
  char v109; // al
  __int64 v110; // rbp
  __int64 v111; // rsi
  __int64 v112; // rdi
  __int64 v113; // r8
  volatile signed __int32 *v114; // rcx
  volatile signed __int32 *v115; // rcx
  int v117; // [rsp+20h] [rbp-218h]
  int v118; // [rsp+20h] [rbp-218h]
  int v119; // [rsp+28h] [rbp-210h]
  char v120[8]; // [rsp+40h] [rbp-1F8h] BYREF
  int v121; // [rsp+48h] [rbp-1F0h] BYREF
  __int64 v122; // [rsp+50h] [rbp-1E8h] BYREF
  int v123; // [rsp+58h] [rbp-1E0h] BYREF
  volatile signed __int32 *v124; // [rsp+60h] [rbp-1D8h] BYREF
  __int64 v125; // [rsp+68h] [rbp-1D0h]
  _QWORD v126[4]; // [rsp+70h] [rbp-1C8h] BYREF
  __int128 v127; // [rsp+90h] [rbp-1A8h] BYREF
  __int64 v128; // [rsp+A0h] [rbp-198h]
  volatile signed __int32 *v129; // [rsp+B0h] [rbp-188h] BYREF
  int v130; // [rsp+B8h] [rbp-180h] BYREF
  __int128 v131; // [rsp+C0h] [rbp-178h] BYREF
  unsigned __int64 v132; // [rsp+D0h] [rbp-168h]
  unsigned __int64 v133; // [rsp+E0h] [rbp-158h] BYREF
  _BYTE v134[12]; // [rsp+E8h] [rbp-150h] BYREF
  int v135; // [rsp+F4h] [rbp-144h]
  __int64 v136; // [rsp+F8h] [rbp-140h] BYREF
  __int64 v137; // [rsp+100h] [rbp-138h] BYREF
  char v138; // [rsp+108h] [rbp-130h]
  char v139[8]; // [rsp+110h] [rbp-128h] BYREF
  char v140[8]; // [rsp+118h] [rbp-120h] BYREF
  _BYTE v141[12]; // [rsp+120h] [rbp-118h] BYREF
  int v142; // [rsp+12Ch] [rbp-10Ch]
  __int64 v143; // [rsp+130h] [rbp-108h]
  __int64 v144; // [rsp+138h] [rbp-100h]
  unsigned __int64 v145; // [rsp+140h] [rbp-F8h]
  __int64 v146; // [rsp+148h] [rbp-F0h] BYREF
  volatile signed __int32 *v147; // [rsp+150h] [rbp-E8h] BYREF
  __int64 v148; // [rsp+158h] [rbp-E0h] BYREF
  __int64 v149; // [rsp+160h] [rbp-D8h] BYREF
  volatile signed __int32 *v150; // [rsp+168h] [rbp-D0h] BYREF
  char v151[8]; // [rsp+170h] [rbp-C8h] BYREF
  char v152[8]; // [rsp+178h] [rbp-C0h] BYREF
  volatile signed __int32 *v153; // [rsp+180h] [rbp-B8h] BYREF
  volatile signed __int32 *v154; // [rsp+188h] [rbp-B0h] BYREF
  volatile signed __int32 *v155; // [rsp+190h] [rbp-A8h] BYREF
  volatile signed __int32 *v156; // [rsp+198h] [rbp-A0h] BYREF
  volatile signed __int32 *v157; // [rsp+1A0h] [rbp-98h] BYREF
  volatile signed __int32 *v158; // [rsp+1A8h] [rbp-90h] BYREF
  _BYTE v159[16]; // [rsp+1B0h] [rbp-88h] BYREF
  _BYTE v160[16]; // [rsp+1C0h] [rbp-78h] BYREF
  _BYTE v161[16]; // [rsp+1D0h] [rbp-68h] BYREF

  v125 = qword_141ABD830;
  sub_140310A50(a1: v134);
  if ( a2 != 0 || a9 != 0 )
  {
    v14 = 0x1418FFDD7LL;
    if ( a2 != 0 )
      v14 = 0x1418DF85ELL;
    sub_140809040(a1: v134, a2: v14, a3: 0xFFFFFFFFLL);
  }
  if ( (unsigned __int8)sub_140809830(a1: a11) == 0 )
  {
    sub_140809540(a1: v134, a2: 0x141924253LL, a3: 0xFFFFFFFFLL);
    sub_140809670(a1: v134, a2: a11);
  }
  sub_14083D2C0(a1: v161);
  sub_140800D80(a1: qword_141ABDFE8, a2: &unk_141ABFDA0, a3: v161);
  if ( *(_WORD *)(a6 + 2) != MEMORY[0x1418761EE] || ((*(_WORD *)a6 ^ MEMORY[0x1418761EC]) & 0x1FF) != 0 )
    *(_DWORD *)(v125 + 1264) = *(_DWORD *)a6;
  v15 = *a4;
  v16 = v125;
  *(_DWORD *)(v125 + 1268) = v15;
  *(_DWORD *)(v16 + 1276) = *a7;
  if ( (unsigned __int8)sub_140809830(a1: a10) != 0 )
  {
    if ( a8 != 0 )
    {
      *(_BYTE *)(v16 + 1359) = 1;
    }
    else
    {
      v18 = qword_141ABDFE8;
      LOBYTE(v17) = 1;
      sub_14083D6D0(a1: v126, a2: v17);
      *(_BYTE *)(v16 + 1359) = sub_140800A10(a1: v18, a2: &unk_141ABFD88, a3: v126, a4: 0);
      sub_14083D320(a1: v126);
    }
  }
  sub_14083D2C0(a1: v160);
  if ( (unsigned __int8)sub_140800D80(a1: qword_141ABDFE8, a2: &unk_141ABFD90, a3: v160) != 0 )
    *(_BYTE *)(v16 + 1365) = sub_14083E0B0(a1: v160);
  v19 = (volatile signed __int32 *)v159;
  sub_14083D2C0(a1: v159);
  v20 = 1;
  if ( (unsigned __int8)sub_140800D80(a1: qword_141ABDFE8, a2: &unk_141ABFD98, a3: v159) != 0 )
    v20 = sub_14083E0B0(a1: v159);
  *(_BYTE *)(v16 + 1356) = 1;
  *(_BYTE *)(v16 + 1352) = 1;
  if ( (unsigned __int8)sub_140809830(a1: a10) != 0 )
  {
    if ( (unsigned __int8)sub_140098C10(a1: v16, a2: 0, a3: 0, a4: 0, a5: a3, a6: (__int64)v126, a7: 0, a8: v20) == 0 )
    {
      if ( *(_QWORD *)(v16 + 320) == *(_QWORD *)(v16 + 328) )
      {
        if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
        {
          v82 = &unk_141ABD978;
          while ( 1 )
          {
            v82 = (_QWORD *)v82[2];
            if ( v82 == nullptr || *v82 == 0 )
              break;
            if ( (*((_BYTE *)v82 + 28) & 1) == 0 || *((int *)v82 + 6) > 1 )
              goto LABEL_30;
          }
          v98 = sub_1407E2C90(a1: 2160);
          sub_1407E2EB0(a1: v98, a2: 1099914335, a3: 18746, a4: 1100015746, a5: 0, a6: 1);
          sub_1407E0010(a1: v98, a2: 0x1418DCE6FLL);
          if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v98) & 4) != 0 )
          {
            sub_1407CD750();
            LODWORD(v19) = 0;
            goto LABEL_271;
          }
        }
      }
      else
      {
        sub_14009F680(a1: v16, a2: &qword_141B59EE0);
      }
LABEL_30:
      LODWORD(v19) = 0;
      goto LABEL_271;
    }
    v21 = v126[0];
    if ( a5 != nullptr )
      *a5 = v126[0];
    if ( v21 == 0 )
    {
      LOBYTE(v19) = 1;
      goto LABEL_271;
    }
  }
  sub_140048080(a1: &v124);
  sub_140809550(a1: a3, a2: v126, a3: v134);
  sub_1407D5F40(a1: v120, a2: v126);
  sub_140808B00(a1: v126);
  if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 304LL))(a1: qword_141B5AD60) != 0 )
  {
    sub_140809550(a1: a3, a2: &v127, a3: v134);
    v22 = 0x1418DCD7ELL;
  }
  else if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 144LL))(a1: qword_141B5AD60) != 0 )
  {
    sub_140809550(a1: a3, a2: &v127, a3: v134);
    v22 = 0x1418DCDF5LL;
  }
  else
  {
    if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 136LL))(a1: qword_141B5AD60) == 0 )
      goto LABEL_34;
    sub_140809550(a1: a3, a2: &v127, a3: v134);
    v22 = 0x1418DCE18LL;
  }
  sub_1408094C0(a1: &v127, a2: &v131, a3: v22);
  sub_1407D5F40(a1: v126, a2: &v131);
  sub_140809170(a1: v120, a2: v126);
  sub_140808B00(a1: v126);
  sub_140808B00(a1: &v131);
  sub_140808B00(a1: &v127);
LABEL_34:
  if ( (unsigned __int8)sub_140809830(a1: a10) == 0 )
  {
    sub_1407D5F40(a1: v126, a2: a10);
    sub_140809170(a1: v120, a2: v126);
    sub_140808B00(a1: v126);
  }
  if ( (unsigned __int8)sub_140094670(a1: qword_141ABD830 + 8) != 0 )
  {
    v24 = 0;
    v25 = 0;
  }
  else
  {
    v26 = qword_141ABDFE8;
    LOBYTE(v23) = 1;
    sub_14083D6D0(a1: v126, a2: v23);
    v25 = 0;
    v27 = sub_140800A10(a1: v26, a2: &unk_141ABFDA8, a3: v126, a4: 0);
    sub_14083D320(a1: v126);
    if ( v27 != 0 )
    {
      sub_1407D8AB0(a1: v126, a2: 0x1418E2C24LL);
      v158 = v124;
      if ( v124 != nullptr )
      {
        _InterlockedIncrement(v124 + 2);
        v28 = v124;
      }
      else
      {
        v28 = nullptr;
      }
      LOBYTE(v119) = 1;
      LOBYTE(v117) = 1;
      sub_140097B50(a1: v16, a2: &v158, a3: v120, a4: v126, a5: v117, a6: v119);
      *(_BYTE *)(v16 + 1374) = 1;
      sub_1407D8AB0(a1: v126, a2: 0x1418E2C24LL);
      v157 = v28;
      if ( v28 != nullptr )
        _InterlockedIncrement(v28 + 2);
      v83 = sub_1400959F0(a1: v16, a2: &v157, a3: v120, a4: v126);
      *(_BYTE *)(v16 + 1374) = 0;
      if ( v83 == 0 )
      {
        v84 = qword_141B5AD60;
        v19 = (volatile signed __int32 *)sub_1400015F0(a1: v120);
        *(_QWORD *)&v131 = 0;
        sub_140809040(a1: &v131, a2: 0x141941E03LL, a3: 0xFFFFFFFFLL);
        sub_140809550(a1: &v131, a2: v126, a3: v19);
        LODWORD(v19) = 0;
        LOBYTE(v85) = 1;
        (*(void (__fastcall **)(__int64, _QWORD *, __int64, _QWORD))(*(_QWORD *)v84 + 120LL))(
          a1: v84,
          a2: v126,
          a3: v85,
          a4: 0);
        sub_140808B00(a1: v126);
        sub_140808B00(a1: &v131);
        goto LABEL_268;
      }
      v30 = 10;
      v29 = &v131;
      v24 = 1;
      LOBYTE(v25) = 1;
      goto LABEL_43;
    }
    v24 = 0;
  }
  LODWORD(v29) = 0;
  v30 = 0;
LABEL_43:
  v137 = v16;
  v138 = v24;
  v31 = v124;
  *(_QWORD *)&v131 = 0;
  sub_140809040(a1: &v131, a2: 0x1418EAAB3LL, a3: 0xFFFFFFFFLL);
  sub_1407D5F40(a1: v126, a2: &v131);
  sub_1407D2430(a1: v31, a2: &v129, a3: v126);
  sub_140808B00(a1: v126);
  sub_140808B00(a1: &v131);
  if ( qword_141ABD470 == 0 )
    qword_141ABD470 = sub_1407E4940();
  v131 = 0;
  v132 = 0;
  v123 = 124518401;
  v121 = 124518401;
  v32 = v129;
  sub_1407D8AB0(a1: v126, a2: 0x1418E2C24LL);
  sub_1407D19F0(a1: v32, a2: &v127, a3: v126, a4: 3);
  v156 = v129;
  if ( v129 != nullptr )
    _InterlockedIncrement(v129 + 2);
  v33 = sub_140048370(a1: (unsigned int)&v137, a2: (unsigned int)&v156, a3: 365, a4: (_DWORD)v29, a5: v30);
  v35 = v125;
  if ( v33 != 0 )
  {
    if ( (_BYTE)v25 == 0 )
      goto LABEL_187;
    sub_1407D8AB0(a1: v126, a2: 0x1418E2C24LL);
    v154 = v124;
    if ( v124 != nullptr )
    {
      _InterlockedIncrement(v124 + 2);
      v36 = v124;
    }
    else
    {
      v36 = nullptr;
    }
    LOBYTE(v119) = 0;
    LOBYTE(v118) = 1;
    sub_140097B50(a1: v35, a2: &v154, a3: v120, a4: v126, a5: v118, a6: v119);
    *(_BYTE *)(v35 + 1374) = 1;
    sub_1407D8AB0(a1: v126, a2: 0x1418E2C24LL);
    v153 = v36;
    if ( v36 != nullptr )
      _InterlockedIncrement(v36 + 2);
    v86 = sub_1400959F0(a1: v35, a2: &v153, a3: v120, a4: v126);
    *(_BYTE *)(v35 + 1374) = 0;
    if ( v86 != 0 )
    {
LABEL_187:
      if ( (unsigned __int8)sub_14083E0B0(a1: v161) == 0 )
      {
LABEL_219:
        v19 = v129;
        sub_1407D8AB0(a1: v126, a2: 0x1418E2C24LL);
        sub_1407D19F0(a1: v19, a2: &v127, a3: v126, a4: 3);
        LODWORD(v19) = (_DWORD)v124;
        sub_1407D8AB0(a1: v126, a2: 0x1418E2C24LL);
        sub_1407D2460(a1: (_DWORD)v19, a2: (unsigned int)&v127, a3: (unsigned int)v120, a4: (unsigned int)v126, a5: 3);
        LOBYTE(v19) = 1;
        goto LABEL_263;
      }
      if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
      {
        v87 = &unk_141ABD978;
        while ( 1 )
        {
          v87 = (_QWORD *)v87[2];
          if ( v87 == nullptr || *v87 == 0 )
            break;
          if ( (*((_BYTE *)v87 + 28) & 1) == 0 || *((int *)v87 + 6) > 1 )
            goto LABEL_215;
        }
        v96 = sub_1407E2C90(a1: 2160);
        sub_1407E2EB0(a1: v96, a2: 1099914335, a3: 18983, a4: 1100015746, a5: 0, a6: 1);
        sub_1407E0010(a1: v96, a2: 0x1418EDC63LL);
        if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v96) & 4) != 0 )
          sub_1407CD750();
      }
LABEL_215:
      sub_1407D8AB0(a1: v126, a2: 0x1418E2C24LL);
      v150 = v124;
      if ( v124 != nullptr )
        _InterlockedIncrement(v124 + 2);
      if ( (unsigned __int8)sub_1400959F0(a1: v35, a2: &v150, a3: v120, a4: v126) != 0 )
      {
        v149 = 0;
        if ( (unsigned __int8)sub_140048370(a1: (unsigned int)&v137, a2: (unsigned int)&v149, a3: 365, a4: 0, a5: 0) != 0 )
          goto LABEL_219;
        if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
        {
          v97 = &unk_141ABD978;
          while ( 1 )
          {
            v97 = (_QWORD *)v97[2];
            if ( v97 == nullptr || *v97 == 0 )
              break;
            if ( (*((_BYTE *)v97 + 28) & 1) == 0 || *((int *)v97 + 6) > 1 )
              goto LABEL_258;
          }
          v111 = sub_1407E2C90(a1: 2160);
          sub_1407E2EB0(a1: v111, a2: 1099914335, a3: 18992, a4: 1100015746, a5: 0, a6: 1);
          sub_1407E0010(a1: v111, a2: 0x141903A8ALL);
          if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v111) & 4) != 0 )
            sub_1407CD750();
        }
LABEL_258:
        v148 = 0;
        sub_140048370(a1: (unsigned int)&v137, a2: (unsigned int)&v148, a3: 365, a4: 0, a5: 0);
        sub_1407D8AB0(a1: v126, a2: 0x1418E2C24LL);
        v147 = v124;
        if ( v124 != nullptr )
          _InterlockedIncrement(v124 + 2);
        if ( (unsigned __int8)sub_1400959F0(a1: v35, a2: &v147, a3: v120, a4: v126) != 0 )
        {
          v146 = 0;
          LODWORD(v19) = 0;
          sub_140048370(a1: (unsigned int)&v137, a2: (unsigned int)&v146, a3: 365, a4: 0, a5: 0);
          goto LABEL_263;
        }
      }
    }
    v112 = qword_141B5AD60;
    v19 = (volatile signed __int32 *)sub_1400015F0(a1: v120);
    *(_QWORD *)&v127 = 0;
    sub_140809040(a1: &v127, a2: 0x141941E03LL, a3: 0xFFFFFFFFLL);
    sub_140809550(a1: &v127, a2: v126, a3: v19);
    LODWORD(v19) = 0;
    LOBYTE(v113) = 1;
    (*(void (__fastcall **)(__int64, _QWORD *, __int64, _QWORD))(*(_QWORD *)v112 + 120LL))(
      a1: v112,
      a2: v126,
      a3: v113,
      a4: 0);
    sub_140808B00(a1: v126);
    sub_140808B00(a1: &v127);
    goto LABEL_263;
  }
  v143 = v25;
  if ( (_BYTE)v25 != 0 )
  {
    v37 = sub_1400015F0(a1: v120);
    sub_1408094C0(a1: v37, a2: &v127, a3: 0x1418DD548LL);
    sub_1407D5F40(a1: v126, a2: &v127);
    nullsub_1(a1: v35 + 8, a2: v126);
    sub_140808B00(a1: v126);
    sub_140808B00(a1: &v127);
  }
  LOWORD(v34) = 1;
  sub_140DB8850(a1: &dword_141AAE084, a2: v126, a3: v34);
  *(_DWORD *)(v35 + 1268) = v126[0];
  v121 = MEMORY[0x1418761EC];
  v144 = v35 + 8;
LABEL_56:
  if ( (unsigned __int8)sub_140047E50(a1: 0) == 0 )
  {
    v38 = 1;
    if ( *((_QWORD *)&v131 + 1) == (_QWORD)v131 )
      goto LABEL_55;
    v39 = (__int64)(*((_QWORD *)&v131 + 1) - v131) >> 2;
    while ( 1 )
    {
      v40 = *(_DWORD *)(v131 + 4 * v39 - 4);
      v130 = v40;
      v41 = *(unsigned __int16 *)(v35 + 1280);
      if ( (v41 & 0x8000u) != 0 )
      {
        if ( (unsigned __int16)v41 == 0x8000 )
          v41 = 0x7FFF;
        sub_140DB8850(a1: &dword_141AAE084, a2: v126, a3: (unsigned int)-v41);
        v42 = WORD1(v126[0]);
        --v39;
        if ( WORD1(v126[0]) < HIWORD(v40) )
          goto LABEL_59;
      }
      else
      {
        v42 = HIWORD(dword_141AAE084);
        v43 = (dword_141AAE084 & 0x1FF) + ~(_WORD)v41;
        if ( v43 < 0 )
        {
          v44 = HIWORD(dword_141AAE084) - 1;
          do
          {
            v45 = v44;
            v46 = 3;
            if ( 25
               * (unsigned __int16)((((18351 * (unsigned int)v44) >> 16)
                                   + ((unsigned __int16)(v44 - ((18351 * (unsigned int)v44) >> 16)) >> 1)) >> 4) == v44 )
              v46 = 15;
            --v44;
            v43 += ((v45 & v46) == 0) + 365;
          }
          while ( v43 < 0 );
          v42 = v44 + 1;
          v35 = v125;
        }
        WORD1(v126[0]) = v42;
        LOWORD(v126[0]) = (v43 + 1) | dword_141AAE084 & 0xFE00;
        --v39;
        if ( v42 < HIWORD(v40) )
          goto LABEL_59;
      }
      if ( v42 > HIWORD(v40) || (unsigned __int16)(v40 & 0x1FF) <= (unsigned __int16)(v126[0] & 0x1FF) )
      {
        if ( (((unsigned __int16)v121 ^ (unsigned __int16)v130) & 0x1FF) == 0 && HIWORD(v121) == HIWORD(v130) )
          break;
        v142 = v130;
        v121 = v130;
        v47 = (int)sub_140DB9110(a1: &dword_141AAE084, a2: &v130) / 0xAuLL;
        v48 = 1;
        if ( (_DWORD)v47 == 0 )
          v47 = 1;
        v145 = v47;
        LOBYTE(v48) = 1;
        v135 = v48;
        v49 = 0;
        while ( 1 )
        {
          *(_DWORD *)(v35 + 1276) = MEMORY[0x1418761EC];
          sub_1407D8AB0(a1: v126, a2: 0x1418E2C24LL);
          sub_14009FA50(a1: &v127, a2: &v130);
          v155 = v129;
          if ( v129 != nullptr )
            _InterlockedIncrement(v129 + 2);
          v51 = sub_1400959F0(a1: v35, a2: &v155, a3: &v127, a4: v126);
          sub_140808B00(a1: &v127);
          if ( v51 == 0 )
            break;
          if ( (unsigned __int8)sub_140047E50(a1: 0) == 0 )
          {
            if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
            {
              v52 = &unk_141ABD978;
              while ( 1 )
              {
                v52 = (_QWORD *)v52[2];
                if ( v52 == nullptr || *v52 == 0 )
                  break;
                if ( (*((_BYTE *)v52 + 28) & 1) == 0 || *((int *)v52 + 6) > 1 )
                  goto LABEL_94;
              }
              v53 = sub_1407E2C90(a1: 2160);
              sub_1407E2EB0(a1: v53, a2: 1099914335, a3: 18897, a4: 1100015746, a5: 0, a6: 1);
              sub_14009FA50(a1: &v127, a2: &v130);
              v54 = sub_1400015F0(a1: &v127);
              v122 = 0;
              sub_140809040(a1: &v122, a2: 0x1419401CFLL, a3: 0xFFFFFFFFLL);
              sub_140809550(a1: &v122, a2: v126, a3: v54);
              sub_1407D6070(a1: v53, a2: v126);
              sub_140808B00(a1: v126);
              sub_140808B00(a1: &v122);
              sub_140808B00(a1: &v127);
              if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v53) & 4) != 0 )
                sub_1407CD750();
            }
LABEL_94:
            if ( qword_141ABD470 == 0 )
              qword_141ABD470 = sub_1407E4940();
            v127 = 0;
            v128 = 0;
            v55 = v129;
            if ( v129 != nullptr )
            {
              _InterlockedIncrement(v129 + 2);
              v56 = v137;
              v57 = v138;
              v126[0] = v55;
              _InterlockedIncrement(v55 + 2);
            }
            else
            {
              v56 = v137;
              v57 = v138;
              v126[0] = 0;
            }
            v58 = sub_14009CF00(a1: v56, a2: (unsigned int)v126, a3: v145, a4: (unsigned int)&v127, a5: 10, a6: v57);
            if ( v58 == 0 )
            {
              if ( *(_QWORD *)(v137 + 320) == *(_QWORD *)(v137 + 328) )
              {
                if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
                {
                  v64 = &unk_141ABD978;
                  while ( 1 )
                  {
                    v64 = (_QWORD *)v64[2];
                    if ( v64 == nullptr || *v64 == 0 )
                      break;
                    if ( (*((_BYTE *)v64 + 28) & 1) == 0 || *((int *)v64 + 6) > 1 )
                      goto LABEL_102;
                  }
                  v76 = sub_1407E2C90(a1: 2160);
                  sub_1407E2EB0(a1: v76, a2: 1099914335, a3: 18813, a4: 1100211792, a5: 0, a6: 1);
                  sub_1407E0010(a1: v76, a2: 0x1418DCE55LL);
                  if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v76) & 4) != 0 )
                    sub_1407CD750();
                }
              }
              else
              {
                sub_14009F680(a1: v137, a2: &qword_141B59EE0);
              }
            }
LABEL_102:
            if ( v55 != nullptr && _InterlockedDecrement(v55 + 2) == 0 )
              (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v55)(a1: v55, a2: 1);
            if ( v58 == 0 )
            {
              v59 = sub_1400015F0(a1: v120);
              sub_1408094C0(a1: v59, a2: &v122, a3: 0x1418DD548LL);
              sub_1407D5F40(a1: v126, a2: &v122);
              nullsub_1(a1: v144, a2: v126);
              sub_140808B00(a1: v126);
              sub_140808B00(a1: &v122);
              v123 = v142;
              v60 = qword_141ABD468;
              v122 = 0;
              sub_140809040(a1: &v122, a2: 0x1419282D1LL, a3: 0xFFFFFFFFLL);
              sub_140824A20(a1: v60, a2: v126, a3: &v122);
              sub_140808B00(a1: &v122);
              v133 = v49 + 1;
              sub_140828EC0(a1: &v122, a2: &v133);
              sub_14081D7C0(a1: v126, a2: 1, a3: &v122, a4: 0);
              v61 = (void (__fastcall ***)(_QWORD, __int64))v122;
              if ( v122 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v122 + 8)) == 0 )
                (**v61)(a1: v61, a2: 1);
              sub_140DAB5E0(a1: &v122, a2: &v123);
              sub_14081D7C0(a1: v126, a2: 1, a3: &v122, a4: 0);
              v62 = (void (__fastcall ***)(_QWORD, __int64))v122;
              if ( v122 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v122 + 8)) == 0 )
                (**v62)(a1: v62, a2: 1);
              if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
              {
                v63 = &unk_141ABD978;
                while ( 1 )
                {
                  v63 = (_QWORD *)v63[2];
                  if ( v63 == nullptr || *v63 == 0 )
                    break;
                  if ( (*((_BYTE *)v63 + 28) & 1) == 0 || *((int *)v63 + 6) > 1 )
                    goto LABEL_130;
                }
                v65 = sub_1407E2C90(a1: 2160);
                sub_1407E2EB0(a1: v65, a2: 1099914335, a3: 18912, a4: 1100015746, a5: 0, a6: 1);
                sub_14081ED40(a1: v126, a2: &v122, a3: 0);
                sub_1407D6070(a1: v65, a2: &v122);
                sub_140808B00(a1: &v122);
                if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v65) & 4) != 0 )
                  sub_1407CD750();
              }
LABEL_130:
              v66 = v127;
              v67 = *((_QWORD *)&v127 + 1) - v127;
              v68 = (__int64)(*((_QWORD *)&v127 + 1) - v127) >> 2;
              v69 = (__int64)(v132 - v131) >> 2;
              if ( v69 >= v68 )
              {
                v73 = (__int64)(*((_QWORD *)&v131 + 1) - v131) >> 2;
                v74 = v68 - v73;
                if ( v68 <= v73 )
                {
                  v72 = v131 + 4 * v68;
                  sub_141758A00(a1: v131, a2: v127, a3: *((_QWORD *)&v127 + 1) - v127);
                }
                else
                {
                  sub_141758A00(a1: v131, a2: v127, a3: *((_QWORD *)&v131 + 1) - v131);
                  v75 = *((_QWORD *)&v131 + 1);
                  sub_141758A00(a1: *((_QWORD *)&v131 + 1), a2: v66 + 4 * v73, a3: 4 * v74);
                  v72 = v75 + 4 * v74;
                }
              }
              else
              {
                if ( v67 < 0 )
                  sub_1400526C0();
                if ( (_QWORD)v131 != 0 )
                {
                  sub_1407E4890(a1: qword_141ABD470);
                  v131 = 0;
                  v132 = 0;
                }
                v70 = v69 + (v69 >> 1);
                if ( v70 <= v68 )
                  v70 = v68;
                if ( v69 > 0x3FFFFFFFFFFFFFFFLL - (v69 >> 1) )
                  v70 = 0x3FFFFFFFFFFFFFFFLL;
                v71 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v70);
                *(_QWORD *)&v131 = v71;
                *((_QWORD *)&v131 + 1) = v71;
                v132 = v71 + 4 * v70;
                sub_141758A00(a1: v71, a2: v66, a3: v67);
                v72 = v71 + 4 * v68;
              }
              v35 = v125;
              *((_QWORD *)&v131 + 1) = v72;
              sub_14081D040(a1: v126);
              v135 = 0;
            }
            if ( (_QWORD)v127 != 0 )
              sub_1407E4890(a1: qword_141ABD470);
            v50 = v49++ < 4;
            if ( (v50 & v58) != 0 )
              continue;
          }
          goto LABEL_148;
        }
        v77 = qword_141B5AD60;
        sub_14009FA50(a1: &v127, a2: &v130);
        v78 = sub_1400015F0(a1: &v127);
        v122 = 0;
        sub_140809040(a1: &v122, a2: 0x141941E03LL, a3: 0xFFFFFFFFLL);
        sub_140809550(a1: &v122, a2: v126, a3: v78);
        LOBYTE(v79) = 1;
        (*(void (__fastcall **)(__int64, _QWORD *, __int64, _QWORD))(*(_QWORD *)v77 + 120LL))(
          a1: v77,
          a2: v126,
          a3: v79,
          a4: 0);
        sub_140808B00(a1: v126);
        sub_140808B00(a1: &v122);
        sub_140808B00(a1: &v127);
LABEL_148:
        v38 = v135;
LABEL_55:
        if ( (v38 & 1) != 0 )
          break;
        goto LABEL_56;
      }
LABEL_59:
      if ( v39 == 0 )
      {
        v38 = 1;
        goto LABEL_55;
      }
    }
  }
  if ( HIWORD(v123) != MEMORY[0x1418761EE] || (((unsigned __int16)v123 ^ MEMORY[0x1418761EC]) & 0x1FF) != 0 )
  {
    if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
    {
      v81 = &unk_141ABD978;
      while ( 1 )
      {
        v81 = (_QWORD *)v81[2];
        if ( v81 == nullptr || *v81 == 0 )
          break;
        if ( (*((_BYTE *)v81 + 28) & 1) == 0 || *((int *)v81 + 6) > 1 )
          goto LABEL_198;
      }
      v88 = sub_1407E2C90(a1: 2160);
      sub_1407E2EB0(a1: v88, a2: 1099914335, a3: 18945, a4: 1100015746, a5: 0, a6: 1);
      sub_14009FA50(a1: &v127, a2: &v123);
      v89 = sub_1400015F0(a1: &v127);
      v122 = 0;
      sub_140809040(a1: &v122, a2: 0x1419401B4LL, a3: 0xFFFFFFFFLL);
      sub_140809550(a1: &v122, a2: v126, a3: v89);
      sub_1407D6070(a1: v88, a2: v126);
      sub_140808B00(a1: v126);
      sub_140808B00(a1: &v122);
      sub_140808B00(a1: &v127);
      if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v88) & 4) != 0 )
        sub_1407CD750();
    }
LABEL_198:
    v90 = (int)v124;
    sub_1407D8AB0(a1: v126, a2: 0x1418E2C24LL);
    sub_1407D2460(a1: v90, a2: (unsigned int)&v127, a3: (unsigned int)v120, a4: (unsigned int)v126, a5: 3);
    v91 = (int)v129;
    sub_1407D8AB0(a1: v126, a2: 0x1418E2C24LL);
    sub_1407D8AB0(a1: &v127, a2: 0x1418E2C24LL);
    sub_14009FA50(a1: &v122, a2: &v123);
    sub_1407D3AD0(
      a1: v91,
      a2: (unsigned int)&v133,
      a3: (unsigned int)&v122,
      a4: (unsigned int)&v127,
      a5: (__int64)v120,
      a6: (__int64)v126,
      a7: (__int64)&v124);
    v92 = v133;
    sub_140808B00(a1: &v122);
    v93 = (dword_141ABD994 & 1) == 0 || dword_141ABD990 >= 2;
    if ( v92 != 0 )
    {
      if ( v93 )
        goto LABEL_255;
      v94 = &unk_141ABD978;
      while ( 1 )
      {
        v94 = (_QWORD *)v94[2];
        if ( v94 == nullptr || *v94 == 0 )
          break;
        if ( (*((_BYTE *)v94 + 28) & 1) == 0 )
          goto LABEL_255;
        LODWORD(v19) = 0;
        if ( *((int *)v94 + 6) > 1 )
          goto LABEL_263;
      }
      v99 = sub_1407E2C90(a1: 2160);
      sub_1407E2EB0(a1: v99, a2: 1099914335, a3: 18954, a4: 1100015746, a5: 0, a6: 1);
LABEL_249:
      sub_1407E0010(a1: v99, a2: 0x1418F363CLL);
      goto LABEL_253;
    }
    if ( v93 )
      goto LABEL_255;
    v95 = &unk_141ABD978;
    while ( 1 )
    {
      v95 = (_QWORD *)v95[2];
      if ( v95 == nullptr || *v95 == 0 )
        break;
      if ( (*((_BYTE *)v95 + 28) & 1) == 0 )
        goto LABEL_255;
      LODWORD(v19) = 0;
      if ( *((int *)v95 + 6) > 1 )
        goto LABEL_263;
    }
    v125 = sub_1407E2C90(a1: 2160);
    sub_1407E2EB0(a1: v125, a2: 1099914335, a3: 18950, a4: 1100015746, a5: 0, a6: 1);
    (*(void (__fastcall **)(volatile signed __int32 *, __int128 *))(*(_QWORD *)v124 + 32LL))(a1: v124, a2: &v127);
    v102 = sub_1400015F0(a1: v120);
    (*(void (__fastcall **)(volatile signed __int32 *, _BYTE *))(*(_QWORD *)v129 + 32LL))(a1: v129, a2: v141);
    v103 = &v123;
LABEL_252:
    sub_14009FA50(a1: v139, a2: v103);
    v110 = sub_1400015F0(a1: v139);
    v136 = 0;
    sub_140809040(a1: &v136, a2: 0x141940788LL, a3: 0xFFFFFFFFLL);
    sub_140809550(a1: &v136, a2: v140, a3: v110);
    sub_1408094C0(a1: v140, a2: v151, a3: 0x141940331LL);
    sub_140809550(a1: v151, a2: v152, a3: v141);
    sub_1408094C0(a1: v152, a2: &v130, a3: 0x1419400E7LL);
    sub_140809550(a1: &v130, a2: &v133, a3: v102);
    sub_1408094C0(a1: &v133, a2: &v122, a3: 0x1419402FFLL);
    sub_140809550(a1: &v122, a2: v126, a3: &v127);
    v99 = v125;
    sub_1407D6070(a1: v125, a2: v126);
    sub_140808B00(a1: v126);
    sub_140808B00(a1: &v122);
    sub_140808B00(a1: &v133);
    sub_140808B00(a1: &v130);
    sub_140808B00(a1: v152);
    sub_140808B00(a1: v151);
    sub_140808B00(a1: v140);
    sub_140808B00(a1: &v136);
    sub_140808B00(a1: v139);
    sub_140808B00(a1: v141);
    sub_140808B00(a1: &v127);
LABEL_253:
    if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v99) & 4) != 0 )
      sub_1407CD750();
    goto LABEL_255;
  }
  if ( (_BYTE)v143 == 0 )
    goto LABEL_255;
  if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
  {
    v80 = &unk_141ABD978;
    while ( 1 )
    {
      v80 = (_QWORD *)v80[2];
      if ( v80 == nullptr || *v80 == 0 )
        break;
      if ( (*((_BYTE *)v80 + 28) & 1) == 0 || *((int *)v80 + 6) > 1 )
        goto LABEL_233;
    }
    v100 = sub_1407E2C90(a1: 2160);
    sub_1407E2EB0(a1: v100, a2: 1099914335, a3: 18959, a4: 1100015746, a5: 0, a6: 1);
    sub_1407E0010(a1: v100, a2: 0x141913C80LL);
    if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v100) & 4) != 0 )
      sub_1407CD750();
  }
LABEL_233:
  if ( HIWORD(v121) == MEMORY[0x1418761EE] && (((unsigned __int16)v121 ^ MEMORY[0x1418761EC]) & 0x1FF) == 0 )
    goto LABEL_255;
  if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
  {
    v101 = &unk_141ABD978;
    while ( 1 )
    {
      v101 = (_QWORD *)v101[2];
      if ( v101 == nullptr || *v101 == 0 )
        break;
      if ( (*((_BYTE *)v101 + 28) & 1) == 0 || *((int *)v101 + 6) > 1 )
        goto LABEL_246;
    }
    v104 = sub_1407E2C90(a1: 2160);
    sub_1407E2EB0(a1: v104, a2: 1099914335, a3: 18963, a4: 1100015746, a5: 0, a6: 1);
    sub_14009FA50(a1: &v127, a2: &v121);
    v105 = sub_1400015F0(a1: &v127);
    v122 = 0;
    sub_140809040(a1: &v122, a2: 0x141942293LL, a3: 0xFFFFFFFFLL);
    sub_140809550(a1: &v122, a2: v126, a3: v105);
    sub_1407D6070(a1: v104, a2: v126);
    sub_140808B00(a1: v126);
    sub_140808B00(a1: &v122);
    sub_140808B00(a1: &v127);
    if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v104) & 4) != 0 )
      sub_1407CD750();
  }
LABEL_246:
  v106 = (int)v124;
  sub_1407D8AB0(a1: v126, a2: 0x1418E2C24LL);
  sub_1407D2460(a1: v106, a2: (unsigned int)&v127, a3: (unsigned int)v120, a4: (unsigned int)v126, a5: 3);
  v107 = (int)v129;
  sub_1407D8AB0(a1: v126, a2: 0x1418E2C24LL);
  sub_1407D8AB0(a1: &v127, a2: 0x1418E2C24LL);
  sub_14009FA50(a1: &v122, a2: &v121);
  sub_1407D3AD0(
    a1: v107,
    a2: (unsigned int)&v133,
    a3: (unsigned int)&v122,
    a4: (unsigned int)&v127,
    a5: (__int64)v120,
    a6: (__int64)v126,
    a7: (__int64)&v124);
  v108 = v133;
  sub_140808B00(a1: &v122);
  v109 = sub_14000F6A0(a1: &unk_141ABD978, a2: 1);
  if ( v108 == 0 )
  {
    if ( v109 == 0 )
      goto LABEL_255;
    v125 = sub_1407E2C90(a1: 2160);
    sub_1407E2EB0(a1: v125, a2: 1099914335, a3: 18968, a4: 1100015746, a5: 0, a6: 1);
    (*(void (__fastcall **)(volatile signed __int32 *, __int128 *))(*(_QWORD *)v124 + 32LL))(a1: v124, a2: &v127);
    v102 = sub_1400015F0(a1: v120);
    (*(void (__fastcall **)(volatile signed __int32 *, _BYTE *))(*(_QWORD *)v129 + 32LL))(a1: v129, a2: v141);
    v103 = &v121;
    goto LABEL_252;
  }
  if ( v109 != 0 )
  {
    v99 = sub_1407E2C90(a1: 2160);
    sub_1407E2EB0(a1: v99, a2: 1099914335, a3: 18972, a4: 1100015746, a5: 0, a6: 1);
    goto LABEL_249;
  }
LABEL_255:
  LODWORD(v19) = 0;
LABEL_263:
  if ( (_QWORD)v131 != 0 )
    sub_1407E4890(a1: qword_141ABD470);
  v114 = v129;
  if ( v129 != nullptr && _InterlockedDecrement(v129 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v114)(a1: v114, a2: 1);
LABEL_268:
  sub_140808B00(a1: v120);
  v115 = v124;
  if ( v124 != nullptr && _InterlockedDecrement(v124 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v115)(a1: v115, a2: 1);
LABEL_271:
  sub_14083D320(a1: v159);
  sub_14083D320(a1: v160);
  sub_14083D320(a1: v161);
  sub_140808B00(a1: v134);
  return (unsigned int)v19;
}
